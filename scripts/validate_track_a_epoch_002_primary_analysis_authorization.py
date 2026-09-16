#!/usr/bin/env python3
"""Fail-closed Track A Epoch 002 primary-analysis authorization gate.

This validator installs prospective M8/M9 tooling only.  It cannot create a
materialization receipt, execute analysis, increment scientific N, establish
DGAF efficacy, establish independent validation, or authorize High-Assurance.
A positive authorization event is valid only as a later, creation-only commit
whose sole changed file is the canonical authorization record and whose
accepted materialization receipt and frozen analysis identities already exist.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
EPOCH = 2
AUTH_SCOPE = "LOCKED_PRIMARY_ANALYSIS_ONLY"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_VALIDATOR"
MATERIALIZATION_SCOPE = (
    "DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING"
)

SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
ANALYSIS_LOCK_REL = "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
MATERIALIZATION_RECEIPT_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"
)
AUTH_REL = (
    "docs/experiment/track_a_runs/"
    "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
)
LOCKED_RESULT_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
)

SCHEMA_PATH = ROOT / SCHEMA_REL
SEMANTICS_PATH = ROOT / SEMANTICS_REL
ANALYSIS_LOCK_PATH = ROOT / ANALYSIS_LOCK_REL
MATERIALIZATION_RECEIPT_PATH = ROOT / MATERIALIZATION_RECEIPT_REL
AUTH_PATH = ROOT / AUTH_REL
LOCKED_RESULT_PATH = ROOT / LOCKED_RESULT_REL

EXPECTED_PREREG_MERGE = "eed3da6b0c4bae45f13871c45f42027da12ad36e"
EXPECTED_PREREG_BLOB = "9668ec54e50c40b04d40cfa64b817950df4bbffa"
EXPECTED_ANALYSIS_PATH = "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
EXPECTED_ANALYSIS_BLOB = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
EXPECTED_ANALYSIS_CONFIG_SHA256 = (
    "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
)
EXPECTED_REQUIREMENTS_PATH = "experiments/pdmal_pilot/requirements-full-lock.txt"
EXPECTED_REQUIREMENTS_BLOB = "00c1f779e97030f9b25ae494642edb31b5b09de5"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
AUTH_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
SCIENTIFIC_STATE = {
    "empirical_n_increment": 0,
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
}

EXPECTED_ANALYSIS_LOCK = {
    "record_type": "TRACK_A_EPOCH_002_ANALYSIS_LOCK",
    "schema_version": 1,
    "controller_issue": 523,
    "protocol_id": PROTOCOL_ID,
    "status": "ANALYSIS_IMPLEMENTATION_LOCKED_NONEMPIRICAL",
    "preregistration_merge_sha": EXPECTED_PREREG_MERGE,
    "preregistration_blob_sha": EXPECTED_PREREG_BLOB,
    "analysis_path": EXPECTED_ANALYSIS_PATH,
    "analysis_blob_sha": EXPECTED_ANALYSIS_BLOB,
    "analysis_config_sha256": EXPECTED_ANALYSIS_CONFIG_SHA256,
    "environment": {
        "python_version": "3.12.0",
        "requirements_lock_path": EXPECTED_REQUIREMENTS_PATH,
        "requirements_lock_blob_sha": EXPECTED_REQUIREMENTS_BLOB,
        "install_policy": "PIP_REQUIRE_HASHES",
    },
    "numpy_version": "2.5.1",
    "pytest_version": "9.0.3",
    "primary_contract": {
        "seed_count": 50,
        "expected_total_records": 2250,
        "endpoint": "ffcr_success",
        "primary_topology": "pdmal",
        "primary_comparator": "random_regular",
        "estimand": "mean_seed_paired_pdmal_minus_random_regular_ffcr",
        "bootstrap": "paired_seed_effects_percentile",
        "bootstrap_resamples": 10000,
        "bootstrap_seed": 20270251,
        "alpha": 0.05,
        "confirmatory_test_count": 1,
    },
    "boundaries": {
        "runner_implemented_by_this_lock": False,
        "successor_custody_recovery_receipt_established": False,
        "exact_candidate_freeze_established": False,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "empirical_execution_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    },
}


def fail(message: str) -> None:
    raise SystemExit(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def git(*args: str, binary: bool = False) -> str | bytes:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=not binary, stderr=subprocess.STDOUT
        ).strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode() if isinstance(exc.output, bytes) else exc.output
        fail(f"git {' '.join(args)} failed: {output.strip()}")


def schema_validate(record: dict[str, Any]) -> None:
    schema = load_json(SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(record), key=lambda e: list(e.path))
    if errors:
        detail = "; ".join(error.message for error in errors[:5])
        fail(f"result-record schema validation failed: {detail}")


def validate_semantic_contract() -> None:
    semantics = load_json(SEMANTICS_PATH)
    if semantics.get("protocol_id") != PROTOCOL_ID:
        fail("result-record semantics protocol drift")
    profiles = semantics.get("profiles", {})
    auth_profile = profiles.get("PRIMARY_ANALYSIS_AUTHORIZATION_PASS", {})
    if auth_profile.get("authorization_effect") != "BOUNDED_RECORD_ONLY":
        fail("primary-analysis authorization profile effect drift")
    if auth_profile.get("required_non_effects") != AUTH_NON_EFFECTS:
        fail("primary-analysis authorization non-effects drift")
    if auth_profile.get("forbidden_non_effects") != ["DOES_NOT_AUTHORIZE_ANALYSIS"]:
        fail("primary-analysis authorization forbidden non-effect drift")
    records = semantics.get("records", {})
    materialization = records.get("MATERIALIZATION_RECEIPT", {})
    if materialization.get("requires_separate_exact_commit_for") != (
        "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"
    ):
        fail("materialization-to-authorization separation contract drift")
    authorization = records.get("PRIMARY_ANALYSIS_AUTHORIZATION_RECORD", {})
    if authorization.get("authority_class") != "HUMAN_CONTROLLED_AUTHORIZATION":
        fail("primary-analysis authorization authority-class drift")
    if authorization.get("pass_profile") != "PRIMARY_ANALYSIS_AUTHORIZATION_PASS":
        fail("primary-analysis authorization pass-profile drift")
    if authorization.get("bounded_scope") != AUTH_SCOPE:
        fail("primary-analysis authorization bounded-scope drift")


def validate_analysis_lock_object(lock: dict[str, Any]) -> None:
    if lock != EXPECTED_ANALYSIS_LOCK:
        fail("Epoch 002 frozen analysis-lock identity or contract drift")


def validate_materialization_receipt_object(receipt: dict[str, Any]) -> None:
    schema_validate(receipt)
    expected = {
        "record_type": "MATERIALIZATION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": EPOCH,
        "evidence_scope": MATERIALIZATION_SCOPE,
        "status": "PASS",
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": SCIENTIFIC_STATE,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            fail(f"materialization receipt {key} drift")
    if receipt.get("non_effects") != FULL_NON_EFFECTS:
        fail("materialization receipt non-effects drift")


def expected_authorization(
    materialization_receipt: dict[str, Any],
    *,
    materialization_receipt_commit_sha: str,
    materialization_receipt_sha256: str,
    authorization_parent_sha: str,
    authorization_parent_tree_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    validate_materialization_receipt_object(materialization_receipt)
    return {
        "record_type": "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": EPOCH,
        "record_id": f"E002-PRIMARY-AUTH-{materialization_receipt_sha256[:16].upper()}",
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": authorization_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": materialization_receipt_commit_sha,
            "tree_sha": authorization_parent_tree_sha,
            "sha256": materialization_receipt_sha256,
        },
        "evidence_scope": AUTH_SCOPE,
        "non_effects": list(AUTH_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [materialization_receipt["record_id"]],
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": dict(SCIENTIFIC_STATE),
    }


def validate_authorization_object(
    authorization: dict[str, Any],
    materialization_receipt: dict[str, Any],
    *,
    materialization_receipt_commit_sha: str,
    materialization_receipt_sha256: str,
    authorization_parent_sha: str,
    authorization_parent_tree_sha: str,
) -> None:
    validate_semantic_contract()
    validate_materialization_receipt_object(materialization_receipt)
    schema_validate(authorization)
    expected = expected_authorization(
        materialization_receipt,
        materialization_receipt_commit_sha=materialization_receipt_commit_sha,
        materialization_receipt_sha256=materialization_receipt_sha256,
        authorization_parent_sha=authorization_parent_sha,
        authorization_parent_tree_sha=authorization_parent_tree_sha,
        generated_at_utc=authorization.get("generated_at_utc", ""),
    )
    if authorization != expected:
        fail("primary-analysis authorization object does not match exact bounded contract")


def validate_event_shape(
    *,
    parent_count: int,
    changed_files: list[str],
    authorization_existed_at_parent: bool,
    authorization_history: list[str],
    head_sha: str,
    locked_result_exists_at_parent: bool,
    locked_result_exists_at_head: bool,
) -> None:
    if parent_count != 1:
        fail("authorization event must have exactly one parent")
    if changed_files != [AUTH_REL]:
        fail("authorization event must change exactly the canonical authorization record")
    if authorization_existed_at_parent:
        fail("authorization record must be creation-only")
    if authorization_history != [head_sha]:
        fail("authorization record must have first-and-only history at HEAD")
    if locked_result_exists_at_parent or locked_result_exists_at_head:
        fail("locked analysis result must not pre-exist authorization")


def validate_frozen_parent_tree(parent_sha: str) -> str:
    tree_sha = str(git("rev-parse", f"{parent_sha}^{{tree}}"))
    required_blobs = {
        PREREG_REL: EXPECTED_PREREG_BLOB,
        EXPECTED_ANALYSIS_PATH: EXPECTED_ANALYSIS_BLOB,
        EXPECTED_REQUIREMENTS_PATH: EXPECTED_REQUIREMENTS_BLOB,
    }
    for path, expected_blob in required_blobs.items():
        actual_blob = str(git("rev-parse", f"{parent_sha}:{path}"))
        if actual_blob != expected_blob:
            fail(f"frozen parent identity drift for {path}")
    parent_lock_bytes = git("show", f"{parent_sha}:{ANALYSIS_LOCK_REL}", binary=True)
    assert isinstance(parent_lock_bytes, bytes)
    try:
        parent_lock = json.loads(parent_lock_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse parent analysis lock: {exc}")
    validate_analysis_lock_object(parent_lock)
    return tree_sha


def file_exists_at(commit: str, path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{path}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate_tooling_only() -> None:
    validate_semantic_contract()
    validate_analysis_lock_object(load_json(ANALYSIS_LOCK_PATH))
    if AUTH_PATH.exists():
        fail("tooling mode requires canonical authorization record to remain absent")
    if LOCKED_RESULT_PATH.exists():
        fail("tooling mode requires locked analysis result to remain absent")


def validate_authorization_event() -> None:
    head_sha = str(git("rev-parse", "HEAD"))
    parents = str(git("show", "-s", "--format=%P", head_sha)).split()
    parent_count = len(parents)
    if parent_count != 1:
        fail("authorization event must have exactly one parent")
    parent_sha = parents[0]
    changed_files_text = str(git("diff", "--name-only", parent_sha, head_sha))
    changed_files = [line for line in changed_files_text.splitlines() if line]
    authorization_history_text = str(git("log", "--format=%H", "--", AUTH_REL))
    authorization_history = [line for line in authorization_history_text.splitlines() if line]
    validate_event_shape(
        parent_count=parent_count,
        changed_files=changed_files,
        authorization_existed_at_parent=file_exists_at(parent_sha, AUTH_REL),
        authorization_history=authorization_history,
        head_sha=head_sha,
        locked_result_exists_at_parent=file_exists_at(parent_sha, LOCKED_RESULT_REL),
        locked_result_exists_at_head=LOCKED_RESULT_PATH.exists(),
    )

    if not file_exists_at(parent_sha, MATERIALIZATION_RECEIPT_REL):
        fail("accepted materialization receipt must pre-exist authorization event")
    receipt_history_text = str(
        git("log", "--format=%H", "--", MATERIALIZATION_RECEIPT_REL)
    )
    receipt_history = [line for line in receipt_history_text.splitlines() if line]
    if len(receipt_history) != 1:
        fail("materialization receipt must have exactly one immutable history event")
    receipt_commit_sha = receipt_history[0]
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", receipt_commit_sha, parent_sha],
        cwd=ROOT,
        check=False,
    ).returncode != 0:
        fail("materialization receipt event is not an ancestor of authorization parent")

    parent_receipt_bytes = git(
        "show", f"{parent_sha}:{MATERIALIZATION_RECEIPT_REL}", binary=True
    )
    head_receipt_bytes = MATERIALIZATION_RECEIPT_PATH.read_bytes()
    assert isinstance(parent_receipt_bytes, bytes)
    if parent_receipt_bytes != head_receipt_bytes:
        fail("materialization receipt changed across authorization event")
    creation_receipt_bytes = git(
        "show", f"{receipt_commit_sha}:{MATERIALIZATION_RECEIPT_REL}", binary=True
    )
    assert isinstance(creation_receipt_bytes, bytes)
    if creation_receipt_bytes != parent_receipt_bytes:
        fail("materialization receipt bytes drifted after accepted creation event")

    try:
        receipt = json.loads(parent_receipt_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse materialization receipt: {exc}")
    validate_materialization_receipt_object(receipt)
    receipt_sha256 = hashlib.sha256(parent_receipt_bytes).hexdigest()
    parent_tree_sha = validate_frozen_parent_tree(parent_sha)
    authorization = load_json(AUTH_PATH)
    validate_authorization_object(
        authorization,
        receipt,
        materialization_receipt_commit_sha=receipt_commit_sha,
        materialization_receipt_sha256=receipt_sha256,
        authorization_parent_sha=parent_sha,
        authorization_parent_tree_sha=parent_tree_sha,
    )


def main() -> None:
    if AUTH_PATH.exists():
        validate_authorization_event()
        print("PRIMARY_ANALYSIS_AUTHORIZATION=ESTABLISHED")
        print("PRIMARY_ANALYSIS=AUTHORIZED_NOT_RUN")
    else:
        validate_tooling_only()
        if MATERIALIZATION_RECEIPT_PATH.exists():
            print("MATERIALIZATION_RECEIPT=PRESENT_AUTHORIZATION_NOT_ESTABLISHED")
        else:
            print("MATERIALIZATION_RECEIPT=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=PRE_FREEZE_FAIL_CLOSED_NOT_AUTHORIZED_N0")


if __name__ == "__main__":
    main()
