import pytest

from scripts import p4_mode_t_round_policy as policy


def test_round_one_is_genesis():
    assert policy.round_time_unix(1) == policy.QUICKNET_GENESIS_TIME_UNIX


def test_round_times_advance_by_exact_quicknet_period():
    assert policy.round_time_unix(2) == policy.QUICKNET_GENESIS_TIME_UNIX + 3
    assert policy.round_time_unix(100) - policy.round_time_unix(99) == 3


def test_first_round_at_or_after_is_boundary_correct():
    genesis = policy.QUICKNET_GENESIS_TIME_UNIX
    assert policy.first_round_at_or_after(genesis) == 1
    assert policy.first_round_at_or_after(genesis + 1) == 2
    assert policy.first_round_at_or_after(genesis + 3) == 2
    assert policy.first_round_at_or_after(genesis + 4) == 3


def test_release_round_is_derived_only_from_consumption_time_and_frozen_window():
    c_time = policy.QUICKNET_GENESIS_TIME_UNIX + 30
    release_round = policy.select_release_round(c_time, 10)
    release_time = policy.round_time_unix(release_round)
    assert release_time >= c_time + 10
    assert policy.round_time_unix(release_round - 1) < c_time + 10


def test_analysis_lock_must_be_strictly_before_release():
    release_round = 10
    release_time = policy.round_time_unix(release_round)
    assert policy.analysis_lock_precedes_release(release_time - 1, release_round) is True
    assert policy.analysis_lock_precedes_release(release_time, release_round) is False
    assert policy.analysis_lock_precedes_release(release_time + 1, release_round) is False


@pytest.mark.parametrize("bad_round", [0, -1, True, 1.5, "1"])
def test_invalid_round_numbers_fail_closed(bad_round):
    with pytest.raises(ValueError):
        policy.round_time_unix(bad_round)


@pytest.mark.parametrize("bad_window", [0, -1, True, 1.5, "60"])
def test_invalid_analysis_lock_windows_fail_closed(bad_window):
    with pytest.raises(ValueError):
        policy.select_release_round(policy.QUICKNET_GENESIS_TIME_UNIX + 10, bad_window)
