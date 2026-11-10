"""POSIX file-backed fixture witness: separate path/process, NOT external custody.

An append-only HMAC-chained journal and flock guard demonstrate durable
same-host CAS and tamper detection. This file is NOT an independently
administered security domain, anti-rollback hardware, or production authority.
"""

import fcntl
import json
import os
import stat
from contextlib import contextmanager
from hashlib import sha256
from hmac import compare_digest, new
from pathlib import Path
from typing import Iterator

from scripts.triadic_monotonic_custody import (
    CustodyMismatch,
    FixtureMonotonicWitness,
    WitnessState,
    _is_digest,
)

FORMAT = "triadic-posix-witness-v0.1"
MAX_BYTES = 262144
ZERO = "0" * 64


def _encoded(value: dict[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, value in pairs:
        if name in result:
            raise CustodyMismatch("DUPLICATE_WITNESS_KEY")
        result[name] = value
    return result


class PosixFileWitness(FixtureMonotonicWitness):
    """A test witness retained on disk and reloaded by separate processes.

    This subclass implements the same narrow snapshot/initialize/advance
    contract as the in-memory fixture. Both caller and lock directory must be
    trusted; a malicious host can replace witness and lock files together.
    """

    def __init__(self, path: Path, stream_id: str, key: bytes):
        if (
            not isinstance(path, Path)
            or type(stream_id) is not str
            or not stream_id
            or type(key) is not bytes
            or len(key) < 32
            or not path.parent.is_dir()
        ):
            raise ValueError("BAD_FILE_WITNESS_MANIFEST")
        if os.name != "posix":
            raise RuntimeError("POSIX_REQUIRED")
        super().__init__(stream_id)
        self._path = path
        self._guard = path.with_name(path.name + ".lock")
        self._key = key

    @contextmanager
    def _locked(self) -> Iterator[None]:
        flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(self._guard, flags, 0o600)
        except OSError as error:
            raise CustodyMismatch("WITNESS_LOCK_UNAVAILABLE") from error
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise CustodyMismatch("INVALID_LOCK_FILE")
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            os.close(fd)

    def _directory_fsync(self) -> None:
        fd = os.open(self._path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _event(self, sequence: int, digest: str, previous: str) -> bytes:
        body: dict[str, object] = {
            "format": FORMAT,
            "stream_id": self._stream_id,
            "sequence": sequence,
            "journal_digest": digest,
            "previous_line_digest": previous,
        }
        tag = new(self._key, _encoded(body), "sha256").hexdigest()
        return _encoded({"body": body, "mac": tag}) + b"\n"

    def _read(self) -> tuple[WitnessState, str] | None:
        if self._path.is_symlink():
            raise CustodyMismatch("SYMLINK_WITNESS")
        try:
            fd = os.open(self._path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        except FileNotFoundError:
            return None
        except OSError as error:
            raise CustodyMismatch("UNREADABLE_WITNESS") from error
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise CustodyMismatch("INVALID_WITNESS_FILE")
            with os.fdopen(fd, "rb") as handle:
                raw = handle.read(MAX_BYTES + 1)
        except OSError as error:
            raise CustodyMismatch("UNREADABLE_WITNESS") from error
        if not raw or len(raw) > MAX_BYTES or not raw.endswith(b"\n"):
            raise CustodyMismatch("INCOMPLETE_WITNESS")
        prior = ZERO
        state: WitnessState | None = None
        for sequence, line in enumerate(raw.splitlines()):
            try:
                event = json.loads(line, object_pairs_hook=_unique)
            except (UnicodeError, json.JSONDecodeError) as error:
                raise CustodyMismatch("MALFORMED_WITNESS") from error
            if type(event) is not dict or set(event) != {"body", "mac"}:
                raise CustodyMismatch("BAD_WITNESS_ENVELOPE")
            body, mac = event["body"], event["mac"]
            if type(body) is not dict or type(mac) is not str or not _is_digest(mac):
                raise CustodyMismatch("BAD_WITNESS_ENVELOPE")
            if set(body) != {
                "format", "stream_id", "sequence", "journal_digest", "previous_line_digest"
            }:
                raise CustodyMismatch("BAD_WITNESS_SCHEMA")
            if (
                body["format"] != FORMAT
                or body["stream_id"] != self._stream_id
                or type(body["sequence"]) is not int
                or body["sequence"] != sequence
                or not _is_digest(body["journal_digest"])
                or body["previous_line_digest"] != prior
            ):
                raise CustodyMismatch("INVALID_WITNESS_CHAIN")
            expected = new(self._key, _encoded(body), "sha256").hexdigest()
            if not compare_digest(expected, mac):
                raise CustodyMismatch("INVALID_WITNESS_MAC")
            if state is not None and state.journal_digest == body["journal_digest"]:
                raise CustodyMismatch("NON_ADVANCING_WITNESS")
            state = WitnessState(self._stream_id, sequence, body["journal_digest"])
            prior = sha256(line).hexdigest()
        if state is None:
            raise CustodyMismatch("EMPTY_WITNESS")
        return state, prior

    def snapshot(self) -> WitnessState | None:
        with self._locked():
            result = self._read()
            return result[0] if result is not None else None

    def initialize(self, digest: str) -> WitnessState:
        if not _is_digest(digest):
            raise ValueError("BAD_DIGEST")
        with self._locked():
            if self._read() is not None:
                raise CustodyMismatch("ALREADY_INITIALIZED")
            if self._path.is_symlink():
                raise CustodyMismatch("SYMLINK_WITNESS")
            try:
                fd = os.open(
                    self._path,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                )
            except FileExistsError as error:
                raise CustodyMismatch("ALREADY_INITIALIZED") from error
            except OSError as error:
                raise CustodyMismatch("WITNESS_CREATE_FAILED") from error
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(self._event(0, digest, ZERO))
                    handle.flush()
                    os.fsync(handle.fileno())
                self._directory_fsync()
            except BaseException:
                raise
            return WitnessState(self._stream_id, 0, digest)

    def advance(self, expected: WitnessState, new_digest: str) -> WitnessState:
        if type(expected) is not WitnessState or not _is_digest(new_digest):
            raise ValueError("BAD_WITNESS_UPDATE")
        with self._locked():
            current = self._read()
            if current is None or current[0] != expected:
                raise CustodyMismatch("STALE_WITNESS")
            if expected.stream_id != self._stream_id or new_digest == expected.journal_digest:
                raise CustodyMismatch("NON_ADVANCING_WITNESS")
            next_state = WitnessState(self._stream_id, expected.sequence + 1, new_digest)
            appended = self._event(next_state.sequence, new_digest, current[1])
            if self._path.stat().st_size + len(appended) > MAX_BYTES:
                raise CustodyMismatch("WITNESS_CAPACITY")
            try:
                fd = os.open(
                    self._path, os.O_WRONLY | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0)
                )
                with os.fdopen(fd, "ab") as handle:
                    handle.write(appended)
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as error:
                raise CustodyMismatch("WITNESS_APPEND_FAILED") from error
            return next_state
