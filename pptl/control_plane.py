"""Deterministic DGAF v1 task/branch lifecycle controller."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .branch_registry import BranchRecord, BranchRegistry
from .budget_ledger import BudgetExceeded, Consumption, BudgetLedger
from .governance_envelope import GovernanceEnvelope
from .state_identity import StateRegistry


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


_ALLOWED: dict[TaskState, frozenset[TaskState]] = {
    TaskState.RECEIVED: frozenset({TaskState.PREFLIGHT, TaskState.TERMINATED}),
    TaskState.PREFLIGHT: frozenset({TaskState.ADMITTED, TaskState.ESCALATED}),
    TaskState.ADMITTED: frozenset({TaskState.EXPANDING, TaskState.EVALUATING, TaskState.ESCALATED}),
    TaskState.EXPANDING: frozenset({TaskState.EVALUATING, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.EVALUATING: frozenset({TaskState.EXPANDING, TaskState.MERGE_READY, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.MERGE_READY: frozenset({TaskState.COMMIT_READY, TaskState.ESCALATED, TaskState.TERMINATED}),
    TaskState.COMMIT_READY: frozenset({TaskState.TERMINATED, TaskState.ESCALATED}),
    TaskState.ESCALATED: frozenset({TaskState.TERMINATED}),
    TaskState.TERMINATED: frozenset(),
}


class ControlPlaneViolation(RuntimeError):
    """Raised when a lifecycle or governance invariant is violated."""


@dataclass
class ControlTask:
    task_id: str
    envelope: GovernanceEnvelope
    state: TaskState = TaskState.RECEIVED
    depth: int = 0
    state_history: list[str] = field(default_factory=list)
    concurrency_acquired: bool = False
    lineage_id: str | None = None

    def snapshot(self) -> dict[str, object]:
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
        self.events: list[dict[str, object]] = []
        self._lineage_active: dict[str, int] = {}
        self._lineage_limits: dict[str, int] = {}

    def submit(self, task: ControlTask) -> None:
        if task.task_id in self.tasks:
            raise ControlPlaneViolation(f"duplicate task_id: {task.task_id}")
        if task.lineage_id is None:
            task.lineage_id = task.envelope.trace_id
        self._lineage_limits.setdefault(task.lineage_id, task.envelope.budget.max_concurrency)
        self.tasks[task.task_id] = task
        self.ledgers[task.task_id] = BudgetLedger(task.envelope.budget)
        self._transition(task, TaskState.PREFLIGHT)

    def admit(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.ADMITTED)

    def start_expansion(self, task_id: str) -> None:
        task = self._task(task_id)
        if task.depth >= task.envelope.budget.max_depth:
            self._transition(task, TaskState.ESCALATED)
            return
        lineage = task.lineage_id or task.envelope.trace_id
        limit = self._lineage_limits[lineage]
        if self._lineage_active.get(lineage, 0) >= limit:
            self.events.append({"event": "CONCURRENCY_EXCEEDED", "task_id": task_id, "lineage_id": lineage})
            self._transition(task, TaskState.ESCALATED)
            return
        try:
            self.ledgers[task_id].acquire_concurrency()
            self.ledgers[task_id].reserve(Consumption(rounds=1, nodes=1))
        except BudgetExceeded as exc:
            if self.ledgers[task_id].active_concurrency:
                self.ledgers[task_id].release_concurrency()
            self.events.append({"event": "BUDGET_EXCEEDED", "task_id": task_id, "reason": str(exc)})
            self._transition(task, TaskState.ESCALATED)
            return
        self._lineage_active[lineage] = self._lineage_active.get(lineage, 0) + 1
        task.concurrency_acquired = True
        self._transition(task, TaskState.EXPANDING)

    def begin_evaluation(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.EVALUATING)

    def evaluate_turn(self, task_id: str, input_text: str, context: dict[str, Any] | None = None) -> Any:
        """Evaluate the task through the configured TGL runner from EVALUATING state only."""
        if self.tgl_runner is None:
            raise ControlPlaneViolation("no TGL runner configured")
        task = self._task(task_id)
        if task.state is not TaskState.EVALUATING:
            raise ControlPlaneViolation("TGL evaluation requires EVALUATING state")
        result = self.tgl_runner(input_text, context or {})
        status = getattr(getattr(result, "final_status", None), "value", getattr(result, "final_status", None))
        self.events.append({"event": "TGL_EVALUATED", "task_id": task_id, "status": status})
        if status in {"KILL", "KILL_REC"}:
            self.veto(task_id, "TGL terminal failure")
        elif status == "ESCALATE":
            self._transition(task, TaskState.ESCALATED)
        return result

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
        if task.state is not TaskState.ESCALATED:
            self._transition(task, TaskState.ESCALATED)

    def terminate(self, task_id: str) -> None:
        task = self._task(task_id)
        self._transition(task, TaskState.TERMINATED)
        if task.concurrency_acquired:
            self.ledgers[task_id].release_concurrency()
            lineage = task.lineage_id or task.envelope.trace_id
            self._lineage_active[lineage] = max(0, self._lineage_active.get(lineage, 0) - 1)
            task.concurrency_acquired = False

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
        if parent.state not in {TaskState.ADMITTED, TaskState.EXPANDING, TaskState.EVALUATING}:
            raise ControlPlaneViolation("child creation requires an active parent task")
        child_depth = parent.depth + 1
        if child_depth > parent.envelope.budget.max_depth:
            raise ControlPlaneViolation("child exceeds maximum recursion depth")
        child = ControlTask(
            task_id=task_id,
            depth=child_depth,
            lineage_id=parent.lineage_id,
            envelope=parent.envelope.derive_child(
                trace_id=trace_id,
                task_id=task_id,
                authority_scope=authority_scope,
                permitted_tools=permitted_tools,
                data_classes=data_classes,
                budget=envelope_budget,
            ),
        )
        snapshot = child.snapshot()
        if self.state_registry.contains(snapshot):
            raise ControlPlaneViolation("repeated orchestration state")
        self.state_registry.observe(snapshot)
        self.submit(child)
        return child

    def register_branch(self, branch: BranchRecord) -> None:
        self.branches.add(branch)
        self.events.append(
            {
                "event": "BRANCH_RECORDED",
                "branch_id": branch.branch_id,
                "policy_verdict": branch.policy_verdict,
                "merge_status": branch.merge_status,
            }
        )

    def consume(self, task_id: str, amount: Consumption) -> None:
        try:
            self.ledgers[task_id].consume(amount)
        except BudgetExceeded as exc:
            task = self._task(task_id)
            self.events.append({"event": "BUDGET_EXCEEDED", "task_id": task_id, "reason": str(exc)})
            if task.state is not TaskState.ESCALATED:
                self._transition(task, TaskState.ESCALATED)
            raise

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
