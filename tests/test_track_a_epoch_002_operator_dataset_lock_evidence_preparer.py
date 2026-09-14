from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/prepare_track_a_epoch_002_operator_dataset_lock_evidence.py"


def load_preparer():
    spec = importlib.util.spec_from_file_location("epoch_002_operator_dataset_lock_evidence", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_auth() -> dict:
    return {
        "frozen_candidate_sha": "a" * 40,
        "frozen_candidate_tree_sha": "b" * 40,
        "custody_receipt_blob_sha": "c" * 40,
    }


def sample_admission() -> dict:
    return {
        "collection_execution_receipt_sha256": "1" * 64,
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
            "custody_certificate_sha256": "7" * 64,
            "custody_certificate_public_key_der_sha256": "8" * 64,
        },
    }


def sample_ledger() -> list[dict]:
    records = [
        {
            "record_type": "PRECOLLECTION_GATE_CHECKLIST",
            "record_id": "E002:GATE:RETROSPECTIVE_OPERATOR",
        },
        {
            "record_type": "COLLECTION_START_RECEIPT",
            "record_id": "E002:START:RETROSPECTIVE_OPERATOR",
        },
    ]
    for seed in range(20270201, 20270251):
        records.append(
            {
                "record_type": "PER_SEED_EXECUTION_RECORD",
                "record_id": f"E002:SEED:{seed}:RETROSPECTIVE_OPERATOR",
            }
        )
    records.append(
        {
            "record_type": "QC_LEDGER",
            "record_id": "E002:QC:RETROSPECTIVE_OPERATOR",
            "status": "PASS",
        }
    )
    return records


def test_build_evidence_is_operator_non_authorizing_and_actions_id_free() -> None:
    preparer = load_preparer()
    evidence = preparer.build_evidence(
        auth=sample_auth(),
        admission_record=sample_admission(),
        admission_record_sha256="9" * 64,
        ledger=sample_ledger(),
        ledger_sha256="d" * 64,
        evidence_tooling_commit_sha="e" * 40,
        collection_authorization_blob_sha="f" * 40,
    )

    assert evidence["evidence_execution_class"] == "OPERATOR_CODESPACE"
    assert evidence["collection_execution_class"] == "OPERATOR_CODESPACE"
    assert evidence["operator_admission_record_sha256"] == "9" * 64
    assert evidence["collection_execution_receipt_sha256"] == "1" * 64
    assert evidence["pre_lock_result_ledger_record_count"] == 53
    assert evidence["scientific_n_increment"] == 0
    assert evidence["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert evidence["unblinding_authorized"] is False
    assert evidence["primary_analysis_authorized"] is False
    assert "evidence_workflow_run_id" not in evidence
    assert "collection_workflow_run_id" not in evidence
    assert "artifact_id" not in evidence["public_artifact"]
    assert "artifact_id" not in evidence["protected_artifact"]
    preparer.dataset_lock.validate_evidence_object(evidence)


def test_validate_retained_bytes_runs_every_structural_boundary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    calls: list[str] = []
    ledger = tmp_path / "ledger.json"
    public_archive = tmp_path / "public.tar"
    protected_archive = tmp_path / "protected.tar"
    ledger.write_text("[]\n", encoding="utf-8")
    public_archive.write_bytes(b"public")
    protected_archive.write_bytes(b"protected")

    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_pre_lock_ledger",
        lambda path, evidence: calls.append("ledger"),
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_archive",
        lambda path, spec, label: calls.append(f"archive:{label}"),
    )
    monkeypatch.setattr(
        preparer.admission,
        "_tar_members",
        lambda path, allowed, label: {name: name.encode() for name in allowed},
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_public_root",
        lambda root, evidence: calls.append("public-root"),
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_protected_root",
        lambda root, evidence: calls.append("protected-root"),
    )

    preparer.validate_retained_bytes(
        evidence={"public_artifact": {}, "protected_artifact": {}},
        ledger_path=ledger,
        public_archive=public_archive,
        protected_archive=protected_archive,
    )

    assert calls == [
        "ledger",
        "archive:public",
        "archive:protected",
        "public-root",
        "protected-root",
    ]


def test_preparer_source_has_no_decryption_secret_or_outcome_reader_surface() -> None:
    load_preparer()
    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden = (
        "openssl cms -decrypt",
        "PDMAL_TOPOLOGY_BLINDING_KEY",
        "BEGIN PRIVATE KEY",
        "BEGIN ENCRYPTED PRIVATE KEY",
        "ffcr_success",
        "authorize_unblinding=True",
        "authorize_primary_analysis=True",
    )
    for marker in forbidden:
        assert marker not in source
