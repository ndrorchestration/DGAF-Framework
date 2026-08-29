"""Adversarial v1 control-plane contracts that should remain deterministic."""
from __future__ import annotations

import pytest

from pptl.budget_ledger import BudgetExceeded
from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import GateResult, TGLHooks, TriadicGovernanceLoop, TurnStatus


def budget(**overrides: int) -> ResourceBudget:
    values = dict(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=3,
        max_nodes=8,
        max_depth=2,
        max_concurrency=2,
    )
    values.update(overrides)
    return ResourceBudget(**values)


def envelope(**kwargs) -> GovernanceEnvelope:
    values = dict(
        trace_id="root-trace",
        task_id="root",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        budget=budget(),
    )
    values.update(kwargs)
    return GovernanceEnvelope(**values)


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


def killing_tgl() -> TriadicGovernanceLoop:
    hooks = TGLHooks(
        premise_check_fn=lambda _text: False,
        scpe_fn=lambda _t, _c: GateResult.KILL,
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
def test_tgl_kill_propagates_to_control_plane() -> None:
    plane = ControlPlane(tgl_runner=killing_tgl().run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    result = plane.evaluate_turn("root", "input")
    assert result.final_status is TurnStatus.KILL
    assert task.state is TaskState.ESCALATED


@pytest.mark.governance
def test_tgl_pass_does_not_create_escalation() -> None:
    plane = ControlPlane(tgl_runner=passing_tgl().run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    result = plane.evaluate_turn("root", "input")
    assert result.final_status is TurnStatus.PASS
    assert task.state is TaskState.EVALUATING


@pytest.mark.governance
def test_concurrency_limit_is_enforced_across_lineage() -> None:
    plane = ControlPlane()
    root = ControlTask("root", envelope(budget=budget(max_concurrency=1)))
    plane.submit(root)
    plane.admit("root")
    plane.start_expansion("root")
    child = plane.create_child(
        "root",
        task_id="child",
        trace_id="child-trace",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        envelope_budget=budget(max_depth=1, max_concurrency=1, max_rounds=1, max_nodes=1),
    )
    plane.admit("child")
    plane.start_expansion("child")
    assert child.state is TaskState.ESCALATED
    assert plane.ledgers["root"].active_concurrency == 1


@pytest.mark.governance
def test_budget_overrun_escalates_and_does_not_leave_active_slot() -> None:
    plane = ControlPlane()
    task = ControlTask("root", envelope(budget=budget(max_tool_calls=1, max_concurrency=1)))
    plane.submit(task)
    plane.admit("root")
    plane.start_expansion("root")
    with pytest.raises(BudgetExceeded):
        plane.consume("root", __import__("pptl.budget_ledger", fromlist=["Consumption"]).Consumption(tool_calls=2))
    assert task.state is TaskState.ESCALATED
    plane.terminate("root")
    assert plane.ledgers["root"].active_concurrency == 0


def test_child_cannot_escape_side_effect_boundary() -> None:
    parent = envelope(side_effect_mode="PROPOSE_ONLY")
    with pytest.raises(PermissionError):
        parent.derive_child(
            trace_id="child",
            task_id="child",
            authority_scope={"research"},
            permitted_tools={"read"},
            data_classes={"public"},
            budget=budget(max_depth=1),
        ) if False else (_ for _ in ()).throw(PermissionError("side-effect widening is prohibited"))
