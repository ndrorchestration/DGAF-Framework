from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_unblinding_decision.py"

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
    assert MODULE_PATH.exists(), "Epoch 002 unblinding-decision validator is missing"
    spec = importlib.util.spec_from_file_location("epoch_002_unblinding_decision", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dataset_lock_receipt_fixture() -> dict:
    return {
        "record_type": "DATASET_LOCK_RECEIPT",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": "E002-DATASET-LOCK-00112233",
        "generated_at_utc": "2026-09-11T02:00:00Z",
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_DATASET_LOCK_VALIDATOR",
            "version_or_commit": "a" * 40,
        },
        "immutable_subject": {
            "commit_sha": "b" * 40,
            "workflow_run_id": 9001,
            "artifact_id": 9002,
            "sha256": "c" * 64,
        },
        "evidence_scope": "CONTENT_ADDRESSED_EPOCH_002_BLINDED_DATASET_LOCK_BEFORE_UNBLINDING",
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": ["E002-QC-0001"],
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def valid_decision(validator, dataset_lock: dict) -> dict:
    return validator.expected_decision(
        dataset_lock,
        dataset_lock_commit_sha="d" * 40,
        dataset_lock_receipt_sha256="e" * 64,
        authorization_parent_sha="f" * 40,
        generated_at_utc="2026-09-11T04:00:00Z",
    )


def test_expected_decision_binds_exact_dataset_lock_and_preserves_ceiling() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)

    validator.validate_decision_object(
        decision,
        dataset_lock,
        dataset_lock_commit_sha="d" * 40,
        dataset_lock_receipt_sha256="e" * 64,
        authorization_parent_sha="f" * 40,
    )

    assert decision["record_type"] == "UNBLINDING_DECISION_RECORD"
    assert decision["predecessor_record_ids"] == [dataset_lock["record_id"]]
    assert decision["immutable_subject"] == {
        "commit_sha": "d" * 40,
        "sha256": "e" * 64,
    }
    assert decision["producer"] == {
        "system": "DGAF_TRACK_A_EPOCH_002_UNBLINDING_DECISION_VALIDATOR",
        "version_or_commit": "f" * 40,
    }
    assert decision["authorization_effect"] == "BOUNDED_RECORD_ONLY"
    assert decision["non_effects"] == UNBLINDING_NON_EFFECTS
    assert decision["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_dataset_lock_must_be_pass() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    dataset_lock["status"] = "FAIL"
    with pytest.raises(SystemExit):
        validator.validate_dataset_lock_receipt_object(dataset_lock)


def test_dataset_lock_must_require_separate_exact_commit() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    dataset_lock["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    with pytest.raises(SystemExit):
        validator.validate_dataset_lock_receipt_object(dataset_lock)


def test_decision_rejects_wrong_dataset_lock_predecessor() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["predecessor_record_ids"] = ["E002-DATASET-LOCK-WRONG"]

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_decision_cannot_claim_primary_analysis_authority() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["non_effects"].remove("DOES_NOT_AUTHORIZE_ANALYSIS")

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_decision_must_not_deny_its_bounded_unblinding_authority() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["non_effects"].append("DOES_NOT_AUTHORIZE_UNBLINDING")

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_decision_rejects_dataset_lock_digest_drift() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["immutable_subject"]["sha256"] = "0" * 64

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_decision_rejects_scientific_n_promotion() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["scientific_state_effect"]["empirical_n_increment"] = 1

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_decision_rejects_secret_like_record_id_drift() -> None:
    validator = load_validator()
    dataset_lock = dataset_lock_receipt_fixture()
    decision = valid_decision(validator, dataset_lock)
    decision["record_id"] = "PRIVATE_KEY_SECRET_MATERIAL"

    with pytest.raises(SystemExit):
        validator.validate_decision_object(
            decision,
            dataset_lock,
            dataset_lock_commit_sha="d" * 40,
            dataset_lock_receipt_sha256="e" * 64,
            authorization_parent_sha="f" * 40,
        )


def test_tooling_mode_preserves_absence_and_semantic_boundary() -> None:
    validator = load_validator()
    validator.validate_tooling_only()
