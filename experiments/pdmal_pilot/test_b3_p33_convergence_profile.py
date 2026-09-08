import math

import pytest

from experiments.pdmal_pilot.b3_p33_convergence_profile import (
    PersistentP33Sequence,
    run_registered_sequence,
)


def test_registered_sequence_exercises_p33_status_ladder_and_recovery() -> None:
    result = run_registered_sequence()
    statuses = [event["status"] for event in result["events"]]
    assert statuses == ["stable", "watch", "warn", "alert", "stable", "stable", "converged"]
    assert result["monitor_summary"]["total_alerts"] == 1
    assert result["monitor_summary"]["current_status"] == "converged"
    assert result["scientific_n_increment"] == 0
    assert result["empirical_execution_authorized"] is False
    assert result["consensus_alpha_mapping"] == "PROHIBITED"


def test_state_persists_within_sequence() -> None:
    seq = PersistentP33Sequence("persist", {("a", "b"): 0.5, ("a", "c"): 0.5})
    seq.apply("t1", {("a", "b"): 0.5, ("a", "c"): 0.5})
    seq.apply("t2", {("a", "b"): 0.6, ("a", "c"): 0.4})
    assert seq.monitor._prev_weights == {("a", "b"): 0.6, ("a", "c"): 0.4}
    assert seq.monitor._consec_div == 1
    assert len(seq.monitor._events) == 2


def test_new_sequence_resets_monitor_state() -> None:
    first = PersistentP33Sequence("one", {("a", "b"): 0.5, ("a", "c"): 0.5})
    first.apply("t1", {("a", "b"): 0.5, ("a", "c"): 0.5})
    first.apply("t2", {("a", "b"): 0.6, ("a", "c"): 0.4})
    second = PersistentP33Sequence("two", {("a", "b"): 0.8, ("a", "c"): 0.2})
    result = second.apply("t1", {("a", "b"): 0.8, ("a", "c"): 0.2})
    assert result["status"] == "stable"
    assert result["turn_number"] == 1
    assert len(second.monitor._events) == 1


@pytest.mark.parametrize(
    "snapshot",
    [
        {("a", "b"): 1.0},
        {("a", "b"): 0.5, ("a", "c"): 0.4, ("x", "y"): 0.1},
        {("a", "b"): "0.5", ("a", "c"): 0.5},
        {("a", "b"): math.inf, ("a", "c"): 0.0},
        {("a", "b"): 0.6, ("a", "c"): 0.5},
    ],
)
def test_malformed_graph_state_fails_closed(snapshot) -> None:
    with pytest.raises(ValueError):
        PersistentP33Sequence("bad", snapshot)


def test_empty_sequence_id_fails_closed() -> None:
    with pytest.raises(ValueError):
        PersistentP33Sequence("", {("a", "b"): 0.5, ("a", "c"): 0.5})
