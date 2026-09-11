#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 materialization evidence and receipt.

This tool validates prospective, non-authorizing materialization evidence and a
future one-file MATERIALIZATION_RECEIPT event. It does not perform decryption,
materialize analysis input, authorize or run primary analysis, inspect outcomes,
or change scientific N.
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
EVIDENCE_SCHEMA_PATH = ROOT / ("docs/experiment/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE_SCHEMA.json")
RESULT_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"

DATASET_LOCK_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
UNBLINDING_DECISION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json"
MATERIALIZATION_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"
PRIMARY_ANALYSIS_AUTH_REL = (
    "docs/experiment/track_a_runs/" "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
)
LOCKED_ANALYSIS_RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"

DATASET_LOCK_PATH = ROOT / DATASET_LOCK_REL
UNBLINDING_DECISION_PATH = ROOT / UNBLINDING_DECISION_REL
MATERIALIZATION_RECEIPT_PATH = ROOT / MATERIALIZATION_RECEIPT_REL
PRIMARY_ANALYSIS_AUTH_PATH = ROOT / PRIMARY_ANALYSIS_AUTH_REL
LOCKED_ANALYSIS_RESULT_PATH = ROOT / LOCKED_ANALYSIS_RESULT_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_VALIDATOR"
UNBLINDING_SCOPE = "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY"
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
UNBLINDING_NON_EFFECTS = [effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_UNBLINDING"]
SCIENTIFIC_NON_EFFECT = {
    "empirical_n_increment": 0,
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
}
PROHIBITED_RETENTION_TOKENS = (
    "private_key",
    "passphrase",
    "blinding_secret",
    "protected_plaintext",
    "decrypted_mapping",
    "secret_material",
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_MATERIALIZATION_FAIL: {message}")


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


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def git_object_exists(spec: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", spec],
            cwd=ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def schema_validator(path: Path) -> Draft202012Validator:
    return Draft202012Validator(load_json(path), format_checker=FormatChecker())


def validate_against(
    validator: Draft202012Validator,
    value: dict[str, Any],
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(value), key=lambda item: list(item.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        fail(f"{label} schema violation at {location}: {first.message}")


def validate_unblinding_decision_object(decision: dict[str, Any]) -> None:
    validate_against(
        schema_validator(RESULT_SCHEMA_PATH),
        decision,
        "unblinding decision",
    )
    expected = {
        "record_type": "UNBLINDING_DECISION_RECORD",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "evidence_scope": UNBLINDING_SCOPE,
        "non_effects": UNBLINDING_NON_EFFECTS,
        "status": "PASS",
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": SCIENTIFIC_NON_EFFECT,
    }
    for key, wanted in expected.items():
        if decision.get(key) != wanted:
            fail(f"unblinding decision {key} mismatch")
    predecessors = decision.get("predecessor_record_ids")
    if not isinstance(predecessors, list) or len(predecessors) != 1:
        fail("unblinding decision must have exactly one dataset-lock predecessor")


def validate_evidence_object(evidence: dict[str, Any]) -> None:
    validate_against(
        schema_validator(EVIDENCE_SCHEMA_PATH),
        evidence,
        "materialization evidence",
    )
    public_id = evidence["public_artifact"]["artifact_id"]
    protected_id = evidence["protected_artifact"]["artifact_id"]
    if public_id == protected_id:
        fail("public and protected artifact IDs must be distinct")
    digests = {
        evidence["materialized_input_sha256"],
        evidence["materialization_manifest_sha256"],
        evidence["materialization_sidecar_sha256"],
    }
    if len(digests) != 3:
        fail("materialized input, manifest, and sidecar digests must be distinct")
    retention_id = evidence["durable_retention"]["id"].lower()
    if any(token in retention_id for token in PROHIBITED_RETENTION_TOKENS):
        fail("durable retention identity must not encode secret-bearing material")


def receipt_record_id(
    unblinding_decision_commit_sha: str,
    unblinding_decision_sha256: str,
    evidence_sha256: str,
) -> str:
    payload = f"{unblinding_decision_commit_sha}:" f"{unblinding_decision_sha256}:" f"{evidence_sha256}"
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    return f"E002-MATERIALIZE-{digest[:16].upper()}"


def expected_receipt(
    decision: dict[str, Any],
    evidence: dict[str, Any],
    *,
    unblinding_decision_commit_sha: str,
    unblinding_decision_sha256: str,
    evidence_sha256: str,
    materialization_parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    validate_unblinding_decision_object(decision)
    validate_evidence_object(evidence)
    if evidence["unblinding_decision_record_id"] != decision["record_id"]:
        fail("materialization evidence unblinding decision record ID mismatch")
    if evidence["unblinding_decision_commit_sha"] != unblinding_decision_commit_sha:
        fail("materialization evidence unblinding decision commit mismatch")
    if evidence["unblinding_decision_sha256"] != unblinding_decision_sha256:
        fail("materialization evidence unblinding decision digest mismatch")
    if evidence["dataset_lock_record_id"] != decision["predecessor_record_ids"][0]:
        fail("materialization evidence dataset-lock lineage mismatch")
    return {
        "record_type": "MATERIALIZATION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": receipt_record_id(
            unblinding_decision_commit_sha,
            unblinding_decision_sha256,
            evidence_sha256,
        ),
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": materialization_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": unblinding_decision_commit_sha,
            "workflow_run_id": evidence["evidence_workflow_run_id"],
            "artifact_id": evidence["evidence_artifact_id"],
            "sha256": evidence_sha256,
        },
        "evidence_scope": MATERIALIZATION_SCOPE,
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [decision["record_id"]],
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": dict(SCIENTIFIC_NON_EFFECT),
    }


def validate_receipt_object(
    receipt: dict[str, Any],
    decision: dict[str, Any],
    evidence: dict[str, Any],
    *,
    unblinding_decision_commit_sha: str,
    unblinding_decision_sha256: str,
    evidence_sha256: str,
    materialization_parent_sha: str,
) -> None:
    validate_against(
        schema_validator(RESULT_SCHEMA_PATH),
        receipt,
        "materialization receipt",
    )
    generated_at = receipt.get("generated_at_utc")
    if not isinstance(generated_at, str):
        fail("materialization receipt generated_at_utc must be a string")
    expected = expected_receipt(
        decision,
        evidence,
        unblinding_decision_commit_sha=unblinding_decision_commit_sha,
        unblinding_decision_sha256=unblinding_decision_sha256,
        evidence_sha256=evidence_sha256,
        materialization_parent_sha=materialization_parent_sha,
        generated_at_utc=generated_at,
    )
    if receipt != expected:
        fail("materialization receipt does not exactly match the non-authorizing contract")


def validate_semantic_policy() -> None:
    semantics = load_json(SEMANTICS_PATH)
    if semantics.get("protocol_id") != PROTOCOL_ID:
        fail("semantic policy protocol drift")
    profiles = semantics.get("profiles")
    records = semantics.get("records")
    if not isinstance(profiles, dict) or not isinstance(records, dict):
        fail("semantic policy profiles/records are malformed")
    expected_record_policy = {
        "authority_class": "NONAUTHORIZING_STATE_TRANSITION",
        "pass_profile": "MATERIALIZATION_PASS",
        "requires_separate_exact_commit_for": "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD",
    }
    if records.get("MATERIALIZATION_RECEIPT") != expected_record_policy:
        fail("materialization receipt semantic classification drift")
    expected_profile = {
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "required_non_effects": FULL_NON_EFFECTS,
        "forbidden_non_effects": [],
    }
    if profiles.get("MATERIALIZATION_PASS") != expected_profile:
        fail("materialization semantic profile drift")
    expected_unblinding_policy = {
        "authority_class": "HUMAN_CONTROLLED_AUTHORIZATION",
        "pass_profile": "UNBLINDING_AUTHORIZATION_PASS",
        "bounded_scope": UNBLINDING_SCOPE,
    }
    if records.get("UNBLINDING_DECISION_RECORD") != expected_unblinding_policy:
        fail("unblinding predecessor semantic policy drift")


def validate_tooling_only() -> None:
    validate_semantic_policy()
    schema_validator(EVIDENCE_SCHEMA_PATH)
    if MATERIALIZATION_RECEIPT_PATH.exists():
        fail("canonical materialization receipt must remain absent in tooling-only mode")
    if PRIMARY_ANALYSIS_AUTH_PATH.exists():
        fail("primary-analysis authorization must remain absent in tooling-only mode")
    if LOCKED_ANALYSIS_RESULT_PATH.exists():
        fail("locked analysis result must remain absent in tooling-only mode")


def path_history(path: str, ref: str = "HEAD") -> list[str]:
    output = git("log", "--format=%H", ref, "--", path)
    return [line for line in output.splitlines() if line]


def validate_materializer_identity(evidence: dict[str, Any], parent: str) -> None:
    commit_sha = evidence["materializer_commit_sha"]
    if not git_is_ancestor(commit_sha, parent):
        fail("materializer commit is not an ancestor of the materialization event parent")
    spec = f"{commit_sha}:{evidence['materializer_path']}"
    if not git_object_exists(spec):
        fail("materializer source is absent at its declared commit")
    if git("rev-parse", spec) != evidence["materializer_blob_sha"]:
        fail("materializer blob identity mismatch")


def validate_dataset_lock_lineage(evidence: dict[str, Any], parent: str) -> None:
    if not git_object_exists(f"{parent}:{DATASET_LOCK_REL}"):
        fail("dataset-lock receipt is not established at the materialization parent")
    history = path_history(DATASET_LOCK_REL, parent)
    if len(history) != 1:
        fail("dataset-lock receipt must have exactly one immutable history event")
    if history[0] != evidence["dataset_lock_commit_sha"]:
        fail("materialization evidence dataset-lock commit mismatch")
    dataset_lock_bytes = git("show", f"{parent}:{DATASET_LOCK_REL}").encode("utf-8")
    if sha256_bytes(dataset_lock_bytes) != evidence["dataset_lock_receipt_sha256"]:
        fail("materialization evidence dataset-lock receipt digest mismatch")
    dataset_lock = json.loads(dataset_lock_bytes.decode("utf-8"))
    record_id = dataset_lock.get("record_id") if isinstance(dataset_lock, dict) else None
    if record_id != evidence["dataset_lock_record_id"]:
        fail("materialization evidence dataset-lock record ID mismatch")


def validate_event(evidence_path: Path) -> None:
    validate_semantic_policy()
    if not MATERIALIZATION_RECEIPT_PATH.exists():
        fail("canonical materialization receipt is absent")
    if not UNBLINDING_DECISION_PATH.exists():
        fail("canonical unblinding decision is absent")
    if PRIMARY_ANALYSIS_AUTH_PATH.exists() or LOCKED_ANALYSIS_RESULT_PATH.exists():
        fail("materialization event cannot contain or follow analysis " "authorization/result at event HEAD")

    head = git("rev-parse", "HEAD")
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        fail("materialization receipt event must have exactly one parent")
    parent = parents[1]
    changed = [line for line in git("diff", "--name-only", parent, head).splitlines() if line]
    if changed != [MATERIALIZATION_RECEIPT_REL]:
        fail("materialization receipt event must change exactly the canonical receipt path")
    if git_object_exists(f"{parent}:{MATERIALIZATION_RECEIPT_REL}"):
        fail("materialization receipt path must be absent at the event parent")
    if path_history(MATERIALIZATION_RECEIPT_REL) != [head]:
        fail("materialization receipt must have first-and-only history at event HEAD")

    decision_history = path_history(UNBLINDING_DECISION_REL, parent)
    if len(decision_history) != 1:
        fail("unblinding decision must have exactly one immutable history event")
    decision_commit = decision_history[0]
    decision_event = git("rev-list", "--parents", "-n", "1", decision_commit).split()
    if len(decision_event) != 2:
        fail("unblinding decision event must have exactly one parent")
    decision_parent = decision_event[1]
    decision_changed = [
        line
        for line in git(
            "diff",
            "--name-only",
            decision_parent,
            decision_commit,
        ).splitlines()
        if line
    ]
    if decision_changed != [UNBLINDING_DECISION_REL]:
        fail("unblinding decision event changed unexpected paths")
    parent_decision_blob = git("rev-parse", f"{parent}:{UNBLINDING_DECISION_REL}")
    head_decision_blob = git("rev-parse", f"HEAD:{UNBLINDING_DECISION_REL}")
    if parent_decision_blob != head_decision_blob:
        fail("unblinding decision changed during materialization receipt event")

    decision = load_json(UNBLINDING_DECISION_PATH)
    validate_unblinding_decision_object(decision)
    decision_digest = sha256_file(UNBLINDING_DECISION_PATH)
    evidence = load_json(evidence_path)
    validate_evidence_object(evidence)
    if evidence["unblinding_decision_commit_sha"] != decision_commit:
        fail("materialization evidence does not bind the accepted unblinding event commit")
    if evidence["unblinding_decision_sha256"] != decision_digest:
        fail("materialization evidence does not bind the exact unblinding decision bytes")
    if evidence["unblinding_decision_record_id"] != decision["record_id"]:
        fail("materialization evidence unblinding decision record ID mismatch")

    validate_dataset_lock_lineage(evidence, parent)
    validate_materializer_identity(evidence, parent)

    evidence_digest = sha256_file(evidence_path)
    receipt = load_json(MATERIALIZATION_RECEIPT_PATH)
    validate_receipt_object(
        receipt,
        decision,
        evidence,
        unblinding_decision_commit_sha=decision_commit,
        unblinding_decision_sha256=decision_digest,
        evidence_sha256=evidence_digest,
        materialization_parent_sha=parent,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling-only", action="store_true")
    mode.add_argument("--validate-event", action="store_true")
    parser.add_argument("--evidence", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tooling_only:
        if args.evidence is not None:
            fail("tooling-only mode does not accept materialization evidence")
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_MATERIALIZATION_TOOLING=PASS_ABSENT")
        print("MATERIALIZATION=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("SCIENTIFIC_N_INCREMENT=0")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
        return
    if args.evidence is None:
        fail("--validate-event requires --evidence")
    validate_event(args.evidence)
    print("TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT=PASS_NONAUTHORIZING")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")


if __name__ == "__main__":
    main()
