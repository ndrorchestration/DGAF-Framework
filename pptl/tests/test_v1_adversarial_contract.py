"""Adversarial DGAF v1 control-plane contract tests."""
from __future__ import annotations

import pytest

from pptl.budget_ledger import BudgetExceeded, Consumption
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
        max_concurrency=1,
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


def _tgl(status: GateResult) -> TriadicGovernanceLoop:
    hooks = TGLHooks(
        premise_check_fn=lambda _text: False,
        scpe_fn=lambda _t, _c: status,
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
    plane = ControlPlane(tgl_runner=_tgl(GateResult.KILL).run_turn)
    task = ControlTask("root", envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    result = plane.evaluate_turn("root", "input")
    assert result.final_status is TurnStatus.KILL
    assert task.state is TaskState.ESCALATED


@pytest.mark.governance
def test_concurrency_ceiling_is_lineage_wide() -> None:
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
def test_budget_overrun_escalates_and_releases_slot_on_termination() -> None:
    plane = ControlPlane()
    task = ControlTask("root", envelope(budget=budget(max_tool_calls=1)))
    plane.submit(task)
    plane.admit("root")
    plane.start_expansion("root")
    with pytest.raises(BudgetExceeded):
        plane.consume("root", Consumption(tool_calls=2))
    assert task.state is TaskState.ESCALATED
    plane.terminate("root")
    assert plane.ledgers["root"].active_concurrency == 0


def test_child_creation_requires_active_parent() -> None:
    plane = ControlPlane()
    root = ControlTask("root", envelope())
    plane.submit(root)
    with pytest.raises(ControlPlaneViolation):
        plane.create_child(
            "root",
            task_id="child",
            trace_id="child-trace",
            authority_scope={"research"},
            permitted_tools={"read"},
            data_classes={"public"},
            envelope_budget=budget(max_depth=1, max_concurrency=1),
        )
