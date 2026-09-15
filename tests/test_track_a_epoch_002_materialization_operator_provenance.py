from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"
DATASET_LOCK_EVIDENCE_PATH = ROOT / (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json"
)

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
UNBLINDING_NON_EFFECTS = [
    effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_UNBLINDING"
]


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "epoch_002_materialization_operator_provenance",
        MODULE_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unblinding_decision_fixture() -> dict:
    return {
        "record_type": "UNBLINDING_DECISION_RECORD",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": "E002-UNBLINDING-00112233",
        "generated_at_utc": "2026-09-15T12:00:00Z",
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_UNBLINDING_DECISION_VALIDATOR",
            "version_or_commit": "a" * 40,
        },
        "immutable_subject": {
            "commit_sha": "b" * 40,
            "sha256": "c" * 64,
        },
        "evidence_scope": "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY",
        "non_effects": list(UNBLINDING_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": ["E002-DATASET-LOCK-A16973BD7AA9E1EB"],
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def operator_materialization_evidence_fixture(dataset_lock: dict) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "operator_execution_receipt_sha256": "1" * 64,
        "evidence_tooling_commit_sha": "2" * 40,
        "materializer_path": "scripts/materialize_track_a_epoch_002_unblinded_input.py",
        "materializer_commit_sha": "3" * 40,
        "materializer_blob_sha": "4" * 40,
        "dataset_lock_record_id": "E002-DATASET-LOCK-A16973BD7AA9E1EB",
        "dataset_lock_commit_sha": "e7ba2fe6fc6b3587957c59231da81ae107cacab2",
        "dataset_lock_receipt_sha256": "5" * 64,
        "unblinding_decision_record_id": "E002-UNBLINDING-00112233",
        "unblinding_decision_commit_sha": "bf6279b9989f211e324ff3e9012788bed95e5c84",
        "unblinding_decision_sha256": "6" * 64,
        "public_artifact": dict(dataset_lock["public_artifact"]),
        "protected_artifact": dict(dataset_lock["protected_artifact"]),
        "materialized_input_sha256": "7" * 64,
        "materialization_manifest_sha256": "8" * 64,
        "materialization_sidecar_sha256": "9" * 64,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "durable_retention": {
            "class": "LOCAL_CUSTODY_ARCHIVE",
            "id": "epoch002-materialization-evidence-content-addressed",
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "secret_material_persisted": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "historical_pooling_allowed": False,
        "epoch_001_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "materialization_evidence_status": (
            "MATERIALIZATION_PASS_PENDING_REPOSITORY_RECEIPT"
        ),
    }


def test_operator_materialization_evidence_matches_accepted_dataset_lock_without_actions_ids() -> None:
    validator = load_validator()
    dataset_lock = json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    evidence = operator_materialization_evidence_fixture(dataset_lock)

    validator.validate_evidence_against_dataset_lock(evidence, dataset_lock)


def test_operator_materialization_evidence_rejects_actions_identity_smuggling() -> None:
    validator = load_validator()
    dataset_lock = json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    evidence = operator_materialization_evidence_fixture(dataset_lock)
    evidence["evidence_workflow_run_id"] = 123
    evidence["evidence_artifact_id"] = 456
    evidence["public_artifact"]["artifact_id"] = 789

    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_operator_materialization_evidence_rejects_source_size_drift() -> None:
    validator = load_validator()
    dataset_lock = json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    evidence = operator_materialization_evidence_fixture(dataset_lock)
    evidence["public_artifact"]["size_bytes"] += 1

    with pytest.raises(SystemExit):
        validator.validate_evidence_against_dataset_lock(evidence, dataset_lock)


def test_operator_receipt_binds_repository_evidence_commit_and_digest_only() -> None:
    validator = load_validator()
    dataset_lock = json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))
    decision = unblinding_decision_fixture()
    evidence = operator_materialization_evidence_fixture(dataset_lock)
    parent = "a" * 40
    evidence_digest = "f" * 64

    receipt = validator.expected_receipt(
        decision,
        evidence,
        unblinding_decision_commit_sha=evidence["unblinding_decision_commit_sha"],
        unblinding_decision_sha256=evidence["unblinding_decision_sha256"],
        evidence_sha256=evidence_digest,
        materialization_parent_sha=parent,
        generated_at_utc="2026-09-15T13:00:00Z",
    )

    assert receipt["immutable_subject"] == {
        "commit_sha": parent,
        "sha256": evidence_digest,
    }
