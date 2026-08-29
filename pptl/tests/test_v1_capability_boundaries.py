from __future__ import annotations

from types import SimpleNamespace

import pytest

from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget


VALID_SEAL = "0" * 64


def budget() -> ResourceBudget:
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


def envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="root-trace",
        task_id="root",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        prohibited_actions={"delete"},
        budget=budget(),
    )


def test_tgl_runner_is_immutable_after_construction():
    runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash=VALID_SEAL)
    plane = ControlPlane(tgl_runner=runner)
    with pytest.raises(AttributeError):
        plane.tgl_runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash=VALID_SEAL)
    assert plane.tgl_runner is runner


def test_read_only_views_do_not_expose_mutators():
    plane = ControlPlane()
    task = ControlTask("root", envelope())
    plane.submit(task)
    assert not hasattr(plane.state_registry, "observe")
    assert not hasattr(plane.branches, "add")
    with pytest.raises(AttributeError):
        plane.tasks["other"] = task
    with pytest.raises(AttributeError):
        plane.ledgers["root"] = plane.ledgers["root"]
    events = plane.events
    assert isinstance(events, tuple)
    with pytest.raises(AttributeError):
        events.append({"event": "tamper"})


def test_fake_unsealed_tgl_result_fails_closed():
    runner = lambda _input, _context: SimpleNamespace(final_status="PASS", seal_hash="not-a-seal")
    plane = ControlPlane(tgl_runner=runner)
    task = ControlTask("root", envelope())
    plane.submit(task)
    plane.admit("root")
    plane.begin_evaluation("root")
    with pytest.raises(ControlPlaneViolation, match="valid sealed evidence"):
        plane.evaluate_turn("root", "input")
    assert task.state.value == "ESCALATED"
