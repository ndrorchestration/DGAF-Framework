from __future__ import annotations

import hashlib
import io
import tarfile
from pathlib import Path

import pytest

from scripts import prepare_track_a_epoch_002_operator_collection_admission as preparer


def write_tar(path: Path, names: list[str]) -> None:
    with tarfile.open(path, "w") as archive:
        for name in names:
            data = b"x"
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


def test_classify_archive_uses_exact_member_sets(tmp_path: Path) -> None:
    public_path = tmp_path / "arbitrary-public-name.bin"
    protected_path = tmp_path / "arbitrary-protected-name.bin"
    write_tar(public_path, sorted(preparer.admission.PUBLIC_NAMES))
    write_tar(protected_path, sorted(preparer.admission.PROTECTED_NAMES))

    assert preparer.classify_archive(public_path) == "public"
    assert preparer.classify_archive(protected_path) == "protected"


def test_discover_archives_rejects_ambiguous_candidates(tmp_path: Path) -> None:
    for name in ("public-a.tar", "public-b.tar"):
        write_tar(tmp_path / name, sorted(preparer.admission.PUBLIC_NAMES))
    write_tar(tmp_path / "protected.tar", sorted(preparer.admission.PROTECTED_NAMES))

    with pytest.raises(SystemExit, match="exactly one public archive"):
        preparer.discover_archives(tmp_path)


def test_execution_receipt_preserves_non_authorizing_boundary() -> None:
    auth = {
        "frozen_candidate_sha": "7bbd97604d82efada43d0b139901f06eb2582a23",
        "frozen_candidate_tree_sha": "d6c4e94586551880d657ae3464043a08bfc5d8e1",
        "requirements_lock_blob_sha": "00c1f779e97030f9b25ae494642edb31b5b09de5",
    }

    receipt = preparer.build_execution_receipt(auth)

    assert receipt["collection_execution_class"] == "OPERATOR_CODESPACE"
    assert receipt["paired_seed_units"] == 50
    assert receipt["blinded_observations"] == 2250
    assert receipt["outcomes_inspected_for_receipt"] is False
    assert receipt["outcome_aggregation_performed"] is False
    assert receipt["unblinding_authorized"] is False
    assert receipt["primary_analysis_authorized"] is False
    assert receipt["high_assurance_authorized"] is False
    assert receipt["scientific_n_increment"] == 0
    assert receipt["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_write_new_or_identical_refuses_drift(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    original = b'{"a":1}\n'
    preparer.write_new_or_identical(path, original)
    preparer.write_new_or_identical(path, original)

    with pytest.raises(SystemExit, match="refusing to overwrite different bytes"):
        preparer.write_new_or_identical(path, b'{"a":2}\n')


def test_build_record_content_addresses_actual_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    public_path = tmp_path / "public.tar"
    protected_path = tmp_path / "protected.tar"
    public_manifest = b'{"manifest":true}\n'
    cert = b"certificate"
    ciphertext = b"ciphertext"
    plaintext_digest = "a" * 64

    public_path.write_bytes(b"public-archive")
    protected_path.write_bytes(b"protected-archive")

    public_members = {"track_a_epoch_002_manifest.json": public_manifest}
    protected_members = {
        "track_a_epoch_002_custody_cert.pem": cert,
        "track_a_epoch_002_protected.cms": ciphertext,
        "track_a_epoch_002_protected_plaintext_tar.sha256": (
            f"{plaintext_digest}  track_a_epoch_002_protected.tar\n".encode()
        ),
    }

    def fake_members(path: Path, allowed: frozenset[str], label: str) -> dict[str, bytes]:
        del allowed
        return public_members if label == "public" else protected_members

    monkeypatch.setattr(preparer.admission, "_tar_members", fake_members)

    auth = {
        "frozen_candidate_sha": "7bbd97604d82efada43d0b139901f06eb2582a23",
        "frozen_candidate_tree_sha": "d6c4e94586551880d657ae3464043a08bfc5d8e1",
        "requirements_lock_blob_sha": "00c1f779e97030f9b25ae494642edb31b5b09de5",
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "custody_certificate_public_key_der_sha256": "b" * 64,
    }
    receipt_bytes = preparer.canonical_json_bytes(preparer.build_execution_receipt(auth))

    record = preparer.build_admission_record(
        auth=auth,
        receipt_bytes=receipt_bytes,
        public_archive=public_path,
        protected_archive=protected_path,
    )

    assert record["collection_execution_receipt_sha256"] == hashlib.sha256(receipt_bytes).hexdigest()
    assert record["public_retention"]["size_bytes"] == len(b"public-archive")
    assert record["public_retention"]["archive_sha256"] == hashlib.sha256(b"public-archive").hexdigest()
    assert record["public_retention"]["manifest_sha256"] == hashlib.sha256(public_manifest).hexdigest()
    assert record["protected_retention"]["size_bytes"] == len(b"protected-archive")
    assert record["protected_retention"]["archive_sha256"] == hashlib.sha256(b"protected-archive").hexdigest()
    assert record["protected_retention"]["ciphertext_sha256"] == hashlib.sha256(ciphertext).hexdigest()
    assert record["protected_retention"]["plaintext_tar_sha256"] == plaintext_digest
    assert record["protected_retention"]["custody_certificate_sha256"] == hashlib.sha256(cert).hexdigest()
    assert record["protected_retention"]["custody_certificate_public_key_der_sha256"] == "b" * 64
    assert record["admission_status"] == "CONTENT_ADDRESSED_PENDING_DATASET_LOCK"
    assert record["unblinding_authorized"] is False
    assert record["primary_analysis_authorized"] is False
    assert record["scientific_n_increment"] == 0


def test_retention_directory_must_not_be_inside_repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_root = tmp_path / "repo"
    fake_root.mkdir()
    retention = fake_root / "retention"
    retention.mkdir()
    monkeypatch.setattr(preparer, "ROOT", fake_root)

    with pytest.raises(SystemExit, match="outside the repository"):
        preparer.require_external_retention_dir(retention)


def test_explicit_archive_path_must_not_be_inside_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_root = tmp_path / "repo"
    fake_root.mkdir()
    retention = tmp_path / "retention"
    retention.mkdir()
    public_archive = fake_root / "public.tar"
    protected_archive = retention / "protected.tar"
    public_archive.write_bytes(b"x")
    protected_archive.write_bytes(b"x")
    monkeypatch.setattr(preparer, "ROOT", fake_root)

    with pytest.raises(SystemExit, match="archive must remain outside the repository"):
        preparer.resolve_archives(retention, public_archive, protected_archive)


def test_write_mode_validates_before_persisting(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    retention = tmp_path / "retention"
    retention.mkdir()
    public_archive = retention / "public.tar"
    protected_archive = retention / "protected.tar"
    public_archive.write_bytes(b"public")
    protected_archive.write_bytes(b"protected")
    writes: list[Path] = []

    monkeypatch.setattr(preparer, "require_external_retention_dir", lambda path: path)
    monkeypatch.setattr(
        preparer,
        "resolve_archives",
        lambda retention_dir, public, protected: (public_archive, protected_archive),
    )
    monkeypatch.setattr(preparer.admission, "accepted_authorization", lambda: {})
    monkeypatch.setattr(preparer, "build_execution_receipt", lambda auth: {})
    monkeypatch.setattr(preparer, "build_admission_record", lambda **kwargs: {})
    monkeypatch.setattr(preparer.admission, "validate_record", lambda record: None)
    monkeypatch.setattr(
        preparer.admission,
        "validate_evidence_acceptance",
        lambda *args: (_ for _ in ()).throw(SystemExit("invalid retained evidence")),
    )
    monkeypatch.setattr(preparer, "write_new_or_identical", lambda path, content: writes.append(path))

    with pytest.raises(SystemExit, match="invalid retained evidence"):
        preparer.prepare(retention_dir=retention, write=True)

    assert writes == []
