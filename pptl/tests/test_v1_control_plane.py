"""Deterministic v1 control-plane contract tests."""
from __future__ import annotations

import pytest

from pptl.branch_registry import BranchRecord, BranchRegistry
from pptl.budget_ledger import BudgetExceeded, BudgetLedger, Consumption
from pptl.commit_gate import CommitDenied, CommitGate, CommitRequest
from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.state_identity import StateRegistry, canonical_state, state_id


def envelope(**kwargs) -> GovernanceEnvelope:
    defaults = dict(
        trace_id="root-trace",
        task_id="root",
        authority_scope={"research", "draft"},
        permitted_tools={"read", "search"},
        data_classes={"public", "internal"},
        prohibited_actions={"delete", "send"},
        budget=ResourceBudget(
            max_input_tokens=100,
            max_output_tokens=100,
            max_tool_calls=10,
            max_elapsed_ms=1000,
            max_rounds=3,
            max_nodes=8,
            max_depth=2,
            max_concurrency=2,
        ),
    )
    defaults.update(kwargs)
    return GovernanceEnvelope(**defaults)


def test_child_scope_must_narrow_parent() -> None:
    parent = envelope()
    child = parent.derive_child(
        trace_id="child-trace",
        task_id="child",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        budget=ResourceBudget(max_input_tokens=50, max_output_tokens=50, max_tool_calls=4, max_elapsed_ms=500, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
    )
    assert child.parent_trace_id == parent.trace_id
    assert child.risk_tier == parent.risk_tier
    with pytest.raises(PermissionError):
        parent.derive_child(
            trace_id="bad",
            task_id="bad",
            authority_scope={"research", "deploy"},
            permitted_tools={"read"},
            data_classes={"public"},
            budget=child.budget,
        )


def test_child_risk_cannot_increase() -> None:
    parent = envelope(risk_tier="low")
    with pytest.raises(PermissionError):
        parent.derive_child(
            trace_id="bad-risk",
            task_id="bad-risk",
            authority_scope={"research"},
            permitted_tools={"read"},
            data_classes={"public"},
            budget=ResourceBudget(max_input_tokens=10, max_output_tokens=10, max_tool_calls=1, max_elapsed_ms=100, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
            risk_tier="medium",
        )


def test_budget_reservation_is_fail_closed() -> None:
    ledger = BudgetLedger(envelope().budget)
    ledger.reserve(Consumption(tool_calls=3, nodes=1))
    with pytest.raises(BudgetExceeded):
        ledger.reserve(Consumption(tool_calls=8, nodes=1))
    assert ledger.reserved.tool_calls == 3


def test_state_identity_is_deterministic() -> None:
    state = {"b": 2, "a": [1, 2]}
    assert canonical_state(state) == canonical_state({"a": [1, 2], "b": 2})
    assert state_id(state) == state_id({"a": [1, 2], "b": 2})
    registry = StateRegistry()
    registry.observe(state)
    assert registry.contains(state)


def test_branch_registry_retains_rejected_and_vetoing_records() -> None:
    registry = BranchRegistry()
    registry.add(BranchRecord("root.v", None, "VERIFY", "state-1", merge_status="correlated"))
    registry.add(BranchRecord("root.g", None, "GOVERN", "state-2", policy_verdict="ESCALATE", merge_status="escalated", terminal=True))
    assert len(registry.all()) == 2
    assert registry.get("root.g").terminal is True
    assert registry.by_status("correlated")[0].branch_id == "root.v"


def test_commit_requires_explicit_authorization() -> None:
    gate = CommitGate()
    req = gate.propose(CommitRequest("r1", "t1", "send", "external", {"channel": "x"}))
    with pytest.raises(CommitDenied):
        gate.commit(req.request_id)
    gate.authorize("r1", "operator", "AUTH-1")
    assert gate.commit("r1") == "operator:AUTH-1"


def test_control_plane_legal_transitions_and_veto() -> None:
    plane = ControlPlane()
    task = ControlTask("t1", envelope(task_id="t1", trace_id="t1-trace"))
    plane.submit(task)
    plane.admit("t1")
    plane.start_expansion("t1")
    plane.begin_evaluation("t1")
    plane.veto("t1", "governance failure")
    assert task.state is TaskState.ESCALATED
    plane.terminate("t1")
    assert task.state is TaskState.TERMINATED


def test_illegal_transition_fails_closed() -> None:
    plane = ControlPlane()
    task = ControlTask("t1", envelope(task_id="t1", trace_id="t1-trace"))
    plane.submit(task)
    with pytest.raises(ControlPlaneViolation):
        plane.terminate("t1")


def test_child_reuses_parent_boundary_without_escalation() -> None:
    plane = ControlPlane()
    root = ControlTask("root", envelope())
    plane.submit(root)
    plane.admit("root")
    child = plane.create_child(
        "root",
        task_id="child",
        trace_id="child-trace",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        envelope_budget=ResourceBudget(max_input_tokens=25, max_output_tokens=25, max_tool_calls=2, max_elapsed_ms=250, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
    )
    assert child.envelope.authority_scope == frozenset({"research"})
    assert child.envelope.permitted_tools == frozenset({"read"})
    assert child.envelope.parent_trace_id == root.envelope.trace_id


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
            envelope_budget=ResourceBudget(max_input_tokens=10, max_output_tokens=10, max_tool_calls=1, max_elapsed_ms=100, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
        )


def test_cycle_detection_rejects_same_child_state() -> None:
    plane = ControlPlane()
    root = ControlTask("root", envelope())
    plane.submit(root)
    plane.admit("root")
    child = plane.create_child(
        "root",
        task_id="child",
        trace_id="child-trace",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        envelope_budget=ResourceBudget(max_input_tokens=10, max_output_tokens=10, max_tool_calls=1, max_elapsed_ms=100, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
    )
    assert child.task_id == "child"
    child.state = TaskState.ADMITTED
    with pytest.raises(ControlPlaneViolation):
        plane.create_child(
            "root",
            task_id="child2",
            trace_id="child-trace",
            authority_scope={"research"},
            permitted_tools={"read"},
            data_classes={"public"},
            envelope_budget=ResourceBudget(max_input_tokens=10, max_output_tokens=10, max_tool_calls=1, max_elapsed_ms=100, max_rounds=1, max_nodes=1, max_depth=1, max_concurrency=1),
        )
