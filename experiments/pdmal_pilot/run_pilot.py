#!/usr/bin/env python3
"""Fail-closed PDMAL pilot runner.

Three explicit execution modes exist:

- ``contract``: non-empirical contract rehearsal only;
- ``solo_pilot``: empirical developer-run pilot with self-freeze/self-authorization;
- ``pilot``: the existing high-assurance pilot path.

Both empirical modes require an exact frozen git SHA, protected blinding material,
and durable retention. The solo track is intentionally distinguishable in its
experiment identity and must not be represented as independently reviewed,
Confidential-Space-qualified, or high-assurance evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import os
import subprocess
from pathlib import Path
from time import monotonic

import numpy as np

from durable_retention import archive_artifact, require_archive_root
from harness_contract import TOPOLOGY_SPECS, deterministic_contract_run, generate_topology, make_streams
from pilot_artifact_schema import ARTIFACT_SCHEMA_VERSION, canonical_json_bytes, validate_artifact, verify_sidecar
from task_engine import AttemptStatus, CONDITION_VALUES, ConsensusTask, RetryPolicy, SEED_RUNTIME_CEILING_SECONDS, ScriptedTask, execute_trial
from topology_utils import graph_fingerprint

SUPPORTED_MODES = {"contract", "solo_pilot", "pilot"}
CONTRACT_ROOT_SEEDS = (20260817, 20260818)
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
PROTOCOL_VERSION = "0.7.6"
MIN_BLINDING_KEY_CHARS = 32
CONDITION_ID_DOMAIN = b"PDMAL-BLINDED-CONDITION-ID-v1"
TRIAL_ORDER_DOMAIN = b"PDMAL-BLINDED-TRIAL-ORDER-v1"
SOLO_EXPERIMENT_ID = "PDMAL-SOLO-PILOT-V1"
HIGH_ASSURANCE_EXPERIMENT_ID = "PDMAL-PILOT-V1"


def require_mode() -> str:
    mode = os.getenv("PDMAL_MODE")
    if mode not in SUPPORTED_MODES:
        raise SystemExit("PDMAL_MODE must be explicitly set to 'contract', 'solo_pilot', or 'pilot'.")
    return mode


def _current_head_sha() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, cwd=Path(__file__).resolve().parents[2])
    if result.returncode != 0:
        raise SystemExit("pilot execution prohibited: unable to resolve git HEAD")
    return result.stdout.strip()


def require_frozen_commit() -> str:
    expected = os.getenv("PDMAL_FROZEN_COMMIT_SHA", "").strip().lower()
    if len(expected) != 40 or any(c not in "0123456789abcdef" for c in expected):
        raise SystemExit("pilot execution prohibited: PDMAL_FROZEN_COMMIT_SHA must be a full 40-character SHA")
    actual = _current_head_sha().lower()
    if not hmac.compare_digest(actual, expected):
        raise SystemExit(f"pilot execution prohibited: frozen SHA mismatch (expected {expected}, actual {actual})")
    return actual


def _require_blinding_and_archive() -> tuple[str, Path]:
    key = os.getenv("PDMAL_BLINDING_KEY", "")
    if len(key) < MIN_BLINDING_KEY_CHARS:
        raise SystemExit(
            f"pilot execution prohibited: PDMAL_BLINDING_KEY must contain at least {MIN_BLINDING_KEY_CHARS} characters"
        )
    try:
        archive_root = require_archive_root()
    except RuntimeError as exc:
        raise SystemExit(f"pilot execution prohibited: {exc}") from exc
    return key, archive_root


def require_pilot_authorization() -> tuple[str, Path]:
    """Require the original high-assurance pilot authorization boundary."""
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("pilot execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required")
    if os.getenv("PDMAL_PILOT_AUTHORIZED") != "1":
        raise SystemExit("pilot execution prohibited: PDMAL_PILOT_AUTHORIZED=1 is required")
    return _require_blinding_and_archive()


def require_solo_pilot_authorization() -> tuple[str, Path]:
    """Require explicit self-freeze and self-authorization for Solo Pilot evidence.

    This intentionally does not satisfy the independent/high-assurance gate. A
    separate limitations acknowledgement is required to make accidental use of
    the relaxed track harder.
    """
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("solo pilot execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required")
    if os.getenv("PDMAL_SOLO_PILOT_AUTHORIZED") != "1":
        raise SystemExit("solo pilot execution prohibited: PDMAL_SOLO_PILOT_AUTHORIZED=1 is required")
    if os.getenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED") != "1":
        raise SystemExit(
            "solo pilot execution prohibited: PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED=1 is required"
        )
    if os.getenv("PDMAL_PILOT_AUTHORIZED") == "1":
        raise SystemExit(
            "solo pilot execution prohibited: high-assurance PDMAL_PILOT_AUTHORIZED must not be asserted in solo mode"
        )
    return _require_blinding_and_archive()


def blind_condition(condition: str, key: str) -> str:
    digest = hmac.new(
        key.encode("utf-8"),
        CONDITION_ID_DOMAIN + b"|" + condition.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"blind_{digest[:16]}"


def _trial_combinations() -> list[tuple[str, str, int]]:
    """Return the complete canonical matrix without assigning public order."""
    return [
        (topology, condition, failure_count)
        for topology in TOPOLOGY_SPECS
        for condition in CONDITION_VALUES
        for failure_count in FAILURE_COUNTS
    ]


def _trial_order_token(
    *, key: str, seed: int, topology: str, condition: str, failure_count: int
) -> bytes:
    """Return a domain-separated secret ordering token for one matrix cell."""
    if not key:
        raise ValueError("blinded trial ordering requires a non-empty protected key")
    payload = f"{seed}|{topology}|{condition}|{failure_count}".encode("utf-8")
    return hmac.new(
        key.encode("utf-8"), TRIAL_ORDER_DOMAIN + b"|" + payload, hashlib.sha256
    ).digest()


def blinded_trial_schedule(*, seed: int, key: str) -> list[tuple[str, str, int]]:
    """Construct the exact matrix in a protected, reproducible per-seed order.

    Public root-seed information alone must not reveal condition position. The
    schedule becomes independently reconstructible only after release of the
    protected blinding material.
    """
    combinations = _trial_combinations()
    keyed = [
        (
            _trial_order_token(
                key=key,
                seed=seed,
                topology=topology,
                condition=condition,
                failure_count=failure_count,
            ),
            (topology, condition, failure_count),
        )
        for topology, condition, failure_count in combinations
    ]
    tokens = [token for token, _ in keyed]
    if len(tokens) != len(set(tokens)):
        raise RuntimeError("pilot execution prohibited: blinded trial-order token collision")
    ordered = [combo for _, combo in sorted(keyed, key=lambda item: item[0])]
    if len(ordered) != 180 or set(ordered) != set(combinations):
        raise RuntimeError("pilot execution prohibited: blinded trial schedule is incomplete")
    return ordered


def _environment_fingerprint() -> str:
    import networkx as nx
    import platform
    return hashlib.sha256(f"{platform.python_version()}|{np.__version__}|{nx.__version__}".encode()).hexdigest()


def _write_sidecar(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    sidecar = f"{digest}  {path.name}\n"
    path.with_suffix(path.suffix + ".sha256").write_text(sidecar, encoding="utf-8")
    return sidecar


def _write_and_validate_artifact(path: Path, document: dict, expected_seed: int) -> None:
    raw = canonical_json_bytes(document)
    path.write_bytes(raw)
    sidecar = _write_sidecar(path)
    validate_artifact(document, expected_seed=expected_seed)
    verify_sidecar(raw, sidecar, path.name)


def _retain(path: Path, archive_root: Path, frozen_sha: str, *, kind: str) -> None:
    archive_artifact(path, archive_root=archive_root, freeze_sha=frozen_sha, metadata={"artifact_kind": kind})


def run_contract(output_dir: Path) -> int:
    key = b"contract-only-test-key-000000000000000000"
    for seed in CONTRACT_ROOT_SEEDS:
        results = deterministic_contract_run(seed, key)
        if len(results) != 5 or not all(r.topology_valid for r in results):
            raise SystemExit(f"contract validation failed for seed {seed}")
        trial = execute_trial(ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.SUCCESS]), seed=seed, condition="CONTRACT_ONLY", policy=RetryPolicy(recovery_window_seconds=0.0), sleeper=lambda _: None, isolate=False)
        if not trial.ffcr_success:
            raise SystemExit(f"retry contract failed for seed {seed}")
    output_dir.mkdir(parents=True, exist_ok=True)
    print("CONTRACT_MODE_PASS: two validation seeds exercised; no empirical data collection performed")
    return 0


def run_pilot(output_dir: Path, seeds: int, *, solo: bool = False) -> int:
    frozen_sha = require_frozen_commit()
    if solo:
        blinding_key, archive_root = require_solo_pilot_authorization()
        experiment_id = SOLO_EXPERIMENT_ID
        artifact_prefix = "solo_pilot"
        artifact_kind = "solo_pilot_seed"
        completion_label = "SOLO_PILOT_MODE_COMPLETE"
    else:
        blinding_key, archive_root = require_pilot_authorization()
        experiment_id = HIGH_ASSURANCE_EXPERIMENT_ID
        artifact_prefix = "pilot"
        artifact_kind = "pilot_seed"
        completion_label = "PILOT_MODE_COMPLETE"
    os.environ.pop("PDMAL_BLINDING_KEY", None)
    if seeds < 1:
        raise SystemExit("--seeds must be >= 1")
    if len(_trial_combinations()) != 180:
        raise SystemExit("pilot execution prohibited: canonical matrix must contain exactly 180 cells")
    output_dir.mkdir(parents=True, exist_ok=True)
    environment_fingerprint = _environment_fingerprint()
    for seed_idx in range(seeds):
        seed = 20260819 + seed_idx
        seed_start = monotonic()
        streams = make_streams(seed)
        records: list[dict] = []
        combinations = blinded_trial_schedule(seed=seed, key=blinding_key)
        for trial_idx, (topology, condition, failure_count) in enumerate(combinations):
            task = ConsensusTask(topology=topology, failure_count=failure_count, condition=condition)
            try:
                result = task.run_detailed(seed=seed, attempt=1)
                status = result.attempt_status
            except Exception:
                result = None
                status = AttemptStatus.FAILURE
            raw_trial = {
                "trial_key": task.trial_key(seed, topology, condition, failure_count), "seed": seed,
                "topology": topology, "condition": condition, "failure_count": failure_count,
                "failure_nodes": [int(n) for n in result.failure_nodes] if result else [],
                "initial_values": [float(v) for v in result.initial_values] if result else [],
                "final_values": [float(v) for v in result.final_values] if result else [],
                "final_std": float(result.final_std) if result else 0.0,
                "topology_fingerprint": result.topology_fingerprint if result else graph_fingerprint(generate_topology(topology, streams["topology_construction"])),
                "iterations_completed": result.iterations_completed if result else 0,
                "attempt_status": status.value,
                "consensus_success": bool(result.consensus_success) if result else False,
                "deviation": result.deviation if result else None,
                # Detailed governance trace remains process-local. It is
                # intentionally excluded from the public blinded artifact.
                "governance_trace": list(result.governance_trace) if result else [],
            }
            execution_success = status is AttemptStatus.SUCCESS
            recovered = failure_count > 0 and execution_success
            record = {
                "experiment_id": experiment_id, "protocol_version": PROTOCOL_VERSION,
                "experiment_commit_sha": frozen_sha, "seed_id": seed,
                "blinded_condition_id": blind_condition(condition, blinding_key), "trial_id": trial_idx,
                "topology": topology, "failure_count": failure_count,
                "primary_outcome": raw_trial["final_std"],
                "secondary_outcomes": {"final_mean": float(np.mean(raw_trial["final_values"])) if raw_trial["final_values"] else 0.0},
                "failure": failure_count > 0, "recovery": recovered,
                "ffcr_success": bool(raw_trial["consensus_success"] and execution_success),
                "status": "RECOVERED" if recovered else ("SUCCESS" if execution_success else "UNRECOVERED_FAILURE"),
                "excluded": False, "exclusion_reason": None,
                "environment_fingerprint": environment_fingerprint,
            }
            record["artifact_sha256"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
            records.append(record)
        elapsed = monotonic() - seed_start
        if elapsed > SEED_RUNTIME_CEILING_SECONDS:
            raise SystemExit(f"pilot execution prohibited: seed {seed} exceeded runtime ceiling ({elapsed:.3f}s)")
        document = {
            "schema_version": ARTIFACT_SCHEMA_VERSION,
            "artifact_version": f"{artifact_prefix}-seed-{seed}",
            "protocol_status": "FROZEN",
            "empirical_data_collection": True,
            "frozen_commit_sha": frozen_sha,
            "seed_id": seed,
            "runtime_seconds": elapsed,
            "records": records,
        }
        path = output_dir / f"{artifact_prefix}_seed_{seed}.json"
        _write_and_validate_artifact(path, document, expected_seed=seed)
        _retain(path, archive_root, frozen_sha, kind=artifact_kind)
        _retain(path.with_suffix(path.suffix + ".sha256"), archive_root, frozen_sha, kind=f"{artifact_kind}_sidecar")
    summary = {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_version": f"{artifact_prefix}_summary",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "validation_track": "SOLO_DEVELOPER" if solo else "HIGH_ASSURANCE",
        "independently_verified": False if solo else True,
        "frozen_commit_sha": frozen_sha,
        "total_seeds": seeds,
        "trials_per_seed": len(_trial_combinations()),
        "total_trials": seeds * len(_trial_combinations()),
        "environment_fingerprint": environment_fingerprint,
    }
    summary_path = output_dir / f"{artifact_prefix}_summary.json"
    raw_summary = canonical_json_bytes(summary)
    summary_path.write_bytes(raw_summary)
    _write_sidecar(summary_path)
    _retain(summary_path, archive_root, frozen_sha, kind=f"{artifact_prefix}_summary")
    _retain(summary_path.with_suffix(summary_path.suffix + ".sha256"), archive_root, frozen_sha, kind=f"{artifact_prefix}_summary_sidecar")
    print(f"{completion_label}: {seeds} seeds; {seeds * len(_trial_combinations())} observations")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts"))
    args = parser.parse_args(argv)
    mode = require_mode()
    if mode == "contract":
        if args.seeds != 2:
            raise SystemExit("contract mode is fixed at 2 validation seeds")
        return run_contract(args.output_dir)
    if mode == "solo_pilot":
        return run_pilot(args.output_dir, args.seeds, solo=True)
    return run_pilot(args.output_dir, args.seeds, solo=False)


if __name__ == "__main__":
    raise SystemExit(main())
