"""Durable PDMAL artifact retention primitives.

The module deliberately does not claim that an archive exists. Pilot-mode code
must be configured with PDMAL_ARCHIVE_ROOT, and closure of the retention gate
requires an actual archive/retrieval/hash verification event.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any, Mapping


ARCHIVE_ROOT_ENV = "PDMAL_ARCHIVE_ROOT"


def require_archive_root() -> Path:
    value = os.getenv(ARCHIVE_ROOT_ENV, "").strip()
    if not value:
        raise RuntimeError(f"{ARCHIVE_ROOT_ENV} must be configured for durable retention")
    root = Path(value).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    if not root.is_dir():
        raise RuntimeError(f"durable archive root is not a directory: {root}")
    return root


def compute_sha256_file(path: str | Path) -> str:
    source = Path(path)
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_name(name: str) -> str:
    candidate = Path(name).name
    if candidate in {"", ".", ".."}:
        raise ValueError("invalid artifact name")
    return candidate


def archive_artifact(
    artifact_path: str | Path,
    *,
    archive_root: str | Path | None = None,
    freeze_sha: str,
    metadata: Mapping[str, Any] | None = None,
) -> Path:
    source = Path(artifact_path).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    root = Path(archive_root).expanduser().resolve() if archive_root else require_archive_root()
    root.mkdir(parents=True, exist_ok=True)

    target = root / _safe_name(source.name)
    shutil.copy2(source, target)
    source_sha = compute_sha256_file(source)
    target_sha = compute_sha256_file(target)
    if source_sha != target_sha:
        raise RuntimeError("durable archive checksum mismatch immediately after copy")

    manifest = generate_retention_manifest(
        target,
        freeze_sha=freeze_sha,
        metadata=metadata,
    )
    manifest_path = target.with_suffix(target.suffix + ".retention.json")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def generate_retention_manifest(
    archived_artifact: str | Path,
    *,
    freeze_sha: str,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(archived_artifact).resolve()
    return {
        "artifact": path.name,
        "artifact_sha256": compute_sha256_file(path),
        "freeze_sha": freeze_sha,
        "metadata": dict(metadata or {}),
    }


def list_archives(archive_root: str | Path | None = None) -> list[Path]:
    root = Path(archive_root).expanduser().resolve() if archive_root else require_archive_root()
    if not root.exists():
        return []
    return sorted(
        p for p in root.iterdir()
        if p.is_file() and not p.name.endswith(".retention.json")
    )


def retrieve_archived_artifact(
    name: str,
    *,
    archive_root: str | Path | None = None,
    destination: str | Path,
) -> Path:
    root = Path(archive_root).expanduser().resolve() if archive_root else require_archive_root()
    source = root / _safe_name(name)
    if not source.is_file():
        raise FileNotFoundError(source)
    target = Path(destination).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def verify_archived_artifact(
    archived_artifact: str | Path,
    expected_sha256: str,
) -> bool:
    return compute_sha256_file(archived_artifact) == expected_sha256


def verify_retention_round_trip(
    artifact_path: str | Path,
    *,
    archive_root: str | Path,
    destination: str | Path,
    freeze_sha: str,
) -> dict[str, Any]:
    source = Path(artifact_path).resolve()
    source_sha = compute_sha256_file(source)
    archived = archive_artifact(source, archive_root=archive_root, freeze_sha=freeze_sha)
    retrieved = retrieve_archived_artifact(
        archived.name,
        archive_root=archive_root,
        destination=destination,
    )
    retrieved_sha = compute_sha256_file(retrieved)
    return {
        "source": str(source),
        "archive": str(archived),
        "retrieved": str(retrieved),
        "source_sha256": source_sha,
        "archive_sha256": compute_sha256_file(archived),
        "retrieved_sha256": retrieved_sha,
        "round_trip_match": source_sha == retrieved_sha,
        "freeze_sha": freeze_sha,
    }
