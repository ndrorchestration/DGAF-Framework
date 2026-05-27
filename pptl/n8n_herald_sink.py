"""
n8n_herald_sink.py — Production N8nHeraldSink for live dashboard wiring.

Features vs basic N8nWebhookSink:
  - Event batching (configurable batch_size + flush_interval)
  - Exponential backoff retry (max 3 attempts)
  - HMAC-SHA256 request signature (X-Herald-Signature header)
  - Dead-letter JSONL fallback on permanent failure
  - Thread-safe flush via threading.Lock
  - dry_run mode for CI/testing (no HTTP, events logged to stdout)

Usage:
    from pptl.n8n_herald_sink import N8nHeraldSink
    import os

    sink = N8nHeraldSink(
        webhook_url = os.environ["HERALD_N8N_WEBHOOK_URL"],
        hmac_secret = os.environ.get("HERALD_N8N_HMAC_SECRET", ""),
        batch_size  = 20,
        dry_run     = False,
    )
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import threading
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEAD_LETTER_PATH = Path("output/herald_dead_letter.jsonl")
_DEAD_LETTER_PATH.parent.mkdir(parents=True, exist_ok=True)


class N8nHeraldSink:
    """
    Production Herald sink: batched HTTP POST to n8n webhook with
    HMAC signing, retry backoff, and dead-letter fallback.
    """

    MAX_RETRIES    = 3
    RETRY_BASE_S   = 0.5      # exponential base: 0.5s, 1.0s, 2.0s
    FLUSH_INTERVAL = 10.0     # seconds between auto-flush if batch not full

    def __init__(
        self,
        webhook_url: str,
        hmac_secret: str = "",
        batch_size:  int = 20,
        dry_run:     bool = True,
    ) -> None:
        self.webhook_url = webhook_url
        self.hmac_secret = hmac_secret.encode() if hmac_secret else b""
        self.batch_size  = batch_size
        self.dry_run     = dry_run

        self._batch: list[dict[str, Any]] = []
        self._lock  = threading.Lock()
        self._last_flush = time.monotonic()

    # ── Sink protocol ──────────────────────────────────────────────────

    def write(self, event: dict[str, Any]) -> None:
        """Buffer event; flush when batch_size reached or interval elapsed."""
        with self._lock:
            self._batch.append(event)
            age = time.monotonic() - self._last_flush
            if len(self._batch) >= self.batch_size or age >= self.FLUSH_INTERVAL:
                self._flush_locked()

    def close(self) -> None:
        """Flush remaining buffered events and release resources."""
        with self._lock:
            if self._batch:
                self._flush_locked()

    # ── Internal ────────────────────────────────────────────────────────────

    def _flush_locked(self) -> None:
        """Must be called with self._lock held."""
        batch = self._batch[:]
        self._batch.clear()
        self._last_flush = time.monotonic()
        # Release lock before I/O so writes aren't blocked during HTTP
        self._lock.release()
        try:
            self._send_with_retry(batch)
        finally:
            self._lock.acquire()

    def _send_with_retry(self, batch: list[dict[str, Any]]) -> None:
        """POST batch to webhook with exponential backoff retry."""
        payload = json.dumps({"events": batch}, default=str).encode()
        headers = {"Content-Type": "application/json"}

        if self.hmac_secret:
            sig = hmac.new(self.hmac_secret, payload, hashlib.sha256).hexdigest()
            headers["X-Herald-Signature"] = f"sha256={sig}"

        if self.dry_run:
            logger.info("[N8nHeraldSink dry_run] batch=%d events", len(batch))
            return

        import urllib.request
        import urllib.error

        last_exc: Exception | None = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                req = urllib.request.Request(
                    self.webhook_url,
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    if resp.status < 300:
                        logger.debug(
                            "[N8nHeraldSink] flushed %d events (attempt %d)",
                            len(batch), attempt,
                        )
                        return
                    raise RuntimeError(f"HTTP {resp.status}")
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                wait = self.RETRY_BASE_S * (2 ** (attempt - 1))
                logger.warning(
                    "[N8nHeraldSink] attempt %d failed: %s — retrying in %.1fs",
                    attempt, exc, wait,
                )
                time.sleep(wait)

        # Permanent failure — write to dead-letter
        logger.error(
            "[N8nHeraldSink] permanent failure after %d attempts: %s",
            self.MAX_RETRIES, last_exc,
        )
        self._write_dead_letter(batch)

    @staticmethod
    def _write_dead_letter(batch: list[dict[str, Any]]) -> None:
        """Append failed events to dead-letter JSONL. Never raises."""
        try:
            with _DEAD_LETTER_PATH.open("a", encoding="utf-8") as fh:
                for event in batch:
                    fh.write(json.dumps(event, default=str) + "\n")
            logger.warning(
                "[N8nHeraldSink] %d events written to dead-letter: %s",
                len(batch), _DEAD_LETTER_PATH,
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("[N8nHeraldSink] dead-letter write failed: %s", exc)
