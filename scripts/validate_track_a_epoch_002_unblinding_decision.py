#!/usr/bin/env python3
"""Fail-closed validator for the Track A Epoch 002 unblinding decision.

This tool validates a future human-controlled authorization record only. It does
not decrypt protected material, release mappings, materialize analysis input,
authorize primary analysis, execute empirical work, or change scientific N.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RESULT_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"

DATASET_LOCK_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
DECISION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json"
DATASET_LOCK_PATH = ROOT / DATASET_LOCK_REL
DECISION_PATH = ROOT / DECISION_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_UNBLINDING_DECISION_VALIDATOR"
DATASET_LOCK_SCOPE = "CONTENT_ADDRESSED_EPOCH_002_BLINDED_DATASET_LOCK_BEFORE_UNBLINDING"
UNBLINDING_SCOPE = "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
UNBLINDING_NON_EFFECTS = [effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_UNBLINDING"]
SCIENTIFIC_NON_EFFECT = {
    "empirical_n_increment": 0,
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
}
PROHIBITED_TOKENS = (
    "private_key",
    "passphrase",
    "blinding_secret",
    "recovery_key",
    "protected_plaintext",
    "decrypted_mapping",
    "encrypted_backup",
    "secret_material",
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_UNBLINDING_DECISION_FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"required file is absent: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {path.relative_to(ROOT)}")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def assert_no_secret_surface(value: Any, path: str = "record") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered_key = str(key).lower()
            if any(token in lowered_key for token in PROHIBITED_TOKENS):
                fail(f"prohibited secret-bearing field at {path}.{key}")
            assert_no_secret_surface(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_secret_surface(child, f"{path}[{index}]")
        return
    if isinstance(value, str):
        lowered_value = value.lower()
        if any(token in lowered_value for token in PROHIBITED_TOKENS):
            fail(f"prohibited secret-bearing value at {path}")


def validate_structural_record(record: dict[str, Any]) -> None:
    schema = load_json(RESULT_SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda item: list(item.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        fail(f"result-record schema violation at {location}: {first.message}")


def validate_dataset_lock_receipt_object(record: dict[str, Any]) -> None:
    assert_no_secret_surface(record, "dataset_lock")
    validate_structural_record(record)
    expected = {
        "record_type": "DATASET_LOCK_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "evidence_scope": DATASET_LOCK_SCOPE,
        "non_effects": FULL_NON_EFFECTS,
        "status": "PASS",
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": SCIENTIFIC_NON_EFFECT,
    }
    for key, wanted in expected.items():
        if record.get(key) != wanted:
            fail(f"dataset-lock receipt {key} mismatch")
    predecessors = record.get("predecessor_record_ids")
    if not isinstance(predecessors, list) or len(predecessors) != 1:
        fail("dataset-lock receipt must have exactly one QC predecessor")


def decision_record_id(dataset_lock_commit_sha: str, dataset_lock_receipt_sha256: str) -> str:
    digest = hashlib.sha256(f"{dataset_lock_commit_sha}:{dataset_lock_receipt_sha256}".encode("ascii")).hexdigest()
    return f"E002-UNBLINDING-{digest[:16].upper()}"


def expected_decision(
    dataset_lock: dict[str, Any],
    *,
    dataset_lock_commit_sha: str,
    dataset_lock_receipt_sha256: str,
    authorization_parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    validate_dataset_lock_receipt_object(dataset_lock)
    return {
        "record_type": "UNBLINDING_DECISION_RECORD",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": decision_record_id(dataset_lock_commit_sha, dataset_lock_receipt_sha256),
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": authorization_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": dataset_lock_commit_sha,
            "sha256": dataset_lock_receipt_sha256,
        },
        "evidence_scope": UNBLINDING_SCOPE,
        "non_effects": list(UNBLINDING_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [dataset_lock["record_id"]],
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": dict(SCIENTIFIC_NON_EFFECT),
    }


def validate_decision_object(
    decision: dict[str, Any],
    dataset_lock: dict[str, Any],
    *,
    dataset_lock_commit_sha: str,
    dataset_lock_receipt_sha256: str,
    authorization_parent_sha: str,
) -> None:
    assert_no_secret_surface(decision, "unblinding_decision")
    validate_structural_record(decision)
    generated_at = decision.get("generated_at_utc")
    if not isinstance(generated_at, str):
        fail("unblinding decision generated_at_utc must be a string")
    expected = expected_decision(
        dataset_lock,
        dataset_lock_commit_sha=dataset_lock_commit_sha,
        dataset_lock_receipt_sha256=dataset_lock_receipt_sha256,
        authorization_parent_sha=authorization_parent_sha,
        generated_at_utc=generated_at,
    )
    if decision != expected:
        fail("unblinding decision does not exactly match the bounded authorization contract")


def validate_semantic_policy() -> None:
    semantics = load_json(SEMANTICS_PATH)
    if semantics.get("protocol_id") != PROTOCOL_ID:
        fail("semantic policy protocol drift")
    policy_effect = semantics.get("policy_effect")
    expected_policy_effect = {
        "creates_result_records": False,
        "authorizes_collection": False,
        "authorizes_unblinding": False,
        "authorizes_primary_analysis": False,
        "executes_empirical_work": False,
        "increments_scientific_n": False,
        "establishes_canonical_dgaf_efficacy": False,
        "establishes_independent_validation": False,
        "authorizes_high_assurance": False,
    }
    if policy_effect != expected_policy_effect:
        fail("semantic policy non-authorizing effect drift")
    profiles = semantics.get("profiles")
    records = semantics.get("records")
    if not isinstance(profiles, dict) or not isinstance(records, dict):
        fail("semantic policy profiles/records are malformed")
    unblinding_record = records.get("UNBLINDING_DECISION_RECORD")
    expected_record_policy = {
        "authority_class": "HUMAN_CONTROLLED_AUTHORIZATION",
        "pass_profile": "UNBLINDING_AUTHORIZATION_PASS",
        "bounded_scope": UNBLINDING_SCOPE,
    }
    if unblinding_record != expected_record_policy:
        fail("unblinding record semantic classification drift")
    profile = profiles.get("UNBLINDING_AUTHORIZATION_PASS")
    expected_profile = {
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "required_non_effects": UNBLINDING_NON_EFFECTS,
        "forbidden_non_effects": ["DOES_NOT_AUTHORIZE_UNBLINDING"],
    }
    if profile != expected_profile:
        fail("unblinding authorization semantic profile drift")
    dataset_lock_policy = records.get("DATASET_LOCK_RECEIPT")
    expected_dataset_lock_policy = {
        "authority_class": "NONAUTHORIZING_STATE_TRANSITION",
        "pass_profile": "DATASET_LOCK_PASS",
        "requires_separate_exact_commit_for": "UNBLINDING_DECISION_RECORD",
    }
    if dataset_lock_policy != expected_dataset_lock_policy:
        fail("dataset-lock predecessor semantic policy drift")


def validate_tooling_only() -> None:
    validate_semantic_policy()
    if DECISION_PATH.exists():
        fail("canonical unblinding decision must remain absent in tooling-only mode")


def path_history(path: str) -> list[str]:
    output = git("log", "--format=%H", "--", path)
    return [line for line in output.splitlines() if line]


def validate_event() -> None:
    validate_semantic_policy()
    if not DECISION_PATH.exists():
        fail("canonical unblinding decision is absent")
    if not DATASET_LOCK_PATH.exists():
        fail("canonical dataset-lock receipt is absent")

    head = git("rev-parse", "HEAD")
    parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
    if len(parents) != 2:
        fail("unblinding decision event must have exactly one parent")
    parent = parents[1]

    changed = [line for line in git("diff", "--name-only", parent, head).splitlines() if line]
    if changed != [DECISION_REL]:
        fail("unblinding decision event must change exactly the canonical decision path")

    parent_presence = subprocess.run(
        ["git", "cat-file", "-e", f"{parent}:{DECISION_REL}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if parent_presence.returncode == 0:
        fail("unblinding decision path must be absent at the event parent")

    decision_history = path_history(DECISION_REL)
    if decision_history != [head]:
        fail("unblinding decision must have first-and-only history at event HEAD")

    lock_history = path_history(DATASET_LOCK_REL)
    if len(lock_history) != 1:
        fail("dataset-lock receipt must have exactly one immutable history event")
    dataset_lock_commit = lock_history[0]

    lock_blob_head = git("rev-parse", f"HEAD:{DATASET_LOCK_REL}")
    lock_blob_parent = git("rev-parse", f"{parent}:{DATASET_LOCK_REL}")
    if lock_blob_head != lock_blob_parent:
        fail("dataset-lock receipt changed during unblinding authorization event")

    dataset_lock_bytes = DATASET_LOCK_PATH.read_bytes()
    dataset_lock_digest = sha256_bytes(dataset_lock_bytes)
    dataset_lock = load_json(DATASET_LOCK_PATH)
    decision = load_json(DECISION_PATH)
    validate_decision_object(
        decision,
        dataset_lock,
        dataset_lock_commit_sha=dataset_lock_commit,
        dataset_lock_receipt_sha256=dataset_lock_digest,
        authorization_parent_sha=parent,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling-only", action="store_true")
    mode.add_argument("--validate-event", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tooling_only:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_UNBLINDING_DECISION_TOOLING=PASS_ABSENT")
        print("UNBLINDING=NOT_AUTHORIZED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED")
        print("SCIENTIFIC_N_INCREMENT=0")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
        return
    validate_event()
    print("TRACK_A_EPOCH_002_UNBLINDING_DECISION_EVENT=PASS_BOUNDED")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")


if __name__ == "__main__":
    main()
