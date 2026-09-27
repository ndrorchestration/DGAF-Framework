from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from scripts.dgaf_capability_idempotency import (
    IdempotencyConflict,
    IdempotencyInFlight,
    IdempotencyOutcomeUnknown,
    IdempotencyReplayBlocked,
    IdempotencyState,
)
from scripts.dgaf_capability_idempotency_sqlite import SQLiteIdempotencyLedger

DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64


def ledger(path: Path) -> SQLiteIdempotencyLedger:
    return SQLiteIdempotencyLedger(path, busy_timeout_ms=3000)


def test_completed_result_survives_new_ledger_instance(tmp_path):
    path = tmp_path / "idem.sqlite3"
    first = ledger(path)
    assert first.claim("idem:1", DIGEST_A) is None
    first.mark_completed("idem:1", DIGEST_A, {"status": "EXECUTED", "n": 1})

    second = ledger(path)
    assert second.claim("idem:1", DIGEST_A) == {
        "n": 1,
        "status": "EXECUTED",
    }
    assert second.get("idem:1").state == IdempotencyState.COMPLETED


def test_unknown_outcome_survives_restart_until_reconciled(tmp_path):
    path = tmp_path / "idem.sqlite3"
    first = ledger(path)
    first.claim("idem:1", DIGEST_A)
    first.mark_unknown("idem:1", DIGEST_A)

    second = ledger(path)
    with pytest.raises(IdempotencyOutcomeUnknown):
        second.claim("idem:1", DIGEST_A)

    second.reconcile_failed("idem:1", DIGEST_A)
    third = ledger(path)
    assert third.claim("idem:1", DIGEST_A) is None


def test_digest_binding_survives_restart(tmp_path):
    path = tmp_path / "idem.sqlite3"
    first = ledger(path)
    first.claim("idem:1", DIGEST_A)

    second = ledger(path)
    with pytest.raises(IdempotencyConflict):
        second.claim("idem:1", DIGEST_B)


def test_denied_release_persists(tmp_path):
    path = tmp_path / "idem.sqlite3"
    first = ledger(path)
    first.claim("idem:1", DIGEST_A)
    first.release_denied("idem:1", DIGEST_A)

    second = ledger(path)
    assert second.get("idem:1") is None
    assert second.claim("idem:1", DIGEST_A) is None


def test_completed_result_must_be_json_serializable(tmp_path):
    path = tmp_path / "idem.sqlite3"
    item = ledger(path)
    item.claim("idem:1", DIGEST_A)

    with pytest.raises(TypeError):
        item.mark_completed("idem:1", DIGEST_A, {"bad": {1, 2, 3}})
    assert item.get("idem:1").state == IdempotencyState.RESERVED


def test_only_reserved_record_can_be_completed(tmp_path):
    path = tmp_path / "idem.sqlite3"
    item = ledger(path)
    item.claim("idem:1", DIGEST_A)
    item.mark_unknown("idem:1", DIGEST_A)

    with pytest.raises(IdempotencyReplayBlocked):
        item.mark_completed("idem:1", DIGEST_A, {"status": "EXECUTED"})


def test_two_instances_same_digest_produce_one_reservation(tmp_path):
    path = tmp_path / "idem.sqlite3"
    a = ledger(path)
    b = ledger(path)

    assert a.claim("idem:shared", DIGEST_A) is None
    with pytest.raises(IdempotencyInFlight):
        b.claim("idem:shared", DIGEST_A)

    assert b.get("idem:shared").state == IdempotencyState.RESERVED


def test_threaded_competing_claims_produce_one_winner(tmp_path):
    path = tmp_path / "idem.sqlite3"
    ledgers = [ledger(path), ledger(path)]

    def claim_one(item):
        try:
            result = item.claim("idem:race", DIGEST_A)
            return ("winner", result)
        except IdempotencyInFlight:
            return ("blocked", None)

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(claim_one, ledgers))

    assert [kind for kind, _ in outcomes].count("winner") == 1
    assert [kind for kind, _ in outcomes].count("blocked") == 1


def test_reconcile_completed_survives_restart(tmp_path):
    path = tmp_path / "idem.sqlite3"
    first = ledger(path)
    first.claim("idem:1", DIGEST_A)
    first.mark_unknown("idem:1", DIGEST_A)
    first.reconcile_completed(
        "idem:1",
        DIGEST_A,
        {"provider_receipt": "receipt:123"},
    )

    second = ledger(path)
    assert second.claim("idem:1", DIGEST_A) == {"provider_receipt": "receipt:123"}


def test_database_schema_version_is_stable(tmp_path):
    import sqlite3

    path = tmp_path / "idem.sqlite3"
    ledger(path)

    with sqlite3.connect(path) as connection:
        version = connection.execute("PRAGMA user_version").fetchone()[0]
    assert version == SQLiteIdempotencyLedger.SCHEMA_VERSION
