#!/usr/bin/env python3
"""Fresh blinded Solo empirical runner for DGAF-P30-EXPLICIT-0.45.

This runner is intentionally distinct from the canonical DGAF Solo runner. It tests
one explicitly named treatment variant in which the DGAF condition receives the
synthetic minimum-passing P-30 fixture established by non-empirical diagnostic
Epoch 002. The fixture is not a real or calibrated Apogee confidence and results
from this runner must not be promoted to canonical DGAF efficacy evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from time import monotonic

import numpy as np

from harness_contract import TOPOLOGY_SPECS, generate_topology, make_streams
from p30_remediation_diagnostic import (
    P30_BINDING_ID,
    P30_FIXTURE_CONFIDENCE,
    P30FixtureConsensusTask,
    validate_fixture_contract,
)
from pilot_artifact_schema import ARTIFACT_SCHEMA_VERSION, canonical_json_bytes
from run_pilot import (
    _environment_fingerprint,
    _require_blinding_and_archive,
    _retain,
    _trial_combinations,
    _write_and_validate_artifact,
    _write_sidecar,
    blind_condition,
    blinded_trial_schedule,
    require_frozen_commit,
)
from task_engine import AttemptStatus, ConsensusTask, SEED_RUNTIME_CEILING_SECONDS
from topology_utils import graph_fingerprint

PROTOCOL_VERSION = "0.7.6"
VARIANT_EXPERIMENT_ID = "PDMAL-SOLO-P30-EXPLICIT-V1"
VARIANT_SCOPE = "DGAF-P30-EXPLICIT-0.45"
VARIANT_MODE = "solo_p30_variant"
VARIANT_SEED_START = 20260901
VARIANT_SEEDS = 50
VARIANT_OBSERVATIONS = 9000
VARIANT_BINDING_KIND = "SYNTHETIC_MINIMUM_PASSING_FIXTURE"


def require_variant_authorization() -> tuple[str, Path]:
    if os.getenv("PDMAL_MODE") != VARIANT_MODE:
        raise SystemExit(f"variant execution prohibited: PDMAL_MODE={VARIANT_MODE} is required")
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("variant execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required")
    if os.getenv("PDMAL_SOLO_P30_VARIANT_AUTHORIZED") != "1":
        raise SystemExit("variant execution prohibited: PDMAL_SOLO_P30_VARIANT_AUTHORIZED=1 is required")
    if os.getenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED") != "1":
        raise SystemExit("variant execution prohibited: PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED=1 is required")
    if os.getenv("PDMAL_PILOT_AUTHORIZED") == "1":
        raise SystemExit("variant execution prohibited: high-assurance authorization must not be asserted")
    if os.getenv("PDMAL_P30_BINDING_ID") != P30_BINDING_ID:
        raise SystemExit(f"variant execution prohibited: PDMAL_P30_BINDING_ID must equal {P30_BINDING_ID}")
    if os.getenv("PDMAL_P30_BINDING_KIND") != VARIANT_BINDING_KIND:
        raise SystemExit(f"variant execution prohibited: PDMAL_P30_BINDING_KIND must equal {VARIANT_BINDING_KIND}")
    if os.getenv("PDMAL_P30_CONFIDENCE") != "0.45":
        raise SystemExit("variant execution prohibited: PDMAL_P30_CONFIDENCE must equal exactly 0.45")
    validate_fixture_contract()
    return _require_blinding_and_archive()


def _task_for(*, topology: str, failure_count: int, condition: str) -> ConsensusTask:
    if condition == "dgaf":
        return P30FixtureConsensusTask(topology=topology, failure_count=failure_count)
    return ConsensusTask(topology=topology, failure_count=failure_count, condition=condition)


def run_variant(output_dir: Path, *, seeds: int, seed_start: int) -> int:
    if seeds != VARIANT_SEEDS:
        raise SystemExit(f"variant execution prohibited: seeds must remain exactly {VARIANT_SEEDS}")
    if seed_start != VARIANT_SEED_START:
        raise SystemExit(f"variant execution prohibited: seed_start must remain exactly {VARIANT_SEED_START}")
    if len(_trial_combinations()) != 180:
        raise SystemExit("variant execution prohibited: canonical matrix must contain exactly 180 cells")

    frozen_sha = require_frozen_commit()
    blinding_key, archive_root = require_variant_authorization()
    os.environ.pop("PDMAL_BLINDING_KEY", None)
    output_dir.mkdir(parents=True, exist_ok=True)
    environment_fingerprint = _environment_fingerprint()

    for seed_idx in range(seeds):
        seed = seed_start + seed_idx
        seed_started = monotonic()
        streams = make_streams(seed)
        records: list[dict] = []
        combinations = blinded_trial_schedule(seed=seed, key=blinding_key)
        for trial_idx, (topology, condition, failure_count) in enumerate(combinations):
            task = _task_for(topology=topology, failure_count=failure_count, condition=condition)
            try:
                result = task.run_detailed(seed=seed, attempt=1)
                status = result.attempt_status
            except Exception:
                result = None
                status = AttemptStatus.FAILURE
            final_values = [float(v) for v in result.final_values] if result else []
            execution_success = status is AttemptStatus.SUCCESS
            recovered = failure_count > 0 and execution_success
            record = {
                "experiment_id": VARIANT_EXPERIMENT_ID,
                "protocol_version": PROTOCOL_VERSION,
                "experiment_commit_sha": frozen_sha,
                "seed_id": seed,
                "blinded_condition_id": blind_condition(condition, blinding_key),
                "trial_id": trial_idx,
                "topology": topology,
                "failure_count": failure_count,
                "primary_outcome": float(result.final_std) if result else 0.0,
                "secondary_outcomes": {"final_mean": float(np.mean(final_values)) if final_values else 0.0},
                "failure": failure_count > 0,
                "recovery": recovered,
                "ffcr_success": bool(result.consensus_success and execution_success) if result else False,
                "status": "RECOVERED" if recovered else ("SUCCESS" if execution_success else "UNRECOVERED_FAILURE"),
                "excluded": False,
                "exclusion_reason": None,
                "environment_fingerprint": environment_fingerprint,
            }
            record["artifact_sha256"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
            records.append(record)

        elapsed = monotonic() - seed_started
        if elapsed > SEED_RUNTIME_CEILING_SECONDS:
            raise SystemExit(f"variant execution prohibited: seed {seed} exceeded runtime ceiling ({elapsed:.3f}s)")
        document = {
            "schema_version": ARTIFACT_SCHEMA_VERSION,
            "artifact_version": f"solo-p30-variant-seed-{seed}",
            "protocol_status": "FROZEN",
            "empirical_data_collection": True,
            "frozen_commit_sha": frozen_sha,
            "seed_id": seed,
            "runtime_seconds": elapsed,
            "records": records,
        }
        path = output_dir / f"solo_p30_variant_seed_{seed}.json"
        _write_and_validate_artifact(path, document, expected_seed=seed)
        _retain(path, archive_root, frozen_sha, kind="solo_p30_variant_seed")
        _retain(path.with_suffix(path.suffix + ".sha256"), archive_root, frozen_sha, kind="solo_p30_variant_seed_sidecar")

    summary = {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_version": "solo_p30_variant_summary",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "validation_track": "SOLO_DEVELOPER_VARIANT",
        "independent_verification_status": "NOT_ESTABLISHED_BY_RUNNER",
        "frozen_commit_sha": frozen_sha,
        "experiment_id": VARIANT_EXPERIMENT_ID,
        "variant_scope": VARIANT_SCOPE,
        "p30_binding_id": P30_BINDING_ID,
        "p30_binding_kind": VARIANT_BINDING_KIND,
        "p30_fixture_confidence": P30_FIXTURE_CONFIDENCE,
        "p30_fixture_is_real_confidence": False,
        "canonical_dgaf_efficacy_claim_allowed": False,
        "seed_start": seed_start,
        "total_seeds": seeds,
        "trials_per_seed": 180,
        "total_trials": seeds * 180,
        "environment_fingerprint": environment_fingerprint,
    }
    summary_path = output_dir / "solo_p30_variant_summary.json"
    summary_path.write_bytes(canonical_json_bytes(summary))
    _write_sidecar(summary_path)
    _retain(summary_path, archive_root, frozen_sha, kind="solo_p30_variant_summary")
    _retain(summary_path.with_suffix(summary_path.suffix + ".sha256"), archive_root, frozen_sha, kind="solo_p30_variant_summary_sidecar")
    print(f"SOLO_P30_VARIANT_COMPLETE: {seeds} seeds; {seeds * 180} observations; scope={VARIANT_SCOPE}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=VARIANT_SEEDS)
    parser.add_argument("--seed-start", type=int, default=VARIANT_SEED_START)
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts"))
    args = parser.parse_args(argv)
    return run_variant(args.output_dir, seeds=args.seeds, seed_start=args.seed_start)


if __name__ == "__main__":
    raise SystemExit(main())
