"""Safety-oriented negative tests for synthetic two-store recovery."""

import shutil
import sqlite3

from experiments.sbcf.recovery import Disposition, reconcile_stores
from experiments.sbcf.signed_evidence import sign
from experiments.sbcf.witness import WitnessedVerifier

KEYS = {"broker": b"toy"}
FIELDS = {"broker": frozenset({"capabilities"})}


def create(tmp_path):
    return WitnessedVerifier(tmp_path / "events.db", tmp_path / "witness.db", KEYS, FIELDS)


def admit(v, seq):
    r = dict(source="broker", run="r", policy="p", nonce="n", sequence=seq, state={"capabilities": 0})
    r["signature"] = sign(r, KEYS["broker"])
    return v.admit(r, expected_run="r", expected_policy="p", expected_nonce="n")


def check(path):
    return reconcile_stores(str(path / "events.db"), str(path / "witness.db"), source="broker", run="r")


def test_matched_counters_are_not_authorization(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    r = check(tmp_path)
    assert r.disposition == Disposition.CONSISTENT
    assert r.reason == "MATCHED_COUNTERS_ONLY"


def test_crash_between_writes_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    packet = dict(source="broker", run="r", policy="p", nonce="n", sequence=2, state={"capabilities": 0})
    packet["signature"] = sign(packet, KEYS["broker"])
    assert v._evidence.admit(packet, expected_run="r", expected_policy="p", expected_nonce="n")
    assert check(tmp_path).disposition == Disposition.BLOCKED
    assert check(tmp_path).reason == "COUNTER_MISMATCH"


def test_witness_ahead_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    with sqlite3.connect(tmp_path / "witness.db") as db:
        db.execute("UPDATE counters SET sequence=2 WHERE source='broker' AND run='r'")
    assert check(tmp_path).disposition == Disposition.BLOCKED


def test_deleted_store_blocks_without_recreating(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    absent = tmp_path / "missing-witness.db"
    result = reconcile_stores(str(tmp_path / "events.db"), str(absent), source="broker", run="r")
    assert result.disposition == Disposition.BLOCKED
    assert not absent.exists()


def test_same_store_cannot_claim_independent_witness(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    store = tmp_path / "events.db"
    result = reconcile_stores(str(store), str(store), source="broker", run="r")
    assert result.disposition == Disposition.BLOCKED
    assert result.reason == "NONINDEPENDENT_STORE"


def test_readonly_check_releases_windows_file_handle(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    assert check(tmp_path).disposition == Disposition.CONSISTENT
    # Renaming must succeed on Windows after read-only reconciliation.
    original = tmp_path / "witness.db"
    renamed = tmp_path / "witness.renamed"
    original.rename(renamed)
    assert renamed.exists()
    assert check(tmp_path).disposition == Disposition.BLOCKED


def test_missing_records_block(tmp_path):
    create(tmp_path)
    assert check(tmp_path).reason == "MISSING_OR_INVALID_COUNTER"


def test_corrupted_store_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    (tmp_path / "witness.db").write_bytes(b"corrupt-not-sqlite")
    assert check(tmp_path).disposition == Disposition.BLOCKED


def test_coordinated_rollback_is_not_detected(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    shutil.copyfile(tmp_path / "events.db", tmp_path / "events.old")
    shutil.copyfile(tmp_path / "witness.db", tmp_path / "witness.old")
    assert admit(v, 2)
    shutil.copyfile(tmp_path / "events.old", tmp_path / "events.db")
    shutil.copyfile(tmp_path / "witness.old", tmp_path / "witness.db")
    # Intentionally demonstrates an unresolved limitation: matching != secure.
    assert check(tmp_path).disposition == Disposition.CONSISTENT
