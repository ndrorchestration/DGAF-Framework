from __future__ import annotations

from types import SimpleNamespace

import pytest

from pptl.control_plane import (
    ControlPlane,
    ControlPlaneViolation,
    ControlTask,
    TaskState,
)
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import (
    GateRecord,
    GateResult,
    TurnAuditRecord,
    TurnStatus,
)


def _budget() -> ResourceBudget:
    return ResourceBudget(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=3,
        max_nodes=8,
        max_depth=2,
        max_concurrency=2,
    )


def _envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="root-trace",
        task_id="root",
        authority_scope=frozenset({"research", "draft"}),
        permitted_tools=frozenset({"read", "search"}),
        data_classes=frozenset({"public", "internal"}),
        prohibited_actions=frozenset({"delete", "send"}),
        budget=_budget(),
    )


def _canonical_gate_records() -> list[GateRecord]:
    return [
        GateRecord(step, pattern, gate_name, GateResult.PASS)
        for step, pattern, gate_name in [
            (0, "P-35", "ProcludingPremiseGate"),
            (1, "P-31", "SCPE_Prune"),
            (2, "P-33", "PDMAL_ConvergenceMonitor"),
            (3, "N/A", "DemiJoule_SafetyGate"),
            (4, "P-27", "KAPPA_Router"),
            (5, "P-29", "Sentinel_RiskPass"),
            (6, "P-32", "PhiClosure_Gate"),
            (7, "N/A", "HPG_OctaveGate"),
            (8, "P-30", "Apogee_AttestationGate"),
            (9, "P-01", "Herald_FanOut"),
        ]
    ]


def _sealed_audit(
    status: TurnStatus = TurnStatus.PASS,
    gate_records: list[GateRecord] | None = None,
) -> TurnAuditRecord:
    audit = TurnAuditRecord(
        session_id="session-1",
        turn_index=1,
        agent_id="agent-1",
        input_hash="a" * 64,
        gate_records=_canonical_gate_records() if gate_records is None else gate_records,
        final_status=status,
        timestamp="2026-09-17T00:00:00+00:00",
    )
    audit.seal()
    return audit


def _evaluating_plane(result: object) -> tuple[ControlPlane, ControlTask]:
    plane = ControlPlane(tgl_runner=lambda _input, _context: result)
    task = ControlTask("root", _envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    return plane, task


def test_control_plane_accepts_authentic_tgl_seal() -> None:
    plane, task = _evaluating_plane(_sealed_audit())

    plane.evaluate_turn("root", "input")
    plane.mark_merge_ready("root")

    assert task.state is TaskState.MERGE_READY


def test_control_plane_rejects_arbitrary_64_character_seal() -> None:
    forged = SimpleNamespace(final_status="PASS", seal_hash="0" * 64)
    plane, task = _evaluating_plane(forged)

    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")

    assert task.state is TaskState.ESCALATED


def test_control_plane_rejects_tampered_audit_after_sealing() -> None:
    audit = _sealed_audit()
    audit.gate_records.append(GateRecord(1, "P-31", "SCPE_Prune", GateResult.KILL, "tampered after seal"))
    plane, task = _evaluating_plane(audit)

    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")

    assert task.state is TaskState.ESCALATED


def test_control_plane_rejects_incomplete_self_sealed_pass() -> None:
    audit = _sealed_audit(gate_records=[GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS)])
    plane, task = _evaluating_plane(audit)

    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")

    assert task.state is TaskState.ESCALATED


@pytest.mark.parametrize(
    "gate_records",
    [
        lambda records: records[:3] + [records[2]] + records[3:],
        lambda records: records[:2] + [records[3], records[2]] + records[4:],
        lambda records: [
            *records[:4],
            GateRecord(4, "P-27", "SubstitutedRouter", GateResult.PASS),
            *records[5:],
        ],
    ],
)
def test_control_plane_rejects_duplicate_reordered_or_substituted_gates(gate_records) -> None:
    records = gate_records(_canonical_gate_records())
    audit = _sealed_audit(gate_records=records)
    plane, task = _evaluating_plane(audit)

    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")

    assert task.state is TaskState.ESCALATED


def test_control_plane_rejects_self_sealed_final_status_override() -> None:
    audit = _sealed_audit(status=TurnStatus.WARN)
    plane, task = _evaluating_plane(audit)

    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")

    assert task.state is TaskState.ESCALATED
