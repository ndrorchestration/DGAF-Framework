"""Deterministic DGAF v1 task/branch lifecycle controller."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Callable, Mapping

from .branch_registry import BranchRecord, BranchRegistry
from .budget_ledger import BudgetExceeded, BudgetLedger, Consumption
from .governance_envelope import GovernanceEnvelope, ResourceBudget
from .state_identity import StateRegistry
from .triadic_governance_loop import TurnAuditRecord


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


_ALLOWED = {
    TaskState.RECEIVED: {TaskState.PREFLIGHT, TaskState.TERMINATED},
    TaskState.PREFLIGHT: {TaskState.ADMITTED, TaskState.ESCALATED, TaskState.TERMINATED},
    TaskState.ADMITTED: {TaskState.EXPANDING, TaskState.EVALUATING, TaskState.ESCALATED, TaskState.TERMINATED},
    TaskState.EXPANDING: {TaskState.EVALUATING, TaskState.ESCALATED, TaskState.TERMINATED},
    TaskState.EVALUATING: {TaskState.EXPANDING, TaskState.MERGE_READY, TaskState.ESCALATED, TaskState.TERMINATED},
    TaskState.MERGE_READY: {TaskState.COMMIT_READY, TaskState.ESCALATED, TaskState.TERMINATED},
    TaskState.COMMIT_READY: {TaskState.TERMINATED, TaskState.ESCALATED},
    TaskState.ESCALATED: {TaskState.TERMINATED},
    TaskState.TERMINATED: set(),
}


class ControlPlaneViolation(RuntimeError):
    pass


@dataclass(frozen=True)
class LedgerView:
    """Read-only snapshot of a task ledger."""

    budget: ResourceBudget
    consumed: Consumption
    reserved: Consumption
    active_concurrency: int


class StateRegistryView:
    def __init__(self, registry: StateRegistry) -> None:
        self._registry = registry

    @property
    def count(self) -> int:
        return self._registry.count

    def contains(self, state: dict[str, Any]) -> bool:
        return self._registry.contains(state)

    def ids(self) -> tuple[str, ...]:
        return tuple(self._registry.ids())


class BranchRegistryView:
    def __init__(self, registry: BranchRegistry) -> None:
        self._registry = registry

    @property
    def count(self) -> int:
        return self._registry.count

    def all(self) -> tuple[BranchRecord, ...]:
        return self._registry.all()

    def by_status(self, merge_status: str) -> tuple[BranchRecord, ...]:
        return self._registry.by_status(merge_status)

    def by_state(self, state_id: str) -> tuple[BranchRecord, ...]:
        return self._registry.by_state(state_id)

    def lineage(self, branch_id: str) -> tuple[BranchRecord, ...]:
        return self._registry.lineage(branch_id)

    def ids(self) -> tuple[str, ...]:
        return tuple(self._registry.ids())


@dataclass
class ControlTask:
    task_id: str
    envelope: GovernanceEnvelope
    depth: int = 0
    lineage_id: str | None = None
    _state: TaskState = field(default=TaskState.RECEIVED, init=False, repr=False)
    _state_history: list[str] = field(default_factory=list, init=False, repr=False)
    _concurrency_acquired: bool = field(default=False, init=False, repr=False)
    _last_tgl_status: str | None = field(default=None, init=False, repr=False)
    _last_tgl_seal: str | None = field(default=None, init=False, repr=False)
    _identity_sealed: bool = field(default=False, init=False, repr=False)

    _IMMUTABLE_FIELDS = frozenset({"task_id", "envelope", "depth", "lineage_id"})

    def __post_init__(self) -> None:
        if self.lineage_id is None:
            object.__setattr__(self, "lineage_id", self.envelope.trace_id)
        if self.depth < 0:
            raise ValueError("depth must be non-negative")
        object.__setattr__(self, "_identity_sealed", True)

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_identity_sealed", False) and name in self._IMMUTABLE_FIELDS:
            current = getattr(self, name)
            if value != current:
                raise ControlPlaneViolation(f"immutable task identity field: {name}")
        if name in {"state", "state_history", "concurrency_acquired", "last_tgl_status", "last_tgl_seal"}:
            raise AttributeError(f"{name} is controller-managed")
        object.__setattr__(self, name, value)

    @property
    def state(self) -> TaskState:
        return self._state

    @property
    def state_history(self) -> tuple[str, ...]:
        return tuple(self._state_history)

    @property
    def concurrency_acquired(self) -> bool:
        return self._concurrency_acquired

    @property
    def last_tgl_status(self) -> str | None:
        return self._last_tgl_status

    @property
    def last_tgl_seal(self) -> str | None:
        return self._last_tgl_seal

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
        self._tgl_runner = tgl_runner
        self._state_registry = StateRegistry()
        self._branches = BranchRegistry()
        self._tasks: dict[str, ControlTask] = {}
        self._ledgers: dict[str, BudgetLedger] = {}
        self._events: list[dict[str, object]] = []
        self._lineage_active: dict[str, int] = {}
        self._lineage_limits: dict[str, int] = {}

    @property
    def tgl_runner(self) -> Callable[..., Any] | None:
        return self._tgl_runner

    @property
    def tasks(self) -> Mapping[str, ControlTask]:
        return MappingProxyType(self._tasks)

    @property
    def ledgers(self) -> Mapping[str, LedgerView]:
        return MappingProxyType(
            {
                task_id: LedgerView(
                    budget=ledger.budget,
                    consumed=ledger.consumed,
                    reserved=ledger.reserved,
                    active_concurrency=ledger.active_concurrency,
                )
                for task_id, ledger in self._ledgers.items()
            }
        )

    @property
    def events(self) -> tuple[dict[str, object], ...]:
        return tuple(dict(event) for event in self._events)

    @property
    def state_registry(self) -> StateRegistryView:
        return StateRegistryView(self._state_registry)

    @property
    def branches(self) -> BranchRegistryView:
        return BranchRegistryView(self._branches)

    def submit(self, task: ControlTask) -> None:
        if task.task_id in self._tasks:
            raise ControlPlaneViolation(f"duplicate task_id: {task.task_id}")
        lineage = task.lineage_id or task.envelope.trace_id
        self._lineage_limits.setdefault(lineage, task.envelope.budget.max_concurrency)
        self._tasks[task.task_id] = task
        self._ledgers[task.task_id] = BudgetLedger(task.envelope.budget)
        self._transition(task, TaskState.PREFLIGHT)

    def admit(self, task_id: str) -> None:
        self._transition(self._task(task_id), TaskState.ADMITTED)

    def _set_runtime(
        self,
        task: ControlTask,
        *,
        state: TaskState | None = None,
        concurrency: bool | None = None,
        tgl_status: str | None = None,
        tgl_seal: str | None = None,
        reset_tgl: bool = False,
    ) -> None:
        if state is not None:
            object.__setattr__(task, "_state", state)
        if concurrency is not None:
            object.__setattr__(task, "_concurrency_acquired", concurrency)
        if reset_tgl:
            object.__setattr__(task, "_last_tgl_status", None)
            object.__setattr__(task, "_last_tgl_seal", None)
        if tgl_status is not None:
            object.__setattr__(task, "_last_tgl_status", tgl_status)
        if tgl_seal is not None:
            object.__setattr__(task, "_last_tgl_seal", tgl_seal)

    def _release_concurrency(self, task: ControlTask) -> None:
        if not task.concurrency_acquired:
            return
        self._ledgers[task.task_id].release_concurrency()
        lineage = task.lineage_id or task.envelope.trace_id
        self._lineage_active[lineage] = max(0, self._lineage_active.get(lineage, 0) - 1)
        self._set_runtime(task, concurrency=False)

    def _escalate(self, task: ControlTask, reason: str) -> None:
        if task.state is not TaskState.ESCALATED:
            self._transition(task, TaskState.ESCALATED)
        self._events.append({"event": "ESCALATION", "task_id": task.task_id, "reason": reason})
        self._release_concurrency(task)

    def start_expansion(self, task_id: str) -> None:
        task = self._task(task_id)
        if TaskState.EXPANDING not in _ALLOWED[task.state]:
            raise ControlPlaneViolation(f"illegal transition {task.state.value} -> {TaskState.EXPANDING.value}")
        lineage = task.lineage_id or task.envelope.trace_id
        if task.depth >= task.envelope.budget.max_depth:
            self._escalate(task, "maximum recursion depth reached")
            return
        if self._lineage_active.get(lineage, 0) >= self._lineage_limits[lineage]:
            self._escalate(task, "active concurrency limit reached")
            return
