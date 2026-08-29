from __future__ import annotations

import pytest

from pptl.control_plane import ControlPlane, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import GateResult, TGLHooks, TriadicGovernanceLoop, TurnStatus


def envelope():
    return GovernanceEnvelope(
        trace_id="root-trace", task_id="root", authority_scope={"research"},
        permitted_tools={"read"}, data_classes={"public"},
        budget=ResourceBudget(max_input_tokens=100, max_output_tokens=100,
                              max_tool_calls=4, max_elapsed_ms=1000,
                              max_rounds=2, max_nodes=4, max_depth=2,
                              max_concurrency=1),
    )


def tgl(result=GateResult.PASS):
    hooks = TGLHooks(
        premise_check_fn=lambda _text: False,
        scpe_fn=lambda _t, _c: result,
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
def test_tgl_pass_remains_evaluable_inside_lifecycle():
    plane = ControlPlane(tgl_runner=tgl().run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root"); plane.begin_evaluation("root")
    result = plane.evaluate_turn("root", "safe")
    assert result.final_status is TurnStatus.PASS
    assert task.state is TaskState.EVALUATING


@pytest.mark.governance
def test_tgl_kill_becomes_lifecycle_escalation():
    plane = ControlPlane(tgl_runner=tgl(GateResult.KILL).run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root"); plane.begin_evaluation("root")
    result = plane.evaluate_turn("root", "unsafe")
    assert result.final_status is TurnStatus.KILL
    assert task.state is TaskState.ESCALATED


@pytest.mark.governance
def test_tgl_evaluation_requires_evaluating_state():
    plane = ControlPlane(tgl_runner=tgl().run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root")
    with pytest.raises(RuntimeError):
        plane.evaluate_turn("root", "premature")
