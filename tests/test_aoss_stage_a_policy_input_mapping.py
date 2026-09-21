import pytest

from scripts.aoss_stage_a.policy_input_mapping import (
    MappingError,
    map_observation,
)
from scripts.aoss_v0_6_stage_a_decision_policy import evaluate_policy


def _observation(**overrides):
    value = {
        "terminal_event_kind": "task.completed",
        "terminal_event_count": 1,
        "freshness": "FRESH",
        "source_order_ambiguous": False,
        "authorization": "TRUE",
        "validation": "TRUE",
        "provenance_valid": "TRUE",
        "conflicted": False,
        "deadlock_candidate": False,
    }
    value.update(overrides)
    return value


def test_fresh_completion_maps_to_terminal_policy_input():
    state = map_observation(_observation())

    assert state.terminal is True
    assert state.blocked is False
    assert state.required_predicate_inconclusive is False


def test_fresh_noncompletion_terminal_maps_to_blocked():
    state = map_observation(_observation(terminal_event_kind="task.denied"))

    assert state.terminal is False
    assert state.blocked is True
    assert state.required_predicate_inconclusive is False


@pytest.mark.parametrize(
    "overrides",
    [
        {"freshness": "STALE"},
        {"freshness": "FUTURE_SKEW"},
        {"freshness": "INCONCLUSIVE"},
        {"terminal_event_kind": None, "terminal_event_count": 0},
        {"terminal_event_kind": None, "terminal_event_count": 2},
        {"source_order_ambiguous": True},
        {"authorization": "INCONCLUSIVE"},
    ],
)
def test_ambiguous_or_unfresh_observations_hold_without_action(overrides):
    state = map_observation(_observation(**overrides))

    assert state.terminal is False
    assert state.blocked is False
    assert state.uncertain is True
    assert state.required_predicate_inconclusive is True

    result = evaluate_policy(state)
    assert result.decision == "REQUEST_EVIDENCE"
    assert result.matched_rule == "UNCERTAIN"


@pytest.mark.parametrize(
    "field",
    [
        "authorization",
        "validation",
        "provenance_valid",
    ],
)
def test_missing_required_predicate_is_rejected(field):
    value = _observation()
    del value[field]

    with pytest.raises(MappingError, match="required mapping fields missing"):
        map_observation(value)


def test_unknown_terminal_kind_is_rejected():
    with pytest.raises(MappingError, match="terminal_event_kind is unknown"):
        map_observation(_observation(terminal_event_kind="task.started"))


def test_one_terminal_without_kind_is_rejected():
    with pytest.raises(MappingError, match="one terminal event"):
        map_observation(_observation(terminal_event_kind=None))


def test_multiple_terminals_cannot_be_relabelled_as_a_single_action():
    with pytest.raises(MappingError, match="ambiguous"):
        map_observation(
            _observation(
                terminal_event_kind="task.completed",
                terminal_event_count=2,
            )
        )
