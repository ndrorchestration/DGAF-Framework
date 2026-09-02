"""Deterministic PDMAL task execution and frozen retry engine.

The retry engine is protocol mechanics. ``ConsensusTask`` is the pre-pilot real
workload defined by PDMAL task specification v0.7.4. Pilot mode remains gated by
protocol freeze and explicit authorization in ``run_pilot.py``.
"""
from __future__ import annotations

import hashlib
import multiprocessing
from dataclasses import dataclass, field
from enum import Enum
from queue import Empty
from time import monotonic, sleep
from typing import Any, Callable, Protocol

import numpy as np

from harness_contract import TOPOLOGY_SPECS, generate_topology, make_streams, validate_topology
from topology_utils import graph_fingerprint

TRIAL_TIMEOUT_SECONDS = 60.0
RECOVERY_WINDOW_SECONDS = 30.0
MAX_ATTEMPTS = 3
SEED_RUNTIME_CEILING_SECONDS = 300.0
CONSENSUS_ITERATIONS = 100
FAILURE_INJECTION_ITERATION = 33
FAILURE_RECOVERY_ITERATION = 66
CONDITION_VALUES = ("null", "simple", "static", "dgaf")
PILOT_FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
CONSENSUS_THRESHOLD = 0.01


class AttemptStatus(str, Enum):
    SUCCESS = "SUCCESS"
    TIMEOUT = "TIMEOUT"
    FAILURE = "FAILURE"


class TrialStatus(str, Enum):
    SUCCESS = "SUCCESS"
    RECOVERED = "RECOVERED"
    UNRECOVERED_FAILURE = "UNRECOVERED_FAILURE"


class TaskAdapter(Protocol):
    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        """Run exactly one task attempt."""


@dataclass(frozen=True)
class AttemptResult:
    attempt: int
    status: AttemptStatus
    elapsed_seconds: float
    isolated: bool = False
    termination_reason: str | None = None


@dataclass(frozen=True)
class TrialResult:
    status: TrialStatus
    attempts: tuple[AttemptResult, ...]
    recovery_wait_seconds: float

    @property
    def ffcr_success(self) -> bool:
        return self.status in {TrialStatus.SUCCESS, TrialStatus.RECOVERED}


@dataclass(frozen=True)
class RetryPolicy:
    timeout_seconds: float = TRIAL_TIMEOUT_SECONDS
    recovery_window_seconds: float = RECOVERY_WINDOW_SECONDS
    max_attempts: int = MAX_ATTEMPTS

    def validate(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.recovery_window_seconds < 0:
            raise ValueError("recovery_window_seconds cannot be negative")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")


def _task_worker(result_queue, task: TaskAdapter, seed: int, condition: str, attempt: int) -> None:
    try:
        status = task.run(seed=seed, condition=condition, attempt=attempt)
        if not isinstance(status, AttemptStatus):
            status = AttemptStatus(status)
        result_queue.put((status.value, None))
    except Exception as exc:
        result_queue.put((AttemptStatus.FAILURE.value, f"{type(exc).__name__}: {exc}"))


def run_task_with_timeout(
    task: TaskAdapter,
    *,
    seed: int,
    condition: str,
    attempt: int,
    timeout_seconds: float,
    clock: Callable[[], float] = monotonic,
) -> tuple[AttemptStatus, float, str | None]:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    ctx = multiprocessing.get_context("spawn")
    result_queue = ctx.Queue(maxsize=1)
    process = ctx.Process(target=_task_worker, args=(result_queue, task, seed, condition, attempt))
    started = clock()
    try:
        process.start()
    except Exception as exc:
        result_queue.close()
        result_queue.join_thread()
        return AttemptStatus.FAILURE, max(0.0, clock() - started), f"process-start-failed:{type(exc).__name__}: {exc}"
    process.join(timeout_seconds)
    elapsed = max(0.0, clock() - started)
    if process.is_alive():
        process.terminate()
        process.join(0.1)
        if process.is_alive() and hasattr(process, "kill"):
            process.kill()
            process.join(0.1)
        result_queue.close()
        result_queue.join_thread()
        return AttemptStatus.TIMEOUT, elapsed, "process-terminated-on-timeout"
    try:
        raw_status, error = result_queue.get(timeout=1.0)
    except Empty:
        result = (
            AttemptStatus.FAILURE,
            elapsed,
            "child-exited-without-result" if process.exitcode == 0 else f"child-exit-code:{process.exitcode}",
        )
    else:
        if raw_status == AttemptStatus.TIMEOUT.value:
            result = AttemptStatus.TIMEOUT, elapsed, error
        elif raw_status == AttemptStatus.FAILURE.value:
            result = AttemptStatus.FAILURE, elapsed, error
        else:
            result = AttemptStatus.SUCCESS, elapsed, None
    finally:
        result_queue.close()
        result_queue.join_thread()
    return result


def execute_trial(
    task: TaskAdapter,
    *,
    seed: int,
    condition: str,
    policy: RetryPolicy = RetryPolicy(),
    monotonic_clock: Callable[[], float] = monotonic,
    sleeper: Callable[[float], None] = sleep,
    isolate: bool = True,
) -> TrialResult:
    """Execute a trial under the frozen retry semantics."""
    policy.validate()
    results: list[AttemptResult] = []
    recovery_wait = 0.0
    for attempt in range(1, policy.max_attempts + 1):
        started = monotonic_clock()
        termination_reason: str | None = None
        if isolate:
            status, isolated_elapsed, termination_reason = run_task_with_timeout(
                task, seed=seed, condition=condition, attempt=attempt,
                timeout_seconds=policy.timeout_seconds, clock=monotonic_clock,
            )
            elapsed = isolated_elapsed
        else:
            status = task.run(seed=seed, condition=condition, attempt=attempt)
            elapsed = max(0.0, monotonic_clock() - started)
            if elapsed > policy.timeout_seconds and status == AttemptStatus.SUCCESS:
                status = AttemptStatus.TIMEOUT
                termination_reason = "elapsed-time-classification"
        results.append(AttemptResult(attempt, status, elapsed, isolate, termination_reason))
        if status == AttemptStatus.SUCCESS:
            final = TrialStatus.SUCCESS if attempt == 1 else TrialStatus.RECOVERED
            return TrialResult(final, tuple(results), recovery_wait)
        if attempt < policy.max_attempts:
            recovery_wait += policy.recovery_window_seconds
            sleeper(policy.recovery_window_seconds)
    return TrialResult(TrialStatus.UNRECOVERED_FAILURE, tuple(results), recovery_wait)


def validate_seed_runtime(elapsed_seconds: float) -> bool:
    if elapsed_seconds < 0:
        raise ValueError("elapsed_seconds cannot be negative")
    return elapsed_seconds <= SEED_RUNTIME_CEILING_SECONDS


@dataclass(frozen=True)
class ConsensusTrialResult:
    trial_key: str
    condition: str
    topology: str
    failure_count: int
    failure_nodes: tuple[int, ...]
    initial_values: tuple[float, ...]
    final_values: tuple[float, ...]
    final_std: float
    topology_fingerprint: str
    iterations_completed: int
    attempt_status: AttemptStatus
    deviation: str | None = None
    governance_trace: tuple[dict[str, Any], ...] = ()

    @property
    def consensus_success(self) -> bool:
        return self.final_std < CONSENSUS_THRESHOLD and self.attempt_status is AttemptStatus.SUCCESS


class ConsensusTask:
    """Deterministic v0.7.4 endogenous-consensus workload.

    Trial identity is (seed, topology, condition, failure_count). ``attempt``
    never influences topology, initial state, or failure selection.
    """

    def __init__(
        self,
        *,
        topology: str,
        failure_count: int,
        condition: str,
        premise_check_fn: Callable[[str, Any], bool] | None = None,
    ) -> None:
        if topology not in TOPOLOGY_SPECS:
            raise ValueError(f"unsupported topology: {topology!r}")
        if condition not in CONDITION_VALUES:
            raise ValueError(f"unsupported pilot condition: {condition!r}")
        if not isinstance(failure_count, int) or isinstance(failure_count, bool) or failure_count not in PILOT_FAILURE_COUNTS:
            raise ValueError(f"failure_count must be one of {PILOT_FAILURE_COUNTS!r}")
        if condition == "dgaf" and not callable(premise_check_fn):
            raise ValueError("dgaf condition requires an explicit P-35 premise_check_fn; omission is fail-closed")
        self.topology = topology
        self.failure_count = failure_count
        self.condition = condition
        self.premise_check_fn = premise_check_fn

    @staticmethod
    def trial_key(seed: int, topology: str, condition: str, failure_count: int) -> str:
        return hashlib.sha256(f"{seed}|{topology}|{condition}|{failure_count}".encode()).hexdigest()

    def _build_trial_inputs(self, seed: int):
        streams = make_streams(seed)
        graph = generate_topology(self.topology, streams["topology_construction"])
        validate_topology(graph, self.topology)
        initial_values = tuple(float(x) for x in streams["task_initialization"].uniform(-1.0, 1.0, size=20))
        failure_nodes = tuple(sorted(int(x) for x in streams["failure_injection"].choice(20, size=self.failure_count, replace=False)))
        return graph, initial_values, failure_nodes

    @staticmethod
    def _active_neighbors(graph, failed: set[int]) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(sorted(j for j in graph.neighbors(i) if j not in failed)) for i in range(20))

    @staticmethod
    def _null_or_simple_update(values: np.ndarray, active_neighbors: tuple[tuple[int, ...], ...], alpha: float) -> np.ndarray:
        next_values = values.copy()
        for i, neighbors in enumerate(active_neighbors):
            if neighbors:
                avg = float(np.mean([values[j] for j in neighbors]))
                next_values[i] = (1.0 - alpha) * values[i] + alpha * avg
        return next_values

    @staticmethod
    def _static_update(values: np.ndarray, graph, active_neighbors: tuple[tuple[int, ...], ...]) -> np.ndarray:
        original_degrees = dict(graph.degree())
        weights = {(i, j): 1.0 / max(original_degrees[i], original_degrees[j]) for i, j in graph.edges()}
        weights.update({(j, i): w for (i, j), w in list(weights.items())})
        next_values = values.copy()
        for i, neighbors in enumerate(active_neighbors):
            if not neighbors:
                continue
            sum_w = sum(weights[(i, j)] for j in neighbors)
            if sum_w <= 0.0:
                continue
            weighted_sum = sum(weights[(i, j)] * values[j] for j in neighbors)
            next_values[i] = (1.0 - sum_w) * values[i] + weighted_sum
        return next_values

    def _dgaf_update(self, *, seed: int, iteration: int, values: np.ndarray, graph, alive: tuple[bool, ...],
                     active_neighbors: tuple[tuple[int, ...], ...], failure_history: tuple[tuple[int, ...], ...],
                     failure_count_current: int, failure_count_total: int):
        from dgaf_tgl_adapter import ConsensusState, DGAF_TGLAdapter

        adapter = DGAF_TGLAdapter(
            session_id=f"pdmAL-{self.trial_key(seed, self.topology, self.condition, self.failure_count)}",
            premise_check_fn=self.premise_check_fn,
        )
        state = ConsensusState(
            seed_id=seed,
            iteration=iteration,
            agent_values=tuple(float(x) for x in values),
            alive=alive,
            original_neighbors=tuple(tuple(sorted(graph.neighbors(i))) for i in range(20)),
            active_neighbors=active_neighbors,
            failure_history=failure_history,
            failure_count_current=failure_count_current,
            failure_count_total=failure_count_total,
            current_final_std=float(np.std(values)),
            current_mean=float(np.mean(values)),
            runtime_budget_remaining_ms=int(SEED_RUNTIME_CEILING_SECONDS * 1000),
            protocol_id="PDMAL-PREFREEZE-V1",
        )
        try:
            result = adapter.run_turn(state)
        except Exception as exc:
            return values, AttemptStatus.FAILURE, f"dgaf-adapter-error:{type(exc).__name__}: {exc}", None
        governance_trace = result.audit.to_dict()
        governance_trace["decision"] = result.decision
        governance_trace["outcome"] = result.attempt_status.value
        if result.decision == "FAIL_CLOSED" or result.next_values is None:
            return values, AttemptStatus.FAILURE, "dgaf-fail-closed", governance_trace
        return np.asarray(result.next_values, dtype=float), AttemptStatus.SUCCESS, None, governance_trace

    def run_detailed(self, *, seed: int, attempt: int = 1) -> ConsensusTrialResult:
        del attempt
        trial_key = self.trial_key(seed, self.topology, self.condition, self.failure_count)
        graph, initial_values, failure_nodes = self._build_trial_inputs(seed)
        values = np.asarray(initial_values, dtype=float)
        failed: set[int] = set()
        failure_history: tuple[tuple[int, ...], ...] = ()
        deviation: str | None = None
        governance_trace: list[dict[str, Any]] = []

        for iteration in range(CONSENSUS_ITERATIONS):
            if iteration == FAILURE_INJECTION_ITERATION:
                failed = set(failure_nodes)
                failure_history = (failure_nodes,) if failure_nodes else ()
            elif iteration == FAILURE_RECOVERY_ITERATION:
                failed = set()

            alive = tuple(i not in failed for i in range(20))
            active_neighbors = self._active_neighbors(graph, failed)
            failure_count_current = len(failed)
            failure_count_total = len(failure_history[-1]) if failure_history else 0

            if self.condition == "null":
                values, status = self._null_or_simple_update(values, active_neighbors, 0.5), AttemptStatus.SUCCESS
            elif self.condition == "simple":
                values, status = self._null_or_simple_update(values, active_neighbors, 0.2), AttemptStatus.SUCCESS
            elif self.condition == "static":
                values, status = self._static_update(values, graph, active_neighbors), AttemptStatus.SUCCESS
            else:
                values, status, deviation, trace = self._dgaf_update(
                    seed=seed, iteration=iteration, values=values, graph=graph, alive=alive,
                    active_neighbors=active_neighbors, failure_history=failure_history,
                    failure_count_current=failure_count_current, failure_count_total=failure_count_total,
                )
                if trace is not None:
                    governance_trace.append(trace)

            if status is AttemptStatus.FAILURE:
                return ConsensusTrialResult(
                    trial_key, self.condition, self.topology, self.failure_count, failure_nodes,
                    initial_values, tuple(float(x) for x in values), float(np.std(values)),
                    graph_fingerprint(graph), iteration + 1, AttemptStatus.FAILURE, deviation,
                    tuple(governance_trace),
                )

        return ConsensusTrialResult(
            trial_key, self.condition, self.topology, self.failure_count, failure_nodes,
            initial_values, tuple(float(x) for x in values), float(np.std(values)),
            graph_fingerprint(graph), CONSENSUS_ITERATIONS, AttemptStatus.SUCCESS, deviation,
            tuple(governance_trace),
        )

    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        if condition != self.condition:
            raise ValueError("attempt condition does not match task condition")
        return self.run_detailed(seed=seed, attempt=attempt).attempt_status


@dataclass
class ScriptedTask:
    """Deterministic contract-test adapter for retry mechanics only."""
    statuses: list[AttemptStatus]
    calls: list[int] = field(default_factory=list)

    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        del seed, condition
        self.calls.append(attempt)
        if not self.statuses:
            raise AssertionError("scripted task exhausted")
        return self.statuses.pop(0)
