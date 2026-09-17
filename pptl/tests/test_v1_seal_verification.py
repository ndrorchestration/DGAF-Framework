from __future__ import annotations

from types import SimpleNamespace

import pytest

from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import GateRecord, GateResult, TurnAuditRecord, TurnStatus  # isort: skip


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
        authority_scope={"research", "draft"},
        permitted_tools={"read", "search"},
        data_classes={"public", "internal"},
        prohibited_actions={"delete", "send"},
        budget=_budget(),
    )


def _sealed_audit(status: TurnStatus = TurnStatus.PASS) -> TurnAuditRecord:
    audit = TurnAuditRecord(
        session_id="session-1",
        turn_index=1,
        agent_id="agent-1",
        input_hash="a" * 64,
        gate_records=[GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS)],
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
