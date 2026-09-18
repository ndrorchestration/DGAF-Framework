#!/usr/bin/env python3
"""Fail-closed local runner for the authorized Track A Epoch 002 primary analysis.

The runner consumes only the retained, content-addressed local materialized input.
It requires an accepted repository PRIMARY_ANALYSIS_AUTHORIZATION_RECORD, verifies
the frozen analysis identities and exact locked environment, runs only the frozen
primary analysis, and writes a local content-addressed result bundle.

It does not merge repository records, establish canonical DGAF efficacy,
independent validation, or High-Assurance authorization.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"
AUTH_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
ANALYSIS_BLOB_SHA = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
ANALYSIS_CONFIG_SHA256 = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
REQUIREMENTS_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"
OUTPUT_NAME = "track_a_epoch_002_locked_primary_analysis_output.json"
OUTPUT_SIDECAR_NAME = OUTPUT_NAME + ".sha256"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_FAIL: {message}")


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_bytes(ref: str, relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{relpath}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"cannot read {ref}:{relpath}: {detail}")
    return completed.stdout


def git_object_exists(spec: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object_bytes(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        fail(f"{label} is invalid JSON: {exc}")
    if not isinstance(parsed, dict):
        fail(f"{label} must be a JSON object")
    return parsed


def load_repo_object(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    try:
        return load_object_bytes(path.read_bytes(), relpath)
    except OSError as exc:
        fail(f"cannot read {relpath}: {exc}")


def outside_repository(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return True
    return False


def require_external_regular_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not outside_repository(resolved):
        fail(f"{label} must remain outside the repository")
    if resolved.is_symlink() or not resolved.is_file():
        fail(f"{label} must be an external regular file")
    return resolved


def require_external_output_dir(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not outside_repository(resolved):
        fail("analysis output directory must remain outside the repository")
    if resolved.exists() and resolved.is_symlink():
        fail("analysis output directory must not be a symlink")
    return resolved


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_frozen_identities(ref: str = "HEAD") -> None:
    expected = {
        ANALYSIS_REL: ANALYSIS_BLOB_SHA,
        REQUIREMENTS_REL: REQUIREMENTS_BLOB_SHA,
    }
    for relpath, expected_blob in expected.items():
        actual = git("rev-parse", f"{ref}:{relpath}")
        if actual != expected_blob:
            fail(f"frozen identity drift at {relpath}: " f"expected {expected_blob}, got {actual}")

    analysis = load_module(
        ROOT / ANALYSIS_REL,
        "track_a_epoch_002_locked_analysis_identity_check",
    )
    if analysis.analysis_config_sha256() != ANALYSIS_CONFIG_SHA256:
        fail("frozen analysis configuration digest drift")


def validate_authorization() -> tuple[str, dict[str, Any]]:
    if not git_object_exists(f"HEAD:{AUTH_REL}"):
        fail("accepted primary-analysis authorization record is absent")
    if git_object_exists(f"HEAD:{RESULT_REL}"):
        fail("locked analysis result record already exists; refusing re-execution")

    auth_history = [line for line in git("log", "--format=%H", "HEAD", "--", AUTH_REL).splitlines() if line]
    if len(auth_history) != 1:
        fail("primary-analysis authorization must have one immutable history event")
    auth_event = auth_history[0]

    lineage = git("rev-list", "--parents", "-n", "1", auth_event).split()
    if len(lineage) != 2 or lineage[0] != auth_event:
        fail("primary-analysis authorization event must have exactly one parent")
    auth_parent = lineage[1]

    changed = [
        line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", auth_event).splitlines() if line
    ]
    if changed != [AUTH_REL]:
        fail("authorization event changed more than the canonical authorization path")
    if git_object_exists(f"{auth_parent}:{AUTH_REL}"):
        fail("authorization record is not creation-only")

    if not git_object_exists(f"{auth_parent}:{RECEIPT_REL}"):
        fail("accepted materialization receipt predecessor is absent")

    receipt_history = [line for line in git("log", "--format=%H", auth_parent, "--", RECEIPT_REL).splitlines() if line]
    if len(receipt_history) != 1:
        fail("materialization receipt must have one immutable history event")
    receipt_event = receipt_history[0]

    receipt_bytes = git_bytes(auth_parent, RECEIPT_REL)
    receipt = load_object_bytes(receipt_bytes, "materialization receipt")
    authorization = load_object_bytes(
        git_bytes(auth_event, AUTH_REL),
        "primary-analysis authorization",
    )

    validator = load_module(
        ROOT / AUTH_VALIDATOR_REL,
        "track_a_epoch_002_authorization_for_execution",
    )
    validator.validate_authorization_object(
        authorization,
        receipt,
        materialization_receipt_commit_sha=receipt_event,
        materialization_receipt_sha256=sha256_bytes(receipt_bytes),
        authorization_parent_sha=auth_parent,
    )
    validator.validate_frozen_analysis_identities(auth_parent)
    validate_frozen_identities("HEAD")
    return auth_event, authorization


def validate_locked_environment() -> dict[str, str]:
    lock = load_repo_object(ANALYSIS_LOCK_REL)
    if lock.get("protocol_id") != PROTOCOL_ID:
        fail("analysis lock protocol identity drift")
    if lock.get("status") != "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL":
        fail("analysis lock status drift")

    environment = lock.get("environment")
    if not isinstance(environment, dict):
        fail("analysis lock environment is malformed")

    expected_python = environment.get("python_version")
    expected_numpy = lock.get("numpy_version")
    if not isinstance(expected_python, str) or not isinstance(expected_numpy, str):
        fail("analysis lock runtime versions are malformed")

    actual_python = platform.python_version()
    actual_numpy = np.__version__
    if actual_python != expected_python:
        fail(f"Python version mismatch: expected {expected_python}, got {actual_python}")
    if actual_numpy != expected_numpy:
        fail(f"NumPy version mismatch: expected {expected_numpy}, got {actual_numpy}")

    return {"python": actual_python, "numpy": actual_numpy}


def validate_materialized_input(path: Path) -> tuple[list[dict[str, Any]], str]:
    source = require_external_regular_file(path, "materialized analysis input")
    payload = source.read_bytes()
    digest = sha256_bytes(payload)

    evidence = load_repo_object(EVIDENCE_REL)
    expected_digest = evidence.get("materialized_input_sha256")
    if digest != expected_digest:
        fail("materialized input digest does not match accepted evidence")

    document = load_object_bytes(payload, "materialized analysis input")
    required = {
        "record_type": "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "paired_seed_units": 50,
        "record_count": 2250,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "primary_analysis_status": "NOT_AUTHORIZED_NOT_RUN",
    }
    for key, expected in required.items():
        if document.get(key) != expected:
            fail(f"materialized analysis input historical state drift: {key}")

    records = document.get("records")
    if not isinstance(records, list) or len(records) != 2250:
        fail("materialized analysis input record matrix is malformed")
    if not all(isinstance(row, dict) for row in records):
        fail("materialized analysis input contains a malformed record")
    return records, digest


def build_output(
    *,
    result: dict[str, Any],
    input_sha256: str,
    authorization_event_sha: str,
    authorization_record_id: str,
    environment: dict[str, str],
) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS_OUTPUT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "authorization_event_commit_sha": authorization_event_sha,
        "authorization_record_id": authorization_record_id,
        "materialized_input_sha256": input_sha256,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "environment": dict(environment),
        "result": result,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }


def execute(input_path: Path, output_dir: Path) -> tuple[Path, str]:
    authorization_event, authorization = validate_authorization()
    environment = validate_locked_environment()
    records, input_sha256 = validate_materialized_input(input_path)

    analysis = load_module(
        ROOT / ANALYSIS_REL,
        "track_a_epoch_002_locked_primary_analysis_execution",
    )
    result = analysis.analyze(records)
    if not isinstance(result, dict):
        fail("locked analysis returned a non-object result")

    output = build_output(
        result=result,
        input_sha256=input_sha256,
        authorization_event_sha=authorization_event,
        authorization_record_id=str(authorization["record_id"]),
        environment=environment,
    )
    payload = canonical_json_bytes(output)
    digest = sha256_bytes(payload)

    destination_dir = require_external_output_dir(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / OUTPUT_NAME
    sidecar = destination_dir / OUTPUT_SIDECAR_NAME
    if destination.exists() or sidecar.exists():
        fail("analysis output already exists; refusing to overwrite")

    destination.write_bytes(payload)
    sidecar.write_text(f"{digest}  {OUTPUT_NAME}\n", encoding="ascii")
    return destination, digest


def preflight() -> None:
    validate_authorization()
    validate_locked_environment()
    validate_frozen_identities("HEAD")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.preflight_only:
        preflight()
        print("TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_PREFLIGHT=PASS")
        print("PRIMARY_ANALYSIS_EXECUTION=NOT_PERFORMED")
        print("SCIENTIFIC_N_INCREMENT=0")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
        return 0

    if args.input is None or args.output_dir is None:
        fail("--input and --output-dir are required unless --preflight-only is used")

    destination, digest = execute(args.input, args.output_dir)
    print("TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS=EXECUTED_LOCAL")
    print(f"LOCKED_ANALYSIS_OUTPUT_PATH={destination}")
    print(f"LOCKED_ANALYSIS_OUTPUT_SHA256={digest}")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
