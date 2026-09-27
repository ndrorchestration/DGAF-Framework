from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class IdempotencyState(str, Enum):
    RESERVED = "RESERVED"
    COMPLETED = "COMPLETED"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


class IdempotencyConflict(RuntimeError):
    """A key was reused for a materially different action digest."""


class IdempotencyReplayBlocked(RuntimeError):
    """Base class for unsafe retry states."""


class IdempotencyOutcomeUnknown(IdempotencyReplayBlocked):
    """Retry is unsafe until the prior uncertain outcome is reconciled."""


class IdempotencyInFlight(IdempotencyReplayBlocked):
    """Retry is unsafe while the original invocation is still reserved."""


@dataclass
class IdempotencyRecord:
    key: str
    action_digest: str
    state: IdempotencyState
    result: Any | None = None


class InMemoryIdempotencyLedger:
    """Reference-only ledger for deterministic replay semantics.

    This is intentionally process-local and is not a production persistence
    mechanism. It exists to make the authority/replay contract executable.
    """

    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord] = {}

    def claim(self, key: str, action_digest: str) -> Any | None:
        existing = self._records.get(key)
        if existing is None:
            self._records[key] = IdempotencyRecord(
                key=key,
                action_digest=action_digest,
                state=IdempotencyState.RESERVED,
            )
            return None

        if existing.action_digest != action_digest:
            raise IdempotencyConflict("idempotency key is already bound to a different action digest")

        if existing.state == IdempotencyState.COMPLETED:
            return existing.result

        if existing.state == IdempotencyState.OUTCOME_UNKNOWN:
            raise IdempotencyOutcomeUnknown("idempotency outcome is unknown; reconciliation is required before retry")
        raise IdempotencyInFlight("idempotency key is already reserved by an in-flight transaction")

    def mark_completed(self, key: str, action_digest: str, result: Any) -> None:
        record = self._require_matching(key, action_digest)
        record.state = IdempotencyState.COMPLETED
        record.result = result

    def mark_unknown(self, key: str, action_digest: str) -> None:
        record = self._require_matching(key, action_digest)
        record.state = IdempotencyState.OUTCOME_UNKNOWN
        record.result = None

    def release_denied(self, key: str, action_digest: str) -> None:
        record = self._require_matching(key, action_digest)
        if record.state != IdempotencyState.RESERVED:
            raise IdempotencyReplayBlocked("only a reserved idempotency record may be released after denial")
        del self._records[key]

    def reconcile_completed(self, key: str, action_digest: str, result: Any) -> None:
        record = self._require_matching(key, action_digest)
        if record.state != IdempotencyState.OUTCOME_UNKNOWN:
            raise IdempotencyReplayBlocked("only an unknown outcome may be reconciled to completed")
        record.state = IdempotencyState.COMPLETED
        record.result = result

    def reconcile_failed(self, key: str, action_digest: str) -> None:
        record = self._require_matching(key, action_digest)
        if record.state != IdempotencyState.OUTCOME_UNKNOWN:
            raise IdempotencyReplayBlocked("only an unknown outcome may be reconciled to failed")
        del self._records[key]

    def get(self, key: str) -> IdempotencyRecord | None:
        return self._records.get(key)

    def _require_matching(self, key: str, action_digest: str) -> IdempotencyRecord:
        record = self._records.get(key)
        if record is None:
            raise IdempotencyReplayBlocked("idempotency key is not reserved")
        if record.action_digest != action_digest:
            raise IdempotencyConflict("idempotency key is bound to a different action digest")
        return record
