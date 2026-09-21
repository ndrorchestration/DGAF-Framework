"""Synthetic-only content-addressed custody primitives for Stage-A development."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

_ATTEMPT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_MARKER = b"SYNTHETIC_TEST_ONLY\n"


def canonical_bytes(value: object) -> bytes:
    """Return the foundation bundle canonical JSON convention."""

    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _assert_no_symlink_components(path: Path) -> None:
    current = Path(path.anchor) if path.is_absolute() else Path(".")
    for part in path.parts:
        if part in ("", path.anchor):
            continue
        current = current / part
        if current.exists() and current.is_symlink():
            raise ValueError(f"symlink path component rejected: {current}")


def _fsync_dir(path: Path) -> None:
    flags = os.O_RDONLY
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW_REQUIRED")
    fd = os.open(path, flags | directory_flag | nofollow)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW_REQUIRED")
    flags |= nofollow
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
        _fsync_dir(path.parent)


def reserve_synthetic_attempt(parent: Path, attempt_id: str) -> Path:
    parent = Path(parent)
    if not _ATTEMPT_ID.fullmatch(attempt_id):
        raise ValueError("invalid synthetic attempt id")
    if not parent.exists() or not parent.is_dir():
        raise FileNotFoundError(parent)
    _assert_no_symlink_components(parent)

    attempt = parent / attempt_id
    os.mkdir(attempt, 0o700)
    _fsync_dir(parent)
    try:
        _exclusive_write(attempt / "SYNTHETIC_TEST_ONLY", _MARKER)
        _exclusive_write(
            attempt / "STARTED.json",
            canonical_bytes(
                {
                    "record_type": "AOSS_STAGE_A_SYNTHETIC_ATTEMPT_EVENT",
                    "state": "STARTED",
                    "synthetic_test_only": True,
                }
            ),
        )
        objects = attempt / "objects"
        os.mkdir(objects, 0o700)
        _fsync_dir(attempt)
    except Exception:
        # Preserve the incomplete reservation as evidence. Never clean and reuse.
        raise
    return attempt


def write_object(attempt: Path, payload: object) -> str:
    attempt = Path(attempt)
    marker = attempt / "SYNTHETIC_TEST_ONLY"
    if not marker.is_file() or marker.read_bytes() != _MARKER:
        raise ValueError("synthetic attempt marker missing or invalid")
    _assert_no_symlink_components(attempt)

    data = canonical_bytes(payload)
    digest = digest_bytes(data)
    objects = attempt / "objects"
    if not objects.is_dir() or objects.is_symlink():
        raise ValueError("synthetic object directory invalid")
    target = objects / f"{digest}.json"

    if target.exists():
        if target.is_symlink() or target.read_bytes() != data:
            raise FileExistsError(target)
        return digest

    _exclusive_write(target, data)
    return digest
