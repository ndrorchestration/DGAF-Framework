from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from scripts import validate_track_a_epoch_002_dataset_lock as lock

ALL_NON_EFFECTS = {
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
}


def record(
    record_type: str,
    record_id: str,
    *,
    predecessors: list[str] | None = None,
    status: str = "PASS",
    effect: str = "NONE",
    non_effects: set[str] | None = None,
) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": record_id,
        "generated_at_utc": "2026-09-10T00:00:00Z",
        "producer": {"system": "dataset-lock-test", "version_or_commit": "8414219"},
        "immutable_subject": {"commit_sha": "a" * 40},
        "evidence_scope": "prospective dataset-lock test only",
        "non_effects": sorted(non_effects if non_effects is not None else ALL_NON_EFFECTS),
        "status": status,
        "predecessor_record_ids": predecessors or [],
        "authorization_effect": effect,
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def completed_prefix() -> list[dict[str, Any]]:
    records = [record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001")]
    records.append(
        record(
            "COLLECTION_START_RECEIPT",
            "E002-START-0001",
            predecessors=[records[-1]["record_id"]],
        )
    )
    for seed_index in range(50):
        records.append(
            record(
                "PER_SEED_EXECUTION_RECORD",
                f"E002-SEED-{seed_index + 1:04d}",
                predecessors=[records[-1]["record_id"]],
            )
        )
    records.append(record("QC_LEDGER", "E002-QC-0001", predecessors=[records[-1]["record_id"]]))
    return records


def lock_record(qc_id: str = "E002-QC-0001") -> dict[str, Any]:
    return record(
        "DATASET_LOCK_RECEIPT",
        "E002-LOCK-0001",
        predecessors=[qc_id],
        effect="REQUIRES_SEPARATE_EXACT_COMMIT",
    )


def evidence_manifest() -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "collection_authorization": {
            "commit_sha": "1" * 40,
            "blob_sha": "2" * 40,
            "frozen_candidate_sha": "3" * 40,
            "frozen_candidate_tree_sha": "4" * 40,
        },
        "collection_run": {"workflow_run_id": 101, "job_id": 102},
        "public_artifact": {
            "artifact_id": 201,
            "name": "synthetic-public-blinded",
            "size_bytes": 1234,
            "archive_sha256": "5" * 64,
            "whole_epoch_manifest_sha256": "6" * 64,
        },
        "protected_artifact": {
            "artifact_id": 301,
            "name": "synthetic-protected-encrypted",
            "size_bytes": 5678,
            "archive_sha256": "7" * 64,
            "ciphertext_sha256": "8" * 64,
            "plaintext_tar_sha256": "9" * 64,
        },
        "custody": {
            "class": "SAME_SYSTEM_NONINDEPENDENT",
            "certificate_sha256": "a" * 64,
            "certificate_public_key_der_sha256": "b" * 64,
        },
        "dataset_shape": {"paired_seed_units": 50, "blinded_observations": 2250},
        "structural_qc": {
            "per_seed_sidecars": "PASS",
            "complete_matrix": "PASS",
            "outcome_values_inspected": False,
            "outcome_aggregation_performed": False,
        },
        "authorization_state": {
            "unblinding_authorized": False,
            "primary_analysis_authorized": False,
        },
        "scientific_state": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "independent_validation": False,
            "high_assurance_authorized": False,
        },
        "qc_record_id": "E002-QC-0001",
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
    }


def receipt_for_manifest(manifest_sha256: str) -> dict[str, Any]:
    receipt = lock_record()
    receipt["immutable_subject"] = {"sha256": manifest_sha256}
    return receipt


def write_ledger(tmp_path: Path, records: list[dict[str, Any]]) -> Path:
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def write_manifest(tmp_path: Path, manifest: dict[str, Any]) -> Path:
    path = tmp_path / "dataset-lock-evidence.json"
    path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    return path


def test_valid_dataset_lock_is_exact_append_after_complete_qc(tmp_path: Path) -> None:
    before = completed_prefix()
    after = before + [lock_record()]
    lock.validate_transition(before, after)
    lock.validate_retained_ledger(write_ledger(tmp_path, after), require_lock=True)


def test_dataset_lock_cannot_rewrite_predecessor_evidence() -> None:
    before = completed_prefix()
    after = deepcopy(before) + [lock_record()]
    after[20]["immutable_subject"]["commit_sha"] = "b" * 40
    with pytest.raises(SystemExit, match="must append exactly one record"):
        lock.validate_transition(before, after)


def test_dataset_lock_requires_all_50_seed_records() -> None:
    before = completed_prefix()
    del before[10]
    after = before + [lock_record()]
    with pytest.raises(SystemExit, match="complete through QC_LEDGER"):
        lock.validate_transition(before, after)


def test_dataset_lock_requires_direct_qc_predecessor() -> None:
    before = completed_prefix()
    after = before + [lock_record("E002-SEED-0050")]
    with pytest.raises(SystemExit, match="directly reference prior QC_LEDGER"):
        lock.validate_transition(before, after)


def test_dataset_lock_pass_cannot_authorize_unblinding_or_analysis() -> None:
    before = completed_prefix()
    promoted = lock_record()
    promoted["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    promoted["non_effects"].remove("DOES_NOT_AUTHORIZE_UNBLINDING")
    with pytest.raises(SystemExit, match="dataset-lock semantic ceiling"):
        lock.validate_transition(before, before + [promoted])


def test_non_pass_dataset_lock_has_zero_authority() -> None:
    before = completed_prefix()
    failed = lock_record()
    failed["status"] = "FAIL"
    failed["authorization_effect"] = "NONE"
    with pytest.raises(SystemExit, match="dataset lock requires PASS"):
        lock.validate_transition(before, before + [failed])


def test_evidence_manifest_schema_and_contract_exist() -> None:
    assert lock.EVIDENCE_SCHEMA_PATH.is_file()
    lock.validate_evidence_manifest(evidence_manifest())


def test_evidence_manifest_rejects_wrong_counts() -> None:
    manifest = evidence_manifest()
    manifest["dataset_shape"]["paired_seed_units"] = 49
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_evidence_manifest_rejects_wrong_run_identity_shape() -> None:
    manifest = evidence_manifest()
    manifest["collection_run"]["workflow_run_id"] = "future"
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_evidence_manifest_rejects_custody_promotion() -> None:
    manifest = evidence_manifest()
    manifest["custody"]["class"] = "INDEPENDENT"
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_evidence_manifest_rejects_outcome_inspection_or_aggregation() -> None:
    manifest = evidence_manifest()
    manifest["structural_qc"]["outcome_values_inspected"] = True
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)

    manifest = evidence_manifest()
    manifest["structural_qc"]["outcome_aggregation_performed"] = True
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_evidence_manifest_rejects_unblinding_or_analysis_authority() -> None:
    manifest = evidence_manifest()
    manifest["authorization_state"]["unblinding_authorized"] = True
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)

    manifest = evidence_manifest()
    manifest["authorization_state"]["primary_analysis_authorized"] = True
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_evidence_manifest_rejects_scientific_promotion() -> None:
    manifest = evidence_manifest()
    manifest["scientific_state"]["canonical_dgaf_efficacy"] = "ESTABLISHED"
    with pytest.raises(SystemExit, match="evidence manifest"):
        lock.validate_evidence_manifest(manifest)


def test_receipt_content_addresses_exact_manifest_bytes(tmp_path: Path) -> None:
    manifest = evidence_manifest()
    manifest_path = write_manifest(tmp_path, manifest)
    digest = lock.sha256_file(manifest_path)
    receipt = receipt_for_manifest(digest)
    lock.validate_receipt_against_manifest(receipt, manifest, digest)

    drifted = deepcopy(receipt)
    drifted["immutable_subject"]["sha256"] = "f" * 64
    with pytest.raises(SystemExit, match="evidence manifest digest"):
        lock.validate_receipt_against_manifest(drifted, manifest, digest)


def test_receipt_predecessor_must_match_manifest_qc() -> None:
    manifest = evidence_manifest()
    receipt = receipt_for_manifest("c" * 64)
    receipt["predecessor_record_ids"] = ["E002-SEED-0050"]
    with pytest.raises(SystemExit, match="QC_LEDGER"):
        lock.validate_receipt_against_manifest(receipt, manifest, "c" * 64)


def test_current_boundary_proves_dataset_lock_absent(capsys: pytest.CaptureFixture[str]) -> None:
    lock.validate_boundary()
    output = capsys.readouterr().out
    assert "TRACK_A_EPOCH_002_DATASET_LOCK_TOOLING=PASS_LOCK_ABSENT" in output
    assert "UNBLINDING_AUTHORIZED=FALSE" in output
    assert "PRIMARY_ANALYSIS_AUTHORIZED=FALSE" in output
    assert "SCIENTIFIC_N_INCREMENT=0" in output


def test_tool_has_no_write_execution_or_secret_surface() -> None:
    text = lock.MODULE_PATH.read_text(encoding="utf-8")
    assert "--write" not in text
    assert "write_text(" not in text
    assert "--execute" not in text
    assert "PDMAL_TOPOLOGY_BLINDING_KEY" not in text
    assert "PRIVATE_KEY" not in text
    assert "PASSPHRASE" not in text
