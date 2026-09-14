from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/prepare_track_a_epoch_002_operator_pre_lock_ledger.py"


def load_preparer():
    assert MODULE_PATH.is_file(), "operator pre-lock ledger preparer is not implemented"
    spec = importlib.util.spec_from_file_location("epoch_002_operator_pre_lock", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_auth() -> dict:
    return {
        "frozen_candidate_sha": "7bbd97604d82efada43d0b139901f06eb2582a23",
        "frozen_candidate_tree_sha": "d6c4e94586551880d657ae3464043a08bfc5d8e1",
        "custody_receipt_blob_sha": "c" * 40,
    }


def sample_admission() -> dict:
    return {
        "collection_execution_receipt_sha256": "1" * 64,
        "public_retention": {
            "name": "track-a-epoch-002-public-blinded",
            "size_bytes": 860160,
            "archive_sha256": "2" * 64,
            "manifest_sha256": "3" * 64,
        },
        "protected_retention": {
            "name": "track-a-epoch-002-protected-encrypted",
            "size_bytes": 143360,
            "archive_sha256": "4" * 64,
            "ciphertext_sha256": "5" * 64,
            "plaintext_tar_sha256": "6" * 64,
            "custody_certificate_sha256": "7" * 64,
            "custody_certificate_public_key_der_sha256": "8" * 64,
        },
    }


def sample_seed_digests() -> dict[int, str]:
    return {
        seed: f"{index:064x}"[-64:]
        for index, seed in enumerate(range(20270201, 20270251), start=1)
    }


def test_builds_exact_53_record_retrospective_non_authorizing_ledger() -> None:
    preparer = load_preparer()
    ledger = preparer.build_pre_lock_ledger(
        auth=sample_auth(),
        admission_record=sample_admission(),
        admission_record_sha256="9" * 64,
        seed_digests=sample_seed_digests(),
        generated_at_utc="2026-09-14T06:00:00Z",
        producer_commit="a" * 40,
    )

    assert len(ledger) == 53
    assert ledger[0]["record_type"] == "PRECOLLECTION_GATE_CHECKLIST"
    assert ledger[1]["record_type"] == "COLLECTION_START_RECEIPT"
    assert [record["record_type"] for record in ledger[2:52]] == [
        "PER_SEED_EXECUTION_RECORD"
    ] * 50
    assert ledger[-1]["record_type"] == "QC_LEDGER"
    assert ledger[-1]["status"] == "PASS"

    for index, record in enumerate(ledger):
        assert record["generated_at_utc"] == "2026-09-14T06:00:00Z"
        assert record["producer"] == {
            "system": "DGAF_TRACK_A_EPOCH_002_OPERATOR_PRE_LOCK_LEDGER_PREPARER",
            "version_or_commit": "a" * 40,
        }
        assert record["status"] == "PASS"
        assert record["authorization_effect"] == "NONE"
        assert set(record["non_effects"]) == set(preparer.dataset_lock.FULL_NON_EFFECTS)
        assert record["scientific_state_effect"] == {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        }
        assert "RETROSPECTIVE_OPERATOR" in record["evidence_scope"]
        expected_predecessors = [] if index == 0 else [ledger[index - 1]["record_id"]]
        assert record["predecessor_record_ids"] == expected_predecessors

    assert ledger[0]["immutable_subject"] == {
        "commit_sha": sample_auth()["frozen_candidate_sha"],
        "tree_sha": sample_auth()["frozen_candidate_tree_sha"],
    }
    assert ledger[1]["immutable_subject"] == {
        "commit_sha": preparer.admission.AUTHORIZATION_SHA,
        "sha256": sample_admission()["collection_execution_receipt_sha256"],
    }
    assert ledger[2]["immutable_subject"]["sha256"] == sample_seed_digests()[20270201]
    assert ledger[51]["immutable_subject"]["sha256"] == sample_seed_digests()[20270250]
    assert ledger[-1]["immutable_subject"] == {
        "commit_sha": preparer.admission.AUTHORIZATION_SHA,
        "sha256": "9" * 64,
    }


def test_seed_digest_panel_must_be_exact() -> None:
    preparer = load_preparer()
    digests = sample_seed_digests()
    del digests[20270217]
    digests[99999999] = "f" * 64

    with pytest.raises(SystemExit, match="seed digest panel"):
        preparer.build_pre_lock_ledger(
            auth=sample_auth(),
            admission_record=sample_admission(),
            admission_record_sha256="9" * 64,
            seed_digests=digests,
            generated_at_utc="2026-09-14T06:00:00Z",
            producer_commit="a" * 40,
        )


def test_seed_digests_are_derived_from_sidecar_bound_public_bytes() -> None:
    preparer = load_preparer()
    members: dict[str, bytes] = {}
    expected: dict[int, str] = {}
    for index, seed in enumerate(preparer.admission.SEEDS, start=1):
        payload = json.dumps({"seed": seed}, sort_keys=True).encode()
        digest = preparer.sha256_bytes(payload)
        name = f"track_a_epoch_002_seed_{seed}.json"
        members[name] = payload
        members[f"{name}.sha256"] = f"{digest}  {name}\n".encode()
        expected[seed] = digest

    assert preparer.seed_digests_from_public_members(members) == expected

    first = preparer.admission.SEEDS[0]
    first_name = f"track_a_epoch_002_seed_{first}.json"
    members[first_name] = b"drift"
    with pytest.raises(SystemExit, match="sidecar digest mismatch"):
        preparer.seed_digests_from_public_members(members)


def test_generated_ledger_passes_existing_structural_and_semantic_validators(tmp_path: Path) -> None:
    preparer = load_preparer()
    ledger = preparer.build_pre_lock_ledger(
        auth=sample_auth(),
        admission_record=sample_admission(),
        admission_record_sha256="9" * 64,
        seed_digests=sample_seed_digests(),
        generated_at_utc="2026-09-14T06:00:00Z",
        producer_commit="a" * 40,
    )
    path = tmp_path / "track_a_epoch_002_pre_lock_result_ledger.json"
    path.write_bytes(preparer.canonical_json_bytes(ledger))

    preparer.validate_ledger(path)


def test_write_mode_validates_retained_bytes_before_persisting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    retention = tmp_path / "retention"
    retention.mkdir()
    output = retention / preparer.PRE_LOCK_LEDGER_NAME
    writes: list[Path] = []

    monkeypatch.setattr(preparer, "require_external_retention_dir", lambda path: path)
    monkeypatch.setattr(
        preparer,
        "resolve_inputs",
        lambda **kwargs: preparer.OperatorInputs(
            admission_record_path=retention / "admission.json",
            execution_receipt_path=retention / "receipt.json",
            public_archive=retention / "public.tar",
            protected_archive=retention / "protected.tar",
        ),
    )
    monkeypatch.setattr(
        preparer,
        "validate_and_load_retained_evidence",
        lambda inputs: (_ for _ in ()).throw(SystemExit("invalid retained evidence")),
    )
    monkeypatch.setattr(preparer, "write_new_or_identical", lambda path, content: writes.append(path))

    with pytest.raises(SystemExit, match="invalid retained evidence"):
        preparer.prepare(retention_dir=retention, write=True)

    assert writes == []
    assert not output.exists()


def test_preparer_source_has_no_outcome_aggregation_decryption_or_authorization_surface() -> None:
    load_preparer()
    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden = (
        "ffcr_success",
        "openssl cms -decrypt",
        "PDMAL_TOPOLOGY_BLINDING_KEY",
        "BEGIN PRIVATE KEY",
        "authorize_unblinding=True",
        "authorize_primary_analysis=True",
    )
    for marker in forbidden:
        assert marker not in source
