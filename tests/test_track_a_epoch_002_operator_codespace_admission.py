from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_operator_collection_admission.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_operator_admission", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def operator_admission_fixture() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": validator.AUTHORIZATION_SHA,
        "frozen_candidate_sha": "7bbd97604d82efada43d0b139901f06eb2582a23",
        "frozen_candidate_tree_sha": "d6c4e94586551880d657ae3464043a08bfc5d8e1",
        "python_version": "3.12.3",
        "requirements_lock_blob_sha": "00c1f779e97030f9b25ae494642edb31b5b09de5",
        "collection_execution_receipt_sha256": "0" * 64,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_retention": {
            "name": "track-a-epoch-002-public-blinded",
            "size_bytes": 1000,
            "archive_sha256": "2" * 64,
            "manifest_sha256": "3" * 64,
        },
        "protected_retention": {
            "name": "track-a-epoch-002-protected-encrypted",
            "size_bytes": 2000,
            "archive_sha256": "4" * 64,
            "ciphertext_sha256": "5" * 64,
            "plaintext_tar_sha256": "6" * 64,
            "custody_certificate_sha256": "5d14c89c20e0d22586045dea9fbb5de9a7ec6e7bbe7be4cd5b4da3ce9693db4e",
            "custody_certificate_public_key_der_sha256": "53d0b2a95b2634ef7011b808657e693df426dcaecf8ad70c8094be20d37c4f08",
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "outcomes_inspected_for_admission": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "admission_status": "CONTENT_ADDRESSED_PENDING_DATASET_LOCK",
    }


def execution_receipt_fixture() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_EXECUTION_RECEIPT",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": validator.AUTHORIZATION_SHA,
        "frozen_candidate_sha": "7bbd97604d82efada43d0b139901f06eb2582a23",
        "frozen_candidate_tree_sha": "d6c4e94586551880d657ae3464043a08bfc5d8e1",
        "python_version": "3.12.3",
        "requirements_lock_blob_sha": "00c1f779e97030f9b25ae494642edb31b5b09de5",
        "completion_status": "COMPLETE",
        "runner_terminal_result": "TRACK_A_EPOCH_002_COLLECTION_COMPLETE: 50 seeds; 2250 observations",
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "outcomes_inspected_for_receipt": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_tar(path: Path, members: dict[str, bytes]) -> None:
    with tarfile.open(path, "w") as archive:
        for name, data in members.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


def test_operator_codespace_record_is_accepted_without_actions_ids() -> None:
    validator.validate_record(operator_admission_fixture())


def test_operator_codespace_record_rejects_actions_identity_smuggling() -> None:
    record = operator_admission_fixture()
    record["collection_workflow_run_id"] = 8001
    with pytest.raises(SystemExit):
        validator.validate_record(record)


def test_operator_codespace_record_requires_execution_receipt_digest() -> None:
    record = operator_admission_fixture()
    record.pop("collection_execution_receipt_sha256")
    with pytest.raises(SystemExit):
        validator.validate_record(record)


def test_operator_codespace_record_rejects_authority_promotion() -> None:
    record = operator_admission_fixture()
    record["unblinding_authorized"] = True
    with pytest.raises(SystemExit):
        validator.validate_record(record)


def test_operator_codespace_record_rejects_authorization_drift() -> None:
    record = operator_admission_fixture()
    record["collection_authorization_commit_sha"] = "f" * 40
    with pytest.raises(SystemExit):
        validator.validate_record(record)


def test_schema_only_is_explicitly_non_admitting() -> None:
    assert validator.schema_only_status() == "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=NOT_ADMITTED_SCHEMA_ONLY"


def test_receipt_bytes_are_hashed_and_cross_bound(tmp_path: Path) -> None:
    record = operator_admission_fixture()
    receipt = execution_receipt_fixture()
    receipt_path = tmp_path / "receipt.json"
    write_json(receipt_path, receipt)
    record["collection_execution_receipt_sha256"] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    validator.validate_execution_receipt(record, receipt_path)
    receipt["python_version"] = "3.14.2"
    write_json(receipt_path, receipt)
    with pytest.raises(SystemExit):
        validator.validate_execution_receipt(record, receipt_path)


def test_record_rejects_valid_format_wrong_candidate() -> None:
    record = operator_admission_fixture()
    record["frozen_candidate_sha"] = "f" * 40
    with pytest.raises(SystemExit):
        validator.validate_record(record)


def test_protected_archive_rejects_forbidden_member(tmp_path: Path) -> None:
    archive = tmp_path / "protected.tar"
    write_tar(archive, {"./forbidden_plaintext_mapping.json": b"{}"})
    with pytest.raises(SystemExit):
        validator.validate_protected_archive_members(archive, operator_admission_fixture())


def test_public_archive_rejects_forbidden_member(tmp_path: Path) -> None:
    archive = tmp_path / "public.tar"
    write_tar(archive, {"./unexpected.txt": b"x"})
    with pytest.raises(SystemExit):
        validator.validate_public_archive_members(archive, operator_admission_fixture())


def test_evidence_acceptance_requires_receipt_and_both_archives(tmp_path: Path) -> None:
    record = operator_admission_fixture()
    receipt_path = tmp_path / "receipt.json"
    write_json(receipt_path, execution_receipt_fixture())
    with pytest.raises(SystemExit):
        validator.validate_evidence_acceptance(record, receipt_path, None, None)
