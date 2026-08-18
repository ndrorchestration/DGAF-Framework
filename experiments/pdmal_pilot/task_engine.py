"""Deterministic, pre-freeze task execution and retry engine.

This module implements protocol mechanics only. It is deliberately independent
of the real experimental task and is safe for contract-mode validation.

No empirical workload is defined here. A future real task adapter must satisfy
TaskAdapter and may only be invoked by the pilot runner after protocol freeze
and explicit authorization.
"""

from __future__ import annotations

import multiprocessing
from dataclasses import dataclass, field
from enum import Enum
from queue import Empty
from time import monotonic, sleep
from typing import Callable, Protocol

TRIAL_TIMEOUT_SECONDS = 60.0
RECOVERY_WINDOW_SECONDS = 30.0
MAX_ATTEMPTS = 3
SEED_RUNTIME_CEILING_SECONDS = 300.0


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
    """Run one task attempt in an isolated process and enforce a hard timeout.

    The task adapter must be process-safe/picklable under the platform's spawn
    semantics. When the deadline expires, the child process is terminated and
    the parent classifies the attempt as TIMEOUT without waiting for the task.
    """
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

    By default, each task attempt executes in a separate process. Contract tests
    may set ``isolate=False`` when they need deterministic clock injection for
    pure state-machine tests. The pilot/contract runner uses the isolated path.
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

    return TrialResult(
        TrialStatus.UNRECOVERED_FAILURE,
        tuple(results),
        recovery_wait,
    )


def validate_seed_runtime(elapsed_seconds: float) -> bool:
    """Return whether a seed is within the separate 300-second runtime ceiling."""
    if elapsed_seconds < 0:
        raise ValueError("elapsed_seconds cannot be negative")
    return elapsed_seconds <= SEED_RUNTIME_CEILING_SECONDS


@dataclass
class ScriptedTask:
    """Deterministic contract-test adapter; not an empirical workload."""

    statuses: list[AttemptStatus]
    calls: list[int] = field(default_factory=list)

    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        self.calls.append(attempt)
        if not self.statuses:
            raise AssertionError("scripted task exhausted")
        return self.statuses.pop(0)
