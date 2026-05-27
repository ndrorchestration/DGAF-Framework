"""
test_co_orchestration_schema.py — NDR P-07 contract tests.

Covers AlignmentGate, Opportunity, CoOrchQueue, load_queue, save_queue.
Markers: co_orch, governance
"""
import json
import pytest
from pathlib import Path
from pptl.co_orchestration_schema import (
    AlignmentGate,
    CoOrchQueue,
    Opportunity,
    load_queue,
    save_queue,
)


# ── AlignmentGate ───────────────────────────────────────────────────────

@pytest.mark.co_orch
@pytest.mark.governance
def test_alignment_gate_all_true_passes():
    gate = AlignmentGate(fit=True, risk=True, effort=True, priority=True)
    assert gate.passes is True
    assert gate.verdict() == "PASS"


@pytest.mark.co_orch
@pytest.mark.governance
def test_alignment_gate_partial_fails():
    gate = AlignmentGate(fit=True, risk=True, effort=False, priority=True)
    assert gate.passes is False
    assert "effort" in gate.verdict()


@pytest.mark.co_orch
@pytest.mark.governance
def test_alignment_gate_all_false_fails():
    gate = AlignmentGate()
    assert gate.passes is False
    verdict = gate.verdict()
    for label in ["fit", "risk", "effort", "priority"]:
        assert label in verdict


@pytest.mark.co_orch
def test_alignment_gate_str_contains_verdict():
    gate = AlignmentGate(fit=True, risk=True, effort=True, priority=False)
    s = str(gate)
    assert "FAIL:priority" in s
    assert "✅" in s and "❌" in s


# ── Opportunity ──────────────────────────────────────────────────────────

@pytest.fixture
def ready_opp():
    return Opportunity(
        id="OPP-TEST-001",
        title="Test opportunity",
        layer="pptl/",
        detected_by="COLLEEN",
        mode="ADOPT",
        pattern_ref="P-01",
        gate=AlignmentGate(fit=True, risk=True, effort=True, priority=True),
        status="PENDING",
    )


@pytest.mark.co_orch
@pytest.mark.governance
def test_opportunity_is_ready_all_conditions(ready_opp):
    """PENDING + gate passes + no blocked_by → is_ready True."""
    assert ready_opp.is_ready() is True


@pytest.mark.co_orch
@pytest.mark.governance
def test_opportunity_not_ready_when_blocked(ready_opp):
    ready_opp.blocked_by = "OPP-TEST-000"
    assert ready_opp.is_ready() is False


@pytest.mark.co_orch
@pytest.mark.governance
def test_opportunity_not_ready_when_gate_fails(ready_opp):
    ready_opp.gate.effort = False
    assert ready_opp.is_ready() is False


@pytest.mark.co_orch
@pytest.mark.governance
def test_opportunity_not_ready_when_done(ready_opp):
    ready_opp.status = "DONE"
    assert ready_opp.is_ready() is False


@pytest.mark.co_orch
@pytest.mark.governance
def test_opportunity_mark_done(ready_opp):
    ready_opp.mark_done(commit_sha="abc123", session="S042", note="shipped")
    assert ready_opp.status == "DONE"
    assert ready_opp.commit_sha == "abc123"
    assert ready_opp.session_done == "S042"
    assert ready_opp.amethyst_note == "shipped"


# ── CoOrchQueue ──────────────────────────────────────────────────────────

@pytest.fixture
def queue_with_opps(ready_opp):
    blocked = Opportunity(
        id="OPP-TEST-002",
        title="Blocked opp",
        layer="pptl/",
        detected_by="COLLEEN",
        mode="COMPOSE",
        pattern_ref="P-09",
        gate=AlignmentGate(fit=True, risk=True, effort=True, priority=True),
        status="PENDING",
        blocked_by="OPP-TEST-001",
    )
    done = Opportunity(
        id="OPP-TEST-003",
        title="Done opp",
        layer="pptl/",
        detected_by="Amethyst",
        mode="ALTER",
        pattern_ref="P-05",
        gate=AlignmentGate(fit=True, risk=True, effort=True, priority=True),
        status="DONE",
    )
    q = CoOrchQueue()
    q.opportunities = [ready_opp, blocked, done]
    return q


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_pending_filters_correctly(queue_with_opps):
    pending = queue_with_opps.pending()
    assert len(pending) == 2
    assert all(o.status == "PENDING" for o in pending)


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_ready_excludes_blocked(queue_with_opps):
    ready = queue_with_opps.ready()
    assert len(ready) == 1
    assert ready[0].id == "OPP-TEST-001"


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_next_for_amethyst_returns_first_ready(queue_with_opps):
    nxt = queue_with_opps.next_for_amethyst()
    assert nxt is not None
    assert nxt.id == "OPP-TEST-001"


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_next_for_amethyst_none_when_empty():
    q = CoOrchQueue()
    assert q.next_for_amethyst() is None


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_blocked_list(queue_with_opps):
    blocked = queue_with_opps.blocked()
    assert len(blocked) == 1
    assert blocked[0].id == "OPP-TEST-002"


@pytest.mark.co_orch
def test_colleen_scan_report_contains_counts(queue_with_opps):
    report = queue_with_opps.colleen_scan_report()
    assert "PENDING" in report
    assert "DONE" in report
    assert "Next for Amethyst" in report


@pytest.mark.co_orch
@pytest.mark.governance
def test_queue_round_trip_serialization(queue_with_opps):
    """to_dict() → from_dict() must preserve all opportunity states."""
    d = queue_with_opps.to_dict()
    restored = CoOrchQueue.from_dict(d)
    assert len(restored.opportunities) == len(queue_with_opps.opportunities)
    for orig, rest in zip(queue_with_opps.opportunities, restored.opportunities):
        assert orig.id == rest.id
        assert orig.status == rest.status
        assert orig.gate.passes == rest.gate.passes


@pytest.mark.co_orch
def test_load_queue_missing_file_returns_empty(tmp_path):
    """load_queue() with non-existent path returns empty CoOrchQueue."""
    q = load_queue(path=tmp_path / "nonexistent.json")
    assert isinstance(q, CoOrchQueue)
    assert q.opportunities == []


@pytest.mark.co_orch
def test_save_and_load_queue_round_trip(tmp_path, queue_with_opps):
    path = tmp_path / "test_queue.json"
    save_queue(queue_with_opps, path=path)
    assert path.exists()
    loaded = load_queue(path=path)
    assert len(loaded.opportunities) == len(queue_with_opps.opportunities)
    assert loaded.opportunities[0].id == "OPP-TEST-001"
