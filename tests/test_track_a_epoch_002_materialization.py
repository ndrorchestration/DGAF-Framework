from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"

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


def load_validator():
    assert MODULE_PATH.exists(), "Epoch 002 materialization validator is missing"
    spec = importlib.util.spec_from_file_location("epoch_002_materialization", MODULE_PATH)
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
        "generated_at_utc": "2026-09-11T04:00:00Z",
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
        "predecessor_record_ids": ["E002-DATASET-LOCK-00112233"],
        "authorization_effect": "BOUNDED_RECORD_ONLY",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def materialization_evidence_fixture() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "evidence_workflow_run_id": 9101,
        "evidence_artifact_id": 9102,
        "evidence_tooling_commit_sha": "d" * 40,
        "materializer_path": "scripts/materialize_track_a_epoch_002_unblinded_input.py",
        "materializer_commit_sha": "e" * 40,
        "materializer_blob_sha": "f" * 40,
        "dataset_lock_record_id": "E002-DATASET-LOCK-00112233",
        "dataset_lock_commit_sha": "1" * 40,
        "dataset_lock_receipt_sha256": "2" * 64,
        "unblinding_decision_record_id": "E002-UNBLINDING-00112233",
        "unblinding_decision_commit_sha": "3" * 40,
        "unblinding_decision_sha256": "4" * 64,
        "public_artifact": {
            "artifact_id": 9201,
            "name": "track-a-epoch-002-public-blinded",
            "archive_sha256": "5" * 64,
            "manifest_sha256": "6" * 64,
        },
        "protected_artifact": {
            "artifact_id": 9202,
            "name": "track-a-epoch-002-protected-encrypted",
            "archive_sha256": "7" * 64,
            "ciphertext_sha256": "8" * 64,
            "plaintext_tar_sha256": "9" * 64,
            "custody_certificate_sha256": "a" * 64,
            "custody_certificate_public_key_der_sha256": "b" * 64,
        },
        "materialized_input_sha256": "c" * 64,
        "materialization_manifest_sha256": "d" * 64,
        "materialization_sidecar_sha256": "e" * 64,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "durable_retention": {
            "class": "GITHUB_ACTIONS_ARTIFACT",
            "id": "track-a-epoch-002-materialized-input-9103",
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
        "materialization_evidence_status": "MATERIALIZATION_PASS_PENDING_REPOSITORY_RECEIPT",
    }


def valid_receipt(validator, decision: dict, evidence: dict) -> dict:
    return validator.expected_receipt(
        decision,
        evidence,
        unblinding_decision_commit_sha="3" * 40,
        unblinding_decision_sha256="4" * 64,
        evidence_sha256="f" * 64,
        materialization_parent_sha="0" * 40,
        generated_at_utc="2026-09-11T05:00:00Z",
    )


def test_expected_receipt_binds_evidence_and_exact_unblinding_predecessor() -> None:
    validator = load_validator()
    decision = unblinding_decision_fixture()
    evidence = materialization_evidence_fixture()
    receipt = valid_receipt(validator, decision, evidence)

    validator.validate_receipt_object(
        receipt,
        decision,
        evidence,
        unblinding_decision_commit_sha="3" * 40,
        unblinding_decision_sha256="4" * 64,
        evidence_sha256="f" * 64,
        materialization_parent_sha="0" * 40,
    )

    assert receipt["record_type"] == "MATERIALIZATION_RECEIPT"
    assert receipt["predecessor_record_ids"] == [decision["record_id"]]
    assert receipt["immutable_subject"] == {
        "commit_sha": "3" * 40,
        "workflow_run_id": 9101,
        "artifact_id": 9102,
        "sha256": "f" * 64,
    }
    assert receipt["authorization_effect"] == "REQUIRES_SEPARATE_EXACT_COMMIT"
    assert receipt["non_effects"] == FULL_NON_EFFECTS
    assert receipt["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_evidence_requires_exact_materializer_path() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["materializer_path"] = "scripts/other_materializer.py"
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_evidence_rejects_primary_analysis_authority() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["primary_analysis_authorized"] = True
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_evidence_rejects_outcome_aggregation() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["outcome_aggregation_performed"] = True
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_evidence_rejects_independent_custody_promotion() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["independent_custody"] = True
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_evidence_rejects_historical_pooling() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["epoch_001_pooling_allowed"] = True
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_receipt_rejects_evidence_digest_drift() -> None:
    validator = load_validator()
    decision = unblinding_decision_fixture()
    evidence = materialization_evidence_fixture()
    receipt = valid_receipt(validator, decision, evidence)
    receipt["immutable_subject"]["sha256"] = "0" * 64

    with pytest.raises(SystemExit):
        validator.validate_receipt_object(
            receipt,
            decision,
            evidence,
            unblinding_decision_commit_sha="3" * 40,
            unblinding_decision_sha256="4" * 64,
            evidence_sha256="f" * 64,
            materialization_parent_sha="0" * 40,
        )


def test_receipt_rejects_wrong_unblinding_predecessor() -> None:
    validator = load_validator()
    decision = unblinding_decision_fixture()
    evidence = materialization_evidence_fixture()
    receipt = valid_receipt(validator, decision, evidence)
    receipt["predecessor_record_ids"] = ["E002-UNBLINDING-WRONG"]

    with pytest.raises(SystemExit):
        validator.validate_receipt_object(
            receipt,
            decision,
            evidence,
            unblinding_decision_commit_sha="3" * 40,
            unblinding_decision_sha256="4" * 64,
            evidence_sha256="f" * 64,
            materialization_parent_sha="0" * 40,
        )


def test_receipt_cannot_authorize_primary_analysis() -> None:
    validator = load_validator()
    decision = unblinding_decision_fixture()
    evidence = materialization_evidence_fixture()
    receipt = valid_receipt(validator, decision, evidence)
    receipt["non_effects"].remove("DOES_NOT_AUTHORIZE_ANALYSIS")

    with pytest.raises(SystemExit):
        validator.validate_receipt_object(
            receipt,
            decision,
            evidence,
            unblinding_decision_commit_sha="3" * 40,
            unblinding_decision_sha256="4" * 64,
            evidence_sha256="f" * 64,
            materialization_parent_sha="0" * 40,
        )


def test_tooling_mode_preserves_absence_and_semantic_boundary() -> None:
    validator = load_validator()
    validator.validate_tooling_only()
