#!/usr/bin/env python3
"""Prepare or validate the non-authorizing Track A Epoch 002 final closure."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
FREEZE_HELPER_PATH = ROOT / "scripts/prepare_track_a_epoch_002_immutable_freeze.py"
CONTRACT_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json"
FREEZE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json"
CLOSURE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json"
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"
FREEZE_PATH = ROOT / FREEZE_REL
CLOSURE_PATH = ROOT / CLOSURE_REL
DOWNSTREAM_REL = (VERIFICATION_REL, AUTH_REL)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_CLOSURE_FAIL: {message}")


def load_freeze_helper() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_freeze_helper", FREEZE_HELPER_PATH)
    if spec is None or spec.loader is None:
        fail("freeze helper cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


freeze = load_freeze_helper()


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


def git_blob(path: str, revision: str = "HEAD") -> str:
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


def validate_contract() -> dict[str, Any]:
    contract = freeze.validate_non_authorizing_contract()
    if contract.get("track_a_freeze") != "NOT_ESTABLISHED":
        fail("runner contract must remain pre-freeze until evidence establishes otherwise")
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


def expected_record(*, protocol_id: str, candidate_sha: str, freeze_blob_sha: str) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET",
        "schema_version": 1,
        "protocol_id": protocol_id,
        "frozen_candidate_sha": candidate_sha,
        "freeze_manifest_blob_sha": freeze_blob_sha,
        "open_blockers": [],
        "closure_status": "CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW",
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
        fail(f"closure record mismatch missing={missing} extra={extra} mismatched={mismatched}")


def require_valid_freeze() -> tuple[str, str]:
    if not FREEZE_PATH.is_file() or not git_path_exists(FREEZE_REL):
        fail("canonical immutable-freeze manifest is absent")

    contract = validate_contract()
    freeze_record = load_object(FREEZE_PATH, "freeze manifest")
    candidate_sha = str(freeze_record.get("frozen_candidate_sha", "")).lower()
    candidate_tree = str(freeze_record.get("frozen_candidate_tree_sha", "")).lower()
    if not freeze.preflight.HEX40.fullmatch(candidate_sha) or not freeze.preflight.HEX40.fullmatch(candidate_tree):
        fail("freeze candidate identity is malformed")

    _, preflight_candidate, preflight_tree, preflight_blob = freeze.require_valid_preflight()
    if (candidate_sha, candidate_tree) != (preflight_candidate, preflight_tree):
        fail("freeze candidate does not match validated preflight candidate")

    protected = freeze.protected_source_blobs_at(candidate_sha)
    freeze.require_sources_unchanged(candidate_sha, protected)
    expected_freeze = freeze.expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        protected_source_blobs=protected,
    )
    freeze.validate_record(freeze_record, expected_freeze)

    history = git_history(FREEZE_REL)
    if len(history) != 1:
        fail(f"freeze manifest must have exactly one immutable history commit; history={list(history)}")
    freeze_commit = history[0]
    if freeze_commit == candidate_sha or not is_ancestor(candidate_sha, freeze_commit):
        fail("freeze must be introduced strictly after the frozen candidate")
    if not is_ancestor(freeze_commit, git("rev-parse", "HEAD").lower()):
        fail("freeze introduction commit is not in HEAD ancestry")

    return candidate_sha, git_blob(FREEZE_REL)


def prepare() -> dict[str, Any]:
    contract = validate_contract()
    reject_downstream_gates()
    if CLOSURE_PATH.exists() or git_path_exists(CLOSURE_REL):
        fail("closure packet already exists; refusing to overwrite")
    candidate_sha, freeze_blob_sha = require_valid_freeze()
    return expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        freeze_blob_sha=freeze_blob_sha,
    )


def write_closure() -> None:
    record = prepare()
    CLOSURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLOSURE_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE={CLOSURE_REL}")
    print("TRACK_A_EPOCH_002_FINAL_CLOSURE=PREPARED_NOT_ACCEPTED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_closure(expected_base_sha: str | None) -> None:
    contract = validate_contract()
    reject_downstream_gates()
    if not CLOSURE_PATH.is_file() or not git_path_exists(CLOSURE_REL):
        fail("closure packet absent")

    candidate_sha, freeze_blob_sha = require_valid_freeze()
    expected = expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        freeze_blob_sha=freeze_blob_sha,
    )
    validate_record(load_object(CLOSURE_PATH, "closure packet"), expected)

    history = git_history(CLOSURE_REL)
    if len(history) != 1:
        fail(f"closure packet must have exactly one immutable history commit; history={list(history)}")

    freeze_commit = git_history(FREEZE_REL)[0]
    closure_commit = history[0]
    if freeze_commit == closure_commit or not is_ancestor(freeze_commit, closure_commit):
        fail("closure must be introduced strictly after immutable freeze")

    if expected_base_sha is not None:
        base = expected_base_sha.lower()
        if not freeze.preflight.HEX40.fullmatch(base):
            fail("malformed expected base SHA")
        if git_path_exists(CLOSURE_REL, base):
            fail("closure packet already existed at expected base")
        if not git_path_exists(FREEZE_REL, base):
            fail("immutable freeze must already exist at expected base")
        changed = tuple(line for line in git("diff", "--name-only", f"{base}...HEAD").splitlines() if line)
        if changed != (CLOSURE_REL,):
            fail(f"closure PR must change only {CLOSURE_REL}; changed={list(changed)}")

    print("TRACK_A_EPOCH_002_FINAL_CLOSURE=VALIDATED_NONAUTHORIZING")
    print(f"FROZEN_CANDIDATE_SHA={candidate_sha}")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("HIGH_ASSURANCE_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_boundary() -> None:
    validate_contract()
    reject_downstream_gates()
    if CLOSURE_PATH.exists() or git_path_exists(CLOSURE_REL):
        fail("boundary validation requires closure packet absent")
    if FREEZE_PATH.exists() or git_path_exists(FREEZE_REL):
        require_valid_freeze()
    print("TRACK_A_EPOCH_002_FINAL_CLOSURE_TOOLING=PASS_CLOSURE_ABSENT")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="prepare closure only after an accepted freeze")
    mode.add_argument("--validate", action="store_true", help="validate an existing closure packet")
    mode.add_argument("--expect-absent", action="store_true", help="prove closure/downstream gates remain absent")
    parser.add_argument("--expected-base-sha", default=None)
    args = parser.parse_args(argv)

    if args.expected_base_sha is not None and not args.validate:
        fail("--expected-base-sha is valid only with --validate")
    if args.write:
        write_closure()
    elif args.validate:
        validate_closure(args.expected_base_sha)
    else:
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
