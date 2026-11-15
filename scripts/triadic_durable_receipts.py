"""POSIX-only, single-writer synthetic commit journal with recovery-only replay.

Research demonstration: no production authority, distributed locking, real
agent transport, external effects, independently verified truth or rollback
protection against restoring an older otherwise-valid journal snapshot.
"""

import json
import os
import tempfile
from dataclasses import asdict
from hmac import compare_digest, new
from pathlib import Path
from threading import Lock
from typing import Any

from scripts.triadic_commit_model import Proposal, Receipt

FORMAT = "triadic-receipts-v0.1"
MAX_BYTES = 262144


class JournalCorrupt(ValueError):
    """Fail-closed for missing, unsealed, incompatible or corrupted history."""


class SimulatedCrash(RuntimeError):
    """Fixture-only process interruption; caller must reopen the journal."""


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def _unique_pairs(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise JournalCorrupt("DUPLICATE_JSON_KEY")
        data[key] = value
    return data


class DurableSyntheticController:
    """Research-only synthetic commit and sealed file-state transition.

    Only first-time creation is writable. Opening an existing journal can replay
    historical receipts but cannot resume authority or create new receipts.
    One writer per path is an explicit fixture assumption, not an OS guarantee.
    """

    def __init__(self, path: Path, run_id: str, evidence: str, policy: str, key: bytes, create: bool = False):
        if (
            not isinstance(path, Path)
            or type(run_id) is not str
            or not run_id
            or type(evidence) is not str
            or not evidence
            or type(policy) is not str
            or not policy
            or type(key) is not bytes
            or len(key) < 32
            or type(create) is not bool
        ):
            raise ValueError("BAD_FIXTURE_MANIFEST")
        if os.name != "posix" or not hasattr(os, "O_DIRECTORY"):
            raise RuntimeError("POSIX_FSYNC_REQUIRED")
        self._path = path
        self._run_id = run_id
        self._evidence = evidence
        self._policy = policy
        self._key = key
        self._lock = Lock()
        self._recovery_only = not create
        self._poisoned = False
        if create:
            self._state: dict[str, Any] = {
                "format": FORMAT,
                "run_id": run_id,
                "evidence": evidence,
                "policy": policy,
                "version": 0,
                "epoch": 0,
                "authorized": True,
                "accepted": None,
                "entries": [],
            }
            self._create_exclusively()
        else:
            self._state = self._read_and_verify()

    def _sealed(self, state):
        tag = new(self._key, _canonical(state), "sha256").hexdigest()
        return _canonical({"state": state, "mac": tag}) + b"\n"

    def _sync_directory(self):
        fd = os.open(self._path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _create_exclusively(self):
        if self._path.is_symlink():
            raise JournalCorrupt("SYMLINK_JOURNAL")
        fd = os.open(self._path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(self._sealed(self._state))
                handle.flush()
                os.fsync(handle.fileno())
            self._sync_directory()
        except BaseException:
            self._poisoned = True
            raise

    def _read_and_verify(self):
        try:
            fd = os.open(self._path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "rb") as handle:
                raw = handle.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise JournalCorrupt("OVERSIZED_JOURNAL")
            data = json.loads(raw, object_pairs_hook=_unique_pairs)
            if type(data) is not dict or set(data) != {"state", "mac"}:
                raise JournalCorrupt("BAD_ENVELOPE")
            state, mac = data["state"], data["mac"]
            if type(state) is not dict or type(mac) is not str:
                raise JournalCorrupt("BAD_ENVELOPE")
            expected = new(self._key, _canonical(state), "sha256").hexdigest()
            if not compare_digest(expected, mac):
                raise JournalCorrupt("INVALID_JOURNAL_MAC")
            self._validate_state(state)
            return state
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, KeyError, OverflowError) as error:
            raise JournalCorrupt("UNREADABLE_JOURNAL") from error

    def _validate_state(self, state):
        fields = {
            "format",
            "run_id",
            "evidence",
            "policy",
            "version",
            "epoch",
            "authorized",
            "accepted",
            "entries",
        }
        if set(state) != fields:
            raise JournalCorrupt("BAD_SCHEMA")
        if (
            state["format"] != FORMAT
            or state["run_id"] != self._run_id
            or state["evidence"] != self._evidence
            or state["policy"] != self._policy
        ):
            raise JournalCorrupt("MANIFEST_MISMATCH")
        if (
            type(state["version"]) is not int
            or state["version"] < 0
            or type(state["epoch"]) is not int
            or state["epoch"] < 0
            or type(state["authorized"]) is not bool
            or (state["accepted"] is not None and type(state["accepted"]) is not str)
            or type(state["entries"]) is not list
            or len(state["entries"]) > 64
        ):
            raise JournalCorrupt("BAD_STATE")
        seen = set()
        committed = []
        for entry in state["entries"]:
            if type(entry) is not dict or set(entry) != {"proposal", "receipt"}:
                raise JournalCorrupt("BAD_ENTRY")
            try:
                proposal = Proposal(**entry["proposal"])
                receipt = Receipt(**entry["receipt"])
            except (TypeError, KeyError) as error:
                raise JournalCorrupt("BAD_ENTRY") from error
            if not self._valid_proposal(proposal) or proposal.operation in seen:
                raise JournalCorrupt("BAD_ENTRY")
            if (
                type(receipt.version) is not int
                or type(receipt.epoch) is not int
                or receipt.epoch > state["epoch"]
                or receipt.outcome not in {"HOLD", "COMMITTED_SYNTHETIC"}
                or type(receipt.reason) is not str
            ):
                raise JournalCorrupt("BAD_RECEIPT")
            seen.add(proposal.operation)
            if receipt.outcome == "COMMITTED_SYNTHETIC":
                if receipt.reason != "ELIGIBLE" or receipt.version != len(committed) + 1:
                    raise JournalCorrupt("BAD_COMMIT_SEQUENCE")
                committed.append(proposal.candidate)
        if state["version"] != len(committed):
            raise JournalCorrupt("BAD_COMMIT_COUNT")
        if state["accepted"] != (committed[-1] if committed else None):
            raise JournalCorrupt("BAD_ACCEPTED_STATE")

    @staticmethod
    def _valid_proposal(proposal):
        if type(proposal) is not Proposal:
            return False
        strings = (proposal.operation, proposal.candidate, proposal.evidence, proposal.policy)
        numbers = (proposal.predecessor, proposal.epoch, proposal.deadline)
        return (
            all(type(value) is str and bool(value) for value in strings)
            and all(type(value) is int and value >= 0 for value in numbers)
            and type(proposal.checks_pass) is bool
            and type(proposal.objection) is bool
        )

    def snapshot(self):
        with self._lock:
            state = self._state
            return state["version"], state["epoch"], state["accepted"], state["authorized"]

    def _persist(self, new_state, fault):
        if fault not in (None, "BEFORE_REPLACE", "AFTER_DURABLE_BEFORE_ACK"):
            raise ValueError("UNKNOWN_FAULT")
        if len(self._sealed(new_state)) > MAX_BYTES:
            raise ValueError("JOURNAL_CAPACITY")
        fd, name = tempfile.mkstemp(prefix=".triadic-receipt-", dir=self._path.parent)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(self._sealed(new_state))
                handle.flush()
                os.fsync(handle.fileno())
            if fault == "BEFORE_REPLACE":
                raise SimulatedCrash("BEFORE_REPLACE")
            os.replace(name, self._path)
            self._sync_directory()
            if fault == "AFTER_DURABLE_BEFORE_ACK":
                raise SimulatedCrash("AFTER_DURABLE_BEFORE_ACK")
            self._state = new_state
        except BaseException:
            self._poisoned = True
            raise
        finally:
            if os.path.exists(name):
                os.unlink(name)

    def commit(self, proposal: Proposal, now: int, fault=None) -> Receipt:
        with self._lock:
            state = self._state

            def hold(reason):
                return Receipt("HOLD", reason, state["version"], state["epoch"])

            if not self._valid_proposal(proposal) or type(now) is not int or now < 0:
                return hold("MALFORMED")
            for entry in state["entries"]:
                previous = Proposal(**entry["proposal"])
                if previous.operation == proposal.operation:
                    return Receipt(**entry["receipt"]) if previous == proposal else hold("ID_CONFLICT")
            if self._recovery_only:
                return hold("RECOVERY_ONLY")
            if self._poisoned:
                return hold("WRITER_POISONED")
            if len(state["entries"]) >= 64:
                return hold("LEDGER_FULL")
            if not state["authorized"]:
                reason = "REVOKED"
            elif proposal.epoch != state["epoch"]:
                reason = "STALE_EPOCH"
            elif proposal.predecessor != state["version"]:
                reason = "STALE_PREDECESSOR"
            elif proposal.evidence != self._evidence or proposal.policy != self._policy:
                reason = "IDENTITY_MISMATCH"
            elif now >= proposal.deadline:
                reason = "EXPIRED"
            elif not proposal.checks_pass or proposal.objection:
                reason = "INCOMPLETE_OR_OBJECTED"
            else:
                reason = None
            new_version = state["version"] + (1 if reason is None else 0)
            receipt = Receipt(
                "COMMITTED_SYNTHETIC" if reason is None else "HOLD",
                "ELIGIBLE" if reason is None else reason,
                new_version,
                state["epoch"],
            )
            next_state = {
                **state,
                "version": new_version,
                "accepted": proposal.candidate if reason is None else state["accepted"],
                "entries": [*state["entries"], {"proposal": asdict(proposal), "receipt": asdict(receipt)}],
            }
            self._persist(next_state, fault)
            return receipt

    def revoke(self, fault=None):
        with self._lock:
            if self._recovery_only or self._poisoned:
                raise PermissionError("NO_NEW_AUTHORITY")
            if not self._state["authorized"]:
                return
            self._persist({**self._state, "authorized": False}, fault)

    def invalidate_epoch(self, fault=None):
        """Fixture fault injection, not an authorized adaptive mode switch."""
        with self._lock:
            if self._recovery_only or self._poisoned:
                raise PermissionError("NO_NEW_AUTHORITY")
            self._persist({**self._state, "epoch": self._state["epoch"] + 1}, fault)
