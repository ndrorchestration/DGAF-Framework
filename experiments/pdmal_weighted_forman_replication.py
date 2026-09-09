#!/usr/bin/env python3
"""Prospective synthetic weighted Forman–Ricci replication for issue #72.

This experiment is deliberately separate from Track A. It tests whether weighted
Forman–Ricci curvature restores variance and how several anomaly thresholds
behave under controlled edge-weight perturbations on the canonical
20-node/30-edge dodecahedral graph.

The weighted undirected formula follows Sreejith et al. (2016),
"Forman curvature for complex networks" (arXiv:1603.00386). With all vertex
and edge weights equal to 1 it reduces exactly to 4 - deg(u) - deg(v), hence
-2 on every edge of the 3-regular dodecahedral graph.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from pathlib import Path
from statistics import fmean, median, pstdev, pvariance
from typing import Iterable

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.pdmal.lattice_harness import DODECAHEDRAL_EDGES  # noqa: E402

SCHEMA = "PDMAL_WEIGHTED_FORMAN_REPLICATION_V1"
MASTER_SEED = 20260909
BASELINE_EDGE_WEIGHT = 1.0
HEALTHY_CURVATURE = -2.0
PERTURBED_EDGE_COUNTS = (1, 3, 5, 10)
TARGET_EDGE_WEIGHTS = (0.1, 0.3, 0.5, 0.7, 1.3, 2.0)
CALIBRATION_REPLICATES = tuple(range(10))
HELDOUT_REPLICATES = tuple(range(10, 20))
MAD_Z_THRESHOLD = 3.5
PERCENTILE = 0.90
VARIANCE_EPSILON = 1e-15

Edge = tuple[int, int]


def canonical_edge(edge: Edge) -> Edge:
    return tuple(sorted(edge))  # type: ignore[return-value]


EDGES = tuple(canonical_edge(edge) for edge in DODECAHEDRAL_EDGES)


def _adjacency() -> dict[int, list[Edge]]:
    adjacency: dict[int, list[Edge]] = {}
    for edge in EDGES:
        u, v = edge
        adjacency.setdefault(u, []).append(edge)
        adjacency.setdefault(v, []).append(edge)
    return adjacency


ADJACENCY = _adjacency()


def weighted_forman_ricci(
    edge_weights: dict[Edge, float],
    vertex_weights: dict[int, float] | None = None,
) -> dict[Edge, float]:
    """Compute weighted Forman–Ricci curvature for every canonical edge."""
    if set(edge_weights) != set(EDGES):
        raise ValueError("edge_weights must cover the canonical dodecahedral edge set exactly")
    if any(weight <= 0 for weight in edge_weights.values()):
        raise ValueError("all edge weights must be positive")

    if vertex_weights is None:
        vertex_weights = {node: 1.0 for node in ADJACENCY}
    if set(vertex_weights) != set(ADJACENCY):
        raise ValueError("vertex_weights must cover the canonical vertex set exactly")
    if any(weight <= 0 for weight in vertex_weights.values()):
        raise ValueError("all vertex weights must be positive")

    curvature: dict[Edge, float] = {}
    for edge in EDGES:
        u, v = edge
        edge_weight = edge_weights[edge]
        u_weight = vertex_weights[u]
        v_weight = vertex_weights[v]
        u_neighbors = sum(
            u_weight / math.sqrt(edge_weight * edge_weights[other])
            for other in ADJACENCY[u]
            if other != edge
        )
        v_neighbors = sum(
            v_weight / math.sqrt(edge_weight * edge_weights[other])
            for other in ADJACENCY[v]
            if other != edge
        )
        curvature[edge] = edge_weight * (
            u_weight / edge_weight
            + v_weight / edge_weight
            - u_neighbors
            - v_neighbors
        )
    return curvature


def anomaly_scores(curvature: dict[Edge, float]) -> dict[Edge, float]:
    return {edge: abs(value - HEALTHY_CURVATURE) for edge, value in curvature.items()}


def percentile(values: Iterable[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    if not 0 <= quantile <= 1:
        raise ValueError("quantile must be in [0, 1]")
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def ranked_edges(scores: dict[Edge, float]) -> list[Edge]:
    return sorted(scores, key=lambda edge: (-scores[edge], edge))


def detect(
    curvature: dict[Edge, float],
    perturbed_count: int,
    method: str,
    calibrated_threshold: float | None = None,
) -> set[Edge]:
    values = list(curvature.values())
    scores = anomaly_scores(curvature)

    if method == "mean_plus_3sigma_score":
        score_values = list(scores.values())
        threshold = fmean(score_values) + 3 * pstdev(score_values)
        return {edge for edge, score in scores.items() if score > threshold}

    if method == "two_sided_3sigma_raw":
        mean = fmean(values)
        sigma = pstdev(values)
        return {
            edge
            for edge, value in curvature.items()
            if value < mean - 3 * sigma or value > mean + 3 * sigma
        }

    if method == "mad_modified_z":
        center = median(values)
        mad = median(abs(value - center) for value in values)
        if mad == 0:
            return {edge for edge, value in curvature.items() if value != center}
        return {
            edge
            for edge, value in curvature.items()
            if abs(0.6745 * (value - center) / mad) > MAD_Z_THRESHOLD
        }

    if method == "percentile_90_score":
        threshold = percentile(scores.values(), PERCENTILE)
        return {
            edge
            for edge, score in scores.items()
            if score > 0 and score >= threshold
        }

    if method == "rank_top_k_oracle":
        return set(ranked_edges(scores)[:perturbed_count])

    if method == "calibrated_global_score":
        if calibrated_threshold is None:
            raise ValueError("calibrated threshold required")
        return {
            edge
            for edge, score in scores.items()
            if score > 0 and score >= calibrated_threshold
        }

    raise ValueError(f"unknown detector: {method}")


def selection_seed(perturbed_count: int, target_weight: float, replicate: int) -> int:
    """Derive a collision-free deterministic seed for the preregistered cells."""
    target_milli = int(round(target_weight * 1000))
    return MASTER_SEED + perturbed_count * 100_000 + target_milli * 100 + replicate


def make_trial(perturbed_count: int, target_weight: float, replicate: int) -> dict:
    seed = selection_seed(perturbed_count, target_weight, replicate)
    rng = random.Random(seed)
    truth = set(rng.sample(list(EDGES), perturbed_count))
    weights = {edge: BASELINE_EDGE_WEIGHT for edge in EDGES}
    for edge in truth:
        weights[edge] = target_weight
    curvature = weighted_forman_ricci(weights)
    scores = anomaly_scores(curvature)
    return {
        "perturbed_count": perturbed_count,
        "target_weight": target_weight,
        "direction": "decrease" if target_weight < 1 else "increase",
        "replicate": replicate,
        "selection_seed": seed,
        "truth": sorted(truth),
        "curvature": curvature,
        "scores": scores,
        "curvature_variance": pvariance(curvature.values()),
    }


def f1_score(predicted: set[Edge], truth: set[Edge]) -> float:
    tp = len(predicted & truth)
    fp = len(predicted - truth)
    fn = len(truth - predicted)
    denominator = 2 * tp + fp + fn
    return 2 * tp / denominator if denominator else 0.0


def calibrate_global_threshold(trials: list[dict]) -> tuple[float, float]:
    candidates = sorted(
        {score for trial in trials for score in trial["scores"].values()}
    )
    if not candidates:
        raise ValueError("calibration requires score candidates")

    best_mean_f1 = -1.0
    best_threshold = candidates[0]
    for threshold in candidates:
        trial_f1 = []
        for trial in trials:
            truth = set(trial["truth"])
            predicted = {
                edge
                for edge, score in trial["scores"].items()
                if score > 0 and score >= threshold
            }
            trial_f1.append(f1_score(predicted, truth))
        mean_f1 = fmean(trial_f1)
        if mean_f1 > best_mean_f1 or (
            math.isclose(mean_f1, best_mean_f1) and threshold > best_threshold
        ):
            best_mean_f1 = mean_f1
            best_threshold = threshold
    return best_threshold, best_mean_f1


def detector_metrics(
    predicted: set[Edge], truth: set[Edge], scores: dict[Edge, float]
) -> dict[str, float | int]:
    tp = len(predicted & truth)
    fp = len(predicted - truth)
    fn = len(truth - predicted)
    tn = len(scores) - tp - fp - fn
    ranking = {edge: rank for rank, edge in enumerate(ranked_edges(scores), start=1)}
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "tpr": tp / len(truth),
        "fpr": fp / (fp + tn) if fp + tn else 0.0,
        "precision": tp / (tp + fp) if tp + fp else 0.0,
        "recall": tp / len(truth),
        "worst_true_anomaly_rank": max(ranking[edge] for edge in truth),
    }


def _mean(records: list[dict], field: str) -> float:
    return fmean(float(record[field]) for record in records)


def run_experiment() -> dict:
    trials = [
        make_trial(count, target, replicate)
        for count in PERTURBED_EDGE_COUNTS
        for target in TARGET_EDGE_WEIGHTS
        for replicate in (*CALIBRATION_REPLICATES, *HELDOUT_REPLICATES)
    ]
    calibration = [
        trial for trial in trials if trial["replicate"] in CALIBRATION_REPLICATES
    ]
    heldout = [trial for trial in trials if trial["replicate"] in HELDOUT_REPLICATES]
    threshold, calibration_mean_f1 = calibrate_global_threshold(calibration)

    methods = (
        "mean_plus_3sigma_score",
        "two_sided_3sigma_raw",
        "mad_modified_z",
        "percentile_90_score",
        "rank_top_k_oracle",
        "calibrated_global_score",
    )
    heldout_records: list[dict] = []
    summaries: dict[str, dict[str, float]] = {}

    for trial in heldout:
        truth = set(trial["truth"])
        for method in methods:
            predicted = detect(
                trial["curvature"],
                trial["perturbed_count"],
                method,
                calibrated_threshold=threshold,
            )
            metrics = detector_metrics(predicted, truth, trial["scores"])
            heldout_records.append(
                {
                    "perturbed_count": trial["perturbed_count"],
                    "target_weight": trial["target_weight"],
                    "direction": trial["direction"],
                    "replicate": trial["replicate"],
                    "selection_seed": trial["selection_seed"],
                    "detector": method,
                    **metrics,
                }
            )

    for method in methods:
        records = [record for record in heldout_records if record["detector"] == method]
        summaries[method] = {
            "mean_tpr": _mean(records, "tpr"),
            "mean_fpr": _mean(records, "fpr"),
            "mean_precision": _mean(records, "precision"),
            "mean_recall": _mean(records, "recall"),
            "mean_worst_true_anomaly_rank": _mean(records, "worst_true_anomaly_rank"),
        }

    variances = [float(trial["curvature_variance"]) for trial in trials]
    source_commit = os.environ.get("SOURCE_SHA") or os.environ.get(
        "GITHUB_SHA", "UNBOUND_LOCAL"
    )
    return {
        "schema": SCHEMA,
        "source_commit": source_commit,
        "source_run_id": os.environ.get("GITHUB_RUN_ID", "UNBOUND_LOCAL"),
        "epistemic_classification": {
            "matrix_results": "COMPUTED_SYNTHETIC",
            "general_reliability": "NOT_ESTABLISHED",
            "production_method": "NOT_SELECTED",
            "track_a_state_effect": "NONE",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
        "protocol": {
            "graph": "canonical 20-node / 30-edge dodecahedral graph",
            "vertex_weight": 1.0,
            "baseline_edge_weight": BASELINE_EDGE_WEIGHT,
            "healthy_curvature": HEALTHY_CURVATURE,
            "perturbed_edge_counts": list(PERTURBED_EDGE_COUNTS),
            "target_edge_weights": list(TARGET_EDGE_WEIGHTS),
            "calibration_replicates": list(CALIBRATION_REPLICATES),
            "heldout_replicates": list(HELDOUT_REPLICATES),
            "master_seed": MASTER_SEED,
            "total_trials": len(trials),
            "calibration_trials": len(calibration),
            "heldout_trials": len(heldout),
            "weighted_forman_reference": "Sreejith et al. 2016, arXiv:1603.00386",
        },
        "calibration": {
            "global_score_threshold": threshold,
            "mean_f1_on_calibration_trials": calibration_mean_f1,
            "threshold_frozen_before_heldout_scoring": True,
        },
        "variance_restoration": {
            "trials_with_variance_above_epsilon": sum(
                variance > VARIANCE_EPSILON for variance in variances
            ),
            "total_trials": len(variances),
            "fraction": sum(variance > VARIANCE_EPSILON for variance in variances)
            / len(variances),
            "minimum_variance": min(variances),
            "maximum_variance": max(variances),
            "epsilon": VARIANCE_EPSILON,
        },
        "heldout_detector_summary": summaries,
        "heldout_records": heldout_records,
    }


def validate_result(result: dict) -> None:
    if result.get("schema") != SCHEMA:
        raise ValueError("unexpected result schema")
    protocol = result["protocol"]
    if protocol["total_trials"] != 480:
        raise ValueError("expected exactly 480 preregistered trials")
    if protocol["calibration_trials"] != 240 or protocol["heldout_trials"] != 240:
        raise ValueError("expected 240 calibration and 240 held-out trials")
    if len(result["heldout_records"]) != 240 * 6:
        raise ValueError("expected six detector records for each held-out trial")
    if result["epistemic_classification"]["track_a_state_effect"] != "NONE":
        raise ValueError("research result must have no Track A state effect")
    if result["epistemic_classification"]["canonical_dgaf_efficacy"] != "NOT_ESTABLISHED":
        raise ValueError("research result cannot establish canonical DGAF efficacy")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="weighted-forman-replication.json")
    args = parser.parse_args()
    result = run_experiment()
    validate_result(result)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result["variance_restoration"], sort_keys=True))
    print(json.dumps(result["heldout_detector_summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
