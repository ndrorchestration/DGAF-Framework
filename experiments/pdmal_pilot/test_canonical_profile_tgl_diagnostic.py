from __future__ import annotations

from canonical_profile_tgl_diagnostic import (
    PROFILE_ID,
    PROFILE_SOURCE_SHA,
    QUALIFICATION_SHA256,
    _audit_summary,
    _qualified_input_text,
    load_and_validate_qualification,
)
from dgaf_tgl_adapter import ConsensusState
from task_engine import AttemptStatus, ConsensusTrialResult


def _state() -> ConsensusState:
    neighbors = tuple((1,) if i == 0 else (0,) if i == 1 else () for i in range(20))
    return ConsensusState(
        seed_id=20260819,
        iteration=0,
        agent_values=tuple(0.0 for _ in range(20)),
        alive=tuple(True for _ in range(20)),
        original_neighbors=neighbors,
        active_neighbors=neighbors,
        failure_history=(),
        failure_count_current=0,
        failure_count_total=0,
        current_final_std=0.0,
        current_mean=0.0,
        runtime_budget_remaining_ms=300000,
        protocol_id="PDMAL-CANONICAL-PROFILE-DIAGNOSTIC-V1",
    )


def _result(trace: tuple[dict, ...]) -> ConsensusTrialResult:
    return ConsensusTrialResult(
        trial_key="x",
        condition="dgaf",
        topology="dodecahedral",
        failure_count=0,
        failure_nodes=(),
        initial_values=tuple(0.0 for _ in range(20)),
        final_values=tuple(0.0 for _ in range(20)),
        final_std=0.0,
        topology_fingerprint="x",
        iterations_completed=len(trace),
        attempt_status=AttemptStatus.SUCCESS,
        governance_trace=trace,
    )


def test_qualification_is_current_and_verifiable():
    raw = load_and_validate_qualification()
    assert raw


def test_canonical_input_removes_retired_scalar_and_binds_external_qualification():
    text = _qualified_input_text(_state())
    assert "\napogee=" not in "\n" + text
    assert f"profile_id={PROFILE_ID}" in text
    assert f"profile_source_sha={PROFILE_SOURCE_SHA}" in text
    assert f"qualification_sha256={QUALIFICATION_SHA256}" in text
    assert "mode=VERIFY_EXTERNAL_11Q" in text


def test_audit_summary_counts_exact_step8_pass_and_required_failure():
    trace = ({
        "gates": [
            {"step": 8, "pattern": "P-30", "gate": "Apogee", "result": "PASS"},
            {"step": 6, "pattern": "P-32", "gate": "PhiClosure_Gate", "result": "KILL"},
        ]
    },)
    summary = _audit_summary(_result(trace))
    assert summary["governance_turn_count"] == 1
    assert summary["step8_pass_count"] == 1
    assert summary["required_gate_failures"] == {"step6:PhiClosure_Gate:KILL": 1}


def test_audit_summary_fails_visible_on_malformed_or_missing_step8():
    summary = _audit_summary(_result(({"gates": "wrong"}, {"gates": []})))
    assert summary["malformed_turn_count"] == 1
    assert summary["step8_pass_count"] == 0
    assert summary["required_gate_failures"] == {"STEP8_MISSING_OR_NONPASS": 1}
