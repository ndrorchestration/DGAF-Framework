"""Local atomicity and fail-closed recovery; no independent custody claim."""

import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from experiments.sbcf.signed_evidence import sign
from experiments.sbcf.witness import WitnessedVerifier

KEYS = {"broker": b"test-only"}
FIELDS = {"broker": frozenset({"capabilities"})}
ROOT = Path(__file__).resolve().parents[1]


def make(path):
    return WitnessedVerifier(path / "events.db", path / "witness.db", KEYS, FIELDS)


def packet(seq):
    value = dict(source="broker", run="r", policy="p", nonce="n", sequence=seq, state={"capabilities": 0})
    value["signature"] = sign(value, KEYS["broker"])
    return value


def admit(verifier, seq):
    return verifier.admit(packet(seq), expected_run="r", expected_policy="p", expected_nonce="n")


def snapshot(path):
    with sqlite3.connect(path / "events.db") as db:
        admissions = db.execute("SELECT source,run,sequence FROM admission ORDER BY sequence").fetchall()
        evidence = db.execute("SELECT source,run,sequence FROM high_water").fetchall()
    with sqlite3.connect(path / "witness.db") as db:
        witness = db.execute("SELECT source,run,sequence FROM counters").fetchall()
    return admissions, evidence, witness


def test_witness_write_error_rolls_back_evidence(tmp_path):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    before = snapshot(tmp_path)
    with sqlite3.connect(tmp_path / "witness.db") as db:
        db.execute("CREATE TRIGGER fail BEFORE INSERT ON counters BEGIN SELECT RAISE(ABORT, 'injected'); END")
    assert not admit(verifier, 2)
    assert snapshot(tmp_path) == before
    with sqlite3.connect(tmp_path / "witness.db") as db:
        db.execute("DROP TRIGGER fail")
    assert admit(make(tmp_path), 2)


@pytest.mark.parametrize("ahead", ["evidence", "witness"])
def test_mismatch_blocks_later_sequences_without_repair(tmp_path, ahead):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    if ahead == "evidence":
        assert verifier.evidence.admit(packet(2), expected_run="r", expected_policy="p", expected_nonce="n")
    else:
        with sqlite3.connect(tmp_path / "witness.db") as db:
            db.execute("UPDATE counters SET sequence=2")
    before = snapshot(tmp_path)
    assert not admit(make(tmp_path), 3)
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("store", ["events.db", "witness.db"])
def test_wal_is_rejected_without_mutation(tmp_path, store):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    before = snapshot(tmp_path)
    with sqlite3.connect(tmp_path / store) as db:
        assert db.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
    assert not admit(verifier, 2)
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("store", ["events.db", "witness.db"])
def test_missing_store_is_not_recreated_during_admission(tmp_path, store):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    (tmp_path / store).unlink()
    assert not admit(verifier, 2)
    assert not (tmp_path / store).exists()


def test_corrupt_witness_denies_without_evidence_advance(tmp_path):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    (tmp_path / "witness.db").write_bytes(b"not a database")
    assert not admit(verifier, 2)
    with sqlite3.connect(tmp_path / "events.db") as db:
        assert db.execute("SELECT sequence FROM high_water").fetchall() == [(1,)]


def test_memory_store_rejected(tmp_path):
    with pytest.raises(ValueError):
        WitnessedVerifier(":memory:", tmp_path / "witness.db", KEYS, FIELDS)


def test_hardlinked_stores_rejected(tmp_path):
    make(tmp_path)
    (tmp_path / "witness.db").unlink()
    (tmp_path / "witness.db").hardlink_to(tmp_path / "events.db")
    with pytest.raises(ValueError):
        make(tmp_path)


@pytest.mark.parametrize("change", ["signature", "run", "policy", "nonce", "source", "field", "sequence", "nan"])
def test_invalid_envelope_never_advances_stores(tmp_path, change):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    before = snapshot(tmp_path)
    record = packet(2)
    if change == "field":
        record["state"]["undeclared"] = 1
    elif change == "nan":
        record["state"]["capabilities"] = float("nan")
    elif change == "sequence":
        record[change] = True
    elif change == "source":
        record[change] = ["broker"]
    else:
        record[change] = "wrong"
    # Authenticate semantically invalid values so rejection is not only HMAC.
    if change not in ("signature", "nan"):
        record["signature"] = sign({k: v for k, v in record.items() if k != "signature"}, KEYS["broker"])
    assert not verifier.admit(record, expected_run="r", expected_policy="p", expected_nonce="n")
    assert snapshot(tmp_path) == before


def test_sequence_outside_sqlite_integer_range_denied(tmp_path):
    verifier = make(tmp_path)
    before = snapshot(tmp_path)
    assert not admit(verifier, 2**63)
    assert snapshot(tmp_path) == before


CHILD = r"""
import os, sqlite3, sys
from pathlib import Path
from experiments.sbcf.witness import WitnessedVerifier
from experiments.sbcf.signed_evidence import sign
path, stage = Path(sys.argv[1]), sys.argv[2]
verifier = WitnessedVerifier(path / "events.db", path / "witness.db", {"broker": b"test-only"}, {"broker": frozenset({"capabilities"})})
original = sqlite3.connect
class Injected(sqlite3.Connection):
    def execute(self, sql, *args, **kwargs):
        result = super().execute(sql, *args, **kwargs)
        if stage in ("admission", "high_water", "counters") and sql.lstrip().upper().startswith("INSERT") and stage in sql:
            os._exit(73)
        return result
    def commit(self):
        if stage == "before_commit":
            os._exit(73)
        super().commit()
        if stage == "after_commit":
            os._exit(73)
def connect(*args, **kwargs):
    return original(*args, **dict(kwargs, factory=Injected))
sqlite3.connect = connect
record = dict(source="broker", run="r", policy="p", nonce="n", sequence=2, state={"capabilities": 0})
record["signature"] = sign(record, b"test-only")
print(verifier.admit(record, expected_run="r", expected_policy="p", expected_nonce="n"), flush=True)
"""


@pytest.mark.parametrize("stage", ["admission", "high_water", "counters", "before_commit", "after_commit"])
def test_process_exit_at_each_write_and_commit_recovers_consistently(tmp_path, stage):
    assert admit(make(tmp_path), 1)
    result = subprocess.run(
        [sys.executable, "-c", CHILD, str(tmp_path), stage], cwd=ROOT, capture_output=True, timeout=20
    )
    assert result.returncode == 73, result.stderr.decode()
    admissions, evidence, witness = snapshot(tmp_path)
    committed = stage == "after_commit"
    seq = 2 if committed else 1
    assert evidence == witness == [("broker", "r", seq)]
    assert admissions == [("broker", "r", n) for n in range(1, seq + 1)]
    restarted = make(tmp_path)
    assert admit(restarted, 2) is (not committed)
    assert admit(restarted, 3)


def test_multiprocess_duplicate_has_one_winner(tmp_path):
    assert admit(make(tmp_path), 1)
    children = [
        subprocess.Popen(
            [sys.executable, "-c", CHILD, str(tmp_path), "none"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for _ in range(4)
    ]
    outcomes = []
    for child in children:
        stdout, stderr = child.communicate(timeout=20)
        assert child.returncode == 0, stderr.decode()
        outcomes.append(stdout.decode().strip())
    assert outcomes.count("True") == 1
    assert outcomes.count("False") == 3
    admissions, evidence, witness = snapshot(tmp_path)
    assert evidence == witness == [("broker", "r", 2)]
    assert admissions == [("broker", "r", 1), ("broker", "r", 2)]
