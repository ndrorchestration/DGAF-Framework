from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"
DATASET_LOCK_EVIDENCE_PATH = ROOT / ("docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json")

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


def dataset_lock_evidence_fixture() -> dict:
    return json.loads(DATASET_LOCK_EVIDENCE_PATH.read_text(encoding="utf-8"))


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


def materialization_evidence_fixture() -> dict:
    dataset_lock = dataset_lock_evidence_fixture()
    return {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "operator_execution_receipt_sha256": "0" * 64,
        "evidence_tooling_commit_sha": "d" * 40,
        "materializer_path": "scripts/materialize_track_a_epoch_002_unblinded_input.py",
        "materializer_commit_sha": "e" * 40,
        "materializer_blob_sha": "f" * 40,
        "dataset_lock_record_id": "E002-DATASET-LOCK-A16973BD7AA9E1EB",
        "dataset_lock_commit_sha": "1" * 40,
        "dataset_lock_receipt_sha256": "2" * 64,
        "unblinding_decision_record_id": "E002-UNBLINDING-00112233",
        "unblinding_decision_commit_sha": "3" * 40,
        "unblinding_decision_sha256": "4" * 64,
        "public_artifact": dict(dataset_lock["public_artifact"]),
        "protected_artifact": dict(dataset_lock["protected_artifact"]),
        "materialized_input_sha256": "c" * 64,
        "materialization_manifest_sha256": "d" * 64,
        "materialization_sidecar_sha256": "e" * 64,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "durable_retention": {
            "class": "LOCAL_CUSTODY_ARCHIVE",
            "id": "track-a-epoch-002-materialized-input-content-addressed",
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
        "materialization_evidence_status": ("MATERIALIZATION_PASS_PENDING_REPOSITORY_RECEIPT"),
    }


def valid_receipt(validator, decision: dict, evidence: dict) -> dict:
    return validator.expected_receipt(
        decision,
        evidence,
        unblinding_decision_commit_sha="3" * 40,
        unblinding_decision_sha256="4" * 64,
        evidence_sha256="f" * 64,
        materialization_parent_sha="0" * 40,
        generated_at_utc="2026-09-15T13:00:00Z",
    )


def test_expected_receipt_binds_repository_evidence_and_exact_unblinding_predecessor() -> None:
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
        "commit_sha": "0" * 40,
        "sha256": "f" * 64,
    }
    assert receipt["authorization_effect"] == "REQUIRES_SEPARATE_EXACT_COMMIT"
    assert receipt["non_effects"] == FULL_NON_EFFECTS
    assert receipt["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_evidence_matches_dataset_lock_content_addressed_lineage() -> None:
    validator = load_validator()
    validator.validate_evidence_against_dataset_lock(
        materialization_evidence_fixture(),
        dataset_lock_evidence_fixture(),
    )


def test_evidence_rejects_public_artifact_drift_from_dataset_lock() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["public_artifact"]["archive_sha256"] = "f" * 64
    with pytest.raises(SystemExit):
        validator.validate_evidence_against_dataset_lock(
            evidence,
            dataset_lock_evidence_fixture(),
        )


def test_evidence_rejects_public_artifact_size_drift_from_dataset_lock() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["public_artifact"]["size_bytes"] += 1
    with pytest.raises(SystemExit):
        validator.validate_evidence_against_dataset_lock(
            evidence,
            dataset_lock_evidence_fixture(),
        )


def test_evidence_rejects_protected_artifact_drift_from_dataset_lock() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["protected_artifact"]["custody_certificate_sha256"] = "f" * 64
    with pytest.raises(SystemExit):
        validator.validate_evidence_against_dataset_lock(
            evidence,
            dataset_lock_evidence_fixture(),
        )


def test_evidence_requires_exact_materializer_path() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["materializer_path"] = "scripts/other_materializer.py"
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_evidence_rejects_actions_identity_smuggling() -> None:
    validator = load_validator()
    evidence = materialization_evidence_fixture()
    evidence["evidence_workflow_run_id"] = 9101
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
    receipt["immutable_subject"]["sha256"] = "1" * 64

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


def test_tooling_mode_accepts_established_predecessors_and_preserves_successor_absence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    validator = load_validator()
    monkeypatch.setattr(
        validator,
        "MATERIALIZATION_EVIDENCE_PATH",
        tmp_path / "missing-materialization-evidence.json",
    )
    monkeypatch.setattr(
        validator,
        "MATERIALIZATION_RECEIPT_PATH",
        tmp_path / "missing-materialization-receipt.json",
    )
    monkeypatch.setattr(
        validator,
        "PRIMARY_ANALYSIS_AUTH_PATH",
        tmp_path / "missing-primary-analysis-authorization.json",
    )
    monkeypatch.setattr(
        validator,
        "LOCKED_ANALYSIS_RESULT_PATH",
        tmp_path / "missing-locked-analysis-result.json",
    )
    validator.validate_tooling_only()


def test_tooling_mode_requires_dataset_lock_predecessor(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    validator = load_validator()
    monkeypatch.setattr(validator, "DATASET_LOCK_PATH", tmp_path / "missing-dataset-lock.json")
    with pytest.raises(SystemExit):
        validator.validate_tooling_only()


def test_tooling_mode_requires_unblinding_predecessor(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    validator = load_validator()
    monkeypatch.setattr(
        validator,
        "UNBLINDING_DECISION_PATH",
        tmp_path / "missing-unblinding.json",
    )
    with pytest.raises(SystemExit):
        validator.validate_tooling_only()


def test_cli_rejects_obsolete_external_evidence_arguments() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--validate-receipt-event",
            "--evidence",
            "materialization-evidence.json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "unrecognized arguments" in (result.stdout + result.stderr)
