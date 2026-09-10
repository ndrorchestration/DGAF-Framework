#!/usr/bin/env python3
"""Validate the human-controlled Track A Epoch 002 collection-authorization boundary.

This tool never writes an authorization record and never executes empirical work.
It can prove that authorization is absent now or validate a future human-authored
one-record authorization event against the canonical runner contract.
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
VERIFICATION_HELPER_PATH = ROOT / "scripts/prepare_track_a_epoch_002_verification_classification.py"
RECONCILER_PATH = ROOT / "registry/dgaf_completion_state_reconciler.v0.1.json"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"
AUTH_PATH = ROOT / AUTH_REL
VERIFICATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json"
VERIFICATION_PATH = ROOT / VERIFICATION_REL

CUSTODY_KEYS = (
    "custody_receipt_blob_sha",
    "custody_certificate_blob_sha",
    "custody_encrypted_private_key_sha256",
    "custody_certificate_sha256",
    "custody_certificate_public_key_der_sha256",
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_AUTHORIZATION_FAIL: {message}")


def load_verification_helper() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_verification_helper", VERIFICATION_HELPER_PATH)
    if spec is None or spec.loader is None:
        fail("verification helper cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


verification = load_verification_helper()


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


def find_reconciler_node(value: object, node_id: str) -> dict[str, Any] | None:
    if isinstance(value, dict):
        if value.get("id") == node_id:
            return value
        for child in value.values():
            found = find_reconciler_node(child, node_id)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_reconciler_node(child, node_id)
            if found is not None:
                return found
    return None


def validate_contract() -> dict[str, Any]:
    contract = verification.validate_contract()
    authorization = contract.get("authorization")
    if not isinstance(authorization, dict):
        fail("runner contract authorization object missing")
    required = {
        "one_file_path": AUTH_REL,
        "authorization_head_exactly_one_parent": True,
        "authorization_file_must_be_only_change": True,
        "authorization_must_bind_frozen_candidate_sha_and_tree": True,
        "authorization_must_bind_preflight_freeze_closure_verification_blobs": True,
        "authorization_must_bind_custody_receipt_and_certificate": True,
        "pr_validation_can_authorize": False,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }
    for field, expected in required.items():
        if authorization.get(field) != expected:
            fail(f"runner contract authorization.{field} drift")

    reconciler = load_object(RECONCILER_PATH, "completion-state reconciler")
    node = find_reconciler_node(reconciler, "collection_authorization")
    if node is None:
        fail("completion-state collection_authorization node missing")
    if node.get("action_class") != "human_controlled":
        fail("collection authorization must remain human_controlled")
    return contract


def expected_record(
    contract: dict[str, Any],
    *,
    authorization_parent_sha: str,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    freeze_blob_sha: str,
    closure_blob_sha: str,
    verification_blob_sha: str,
    custody: dict[str, str],
) -> dict[str, Any]:
    bindings = contract["source_bindings"]
    matrix = contract["matrix"]
    seeds = matrix["seeds"]
    if not isinstance(seeds, list) or not seeds:
        fail("runner contract seed panel missing")
    return {
        "record_type": "TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION",
        "schema_version": 1,
        "protocol_id": contract["protocol_id"],
        "epoch_id": contract["epoch_id"],
        "authorization_parent_sha": authorization_parent_sha,
        "frozen_candidate_sha": candidate_sha,
        "frozen_candidate_tree_sha": candidate_tree_sha,
        "preflight_blob_sha": preflight_blob_sha,
        "freeze_manifest_blob_sha": freeze_blob_sha,
        "closure_packet_blob_sha": closure_blob_sha,
        "verification_classification_blob_sha": verification_blob_sha,
        "preregistration_merge_sha": bindings["preregistration_merge_sha"],
        "analysis_lock_merge_sha": bindings["analysis_lock_merge_sha"],
        "analysis_blob_sha": bindings["analysis_blob_sha"],
        "analysis_config_sha256": bindings["analysis_config_sha256"],
        "requirements_lock_blob_sha": bindings["requirements_lock_blob_sha"],
        "algorithm_id": contract["algorithm_id"],
        "seed_start": seeds[0],
        "seed_end": seeds[-1],
        "seed_count": len(seeds),
        "expected_observations": matrix["expected_total_observations"],
        **custody,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "custody_recovery_drill": "PASS",
        "authorize_empirical_collection": True,
        "authorize_unblinding": False,
        "authorize_primary_analysis": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
    }


def validate_record(record: dict[str, Any], expected: dict[str, Any]) -> None:
    if record != expected:
        missing = sorted(set(expected) - set(record))
        extra = sorted(set(record) - set(expected))
        mismatched = sorted(key for key in set(expected) & set(record) if record[key] != expected[key])
        fail(f"authorization record mismatch missing={missing} extra={extra} mismatched={mismatched}")
    if record["authorize_empirical_collection"] is not True:
        fail("authorization record must make the collection decision explicit")
    for field in (
        "authorize_unblinding",
        "authorize_primary_analysis",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
        "high_assurance_authorized",
    ):
        if record[field] is not False:
            fail(f"authorization record must keep {field}=false")
    if record["custody_class"] != "SAME_SYSTEM_NONINDEPENDENT":
        fail("authorization cannot promote custody independence")
    if record["custody_recovery_drill"] != "PASS":
        fail("authorization requires accepted recovery drill PASS")


def require_valid_verification() -> tuple[str, str, str, str, str, str, dict[str, str]]:
    if not VERIFICATION_PATH.is_file() or not git_path_exists(VERIFICATION_REL):
        fail("canonical verification classification is absent")

    contract = validate_contract()
    candidate_sha, closure_blob_sha = verification.require_valid_closure()
    record = load_object(VERIFICATION_PATH, "verification classification")
    expected_verification = verification.expected_record(
        protocol_id=str(contract["protocol_id"]),
        candidate_sha=candidate_sha,
        closure_blob_sha=closure_blob_sha,
    )
    verification.validate_record(record, expected_verification)

    verification_history = git_history(VERIFICATION_REL)
    if len(verification_history) != 1:
        fail(f"verification must have exactly one immutable history commit; history={list(verification_history)}")
    verification_commit = verification_history[0]
    closure_history = git_history(verification.CLOSURE_REL)
    if len(closure_history) != 1:
        fail("final-closure history is not singular")
    closure_commit = closure_history[0]
    if closure_commit == verification_commit or not is_ancestor(closure_commit, verification_commit):
        fail("verification must be introduced strictly after final closure")

    preflight_record, preflight_candidate, candidate_tree_sha, preflight_blob_sha = (
        verification.closure.freeze.require_valid_preflight()
    )
    if preflight_candidate != candidate_sha:
        fail("preflight and verification candidate identities differ")
    freeze_candidate, freeze_blob_sha = verification.closure.require_valid_freeze()
    if freeze_candidate != candidate_sha:
        fail("freeze and verification candidate identities differ")

    custody: dict[str, str] = {}
    for key in CUSTODY_KEYS:
        value = preflight_record.get(key)
        if not isinstance(value, str) or not value:
            fail(f"preflight missing custody binding {key}")
        custody[key] = value

    return (
        candidate_sha,
        candidate_tree_sha,
        preflight_blob_sha,
        freeze_blob_sha,
        closure_blob_sha,
        git_blob(VERIFICATION_REL),
        custody,
    )


def authorization_parent(expected_base_sha: str | None) -> str:
    head = git("rev-parse", "HEAD").lower()
    parents = git("rev-list", "--parents", "-n", "1", head).lower().split()[1:]
    if len(parents) != 1:
        fail("authorization head must have exactly one parent")
    parent = parents[0]
    if expected_base_sha is None:
        return parent
    base = expected_base_sha.lower()
    if not verification.closure.freeze.preflight.HEX40.fullmatch(base):
        fail("malformed expected base SHA")
    if parent != base:
        fail(f"authorization head parent {parent} does not equal expected base {base}")
    return base


def validate_authorization(expected_base_sha: str | None) -> None:
    contract = validate_contract()
    if not AUTH_PATH.is_file() or not git_path_exists(AUTH_REL):
        fail("collection authorization record is absent")

    parent = authorization_parent(expected_base_sha)
    if git_path_exists(AUTH_REL, parent):
        fail("authorization record already existed at authorization parent")
    if not git_path_exists(VERIFICATION_REL, parent):
        fail("verification classification must already exist at authorization parent")

    (
        candidate_sha,
        candidate_tree_sha,
        preflight_blob_sha,
        freeze_blob_sha,
        closure_blob_sha,
        verification_blob_sha,
        custody,
    ) = require_valid_verification()

    verification_commit = git_history(VERIFICATION_REL)[0]
    if verification_commit == parent or not is_ancestor(verification_commit, parent):
        fail("accepted verification must strictly predate authorization parent")

    head = git("rev-parse", "HEAD").lower()
    changed = tuple(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if line)
    if changed != (AUTH_REL,):
        fail(f"authorization head must change only {AUTH_REL}; changed={list(changed)}")
    history = git_history(AUTH_REL)
    if history != (head,):
        fail(f"authorization path must be introduced exactly at HEAD; history={list(history)}")

    expected = expected_record(
        contract,
        authorization_parent_sha=parent,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree_sha,
        preflight_blob_sha=preflight_blob_sha,
        freeze_blob_sha=freeze_blob_sha,
        closure_blob_sha=closure_blob_sha,
        verification_blob_sha=verification_blob_sha,
        custody=custody,
    )
    validate_record(load_object(AUTH_PATH, "collection authorization"), expected)

    print("TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION=VALIDATED_HUMAN_CONTROLLED_EVENT")
    print("PR_VALIDATION_CAN_AUTHORIZE=FALSE")
    print("AUTHORIZE_EMPIRICAL_COLLECTION=TRUE_IN_PROPOSED_RECORD")
    print("EMPIRICAL_EXECUTION_PERFORMED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("HIGH_ASSURANCE_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_boundary() -> None:
    validate_contract()
    if AUTH_PATH.exists() or git_path_exists(AUTH_REL):
        fail("boundary validation requires collection authorization absent")
    print("TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION_TOOLING=PASS_AUTHORIZATION_ABSENT")
    print("ACTION_CLASS=HUMAN_CONTROLLED")
    print("PR_VALIDATION_CAN_AUTHORIZE=FALSE")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("EMPIRICAL_EXECUTION_PERFORMED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true", help="validate a human-authored authorization event")
    mode.add_argument("--expect-absent", action="store_true", help="prove authorization remains absent")
    parser.add_argument("--expected-base-sha", default=None)
    args = parser.parse_args(argv)

    if args.expected_base_sha is not None and not args.validate:
        fail("--expected-base-sha is valid only with --validate")
    if args.validate:
        validate_authorization(args.expected_base_sha)
    else:
        validate_boundary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
