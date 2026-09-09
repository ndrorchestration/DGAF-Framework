#!/usr/bin/env python3
"""Synthetic timing for the complete 50-seed PDMAL task-execution shape.

This correction exists because the component Mode-T timing harness measures one
180-trial seed-shaped matrix per repetition while canonical ``run_pilot`` loops
50 planned empirical seeds sequentially. This module measures that full
50 x 180 = 9,000 task shape without pilot authorization, protected material,
or retention of scientific outcomes.

The resulting evidence is deliberately *not* a complete C-to-L timing record.
Artifact-set publication/independent retention and external transparency remain
separate required stages before any analysis-lock window W can be proposed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic

import numpy as np

import mode_t_timing_study as component

EVIDENCE_CLASS = "P4_MODE_T_SYNTHETIC_FULL_PILOT_TASK_TIMING_V1"
PILOT_SEED_COUNT = 50
DEFAULT_REPETITIONS = 3
DEFAULT_SEED_BASE = 2026090600
MAX_REPETITIONS = 10


def expected_total_trials() -> int:
    return PILOT_SEED_COUNT * component.expected_trials_per_seed()


def _stats(values: list[float]) -> dict[str, float | int]:
    arr = np.asarray(values, dtype=float)
    if arr.size < 1 or not np.all(np.isfinite(arr)) or np.any(arr < 0):
        raise ValueError("timing samples must be finite and non-negative")
    return {
        "sample_count": int(arr.size),
        "min_ms": round(float(np.min(arr)), 3),
        "p50_ms": round(float(np.quantile(arr, 0.50)), 3),
        "p95_ms": round(float(np.quantile(arr, 0.95)), 3),
        "max_ms": round(float(np.max(arr)), 3),
        "mean_ms": round(float(np.mean(arr)), 3),
    }


def measure_complete_task_shape(*, seed_base: int, seed_count: int = PILOT_SEED_COUNT) -> dict:
    """Execute the canonical task shape for exactly 50 sequential synthetic seeds."""
    if not isinstance(seed_base, int) or isinstance(seed_base, bool) or seed_base < 1:
        raise ValueError("seed_base must be a positive integer")
    if seed_count != PILOT_SEED_COUNT:
        raise ValueError("full-pilot timing requires exactly 50 sequential seeds")

    trials_per_seed = component.expected_trials_per_seed()
    if trials_per_seed != 180:
        raise RuntimeError("canonical trial shape drifted from 180 trials per seed")

    seed_samples_ms: list[float] = []
    started = monotonic()
    for offset in range(seed_count):
        seed = seed_base + offset
        elapsed_ms = component.measure_full_synthetic_matrix(seed)
        if not math.isfinite(elapsed_ms) or elapsed_ms < 0:
            raise RuntimeError("invalid per-seed timing result")
        seed_samples_ms.append(float(elapsed_ms))
    elapsed_ms = (monotonic() - started) * 1000.0

    if len(seed_samples_ms) != PILOT_SEED_COUNT:
        raise RuntimeError("full-pilot timing did not execute exactly 50 seeds")

    return {
        "seed_base": seed_base,
        "seed_count": PILOT_SEED_COUNT,
        "trials_per_seed": trials_per_seed,
        "total_trials": PILOT_SEED_COUNT * trials_per_seed,
        "execution_order": "sequential_seed_loop",
        "full_task_shape_duration_ms": round(elapsed_ms, 6),
        "per_seed_duration_statistics": _stats(seed_samples_ms),
    }


def run_study(*, output_path: Path, repetitions: int = DEFAULT_REPETITIONS) -> dict:
    if (
        not isinstance(repetitions, int)
        or isinstance(repetitions, bool)
        or not 1 <= repetitions <= MAX_REPETITIONS
    ):
        raise ValueError(f"repetitions must be between 1 and {MAX_REPETITIONS}")

    repetitions_out: list[dict] = []
    full_samples_ms: list[float] = []
    for index in range(repetitions):
        measurement = measure_complete_task_shape(
            seed_base=DEFAULT_SEED_BASE + (index * PILOT_SEED_COUNT)
        )
        repetitions_out.append(measurement)
        full_samples_ms.append(float(measurement["full_task_shape_duration_ms"]))

    if any(item["total_trials"] != 9000 for item in repetitions_out):
        raise RuntimeError("full-pilot timing total-trial invariant failed")

    artifact = {
        "schema_version": 1,
        "evidence_class": EVIDENCE_CLASS,
        "epistemic_status": "BOUNDED_FULL_TASK_SHAPE_NOT_COMPLETE_C_TO_L_TIMING",
        "issue": 293,
        "parent_issue": 287,
        "control_plane_sha": os.environ.get("EVIDENCE_SHA", "unknown"),
        "workflow_content_sha256": os.environ.get("FULL_TIMING_WORKFLOW_SHA256", "unknown"),
        "helper_content_sha256": os.environ.get("FULL_TIMING_HELPER_SHA256", "unknown"),
        "component_helper_sha256": os.environ.get("COMPONENT_TIMING_HELPER_SHA256", "unknown"),
        "run_pilot_content_sha256": os.environ.get("RUN_PILOT_SHA256", "unknown"),
        "runner_class": os.environ.get("RUNNER_CLASS", "unknown"),
        "repetitions": repetitions,
        "synthetic_seed_count_per_repetition": PILOT_SEED_COUNT,
        "trials_per_seed": component.expected_trials_per_seed(),
        "total_trials_per_repetition": expected_total_trials(),
        "canonical_seed_execution_semantics": "sequential",
        "full_task_shape_duration_statistics": _stats(full_samples_ms),
        "measurements": repetitions_out,
        "full_boundary_contiguous_timing_established": False,
        "complete_blinded_artifact_set_publication_timed": False,
        "accepted_independent_retention_timed": False,
        "external_transparency_timed": False,
        "coverage_complete": False,
        "w_proposal_eligible": False,
        "numeric_w_selected": False,
        "proposed_w_seconds": None,
        "protocol_frozen": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "protected_material_present": False,
        "secret_instantiation": False,
        "unblinding_requested": False,
        "empirical_n": 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(artifact, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="utf-8"
    )
    return artifact


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=DEFAULT_REPETITIONS)
    args = parser.parse_args(argv)
    artifact = run_study(output_path=args.output, repetitions=args.repetitions)
    print(
        json.dumps(
            {
                "status": "PASS",
                "evidence_class": artifact["evidence_class"],
                "repetitions": artifact["repetitions"],
                "total_trials_per_repetition": artifact["total_trials_per_repetition"],
                "w_proposal_eligible": artifact["w_proposal_eligible"],
                "numeric_w_selected": artifact["numeric_w_selected"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
