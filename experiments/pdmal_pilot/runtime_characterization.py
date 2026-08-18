#!/usr/bin/env python3
"""Non-empirical runtime characterization for the v0.7.4 PDMAL workload.

This harness measures operational runtime only. It does not invoke ``run_pilot``
contract/pilot modes, does not authorize pilot execution, and does not write
pilot artifacts. Each trial is executed once with the deterministic
``ConsensusTask`` using a fixed trial identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from time import monotonic

from task_engine import (
    CONSENSUS_ITERATIONS,
    CONSENSUS_THRESHOLD,
    SEED_RUNTIME_CEILING_SECONDS,
    AttemptStatus,
    ConsensusTask,
)

CHARACTERIZATION_ID = "PDMAL_RUNTIME_CHAR_v1"
DEFAULT_SEEDS = (20260817, 20260818, 20260819)
DEFAULT_CONDITIONS = ("null", "simple", "static", "dgaf")
DEFAULT_TOPOLOGIES = ("ring", "pdmal")
DEFAULT_FAILURE_COUNTS = (0, 2, 5)


def _stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"min_ms": None, "max_ms": None, "mean_ms": None, "stdev_ms": None}
    return {
        "min_ms": min(values),
        "max_ms": max(values),
        "mean_ms": mean(values),
        "stdev_ms": pstdev(values) if len(values) > 1 else 0.0,
    }


def run_characterization(
    *,
    output_dir: Path,
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    conditions: tuple[str, ...] = DEFAULT_CONDITIONS,
    topologies: tuple[str, ...] = DEFAULT_TOPOLOGIES,
    failure_counts: tuple[int, ...] = DEFAULT_FAILURE_COUNTS,
) -> dict:
    if not seeds:
        raise ValueError("at least one characterization seed is required")
    if not conditions or not topologies or not failure_counts:
        raise ValueError("characterization matrix must not be empty")

    output_dir.mkdir(parents=True, exist_ok=True)
    trial_results: list[dict] = []
    seed_results: list[dict] = []

    for seed in seeds:
        seed_started = monotonic()
        for condition in conditions:
            for topology in topologies:
                for failure_count in failure_counts:
                    task = ConsensusTask(
                        topology=topology,
                        failure_count=failure_count,
                        condition=condition,
                    )
                    trial_started = monotonic()
                    result = task.run_detailed(seed=seed, attempt=1)
                    runtime_ms = (monotonic() - trial_started) * 1000.0

                    trial_results.append(
                        {
                            "seed": seed,
                            "condition": condition,
                            "topology": topology,
                            "failure_count": failure_count,
                            "runtime_ms": round(runtime_ms, 3),
                            "attempt_status": result.attempt_status.value,
                            "iterations_completed": result.iterations_completed,
                            "final_std": result.final_std,
                            "consensus_success": result.consensus_success,
                            "trial_key": result.trial_key,
                            "topology_fingerprint": result.topology_fingerprint,
                            "failure_nodes": list(result.failure_nodes),
                            "deviation": result.deviation,
                        }
                    )

        seed_runtime_seconds = monotonic() - seed_started
        seed_results.append(
            {
                "seed": seed,
                "runtime_ms": round(seed_runtime_seconds * 1000.0, 3),
                "ceiling_seconds": SEED_RUNTIME_CEILING_SECONDS,
                "ceiling_met": seed_runtime_seconds <= SEED_RUNTIME_CEILING_SECONDS,
            }
        )

    seed_runtimes = [entry["runtime_ms"] for entry in seed_results]
    trial_runtimes = [entry["runtime_ms"] for entry in trial_results]
    failed_trials = [entry for entry in trial_results if entry["attempt_status"] != AttemptStatus.SUCCESS.value]

    artifact = {
        "experiment": "runtime_characterization",
        "characterization_id": CHARACTERIZATION_ID,
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "non_empirical_operational_verification": True,
        "consensus_iterations": CONSENSUS_ITERATIONS,
        "consensus_threshold": CONSENSUS_THRESHOLD,
        "seed_count": len(seeds),
        "seeds": list(seeds),
        "conditions": list(conditions),
        "topologies": list(topologies),
        "failure_counts": list(failure_counts),
        "expected_trial_count": len(seeds) * len(conditions) * len(topologies) * len(failure_counts),
        "completed_trial_count": len(trial_results),
        "seed_results": seed_results,
        "trial_results": trial_results,
        "trial_runtime_stats": _stats(trial_runtimes),
        "seed_runtime_stats": _stats(seed_runtimes),
        "ceiling_passed": all(entry["ceiling_met"] for entry in seed_results),
        "all_trials_completed": len(failed_trials) == 0 and len(trial_results) == len(seeds) * len(conditions) * len(topologies) * len(failure_counts),
        "failed_trial_count": len(failed_trials),
        "git_sha": os.environ.get("GITHUB_SHA", "unknown"),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    raw = (json.dumps(artifact, indent=2, sort_keys=True) + "\n").encode("utf-8")
    artifact_path = output_dir / "runtime_characterization.json"
    artifact_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    (output_dir / "runtime_characterization.json.sha256").write_text(
        f"{digest}  {artifact_path.name}\n", encoding="utf-8"
    )

    if not artifact["all_trials_completed"]:
        raise SystemExit("Runtime characterization failed: one or more task trials did not complete successfully.")
    if not artifact["ceiling_passed"]:
        raise SystemExit("Runtime characterization failed: at least one seed exceeded the 300-second ceiling.")
    if not math.isfinite(max(seed_runtimes, default=0.0)):
        raise SystemExit("Runtime characterization failed: non-finite runtime observed.")

    print(json.dumps({
        "characterization_id": CHARACTERIZATION_ID,
        "seed_runtime_stats": artifact["seed_runtime_stats"],
        "trial_runtime_stats": artifact["trial_runtime_stats"],
        "ceiling_passed": artifact["ceiling_passed"],
        "all_trials_completed": artifact["all_trials_completed"],
        "artifact": str(artifact_path),
    }, indent=2, sort_keys=True))
    return artifact


def parse_csv(value: str) -> tuple[str, ...]:
    items = tuple(item.strip() for item in value.split(",") if item.strip())
    if not items:
        raise argparse.ArgumentTypeError("value must contain at least one item")
    return items


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("runtime_artifacts"))
    parser.add_argument("--seeds", default=",".join(str(seed) for seed in DEFAULT_SEEDS), type=parse_csv)
    parser.add_argument("--conditions", default=",".join(DEFAULT_CONDITIONS), type=parse_csv)
    parser.add_argument("--topologies", default=",".join(DEFAULT_TOPOLOGIES), type=parse_csv)
    parser.add_argument("--failure-counts", default=",".join(str(x) for x in DEFAULT_FAILURE_COUNTS), type=parse_csv)
    args = parser.parse_args(argv)

    seeds = tuple(int(value) for value in args.seeds)
    failure_counts = tuple(int(value) for value in args.failure_counts)
    run_characterization(
        output_dir=args.output_dir,
        seeds=seeds,
        conditions=args.conditions,
        topologies=args.topologies,
        failure_counts=failure_counts,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
