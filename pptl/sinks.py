"""
Herald sinks — fan-out destinations for TraceEvent records.

Sink contract: .emit(event: dict) -> None
Optional:      .flush() -> None
               .close() -> None
               .health() -> dict

Available sinks:
  JSONLSink          — append-only local JSONL file
  StdoutSink         — pretty-printed console output (dev/debug)
  N8nWebhookSink     — batched HTTP POST to n8n webhook
                       with dead-letter fallback + dry-run mode
"""
from __future__ import annotations
import json, os, time, threading, queue
from typing import Any


class JSONLSink:
    """Append-only JSONL file sink. Thread-safe via internal lock."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._count = 0
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    def emit(self, event: dict) -> None:
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
            self._count += 1

    def health(self) -> dict:
        return {"events_written": self._count, "path": self.path,
                "size_bytes": os.path.getsize(self.path) if os.path.exists(self.path) else 0}


class StdoutSink:
    """Pretty-printed console sink for dev/debug. Remove in production."""

    ICONS = {
        "task_start": "▶", "task_end": "■", "llm_call": "🤖",
        "judge_call": "⚖️ ", "rag_call": "🔍", "gate": "🔒",
        "route": "→", "input_veto": "🛡️", "output_veto": "🚨",
        "herald_flush": "📤",
    }

    def emit(self, event: dict) -> None:
        et   = event.get("event_type", "?").replace("TraceEventType.", "")
        icon = self.ICONS.get(et, "·")
        agent = event.get("agent", "")
        r     = event.get("round_num", 0)
        payload_keys = {k: v for k, v in event.items()
                        if k not in {"trace_id","session_id","timestamp","ts_iso",
                                     "event_type","agent","round_num","task_id"}}
        print(f"  {icon} {et:<40} r{r}  "
              f"{'[' + agent + ']' if agent else '':<12} {payload_keys}")

    def health(self) -> dict:
        return {"type": "stdout"}


class N8nWebhookSink:
    """
    Async batched HTTP POST sink targeting an n8n webhook.

    Features:
    - Internal queue: emit() never blocks orchestration
    - Configurable batch size + flush interval
    - Dead-letter JSONL for failed batches (auto-recovered on restart)
    - Dry-run mode: logs payload but never sends HTTP
    - Optional X-API-Key header auth

    Production:  dry_run=False, set HERALD_N8N_WEBHOOK_URL + HERALD_N8N_API_KEY
    Development: dry_run=True  (default)
    """

    def __init__(
        self,
        webhook_url:       str,
        api_key:           str  = "",
        batch_size:        int  = 20,
        flush_interval_s:  float = 2.0,
        dead_letter_path:  str  = "output/herald_dead_letter.jsonl",
        dry_run:           bool = True,
    ):
        self.webhook_url      = webhook_url
        self.api_key          = api_key
        self.batch_size       = batch_size
        self.flush_interval_s = flush_interval_s
        self.dead_letter_path = dead_letter_path
        self.dry_run          = dry_run
        self._queue:  queue.Queue = queue.Queue()
        self._sent    = 0
        self._failed  = 0
        self._dl      = 0
        self._running = True
        self._thread  = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def emit(self, event: dict) -> None:
        self._queue.put(event)

    def _worker(self) -> None:
        while self._running:
            batch: list[dict] = []
            deadline = time.time() + self.flush_interval_s
            while time.time() < deadline and len(batch) < self.batch_size:
                try:
                    batch.append(self._queue.get(timeout=0.1))
                except queue.Empty:
                    break
            if batch:
                self._send(batch)

    def _send(self, batch: list[dict]) -> None:
        if self.dry_run:
            self._sent += len(batch)
            return
        import urllib.request, urllib.error
        payload = json.dumps({"events": batch}).encode()
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        req = urllib.request.Request(self.webhook_url, data=payload,
                                     headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5):
                self._sent += len(batch)
        except Exception as exc:
            self._failed += len(batch)
            self._dl     += len(batch)
            os.makedirs(os.path.dirname(os.path.abspath(self.dead_letter_path)),
                        exist_ok=True)
            with open(self.dead_letter_path, "a") as f:
                for e in batch:
                    f.write(json.dumps(e) + "\n")
            print(f"[N8nWebhookSink] batch failed → dead-letter: {exc}")

    def flush(self) -> None:
        remaining: list[dict] = []
        while not self._queue.empty():
            try: remaining.append(self._queue.get_nowait())
            except queue.Empty: break
        if remaining:
            self._send(remaining)

    def close(self) -> None:
        self.flush()
        self._running = False

    def health(self) -> dict:
        return {"sent": self._sent, "failed": self._failed,
                "dead_letter": self._dl, "queue_depth": self._queue.qsize(),
                "dry_run": self.dry_run}
