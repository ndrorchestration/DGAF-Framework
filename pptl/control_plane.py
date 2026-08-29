"""Deterministic DGAF v1 task/branch lifecycle controller."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .branch_registry import BranchRecord, BranchRegistry
from .budget_ledger import BudgetExceeded, BudgetLedger, Consumption
from .governance_envelope import GovernanceEnvelope
from .state_identity import StateRegistry, state_id


class TaskState(str, Enum):
    RECEIVED = "RECEIVED"
    PREFLIGHT = "PREFLIGHT"
    ADMITTED = "ADMITTED"
    EXPANDING = "EXPANDING"
    EVALUATING = "EVALUATING"
    MERGE_READY = "MERGE_READY"
    COMMIT_READY = "COMMIT_READY"
    ESCALATED = "ESCALATED"
    TERMINATED = "TERMINATED"


class ControlPlaneViolation(RuntimeError):
    """Raised when a lifecycle or governance invariant is violated."""


_ALLOWED: dict[TaskState, frozenset[TaskState]] = {
    TaskState.RECEIVED: frozenset({TaskState.PREFLIGHT, TaskState.TERMINATED}),
    TaskState.PREFLIGHT: frozenset({TaskState.ADMITTED, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.ADMITTED: frozenset({TaskState.EXPANDING, TaskState.EVALUATING, TaskState.ESCALATED}),
    TaskState.EXPANDING: frozenset({TaskState.EVALUATING, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.EVALUATING: frozenset({TaskState.EXPANDING, TaskState.MERGE_READY, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.MERGE_READY: frozenset({TaskState.COMMIT_READY, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.COMMIT_READY: frozenset({TaskState.TERMINATED, TaskState.ESCALATED}),
    TaskState.ESCALATED: frozenset({TaskState.TERMINATED}),
    TaskState.TERMINATED: frozenset(),
}


@dataclass
class ControlTask:
    task_id: str
    envelope: GovernanceEnvelope
    state: TaskState = TaskState.RECEIVED
    depth: int = 0
    state_history: list[str] = field(default_factory=list)

    def snapshot(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "state": self.state.value,
            "depth": self.depth,
            "envelope_trace": self.envelope.trace_id,
            "parent_trace": self.envelope.parent_trace_id,
        }


class ControlPlane:
    """Single-run deterministic controller; external actions remain prohibited by default."""

    def __init__(self, *, tgl_runner: Callable[..., Any] | None = None) -> None:
        self.tgl_runner = tgl_runner
        self.state_registry = StateRegistry()
        self.branches = BranchRegistry()
        self.tasks: dict[str, ControlTask] = {}
        self.ledgers: dict[str, BudgetLedger] = {}
        self.events: list[dict[str, Any]] = []

    def submit(self, task: ControlTask) -> None:
        if task.task_id in self.tasks:
            raise ControlPlaneViolation(f"duplicate task_id: {task.task_id}")
        self.tasks[task.task_id] = task
        self.ledgers[task.task_id] = BudgetLedger(task.envelope.budget)
        self._transition(task, TaskState.PREFLIGHT)

    def admit(self, task_id: str) -> None:
        task = self._task(task_id)
        self._transition(task, TaskState.ADMITTED)

    def start_expansion(self, task_id: str) -> None:
        task = self._task(task_id)
        if task.depth >= task.envelope.budget.max_rounds:
            self._transition(task, TaskState.ESCALATED)
            return
        self.ledgers[task_id].reserve(Consumption(rounds=1, nodes=1))
        self._transition(task, TaskState.EXPANDING)

    def begin_evaluation(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.EVALUATING)

    def mark_merge_ready(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.MERGE_READY)

    def mark_commit_ready(self, task_id: str) -> None:
        task = self._task(task_id)
        if task.envelope.side_effect_mode != "COMMIT_ALLOWED":
            raise ControlPlaneViolation("task envelope does not permit commit")
        self._transition(task, TaskState.COMMIT_READY)

    def veto(self, task_id: str, reason: str) -> None:
        task = self._task(task_id)
        self.events.append({"event": "VETO", "task_id": task_id, "reason": reason})
        self._transition(task, TaskState.ESCALATED)

    def terminate(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.TERMINATED)

    def create_child(
        self,
        parent_id: str,
        *,
        task_id: str,
        trace_id: str,
        authority_scope: set[str],
        permitted_tools: set[str],
        data_classes: set[str],
        envelope_budget,
    ) -> ControlTask:
        parent = self._task(parent_id)
        child = ControlTask(
            task_id=task_id,
            depth=parent.depth + 1,
            envelope=parent.envelope.derive_child(
                trace_id=trace_id,
                task_id=task_id,
                authority_scope=authority_scope,
                permitted_tools=permitted_tools,
                data_classes=data_classes,
                budget=envelope_budget,
            ),
        )
        if child.depth > parent.envelope.budget.max_rounds:
            raise ControlPlaneViolation("child exceeds maximum recursion depth")
        snapshot = child.snapshot()
        if self.state_registry.contains(snapshot):
            raise ControlPlaneViolation("repeated orchestration state")
        self.state_registry.observe(snapshot)
        self.submit(child)
        return child

    def register_branch(self, branch: BranchRecord) -> None:
        self.branches.add(branch)
        if branch.policy_verdict in {"KILL", "ESCALATE"}:
            parent = self.tasks.get(branch.parent_branch_id or "")
            if parent is not None:
                self.veto(parent.task_id, branch.policy_verdict)

    def consume(self, task_id: str, amount: Consumption) -> None:
        self.ledgers[task_id].consume(amount)

    def _transition(self, task: ControlTask, new_state: TaskState) -> None:
        if new_state not in _ALLOWED[task.state]:
            raise ControlPlaneViolation(f"illegal transition {task.state.value} -> {new_state.value}")
        task.state_history.append(task.state.value)
        task.state = new_state
        self.events.append({"event": "STATE", "task_id": task.task_id, "state": new_state.value})

    def _task(self, task_id: str) -> ControlTask:
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise KeyError(task_id) from exc
