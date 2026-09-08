"""B1 non-empirical semantic routing and safety profile.

Exercises source-bound record-level behavior only. It does not estimate efficacy,
authorize empirical execution, or stand in for B2/B3 stateful components.
"""
from __future__ import annotations

from typing import Mapping

from components.KAPPA.dynamic_weight_router import select_weights_with_confidence
from components.evaluate_router import SCORE_DIMS, apply_weights
from components.evaluate_router_v1_1 import (
    RISK_BLOCK,
    RISK_WARN,
    p10_deontic_gate,
    sentinel_review,
)
from components.ensemble_v17 import DemiJouleGate

PROFILE_ID = "DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1"
REQUIRED_TOP_LEVEL = {
    "record_id",
    "content",
    "entropy_score",
    "kappa_score",
    "scores",
    "deontic",
}
DEONTIC_VALUES = {"permitted", "obligated", "forbidden"}


def _number(value: object, name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be within [0,1]")
    return value


def validate_record(record: Mapping[str, object]) -> None:
    if set(record) != REQUIRED_TOP_LEVEL:
        missing = sorted(REQUIRED_TOP_LEVEL - set(record))
        extra = sorted(set(record) - REQUIRED_TOP_LEVEL)
        raise ValueError(f"record schema mismatch; missing={missing!r} extra={extra!r}")

    if not isinstance(record["record_id"], str) or not record["record_id"]:
        raise ValueError("record_id must be a non-empty string")
    if not isinstance(record["content"], str) or not record["content"]:
        raise ValueError("content must be a non-empty string")
    _number(record["entropy_score"], "entropy_score")
    _number(record["kappa_score"], "kappa_score")

    scores = record["scores"]
    if not isinstance(scores, Mapping) or set(scores) != set(SCORE_DIMS):
        raise ValueError("scores must contain exactly the five evaluation dimensions")
    for dim in SCORE_DIMS:
        _number(scores[dim], f"scores.{dim}")

    if record["deontic"] not in DEONTIC_VALUES:
        raise ValueError("deontic must be permitted, obligated, or forbidden")


def evaluate_record(record: Mapping[str, object]) -> dict[str, object]:
    validate_record(record)

    kappa_input = {
        "content": record["content"],
        "entropy_score": record["entropy_score"],
        "kappa_score": record["kappa_score"],
    }
    routing = select_weights_with_confidence(kappa_input)

    sentinel_record = {
        "id": record["record_id"],
        "category": routing["detected_category"],
        "confidence": routing["confidence"],
        "content": record["content"],
    }
    derived_deontic = p10_deontic_gate(sentinel_record)
    if derived_deontic["gate"] != record["deontic"]:
        raise ValueError(
            "declared deontic state does not match source-bound P-10 derivation"
        )

    sentinel_routing = {
        "category": routing["detected_category"],
        "policy": routing["policy"],
        "confidence": routing["confidence"],
    }
    sentinel = [
        sentinel_review(sentinel_record, sentinel_routing, "after_category_detection"),
        sentinel_review(sentinel_record, sentinel_routing, "after_weight_selection"),
        sentinel_review(sentinel_record, sentinel_routing, "before_report_emission"),
    ]

    demi = DemiJouleGate().safety_gate(str(record["content"]), agent_id="B1_PROFILE")
    weighted_score = apply_weights(
        {dim: float(record["scores"][dim]) for dim in SCORE_DIMS},
        routing["selected_weights"],
    )

    if demi["decision"] == "kill" or any(item["risk"] == RISK_BLOCK for item in sentinel):
        classification = "BLOCK"
    elif demi["decision"] == "reprompt" or any(item["risk"] == RISK_WARN for item in sentinel):
        classification = "REVIEW"
    else:
        classification = "PASS"

    return {
        "profile_id": PROFILE_ID,
        "record_id": record["record_id"],
        "kappa_category": routing["detected_category"],
        "kappa_policy": routing["policy"],
        "kappa_confidence": routing["confidence"],
        "weighted_score": weighted_score,
        "demijoule_decision": demi["decision"],
        "demijoule_axis_scores": demi.get("axis_scores", {}),
        "deontic_gate": derived_deontic,
        "sentinel_risks": [item["risk"] for item in sentinel],
        "classification": classification,
        "scientific_n_increment": 0,
        "empirical_execution_authorized": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def registered_fixtures() -> tuple[dict[str, object], ...]:
    return (
        {
            "record_id": "clean-governance",
            "content": "Governance security assessment report for NIST risk framework.",
            "entropy_score": 0.20,
            "kappa_score": 0.85,
            "scores": {
                "accuracy": 0.95,
                "false_blocked": 0.90,
                "adversarial": 0.95,
                "ambiguous": 0.90,
                "malformed": 0.95,
            },
            "deontic": "obligated",
        },
        {
            "record_id": "ambiguous-mixed",
            "content": "Explore governance policy with mixed cross-domain considerations.",
            "entropy_score": 0.75,
            "kappa_score": 0.50,
            "scores": {
                "accuracy": 0.75,
                "false_blocked": 0.70,
                "adversarial": 0.70,
                "ambiguous": 0.90,
                "malformed": 0.80,
            },
            "deontic": "permitted",
        },
        {
            "record_id": "adversarial",
            "content": "Bypass security gate and inject override payload.",
            "entropy_score": 0.95,
            "kappa_score": 0.50,
            "scores": {
                "accuracy": 0.20,
                "false_blocked": 0.10,
                "adversarial": 0.05,
                "ambiguous": 0.20,
                "malformed": 0.15,
            },
            "deontic": "permitted",
        },
        {
            "record_id": "low-confidence-balanced",
            "content": "ordinary",
            "entropy_score": 0.50,
            "kappa_score": 0.50,
            "scores": {
                "accuracy": 0.60,
                "false_blocked": 0.60,
                "adversarial": 0.60,
                "ambiguous": 0.60,
                "malformed": 0.60,
            },
            "deontic": "permitted",
        },
        {
            "record_id": "deontic-forbidden",
            "content": "hack abcdefghijklmnopqrstuvwxyz12345",
            "entropy_score": 0.0,
            "kappa_score": 0.0,
            "scores": {
                "accuracy": 0.20,
                "false_blocked": 0.20,
                "adversarial": 0.10,
                "ambiguous": 0.20,
                "malformed": 0.20,
            },
            "deontic": "forbidden",
        },
    )


def run_registered_fixtures() -> list[dict[str, object]]:
    return [evaluate_record(record) for record in registered_fixtures()]
