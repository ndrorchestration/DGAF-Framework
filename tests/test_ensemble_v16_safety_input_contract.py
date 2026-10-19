"""Legacy v1.6 DemiJoule input validity; same-system engineering guard only."""

from types import MappingProxyType

import pytest

from components.ensemble_v16 import AgentAmethyst, DemiJouleGate

AXES = DemiJouleGate.AXES


def safe_scores() -> dict[str, float]:
    return dict.fromkeys(AXES, 0.9)


@pytest.mark.parametrize("score", [0.5, 0.9, 1.0])
def test_finite_normalized_threshold_positives(score: float) -> None:
    scores = dict.fromkeys(AXES, score)
    assert DemiJouleGate().safety_gate(scores)["decision"] == "PASS"


def test_read_only_mapping_supported() -> None:
    assert DemiJouleGate().safety_gate(MappingProxyType(safe_scores()))["decision"] == "PASS"


def test_missing_axis_fails_closed() -> None:
    scores = safe_scores()
    del scores["consent"]
    result = DemiJouleGate().safety_gate(scores)
    assert result["decision"] == "ESCALATE"
    assert "consent" in result["reason"]


@pytest.mark.parametrize(
    "invalid",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
        -0.1,
        1.1,
        True,
        False,
        "0.9",
        None,
        [],
        {},
        complex(0.9, 0),
        10**1000,
    ],
)
def test_nonfinite_malformed_or_unnormalized_score_fails_closed(invalid: object) -> None:
    scores: dict[str, object] = dict(safe_scores())
    scores["consent"] = invalid
    result = DemiJouleGate().safety_gate(scores)
    assert result["decision"] == "ESCALATE"
    assert "consent" in result["reason"]


@pytest.mark.parametrize("invalid", [None, [], "unsafe", 0.9, True, float("nan")])
def test_nonmapping_input_fails_closed_without_exception(invalid: object) -> None:
    result = DemiJouleGate().safety_gate(invalid)
    assert result["decision"] == "ESCALATE"


@pytest.mark.parametrize("low", [0.0, 0.2, 0.49999])
def test_low_but_numeric_normalized_score_remains_escalation(low: float) -> None:
    scores = safe_scores()
    scores["consent"] = low
    result = DemiJouleGate().safety_gate(scores)
    assert result["decision"] == "ESCALATE"
    assert "below 0.5" in result["reason"]


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), "0.9", True, None])
def test_orchestrator_does_not_gold_star_invalid_safety(bad: object) -> None:
    scores: dict[str, object] = dict(safe_scores())
    scores["consent"] = bad
    audit = AgentAmethyst().orchestrate_turn("bounded-invalid-safety", {"safety": scores})
    assert audit.apogee_grade == "ESCALATE"
    assert audit.gold_star is False
    # Early schema-placeholder dgaf_decision is not execution permission.


def test_orchestrator_null_safety_does_not_crash_or_gold_star() -> None:
    audit = AgentAmethyst().orchestrate_turn("bounded-null-safety", {"safety": None})
    assert audit.apogee_grade == "ESCALATE"
    assert audit.gold_star is False
