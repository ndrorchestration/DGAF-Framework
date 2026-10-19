"""Ensemble v1.6 current-interface contract tests.

The 2026-10-18 cold reproduction caught a module-level ImportError handler
that incorrectly suppressed all historical tests under "run from repo root".
The obsolete ApogeeReviewer and _build_default_pdmal imports and legacy
call signatures are not interfaces of the actual module at this source head.
This suite checks the supported interfaces directly and fails at collection
if they disappear; historical assertions remain in Git history.
Evidence class: same-system engineering only, not validated efficacy.
"""

import hashlib
import json
import math
import time

import pytest

from components.ensemble_v16 import (
    IONIAN_INTERVALS,
    PSI,
    AgentAmethyst,
    ContextToken,
    DemiJouleGate,
    FibonacciPhiClosureGate,
    HarmonicParametricGate,
    PDMALConvergenceMonitor,
    PDMALGraph,
    StructuralContextPruningEngine,
    Tier,
)


def _safe_payload(**kwargs):
    payload = {
        "safety": {
            "identity": 0.9,
            "intent": 0.9,
            "consent": 0.9,
            "risk": 0.9,
            "provenance": 0.9,
            "coherence": 0.9,
        }
    }
    payload.update(kwargs)
    return payload


def test_psi_quadratic_identity():
    assert math.isclose(PSI**2, PSI + 1, rel_tol=0, abs_tol=1e-12)


def test_scpe_retains_axiom_while_pruning_stale_exploratory():
    engine = StructuralContextPruningEngine(threshold=0.99)
    aged = time.time() - 200
    engine.ingest(ContextToken("axiom", "fixed authority", Tier.AXIOM, inserted_at=aged))
    engine.ingest(ContextToken("explore", "disposable speculation", Tier.EXPLORATORY, inserted_at=aged))
    result = engine.prune()
    assert result["axiom_count"] == 1
    assert result["exploratory_count"] == 0
    assert result["pruned"] == 1
    assert engine.prune_log[0].token_id == "explore"


def test_scpe_retains_last_three_operational_tokens():
    engine = StructuralContextPruningEngine(threshold=0.99)
    aged = time.time() - 200
    for number in range(8):
        engine.ingest(ContextToken(f"op-{number}", "operational", Tier.OPERATIONAL, inserted_at=aged + number))
    result = engine.prune()
    assert result["operational_count"] == 3
    assert set(engine.snapshot()) == {"op-5", "op-6", "op-7"}


def test_scpe_prune_log_hash_is_bound_to_removed_content():
    engine = StructuralContextPruningEngine(threshold=0.99)
    engine.ingest(ContextToken("old", "source content", Tier.EXPLORATORY, inserted_at=time.time() - 100))
    engine.prune()
    assert engine.prune_log[0].content_hash == hashlib.sha256(b"source content").hexdigest()[:16]


@pytest.mark.parametrize("interval", IONIAN_INTERVALS)
def test_hpg_admits_named_ionian_interval(interval):
    assert HarmonicParametricGate().gate(interval) is True


def test_hpg_rejects_out_of_tolerance_ratio():
    assert HarmonicParametricGate(tolerance=0.02).gate(0.5) is False


def test_phi_checkpoint_passes_at_actual_reference():
    event = FibonacciPhiClosureGate().check(13, PSI)
    assert event.passed is True
    assert event.decision == "PASS"
    assert event.consecutive_fails == 0


def test_phi_warn_then_escalates_on_second_bad_checkpoint():
    phi = FibonacciPhiClosureGate()
    warning = phi.check(13, 1.0)
    escalation = phi.check(21, 1.0)
    assert (warning.decision, warning.consecutive_fails) == ("WARN", 1)
    assert (escalation.decision, escalation.consecutive_fails) == ("ESCALATE", 2)


def test_phi_fails_closed_on_unlisted_checkpoint():
    with pytest.raises(ValueError, match="Unsupported Fibonacci checkpoint"):
        FibonacciPhiClosureGate().check(12, PSI)


def test_pdmal_monitor_baseline_and_convergence():
    graph = PDMALGraph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", 1.0)
    monitor = PDMALConvergenceMonitor(graph)
    baseline = monitor.check("T0")
    assert baseline.status == "stable"
    assert baseline.graph_norm_delta == 0
    for turn in range(1, 4):
        event = monitor.check(f"T{turn}")
    assert event.status == "converged"
    assert event.routing_action == "log"


def test_pdmal_monitor_registers_actual_edge_weight_change():
    graph = PDMALGraph()
    for node in ("a", "b", "c"):
        graph.add_node(node)
    graph.add_edge("a", "b", 0.5)
    graph.add_edge("a", "c", 0.5)
    monitor = PDMALConvergenceMonitor(graph)
    monitor.check("baseline")
    graph.reweight("a", "b", 0.5)
    changed = monitor.check("after")
    assert changed.status == "watch"
    assert changed.graph_norm_delta > 0.08
    assert changed.max_edge_delta > 0


def test_demijoule_missing_or_low_safety_axes_escalate():
    gate = DemiJouleGate()
    missing = gate.safety_gate({"identity": 1.0})
    assert missing["decision"] == "ESCALATE"
    weak = _safe_payload()["safety"]
    weak["consent"] = 0.1
    assert gate.safety_gate(weak)["decision"] == "ESCALATE"
    assert gate.safety_gate(_safe_payload()["safety"])["decision"] == "PASS"


def test_orchestrator_records_missing_safety_as_non_gold_star():
    record = AgentAmethyst().orchestrate_turn("turn", {"value": "no safety axes"})
    assert record.apogee_grade == "ESCALATE"
    assert record.gold_star is False
    assert record.hpg_applied is False
    assert record.phi_decision == "SKIP"


def test_orchestrator_phi_pass_controls_hpg_and_seal_binding():
    payload = _safe_payload(fib_index=13, ratio=PSI)
    one = AgentAmethyst().orchestrate_turn("turn-a", payload)
    two = AgentAmethyst().orchestrate_turn("turn-a", payload)
    assert one.phi_decision == "PASS"
    assert one.hpg_applied is True
    assert one.hpg_effective_confidence == 0.0  # PSI is not an Ionian interval
    assert one.payload_hash == hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    assert one.seal_hash == two.seal_hash
    assert one.gold_star is True


def test_orchestrator_bad_phi_does_not_activate_hpg():
    record = AgentAmethyst().orchestrate_turn("bad-phi", _safe_payload(fib_index=13, ratio=1.0))
    assert record.phi_decision == "WARN"
    assert record.hpg_applied is False


def test_orchestrator_audit_records_are_monotonic_for_turn_number():
    agent = AgentAmethyst()
    first = agent.orchestrate_turn("t-1", _safe_payload())
    second = agent.orchestrate_turn("t-2", _safe_payload())
    assert (first.turn_number, second.turn_number) == (1, 2)
    assert len(agent.audit_log) == 2
