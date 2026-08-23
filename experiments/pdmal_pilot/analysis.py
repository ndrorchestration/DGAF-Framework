"""Locked candidate-scoped primary analysis primitives for P8.

This module contains analysis mechanics only. It consumes validated pilot seed
artifacts; it does not execute trials, regenerate observations, or repair data.
The primary estimand is the mean paired seed-level FFCR difference:

    Delta_s = FFCR_s(dgaf) - FFCR_s(null)

FFCR is the proportion of complete matrix cells whose recorded ``ffcr_success``
is true. Bootstrap resampling is over complete paired seed effects, never
individual trials.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

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


def _expected_keys(condition: str) -> set[tuple[str, int]]:
    return {(topology, failure_count) for topology in TOPOLOGIES for failure_count in FAILURE_COUNTS}


def condition_ffcr(records: Sequence[Mapping[str, object]], condition: str) -> float:
    """Return FFCR for one condition from one complete seed artifact.

    The caller must provide records for exactly one seed. Every expected
    topology/failure-count cell must occur exactly once. Missing, duplicate,
    malformed, or outcome-unusable records raise rather than being repaired.
    """
    if condition not in CONDITIONS:
        raise ValueError(f"unsupported condition: {condition!r}")
    expected = _expected_keys(condition)
    seen: set[tuple[str, int]] = set()
    successes: list[bool] = []
    for record in records:
        if record.get("condition") != condition:
            continue
        topology = record.get("topology")
        failure_count = record.get("failure_count")
        if not isinstance(topology, str) or not isinstance(failure_count, int):
            raise ValueError("malformed topology/failure_count")
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


def seed_effect_from_artifact(document: Mapping[str, object]) -> SeedEffect:
    records = document.get("records")
    seed = document.get("seed_id")
    if not isinstance(seed, int) or not isinstance(records, list):
        raise ValueError("invalid seed artifact")
    return SeedEffect(
        seed=seed,
        ffcr_dgaf=condition_ffcr(records, "dgaf"),
        ffcr_null=condition_ffcr(records, "null"),
    )


def primary_estimate(effects: Sequence[SeedEffect]) -> float:
    if not effects:
        raise ValueError("at least one analyzable paired seed is required")
    return float(np.mean([effect.delta for effect in effects]))


def paired_bootstrap_ci(
    effects: Sequence[SeedEffect],
    *,
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
    alpha: float = ALPHA,
) -> tuple[float, float]:
    """Two-sided percentile paired-bootstrap CI over complete seed effects."""
    if not effects:
        raise ValueError("at least one analyzable paired seed is required")
    if resamples < 1:
        raise ValueError("resamples must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    deltas = np.asarray([effect.delta for effect in effects], dtype=float)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(deltas), size=(resamples, len(deltas)))
    boot_means = deltas[indices].mean(axis=1)
    return tuple(float(x) for x in np.quantile(boot_means, [alpha / 2, 1 - alpha / 2]))


def decision(effects: Sequence[SeedEffect], ci: tuple[float, float]) -> str:
    estimate = primary_estimate(effects)
    low, high = ci
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
