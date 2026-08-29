from __future__ import annotations

import pytest

from pptl.branch_registry import BranchRecord, BranchRegistry
from pptl.budget_ledger import BudgetExceeded, BudgetLedger, Consumption
from pptl.commit_gate import CommitDenied, CommitGate, CommitRequest
from pptl.control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.state_identity import StateRegistry, canonical_state, state_id


def budget(**overrides):
    values = dict(max_input_tokens=100, max_output_tokens=100, max_tool_calls=4,
                  max_elapsed_ms=1000, max_rounds=3, max_nodes=8, max_depth=2,
                  max_concurrency=2)
    values.update(overrides)
    return ResourceBudget(**values)


def envelope(**overrides):
    values = dict(trace_id="root-trace", task_id="root",
                  authority_scope={"research", "draft"},
                  permitted_tools={"read", "search"},
                  data_classes={"public", "internal"},
                  prohibited_actions={"delete", "send"}, budget=budget())
    values.update(overrides)
    return GovernanceEnvelope(**values)


def test_scope_and_risk_can_only_narrow():
    parent = envelope(risk_tier="medium")
    child = parent.derive_child(trace_id="child", task_id="child",
        authority_scope={"research"}, permitted_tools={"read"},
        data_classes={"public"}, budget=budget(max_depth=1), risk_tier="low")
    assert child.parent_trace_id == parent.trace_id
    assert child.risk_tier == "low"
    with pytest.raises(PermissionError):
        parent.derive_child(trace_id="bad", task_id="bad",
            authority_scope={"deploy"}, permitted_tools={"read"},
            data_classes={"public"}, budget=budget(max_depth=1))


def test_budget_reservation_is_atomic_and_fail_closed():
    ledger = BudgetLedger(budget(max_tool_calls=4))
    ledger.reserve(Consumption(tool_calls=2))
    with pytest.raises(BudgetExceeded):
        ledger.reserve(Consumption(tool_calls=3))
    assert ledger.reserved.tool_calls == 2


def test_concurrency_ceiling_is_enforced():
    ledger = BudgetLedger(budget(max_concurrency=2))
    ledger.acquire_concurrency(2)
    with pytest.raises(BudgetExceeded):
        ledger.acquire_concurrency()
    ledger.release_concurrency()
    assert ledger.active_concurrency == 1


def test_exact_state_identity_is_deterministic():
    a = {"state": "EVALUATING", "role": "VERIFY", "depth": 1}
    b = {"depth": 1, "role": "VERIFY", "state": "EVALUATING"}
    assert canonical_state(a) == canonical_state(b)
    assert state_id(a) == state_id(b)
    registry = StateRegistry(); registry.observe(a)
    assert registry.contains(b)


def test_branch_registry_retains_correlated_and_vetoing_records():
    registry = BranchRegistry()
    registry.add(BranchRecord("verify", None, "VERIFY", "s1", merge_status="correlated"))
    registry.add(BranchRecord("govern", None, "GOVERN", "s2", policy_verdict="ESCALATE", merge_status="escalated", terminal=True))
    assert registry.count == 2
    assert registry.by_status("correlated")[0].branch_id == "verify"


def test_branch_metadata_is_immutable():
    source = {"authorization": "AUTH-1"}
    record = BranchRecord("verify", None, "VERIFY", "s1", metadata=source)
    source["authorization"] = "tampered"
    assert record.metadata["authorization"] == "AUTH-1"
    with pytest.raises(TypeError):
        record.metadata["authorization"] = "tampered"


def test_commit_gate_requires_explicit_authorization():
    gate = CommitGate()
    request = gate.propose(CommitRequest("r1", "t1", "send", "external", {"channel": "x"}))
    with pytest.raises(CommitDenied):
        gate.commit("r1")
    gate.authorize("r1", "operator", "AUTH-1")
    assert gate.commit("r1") == "operator:AUTH-1"
    with pytest.raises(CommitDenied):
        gate.authorize("r1", "other", "AUTH-2")


def test_commit_request_parameters_are_immutable_after_proposal():
    parameters = {"channel": "x"}
    request = CommitRequest("r1", "t1", "send", "external", parameters)
    parameters["channel"] = "tampered"
    assert request.parameters["channel"] == "x"
    with pytest.raises(TypeError):
        request.parameters["channel"] = "tampered"


def test_commit_cannot_be_replayed():
    gate = CommitGate()
    gate.propose(CommitRequest("r1", "t1", "send", "external", {"channel": "x"}))
    gate.authorize("r1", "operator", "AUTH-1")
    assert gate.commit("r1") == "operator:AUTH-1"
    with pytest.raises(CommitDenied, match="already committed"):
        gate.commit("r1")


def test_control_plane_lifecycle_and_cleanup():
    plane = ControlPlane()
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root"); plane.start_expansion("root"); plane.begin_evaluation("root")
    plane.veto("root", "governance failure")
    assert task.state is TaskState.ESCALATED
    plane.terminate("root")
    assert task.state is TaskState.TERMINATED
    assert plane.ledgers["root"].active_concurrency == 0


def test_child_requires_active_parent_and_inherits_lineage():
    plane = ControlPlane()
    root = ControlTask("root", envelope()); plane.submit(root)
    with pytest.raises(ControlPlaneViolation):
        plane.create_child("root", task_id="child", trace_id="child", authority_scope={"research"},
                           permitted_tools={"read"}, data_classes={"public"}, envelope_budget=budget(max_depth=1))
    plane.admit("root")
    child = plane.create_child("root", task_id="child", trace_id="child", authority_scope={"research"},
                               permitted_tools={"read"}, data_classes={"public"}, envelope_budget=budget(max_depth=1))
    assert child.lineage_id == root.lineage_id


def test_commit_ready_requires_explicit_envelope_permission():
    plane = ControlPlane()
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root"); plane.begin_evaluation("root"); plane.mark_merge_ready("root")
    with pytest.raises(ControlPlaneViolation):
        plane.mark_commit_ready("root")


def test_tgl_exception_escalates_and_releases_slot():
    def failing_tgl(_input, _context):
        raise RuntimeError("synthetic TGL failure")

    plane = ControlPlane(tgl_runner=failing_tgl)
    task = ControlTask("root", envelope())
    plane.submit(task); plane.admit("root"); plane.start_expansion("root"); plane.begin_evaluation("root")
    with pytest.raises(ControlPlaneViolation, match="TGL runner failed"):
        plane.evaluate_turn("root", "input")
    assert task.state is TaskState.ESCALATED
    assert plane.ledgers["root"].active_concurrency == 0
    assert plane._lineage_active[root_lineage(task)] == 0


def root_lineage(task: ControlTask) -> str:
    return task.lineage_id or task.envelope.trace_id
