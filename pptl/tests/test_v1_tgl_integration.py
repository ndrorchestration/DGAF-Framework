"""Cross-module v1 control-plane ↔ TGL contract tests."""
from __future__ import annotations

import pytest

from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import GateResult, TGLHooks, TriadicGovernanceLoop, TurnStatus


def root_envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="root-trace",
        task_id="root",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        budget=ResourceBudget(
            max_input_tokens=100,
            max_output_tokens=100,
            max_tool_calls=4,
            max_elapsed_ms=1000,
            max_rounds=2,
            max_nodes=4,
            max_depth=2,
            max_concurrency=2,
        ),
    )


def passing_tgl() -> TriadicGovernanceLoop:
    hooks = TGLHooks(
        premise_check_fn=lambda _text: False,
        scpe_fn=lambda _t, _c: GateResult.PASS,
        pdmal_fn=lambda _t, _c: GateResult.PASS,
        demijoul_fn=lambda _t, _c: GateResult.PASS,
        kappa_fn=lambda _t, _c: GateResult.PASS,
        sentinel_fn=lambda _t, _c: GateResult.PASS,
        phi_closure_fn=lambda _t, _c: GateResult.PASS,
        hpg_fn=lambda _t, _c: GateResult.PASS,
        apogee_fn=lambda _t, _c: GateResult.PASS,
        herald_fn=lambda _t, _c: GateResult.PASS,
    )
    return TriadicGovernanceLoop("session", "agent", hooks)


@pytest.mark.governance
def test_control_plane_evaluate_turn_requires_evaluating_state() -> None:
    plane = ControlPlane(tgl_runner=lambda text, context: passing_tgl().run_turn(text, context))
    task = ControlTask("root", root_envelope())
    plane.submit(task)
    plane.admit("root")
    with pytest.raises(ControlPlaneViolation):
        plane.evaluate_turn("root", "safe input")


@pytest.mark.governance
def test_control_plane_evaluate_turn_records_tgl_result() -> None:
    plane = ControlPlane(tgl_runner=lambda text, context: passing_tgl().run_turn(text, context))
    task = ControlTask("root", root_envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    audit = plane.evaluate_turn("root", "safe input")
    assert audit.final_status is TurnStatus.PASS
    assert any(event["event"] == "TGL_EVALUATED" for event in plane.events)


@pytest.mark.governance
def test_tgl_failure_is_representable_as_control_plane_escalation() -> None:
    plane = ControlPlane()
    task = ControlTask("root", root_envelope())
    plane.submit(task)
    plane.admit("root")
    plane.start_expansion("root")
    plane.begin_evaluation("root")
    plane.veto("root", "TGL KILL")
    assert task.state is TaskState.ESCALATED


@pytest.mark.governance
def test_control_plane_illegal_commit_transition_fails_closed() -> None:
    plane = ControlPlane()
    task = ControlTask("root", root_envelope())
    plane.submit(task)
    plane.admit("root")
    plane.start_expansion("root")
    plane.begin_evaluation("root")
    plane.mark_merge_ready("root")
    with pytest.raises(ControlPlaneViolation):
        plane.mark_commit_ready("root")
