from pathlib import Path

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
