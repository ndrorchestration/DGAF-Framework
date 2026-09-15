#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 materialization evidence and receipt.

This tool validates prospective operator-produced materialization evidence, a
creation-only repository evidence-admission event, and a later one-file
MATERIALIZATION_RECEIPT event. It does not perform decryption, materialize
analysis input, authorize or run primary analysis, inspect outcomes, or change
scientific N.
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
DATASET_LOCK_EVIDENCE_SCHEMA_PATH = ROOT / ("docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json")
RESULT_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"

DATASET_LOCK_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
DATASET_LOCK_EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json"
UNBLINDING_DECISION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json"
MATERIALIZATION_EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"
MATERIALIZATION_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json"
PRIMARY_ANALYSIS_AUTH_REL = (
    "docs/experiment/track_a_runs/" "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
)
LOCKED_ANALYSIS_RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"

DATASET_LOCK_PATH = ROOT / DATASET_LOCK_REL
DATASET_LOCK_EVIDENCE_PATH = ROOT / DATASET_LOCK_EVIDENCE_REL
UNBLINDING_DECISION_PATH = ROOT / UNBLINDING_DECISION_REL
MATERIALIZATION_EVIDENCE_PATH = ROOT / MATERIALIZATION_EVIDENCE_REL
MATERIALIZATION_RECEIPT_PATH = ROOT / MATERIALIZATION_RECEIPT_REL
PRIMARY_ANALYSIS_AUTH_PATH = ROOT / PRIMARY_ANALYSIS_AUTH_REL
LOCKED_ANALYSIS_RESULT_PATH = ROOT / LOCKED_ANALYSIS_RESULT_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_VALIDATOR"
DATASET_LOCK_SCOPE = "CONTENT_ADDRESSED_EPOCH_002_BLINDED_DATASET_LOCK_BEFORE_UNBLINDING"
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


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"required file is absent: {display_path(path)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at {display_path(path)}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {display_path(path)}")
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


def path_history(path: str, ref: str = "HEAD") -> list[str]:
    output = git("log", "--format=%H", ref, "--", path)
    return [line for line in output.splitlines() if line]


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


def validate_dataset_lock_receipt_object(receipt: dict[str, Any]) -> None:
    validate_against(
        schema_validator(RESULT_SCHEMA_PATH),
        receipt,
        "dataset-lock receipt",
    )
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
        if receipt.get(key) != wanted:
            fail(f"dataset-lock receipt {key} mismatch")
    predecessors = receipt.get("predecessor_record_ids")
    if not isinstance(predecessors, list) or len(predecessors) != 1:
        fail("dataset-lock receipt must have exactly one predecessor")


def validate_unblinding_decision_object(
    decision: dict[str, Any],
    dataset_lock: dict[str, Any] | None = None,
) -> None:
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
    if dataset_lock is not None and predecessors != [dataset_lock.get("record_id")]:
        fail("unblinding decision does not bind the accepted dataset-lock record")


def validate_accepted_predecessor_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    if not DATASET_LOCK_PATH.exists():
        fail("accepted dataset-lock receipt is required before materialization tooling")
    if not UNBLINDING_DECISION_PATH.exists():
        fail("accepted bounded unblinding decision is required before materialization tooling")

    dataset_lock = load_json(DATASET_LOCK_PATH)
    decision = load_json(UNBLINDING_DECISION_PATH)
    validate_dataset_lock_receipt_object(dataset_lock)
    validate_unblinding_decision_object(decision, dataset_lock)

    lock_history = path_history(DATASET_LOCK_REL)
    if len(lock_history) != 1:
        fail("dataset-lock receipt must have exactly one immutable history event")
    decision_history = path_history(UNBLINDING_DECISION_REL)
    if len(decision_history) != 1:
        fail("unblinding decision must have exactly one immutable history event")
    lock_commit = lock_history[0]
    decision_commit = decision_history[0]
    if not git_is_ancestor(lock_commit, decision_commit):
        fail("unblinding decision is not descended from the accepted dataset-lock event")

    subject = decision.get("immutable_subject")
    if not isinstance(subject, dict):
        fail("unblinding decision immutable subject is malformed")
    if subject.get("commit_sha") != lock_commit:
        fail("unblinding decision does not bind the accepted dataset-lock event commit")
    if subject.get("sha256") != sha256_file(DATASET_LOCK_PATH):
        fail("unblinding decision does not bind the exact dataset-lock receipt bytes")
    return dataset_lock, decision


def validate_evidence_object(evidence: dict[str, Any]) -> None:
    validate_against(
        schema_validator(EVIDENCE_SCHEMA_PATH),
        evidence,
        "materialization evidence",
    )
    if evidence.get("evidence_execution_class") != "OPERATOR_CODESPACE":
        fail("materialization evidence execution class must be OPERATOR_CODESPACE")
    forbidden_actions_fields = ("evidence_workflow_run_id", "evidence_artifact_id")
    if any(field in evidence for field in forbidden_actions_fields):
        fail("operator materialization evidence must not contain GitHub Actions IDs")
    for label in ("public_artifact", "protected_artifact"):
        if "artifact_id" in evidence[label]:
            fail(f"operator {label} must not contain a GitHub Actions artifact ID")

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


def validate_evidence_against_dataset_lock(
    evidence: dict[str, Any],
    dataset_lock_evidence: dict[str, Any],
) -> None:
    validate_evidence_object(evidence)
    validate_against(
        schema_validator(DATASET_LOCK_EVIDENCE_SCHEMA_PATH),
        dataset_lock_evidence,
        "dataset-lock evidence",
    )
    if dataset_lock_evidence.get("protocol_id") != evidence["protocol_id"]:
        fail("dataset-lock evidence protocol identity mismatch")
    if dataset_lock_evidence.get("epoch") != evidence["epoch"]:
        fail("dataset-lock evidence epoch mismatch")
    if dataset_lock_evidence.get("paired_seed_units") != evidence["paired_seed_units"]:
        fail("materialization paired seed-unit count drifted from dataset lock")
    if dataset_lock_evidence.get("blinded_observations") != evidence["record_count"]:
        fail("materialization record count drifted from dataset lock")

    public_fields = (
        "name",
        "size_bytes",
        "archive_sha256",
        "manifest_sha256",
    )
    for field in public_fields:
        if dataset_lock_evidence["public_artifact"].get(field) != evidence["public_artifact"].get(field):
            fail(f"public artifact {field} drifted from dataset-lock evidence")

    protected_fields = (
        "name",
        "size_bytes",
        "archive_sha256",
        "ciphertext_sha256",
        "plaintext_tar_sha256",
        "custody_certificate_sha256",
        "custody_certificate_public_key_der_sha256",
    )
    for field in protected_fields:
        if dataset_lock_evidence["protected_artifact"].get(field) != evidence["protected_artifact"].get(field):
            fail(f"protected artifact {field} drifted from dataset-lock evidence")

    if dataset_lock_evidence.get("custody_class") != evidence["custody_class"]:
        fail("custody class drifted from dataset-lock evidence")
    if dataset_lock_evidence.get("independent_custody") != evidence["independent_custody"]:
        fail("custody independence classification drifted from dataset-lock evidence")

    expected_lock_state = {
        "outcomes_inspected_for_lock": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "dataset_lock_evidence_status": "STRUCTURAL_QC_PASS_PENDING_REPOSITORY_RECEIPT",
    }
    for key, expected in expected_lock_state.items():
        if dataset_lock_evidence.get(key) != expected:
            fail(f"dataset-lock evidence state drift: {key}")


def receipt_record_id(evidence_admission_commit_sha: str, evidence_sha256: str) -> str:
    payload = f"{evidence_admission_commit_sha}:{evidence_sha256}"
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
        "record_id": receipt_record_id(materialization_parent_sha, evidence_sha256),
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": materialization_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": materialization_parent_sha,
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


def validate_no_analysis_successor() -> None:
    if PRIMARY_ANALYSIS_AUTH_PATH.exists():
        fail("primary-analysis authorization must remain absent")
    if LOCKED_ANALYSIS_RESULT_PATH.exists():
        fail("locked analysis result must remain absent")


def validate_tooling_only() -> None:
    validate_semantic_policy()
    schema_validator(EVIDENCE_SCHEMA_PATH)
    schema_validator(DATASET_LOCK_EVIDENCE_SCHEMA_PATH)
    validate_accepted_predecessor_chain()
    if MATERIALIZATION_EVIDENCE_PATH.exists():
        fail("canonical materialization evidence must remain absent in tooling-only mode")
    if MATERIALIZATION_RECEIPT_PATH.exists():
        fail("canonical materialization receipt must remain absent in tooling-only mode")
    validate_no_analysis_successor()


def validate_materializer_identity(evidence: dict[str, Any], parent: str) -> None:
    commit_sha = evidence["materializer_commit_sha"]
    if not git_is_ancestor(commit_sha, parent):
        fail("materializer commit is not an ancestor of the evidence-admission parent")
    spec = f"{commit_sha}:{evidence['materializer_path']}"
    if not git_object_exists(spec):
        fail("materializer source is absent at its declared commit")
    if git("rev-parse", spec) != evidence["materializer_blob_sha"]:
        fail("materializer blob identity mismatch")
    tooling_commit = evidence["evidence_tooling_commit_sha"]
    if not git_is_ancestor(tooling_commit, parent):
        fail("evidence tooling commit is not an ancestor of the evidence-admission parent")


def validate_dataset_lock_lineage(evidence: dict[str, Any], parent: str) -> None:
    if not git_object_exists(f"{parent}:{DATASET_LOCK_REL}"):
        fail("dataset-lock receipt is not established at the evidence-admission parent")
    history = path_history(DATASET_LOCK_REL, parent)
    if len(history) != 1:
        fail("dataset-lock receipt must have exactly one immutable history event")
    if history[0] != evidence["dataset_lock_commit_sha"]:
        fail("materialization evidence dataset-lock commit mismatch")
    dataset_lock_bytes = git("show", f"{parent}:{DATASET_LOCK_REL}").encode("utf-8")
    if sha256_bytes(dataset_lock_bytes) != evidence["dataset_lock_receipt_sha256"]:
        fail("materialization evidence dataset-lock receipt digest mismatch")
    dataset_lock = json.loads(dataset_lock_bytes.decode("utf-8"))
    if not isinstance(dataset_lock, dict):
        fail("dataset-lock receipt at evidence-admission parent is malformed")
    validate_dataset_lock_receipt_object(dataset_lock)
    if dataset_lock.get("record_id") != evidence["dataset_lock_record_id"]:
        fail("materialization evidence dataset-lock record ID mismatch")


def validate_evidence_predecessors(evidence: dict[str, Any], parent: str) -> None:
    dataset_lock = load_json(DATASET_LOCK_PATH)
    decision = load_json(UNBLINDING_DECISION_PATH)
    validate_dataset_lock_receipt_object(dataset_lock)
    validate_unblinding_decision_object(decision, dataset_lock)

    decision_history = path_history(UNBLINDING_DECISION_REL, parent)
    if len(decision_history) != 1:
        fail("unblinding decision must have exactly one immutable history event")
    decision_commit = decision_history[0]
    decision_bytes = git("show", f"{parent}:{UNBLINDING_DECISION_REL}").encode("utf-8")
    decision_digest = sha256_bytes(decision_bytes)
    if evidence["unblinding_decision_commit_sha"] != decision_commit:
        fail("materialization evidence does not bind the accepted unblinding event commit")
    if evidence["unblinding_decision_sha256"] != decision_digest:
        fail("materialization evidence does not bind the exact unblinding decision bytes")
    if evidence["unblinding_decision_record_id"] != decision["record_id"]:
        fail("materialization evidence unblinding decision record ID mismatch")

    validate_dataset_lock_lineage(evidence, parent)
    validate_materializer_identity(evidence, parent)


def validate_evidence_admission() -> None:
    validate_semantic_policy()
    if not MATERIALIZATION_EVIDENCE_PATH.exists():
        fail("canonical materialization evidence is absent")
    if MATERIALIZATION_RECEIPT_PATH.exists():
        fail("materialization evidence admission must precede receipt creation")
    validate_no_analysis_successor()

    head = git("rev-parse", "HEAD")
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        fail("materialization evidence admission must have exactly one parent")
    parent = parents[1]
    changed = [line for line in git("diff", "--name-only", parent, head).splitlines() if line]
    if changed != [MATERIALIZATION_EVIDENCE_REL]:
        fail("materialization evidence admission must change exactly the canonical evidence path")
    if git_object_exists(f"{parent}:{MATERIALIZATION_EVIDENCE_REL}"):
        fail("materialization evidence path must be absent at the admission parent")
    if path_history(MATERIALIZATION_EVIDENCE_REL) != [head]:
        fail("materialization evidence must have first-and-only history at admission HEAD")

    evidence = load_json(MATERIALIZATION_EVIDENCE_PATH)
    dataset_lock_evidence = load_json(DATASET_LOCK_EVIDENCE_PATH)
    validate_evidence_against_dataset_lock(evidence, dataset_lock_evidence)
    validate_evidence_predecessors(evidence, parent)


def validate_receipt_event() -> None:
    validate_semantic_policy()
    if not MATERIALIZATION_EVIDENCE_PATH.exists():
        fail("canonical materialization evidence is absent")
    if not MATERIALIZATION_RECEIPT_PATH.exists():
        fail("canonical materialization receipt is absent")
    validate_no_analysis_successor()

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

    evidence_history = path_history(MATERIALIZATION_EVIDENCE_REL, parent)
    if len(evidence_history) != 1:
        fail("materialization evidence must have exactly one immutable history event")
    evidence_commit = evidence_history[0]
    if evidence_commit != parent:
        fail("materialization receipt must directly follow the evidence-admission event")
    evidence_event = git("rev-list", "--parents", "-n", "1", evidence_commit).split()
    if len(evidence_event) != 2:
        fail("materialization evidence admission must have exactly one parent")
    evidence_parent = evidence_event[1]
    evidence_changed = [line for line in git("diff", "--name-only", evidence_parent, evidence_commit).splitlines() if line]
    if evidence_changed != [MATERIALIZATION_EVIDENCE_REL]:
        fail("materialization evidence admission changed unexpected paths")

    dataset_lock = load_json(DATASET_LOCK_PATH)
    decision = load_json(UNBLINDING_DECISION_PATH)
    evidence = load_json(MATERIALIZATION_EVIDENCE_PATH)
    dataset_lock_evidence = load_json(DATASET_LOCK_EVIDENCE_PATH)
    validate_dataset_lock_receipt_object(dataset_lock)
    validate_unblinding_decision_object(decision, dataset_lock)
    validate_evidence_against_dataset_lock(evidence, dataset_lock_evidence)
    validate_evidence_predecessors(evidence, evidence_parent)

    decision_history = path_history(UNBLINDING_DECISION_REL, evidence_parent)
    decision_commit = decision_history[0]
    decision_bytes = git("show", f"{evidence_parent}:{UNBLINDING_DECISION_REL}").encode("utf-8")
    decision_digest = sha256_bytes(decision_bytes)
    evidence_digest = sha256_file(MATERIALIZATION_EVIDENCE_PATH)
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
    mode.add_argument("--validate-evidence-admission", action="store_true")
    mode.add_argument("--validate-receipt-event", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tooling_only:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_MATERIALIZATION_TOOLING=PASS_ABSENT")
        print("DATASET_LOCK=ESTABLISHED")
        print("UNBLINDING=AUTHORIZED_BOUNDED")
        print("MATERIALIZATION=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("SCIENTIFIC_N_INCREMENT=0")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
        return
    if args.validate_evidence_admission:
        validate_evidence_admission()
        print("TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE=PASS_NONAUTHORIZING")
        print("MATERIALIZATION_RECEIPT=NOT_ESTABLISHED")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("SCIENTIFIC_N_INCREMENT=0")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
        return
    validate_receipt_event()
    print("TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT=PASS_NONAUTHORIZING")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")


if __name__ == "__main__":
    main()
