from __future__ import annotations

from time import monotonic, sleep

import numpy as np
import pytest

from task_engine import (
    AttemptStatus,
    ConsensusTask,
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


def allow_all_premises(_text, _invariant) -> bool:
    return True


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
    with pytest.raises(ValueError):
        RetryPolicy(timeout_seconds=0).validate()
    with pytest.raises(ValueError):
        RetryPolicy(recovery_window_seconds=-1).validate()
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0).validate()


def test_dgaf_consensus_task_requires_explicit_premise_checker():
    with pytest.raises(ValueError, match="explicit P-35 premise_check_fn"):
        ConsensusTask(topology="ring", failure_count=2, condition="dgaf")


def test_consensus_task_is_deterministic_across_attempts():
    for condition in ("null", "simple", "static"):
        task = ConsensusTask(topology="ring", failure_count=2, condition=condition)
        first = task.run_detailed(seed=20260817, attempt=1)
        second = task.run_detailed(seed=20260817, attempt=2)

        assert first.trial_key == second.trial_key
        assert first.failure_nodes == second.failure_nodes
        assert first.initial_values == second.initial_values
        assert first.final_values == second.final_values
        assert first.final_std == second.final_std
        assert first.topology_fingerprint == second.topology_fingerprint
        assert first.iterations_completed == second.iterations_completed
        assert first.attempt_status is second.attempt_status


def test_dgaf_consensus_task_is_deterministic_across_attempts_with_explicit_checker():
    task = ConsensusTask(
        topology="ring",
        failure_count=2,
        condition="dgaf",
        premise_check_fn=allow_all_premises,
    )
    first = task.run_detailed(seed=20260817, attempt=1)
    second = task.run_detailed(seed=20260817, attempt=2)

    assert first.trial_key == second.trial_key
    assert first.failure_nodes == second.failure_nodes
    assert first.initial_values == second.initial_values
    assert first.final_values == second.final_values
    assert first.final_std == second.final_std
    assert first.topology_fingerprint == second.topology_fingerprint
    assert first.iterations_completed == second.iterations_completed
    assert first.attempt_status is second.attempt_status


def test_consensus_task_completes_exactly_100_iterations_for_non_dgaf_conditions():
    for condition in ("null", "simple", "static"):
        result = ConsensusTask(topology="ring", failure_count=2, condition=condition).run_detailed(
            seed=20260817,
            attempt=1,
        )
        assert result.attempt_status is AttemptStatus.SUCCESS
        assert result.iterations_completed == 100
        assert len(result.final_values) == 20
        assert np.isfinite(result.final_std)


def test_consensus_task_accepts_only_pilot_condition_set():
    with pytest.raises(ValueError):
        ConsensusTask(topology="ring", failure_count=1, condition="dgaf_pdmal")

    for condition in ("null", "simple", "static"):
        task = ConsensusTask(topology="ring", failure_count=0, condition=condition)
        assert task.condition == condition

    task = ConsensusTask(
        topology="ring",
        failure_count=0,
        condition="dgaf",
        premise_check_fn=allow_all_premises,
    )
    assert task.condition == "dgaf"


def test_consensus_task_rejects_out_of_contract_failure_counts():
    for bad in (-1, 7, 11, 20, True):
        with pytest.raises(ValueError):
            ConsensusTask(topology="ring", failure_count=bad, condition="null")


def test_consensus_trial_identity_excludes_attempt():
    task_a = ConsensusTask(topology="complete", failure_count=3, condition="simple")
    task_b = ConsensusTask(topology="complete", failure_count=3, condition="simple")
    assert task_a.trial_key(20260817, "complete", "simple", 3) == task_b.trial_key(
        20260817, "complete", "simple", 3
    )
    assert task_a.trial_key(20260817, "complete", "simple", 3) != task_a.trial_key(
        20260818, "complete", "simple", 3
    )


def test_failed_nodes_are_excluded_and_restored_in_neighbor_state():
    task = ConsensusTask(topology="ring", failure_count=1, condition="null")
    graph, initial_values, failure_nodes = task._build_trial_inputs(20260817)
    failed = set(failure_nodes)
    values = np.asarray(initial_values, dtype=float)

    pre = task._active_neighbors(graph, set())
    during = task._active_neighbors(graph, failed)
    post = task._active_neighbors(graph, set())

    assert len(pre) == len(during) == len(post) == 20
    failed_node = failure_nodes[0]
    assert failed_node not in sum((list(x) for x in during), [])
    assert failed_node in sum((list(x) for x in pre), [])
    assert failed_node in sum((list(x) for x in post), [])
    assert values.shape == (20,)


def test_fail_closed_maps_to_attempt_failure_and_retry_engine():
    task = ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.SUCCESS])
    result = execute_trial(
        task,
        seed=20260817,
        condition="dgaf",
        policy=RetryPolicy(recovery_window_seconds=0.0),
        sleeper=lambda _: None,
        isolate=False,
    )
    assert result.status is TrialStatus.RECOVERED
    assert [attempt.status for attempt in result.attempts] == [
        AttemptStatus.FAILURE,
        AttemptStatus.SUCCESS,
    ]
