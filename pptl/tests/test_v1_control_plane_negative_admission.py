"""Characterization-only negative tests for control-plane TGL evidence admission.

The three original negative tests establish the fail-closed boundary and are
expected RED on the 2026-11-03 main baseline. Additional scenarios exercise
the remediation candidate. This file does not modify production behavior.
"""

from __future__ import annotations

import hashlib

import pytest

from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import (
    GateRecord,
    GateResult,
    TriadicGovernanceLoop,
    TurnAuditRecord,
    TurnStatus,
)


def _audit(input_text: str, gates: list[GateRecord]) -> TurnAuditRecord:
    audit = TurnAuditRecord(
        session_id="negative-admission-test",
        turn_index=1,
        agent_id="independent-review",
        input_hash=hashlib.sha256(input_text.encode("utf-8")).hexdigest(),
        gate_records=gates,
        final_status=TurnStatus.PASS,
        timestamp="2026-11-03T00:00:00+00:00",
    )
    audit.seal()
    assert audit.verify_seal()
    return audit


def _evaluate(audit: TurnAuditRecord, input_text: str = "expected input") -> tuple[ControlPlane, ControlTask]:
    envelope = GovernanceEnvelope(
        trace_id="negative-admission-trace",
        task_id="root",
        budget=ResourceBudget(max_concurrency=1),
        side_effect_mode="PROPOSE_ONLY",
    )
    plane = ControlPlane(tgl_runner=lambda _text, _context: audit)
    task = ControlTask("root", envelope)
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    try:
        plane.evaluate_turn("root", input_text)
    except ControlPlaneViolation:
        pass
    return plane, task


def _must_not_advance(audit: TurnAuditRecord, input_text: str = "expected input") -> None:
    plane, task = _evaluate(audit, input_text)
    if task.state is TaskState.EVALUATING:
        with pytest.raises(ControlPlaneViolation):
            plane.mark_merge_ready("root")
    assert task.state is not TaskState.MERGE_READY


def test_sealed_pass_with_missing_required_gates_cannot_advance() -> None:
    """A valid SHA-256 seal is not evidence that required gates ran."""
    _must_not_advance(
        _audit(
            "expected input",
            [
                GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS),
            ],
        )
    )


def test_sealed_pass_with_mismatched_input_hash_cannot_advance() -> None:
    """A valid seal for another input must not authorize this evaluation."""
    gates = [
        GateRecord(step, pattern, name, GateResult.PASS) for step, pattern, name in TriadicGovernanceLoop.GATE_MANIFEST
    ]
    _must_not_advance(_audit("different input", gates), "expected input")


def test_sealed_pass_with_duplicate_required_gate_cannot_advance() -> None:
    """Duplicated gate records must not substitute for a valid unique manifest."""
    gates = [
        GateRecord(step, pattern, name, GateResult.PASS) for step, pattern, name in TriadicGovernanceLoop.GATE_MANIFEST
    ]
    gates.append(GateRecord(1, "P-31", "SCPE_Prune", GateResult.PASS))
    _must_not_advance(_audit("expected input", gates))


def test_out_of_order_gate_manifest_cannot_advance() -> None:
    """A valid seal must not permit reordered gate identities."""
    gates = [
        GateRecord(step, pattern, name, GateResult.PASS) for step, pattern, name in TriadicGovernanceLoop.GATE_MANIFEST
    ]
    gates[2], gates[3] = gates[3], gates[2]
    _must_not_advance(_audit("expected input", gates))


def test_required_gate_skip_cannot_advance_even_if_summary_claims_pass() -> None:
    """A required SKIP is not an admitted PASS even with a consistent seal."""
    gates = [
        GateRecord(step, pattern, name, GateResult.SKIP if step == 6 else GateResult.PASS)
        for step, pattern, name in TriadicGovernanceLoop.GATE_MANIFEST
    ]
    _must_not_advance(_audit("expected input", gates))


def test_valid_manifest_with_unwired_optional_gates_can_advance_to_merge_ready() -> None:
    """Preserve current TGL's optional HPG/Herald semantics without admission inflation."""
    gates = [
        GateRecord(step, pattern, name, GateResult.SKIP if step in (7, 9) else GateResult.PASS)
        for step, pattern, name in TriadicGovernanceLoop.GATE_MANIFEST
    ]
    plane, task = _evaluate(_audit("expected input", gates))
    assert task.state is TaskState.EVALUATING
    plane.mark_merge_ready("root")
    assert task.state is TaskState.MERGE_READY
