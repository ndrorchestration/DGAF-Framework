"""Locked primary analysis for Track A topology-robustness Epoch 001.

Consumes an already authorized, structurally locked, unblinded Track A dataset.
It cannot collect observations, infer missing outcomes, or authorize unblinding.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Mapping, Sequence

import numpy as np

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
SEEDS = tuple(range(20270101, 20270151))
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
PRIMARY_TOPOLOGY = "pdmal"
PRIMARY_COMPARATOR = "random_regular"
EXPECTED_TOTAL_RECORDS = len(SEEDS) * len(TOPOLOGIES) * len(FAILURE_COUNTS)
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 20270151
ALPHA = 0.05


@dataclass(frozen=True)
class PairedSeedEffect:
    seed: int
    pdmal_ffcr: float
    random_regular_ffcr: float

    @property
    def delta(self) -> float:
        return self.pdmal_ffcr - self.random_regular_ffcr


def _validate_records(records: Sequence[Mapping[str, object]]) -> dict[tuple[int, str, int], bool]:
    if len(records) != EXPECTED_TOTAL_RECORDS:
        raise ValueError(f"expected exactly {EXPECTED_TOTAL_RECORDS} records")

    expected = {
        (seed, topology, failure_count)
        for seed in SEEDS
        for topology in TOPOLOGIES
        for failure_count in FAILURE_COUNTS
    }
    observed: dict[tuple[int, str, int], bool] = {}

    for record in records:
        seed = record.get("seed_id")
        topology = record.get("topology")
        failure_count = record.get("failure_count")
        success = record.get("ffcr_success")

        if not isinstance(seed, int) or isinstance(seed, bool):
            raise ValueError("seed_id must be an integer")
        if not isinstance(topology, str):
            raise ValueError("topology must be a string")
        if not isinstance(failure_count, int) or isinstance(failure_count, bool):
            raise ValueError("failure_count must be an integer")
        if not isinstance(success, bool):
            raise ValueError("ffcr_success must be boolean")

        if "excluded" in record and record.get("excluded") is not False:
            raise ValueError("outcome exclusions are prohibited in the primary Track A analysis")

        if "algorithm_id" not in record:
            raise ValueError("record algorithm identity is required by the preregistration")
        algorithm_id = record["algorithm_id"]
        if algorithm_id != ALGORITHM_ID:
            raise ValueError("record algorithm identity does not match the preregistration")

        key = (seed, topology, failure_count)
        if key not in expected:
            raise ValueError(f"unexpected matrix cell: {key!r}")
        if key in observed:
            raise ValueError(f"duplicate matrix cell: {key!r}")
        observed[key] = success

    if set(observed) != expected:
        missing = sorted(expected - set(observed))
        raise ValueError(f"incomplete Track A matrix; missing={missing!r}")

    return observed


def paired_seed_effects(records: Sequence[Mapping[str, object]]) -> list[PairedSeedEffect]:
    observed = _validate_records(records)
    effects: list[PairedSeedEffect] = []
    for seed in SEEDS:
        pdmal_values = [
            observed[(seed, PRIMARY_TOPOLOGY, failure_count)]
            for failure_count in FAILURE_COUNTS
        ]
        rr_values = [
            observed[(seed, PRIMARY_COMPARATOR, failure_count)]
            for failure_count in FAILURE_COUNTS
        ]
        effects.append(
            PairedSeedEffect(
                seed=seed,
                pdmal_ffcr=sum(pdmal_values) / len(pdmal_values),
                random_regular_ffcr=sum(rr_values) / len(rr_values),
            )
        )
    return effects


def primary_estimate(effects: Sequence[PairedSeedEffect]) -> float:
    if len(effects) != len(SEEDS):
        raise ValueError("primary estimate requires exactly 50 paired seed effects")
    seeds = [effect.seed for effect in effects]
    if tuple(seeds) != SEEDS:
        raise ValueError("paired seed effects must use the preregistered seed panel in order")
    deltas = np.asarray([effect.delta for effect in effects], dtype=float)
    if not np.all(np.isfinite(deltas)):
        raise ValueError("paired effects must be finite")
    return float(np.mean(deltas))


def paired_bootstrap_ci(
    effects: Sequence[PairedSeedEffect],
    *,
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
    alpha: float = ALPHA,
) -> tuple[float, float]:
    if resamples != BOOTSTRAP_RESAMPLES:
        raise ValueError("Track A bootstrap resample count is locked")
    if seed != BOOTSTRAP_SEED:
        raise ValueError("Track A bootstrap RNG seed is locked")
    if alpha != ALPHA:
        raise ValueError("Track A alpha is locked")

    _ = primary_estimate(effects)
    deltas = np.asarray([effect.delta for effect in effects], dtype=float)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(deltas), size=(resamples, len(deltas)))
    means = deltas[indices].mean(axis=1)
    low, high = (
        float(x)
        for x in np.quantile(means, [alpha / 2, 1 - alpha / 2])
    )
    if not math.isfinite(low) or not math.isfinite(high) or low > high:
        raise ValueError("invalid bootstrap interval")
    return low, high


def decision(effects: Sequence[PairedSeedEffect], ci: tuple[float, float]) -> str:
    estimate = primary_estimate(effects)
    if not isinstance(ci, tuple) or len(ci) != 2:
        raise ValueError("confidence interval must be a two-element tuple")
    low, high = (float(ci[0]), float(ci[1]))
    if not math.isfinite(low) or not math.isfinite(high) or low > high:
        raise ValueError("confidence interval bounds are invalid")
    if estimate > 0 and low > 0:
        return "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    if estimate < 0 and high < 0:
        return "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    return "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"


def analyze(records: Sequence[Mapping[str, object]]) -> dict[str, object]:
    effects = paired_seed_effects(records)
    estimate = primary_estimate(effects)
    ci = paired_bootstrap_ci(effects)
    return {
        "protocol_id": PROTOCOL_ID,
        "algorithm_id": ALGORITHM_ID,
        "primary_topology": PRIMARY_TOPOLOGY,
        "primary_comparator": PRIMARY_COMPARATOR,
        "paired_seed_count": len(effects),
        "estimate_pdmal_minus_random_regular": estimate,
        "two_sided_95pct_percentile_ci": [ci[0], ci[1]],
        "classification": decision(effects, ci),
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "alpha": ALPHA,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }


def analysis_config_bytes() -> bytes:
    config = {
        "protocol_id": PROTOCOL_ID,
        "algorithm_id": ALGORITHM_ID,
        "seeds": SEEDS,
        "topologies": TOPOLOGIES,
        "failure_counts": FAILURE_COUNTS,
        "primary_topology": PRIMARY_TOPOLOGY,
        "primary_comparator": PRIMARY_COMPARATOR,
        "endpoint": "ffcr_success",
        "estimand": "mean_seed_paired_pdmal_minus_random_regular_ffcr",
        "bootstrap": "paired_seed_effects_percentile",
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "alpha": ALPHA,
        "confirmatory_test_count": 1,
    }
    return json.dumps(config, sort_keys=True, separators=(",", ":")).encode()


def analysis_config_sha256() -> str:
    return hashlib.sha256(analysis_config_bytes()).hexdigest()
