import pytest

from durable_retention import (
    archive_artifact,
    compute_sha256_file,
    require_archive_root,
    retrieve_archived_artifact,
    verify_archived_artifact,
    verify_retention_round_trip,
)


def test_archive_requires_configured_root(monkeypatch, tmp_path):
    monkeypatch.delenv("PDMAL_ARCHIVE_ROOT", raising=False)
    assert tmp_path.is_dir()
    try:
        require_archive_root()
    except RuntimeError as exc:
        assert "PDMAL_ARCHIVE_ROOT" in str(exc)
    else:
        raise AssertionError("archive root must be explicitly configured")


def test_archive_and_retrieve_round_trip(tmp_path):
    source = tmp_path / "artifact.json"
    source.write_text('{"ok":true}\n', encoding="utf-8")
    archive_root = tmp_path / "archive"
    destination = tmp_path / "retrieved" / "artifact.json"

    result = verify_retention_round_trip(
        source,
        archive_root=archive_root,
        destination=destination,
        freeze_sha="a" * 40,
    )

    assert result["round_trip_match"] is True
    assert result["source_sha256"] == result["archive_sha256"]
    assert result["source_sha256"] == result["retrieved_sha256"]

    archived = archive_root / "artifact.json"
    assert verify_archived_artifact(archived, compute_sha256_file(source)) is True


def test_archive_copy_is_checksum_verified(tmp_path):
    source = tmp_path / "artifact.json"
    source.write_text("payload\n", encoding="utf-8")
    archived = archive_artifact(
        source,
        archive_root=tmp_path / "archive",
        freeze_sha="b" * 40,
    )
    retrieved = retrieve_archived_artifact(
        archived.name,
        archive_root=tmp_path / "archive",
        destination=tmp_path / "retrieved.json",
    )
    assert compute_sha256_file(source) == compute_sha256_file(retrieved)


def test_archive_does_not_overwrite_different_bytes(tmp_path):
    source = tmp_path / "artifact.json"
    source.write_text("first\n", encoding="utf-8")
    archive_root = tmp_path / "archive"
    archive_artifact(source, archive_root=archive_root, freeze_sha="c" * 40)

    source.write_text("different\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="different SHA-256"):
        archive_artifact(source, archive_root=archive_root, freeze_sha="c" * 40)


def test_round_trip_fails_closed_on_checksum_mismatch(tmp_path, monkeypatch):
    source = tmp_path / "artifact.json"
    source.write_text("payload\n", encoding="utf-8")
    archive_root = tmp_path / "archive"
    destination = tmp_path / "retrieved.json"

    original = compute_sha256_file
    calls = {"count": 0}

    def tampered_hash(path):
        calls["count"] += 1
        digest = original(path)
        if calls["count"] >= 4:
            return "0" * 64
        return digest

    monkeypatch.setattr("durable_retention.compute_sha256_file", tampered_hash)
    with pytest.raises(RuntimeError, match="round-trip checksum"):
        verify_retention_round_trip(
            source,
            archive_root=archive_root,
            destination=destination,
            freeze_sha="d" * 40,
        )


def test_invalid_freeze_sha_is_rejected(tmp_path):
    source = tmp_path / "artifact.json"
    source.write_text("payload\n", encoding="utf-8")
    with pytest.raises(ValueError, match="full 40-character"):
        archive_artifact(source, archive_root=tmp_path / "archive", freeze_sha="not-a-sha")
