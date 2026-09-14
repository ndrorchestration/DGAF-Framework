from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_dataset_lock.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_dataset_lock_operator_handoff", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def operator_evidence_fixture() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
        "schema_version": 1,
        "protocol_id": validator.PROTOCOL_ID,
        "epoch": 2,
        "evidence_workflow_run_id": 9001,
        "evidence_tooling_commit_sha": "d" * 40,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "operator_admission_record_sha256": "0" * 64,
        "collection_execution_receipt_sha256": "1" * 64,
        "collection_authorization_commit_sha": "b" * 40,
        "collection_authorization_blob_sha": "9" * 40,
        "frozen_candidate_sha": "a" * 40,
        "frozen_candidate_tree_sha": "e" * 40,
        "custody_receipt_blob_sha": "c" * 40,
        "qc_ledger_record_id": "E002-QC-0001",
        "pre_lock_result_ledger_sha256": "2" * 64,
        "pre_lock_result_ledger_record_count": 53,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_artifact": {
            "name": validator.PUBLIC_ARTIFACT_NAME,
            "size_bytes": 1000,
            "archive_sha256": "3" * 64,
            "manifest_sha256": "4" * 64,
        },
        "protected_artifact": {
            "name": validator.PROTECTED_ARTIFACT_NAME,
            "size_bytes": 2000,
            "archive_sha256": "5" * 64,
            "ciphertext_sha256": "6" * 64,
            "plaintext_tar_sha256": "7" * 64,
            "custody_certificate_sha256": "8" * 64,
            "custody_certificate_public_key_der_sha256": "9" * 64,
        },
        "structural_qc": {
            "public_archive_digest_verified": True,
            "protected_archive_digest_verified": True,
            "all_public_sidecars_verified": True,
            "whole_epoch_manifest_verified": True,
            "exact_seed_panel_verified": True,
            "exact_matrix_counts_verified": True,
            "public_schema_allowlist_verified": True,
            "protected_ciphertext_digest_verified": True,
            "protected_plaintext_not_decrypted": True,
            "protected_mapping_not_inspected": True,
            "private_key_not_used": True,
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
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


def test_operator_codespace_evidence_contract_passes_without_actions_ids() -> None:
    validator.validate_evidence_object(operator_evidence_fixture())


def test_operator_codespace_rejects_collection_workflow_run_id() -> None:
    evidence = operator_evidence_fixture()
    evidence["collection_workflow_run_id"] = 8001
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_operator_codespace_rejects_actions_artifact_ids() -> None:
    evidence = operator_evidence_fixture()
    evidence["public_artifact"]["artifact_id"] = 101
    evidence["protected_artifact"]["artifact_id"] = 102
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)
