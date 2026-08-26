"""Locked candidate-scoped primary analysis primitives for P8.

This module contains analysis mechanics only. It consumes validated pilot seed
artifacts; it does not execute trials, regenerate observations, or repair data.
The primary estimand is the mean paired seed-level FFCR difference:

    Delta_s = FFCR_s(dgaf) - FFCR_s(null)

Pilot artifacts remain blinded until an explicit unblinding step supplies the
condition mapping. FFCR is the proportion of complete matrix cells whose
recorded ``ffcr_success`` is true. Bootstrap resampling is over complete
paired seed effects, never individual trials.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Mapping, Sequence

import numpy as np

CONDITIONS = ("null", "simple", "static", "dgaf")
PRIMARY_CONDITIONS = ("dgaf", "null")
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
EXPECTED_CELLS_PER_CONDITION = len(TOPOLOGIES) * len(FAILURE_COUNTS)
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 20260823
ALPHA = 0.05


@dataclass(frozen=True)
class SeedEffect:
    seed: int
    ffcr_dgaf: float
    ffcr_null: float

    @property
    def delta(self) -> float:
        return self.ffcr_dgaf - self.ffcr_null


def _expected_keys() -> set[tuple[str, int]]:
    return {(topology, failure_count) for topology in TOPOLOGIES for failure_count in FAILURE_COUNTS}


def _validate_condition_map(condition_map: Mapping[str, str]) -> None:
    if set(condition_map.values()) != set(CONDITIONS):
        raise ValueError("condition_map must map blinded identifiers bijectively to the four canonical conditions")
    if len(condition_map) != len(CONDITIONS):
        raise ValueError("condition_map must contain exactly four blinded identifiers")


def _validate_effects(effects: Sequence[SeedEffect]) -> np.ndarray:
    if not effects:
        raise ValueError("at least one analyzable paired seed is required")
    seeds = [effect.seed for effect in effects]
    if len(set(seeds)) != len(seeds):
        raise ValueError("paired seed effects must contain unique seed identifiers")
    deltas = np.asarray([effect.delta for effect in effects], dtype=float)
    if not np.all(np.isfinite(deltas)):
        raise ValueError("paired seed effects must be finite")
    return deltas


def condition_ffcr(
    records: Sequence[Mapping[str, object]],
    condition: str,
    *,
    condition_map: Mapping[str, str],
) -> float:
    """Return FFCR for one condition from one complete seed artifact.

    ``condition_map`` is supplied only after explicit unblinding and maps the
    blinded artifact identifier to one of the canonical condition identifiers.
    Every expected topology/failure-count cell must occur exactly once.
    Missing, duplicate, malformed, or outcome-unusable records raise rather
    than being repaired.
    """
    if condition not in CONDITIONS:
        raise ValueError(f"unsupported condition: {condition!r}")
    _validate_condition_map(condition_map)
    expected = _expected_keys()
    seen: set[tuple[str, int]] = set()
    successes: list[bool] = []
    for record in records:
        blinded_id = record.get("blinded_condition_id")
        if not isinstance(blinded_id, str):
            raise ValueError("record missing blinded_condition_id")
        mapped = condition_map.get(blinded_id)
        if mapped != condition:
            continue
        topology = record.get("topology")
        failure_count = record.get("failure_count")
        if (
            not isinstance(topology, str)
            or not isinstance(failure_count, int)
            or isinstance(failure_count, bool)
        ):
            raise ValueError("analysis input requires unblinded topology/failure_count fields")
        key = (topology, failure_count)
        if key not in expected or key in seen:
            raise ValueError(f"invalid or duplicate matrix cell: {key!r}")
        value = record.get("ffcr_success")
        if not isinstance(value, bool):
            raise ValueError("record missing boolean ffcr_success")
        seen.add(key)
        successes.append(value)
    if seen != expected:
        missing = sorted(expected - seen)
        raise ValueError(f"incomplete condition matrix; missing={missing!r}")
    return sum(successes) / len(successes)


def seed_effect_from_artifact(
    document: Mapping[str, object], *, condition_map: Mapping[str, str]
) -> SeedEffect:
    records = document.get("records")
    seed = document.get("seed_id")
    if not isinstance(seed, int) or isinstance(seed, bool) or not isinstance(records, list):
        raise ValueError("invalid seed artifact")
    _validate_condition_map(condition_map)
    return SeedEffect(
        seed=seed,
        ffcr_dgaf=condition_ffcr(records, "dgaf", condition_map=condition_map),
        ffcr_null=condition_ffcr(records, "null", condition_map=condition_map),
    )


def primary_estimate(effects: Sequence[SeedEffect]) -> float:
    deltas = _validate_effects(effects)
    return float(np.mean(deltas))


def paired_bootstrap_ci(
    effects: Sequence[SeedEffect],
    *,
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
    alpha: float = ALPHA,
) -> tuple[float, float]:
    """Two-sided percentile paired-bootstrap CI over complete seed effects."""
    deltas = _validate_effects(effects)
    if not isinstance(resamples, int) or isinstance(resamples, bool) or resamples < 1:
        raise ValueError("resamples must be a positive integer")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("bootstrap seed must be an integer")
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or not 0 < alpha < 1 or not math.isfinite(float(alpha)):
        raise ValueError("alpha must be finite and between 0 and 1")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(deltas), size=(resamples, len(deltas)))
    boot_means = deltas[indices].mean(axis=1)
    low, high = (float(x) for x in np.quantile(boot_means, [float(alpha) / 2, 1 - float(alpha) / 2]))
    if not math.isfinite(low) or not math.isfinite(high) or low > high:
        raise ValueError("bootstrap confidence interval is invalid")
    return low, high


def decision(effects: Sequence[SeedEffect], ci: tuple[float, float]) -> str:
    estimate = primary_estimate(effects)
    if not isinstance(ci, tuple) or len(ci) != 2:
        raise ValueError("confidence interval must be a two-element tuple")
    low, high = ci
    if not all(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)) for value in ci):
        raise ValueError("confidence interval bounds must be finite numbers")
    low, high = float(low), float(high)
    if low > high:
        raise ValueError("confidence interval lower bound exceeds upper bound")
    if estimate > 0 and low > 0:
        return "SUPPORTS_DIRECTIONAL_DGAF"
    if estimate <= 0 and high < 0:
        return "EVIDENCE_AGAINST_DIRECTIONAL_DGAF"
    return "NOT_SUPPORTED_OR_INCONCLUSIVE"


def analysis_config_bytes() -> bytes:
    config = {
        "primary_contrast": "dgaf-vs-null",
        "estimand": "mean_seed_paired_ffcr_difference",
        "bootstrap": "paired_seed_effects_percentile",
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "confidence_level": 1 - ALPHA,
        "alpha": ALPHA,
        "secondary_policy": "Holm_if_confirmatory_otherwise_exploratory_descriptive",
        "matrix_topologies": TOPOLOGIES,
        "matrix_failure_counts": FAILURE_COUNTS,
    }
    return json.dumps(config, sort_keys=True, separators=(",", ":")).encode()


def analysis_config_sha256() -> str:
    return hashlib.sha256(analysis_config_bytes()).hexdigest()
