import math

import pytest

from scripts.qa_rubric_11q import (
    ARTIFACT_QUALITY_THRESHOLD,
    QUESTION_WEIGHTS,
    SEAL_ELIGIBILITY_THRESHOLD,
    artifact_quality_passes,
    score_11q,
    seal_eligibility_passes,
)


def test_weight_sum_preserves_v1_relative_priorities() -> None:
    assert math.isclose(sum(QUESTION_WEIGHTS), 1.5)


def test_score_minimum_is_zero() -> None:
    assert score_11q([0.0] * 11) == 0.0


def test_score_maximum_is_one() -> None:
    assert score_11q([1.0] * 11) == 1.0


def test_uniform_scores_are_scale_preserving() -> None:
    assert score_11q([0.7] * 11) == pytest.approx(0.7)
    assert score_11q([0.9] * 11) == pytest.approx(0.9)


def test_relative_weights_affect_score() -> None:
    q1_only = score_11q([1.0] + [0.0] * 10)
    q11_only = score_11q([0.0] * 10 + [1.0])
    assert q1_only == pytest.approx(0.20 / 1.50)
    assert q11_only == pytest.approx(0.075 / 1.50)
    assert q1_only > q11_only


def test_instrument_scoped_threshold_boundaries() -> None:
    assert ARTIFACT_QUALITY_THRESHOLD == 0.70
    assert SEAL_ELIGIBILITY_THRESHOLD == 0.90
    assert artifact_quality_passes(0.70)
    assert not artifact_quality_passes(0.699999)
    assert seal_eligibility_passes(0.90)
    assert not seal_eligibility_passes(0.899999)


@pytest.mark.parametrize("scores", [[0.0] * 10, [0.0] * 12])
def test_requires_exactly_eleven_scores(scores: list[float]) -> None:
    with pytest.raises(ValueError, match="exactly 11"):
        score_11q(scores)


@pytest.mark.parametrize("bad", [-0.01, 1.01, float("nan"), float("inf")])
def test_rejects_invalid_scores(bad: float) -> None:
    scores = [0.5] * 11
    scores[4] = bad
    with pytest.raises(ValueError):
        score_11q(scores)


def test_rejects_bool_scores() -> None:
    scores = [0.5] * 11
    scores[2] = True
    with pytest.raises(TypeError):
        score_11q(scores)
