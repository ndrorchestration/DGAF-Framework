#!/usr/bin/env python3
"""Fail-closed Track A Epoch 002 primary-analysis authorization validator.

This module installs prospective authorization tooling only. It does not create an
authorization record, perform materialization, execute analysis, inspect outcomes,
or change scientific state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
EPOCH = 2

AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
MATERIALIZATION_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"
SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
ANALYSIS_REL = "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
REQUIREMENTS_REL = "experiments/pdmal_pilot/requirements-full-lock.txt"

PREREG_BLOB_SHA = "9668ec54e50c40b04d40cfa64b817950df4bbffa"
ANALYSIS_LOCK_BLOB_SHA = "26980e27185b3a77980204b2d46a4fdab7e5fc7e"
ANALYSIS_BLOB_SHA = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
ANALYSIS_CONFIG_SHA256 = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
REQUIREMENTS_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"

PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_VALIDATOR"
AUTH_RECORD_ID = "E002-ANALYSIS-AUTH-0001"
AUTH_SCOPE = "LOCKED_PRIMARY_ANALYSIS_ONLY"
MATERIALIZATION_SCOPE = "DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
AUTHORIZATION_NON_EFFECTS = [effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_ANALYSIS"]


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def git(*args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_object_exists(spec: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def read_git_bytes(ref: str, relpath: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "show", f"{ref}:{relpath}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        fail(f"cannot read {ref}:{relpath}: {detail or exc}")
    return completed.stdout


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load JSON from {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {path.relative_to(ROOT)}")
    return value


def load_json_at_ref(ref: str, relpath: str) -> dict[str, Any]:
    try:
        value = json.loads(git("show", f"{ref}:{relpath}"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at {ref}:{relpath}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {ref}:{relpath}")
    return value


def validate_schema(record: dict[str, Any]) -> None:
    schema = load_json(ROOT / SCHEMA_REL)
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"record schema validation failed: {exc.message}")


def validate_semantic_policy() -> None:
    semantics = load_json(ROOT / SEMANTICS_REL)
    if semantics.get("protocol_id") != PROTOCOL_ID:
        fail("primary-analysis authorization semantic policy protocol drifted")

    records = semantics.get("records")
    profiles = semantics.get("profiles")
    if not isinstance(records, dict) or not isinstance(profiles, dict):
        fail("primary-analysis authorization semantic policy is malformed")

    expected_record = {
        "authority_class": "HUMAN_CONTROLLED_AUTHORIZATION",
        "pass_profile": "PRIMARY_ANALYSIS_AUTHORIZATION_PASS",
        "bounded_scope": AUTH_SCOPE,
    }
    if records.get("PRIMARY_ANALYSIS_AUTHORIZATION_RECORD") != expected_record:
        fail("primary-analysis authorization semantic record classification drifted")

    expected_profile = {
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "required_non_effects": AUTHORIZATION_NON_EFFECTS,
        "forbidden_non_effects": ["DOES_NOT_AUTHORIZE_ANALYSIS"],
    }
    if profiles.get("PRIMARY_ANALYSIS_AUTHORIZATION_PASS") != expected_profile:
        fail("primary-analysis authorization semantic PASS profile drifted")


def validate_materialization_receipt(receipt: dict[str, Any]) -> None:
    validate_schema(receipt)
    required = {
        "record_type": "MATERIALIZATION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": EPOCH,
        "evidence_scope": MATERIALIZATION_SCOPE,
        "non_effects": FULL_NON_EFFECTS,
        "status": "PASS",
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }
    for key, expected in required.items():
        if receipt.get(key) != expected:
            fail(f"materialization receipt {key} is not the accepted fail-closed value")


def expected_authorization(
    materialization_receipt: dict[str, Any],
    *,
    materialization_receipt_commit_sha: str,
    materialization_receipt_sha256: str,
    authorization_parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    validate_materialization_receipt(materialization_receipt)
    return {
        "record_type": "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": EPOCH,
        "record_id": AUTH_RECORD_ID,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": authorization_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": materialization_receipt_commit_sha,
            "sha256": materialization_receipt_sha256,
        },
        "evidence_scope": AUTH_SCOPE,
        "non_effects": list(AUTHORIZATION_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [materialization_receipt["record_id"]],
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def validate_authorization_object(
    authorization: dict[str, Any],
    materialization_receipt: dict[str, Any],
    *,
    materialization_receipt_commit_sha: str,
    materialization_receipt_sha256: str,
    authorization_parent_sha: str,
) -> None:
    validate_semantic_policy()
    validate_materialization_receipt(materialization_receipt)
    validate_schema(authorization)

    expected = expected_authorization(
        materialization_receipt,
        materialization_receipt_commit_sha=materialization_receipt_commit_sha,
        materialization_receipt_sha256=materialization_receipt_sha256,
        authorization_parent_sha=authorization_parent_sha,
        generated_at_utc=str(authorization.get("generated_at_utc", "")),
    )
    if authorization != expected:
        fail("primary-analysis authorization record does not match the exact bounded authorization contract")


def validate_frozen_analysis_identities(ref: str) -> None:
    expected_blobs = {
        PREREG_REL: PREREG_BLOB_SHA,
        ANALYSIS_LOCK_REL: ANALYSIS_LOCK_BLOB_SHA,
        ANALYSIS_REL: ANALYSIS_BLOB_SHA,
        REQUIREMENTS_REL: REQUIREMENTS_BLOB_SHA,
    }
    for relpath, expected_blob in expected_blobs.items():
        actual_blob = git("rev-parse", f"{ref}:{relpath}")
        if actual_blob != expected_blob:
            fail(f"frozen Epoch 002 identity drift at {relpath}: " f"expected {expected_blob}, got {actual_blob}")

    lock = load_json_at_ref(ref, ANALYSIS_LOCK_REL)
    if lock.get("protocol_id") != PROTOCOL_ID:
        fail("Epoch 002 analysis lock protocol binding drifted")
    if lock.get("status") != "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL":
        fail("Epoch 002 analysis lock status drifted")
    if lock.get("preregistration_blob_sha") != PREREG_BLOB_SHA:
        fail("Epoch 002 preregistration binding drifted")
    if lock.get("analysis_path") != ANALYSIS_REL:
        fail("Epoch 002 analysis path drifted")
    if lock.get("analysis_blob_sha") != ANALYSIS_BLOB_SHA:
        fail("Epoch 002 analysis blob drifted")
    if lock.get("analysis_config_sha256") != ANALYSIS_CONFIG_SHA256:
        fail("Epoch 002 analysis config digest drifted")
    environment = lock.get("environment")
    if not isinstance(environment, dict):
        fail("Epoch 002 analysis lock environment is malformed")
    if environment.get("requirements_lock_path") != REQUIREMENTS_REL:
        fail("Epoch 002 requirements-lock path drifted")
    if environment.get("requirements_lock_blob_sha") != REQUIREMENTS_BLOB_SHA:
        fail("Epoch 002 requirements-lock blob drifted")


def validate_tooling_only() -> None:
    validate_semantic_policy()
    if (ROOT / AUTH_REL).exists() or git_object_exists(f"HEAD:{AUTH_REL}"):
        fail("tooling mode requires the canonical primary-analysis authorization record to remain absent")
    if (ROOT / RESULT_REL).exists() or git_object_exists(f"HEAD:{RESULT_REL}"):
        fail("tooling mode requires the locked analysis result record to remain absent")
    validate_frozen_analysis_identities("HEAD")


def validate_authorization_event_shape(head: str) -> str:
    lineage = git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("authorization event must have exactly one parent")
    parent = lineage[1]

    changed = [line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if line]
    if changed != [AUTH_REL]:
        fail("authorization event must create exactly the canonical authorization record and no other file")

    if git_object_exists(f"{parent}:{AUTH_REL}"):
        fail("authorization record must be creation-only; it already exists in the parent")

    history = [line for line in git("log", "--format=%H", "--", AUTH_REL).splitlines() if line]
    if history != [head]:
        fail("authorization record must have first-and-only immutable history at the event commit")
    return parent


def validate_authorization_event(head: str, *, accepted_parent_sha: str) -> str:
    parent = validate_authorization_event_shape(head)
    if parent != accepted_parent_sha:
        fail("authorization event parent is not the accepted protected-main parent")
    validate_semantic_policy()

    if not git_object_exists(f"{parent}:{MATERIALIZATION_RECEIPT_REL}"):
        fail("authorization requires an accepted materialization receipt in its parent")
    if not git_object_exists(f"{head}:{MATERIALIZATION_RECEIPT_REL}"):
        fail("materialization receipt must remain present at authorization head")
    if git_object_exists(f"{parent}:{RESULT_REL}") or git_object_exists(f"{head}:{RESULT_REL}"):
        fail("locked analysis result must remain absent during authorization")

    parent_receipt_bytes = read_git_bytes(parent, MATERIALIZATION_RECEIPT_REL)
    head_receipt_bytes = read_git_bytes(head, MATERIALIZATION_RECEIPT_REL)
    if parent_receipt_bytes != head_receipt_bytes:
        fail("materialization receipt bytes changed during authorization event")

    receipt = load_json_at_ref(parent, MATERIALIZATION_RECEIPT_REL)
    validate_materialization_receipt(receipt)

    receipt_history_output = git("log", "--format=%H", "--", MATERIALIZATION_RECEIPT_REL)
    receipt_history = [line for line in receipt_history_output.splitlines() if line]
    if len(receipt_history) != 1:
        fail("materialization receipt must have first-and-only immutable history")
    receipt_event = receipt_history[0]

    receipt_lineage = git("rev-list", "--parents", "-n", "1", receipt_event).split()
    if len(receipt_lineage) != 2 or receipt_lineage[0] != receipt_event:
        fail("materialization receipt event must have exactly one parent")
    receipt_parent = receipt_lineage[1]

    receipt_changed_output = git("diff-tree", "--no-commit-id", "--name-only", "-r", receipt_event)
    receipt_changed = [line for line in receipt_changed_output.splitlines() if line]
    if receipt_changed != [MATERIALIZATION_RECEIPT_REL]:
        fail("materialization receipt event must change exactly the canonical receipt path")
    if git_object_exists(f"{receipt_parent}:{MATERIALIZATION_RECEIPT_REL}"):
        fail("materialization receipt event must be creation-only")

    git("merge-base", "--is-ancestor", receipt_event, parent)

    materialization_receipt_sha256 = hashlib.sha256(parent_receipt_bytes).hexdigest()
    authorization = load_json_at_ref(head, AUTH_REL)
    validate_authorization_object(
        authorization,
        receipt,
        materialization_receipt_commit_sha=receipt_event,
        materialization_receipt_sha256=materialization_receipt_sha256,
        authorization_parent_sha=parent,
    )
    validate_frozen_analysis_identities(parent)
    return parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling", action="store_true", help="validate prospective tooling-only state")
    mode.add_argument("--event-commit", metavar="SHA", help="validate authorization event repository shape")
    parser.add_argument(
        "--accepted-parent",
        metavar="SHA",
        help="accepted protected-main parent SHA required for event validation",
    )
    args = parser.parse_args()

    if args.tooling:
        if args.accepted_parent:
            fail("tooling mode does not accept --accepted-parent")
        validate_tooling_only()
        print("PRIMARY_ANALYSIS_AUTHORIZATION=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("SCIENTIFIC_N_INCREMENT=0")
        return

    if not args.accepted_parent:
        fail("event validation requires --accepted-parent")
    validate_authorization_event(
        args.event_commit,
        accepted_parent_sha=args.accepted_parent,
    )
    print("PRIMARY_ANALYSIS_AUTHORIZATION_EVENT=PASS")
    print("PRIMARY_ANALYSIS_EXECUTION=NOT_PERFORMED")
    print("SCIENTIFIC_N_INCREMENT=0")


if __name__ == "__main__":
    main()
