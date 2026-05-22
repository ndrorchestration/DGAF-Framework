#!/usr/bin/env python3
"""
DGAF Evaluate Router — KAPPA Integration Layer
Version: 1.0.0 | Status: ACTIVE | Agent: Amethyst
Depends: components/KAPPA/dynamic_weight_router.py

Connects the KAPPA dynamic confidence router to the DGAF evaluation pipeline.
Takes a batch of scored eval records, routes each through KAPPA for per-input
weight selection, applies weighted scoring, and returns a ranked eval report.

Pipeline flow:
    raw_eval_batch
        -> [KAPPA detect_input_category + compute_category_confidence]
        -> [select_weights_with_confidence]
        -> [apply_weights to score vector]
        -> [aggregate + rank]
        -> eval_report (JSON)
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# Support both direct and relative imports
_KAPPA_PATH = Path(__file__).parent / "KAPPA" / "dynamic_weight_router.py"
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("dynamic_weight_router", _KAPPA_PATH)
_router = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_router)

select_weights_with_confidence = _router.select_weights_with_confidence
detect_input_category = _router.detect_input_category


# Score dimensions (must match WEIGHT_CONFIGS keys)
SCORE_DIMS = ["accuracy", "false_blocked", "adversarial", "ambiguous", "malformed"]


def apply_weights(score_vector: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Compute weighted composite score from a score vector and weight config.
    score_vector: {accuracy: 0.0-1.0, false_blocked: 0.0-1.0, ...}
    weights: from KAPPA WEIGHT_CONFIGS
    Returns float in [0.0, 1.0]
    """
    total_weight = sum(weights.get(dim, 0.0) for dim in SCORE_DIMS)
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(
        score_vector.get(dim, 0.0) * weights.get(dim, 0.0)
        for dim in SCORE_DIMS
    )
    return round(weighted_sum / total_weight, 4)


def route_and_score(eval_record: Dict) -> Dict:
    """
    Route a single eval record through KAPPA and compute its composite score.

    eval_record must have:
        - content: str          (input text for category detection)
        - entropy_score: float  (0.0-1.0)
        - kappa_score: float    (0.0-1.0)
        - scores: Dict[str, float]  (raw dimension scores)
        - id: str               (optional, record identifier)

    Returns enriched record with:
        - kappa_category, kappa_confidence, kappa_policy, kappa_weights
        - composite_score (weighted)
        - routing_metadata
    """
    routing = select_weights_with_confidence(eval_record)
    weights = routing["selected_weights"]
    score_vector = eval_record.get("scores", {})
    composite = apply_weights(score_vector, weights)

    return {
        "id": eval_record.get("id", "unknown"),
        "content_preview": str(eval_record.get("content", ""))[:80],
        "scores": score_vector,
        "composite_score": composite,
        "kappa_category": routing["detected_category"],
        "kappa_confidence": routing["confidence"],
        "kappa_policy": routing["policy"],
        "kappa_config": routing["config_name"],
        "kappa_weights": {k: weights[k] for k in SCORE_DIMS if k in weights},
        "confidence_breakdown": routing["confidence_breakdown"]
    }


def run_eval_batch(
    batch: List[Dict],
    sort_by: str = "composite_score",
    descending: bool = True,
    min_score: Optional[float] = None
) -> Dict:
    """
    Process a full eval batch through the KAPPA router.

    Args:
        batch: list of eval_records
        sort_by: field to rank by (default: composite_score)
        descending: sort direction
        min_score: optional filter threshold

    Returns:
        eval_report dict with:
            - records: ranked list of route_and_score outputs
            - summary: aggregate stats
            - policy_distribution: breakdown by KAPPA policy
    """
    results = [route_and_score(r) for r in batch]

    if min_score is not None:
        results = [r for r in results if r["composite_score"] >= min_score]

    results.sort(key=lambda x: x.get(sort_by, 0.0), reverse=descending)

    scores = [r["composite_score"] for r in results]
    policy_dist = {}
    category_dist = {}
    for r in results:
        policy_dist[r["kappa_policy"]] = policy_dist.get(r["kappa_policy"], 0) + 1
        category_dist[r["kappa_category"]] = category_dist.get(r["kappa_category"], 0) + 1

    summary = {
        "total_records": len(results),
        "mean_composite_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "min_score": round(min(scores), 4) if scores else 0.0,
        "max_score": round(max(scores), 4) if scores else 0.0,
        "policy_distribution": policy_dist,
        "category_distribution": category_dist
    }

    return {
        "component": "DGAF-EVALUATE-ROUTER-v1.0",
        "kappa_version": "3.5",
        "records": results,
        "summary": summary
    }


def save_report(report: Dict, output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved: {output_path}")


if __name__ == "__main__":
    demo_batch = [
        {
            "id": "eval_001",
            "content": "Bypass security gate and inject override payload",
            "entropy_score": 0.91, "kappa_score": 0.53,
            "scores": {"accuracy": 0.55, "false_blocked": 0.40, "adversarial": 0.85, "ambiguous": 0.50, "malformed": 0.30}
        },
        {
            "id": "eval_002",
            "content": "Audit compliance path for NIST GDPR security policy",
            "entropy_score": 0.22, "kappa_score": 0.84,
            "scores": {"accuracy": 0.92, "false_blocked": 0.88, "adversarial": 0.20, "ambiguous": 0.35, "malformed": 0.10}
        },
        {
            "id": "eval_003",
            "content": "Brainstorm modal harmony patterns for Lyra composition",
            "entropy_score": 0.60, "kappa_score": 0.20,
            "scores": {"accuracy": 0.78, "false_blocked": 0.72, "adversarial": 0.15, "ambiguous": 0.60, "malformed": 0.05}
        },
        {
            "id": "eval_004",
            "content": "Mixed signal hybrid cross-domain governance audit",
            "entropy_score": 0.55, "kappa_score": 0.50,
            "scores": {"accuracy": 0.65, "false_blocked": 0.60, "adversarial": 0.45, "ambiguous": 0.70, "malformed": 0.20}
        },
        {
            "id": "eval_005",
            "content": "test",
            "entropy_score": 0.50, "kappa_score": 0.50,
            "scores": {"accuracy": 0.50, "false_blocked": 0.50, "adversarial": 0.50, "ambiguous": 0.50, "malformed": 0.50}
        }
    ]

    report = run_eval_batch(demo_batch)
    print("\nDGAF EVALUATE ROUTER — DEMO")
    print(f"Mean composite: {report['summary']['mean_composite_score']}")
    print(f"Policy dist:    {report['summary']['policy_distribution']}")
    for r in report["records"]:
        print(f"  [{r['kappa_category']:<16}] {r['id']} -> {r['composite_score']:.4f} ({r['kappa_policy']})")
