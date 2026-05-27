"""
test_herald_agent.py — Unit tests for HeraldAgent.

Covers:
  - All 9 TraceEventType constructors emit the correct event_type
  - Fan-out reaches all registered sinks
  - Broken sink does NOT block other sinks or raise (isolation guarantee)
  - query() filters correctly by event_type and task_id
  - health() reports correct counts and sink health
  - export_df() returns well-formed DataFrame
  - close() emits HERALD_FLUSH and calls sink.close()
  - session_id defaults to sess_{timestamp} pattern
"""
from __future__ import annotations
import re, time
import pytest

from pptl.herald_agent import HeraldAgent, TraceEventType
from pptl.tests.conftest import CaptureSink, BrokenSink


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def h_cap():
    cap = CaptureSink()
    h   = HeraldAgent(session_id="unit-sess")
    h.register_sink(cap)
    return h, cap


# ── Session ID ────────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_default_session_id_format():
    h = HeraldAgent()
    assert re.match(r"sess_\d+", h.session_id)


@pytest.mark.unit
def test_explicit_session_id():
    h = HeraldAgent(session_id="explicit-001")
    assert h.session_id == "explicit-001"


# ── Emit / fan-out ────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_task_start_emits(h_cap):
    h, cap = h_cap
    h.task_start("T1", "analyze phi topology")
    events = cap.of_type("task_start")
    assert len(events) == 1
    e = events[0]
    assert e["task_id"] == "T1"
    assert "prompt_hash" in e
    assert e["prompt_len"] == len("analyze phi topology")


@pytest.mark.unit
def test_task_end_emits(h_cap):
    h, cap = h_cap
    h.task_end("T1", status="pass", rounds=3, output_len=120)
    e = cap.of_type("task_end")[0]
    assert e["status"] == "pass"
    assert e["rounds"] == 3
    assert e["output_len"] == 120


@pytest.mark.unit
def test_llm_call_emits(h_cap):
    h, cap = h_cap
    h.llm_call("Apogee", "mock", "abc123", 200, 42.5, round_num=1)
    e = cap.of_type("llm_call")[0]
    assert e["agent"] == "Apogee"
    assert e["provider"] == "mock"
    assert e["round_num"] == 1
    assert e["elapsed_ms"] == 42.5


@pytest.mark.unit
def test_judge_call_emits(h_cap):
    h, cap = h_cap
    h.judge_call("safety", "mock", "hash", 10.0, {"safety_score": 0.95})
    e = cap.of_type("judge_call")[0]
    assert e["agent"] == "Sentinel"
    assert e["system_key"] == "safety"


@pytest.mark.unit
def test_rag_call_emits(h_cap):
    h, cap = h_cap
    h.rag_call(5, 0.12, 0, False, 8.3)
    e = cap.of_type("rag_call")[0]
    assert e["agent"] == "DemiJoule"
    assert e["n_segments"] == 5
    assert e["max_hallu_risk"] == 0.12


@pytest.mark.governance
def test_gate_pass_emits(h_cap):
    h, cap = h_cap
    h.gate("DGAF_Gate3", 3, {"safety_score": 0.95}, vetoed=False)
    e = cap.of_type("gate")[0]
    assert e["vetoed"] is False
    assert e["veto_reason"] == ""


@pytest.mark.governance
def test_gate_veto_emits(h_cap):
    h, cap = h_cap
    h.gate("DGAF_Gate3", 3, {"safety_score": 0.2}, vetoed=True,
           veto_reason="safety")
    e = cap.of_type("gate")[0]
    assert e["vetoed"] is True
    assert e["veto_reason"] == "safety"


@pytest.mark.governance
def test_input_veto_emits(h_cap):
    h, cap = h_cap
    h.input_veto(reason="bypass_signal", signal="ignore previous instructions")
    e = cap.of_type("input_veto")[0]
    assert e["reason"] == "bypass_signal"
    assert "ignore previous" in e["signal"]


@pytest.mark.governance
def test_output_veto_emits(h_cap):
    h, cap = h_cap
    h.output_veto("DGAF_Gate3", "rag_veto", {"hallucination_risk": 0.8})
    e = cap.of_type("output_veto")[0]
    assert e["agent"] == "DGAF_Gate3"
    assert e["reason"] == "rag_veto"


@pytest.mark.unit
def test_route_emits(h_cap):
    h, cap = h_cap
    h.route("Apogee", "Reson", 1.0, round_num=1, msg_hash="deadbeef")
    e = cap.of_type("route")[0]
    assert e["agent"] == "Apogee"
    assert e["dst"] == "Reson"
    assert e["edge_weight"] == 1.0


# ── Isolation: broken sink ────────────────────────────────────────────────────

@pytest.mark.unit
def test_broken_sink_does_not_block_good_sink():
    good = CaptureSink()
    h    = HeraldAgent(session_id="isolation-test")
    h.register_sink(BrokenSink())
    h.register_sink(good)
    h.task_start("T_iso", "test prompt")
    # Good sink still receives the event despite broken sink
    assert len(good.of_type("task_start")) == 1


@pytest.mark.unit
def test_broken_sink_does_not_raise():
    h = HeraldAgent(session_id="no-raise-test")
    h.register_sink(BrokenSink())
    # Must not raise
    h.task_start("T_safe", "safe prompt")


# ── Query interface ───────────────────────────────────────────────────────────

@pytest.mark.unit
def test_query_by_event_type(h_cap):
    h, cap = h_cap
    h.task_start("T2", "prompt")
    h.task_end("T2", "pass", 3)
    results = h.query(event_type="task_start")
    assert all(r["event_type"] == "task_start" for r in results)
    assert len(results) == 1


@pytest.mark.unit
def test_query_by_task_id(h_cap):
    h, cap = h_cap
    h.task_start("T_A", "prompt A")
    h.task_start("T_B", "prompt B")
    results = h.query(task_id="T_A")
    assert all(r["task_id"] == "T_A" for r in results)
    assert len(results) == 1


# ── Health & export ───────────────────────────────────────────────────────────

@pytest.mark.unit
def test_health_reports_correct_counts(h_cap):
    h, cap = h_cap
    h.task_start("T3", "p")
    h.task_end("T3", "pass", 1)
    info = h.health()
    assert info["total_events"] == 2
    assert info["session_id"] == "unit-sess"


@pytest.mark.unit
def test_export_df_shape(h_cap):
    h, cap = h_cap
    h.task_start("T4", "p")
    h.llm_call("Apogee", "mock", "h", 10, 5.0, round_num=1)
    df = h.export_df()
    assert len(df) == 2
    assert "event_type" in df.columns
    assert "ts_iso" in df.columns


# ── Close / flush ─────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_close_emits_herald_flush(h_cap):
    h, cap = h_cap
    h.task_start("T5", "p")
    h.close()
    flush_events = cap.of_type("herald_flush")
    assert len(flush_events) == 1


@pytest.mark.unit
def test_close_calls_sink_close(h_cap):
    h, cap = h_cap
    h.close()
    assert cap.closed is True
