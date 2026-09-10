"""Executable reference for INST-QA-001 v1.1.

This module implements only the DGAF Core QA Rubric (11Q). It does not
implement INST-GATE-11Q or INST-APOGEE-7Q and does not confer scientific,
freeze, collection, or deployment authorization.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

INSTRUMENT_ID = "INST-QA-001"
INSTRUMENT_VERSION = "1.1"
QUESTION_WEIGHTS = (
    0.20,
    0.20,
    0.20,
    0.15,
    0.15,
    0.15,
    0.10,
    0.10,
    0.10,
    0.075,
    0.075,
)
ARTIFACT_QUALITY_THRESHOLD = 0.70
SEAL_ELIGIBILITY_THRESHOLD = 0.90
THRESHOLD_PROVENANCE = "inherited_v1.0_rubric_defined_heuristic_not_empirically_calibrated"


def score_11q(question_scores: Sequence[float]) -> float:
    """Return the normalized weighted mean for exactly eleven scores in [0, 1]."""
    if len(question_scores) != len(QUESTION_WEIGHTS):
        raise ValueError("INST-QA-001 requires exactly 11 question scores")

    scores = []
    for index, raw_score in enumerate(question_scores, start=1):
        if isinstance(raw_score, bool):
            raise TypeError(f"Q{index} score must be numeric, not bool")
        score = float(raw_score)
        if not math.isfinite(score):
            raise ValueError(f"Q{index} score must be finite")
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"Q{index} score must be within [0, 1]")
        scores.append(score)

    denominator = sum(QUESTION_WEIGHTS)
    if denominator <= 0.0:
        raise RuntimeError("INST-QA-001 weight sum must be positive")

    weighted_sum = sum(weight * score for weight, score in zip(QUESTION_WEIGHTS, scores))
    result = weighted_sum / denominator

    # Defensive numerical guard: valid bounded inputs must produce a bounded result.
    if not 0.0 <= result <= 1.0:
        raise RuntimeError("INST-QA-001 normalized score escaped [0, 1]")
    return result


def artifact_quality_passes(score: float) -> bool:
    """Apply only the INST-QA-001 v1.1 artifact-quality heuristic threshold."""
    return score >= ARTIFACT_QUALITY_THRESHOLD


def seal_eligibility_passes(score: float) -> bool:
    """Apply only the INST-QA-001 v1.1 seal-eligibility heuristic threshold."""
    return score >= SEAL_ELIGIBILITY_THRESHOLD
