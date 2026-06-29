"""
ahg_herald_trace.py — P-01 Herald Fan-Out Trace Sink — AHG Integration (v1.5)
Pattern: P-42 — Adaptive Harmonic Governance, Layer 12 — Cognitive Control Plane
Version: 1.5
Authors: Amethyst × COLLEEN | 2026-06-29

Responsibilities:
  - Receive PhaseIntent events from AHGSidecar via wire_herald_trace()
  - Route to P-01 Herald Fan-Out Trace Sink for audit archival
  - Provide structured trace records for COLLEEN episode archival
  - v1.5: Live P-01 HTTP push enabled via HeraldHTTPSink
    Falls back to local JSONL if Herald endpoint not configured.

Version history:
  v1.3: wire_herald_trace() stub in AHGSidecar
  v1.4: In-memory + JSONL file sink, NDR-STASIS + Tribunal alerts
  v1.5: Live P-01 HTTP push (HeraldHTTPSink), circuit breaker, retry backoff,
        configurable via env vars or HeraldSinkConfig dataclass

Environment variables (v1.5 HTTP push):
  AHG_HERALD_ENDPOINT    — HTTP(S) URL for P-01 Fan-Out endpoint
                           e.g. https://herald.internal/api/v1/ahg/trace
                           If unset: falls back to JSONL-only mode.
  AHG_HERALD_API_KEY     — Bearer token for Herald endpoint auth (optional)
  AHG_HERALD_TIMEOUT     — Request timeout in seconds (default: 2.0)
  AHG_HERALD_MAX_RETRIES — Max retry attempts per push (default: 3)
  AHG_HERALD_BATCH_SIZE  — Batch size for buffered push (default: 10)

Usage (minimal):
    from components.ahg_herald_trace import AHGHeraldTrace
    from components.ahg_sidecar import AHGSidecar
    from components.ahg_conductor import AHGConductor

    conductor = AHGConductor()
    trace = AHGHeraldTrace(session_id="S077", output_dir=Path("logs/ahg"))
    sidecar = AHGSidecar(conductor=conductor)
    sidecar.wire_herald_trace(trace.on_intent)
    # PhaseIntent events now route: in-memory → JSONL → P-01 HTTP (if configured)

Usage (explicit HTTP config):
    from components.ahg_herald_trace import AHGHeraldTrace, HeraldSinkConfig
    config = HeraldSinkConfig(
        endpoint="https://herald.internal/api/v1/ahg/trace",
        api_key="Bearer sk-...",
        timeout=2.0,
        max_retries=3,
        batch_size=10,
    )
    trace = AHGHeraldTrace(session_id="S077", sink_config=config)
"""

from __future__ import annotations

import json
import logging
import os
import time
import threading
import datetime
import urllib.request
import urllib.error
from collections import deque
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Deque, List, Optional

logger = logging.getLogger("ahg.herald_trace")

# Guard: PhaseIntent import is optional (P-42 v1.3+ required)
try:
    from components.ahg_conductor import PhaseIntent
    _CONDUCTOR_AVAILABLE = True
except ImportError:
    _CONDUCTOR_AVAILABLE = False
    PhaseIntent = None  # type: ignore


# ---------------------------------------------------------------------------
# Herald Sink Configuration
# ---------------------------------------------------------------------------

@dataclass
class HeraldSinkConfig:
    """Configuration for P-01 Herald HTTP push sink.
    Can be constructed explicitly or loaded from environment variables.
    """
    endpoint: Optional[str] = None        # AHG_HERALD_ENDPOINT
    api_key: Optional[str] = None         # AHG_HERALD_API_KEY (Bearer token)
    timeout: float = 2.0                  # AHG_HERALD_TIMEOUT
    max_retries: int = 3                  # AHG_HERALD_MAX_RETRIES
    batch_size: int = 10                  # AHG_HERALD_BATCH_SIZE
    retry_backoff_base: float = 0.25      # seconds — exponential backoff base
    circuit_breaker_threshold: int = 5    # consecutive failures before open
    circuit_breaker_reset_sec: float = 60.0

    @classmethod
    def from_env(cls) -> "HeraldSinkConfig":
        """Load config from AHG_HERALD_* environment variables."""
        return cls(
            endpoint=os.environ.get("AHG_HERALD_ENDPOINT"),
            api_key=os.environ.get("AHG_HERALD_API_KEY"),
            timeout=float(os.environ.get("AHG_HERALD_TIMEOUT", "2.0")),
            max_retries=int(os.environ.get("AHG_HERALD_MAX_RETRIES", "3")),
            batch_size=int(os.environ.get("AHG_HERALD_BATCH_SIZE", "10")),
        )

    @property
    def enabled(self) -> bool:
        return bool(self.endpoint)


# ---------------------------------------------------------------------------
# HTTP Push Sink (v1.5)
# ---------------------------------------------------------------------------

class HeraldHTTPSink:
    """Non-blocking HTTP push sink to P-01 Herald Fan-Out endpoint.

    Features:
    - Background thread for batched push (never blocks on_intent())
    - Exponential backoff retry on transient failures
    - Circuit breaker: opens after N consecutive failures, auto-resets
    - Falls back gracefully to JSONL-only on permanent failure
    """

    def __init__(self, config: HeraldSinkConfig):
        self.config = config
        self._queue: Deque[dict] = deque(maxlen=5000)
        self._consecutive_failures = 0
        self._circuit_open = False
        self._circuit_opened_at: Optional[float] = None
        self._total_pushed = 0
        self._total_failed = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._worker, daemon=True, name="ahg-herald-http-sink"
        )
        self._thread.start()
        logger.info(
            f"[HeraldHTTPSink] Started — endpoint={config.endpoint} "
            f"batch={config.batch_size} timeout={config.timeout}s "
            f"retries={config.max_retries}"
        )

    def enqueue(self, record_dict: dict) -> None:
        """Enqueue a trace record for async push. Never blocks."""
        self._queue.append(record_dict)

    def stop(self, timeout: float = 5.0) -> None:
        """Graceful shutdown — flush remaining queue."""
        self._stop_event.set()
        self._thread.join(timeout=timeout)

    def _check_circuit(self) -> bool:
        """Returns True if circuit is closed (pushes allowed)."""
        if not self._circuit_open:
            return True
        elapsed = time.monotonic() - (self._circuit_opened_at or 0)
        if elapsed >= self.config.circuit_breaker_reset_sec:
            logger.info("[HeraldHTTPSink] Circuit breaker RESET — attempting reconnect")
            with self._lock:
                self._circuit_open = False
                self._consecutive_failures = 0
            return True
        return False

    def _push_batch(self, batch: List[dict]) -> bool:
        """Push a batch to Herald endpoint. Returns True on success."""
        if not self._check_circuit():
            logger.debug("[HeraldHTTPSink] Circuit open — skipping push")
            return False

        payload = json.dumps({"records": batch, "count": len(batch)}).encode()
        headers = {
            "Content-Type": "application/json",
            "X-AHG-Session": batch[0].get("session_id", "unknown"),
            "X-AHG-Turn": str(batch[-1].get("turn_id", 0)),
        }
        if self.config.api_key:
            headers["Authorization"] = (
                self.config.api_key if self.config.api_key.startswith("Bearer ")
                else f"Bearer {self.config.api_key}"
            )

        for attempt in range(self.config.max_retries):
            try:
                req = urllib.request.Request(
                    self.config.endpoint,
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                    if resp.status in (200, 201, 202, 204):
                        with self._lock:
                            self._consecutive_failures = 0
                            self._total_pushed += len(batch)
                        logger.debug(
                            f"[HeraldHTTPSink] Pushed {len(batch)} records "
                            f"→ HTTP {resp.status}"
                        )
                        return True
                    else:
                        logger.warning(
                            f"[HeraldHTTPSink] Unexpected status {resp.status} "
                            f"on attempt {attempt + 1}"
                        )
            except (urllib.error.URLError, OSError, TimeoutError) as exc:
                backoff = self.config.retry_backoff_base * (2 ** attempt)
                logger.warning(
                    f"[HeraldHTTPSink] Push failed (attempt {attempt + 1}/{self.config.max_retries}): "
                    f"{exc} — backoff {backoff:.2f}s"
                )
                if attempt < self.config.max_retries - 1:
                    time.sleep(backoff)

        # All retries exhausted
        with self._lock:
            self._consecutive_failures += 1
            self._total_failed += len(batch)
            if self._consecutive_failures >= self.config.circuit_breaker_threshold:
                self._circuit_open = True
                self._circuit_opened_at = time.monotonic()
                logger.error(
                    f"[HeraldHTTPSink] Circuit breaker OPEN after "
                    f"{self._consecutive_failures} consecutive failures. "
                    f"Will retry after {self.config.circuit_breaker_reset_sec}s."
                )
        return False

    def _worker(self) -> None:
        """Background push worker — batches queue and flushes to Herald."""
        while not self._stop_event.is_set():
            if len(self._queue) >= self.config.batch_size:
                batch = []
                while self._queue and len(batch) < self.config.batch_size:
                    batch.append(self._queue.popleft())
                if batch:
                    self._push_batch(batch)
            else:
                time.sleep(0.05)  # 50ms poll interval

        # Drain remaining queue on shutdown
        remaining = list(self._queue)
        if remaining:
            logger.info(f"[HeraldHTTPSink] Draining {len(remaining)} remaining records on shutdown")
            for i in range(0, len(remaining), self.config.batch_size):
                self._push_batch(remaining[i:i + self.config.batch_size])

    @property
    def stats(self) -> dict:
        return {
            "queued": len(self._queue),
            "total_pushed": self._total_pushed,
            "total_failed": self._total_failed,
            "circuit_open": self._circuit_open,
            "consecutive_failures": self._consecutive_failures,
        }


# ---------------------------------------------------------------------------
# Trace Record
# ---------------------------------------------------------------------------

@dataclass
class AHGTraceRecord:
    """Structured trace record for one PhaseIntent event.
    COLLEEN-archivable. Routes to P-01 Herald Fan-Out via HeraldHTTPSink.
    """
    record_id:         str
    session_id:        str
    turn_id:           int
    timestamp_utc:     str
    archetype:         str
    regime:            str
    phi:               float
    v_phi:             float
    a_phi:             float
    tribunal_active:   bool
    ttl:               int
    message:           str
    phase_exploration: Optional[float] = None
    phase_dissent:     Optional[float] = None
    phase_uncertainty: Optional[float] = None
    ndr_stasis_delta:  Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ---------------------------------------------------------------------------
# Herald Trace (main entry point)
# ---------------------------------------------------------------------------

class AHGHeraldTrace:
    """P-01 Herald Fan-Out Trace Sink for AHG PhaseIntent events.

    Routes each PhaseIntent to:
      1. In-memory rolling buffer (always)
      2. JSONL file sink (if output_dir provided)
      3. P-01 Herald HTTP endpoint (v1.5 — if AHG_HERALD_ENDPOINT set or
         sink_config.endpoint provided)

    Alerts:
      - WARNING log on every Tribunal activation
      - INFO log when phi is within ndr_stasis_tolerance of φ = 1.6180339...

    Usage:
        trace = AHGHeraldTrace(session_id="S077", output_dir=Path("logs/ahg"))
        sidecar.wire_herald_trace(trace.on_intent)
    """

    NDR_STASIS_PHI = 1.6180339887498949

    def __init__(
        self,
        session_id: str = "unknown",
        output_dir: Optional[Path] = None,
        sink_config: Optional[HeraldSinkConfig] = None,
        max_memory_records: int = 10_000,
        emit_tribunal_alerts: bool = True,
        emit_ndr_stasis_alerts: bool = True,
        ndr_stasis_tolerance: float = 0.02,
    ):
        self.session_id = session_id
        self.output_dir = Path(output_dir) if output_dir else None
        self.max_memory_records = max_memory_records
        self.emit_tribunal_alerts = emit_tribunal_alerts
        self.emit_ndr_stasis_alerts = emit_ndr_stasis_alerts
        self.ndr_stasis_tolerance = ndr_stasis_tolerance

        self._records: list[AHGTraceRecord] = []
        self._jsonl_path: Optional[Path] = None
        self._http_sink: Optional[HeraldHTTPSink] = None

        # File sink
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            fname = (
                f"ahg_trace_{session_id}_"
                f"{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
            )
            self._jsonl_path = self.output_dir / fname
            logger.info(f"[AHGHeraldTrace] JSONL trace file: {self._jsonl_path}")

        # HTTP sink (v1.5) — explicit config takes priority, then env vars
        resolved_config = sink_config or HeraldSinkConfig.from_env()
        if resolved_config.enabled:
            self._http_sink = HeraldHTTPSink(resolved_config)
            logger.info(
                f"[AHGHeraldTrace] P-01 HTTP push ENABLED → {resolved_config.endpoint}"
            )
        else:
            logger.info(
                "[AHGHeraldTrace] P-01 HTTP push DISABLED "
                "(set AHG_HERALD_ENDPOINT to enable)"
            )

        logger.info(
            f"[AHGHeraldTrace] v1.5 ready — session={session_id} "
            f"jsonl={'on' if self._jsonl_path else 'off'} "
            f"http={'on' if self._http_sink else 'off'}"
        )

    # ------------------------------------------------------------------
    # Primary callback — wired via AHGSidecar.wire_herald_trace()
    # ------------------------------------------------------------------

    def on_intent(self, intent) -> None:
        """Receive a PhaseIntent and route to all configured sinks.
        This is the callback provided to AHGSidecar.wire_herald_trace().
        Never raises — all sink errors are logged and swallowed.
        """
        if not _CONDUCTOR_AVAILABLE:
            logger.warning("[AHGHeraldTrace] ahg_conductor not available — skipping trace")
            return

        ndr_delta = abs(intent.phi - self.NDR_STASIS_PHI)

        record = AHGTraceRecord(
            record_id=f"{self.session_id}-T{intent.turn_id}-{intent.archetype.value}",
            session_id=self.session_id,
            turn_id=intent.turn_id,
            timestamp_utc=datetime.datetime.utcnow().isoformat(),
            archetype=intent.archetype.value,
            regime=intent.regime.value,
            phi=intent.phi,
            v_phi=intent.v_phi,
            a_phi=intent.a_phi,
            tribunal_active=intent.tribunal_active,
            ttl=intent.ttl,
            message=intent.message,
            ndr_stasis_delta=round(ndr_delta, 6),
        )

        # 1. In-memory buffer (rolling)
        self._records.append(record)
        if len(self._records) > self.max_memory_records:
            self._records = self._records[-self.max_memory_records:]

        # 2. JSONL file sink
        if self._jsonl_path:
            try:
                with open(self._jsonl_path, "a") as f:
                    f.write(record.to_json().replace("\n", " ") + "\n")
            except Exception as exc:
                logger.error(f"[AHGHeraldTrace] JSONL write failed: {exc}")

        # 3. P-01 HTTP push (v1.5 — non-blocking via background thread)
        if self._http_sink:
            try:
                self._http_sink.enqueue(record.to_dict())
            except Exception as exc:
                logger.error(f"[AHGHeraldTrace] HTTP enqueue failed: {exc}")

        # Alerts
        if self.emit_tribunal_alerts and intent.tribunal_active:
            logger.warning(
                f"[AHGHeraldTrace] ⚠️ TRIBUNAL ACTIVE — "
                f"T{intent.turn_id} phi={intent.phi:.4f} a_phi={intent.a_phi:.4f}"
            )

        if self.emit_ndr_stasis_alerts and ndr_delta <= self.ndr_stasis_tolerance:
            logger.info(
                f"[AHGHeraldTrace] 🔷 NDR-STASIS proximity — "
                f"T{intent.turn_id} phi={intent.phi:.4f} delta={ndr_delta:.4f} "
                f"(Integration regime — peak productive phase)"
            )

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    def records(self, n: int = 20) -> list[AHGTraceRecord]:
        return self._records[-n:]

    def tribunal_events(self) -> list[AHGTraceRecord]:
        return [r for r in self._records if r.tribunal_active]

    def ndr_stasis_events(self, tolerance: Optional[float] = None) -> list[AHGTraceRecord]:
        tol = tolerance or self.ndr_stasis_tolerance
        return [r for r in self._records if r.ndr_stasis_delta is not None and r.ndr_stasis_delta <= tol]

    def phi_series(self, n: int = 50) -> list[float]:
        return [r.phi for r in self._records[-n:]]

    def summary(self) -> dict:
        """Return a summary dict for COLLEEN episode archival."""
        if not self._records:
            return {"session_id": self.session_id, "total_records": 0}
        phis = [r.phi for r in self._records]
        http_stats = self._http_sink.stats if self._http_sink else None
        return {
            "session_id": self.session_id,
            "total_records": len(self._records),
            "phi_min": round(min(phis), 4),
            "phi_max": round(max(phis), 4),
            "phi_mean": round(sum(phis) / len(phis), 4),
            "tribunal_events": len(self.tribunal_events()),
            "ndr_stasis_events": len(self.ndr_stasis_events()),
            "archetype_distribution": {
                a: sum(1 for r in self._records if r.archetype == a)
                for a in {r.archetype for r in self._records}
            },
            "jsonl_path": str(self._jsonl_path) if self._jsonl_path else None,
            "http_sink": http_stats,
        }

    def shutdown(self) -> None:
        """Graceful shutdown — flushes HTTP queue before exit."""
        if self._http_sink:
            logger.info("[AHGHeraldTrace] Shutting down HTTP sink...")
            self._http_sink.stop(timeout=10.0)
            logger.info("[AHGHeraldTrace] HTTP sink stopped.")
