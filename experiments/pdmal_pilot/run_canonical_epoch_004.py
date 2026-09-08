#!/usr/bin/env python3
"""Fail-closed Solo runner implementation for canonical DGAF Epoch 004.

Code presence is not execution authorization. Empirical collection requires a future
one-file run-request commit whose request binds the known runner-parent SHA; the
actual frozen run SHA is the one-file authorization commit itself. Protected
blinding and retention inputs are also required. PR validation must never satisfy
those predicates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from time import monotonic

import numpy as np

from canonical_profile_tgl_diagnostic import (
    PROFILE_ID,
    PROFILE_SOURCE_SHA,
    QUALIFICATION_SHA256,
    CanonicalQualifiedTGLAdapter,
    load_and_validate_qualification,
)
from dgaf_tgl_adapter import ConsensusState
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

PROTOCOL_VERSION = "0.7.6"
EPOCH_ID = "PDMAL-SOLO-CANONICAL-EPOCH-004"
MODE = "solo_canonical_epoch_004"
SEED_START = 20261001
SEEDS = 50
OBSERVATIONS = 9000
RUN_REQUEST_PATH = Path("docs/experiment/solo_runs/CANONICAL_EPOCH_004_RUN_REQUEST.json")
PREREG_MERGE_SHA = "ae854edf565c903bf799f243841799819333d920"
PREFLIGHT_MERGE_SHA = "15c6621ccab0c28e2938c302d23975ba037bd3ee"
COLLECTION_CONTRACT_MERGE_SHA = "db8595272a9782786e35b94eaacced6e73d9b649"
ANALYSIS_BLOB_SHA = "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
ANALYSIS_CONFIG_SHA256 = "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _git_blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], cwd=_repo_root(), text=True).strip()


def _parent_sha() -> str:
    try:
        parent = subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=_repo_root(), text=True).strip().lower()
    except subprocess.CalledProcessError as exc:
        raise SystemExit("Epoch 004 execution prohibited: unable to resolve authorization parent SHA") from exc
    if len(parent) != 40 or any(c not in "0123456789abcdef" for c in parent):
        raise SystemExit("Epoch 004 execution prohibited: invalid authorization parent SHA")
    return parent


def _load_request(path: Path = RUN_REQUEST_PATH) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Epoch 004 execution prohibited: valid run request absent ({exc})") from exc
    if not isinstance(data, dict):
        raise SystemExit("Epoch 004 execution prohibited: run request must be a JSON object")
    return data


def validate_run_request(data: dict, *, frozen_sha: str, parent_sha: str) -> None:
    if frozen_sha == parent_sha:
        raise SystemExit("Epoch 004 execution prohibited: authorization commit must be distinct from runner parent")
    expected = {
        "record_type": "DGAF_CANONICAL_SOLO_EMPIRICAL_RUN_REQUEST",
        "schema_version": 1,
        "epoch_id": EPOCH_ID,
        "authorized_runner_parent_sha": parent_sha,
        "preregistration_merge_sha": PREREG_MERGE_SHA,
        "treatment_input_preflight_merge_sha": PREFLIGHT_MERGE_SHA,
        "collection_contract_merge_sha": COLLECTION_CONTRACT_MERGE_SHA,
        "seed_start": SEED_START,
        "seeds": SEEDS,
        "expected_observations": OBSERVATIONS,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "validation_track": "SOLO_DEVELOPER",
        "limitations_acknowledged": True,
        "authorize_empirical_collection": True,
        "authorize_unblinding": False,
        "historical_pooling_allowed": False,
    }
    if data != expected:
        missing = sorted(set(expected) - set(data))
        extra = sorted(set(data) - set(expected))
        mismatched = sorted(k for k in set(expected) & set(data) if data[k] != expected[k])
        raise SystemExit(
            "Epoch 004 execution prohibited: run request mismatch "
            f"missing={missing} extra={extra} mismatched={mismatched}"
        )


def require_epoch_authorization() -> tuple[str, Path, str]:
    if os.getenv("PDMAL_MODE") != MODE:
        raise SystemExit(f"Epoch 004 execution prohibited: PDMAL_MODE={MODE} is required")
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("Epoch 004 execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required")
    if os.getenv("PDMAL_SOLO_CANONICAL_EPOCH_004_AUTHORIZED") != "1":
        raise SystemExit("Epoch 004 execution prohibited: explicit Solo Epoch 004 authorization env is required")
    if os.getenv("PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED") != "1":
        raise SystemExit("Epoch 004 execution prohibited: Solo limitations acknowledgement is required")
    if os.getenv("PDMAL_PILOT_AUTHORIZED") == "1":
        raise SystemExit("Epoch 004 execution prohibited: High-Assurance authorization must not be asserted")
    if os.getenv("PDMAL_UNBLINDING_AUTHORIZED") == "1":
        raise SystemExit("Epoch 004 collection prohibited: unblinding must remain unauthorized during collection")

    frozen_sha = require_frozen_commit()
    parent_sha = _parent_sha()
    request = _load_request()
    validate_run_request(request, frozen_sha=frozen_sha, parent_sha=parent_sha)
    qualification = load_and_validate_qualification()
    if _git_blob("experiments/pdmal_pilot/analysis.py") != ANALYSIS_BLOB_SHA:
        raise SystemExit("Epoch 004 execution prohibited: locked analysis source blob mismatch")
    subprocess.run(
        ["python", "scripts/validate_canonical_epoch_004_treatment_input_preflight.py"],
        cwd=_repo_root(),
        check=True,
    )
    blinding_key, archive_root = _require_blinding_and_archive()
    return blinding_key, archive_root, hashlib.sha256(qualification).hexdigest()


class CanonicalEpoch004Task(ConsensusTask):
    """Canonical DGAF task using external P-30/11Q qualification at step 8."""

    def __init__(self, *, topology: str, failure_count: int, qualification_bytes: bytes) -> None:
        super().__init__(topology=topology, failure_count=failure_count, condition="dgaf")
        self.qualification_bytes = qualification_bytes

    def _dgaf_update(
        self,
        *,
        seed: int,
        iteration: int,
        values: np.ndarray,
        graph,
        alive: tuple[bool, ...],
        active_neighbors: tuple[tuple[int, ...], ...],
        failure_history: tuple[tuple[int, ...], ...],
        failure_count_current: int,
        failure_count_total: int,
    ):
        adapter = CanonicalQualifiedTGLAdapter(
            session_id=f"epoch004-{self.trial_key(seed, self.topology, self.condition, self.failure_count)}",
            qualification_bytes=self.qualification_bytes,
        )
        state = ConsensusState(
            seed_id=seed,
            iteration=iteration,
            agent_values=tuple(float(x) for x in values),
            alive=alive,
            original_neighbors=tuple(tuple(sorted(graph.neighbors(i))) for i in range(20)),
            active_neighbors=active_neighbors,
            failure_history=failure_history,
            failure_count_current=failure_count_current,
            failure_count_total=failure_count_total,
            current_final_std=float(np.std(values)),
            current_mean=float(np.mean(values)),
            runtime_budget_remaining_ms=int(SEED_RUNTIME_CEILING_SECONDS * 1000),
            protocol_id=EPOCH_ID,
        )
        try:
            result = adapter.run_turn(state)
        except Exception as exc:
            return values, AttemptStatus.FAILURE, f"canonical-epoch004-adapter-error:{type(exc).__name__}: {exc}", None
        trace = result.audit.to_dict()
        trace["decision"] = result.decision
        trace["outcome"] = result.attempt_status.value
        if result.decision == "FAIL_CLOSED" or result.next_values is None:
            return values, AttemptStatus.FAILURE, "canonical-epoch004-fail-closed", trace
        return np.asarray(result.next_values, dtype=float), AttemptStatus.SUCCESS, None, trace


def _task_for(*, topology: str, failure_count: int, condition: str, qualification_bytes: bytes) -> ConsensusTask:
    if condition == "dgaf":
        return CanonicalEpoch004Task(
            topology=topology,
            failure_count=failure_count,
            qualification_bytes=qualification_bytes,
        )
    return ConsensusTask(topology=topology, failure_count=failure_count, condition=condition)


def run_epoch(output_dir: Path, *, seeds: int, seed_start: int) -> int:
    if seeds != SEEDS or seed_start != SEED_START:
        raise SystemExit(f"Epoch 004 execution prohibited: exact seed panel {SEED_START}..{SEED_START + SEEDS - 1} required")
    if len(_trial_combinations()) != 180:
        raise SystemExit("Epoch 004 execution prohibited: canonical matrix must contain exactly 180 cells")

    frozen_sha = require_frozen_commit()
    blinding_key, archive_root, qualification_digest = require_epoch_authorization()
    qualification_bytes = load_and_validate_qualification()
    if qualification_digest != QUALIFICATION_SHA256:
        raise SystemExit("Epoch 004 execution prohibited: qualification digest mismatch")
    os.environ.pop("PDMAL_BLINDING_KEY", None)
    output_dir.mkdir(parents=True, exist_ok=True)
    environment_fingerprint = _environment_fingerprint()

    for seed_idx in range(seeds):
        seed = seed_start + seed_idx
        seed_started = monotonic()
        records: list[dict] = []
        combinations = blinded_trial_schedule(seed=seed, key=blinding_key)
        for trial_idx, (topology, condition, failure_count) in enumerate(combinations):
            task = _task_for(
                topology=topology,
                failure_count=failure_count,
                condition=condition,
                qualification_bytes=qualification_bytes,
            )
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
                "experiment_id": EPOCH_ID,
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
            raise SystemExit(f"Epoch 004 execution prohibited: seed {seed} exceeded runtime ceiling ({elapsed:.3f}s)")
        if len(records) != 180:
            raise SystemExit(f"Epoch 004 execution prohibited: seed {seed} matrix incomplete")
        document = {
            "schema_version": ARTIFACT_SCHEMA_VERSION,
            "artifact_version": f"canonical-epoch-004-seed-{seed}",
            "protocol_status": "FROZEN",
            "empirical_data_collection": True,
            "frozen_commit_sha": frozen_sha,
            "seed_id": seed,
            "runtime_seconds": elapsed,
            "records": records,
        }
        path = output_dir / f"canonical_epoch_004_seed_{seed}.json"
        _write_and_validate_artifact(path, document, expected_seed=seed)
        _retain(path, archive_root, frozen_sha, kind="canonical_epoch_004_seed")
        _retain(path.with_suffix(path.suffix + ".sha256"), archive_root, frozen_sha, kind="canonical_epoch_004_seed_sidecar")

    summary = {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_version": "canonical_epoch_004_summary",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "validation_track": "SOLO_DEVELOPER",
        "independent_verification_status": "NOT_ESTABLISHED_BY_RUNNER",
        "frozen_commit_sha": frozen_sha,
        "experiment_id": EPOCH_ID,
        "profile_id": PROFILE_ID,
        "profile_source_sha": PROFILE_SOURCE_SHA,
        "qualification_sha256": QUALIFICATION_SHA256,
        "qualification_verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        "canonical_p30_binding": "EXTERNAL_P11_11Q_QUALIFICATION_VERIFICATION",
        "seed_start": seed_start,
        "total_seeds": seeds,
        "trials_per_seed": 180,
        "total_trials": seeds * 180,
        "outcomes_inspected_by_collection_workflow": False,
        "unblinding_authorized": False,
        "historical_pooling_allowed": False,
        "environment_fingerprint": environment_fingerprint,
    }
    summary_path = output_dir / "canonical_epoch_004_summary.json"
    summary_path.write_bytes(canonical_json_bytes(summary))
    _write_sidecar(summary_path)
    _retain(summary_path, archive_root, frozen_sha, kind="canonical_epoch_004_summary")
    _retain(summary_path.with_suffix(summary_path.suffix + ".sha256"), archive_root, frozen_sha, kind="canonical_epoch_004_summary_sidecar")
    print(f"CANONICAL_EPOCH_004_COLLECTION_COMPLETE: {seeds} seeds; {seeds * 180} observations")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=SEEDS)
    parser.add_argument("--seed-start", type=int, default=SEED_START)
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts"))
    args = parser.parse_args(argv)
    return run_epoch(args.output_dir, seeds=args.seeds, seed_start=args.seed_start)


if __name__ == "__main__":
    raise SystemExit(main())
