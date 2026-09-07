#!/usr/bin/env python3
"""Precommitted analysis wrapper for Solo P-30 Explicit Variant Epoch 003.

This module does not authorize unblinding. It may be used only after a separate
post-lock authorization supplies the blinded-condition mapping. Statistical
mechanics are delegated to the already locked ``analysis.py`` primitives.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping

from analysis import (
    ALPHA,
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    analysis_config_sha256,
    decision,
    paired_bootstrap_ci,
    primary_estimate,
    seed_effect_from_artifact,
)
from run_p30_variant import (
    VARIANT_EXPERIMENT_ID,
    VARIANT_SCOPE,
    VARIANT_SEEDS,
    VARIANT_SEED_START,
)

EXPECTED_ANALYSIS_CONFIG_SHA256 = "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"


def _load_condition_map(path: Path) -> Mapping[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("analysis prohibited: condition map must be a JSON object")
    return data


def analyze(dataset_dir: Path, condition_map_path: Path) -> dict:
    if analysis_config_sha256() != EXPECTED_ANALYSIS_CONFIG_SHA256:
        raise SystemExit("analysis prohibited: locked analysis configuration hash mismatch")
    condition_map = _load_condition_map(condition_map_path)
    expected_seeds = [VARIANT_SEED_START + i for i in range(VARIANT_SEEDS)]
    paths = [dataset_dir / f"solo_p30_variant_seed_{seed}.json" for seed in expected_seeds]
    if any(not p.is_file() for p in paths):
        missing = [p.name for p in paths if not p.is_file()]
        raise SystemExit(f"analysis prohibited: missing exact Epoch 003 seed artifacts: {missing!r}")
    extras = sorted(p.name for p in dataset_dir.glob("solo_p30_variant_seed_*.json") if p not in paths)
    if extras:
        raise SystemExit(f"analysis prohibited: unexpected Epoch 003 seed artifacts: {extras!r}")

    effects = []
    for expected_seed, path in zip(expected_seeds, paths, strict=True):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("seed_id") != expected_seed:
            raise SystemExit(f"analysis prohibited: seed identity mismatch in {path.name}")
        records = doc.get("records")
        if not isinstance(records, list) or len(records) != 180:
            raise SystemExit(f"analysis prohibited: incomplete matrix in {path.name}")
        if any(record.get("experiment_id") != VARIANT_EXPERIMENT_ID for record in records):
            raise SystemExit(f"analysis prohibited: wrong experiment identity in {path.name}")
        effects.append(seed_effect_from_artifact(doc, condition_map=condition_map))

    estimate = primary_estimate(effects)
    ci = paired_bootstrap_ci(
        effects,
        resamples=BOOTSTRAP_RESAMPLES,
        seed=BOOTSTRAP_SEED,
        alpha=ALPHA,
    )
    mechanical = decision(effects, ci)
    variant_classification = {
        "SUPPORTS_DIRECTIONAL_DGAF": "SUPPORTS_DIRECTIONAL_DGAF_P30_EXPLICIT_0_45_VARIANT",
        "EVIDENCE_AGAINST_DIRECTIONAL_DGAF": "EVIDENCE_AGAINST_DIRECTIONAL_DGAF_P30_EXPLICIT_0_45_VARIANT",
        "NOT_SUPPORTED_OR_INCONCLUSIVE": "VARIANT_NOT_SUPPORTED_OR_INCONCLUSIVE",
    }[mechanical]
    return {
        "record_type": "DGAF_PDMAL_SOLO_P30_VARIANT_EPOCH_003_PRIMARY_ANALYSIS",
        "schema_version": 1,
        "experiment_id": VARIANT_EXPERIMENT_ID,
        "variant_scope": VARIANT_SCOPE,
        "canonical_dgaf_efficacy_claim_allowed": False,
        "real_or_calibrated_apogee_confidence": False,
        "seed_start": VARIANT_SEED_START,
        "seed_count": VARIANT_SEEDS,
        "paired_seed_effect_count": len(effects),
        "primary_estimate_dgaf_variant_minus_null": estimate,
        "paired_bootstrap_ci_95": [ci[0], ci[1]],
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "alpha": ALPHA,
        "analysis_config_sha256": EXPECTED_ANALYSIS_CONFIG_SHA256,
        "mechanical_base_classification": mechanical,
        "variant_classification": variant_classification,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir", type=Path)
    parser.add_argument("condition_map", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = analyze(args.dataset_dir, args.condition_map)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"EPOCH_003_PRIMARY_ANALYSIS_COMPLETE: {result['variant_classification']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
