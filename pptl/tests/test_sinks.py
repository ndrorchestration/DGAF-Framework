"""
test_sinks.py — Unit tests for Herald sinks.

Covers:
  JSONLSink:
    - Creates file and writes valid JSON lines
    - Thread-safe: concurrent emits produce correct line count
    - health() reports accurate event count and file size
  N8nWebhookSink (dry-run mode):
    - emit() never blocks (returns immediately)
    - dry-run increments _sent counter without HTTP
    - close() drains queue
    - health() reports sent + queue_depth
"""
from __future__ import annotations
import json, threading, time
import pytest

from pptl.sinks import JSONLSink, N8nWebhookSink, StdoutSink


# ── JSONLSink ─────────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_jsonl_creates_file(tmp_jsonl):
    sink = JSONLSink(tmp_jsonl)
    sink.emit({"event_type": "test", "v": 1})
    with open(tmp_jsonl) as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["event_type"] == "test"


@pytest.mark.unit
def test_jsonl_appends_multiple_events(tmp_jsonl):
    sink = JSONLSink(tmp_jsonl)
    for i in range(5):
        sink.emit({"i": i})
    with open(tmp_jsonl) as f:
        lines = f.readlines()
    assert len(lines) == 5
    assert json.loads(lines[4])["i"] == 4


@pytest.mark.unit
def test_jsonl_thread_safety(tmp_jsonl):
    sink    = JSONLSink(tmp_jsonl)
    n       = 50
    threads = [threading.Thread(target=sink.emit, args=({"t": i},))
               for i in range(n)]
    for t in threads: t.start()
    for t in threads: t.join()
    with open(tmp_jsonl) as f:
        lines = f.readlines()
    assert len(lines) == n


@pytest.mark.unit
def test_jsonl_health_reports_count(tmp_jsonl):
    sink = JSONLSink(tmp_jsonl)
    sink.emit({"x": 1})
    sink.emit({"x": 2})
    h = sink.health()
    assert h["events_written"] == 2
    assert h["size_bytes"] > 0


# ── StdoutSink ────────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_stdout_sink_does_not_raise(capsys):
    sink = StdoutSink()
    sink.emit({"event_type": "gate", "agent": "Sentinel", "round_num": 3,
               "vetoed": False, "scores": {}})
    out = capsys.readouterr().out
    assert "gate" in out or "🔒" in out


# ── N8nWebhookSink (dry-run) ──────────────────────────────────────────────────

@pytest.mark.unit
def test_n8n_dry_run_emit_nonblocking():
    sink = N8nWebhookSink("http://localhost:9999/webhook", dry_run=True,
                          flush_interval_s=0.1)
    t0 = time.time()
    sink.emit({"event_type": "test"})
    elapsed = time.time() - t0
    assert elapsed < 0.05  # emit() must return in <50ms
    sink.close()


@pytest.mark.unit
def test_n8n_dry_run_increments_sent():
    sink = N8nWebhookSink("http://localhost:9999/webhook", dry_run=True,
                          flush_interval_s=0.05, batch_size=5)
    for i in range(5):
        sink.emit({"i": i})
    time.sleep(0.2)  # allow worker thread to flush
    assert sink._sent == 5
    sink.close()


@pytest.mark.unit
def test_n8n_close_drains_queue():
    sink = N8nWebhookSink("http://localhost:9999/webhook", dry_run=True,
                          flush_interval_s=999)  # won't auto-flush
    for i in range(3):
        sink.emit({"i": i})
    sink.close()
    assert sink._queue.qsize() == 0


@pytest.mark.unit
def test_n8n_health_keys():
    sink = N8nWebhookSink("http://localhost:9999/webhook", dry_run=True)
    h = sink.health()
    assert {"sent", "failed", "dead_letter", "queue_depth", "dry_run"}.issubset(h.keys())
    assert h["dry_run"] is True
    sink.close()
