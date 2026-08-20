#!/usr/bin/env python3
"""Fail-closed PDMAL experiment runner.

Contract mode is the only executable mode while the protocol is PRE-FREEZE.
Pilot mode requires both protocol freeze AND explicit authorization. When both
are present, the runner invokes the real experimental task executor.

This module never silently upgrades modes.
"""
from __future__ import annotations

import argparse
import hashlib
import numpy as np
import json
import os
import sys
from pathlib import Path
from time import monotonic

from harness_contract import (
    TOPOLOGY_SPECS,
    EXPERIMENT_CONDITIONS,
    generate_topology,
    make_streams,
    stream_fingerprint,
    validate_topology,
    deterministic_contract_run,
)
from task_engine import (
    AttemptStatus,
    RetryPolicy,
    ScriptedTask,
    execute_trial,
    ConsensusTask,
    CONDITION_VALUES,
    FAILURE_INJECTION_ITERATION,
    FAILURE_RECOVERY_ITERATION,
    CONSENSUS_ITERATIONS,
    SEED_RUNTIME_CEILING_SECONDS,
)
from topology_utils import graph_fingerprint

SUPPORTED_MODES = {"contract", "pilot"}
CONTRACT_ROOT_SEEDS = (20260817, 20260818)
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)


def require_contract_mode() -> None:
    mode = os.getenv("PDMAL_MODE")
    if mode not in SUPPORTED_MODES:
        raise SystemExit("PDMAL_MODE must be explicitly set to 'contract' or 'pilot'.")


def write_contract_artifact(output_dir: Path, seed: int, payload: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
    }
    path = output_dir / f"contract_seed_{seed}.json"
    raw = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{digest}  {path.name}\n", encoding="utf-8"
    )


def run_contract(output_dir: Path) -> int:
    key = b"contract-only-test-key-000000000000000000"
    for seed in CONTRACT_ROOT_SEEDS:
        results = deterministic_contract_run(seed, key)
        if len(results) != 5 or not all(r.topology_valid for r in results):
            raise SystemExit(f"contract validation failed for seed {seed}")

        scripted = ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.SUCCESS])
        trial = execute_trial(
            scripted,
            seed=seed,
            condition="CONTRACT_ONLY",
            policy=RetryPolicy(recovery_window_seconds=0.0),
            monotonic_clock=monotonic,
            sleeper=lambda _: None,
            isolate=False,
        )
        if not trial.ffcr_success:
            raise SystemExit(f"retry contract failed for seed {seed}")

        write_contract_artifact(
            output_dir,
            seed,
            {
                "seed": seed,
                "stream_fingerprint": stream_fingerprint(seed),
                "topology_contracts": [result.__dict__ for result in results],
                "retry_contract": {
                    "status": trial.status.value,
                    "ffcr_success": trial.ffcr_success,
                    "recovery_wait_seconds": trial.recovery_wait_seconds,
                    "attempts": [
                        {
                            "attempt": attempt.attempt,
                            "status": attempt.status.value,
                            "elapsed_seconds": attempt.elapsed_seconds,
                            "isolated": attempt.isolated,
                            "termination_reason": attempt.termination_reason,
                        }
                        for attempt in trial.attempts
                    ],
                },
            },
        )

    print(
        "CONTRACT_MODE_PASS: two validation seeds exercised; "
        "no empirical data collection performed"
    )
    return 0


def _trial_combinations() -> list[tuple[str, str, int]]:
    """Generate all (topology, condition, failure_count) combinations.

    5 topologies × 4 conditions × 9 failure counts = 180 trials per seed.
    """
    combinations: list[tuple[str, str, int]] = []
    for topology in TOPOLOGY_SPECS:
        for condition in CONDITION_VALUES:
            for failure_count in FAILURE_COUNTS:
                combinations.append((topology, condition, failure_count))
    return combinations


def run_pilot(output_dir: Path, seeds: int) -> int:
    output_dir = Path(output_dir)
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit(
            "pilot execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required"
        )
    if os.getenv("PDMAL_PILOT_AUTHORIZED") != "1":
        raise SystemExit(
            "pilot execution prohibited: PDMAL_PILOT_AUTHORIZED=1 is required"
        )

    combinations = _trial_combinations()
    total_trials = len(combinations) * seeds
    print(
        f"PILOT_MODE: executing {seeds} seeds × {len(combinations)} trials/seed "
        f"= {total_trials} total observations"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    all_results: list[dict] = []
    seed_records: list[dict] = []

    for seed_idx in range(seeds):
        seed = 20260819 + seed_idx
        print(f"  Seed {seed_idx + 1}/{seeds} (root seed {seed})...")

        streams = make_streams(seed)
        seed_results: list[dict] = []
        seed_start = monotonic()

        for trial_idx, (topology, condition, failure_count) in enumerate(combinations):
            task = ConsensusTask(
                topology=topology,
                failure_count=failure_count,
                condition=condition,
            )
            try:
                result = task.run_detailed(seed=seed, attempt=1)
                status = result.attempt_status
            except Exception as exc:
                status = AttemptStatus.FAILURE
                result = None
                exc_info = f"{type(exc).__name__}: {exc}"
                print(f"    Trial {trial_idx + 1}/180: FAILURE ({exc_info})")
            else:
                if trial_idx % 30 == 0:
                    print(f"    Trial {trial_idx + 1}/180: {status.value}")

            seed_results.append(
                {
                    "trial_key": task.trial_key(seed, topology, condition, failure_count)
                    if result
                    else hashlib.sha256(
                        f"{seed}|{topology}|{condition}|{failure_count}".encode()
                    ).hexdigest(),
                    "seed": seed,
                    "topology": topology,
                    "condition": condition,
                    "failure_count": failure_count,
                    "failure_nodes": (
                        [int(n) for n in result.failure_nodes]
                        if result and result.failure_nodes
                        else []
                    ),
                    "initial_values": (
                        [float(v) for v in result.initial_values]
                        if result and result.initial_values
                        else []
                    ),
                    "final_values": (
                        [float(v) for v in result.final_values]
                        if result and result.final_values
                        else []
                    ),
                    "final_std": float(result.final_std) if result else 0.0,
                    "topology_fingerprint": (
                        result.topology_fingerprint if result else graph_fingerprint(
                            generate_topology(topology, streams["topology_construction"])
                        )
                    ),
                    "iterations_completed": (
                        result.iterations_completed if result else 0
                    ),
                    "attempt_status": status.value,
                    "deviation": result.deviation if result else None,
                }
            )

        seed_elapsed = monotonic() - seed_start
        print(f"  Seed {seed_idx + 1} complete: {len(seed_results)} trials in {seed_elapsed:.1f}s")

        seed_records.append(
            {
                "seed_id": seed,
                "root_seed": seed,
                "stream_fingerprint": stream_fingerprint(seed),
                "trials": seed_results,
                "runtime_seconds": seed_elapsed,
                "trials_total": len(seed_results),
                "trials_success": sum(
                    1 for r in seed_results if r["attempt_status"] == "SUCCESS"
                ),
                "trials_failed": sum(
                    1 for r in seed_results if r["attempt_status"] == "FAILURE"
                ),
            }
        )
        all_results.extend(seed_results)

    # Write per-seed artifact documents
    for idx, record in enumerate(seed_records):
        doc = {
            "schema_version": "1.0",
            "artifact_version": f"seed-{record['seed_id']}",
            "protocol_status": "PRE-FREEZE",
            "empirical_data_collection": False,
            "records": [
                {
                    "experiment_id": "PDMAL-PREFREEZE-V1",
                    "protocol_version": "0.7.4",
                    "experiment_commit_sha": _current_head_sha(),
                    "seed_id": record["seed_id"],
                    "blinded_condition_id": f"blind_unblinded_pre_freeze_{record['seed_id']}",
                    "trial_id": idx,
                    "primary_outcome": r["final_std"],
                    "secondary_outcomes": {
                        "final_mean": float(np.mean(r["final_values"]))
                        if r["final_values"]
                        else 0.0,
                        "topology": r["topology"],
                        "condition": r["condition"],
                        "failure_count": r["failure_count"],
                    },
                    "failure": r["failure_count"] > 0,
                    "recovery": True,
                    "runtime_ms": int(record["runtime_seconds"] * 1000 / len(seed_records)),
                    "status": r["attempt_status"],
                    "excluded": False,
                    "exclusion_reason": None,
                    "environment_fingerprint": _environment_fingerprint(),
                    "artifact_sha256": _compute_artifact_sha256(r),
                }
                for r in record["trials"]
            ],
        }

        path = output_dir / f"pilot_seed_{record['seed_id']}.json"
        raw = json.dumps(doc, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        path.write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        path.with_suffix(path.suffix + ".sha256").write_text(
            f"{digest}  {path.name}\n", encoding="utf-8"
        )

    # Write summary artifact
    summary = {
        "schema_version": "1.0",
        "artifact_version": "pilot_summary",
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "total_seeds": seeds,
        "total_trials": total_trials,
        "seeds": [
            {
                "seed_id": r["seed_id"],
                "runtime_seconds": r["runtime_seconds"],
                "trials_total": r["trials_total"],
                "trials_success": r["trials_success"],
                "trials_failed": r["trials_failed"],
            }
            for r in seed_records
        ],
        "experiment_commit_sha": _current_head_sha(),
        "artifact_sha256": _compute_summary_sha256(seed_records),
    }
    summary_path = output_dir / "pilot_summary.json"
    raw = json.dumps(summary, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    summary_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    summary_path.with_suffix(summary_path.suffix + ".sha256").write_text(
        f"{digest}  {summary_path.name}\n", encoding="utf-8"
    )

    print(
        f"PILOT_MODE_COMPLETE: {seeds} seeds executed; "
        f"{total_trials} total observations collected; "
        f"no empirical analysis performed (pre-freeze)"
    )
    return 0


def _current_head_sha() -> str:
    """Return the current git HEAD SHA, or a placeholder if unavailable."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent.parent,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:12]
    except Exception:
        pass
    return "unknown"


def _environment_fingerprint() -> str:
    """Return a deterministic environment fingerprint."""
    try:
        import numpy as _np
        import networkx as _nx
        import platform
        return hashlib.sha256(
            f"{platform.python_version()}|{ _np.__version__}|{ _nx.__version__}".encode()
        ).hexdigest()[:16]
    except Exception:
        return "unknown"


def _compute_artifact_sha256(record: dict) -> str:
    """Compute SHA-256 of a single trial record."""
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _compute_summary_sha256(records: list[dict]) -> str:
    """Compute SHA-256 of the summary artifact."""
    raw = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts"))
    args = parser.parse_args(argv)

    require_contract_mode()
    mode = os.environ["PDMAL_MODE"]
    if mode == "contract":
        if args.seeds != 2:
            raise SystemExit("contract mode is fixed at 2 validation seeds")
        return run_contract(args.output_dir)
    return run_pilot(args.output_dir, args.seeds)


if __name__ == "__main__":
    raise SystemExit(main())
