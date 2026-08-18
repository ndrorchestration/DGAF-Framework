from __future__ import annotations

from task_engine import (
    AttemptStatus,
    RetryPolicy,
    ScriptedTask,
    TrialStatus,
    execute_trial,
    validate_seed_runtime,
)


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
        policy=RetryPolicy(timeout_seconds=2.0),
        monotonic_clock=fake_clock_factory([0.0, 3.0, 4.0, 5.0, 6.0]),
        sleeper=lambda _: None,
    )
    assert result.status is TrialStatus.UNRECOVERED_FAILURE
    assert result.attempts[0].status is AttemptStatus.TIMEOUT


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
