#!/usr/bin/env python3
"""Prepare or validate non-authorizing Track A Epoch 002 verification classification."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
CLOSURE_HELPER_PATH = ROOT / "scripts/prepare_track_a_epoch_002_final_closure.py"
CLOSURE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json"
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"
CLOSURE_PATH = ROOT / CLOSURE_REL
VERIFICATION_PATH = ROOT / VERIFICATION_REL
AUTH_PATH = ROOT / AUTH_REL


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_VERIFICATION_FAIL: {message}")


def load_closure_helper() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_closure_helper", CLOSURE_HELPER_PATH)
    if spec is None or spec.loader is None:
        fail("closure helper cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


closure = load_closure_helper()


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
    contract = closure.validate_contract()
    if contract.get("successor_collection") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes collection")
    if contract.get("primary_analysis") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes primary analysis")
    if contract.get("scientific_n_increment") != 0:
        fail("runner contract increments scientific N")
    return contract


def reject_authorization() -> None:
    if AUTH_PATH.exists() or git_path_exists(AUTH_REL):
        fail("collection authorization must remain absent during verification classification")


def expected_record(*, protocol_id: str, candidate_sha: str, closure_blob_sha: str) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION",
        "schema_version": 1,
        "protocol_id": protocol_id,
        "frozen_candidate_sha": candidate_sha,
        "closure_packet_blob_sha": closure_blob_sha,
        "verification_status": "PASS",
        "verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        "independent_verification": False,
        "same_system_custody": True,
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
        fail(f"verification record mismatch missing={missing} extra={extra} mismatched={mismatched}")
    if record["verification_class"] != "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT":
        fail("verification class exceeds supported evidence")
    if record["independent_verification"] is not False:
        fail("same-system verification cannot claim independence")
    if record["same_system_custody"] is not True:
        fail("same-system custody must remain explicit")


def require_valid_closure() -> tuple[str, str]:
    if not CLOSURE_PATH.is_file() or not git_path_exists(CLOSURE_REL):
        fail("canonical final-closure packet is absent")

    contract = validate_contract()
    candidate_sha, freeze_blob_sha = closure.require_valid_freeze()
    record = load_object(CLOSURE_PATH, "final-closure packet")
    expected_closure = closure.expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        freeze_blob_sha=freeze_blob_sha,
    )
    closure.validate_record(record, expected_closure)

    history = git_history(CLOSURE_REL)
    if len(history) != 1:
        fail(f"closure packet must have exactly one immutable history commit; history={list(history)}")
    closure_commit = history[0]
    freeze_history = git_history(closure.FREEZE_REL)
    if len(freeze_history) != 1:
        fail("immutable freeze history is not singular")
    freeze_commit = freeze_history[0]
    if freeze_commit == closure_commit or not is_ancestor(freeze_commit, closure_commit):
        fail("final closure must be introduced strictly after immutable freeze")
    if not is_ancestor(closure_commit, git("rev-parse", "HEAD").lower()):
        fail("closure introduction commit is not in HEAD ancestry")

    return candidate_sha, git_blob(CLOSURE_REL)


def prepare() -> dict[str, Any]:
    contract = validate_contract()
    reject_authorization()
    if VERIFICATION_PATH.exists() or git_path_exists(VERIFICATION_REL):
        fail("verification classification already exists; refusing to overwrite")
    candidate_sha, closure_blob_sha = require_valid_closure()
    return expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        closure_blob_sha=closure_blob_sha,
    )


def write_verification() -> None:
    record = prepare()
    VERIFICATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERIFICATION_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE={VERIFICATION_REL}")
    print("TRACK_A_EPOCH_002_VERIFICATION=PREPARED_NOT_ACCEPTED")
    print("VERIFICATION_CLASS=DEVELOPER_SELF_ATTESTED_NONINDEPENDENT")
    print("INDEPENDENT_VERIFICATION=FALSE")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_verification(expected_base_sha: str | None) -> None:
    contract = validate_contract()
    reject_authorization()
    if not VERIFICATION_PATH.is_file() or not git_path_exists(VERIFICATION_REL):
        fail("verification classification absent")

    candidate_sha, closure_blob_sha = require_valid_closure()
    expected = expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        closure_blob_sha=closure_blob_sha,
    )
    validate_record(load_object(VERIFICATION_PATH, "verification classification"), expected)

    history = git_history(VERIFICATION_REL)
    if len(history) != 1:
        fail(f"verification path must have exactly one immutable history commit; history={list(history)}")
    closure_commit = git_history(CLOSURE_REL)[0]
    verification_commit = history[0]
    if closure_commit == verification_commit or not is_ancestor(closure_commit, verification_commit):
        fail("verification must be introduced strictly after final closure")

    if expected_base_sha is not None:
        base = expected_base_sha.lower()
        if not closure.closure.freeze.preflight.HEX40.fullmatch(base):
            fail("malformed expected base SHA")
        if git_path_exists(VERIFICATION_REL, base):
            fail("verification classification already existed at expected base")
        if not git_path_exists(CLOSURE_REL, base):
            fail("final closure must already exist at expected base")
        changed = tuple(line for line in git("diff", "--name-only", f"{base}...HEAD").splitlines() if line)
        if changed != (VERIFICATION_REL,):
            fail(f"verification PR must change only {VERIFICATION_REL}; changed={list(changed)}")

    print("TRACK_A_EPOCH_002_VERIFICATION=VALIDATED_NONAUTHORIZING")
    print("VERIFICATION_CLASS=DEVELOPER_SELF_ATTESTED_NONINDEPENDENT")
    print("INDEPENDENT_VERIFICATION=FALSE")
    print("SAME_SYSTEM_CUSTODY=TRUE")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("HIGH_ASSURANCE_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_boundary() -> None:
    validate_contract()
    reject_authorization()
    if VERIFICATION_PATH.exists() or git_path_exists(VERIFICATION_REL):
        fail("boundary validation requires verification classification absent")
    if CLOSURE_PATH.exists() or git_path_exists(CLOSURE_REL):
        require_valid_closure()
    print("TRACK_A_EPOCH_002_VERIFICATION_TOOLING=PASS_VERIFICATION_ABSENT")
    print("INDEPENDENT_VERIFICATION=FALSE")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="prepare verification only after accepted closure")
    mode.add_argument("--validate", action="store_true", help="validate an existing verification classification")
    mode.add_argument("--expect-absent", action="store_true", help="prove verification/authorization remain absent")
    parser.add_argument("--expected-base-sha", default=None)
    args = parser.parse_args(argv)

    if args.expected_base_sha is not None and not args.validate:
        fail("--expected-base-sha is valid only with --validate")
    if args.write:
        write_verification()
    elif args.validate:
        validate_verification(args.expected_base_sha)
    else:
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
