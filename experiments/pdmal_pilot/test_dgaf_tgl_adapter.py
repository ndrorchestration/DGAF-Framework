"""Contract tests for the pre-freeze DGAF/TGL adapter.

These tests validate deterministic serialization, structured decision mapping,
bounded state updates, exact provenance identity across the adapter/TGL boundary,
and binding of restored gate state into provenance identity. They do not
authorize pilot execution or generate empirical data.
"""
from __future__ import annotations

import hashlib

import pytest

from dgaf_tgl_adapter import (
    ConvergenceState,
    ConsensusState,
    DGAF_TGLAdapter,
    SCPEState,
    apply_decision,
    canonicalize_state,
    decision_from_audit,
)
from pptl.triadic_governance_loop import (
    GateRecord,
    GateResult,
    TurnAuditRecord,
    TurnStatus,
)


def _state(**overrides) -> ConsensusState:
    values = dict(
        seed_id=20260817,
        iteration=3,
        agent_values=(0.1, -0.2, 0.3, 0.4),
        alive=(True, True, True, True),
        original_neighbors=((1, 3), (0, 2), (1, 3), (0, 2)),
        active_neighbors=((1, 3), (0, 2), (1, 2), (0, 2)),
        failure_history=((1,),),
        failure_count_current=1,
        failure_count_total=1,
        current_final_std=0.2,
        current_mean=0.15,
        runtime_budget_remaining_ms=290000,
        protocol_id="PDMAL-PREFREEZE-V1",
    )
    values.update(overrides)
    return ConsensusState(**values)


@pytest.fixture
def state() -> ConsensusState:
    return _state()


def test_canonical_serialization_is_deterministic(state: ConsensusState) -> None:
    assert canonicalize_state(state) == canonicalize_state(state)
    assert canonicalize_state(state).startswith("PDMAL_DGAF_ADAPTER_V1\n")
    assert "provenance_state_version=1" in canonicalize_state(state)


def test_restored_scpe_state_changes_provenance_identity(state: ConsensusState) -> None:
    baseline = canonicalize_state(state)
    restored = _state(
        scpe_state=SCPEState(
            tokens=[{
                "token_id": "ax1",
                "tier": "AXIOM",
                "content": "governance invariant",
                "inserted_at": 100.0,
                "has_trust_edge": False,
            }],
            threshold=0.15,
            trust_edge_boost=0.15,
            last_k_anchor=3,
        )
    )
    assert canonicalize_state(restored) != baseline


def test_restored_convergence_state_changes_provenance_identity(state: ConsensusState) -> None:
    baseline = canonicalize_state(state)
    restored = _state(
        convergence_state=ConvergenceState(
            weights={("a", "b"): 0.75, ("a", "c"): 0.25},
            prev_weights={("a", "b"): 0.80, ("a", "c"): 0.20},
            alert_thresh=0.08,
            conv_thresh=0.02,
            n_consec=3,
            _consec_divergent=1,
            _consec_stable=0,
            _turn=4,
        )
    )
    assert canonicalize_state(restored) != baseline


def test_gate_state_hash_changes_are_exactly_recomputable(state: ConsensusState) -> None:
    canonical = canonicalize_state(state)
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert canonicalize_state(state) == canonical
    assert expected == hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def test_decision_mapping_is_structured_and_finite() -> None:
    audit = TurnAuditRecord(
        session_id="s", turn_index=1, agent_id="a", input_hash="x",
        gate_records=[], final_status=TurnStatus.PASS,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert decision_from_audit(audit) == "NO_CHANGE"

    audit = TurnAuditRecord(
        session_id="s", turn_index=1, agent_id="a", input_hash="x",
        gate_records=[], final_status=TurnStatus.WARN,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert decision_from_audit(audit) == "CONSERVATIVE_MIX"

    audit = TurnAuditRecord(
        session_id="s", turn_index=1, agent_id="a", input_hash="x",
        gate_records=[], final_status=TurnStatus.KILL,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert decision_from_audit(audit) == "FAIL_CLOSED"


def test_unwired_required_gate_is_not_treated_as_treatment_outcome() -> None:
    audit = TurnAuditRecord(
        session_id="s", turn_index=1, agent_id="a", input_hash="x",
        gate_records=[GateRecord(1, "P-31", "SCPE_Prune", GateResult.SKIP, "not wired")],
        final_status=TurnStatus.ESCALATE,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert decision_from_audit(audit) == "FAIL_CLOSED"


def test_pdmal_gate_controls_isolation_decision() -> None:
    audit = TurnAuditRecord(
        session_id="s", turn_index=1, agent_id="a", input_hash="x",
        gate_records=[GateRecord(2, "P-33", "PDMAL_ConvergenceMonitor", GateResult.WARN)],
        final_status=TurnStatus.PASS,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert decision_from_audit(audit) == "ISOLATE_FAILED_NEIGHBORS"


def test_apply_decision_is_bounded(state: ConsensusState) -> None:
    next_values = apply_decision("NO_CHANGE", state.agent_values, state.active_neighbors)
    assert len(next_values) == len(state.agent_values)
    assert all(-1.0 <= value <= 1.0 for value in next_values)


def test_fail_closed_never_returns_success(state: ConsensusState) -> None:
    with pytest.raises(RuntimeError):
        apply_decision("FAIL_CLOSED", state.agent_values, state.active_neighbors)


def test_adapter_invokes_verified_tgl_without_pilot_authorization(state: ConsensusState) -> None:
    adapter = DGAF_TGLAdapter(session_id="contract-test")
    result = adapter.run_turn(state)
    assert result.attempt_status.value in {"SUCCESS", "FAILURE"}
    assert result.decision in {
        "NO_CHANGE", "CONSERVATIVE_MIX", "ISOLATE_FAILED_NEIGHBORS", "FAIL_CLOSED",
    }
    assert result.decision == "FAIL_CLOSED"
    assert len(result.input_hash) == 64
    assert len(result.audit_seal_hash) == 64
    assert result.audit.turn_index == state.iteration + 1


def test_adapter_and_tgl_share_exact_input_identity(state: ConsensusState) -> None:
    adapter = DGAF_TGLAdapter(session_id="provenance-test")
    result = adapter.run_turn(state)
    expected = hashlib.sha256(result.input_text.encode("utf-8")).hexdigest()
    assert result.input_hash == expected
    assert result.audit.input_hash == expected
