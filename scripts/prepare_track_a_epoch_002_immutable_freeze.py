#!/usr/bin/env python3
"""Prepare or validate the non-authorizing Track A Epoch 002 immutable freeze.

The freeze binds an already-validated precollection candidate and its protected
source blobs. This helper never creates custody material, authorizes collection,
unblinds data, runs empirical work, or increments scientific N.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json"
PREFLIGHT_HELPER_PATH = ROOT / "scripts/prepare_track_a_epoch_002_precollection_preflight.py"
PREFLIGHT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json"
FREEZE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json"
CLOSURE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json"
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"
PREFLIGHT_PATH = ROOT / PREFLIGHT_REL
FREEZE_PATH = ROOT / FREEZE_REL

PROTECTED_SOURCE_PATHS = (
    "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json",
    "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json",
    "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json",
    "experiments/pdmal_pilot/track_a_epoch_002_analysis.py",
    "experiments/pdmal_pilot/requirements-full-lock.txt",
    "experiments/pdmal_pilot/task_engine.py",
    "experiments/pdmal_pilot/harness_contract.py",
    "experiments/pdmal_pilot/topology_utils.py",
    "experiments/pdmal_pilot/run_track_a_epoch_002.py",
    "docs/experiment/TRACK_A_SUCCESSOR_SOLO_CUSTODY_CONTRACT.md",
    "scripts/validate_track_a_successor_solo_custody_receipt.py",
    "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json",
    "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem",
)

DOWNSTREAM_REL = (CLOSURE_REL, VERIFICATION_REL, AUTH_REL)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_FREEZE_FAIL: {message}")


def load_preflight_helper() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_preflight_helper", PREFLIGHT_HELPER_PATH)
    if spec is None or spec.loader is None:
        fail("preflight helper cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


preflight = load_preflight_helper()


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git {' '.join(args)} failed ({exc.returncode})")


def git_path_exists(path: str, revision: str = "HEAD") -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def git_blob(path: str, revision: str) -> str:
    return git("rev-parse", f"{revision}:{path}").lower()


def git_history(path: str, revision: str = "HEAD") -> tuple[str, ...]:
    output = git("log", "--format=%H", revision, "--", path).lower()
    return tuple(line for line in output.splitlines() if line)


def is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def validate_non_authorizing_contract() -> dict[str, Any]:
    contract = load_object(CONTRACT_PATH, "runner contract")
    preflight.validate_contract_boundary(contract)
    if contract.get("track_a_freeze") != "NOT_ESTABLISHED":
        fail("runner contract already claims freeze")
    if contract.get("successor_collection") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes collection")
    if contract.get("primary_analysis") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes primary analysis")
    if contract.get("scientific_n_increment") != 0:
        fail("runner contract increments scientific N")
    return contract


def reject_downstream_gates() -> None:
    present = [path for path in DOWNSTREAM_REL if git_path_exists(path) or (ROOT / path).exists()]
    if present:
        fail(f"downstream successor gates must remain absent: {present}")


def protected_source_blobs_at(revision: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in PROTECTED_SOURCE_PATHS:
        if not git_path_exists(path, revision):
            fail(f"protected source absent at candidate: {path}")
        result[path] = git_blob(path, revision)
    return result


def require_sources_unchanged(candidate_sha: str, expected: dict[str, str]) -> None:
    for path, candidate_blob in expected.items():
        if not git_path_exists(path, "HEAD"):
            fail(f"protected source absent at HEAD: {path}")
        current_blob = git_blob(path, "HEAD")
        if current_blob != candidate_blob:
            fail(f"protected source drift {path}: current={current_blob} candidate={candidate_blob}")
    if not is_ancestor(candidate_sha, git("rev-parse", "HEAD").lower()):
        fail("candidate is not an ancestor of HEAD")


def expected_record(
    *,
    protocol_id: str,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    protected_source_blobs: dict[str, str],
) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST",
        "schema_version": 1,
        "protocol_id": protocol_id,
        "frozen_candidate_sha": candidate_sha,
        "frozen_candidate_tree_sha": candidate_tree_sha,
        "preflight_blob_sha": preflight_blob_sha,
        "protected_source_blobs": protected_source_blobs,
        "freeze_status": "ESTABLISHED",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_record(record: dict[str, Any], expected: dict[str, Any]) -> None:
    if record != expected:
        missing = sorted(set(expected) - set(record))
        extra = sorted(set(record) - set(expected))
        mismatched = sorted(key for key in set(expected) & set(record) if record[key] != expected[key])
        fail(f"freeze record mismatch missing={missing} extra={extra} mismatched={mismatched}")


def require_valid_preflight() -> tuple[dict[str, Any], str, str, str]:
    if not PREFLIGHT_PATH.is_file() or not git_path_exists(PREFLIGHT_REL):
        fail("canonical preflight record is absent")

    record = load_object(PREFLIGHT_PATH, "preflight record")
    candidate_sha = str(record.get("candidate_sha", "")).lower()
    candidate_tree = str(record.get("candidate_tree_sha", "")).lower()
    if not preflight.HEX40.fullmatch(candidate_sha) or not preflight.HEX40.fullmatch(candidate_tree):
        fail("preflight candidate identity is malformed")

    expected_preflight = preflight.expected_record_for_candidate(candidate_sha)
    preflight.validate_record(record, expected_preflight)

    actual_tree = git("rev-parse", f"{candidate_sha}^{{tree}}").lower()
    if actual_tree != candidate_tree:
        fail(f"candidate tree mismatch {actual_tree} != {candidate_tree}")

    history = git_history(PREFLIGHT_REL)
    if len(history) != 1:
        fail(f"preflight must have exactly one immutable history commit; history={list(history)}")
    preflight_commit = history[0]
    if preflight_commit == candidate_sha or not is_ancestor(candidate_sha, preflight_commit):
        fail("preflight must be introduced strictly after the frozen candidate")
    if not is_ancestor(preflight_commit, git("rev-parse", "HEAD").lower()):
        fail("preflight introduction commit is not in HEAD ancestry")

    return record, candidate_sha, candidate_tree, git_blob(PREFLIGHT_REL, "HEAD")


def prepare() -> dict[str, Any]:
    contract = validate_non_authorizing_contract()
    reject_downstream_gates()
    if FREEZE_PATH.exists() or git_path_exists(FREEZE_REL):
        fail("freeze manifest already exists; refusing to overwrite")

    _, candidate_sha, candidate_tree, preflight_blob = require_valid_preflight()
    protected = protected_source_blobs_at(candidate_sha)
    require_sources_unchanged(candidate_sha, protected)
    return expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        protected_source_blobs=protected,
    )


def write_freeze() -> None:
    record = prepare()
    FREEZE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREEZE_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE={FREEZE_REL}")
    print(f"FROZEN_CANDIDATE_SHA={record['frozen_candidate_sha']}")
    print("TRACK_A_EPOCH_002_FREEZE_RECORD=PREPARED_NOT_ACCEPTED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_freeze(expected_base_sha: str | None) -> None:
    contract = validate_non_authorizing_contract()
    reject_downstream_gates()
    if not FREEZE_PATH.is_file() or not git_path_exists(FREEZE_REL):
        fail("freeze manifest absent")

    _, candidate_sha, candidate_tree, preflight_blob = require_valid_preflight()
    protected = protected_source_blobs_at(candidate_sha)
    require_sources_unchanged(candidate_sha, protected)
    expected = expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        protected_source_blobs=protected,
    )
    validate_record(load_object(FREEZE_PATH, "freeze manifest"), expected)

    history = git_history(FREEZE_REL)
    if len(history) != 1:
        fail(f"freeze path must have exactly one immutable history commit; history={list(history)}")

    if expected_base_sha is not None:
        base = expected_base_sha.lower()
        if not preflight.HEX40.fullmatch(base):
            fail("malformed expected base SHA")
        if git_path_exists(FREEZE_REL, base):
            fail("freeze manifest already existed at expected base")
        if not git_path_exists(PREFLIGHT_REL, base):
            fail("preflight must already exist at expected base")
        changed = tuple(line for line in git("diff", "--name-only", f"{base}...HEAD").splitlines() if line)
        if changed != (FREEZE_REL,):
            fail(f"freeze PR must change only {FREEZE_REL}; changed={list(changed)}")

    print("TRACK_A_EPOCH_002_IMMUTABLE_FREEZE=VALIDATED_NONAUTHORIZING")
    print(f"FROZEN_CANDIDATE_SHA={candidate_sha}")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("HIGH_ASSURANCE_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_boundary() -> None:
    validate_non_authorizing_contract()
    reject_downstream_gates()
    if FREEZE_PATH.exists() or git_path_exists(FREEZE_REL):
        fail("boundary validation requires freeze manifest absent")

    if PREFLIGHT_PATH.exists() or git_path_exists(PREFLIGHT_REL):
        require_valid_preflight()

    print("TRACK_A_EPOCH_002_FREEZE_TOOLING=PASS_FREEZE_ABSENT")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="prepare the freeze record after valid preflight")
    mode.add_argument("--validate", action="store_true", help="validate an existing freeze record")
    mode.add_argument("--expect-absent", action="store_true", help="prove freeze and downstream gates remain absent")
    parser.add_argument(
        "--expected-base-sha",
        default=None,
        help="for --validate, require a freeze-only delta from this exact PR base",
    )
    args = parser.parse_args(argv)

    if args.expected_base_sha is not None and not args.validate:
        fail("--expected-base-sha is valid only with --validate")
    if args.write:
        write_freeze()
    elif args.validate:
        validate_freeze(args.expected_base_sha)
    else:
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
