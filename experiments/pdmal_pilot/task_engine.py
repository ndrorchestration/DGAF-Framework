"""Deterministic, pre-freeze task execution and retry engine.

This module implements protocol mechanics only. It is deliberately independent
of the real experimental task and is safe for contract-mode validation.

No empirical workload is defined here. A future real task adapter must satisfy
TaskAdapter and may only be invoked by the pilot runner after protocol freeze
and explicit authorization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
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


def execute_trial(
    task: TaskAdapter,
    *,
    seed: int,
    condition: str,
    policy: RetryPolicy = RetryPolicy(),
    monotonic_clock: Callable[[], float] = monotonic,
    sleeper: Callable[[float], None] = sleep,
) -> TrialResult:
    """Execute a trial under the frozen retry semantics.

    The task adapter returns SUCCESS/FAILURE/TIMEOUT. The engine owns retry,
    recovery-window accounting, and final FFCR classification.
    """
    policy.validate()
    results: list[AttemptResult] = []
    recovery_wait = 0.0

    for attempt in range(1, policy.max_attempts + 1):
        started = monotonic_clock()
        status = task.run(seed=seed, condition=condition, attempt=attempt)
        elapsed = max(0.0, monotonic_clock() - started)

        if elapsed > policy.timeout_seconds and status == AttemptStatus.SUCCESS:
            status = AttemptStatus.TIMEOUT

        results.append(AttemptResult(attempt, status, elapsed))

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
