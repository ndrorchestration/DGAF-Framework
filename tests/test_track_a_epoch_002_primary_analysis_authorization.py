from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"

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


def load_validator():
    assert MODULE_PATH.exists(), "Epoch 002 primary-analysis authorization validator is missing"
    spec = importlib.util.spec_from_file_location(
        "epoch_002_primary_analysis_authorization",
        MODULE_PATH,
    )
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
        "record_id": "E002-MATERIALIZE-RECEIPT-0001",
        "generated_at_utc": "2026-09-16T12:00:00Z",
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_VALIDATOR",
            "version_or_commit": "1" * 40,
        },
        "immutable_subject": {
            "commit_sha": "2" * 40,
            "sha256": "3" * 64,
        },
        "evidence_scope": "DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING",
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
        materialization_receipt_commit_sha="a" * 40,
        materialization_receipt_sha256="b" * 64,
        authorization_parent_sha="c" * 40,
        generated_at_utc="2026-09-16T13:00:00Z",
    )


def validate_fixture(validator, authorization: dict) -> None:
    validator.validate_authorization_object(
        authorization,
        materialization_receipt_fixture(),
        materialization_receipt_commit_sha="a" * 40,
        materialization_receipt_sha256="b" * 64,
        authorization_parent_sha="c" * 40,
    )


def test_authorization_binds_exact_materialization_receipt_and_parent() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)

    validate_fixture(validator, authorization)

    assert authorization["predecessor_record_ids"] == [receipt["record_id"]]
    assert authorization["immutable_subject"] == {
        "commit_sha": "a" * 40,
        "sha256": "b" * 64,
    }
    assert authorization["producer"]["version_or_commit"] == "c" * 40


def test_authorization_scope_is_locked_primary_analysis_only() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)

    assert authorization["record_type"] == "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"
    assert authorization["evidence_scope"] == "LOCKED_PRIMARY_ANALYSIS_ONLY"
    assert authorization["authorization_effect"] == "BOUNDED_RECORD_ONLY"
    assert authorization["non_effects"] == AUTHORIZATION_NON_EFFECTS
    assert authorization["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_authorization_rejects_scope_widening() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["evidence_scope"] = "PRIMARY_AND_EXPLORATORY_ANALYSIS"

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_wrong_materialization_predecessor() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["predecessor_record_ids"] = ["E002-MATERIALIZE-RECEIPT-WRONG"]

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_materialization_content_drift() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["immutable_subject"]["sha256"] = "d" * 64

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_parent_binding_drift() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["producer"]["version_or_commit"] = "d" * 40

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_secret_bearing_extension() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["private_key"] = "must-never-be-admitted"

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_false_independence_or_claim_promotion() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["non_effects"].remove("DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION")

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_frozen_epoch_002_analysis_identities_are_exact() -> None:
    validator = load_validator()

    assert validator.PREREG_BLOB_SHA == "9668ec54e50c40b04d40cfa64b817950df4bbffa"
    assert validator.ANALYSIS_LOCK_BLOB_SHA == "26980e27185b3a77980204b2d46a4fdab7e5fc7e"
    assert validator.ANALYSIS_BLOB_SHA == "d4495f7cdf211b974039ec0e66292dc62ea0881f"
    assert validator.ANALYSIS_CONFIG_SHA256 == "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
    assert validator.REQUIREMENTS_BLOB_SHA == "00c1f779e97030f9b25ae494642edb31b5b09de5"


def test_tooling_mode_preserves_authorization_and_result_absence() -> None:
    validator = load_validator()
    validator.validate_tooling_only()


def test_event_shape_rejects_extra_changed_file(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40

    def fake_git(*args: str) -> str:
        if args[:4] == ("rev-list", "--parents", "-n", "1"):
            return f"{head} {parent}"
        if args[:4] == ("diff-tree", "--no-commit-id", "--name-only", "-r"):
            return f"{validator.AUTH_REL}\nREADME.md"
        if args[:3] == ("log", "--format=%H", "--"):
            return head
        raise AssertionError(f"unexpected git call: {args}")

    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", lambda spec: False)

    with pytest.raises(SystemExit):
        validator.validate_authorization_event_shape(head)


def test_event_shape_rejects_preexisting_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40

    def fake_git(*args: str) -> str:
        if args[:4] == ("rev-list", "--parents", "-n", "1"):
            return f"{head} {parent}"
        if args[:4] == ("diff-tree", "--no-commit-id", "--name-only", "-r"):
            return validator.AUTH_REL
        if args[:3] == ("log", "--format=%H", "--"):
            return head
        raise AssertionError(f"unexpected git call: {args}")

    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", lambda spec: spec == f"{parent}:{validator.AUTH_REL}")

    with pytest.raises(SystemExit):
        validator.validate_authorization_event_shape(head)
