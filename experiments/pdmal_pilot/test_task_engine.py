from __future__ import annotations

from time import monotonic, sleep

from task_engine import (
    AttemptStatus,
    RetryPolicy,
    ScriptedTask,
    TrialStatus,
    execute_trial,
    run_task_with_timeout,
    validate_seed_runtime,
)


class HangingTask:
    """Pickle-safe deterministic adapter used only to test hard timeout isolation."""

    def run(self, *, seed: int, condition: str, attempt: int) -> AttemptStatus:
        del seed, condition, attempt
        sleep(5.0)
        return AttemptStatus.SUCCESS


def fake_clock_factory(values):
    iterator = iter(values)
    return lambda: next(iterator)


def test_first_attempt_success():
    task = ScriptedTask([AttemptStatus.SUCCESS])
    result = execute_trial(
        task,
        seed=1,
        condition="contract",
        monotonic_clock=fake_clock_factory([0.0, 1.0]),
        sleeper=lambda _: None,
        isolate=False,
    )
    assert result.status is TrialStatus.SUCCESS
    assert result.ffcr_success is True
    assert result.attempts[0].attempt == 1


def test_failure_then_recovery_is_recovered():
    task = ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.SUCCESS])
    result = execute_trial(
        task,
        seed=1,
        condition="contract",
        policy=RetryPolicy(recovery_window_seconds=0.0),
        monotonic_clock=fake_clock_factory([0.0, 1.0, 2.0, 3.0]),
        sleeper=lambda _: None,
        isolate=False,
    )
    assert result.status is TrialStatus.RECOVERED
    assert result.attempts[-1].attempt == 2
    assert result.ffcr_success is True


def test_retry_exhaustion_is_unrecovered_failure():
    task = ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.TIMEOUT, AttemptStatus.FAILURE])
    result = execute_trial(
        task,
        seed=1,
        condition="contract",
        policy=RetryPolicy(recovery_window_seconds=0.0),
        monotonic_clock=fake_clock_factory([0.0, 1.0, 2.0, 3.0, 4.0, 5.0]),
        sleeper=lambda _: None,
        isolate=False,
    )
    assert result.status is TrialStatus.UNRECOVERED_FAILURE
    assert result.ffcr_success is False
    assert len(result.attempts) == 3


def test_successful_attempt_over_timeout_becomes_timeout():
    task = ScriptedTask([AttemptStatus.SUCCESS])
    result = execute_trial(
        task,
        seed=1,
        condition="contract",
        policy=RetryPolicy(timeout_seconds=2.0, recovery_window_seconds=0.0, max_attempts=1),
        monotonic_clock=fake_clock_factory([0.0, 3.0]),
        sleeper=lambda _: None,
        isolate=False,
    )
    assert result.status is TrialStatus.UNRECOVERED_FAILURE
    assert result.attempts[0].status is AttemptStatus.TIMEOUT
    assert result.attempts[0].termination_reason == "elapsed-time-classification"


def test_hung_task_is_terminated_and_classified_timeout():
    started = monotonic()
    status, elapsed, termination_reason = run_task_with_timeout(
        HangingTask(),
        seed=1,
        condition="contract",
        attempt=1,
        timeout_seconds=0.2,
    )
    wall_clock = monotonic() - started

    assert status is AttemptStatus.TIMEOUT
    assert elapsed >= 0.15
    assert termination_reason == "process-terminated-on-timeout"
    assert wall_clock < 2.0


def test_isolated_execute_trial_records_hard_timeout():
    result = execute_trial(
        HangingTask(),
        seed=1,
        condition="contract",
        policy=RetryPolicy(timeout_seconds=0.2, recovery_window_seconds=0.0, max_attempts=1),
    )

    assert result.status is TrialStatus.UNRECOVERED_FAILURE
    assert result.attempts[0].status is AttemptStatus.TIMEOUT
    assert result.attempts[0].isolated is True
    assert result.attempts[0].termination_reason == "process-terminated-on-timeout"


def test_seed_runtime_ceiling_is_separate_from_ffcr():
    assert validate_seed_runtime(299.999)
    assert validate_seed_runtime(300.0)
    assert not validate_seed_runtime(300.001)


def test_policy_validation_rejects_invalid_values():
    import pytest

    with pytest.raises(ValueError):
        RetryPolicy(timeout_seconds=0).validate()
    with pytest.raises(ValueError):
        RetryPolicy(recovery_window_seconds=-1).validate()
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0).validate()
