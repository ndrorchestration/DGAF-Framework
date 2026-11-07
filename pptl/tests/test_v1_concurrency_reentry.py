"""Regression tests for per-task and per-lineage re-expansion accounting.

Engineering-only characterization for #1548; no effect authority or scientific
candidate is affected. A task owns at most one concurrency slot across cycles.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from pptl.control_plane import (
    ControlPlane,
    ControlPlaneViolation,
    ControlTask,
    TaskState,
)
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget


def _task(
    task_id: str = "root",
    *,
    lineage: str = "synthetic-lineage",
    max_concurrency: int = 1,
    max_rounds: int = 3,
) -> ControlTask:
    budget = ResourceBudget(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=max_rounds,
        max_nodes=8,
        max_depth=2,
        max_concurrency=max_concurrency,
    )
    return ControlTask(
        task_id,
        GovernanceEnvelope(
            trace_id=lineage,
            task_id=task_id,
            authority_scope=frozenset({"research"}),
            permitted_tools=frozenset({"read"}),
            data_classes=frozenset({"public"}),
            prohibited_actions=frozenset({"send"}),
            budget=budget,
            side_effect_mode="PROPOSE_ONLY",
        ),
    )


def _admit(plane: ControlPlane, task: ControlTask) -> None:
    plane.submit(task)
    plane.admit(task.task_id)


def test_repeated_expansion_reuses_one_slot_and_charges_every_round() -> None:
    plane = ControlPlane()
    task = _task()
    _admit(plane, task)

    for expected_round in (1, 2, 3):
        plane.start_expansion("root")
        assert task.state is TaskState.EXPANDING
        assert task.concurrency_acquired
        assert plane.ledgers["root"].active_concurrency == 1
        assert plane._lineage_active["synthetic-lineage"] == 1
        assert plane.ledgers["root"].consumed.rounds == expected_round
        assert plane.ledgers["root"].consumed.nodes == expected_round
        plane.begin_evaluation("root")

    plane.terminate("root")
    assert task.state is TaskState.TERMINATED
    assert not task.concurrency_acquired
    assert plane.ledgers["root"].active_concurrency == 0
    assert plane._lineage_active["synthetic-lineage"] == 0


def test_repeat_then_veto_releases_exactly_one_slot() -> None:
    plane = ControlPlane()
    task = _task()
    _admit(plane, task)
    plane.start_expansion("root")
    plane.begin_evaluation("root")
    plane.start_expansion("root")

    plane.veto("root", "synthetic negative control")
    assert task.state is TaskState.ESCALATED
    assert plane.ledgers["root"].active_concurrency == 0
    assert plane._lineage_active["synthetic-lineage"] == 0
    plane.terminate("root")
    assert plane.ledgers["root"].active_concurrency == 0


def test_reentry_budget_exhaustion_escalates_and_releases_slot() -> None:
    plane = ControlPlane()
    task = _task(max_rounds=1)
    _admit(plane, task)
    plane.start_expansion("root")
    plane.begin_evaluation("root")
    plane.start_expansion("root")

    assert task.state is TaskState.ESCALATED
    assert plane.ledgers["root"].consumed.rounds == 1
    assert plane.ledgers["root"].active_concurrency == 0
    assert plane._lineage_active["synthetic-lineage"] == 0
    assert any(event["event"] == "BUDGET_EXCEEDED" for event in plane.events)


def test_reentry_does_not_bypass_shared_lineage_limit_for_other_task() -> None:
    plane = ControlPlane()
    first = _task("first")
    second = _task("second")
    _admit(plane, first)
    _admit(plane, second)

    plane.start_expansion("first")
    plane.begin_evaluation("first")
    plane.start_expansion("first")
    assert first.state is TaskState.EXPANDING
    assert plane._lineage_active["synthetic-lineage"] == 1

    plane.start_expansion("second")
    assert second.state is TaskState.ESCALATED
    assert plane.ledgers["second"].consumed.rounds == 0
    assert plane.ledgers["second"].active_concurrency == 0
    assert plane._lineage_active["synthetic-lineage"] == 1

    plane.terminate("first")
    assert plane._lineage_active["synthetic-lineage"] == 0
    plane.terminate("second")


def test_narrow_child_budget_reentry_does_not_double_release_on_escalation() -> None:
    """A child may have a one-slot ledger under a two-slot parent lineage."""
    plane = ControlPlane()
    parent = _task(max_concurrency=2)
    _admit(plane, parent)
    child = plane.create_child(
        "root",
        task_id="child",
        trace_id="child-trace",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        envelope_budget=replace(parent.envelope.budget, max_concurrency=1),
    )
    plane.admit("child")
    plane.start_expansion("child")
    plane.begin_evaluation("child")
    plane.start_expansion("child")

    assert child.state is TaskState.EXPANDING
    assert plane.ledgers["child"].active_concurrency == 1
    assert plane._lineage_active["synthetic-lineage"] == 1
    assert plane.ledgers["child"].consumed.rounds == 2

    plane.veto("child", "synthetic child veto")
    assert child.state is TaskState.ESCALATED
    assert plane.ledgers["child"].active_concurrency == 0
    assert plane._lineage_active["synthetic-lineage"] == 0
    plane.terminate("child")
    plane.terminate("root")
    assert plane._lineage_active["synthetic-lineage"] == 0


@pytest.mark.parametrize("already_active", (False, True))
def test_unexpected_ledger_exception_fails_closed_without_slot_leak(
    monkeypatch: pytest.MonkeyPatch, already_active: bool
) -> None:
    plane = ControlPlane()
    task = _task()
    _admit(plane, task)
    if already_active:
        plane.start_expansion("root")
        plane.begin_evaluation("root")

    def fail_consume(_amount: object) -> None:
        raise RuntimeError("synthetic ledger exception")

    monkeypatch.setattr(plane._ledgers["root"], "consume", fail_consume)
    with pytest.raises(ControlPlaneViolation, match="expansion accounting failed"):
        plane.start_expansion("root")
    assert task.state is TaskState.ESCALATED
    assert plane.ledgers["root"].active_concurrency == 0
    assert plane._lineage_active.get("synthetic-lineage", 0) == 0
    assert any(event["event"] == "EXPANSION_FAILURE" for event in plane.events)
