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
from typing import Callable, Protocol

import numpy as np

from dgaf_tgl_adapter import ConsensusState, DGAF_TGLAdapter
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
    """Run one isolated task attempt in a child process."""
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
    """Run one task attempt in an isolated process and enforce a hard timeout."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

    ctx = multiprocessing.get_context("spawn")
    result_queue = ctx.Queue(maxsize=1)
    process = ctx.Process(
        target=_task_worker,
        args=(result_queue, task, seed, condition, attempt),
    )

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
        if process.exitcode == 0:
            result = AttemptStatus.FAILURE, elapsed, "child-exited-without-result"
        else:
            result = AttemptStatus.FAILURE, elapsed, f"child-exit-code:{process.exitcode}"
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
    """Execute a trial under the frozen retry semantics.

    Each attempt receives the same trial identity; ``ConsensusTask`` derives all
    workload state from seed/topology/condition/failure-count rather than attempt.
    """
    policy.validate()
    results: list[AttemptResult] = []
    recovery_wait = 0.0

    for attempt in range(1, policy.max_attempts + 1):
        started = monotonic_clock()
        termination_reason: str | None = None

        if isolate:
            status, isolated_elapsed, termination_reason = run_task_with_timeout(
                task,
                seed=seed,
                condition=condition,
                attempt=attempt,
                timeout_seconds=policy.timeout_seconds,
                clock=monotonic,
            )
            elapsed = isolated_elapsed
        else:
            status = task.run(seed=seed, condition=condition, attempt=attempt)
            elapsed = max(0.0, monotonic_clock() - started)
            if elapsed > policy.timeout_seconds and status == AttemptStatus.SUCCESS:
                status = AttemptStatus.TIMEOUT
                termination_reason = "elapsed-time-classification"

        results.append(
            AttemptResult(
                attempt,
                status,
                elapsed,
                isolated=isolate,
                termination_reason=termination_reason,
            )
        )

        if status == AttemptStatus.SUCCESS:
            final = TrialStatus.SUCCESS if attempt == 1 else TrialStatus.RECOVERED
            return TrialResult(final, tuple(results), recovery_wait)

        if attempt < policy.max_attempts:
            recovery_wait += policy.recovery_window_seconds
            sleeper(policy.recovery_window_seconds)

    return TrialResult(TrialStatus.UNRECOVERED_FAILURE, tuple(results), recovery_wait)


def validate_seed_runtime(elapsed_seconds: float) -> bool:
    """Return whether a seed is within the separate 300-second runtime ceiling."""
    if elapsed_seconds < 0:
        raise ValueError("elapsed_seconds cannot be negative")
    return elapsed_seconds <= SEED_RUNTIME_CEILING_SECONDS


@dataclass(frozen=True)
class ConsensusTrialResult:
    """Detailed deterministic workload result for contract/runtime validation."""

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

    @property
    def consensus_success(self) -> bool:
        return self.final_std < CONSENSUS_THRESHOLD and self.attempt_status is AttemptStatus.SUCCESS


class ConsensusTask:
    """The v0.7.4 deterministic endogenous-consensus workload.

    Trial identity is ``(seed, topology, condition, failure_count)``. The
    ``attempt`` argument is intentionally ignored for state generation so retries
    reproduce the exact same topology, initial values, and failure set.
    """

    def __init__(self, *, topology: str, failure_count: int, condition: str) -> None:
        if topology not in TOPOLOGY_SPECS:
            raise ValueError(f"unsupported topology: {topology!r}")
        if condition not in CONDITION_VALUES:
            raise ValueError(f"unsupported pilot condition: {condition!r}")
        if not 0 <= failure_count <= 20:
            raise ValueError("failure_count must be between 0 and 20")
        self.topology = topology
        self.failure_count = failure_count
        self.condition = condition

    @staticmethod
    def trial_key(seed: int, topology: str, condition: str, failure_count: int) -> str:
        return hashlib.sha256(f"{seed}|{topology}|{condition}|{failure_count}".encode("utf-8")).hexdigest()

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
            if not neighbors:
                continue
            average = float(np.mean([values[j] for j in neighbors]))
            next_values[i] = (1.0 - alpha) * values[i] + alpha * average
        return next_values

    @staticmethod
    def _static_update(values: np.ndarray, graph, active_neighbors: tuple[tuple[int, ...], ...]) -> np.ndarray:
        original_degrees = dict(graph.degree())
        next_values = values.copy()
        weights = {
            (i, j): 1.0 / max(original_degrees[i], original_degrees[j])
            for i, j in graph.edges()
        }
        weights.update({(j, i): weight for (i, j), weight in list(weights.items())})
        for i, neighbors in enumerate(active_neighbors):
            if not neighbors:
                continue
            sum_w = sum(weights[(i, j)] for j in neighbors)
            if sum_w <= 0.0:
                continue
            weighted_sum = sum(weights[(i, j)] * values[j] for j in neighbors)
            next_values[i] = (1.0 - sum_w) * values[i] + weighted_sum
        return next_values

    def _dgaf_update(
        self,
        *,
        seed: int,
        iteration: int,
        values: np.ndarray,
        graph,
        alive: tuple[bool, ...],
        active_neighbors: tuple[tuple[int, ...], ...],
        failure_history: tuple[tuple[int, ...], ...],
        failure_count_current: int,
        failure_count_total: int,
    ) -> tuple[np.ndarray, AttemptStatus, str | None]:
        adapter = DGAF_TGLAdapter(
            session_id=f"pdmAL-{self.trial_key(seed, self.topology, self.condition, self.failure_count)}"
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
            return values, AttemptStatus.FAILURE, f"dgaf-adapter-error:{type(exc).__name__}: {exc}"
        if result.decision == "FAIL_CLOSED" or result.next_values is None:
            return values, AttemptStatus.FAILURE, "dgaf-fail-closed"
        return np.asarray(result.next_values, dtype=float), AttemptStatus.SUCCESS, None

    def run_detailed(self, *, seed: int, attempt: int = 1) -> ConsensusTrialResult:
        """Execute one deterministic attempt; ``attempt`` cannot change trial state."""
        del attempt
        trial_key = self.trial_key(seed, self.topology, self.condition, self.failure_count)
        graph, initial_values, failure_nodes = self._build_trial_inputs(seed)
        values = np.asarray(initial_values, dtype=float)
        failed: set[int] = set()
        failure_history: tuple[tuple[int, ...], ...] = ()
        deviation: str | None = None

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
                values = self._null_or_simple_update(values, active_neighbors, 0.5)
                status = AttemptStatus.SUCCESS
            elif self.condition == "simple":
                values = self._null_or_simple_update(values, active_neighbors, 0.2)
                status = AttemptStatus.SUCCESS
            elif self.condition == "static":
                values = self._static_update(values, graph, active_neighbors)
                status = AttemptStatus.SUCCESS
            else:
                values, status, deviation = self._dgaf_update(
                    seed=seed,
                    iteration=iteration,
                    values=values,
                    graph=graph,
                    alive=alive,
                    active_neighbors=active_neighbors,
                    failure_history=failure_history,
                    failure_count_current=failure_count_current,
                    failure_count_total=failure_count_total,
                )

            if status is AttemptStatus.FAILURE:
                return ConsensusTrialResult(
                    trial_key=trial_key,
                    condition=self.condition,
                    topology=self.topology,
                    failure_count=self.failure_count,
                    failure_nodes=failure_nodes,
                    initial_values=initial_values,
                    final_values=tuple(float(x) for x in values),
                    final_std=float(np.std(values)),
                    topology_fingerprint=graph_fingerprint(graph),
                    iterations_completed=iteration + 1,
                    attempt_status=AttemptStatus.FAILURE,
                    deviation=deviation,
                )

        return ConsensusTrialResult(
            trial_key=trial_key,
            condition=self.condition,
            topology=self.topology,
            failure_count=self.failure_count,
            failure_nodes=failure_nodes,
            initial_values=initial_values,
            final_values=tuple(float(x) for x in values),
            final_std=float(np.std(values)),
            topology_fingerprint=graph_fingerprint(graph),
            iterations_completed=CONSENSUS_ITERATIONS,
            attempt_status=AttemptStatus.SUCCESS,
        )

    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        """Run one attempt; ``condition`` must match the task's frozen identity."""
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
