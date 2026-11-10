"""Disposable monotonic custody fixture for the synthetic durable journal.

This in-memory witness is not durable or external in deployment. It models an
independently retained, monotonic digest/sequence authority in one Python run.
No secure hardware, remote attestations, OS crash testing, or real permissions.
"""

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path
from threading import Lock
from typing import Callable

from scripts.triadic_commit_model import Proposal, Receipt
from scripts.triadic_durable_receipts import DurableSyntheticController, SimulatedCrash

MAX_JOURNAL_BYTES = 262144
FAULTS = frozenset(
    {None, "BEFORE_REPLACE", "AFTER_JOURNAL_BEFORE_WITNESS", "AFTER_WITNESS_BEFORE_ACK", "WITNESS_REFUSED"}
)


class CustodyMismatch(RuntimeError):
    """A missing, stale or divergent witness is a blocking condition."""


@dataclass(frozen=True)
class WitnessState:
    stream_id: str
    sequence: int
    journal_digest: str


class FixtureMonotonicWitness:
    """Explicit trust assumption: state survives while a fixture object lives.

    A replacement or rollback of this object defeats this model. There is no
    production service, independent custody, authenticated caller or storage.
    """

    def __init__(self, stream_id: str):
        if type(stream_id) is not str or not stream_id:
            raise ValueError("BAD_WITNESS_STREAM")
        self._stream_id = stream_id
        self._lock = Lock()
        self._state: WitnessState | None = None

    def snapshot(self) -> WitnessState | None:
        with self._lock:
            return self._state

    def initialize(self, digest: str) -> WitnessState:
        if not _is_digest(digest):
            raise ValueError("BAD_DIGEST")
        with self._lock:
            if self._state is not None:
                raise CustodyMismatch("ALREADY_INITIALIZED")
            self._state = WitnessState(self._stream_id, 0, digest)
            return self._state

    def advance(self, expected: WitnessState, new_digest: str) -> WitnessState:
        if type(expected) is not WitnessState or not _is_digest(new_digest):
            raise ValueError("BAD_WITNESS_UPDATE")
        with self._lock:
            if self._state is None or self._state != expected:
                raise CustodyMismatch("STALE_WITNESS")
            if new_digest == expected.journal_digest:
                raise CustodyMismatch("NON_ADVANCING_WITNESS")
            self._state = WitnessState(self._stream_id, expected.sequence + 1, new_digest)
            return self._state


def _is_digest(value: object) -> bool:
    return type(value) is str and len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _journal_digest(path: Path) -> str:
    """No journal mutation. A symlink or missing/oversized journal fails closed."""
    try:
        if path.is_symlink():
            raise CustodyMismatch("SYMLINK_JOURNAL")
        with path.open("rb") as handle:
            raw = handle.read(MAX_JOURNAL_BYTES + 1)
    except OSError as error:
        raise CustodyMismatch("UNREADABLE_JOURNAL") from error
    if len(raw) > MAX_JOURNAL_BYTES:
        raise CustodyMismatch("OVERSIZED_JOURNAL")
    return sha256(raw).hexdigest()


def _verified_snapshot(path: Path, run_id: str, witness: FixtureMonotonicWitness) -> WitnessState:
    state = witness.snapshot()
    if state is None:
        raise CustodyMismatch("MISSING_WITNESS")
    if state.stream_id != run_id:
        raise CustodyMismatch("WRONG_WITNESS_STREAM")
    if not compare_digest(_journal_digest(path), state.journal_digest):
        raise CustodyMismatch("JOURNAL_WITNESS_DIVERGENCE")
    if witness.snapshot() != state:
        raise CustodyMismatch("WITNESS_CHANGED_DURING_READ")
    return state


class WitnessedSyntheticController:
    """Single-writer adapter; all recovered controller objects remain replay-only.

    Journal writes happen before witness CAS. A crash in between is detected
    but NOT repaired or promoted. Same-process locks are not process leases.
    """

    def __init__(
        self,
        path: Path,
        run_id: str,
        witness: FixtureMonotonicWitness,
        controller: DurableSyntheticController,
    ):
        self._path = path
        self._run_id = run_id
        self._witness = witness
        self._controller = controller
        self._lock = Lock()
        self._poisoned = False

    @classmethod
    def create(
        cls,
        path: Path,
        run_id: str,
        evidence: str,
        policy: str,
        key: bytes,
        witness: FixtureMonotonicWitness,
    ) -> "WitnessedSyntheticController":
        if type(witness) is not FixtureMonotonicWitness:
            raise ValueError("BAD_WITNESS")
        if witness.snapshot() is not None:
            raise CustodyMismatch("ALREADY_INITIALIZED")
        if witness._stream_id != run_id:
            raise CustodyMismatch("WRONG_WITNESS_STREAM")
        controller = DurableSyntheticController(path, run_id, evidence, policy, key, create=True)
        witness.initialize(_journal_digest(path))
        return cls(path, run_id, witness, controller)

    @staticmethod
    def recover(
        path: Path,
        run_id: str,
        evidence: str,
        policy: str,
        key: bytes,
        witness: FixtureMonotonicWitness,
    ) -> DurableSyntheticController:
        if type(witness) is not FixtureMonotonicWitness:
            raise ValueError("BAD_WITNESS")
        old = _verified_snapshot(path, run_id, witness)
        reader = DurableSyntheticController(path, run_id, evidence, policy, key)
        if _verified_snapshot(path, run_id, witness) != old:
            raise CustodyMismatch("WITNESS_CHANGED_DURING_READ")
        return reader

    def snapshot(self) -> tuple[int, int, str | None, bool]:
        with self._lock:
            _verified_snapshot(self._path, self._run_id, self._witness)
            return self._controller.snapshot()

    def _apply(self, operation: Callable[[str | None], Receipt | None], fault: str | None) -> Receipt | None:
        if fault not in FAULTS:
            raise ValueError("UNKNOWN_FAULT")
        with self._lock:
            if self._poisoned:
                raise CustodyMismatch("WRITER_QUARANTINED")
            previous = _verified_snapshot(self._path, self._run_id, self._witness)
            underlying_fault = {
                "BEFORE_REPLACE": "BEFORE_REPLACE",
                "AFTER_JOURNAL_BEFORE_WITNESS": "AFTER_DURABLE_BEFORE_ACK",
            }.get(fault)
            try:
                result = operation(underlying_fault)
                latest = _journal_digest(self._path)
                if not compare_digest(previous.journal_digest, latest):
                    if fault == "WITNESS_REFUSED":
                        raise SimulatedCrash("WITNESS_REFUSED")
                    self._witness.advance(previous, latest)
                    if fault == "AFTER_WITNESS_BEFORE_ACK":
                        raise SimulatedCrash("AFTER_WITNESS_BEFORE_ACK")
                return result
            except BaseException:
                self._poisoned = True
                raise

    def commit(self, proposal: Proposal, now: int, fault: str | None = None) -> Receipt:
        result = self._apply(lambda inner: self._controller.commit(proposal, now, fault=inner), fault)
        assert isinstance(result, Receipt)
        return result

    def revoke(self, fault: str | None = None) -> None:
        self._apply(lambda inner: self._controller.revoke(fault=inner), fault)

    def invalidate_epoch(self, fault: str | None = None) -> None:
        """Synthetic fault injection, not an authorized adaptive-mode transition."""
        self._apply(lambda inner: self._controller.invalidate_epoch(fault=inner), fault)
