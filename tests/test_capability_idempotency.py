from __future__ import annotations

import pytest

from scripts.dgaf_capability_idempotency import (
    IdempotencyConflict,
    IdempotencyInFlight,
    IdempotencyOutcomeUnknown,
    IdempotencyState,
    InMemoryIdempotencyLedger,
)

DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64


def test_inflight_duplicate_is_blocked():
    ledger = InMemoryIdempotencyLedger()
    assert ledger.claim("idem:1", DIGEST_A) is None

    with pytest.raises(IdempotencyInFlight):
        ledger.claim("idem:1", DIGEST_A)

    assert ledger.get("idem:1").state == IdempotencyState.RESERVED


def test_same_key_with_different_digest_is_conflict():
    ledger = InMemoryIdempotencyLedger()
    ledger.claim("idem:1", DIGEST_A)

    with pytest.raises(IdempotencyConflict):
        ledger.claim("idem:1", DIGEST_B)


def test_completed_result_is_returned_without_new_reservation():
    ledger = InMemoryIdempotencyLedger()
    ledger.claim("idem:1", DIGEST_A)
    result = {"execution_state": "EXECUTED"}
    ledger.mark_completed("idem:1", DIGEST_A, result)

    assert ledger.claim("idem:1", DIGEST_A) is result
    assert ledger.get("idem:1").state == IdempotencyState.COMPLETED


def test_unknown_outcome_blocks_retry_until_reconciled():
    ledger = InMemoryIdempotencyLedger()
    ledger.claim("idem:1", DIGEST_A)
    ledger.mark_unknown("idem:1", DIGEST_A)

    with pytest.raises(IdempotencyOutcomeUnknown):
        ledger.claim("idem:1", DIGEST_A)

    ledger.reconcile_failed("idem:1", DIGEST_A)
    assert ledger.claim("idem:1", DIGEST_A) is None


def test_denied_reservation_can_be_released_and_reused():
    ledger = InMemoryIdempotencyLedger()
    ledger.claim("idem:1", DIGEST_A)
    ledger.release_denied("idem:1", DIGEST_A)

    assert ledger.get("idem:1") is None
    assert ledger.claim("idem:1", DIGEST_A) is None
