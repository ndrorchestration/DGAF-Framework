from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"
ANALYSIS_LOCK_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"

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
    effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_ANALYSIS"
]


def load_validator():
    assert MODULE_PATH.exists(), "Epoch 002 primary-analysis authorization validator is missing"
    spec = importlib.util.spec_from_file_location("epoch_002_primary_auth", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def materialization_receipt_fixture() -> dict:
    return {
        "record_type": "MATERIALIZATION_RECEIPT",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": "E002-MATERIALIZE-0011223344556677",
        "generated_at_utc": "2026-09-16T06:00:00Z",
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_VALIDATOR",
            "version_or_commit": "1" * 40,
        },
        "immutable_subject": {
            "commit_sha": "1" * 40,
            "sha256": "2" * 64,
        },
        "evidence_scope": (
            "DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING"
        ),
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": ["E002-UNBLINDING-00112233"],
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def valid_authorization(validator) -> dict:
    return validator.expected_authorization(
        materialization_receipt_fixture(),
        materialization_receipt_commit_sha="3" * 40,
        materialization_receipt_sha256="4" * 64,
        authorization_parent_sha="5" * 40,
        authorization_parent_tree_sha="6" * 40,
        generated_at_utc="2026-09-16T07:00:00Z",
    )


def test_authorization_binds_materialization_receipt_and_locked_scope() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)

    validator.validate_authorization_object(
        authorization,
        receipt,
        materialization_receipt_commit_sha="3" * 40,
        materialization_receipt_sha256="4" * 64,
        authorization_parent_sha="5" * 40,
        authorization_parent_tree_sha="6" * 40,
    )

    assert authorization["record_type"] == "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"
    assert authorization["evidence_scope"] == "LOCKED_PRIMARY_ANALYSIS_ONLY"
    assert authorization["predecessor_record_ids"] == [receipt["record_id"]]
    assert authorization["authorization_effect"] == "BOUNDED_RECORD_ONLY"
    assert authorization["non_effects"] == AUTH_NON_EFFECTS
    assert authorization["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    assert authorization["immutable_subject"] == {
        "commit_sha": "3" * 40,
        "tree_sha": "6" * 40,
        "sha256": "4" * 64,
    }


def test_authorization_rejects_scope_widening() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)
    authorization["evidence_scope"] = "LOCKED_PRIMARY_PLUS_EXPLORATORY_ANALYSIS"

    with pytest.raises(SystemExit):
        validator.validate_authorization_object(
            authorization,
            receipt,
            materialization_receipt_commit_sha="3" * 40,
            materialization_receipt_sha256="4" * 64,
            authorization_parent_sha="5" * 40,
            authorization_parent_tree_sha="6" * 40,
        )


def test_authorization_rejects_false_analysis_non_effect() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)
    authorization["non_effects"].append("DOES_NOT_AUTHORIZE_ANALYSIS")

    with pytest.raises(SystemExit):
        validator.validate_authorization_object(
            authorization,
            receipt,
            materialization_receipt_commit_sha="3" * 40,
            materialization_receipt_sha256="4" * 64,
            authorization_parent_sha="5" * 40,
            authorization_parent_tree_sha="6" * 40,
        )


def test_authorization_rejects_predecessor_drift() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)
    authorization["predecessor_record_ids"] = ["E002-MATERIALIZE-WRONG"]

    with pytest.raises(SystemExit):
        validator.validate_authorization_object(
            authorization,
            receipt,
            materialization_receipt_commit_sha="3" * 40,
            materialization_receipt_sha256="4" * 64,
            authorization_parent_sha="5" * 40,
            authorization_parent_tree_sha="6" * 40,
        )


def test_authorization_rejects_receipt_content_drift() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)
    authorization["immutable_subject"]["sha256"] = "7" * 64

    with pytest.raises(SystemExit):
        validator.validate_authorization_object(
            authorization,
            receipt,
            materialization_receipt_commit_sha="3" * 40,
            materialization_receipt_sha256="4" * 64,
            authorization_parent_sha="5" * 40,
            authorization_parent_tree_sha="6" * 40,
        )


def test_analysis_lock_rejects_analysis_identity_drift() -> None:
    validator = load_validator()
    analysis_lock = json.loads(ANALYSIS_LOCK_PATH.read_text(encoding="utf-8"))
    analysis_lock["analysis_blob_sha"] = "7" * 40

    with pytest.raises(SystemExit):
        validator.validate_analysis_lock_object(analysis_lock)


def test_event_shape_rejects_extra_changed_file() -> None:
    validator = load_validator()
    with pytest.raises(SystemExit):
        validator.validate_event_shape(
            parent_count=1,
            changed_files=[validator.AUTH_REL, "docs/experiment/extra.json"],
            authorization_existed_at_parent=False,
            authorization_history=["a" * 40],
            head_sha="a" * 40,
            locked_result_exists_at_parent=False,
            locked_result_exists_at_head=False,
        )


def test_event_shape_rejects_preexisting_result() -> None:
    validator = load_validator()
    with pytest.raises(SystemExit):
        validator.validate_event_shape(
            parent_count=1,
            changed_files=[validator.AUTH_REL],
            authorization_existed_at_parent=False,
            authorization_history=["a" * 40],
            head_sha="a" * 40,
            locked_result_exists_at_parent=True,
            locked_result_exists_at_head=True,
        )


def test_tooling_mode_preserves_authorization_and_result_absence() -> None:
    validator = load_validator()
    validator.validate_tooling_only()
