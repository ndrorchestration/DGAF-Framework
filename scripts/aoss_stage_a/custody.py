"""Synthetic-only content-addressed custody primitives for Stage-A development."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
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


def _fsync_fd(fd: int) -> None:
    os.fsync(fd)


def _open_dir_fd(path: Path | str, *, dir_fd: int | None = None) -> int:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW_REQUIRED")
    try:
        return os.open(path, flags | nofollow, dir_fd=dir_fd)
    except OSError as exc:
        raise ValueError(f"directory open rejected: {path}") from exc


def _require_path_matches_fd(path: Path, fd: int, message: str) -> None:
    try:
        path_stat = os.stat(path, follow_symlinks=False)
    except OSError as exc:
        raise ValueError(message) from exc
    fd_stat = os.fstat(fd)
    if (
        not stat.S_ISDIR(path_stat.st_mode)
        or path_stat.st_dev != fd_stat.st_dev
        or path_stat.st_ino != fd_stat.st_ino
    ):
        raise ValueError(message)


def _exclusive_write_at(dir_fd: int, name: str, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW_REQUIRED")
    fd = os.open(name, flags | nofollow, 0o600, dir_fd=dir_fd)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            _fsync_fd(handle.fileno())
    finally:
        os.close(fd)
    _fsync_fd(dir_fd)


def _read_at(dir_fd: int, name: str) -> bytes:
    flags = os.O_RDONLY
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW_REQUIRED")
    fd = os.open(name, flags | nofollow, dir_fd=dir_fd)
    try:
        with os.fdopen(fd, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(fd)


def reserve_synthetic_attempt(parent: Path, attempt_id: str) -> Path:
    parent = Path(parent)
    if not _ATTEMPT_ID.fullmatch(attempt_id):
        raise ValueError("invalid synthetic attempt id")
    if not parent.exists() or not parent.is_dir():
        raise FileNotFoundError(parent)
    _assert_no_symlink_components(parent)

    parent_fd = _open_dir_fd(parent)
    attempt = parent / attempt_id
    attempt_fd: int | None = None
    try:
        _require_path_matches_fd(parent, parent_fd, "parent directory changed during reservation")
        os.mkdir(attempt_id, 0o700, dir_fd=parent_fd)
        _fsync_fd(parent_fd)
        _require_path_matches_fd(parent, parent_fd, "parent directory changed during reservation")

        attempt_fd = _open_dir_fd(attempt_id, dir_fd=parent_fd)
        _require_path_matches_fd(attempt, attempt_fd, "attempt directory changed during reservation")
        try:
            _exclusive_write_at(attempt_fd, "SYNTHETIC_TEST_ONLY", _MARKER)
            _exclusive_write_at(
                attempt_fd,
                "STARTED.json",
                canonical_bytes(
                    {
                        "record_type": "AOSS_STAGE_A_SYNTHETIC_ATTEMPT_EVENT",
                        "state": "STARTED",
                        "synthetic_test_only": True,
                    }
                ),
            )
            os.mkdir("objects", 0o700, dir_fd=attempt_fd)
            _fsync_fd(attempt_fd)
        except Exception:
            # Preserve the incomplete reservation as evidence. Never clean and reuse.
            raise

        _require_path_matches_fd(parent, parent_fd, "parent directory changed during reservation")
        _require_path_matches_fd(attempt, attempt_fd, "attempt directory changed during reservation")
        return attempt
    finally:
        if attempt_fd is not None:
            os.close(attempt_fd)
        os.close(parent_fd)


def write_object(attempt: Path, payload: object) -> str:
    attempt = Path(attempt)
    _assert_no_symlink_components(attempt)

    attempt_fd = _open_dir_fd(attempt)
    objects_fd: int | None = None
    try:
        _require_path_matches_fd(attempt, attempt_fd, "synthetic attempt directory changed")
        try:
            marker = _read_at(attempt_fd, "SYNTHETIC_TEST_ONLY")
        except OSError as exc:
            raise ValueError("synthetic attempt marker missing or invalid") from exc
        if marker != _MARKER:
            raise ValueError("synthetic attempt marker missing or invalid")

        try:
            objects_fd = _open_dir_fd("objects", dir_fd=attempt_fd)
        except ValueError as exc:
            raise ValueError("synthetic object directory invalid") from exc
        objects = attempt / "objects"
        _require_path_matches_fd(objects, objects_fd, "synthetic object directory invalid")

        data = canonical_bytes(payload)
        digest = digest_bytes(data)
        name = f"{digest}.json"
        try:
            existing = _read_at(objects_fd, name)
        except FileNotFoundError:
            existing = None
        except OSError as exc:
            raise FileExistsError(objects / name) from exc

        if existing is not None:
            if existing != data:
                raise FileExistsError(objects / name)
            return digest

        _exclusive_write_at(objects_fd, name, data)
        _require_path_matches_fd(attempt, attempt_fd, "synthetic attempt directory changed")
        _require_path_matches_fd(objects, objects_fd, "synthetic object directory invalid")
        return digest
    finally:
        if objects_fd is not None:
            os.close(objects_fd)
        os.close(attempt_fd)
