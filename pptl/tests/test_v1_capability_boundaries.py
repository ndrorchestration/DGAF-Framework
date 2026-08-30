from __future__ import annotations

from types import SimpleNamespace

import pytest

from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget


VALID_SEAL = "0" * 64


def _budget() -> ResourceBudget:
    return ResourceBudget(
        max_input_tokens=10,
        max_output_tokens=10,
        max_tool_calls=2,
        max_elapsed_ms=100,
        max_rounds=2,
        max_nodes=4,
        max_depth=1,
        max_concurrency=1,
    )


def _envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="root-trace",
        task_id="root",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        prohibited_actions={"delete"},
        budget=_budget(),
    )


def test_tgl_runner_is_immutable_after_construction():
    runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash=VALID_SEAL)
    plane = ControlPlane(tgl_runner=runner)
    with pytest.raises(AttributeError):
        plane.tgl_runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash=VALID_SEAL)
    assert plane.tgl_runner is runner


def test_read_only_views_expose_no_mutators():
    plane = ControlPlane()
    plane.submit(ControlTask("root", _envelope()))
    assert not hasattr(plane.state_registry, "observe")
    assert not hasattr(plane.branches, "add")
    with pytest.raises(TypeError):
        plane.tasks["other"] = plane.tasks["root"]
    with pytest.raises(TypeError):
        plane.ledgers["root"] = plane.ledgers["root"]
    assert isinstance(plane.events, tuple)


def test_fake_unsealed_tgl_result_fails_closed():
    runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash="not-a-seal")
    plane = ControlPlane(tgl_runner=runner)
    task = ControlTask("root", _envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")
    assert task.state.value == "ESCALATED"


def test_merge_ready_cannot_be_manufactured_without_tgl():
    plane = ControlPlane()
    task = ControlTask("root", _envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    with pytest.raises(ControlPlaneViolation):
        plane.mark_merge_ready("root")


def test_child_state_registry_observes_post_submit_state():
    plane = ControlPlane()
    root = ControlTask("root", _envelope())
    plane.submit(root)
    plane.admit("root")
    child = plane.create_child(
        "root",
        task_id="child",
        trace_id="child-trace",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        envelope_budget=_budget(),
    )
    assert child.state.value == "PREFLIGHT"
    assert plane.state_registry.contains(child.snapshot())
