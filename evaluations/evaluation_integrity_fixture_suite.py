"""Deterministic repository-native evaluation-integrity fixtures.

Scope: evaluator/mechanism testing only. These fixtures do not claim model
robustness or real-world adversarial resistance.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


THREATS = (
    "benchmark_gaming",
    "measurement_leakage",
    "evaluator_awareness",
    "test_set_contamination",
    "stochastic_seed_artifact",
    "topology_specificity",
)


@dataclass(frozen=True)
class IntegrityCase:
    threat: str
    payload: tuple[str, ...]
    expected_detected: bool


CASES: tuple[IntegrityCase, ...] = (
    IntegrityCase("benchmark_gaming", ("eval_score", "optimize_for_eval_score"), True),
    IntegrityCase("benchmark_gaming", ("eval_score", "optimize_for_task"), False),
    IntegrityCase("measurement_leakage", ("training_metric", "eval_metric_same_source"), True),
    IntegrityCase("measurement_leakage", ("training_metric", "held_out_eval_metric"), False),
    IntegrityCase("evaluator_awareness", ("condition_hidden", "model_cannot_observe_label"), False),
    IntegrityCase("evaluator_awareness", ("condition_visible", "model_can_observe_label"), True),
    IntegrityCase("test_set_contamination", ("fixture_hash", "training_fixture_hash_match"), True),
    IntegrityCase("test_set_contamination", ("fixture_hash", "held_out_hash"), False),
    IntegrityCase("stochastic_seed_artifact", ("same_seed", "same_output"), True),
    IntegrityCase("stochastic_seed_artifact", ("independent_seeds", "same_distribution"), False),
    IntegrityCase("topology_specificity", ("single_topology", "effect_only_on_training_topology"), True),
    IntegrityCase("topology_specificity", ("multiple_topologies", "effect_replicates"), False),
)


def detect(case: IntegrityCase) -> bool:
    """Return whether the fixture contains its designated integrity hazard."""
    if case.threat not in THREATS:
        raise ValueError(f"unsupported threat: {case.threat}")
    tokens = set(case.payload)
    if case.threat == "benchmark_gaming":
        return "optimize_for_eval_score" in tokens
    if case.threat == "measurement_leakage":
        return "eval_metric_same_source" in tokens
    if case.threat == "evaluator_awareness":
        return "condition_visible" in tokens
    if case.threat == "test_set_contamination":
        return "training_fixture_hash_match" in tokens
    if case.threat == "stochastic_seed_artifact":
        return "same_seed" in tokens and "same_output" in tokens
    if case.threat == "topology_specificity":
        return "single_topology" in tokens and "effect_only_on_training_topology" in tokens
    raise AssertionError("unreachable")


def evaluate(cases: Iterable[IntegrityCase] = CASES) -> dict[str, int | float]:
    cases_list = list(cases)
    if not cases_list:
        raise ValueError("at least one integrity case is required")
    correct = sum(detect(case) == case.expected_detected for case in cases_list)
    return {
        "cases": len(cases_list),
        "correct": correct,
        "incorrect": len(cases_list) - correct,
        "accuracy": correct / len(cases_list),
    }


def validate_fixture_set(cases: Sequence[IntegrityCase] = CASES) -> None:
    if not cases:
        raise ValueError("fixture set cannot be empty")
    present = {case.threat for case in cases}
    missing = set(THREATS) - present
    if missing:
        raise ValueError(f"fixture set missing threats: {sorted(missing)}")
    for case in cases:
        if not isinstance(case.expected_detected, bool):
            raise TypeError("expected_detected must be boolean")


def build_report() -> dict[str, object]:
    """Build a deterministic machine-readable synthetic evidence record."""
    validate_fixture_set(CASES)
    score = evaluate(CASES)
    return {
        "evaluation": "evaluation_integrity_fixture_suite",
        "evidence_class": "SYNTHETIC",
        "fixture_version": "v1",
        "threats": list(THREATS),
        "case_count": len(CASES),
        "expected_detection_count": sum(case.expected_detected for case in CASES),
        "score": score,
        "passed": score["incorrect"] == 0,
        "limitations": [
            "Synthetic repository fixture only; not model-facing adversarial evaluation.",
            "Successful fixture detection does not establish adversarial robustness.",
            "No external benchmark or real workload is used as validation evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
