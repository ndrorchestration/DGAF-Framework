from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_dataset_lock.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_dataset_lock", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def evidence_fixture() -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
        "schema_version": 1,
        "protocol_id": validator.PROTOCOL_ID,
        "epoch": 2,
        "evidence_workflow_run_id": 9001,
        "evidence_tooling_commit_sha": "d" * 40,
        "collection_workflow_run_id": 8001,
        "collection_authorization_commit_sha": "b" * 40,
        "collection_authorization_blob_sha": "9" * 40,
        "frozen_candidate_sha": "a" * 40,
        "frozen_candidate_tree_sha": "e" * 40,
        "custody_receipt_blob_sha": "c" * 40,
        "qc_ledger_record_id": "E002-QC-0001",
        "pre_lock_result_ledger_sha256": "1" * 64,
        "pre_lock_result_ledger_record_count": 53,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_artifact": {
            "artifact_id": 101,
            "name": validator.PUBLIC_ARTIFACT_NAME,
            "size_bytes": 1000,
            "archive_sha256": "2" * 64,
            "manifest_sha256": "3" * 64,
        },
        "protected_artifact": {
            "artifact_id": 102,
            "name": validator.PROTECTED_ARTIFACT_NAME,
            "size_bytes": 2000,
            "archive_sha256": "4" * 64,
            "ciphertext_sha256": "5" * 64,
            "plaintext_tar_sha256": "6" * 64,
            "custody_certificate_sha256": "7" * 64,
            "custody_certificate_public_key_der_sha256": "8" * 64,
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


def write_json_with_sidecar(path: Path, value: object) -> str:
    payload = validator.canonical_json_bytes(value)
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{digest}  {path.name}\n",
        encoding="utf-8",
    )
    return digest


def build_public_root(tmp_path: Path, evidence: dict) -> Path:
    public_root = tmp_path / "track_a_epoch_002_public"
    public_root.mkdir()
    rows = []
    for seed in validator.SEEDS:
        blinded = [f"topology_{index:020x}" for index in range(1, 6)]
        records = []
        for blinded_id in blinded:
            for failure_count in validator.FAILURE_COUNTS:
                records.append(
                    {
                        "protocol_id": validator.PROTOCOL_ID,
                        "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
                        "frozen_candidate_sha": evidence["frozen_candidate_sha"],
                        "seed_id": seed,
                        "blinded_topology_id": blinded_id,
                        "failure_count": failure_count,
                        "ffcr_success": bool((seed + failure_count) % 2),
                        "excluded": False,
                    }
                )
        doc = {
            "record_type": "TRACK_A_EPOCH_002_BLINDED_SEED_DATASET",
            "schema_version": 1,
            "protocol_id": validator.PROTOCOL_ID,
            "seed_id": seed,
            "records": records,
            "environment_fingerprint": {"python": "3.12.0"},
            "runtime_seconds": 1.0,
            "outcomes_inspected_by_collection_workflow": False,
            "unblinding_authorized": False,
            "primary_analysis_authorized": False,
        }
        path = public_root / f"track_a_epoch_002_seed_{seed}.json"
        public_digest = write_json_with_sidecar(path, doc)
        rows.append(
            {
                "seed_id": seed,
                "public_dataset_sha256": public_digest,
                "protected_mapping_sha256": f"{seed:064x}"[-64:],
                "record_count": 45,
            }
        )
    manifest = {
        "record_type": "TRACK_A_EPOCH_002_BLINDED_COLLECTION_MANIFEST",
        "schema_version": 1,
        "protocol_id": validator.PROTOCOL_ID,
        "frozen_candidate_sha": evidence["frozen_candidate_sha"],
        "seed_count": 50,
        "expected_observations": 2250,
        "custody_receipt_blob_sha": evidence["custody_receipt_blob_sha"],
        "custody_certificate_sha256": evidence["protected_artifact"]["custody_certificate_sha256"],
        "custody_certificate_public_key_der_sha256": evidence["protected_artifact"][
            "custody_certificate_public_key_der_sha256"
        ],
        "rows": rows,
        "outcomes_inspected_by_collection_workflow": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
    }
    manifest_path = public_root / "track_a_epoch_002_manifest.json"
    evidence["public_artifact"]["manifest_sha256"] = write_json_with_sidecar(
        manifest_path,
        manifest,
    )
    return public_root


def test_evidence_schema_is_valid_json_schema() -> None:
    schema = json.loads(validator.EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)


def test_valid_evidence_contract_passes() -> None:
    validator.validate_evidence_object(evidence_fixture())


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("paired_seed_units",), 49),
        (("blinded_observations",), 2249),
        (("independent_custody",), True),
        (("outcomes_inspected_for_lock",), True),
        (("outcome_aggregation_performed",), True),
        (("unblinding_authorized",), True),
        (("primary_analysis_authorized",), True),
        (("scientific_n_increment",), 1),
        (("canonical_dgaf_efficacy",), "ESTABLISHED"),
        (("structural_qc", "protected_plaintext_not_decrypted"), False),
        (("structural_qc", "protected_mapping_not_inspected"), False),
        (("structural_qc", "private_key_not_used"), False),
    ],
)
def test_evidence_promotions_fail_closed(path: tuple[str, ...], value: object) -> None:
    evidence = evidence_fixture()
    target = evidence
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    with pytest.raises(SystemExit):
        validator.validate_evidence_object(evidence)


def test_public_and_protected_artifact_ids_must_be_distinct() -> None:
    evidence = evidence_fixture()
    evidence["protected_artifact"]["artifact_id"] = evidence["public_artifact"]["artifact_id"]
    with pytest.raises(SystemExit, match="distinct artifact IDs"):
        validator.validate_evidence_object(evidence)


def test_receipt_binds_content_addressed_evidence_and_qc_predecessor() -> None:
    evidence = evidence_fixture()
    digest = "e" * 64
    receipt = validator.expected_receipt(
        evidence,
        digest,
        evidence_artifact_id=303,
        generated_at_utc="2026-09-11T02:00:00Z",
    )
    validator.validate_receipt_object(receipt, evidence, digest)
    assert receipt["immutable_subject"] == {
        "commit_sha": evidence["collection_authorization_commit_sha"],
        "workflow_run_id": evidence["evidence_workflow_run_id"],
        "artifact_id": 303,
        "sha256": digest,
    }
    assert receipt["predecessor_record_ids"] == [evidence["qc_ledger_record_id"]]
    assert receipt["authorization_effect"] == "REQUIRES_SEPARATE_EXACT_COMMIT"
    assert receipt["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_receipt_digest_drift_is_rejected() -> None:
    evidence = evidence_fixture()
    digest = "e" * 64
    receipt = validator.expected_receipt(
        evidence,
        digest,
        evidence_artifact_id=303,
        generated_at_utc="2026-09-11T02:00:00Z",
    )
    receipt["immutable_subject"]["sha256"] = "f" * 64
    with pytest.raises(SystemExit):
        validator.validate_receipt_object(receipt, evidence, digest)


def test_receipt_wrong_predecessor_is_rejected() -> None:
    evidence = evidence_fixture()
    digest = "e" * 64
    receipt = validator.expected_receipt(
        evidence,
        digest,
        evidence_artifact_id=303,
        generated_at_utc="2026-09-11T02:00:00Z",
    )
    receipt["predecessor_record_ids"] = ["E002-QC-WRONG"]
    with pytest.raises(SystemExit):
        validator.validate_receipt_object(receipt, evidence, digest)


def test_receipt_cannot_promote_unblinding_authority() -> None:
    evidence = evidence_fixture()
    digest = "e" * 64
    receipt = validator.expected_receipt(
        evidence,
        digest,
        evidence_artifact_id=303,
        generated_at_utc="2026-09-11T02:00:00Z",
    )
    receipt["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    with pytest.raises(SystemExit):
        validator.validate_receipt_object(receipt, evidence, digest)


def test_public_retained_structure_validates_without_outcome_aggregation(
    tmp_path: Path,
) -> None:
    evidence = evidence_fixture()
    public_root = build_public_root(tmp_path, evidence)
    validator.validate_public_root(public_root, evidence)


def test_public_manifest_outcome_inspection_claim_fails_closed(tmp_path: Path) -> None:
    evidence = evidence_fixture()
    public_root = build_public_root(tmp_path, evidence)
    manifest_path = public_root / "track_a_epoch_002_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["outcomes_inspected_by_collection_workflow"] = True
    evidence["public_artifact"]["manifest_sha256"] = write_json_with_sidecar(
        manifest_path,
        manifest,
    )
    with pytest.raises(SystemExit, match="outcomes_inspected"):
        validator.validate_public_root(public_root, evidence)


def test_flat_member_set_rejects_nested_directory(tmp_path: Path) -> None:
    root = tmp_path / "artifact"
    root.mkdir()
    (root / "unexpected").mkdir()
    with pytest.raises(SystemExit, match="non-regular top-level members"):
        validator._validate_flat_member_set(root, set(), "public")


def test_tooling_source_has_no_empirical_or_secret_writer_surface() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "--write" not in source
    assert "--execute" not in source
    assert "PDMAL_TOPOLOGY_BLINDING_KEY" not in source
    assert "PRIVATE_KEY" not in source
    assert "PASSPHRASE" not in source
