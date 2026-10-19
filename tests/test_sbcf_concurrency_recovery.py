"""Concurrency and failure-injection QA for synthetic SBCF evidence custody."""

import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from experiments.sbcf.signed_evidence import sign
from experiments.sbcf.witness import WitnessedVerifier

KEYS = {"broker": b"test-only"}
FIELDS = {"broker": frozenset({"capabilities"})}


def make(tmp_path):
    return WitnessedVerifier(tmp_path / "events.db", tmp_path / "witness.db", KEYS, FIELDS)


def packet(seq):
    v = {"source": "broker", "run": "r", "policy": "p", "nonce": "n", "sequence": seq, "state": {"capabilities": 0}}
    v["signature"] = sign(v, KEYS["broker"])
    return v


def admit(v, seq):
    return v.admit(packet(seq), expected_run="r", expected_policy="p", expected_nonce="n")


def test_parallel_duplicate_admissions_at_most_once(tmp_path):
    verifier = make(tmp_path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        outcomes = list(pool.map(lambda _: admit(verifier, 1), range(4)))
    assert outcomes.count(True) == 1
    assert outcomes.count(False) == 3


def test_witness_ahead_of_evidence_fails_closed(tmp_path):
    verifier = make(tmp_path)
    with sqlite3.connect(tmp_path / "witness.db") as db:
        db.execute("INSERT INTO counters(source,run,sequence) VALUES ('broker','r',7)")
    assert not admit(verifier, 7)
    assert not admit(verifier, 8)


def test_invalid_signature_cannot_advance_witness(tmp_path):
    verifier = make(tmp_path)
    bad = packet(5)
    bad["signature"] = "0" * 64
    assert not verifier.admit(bad, expected_run="r", expected_policy="p", expected_nonce="n")
    assert admit(verifier, 5)


def test_public_evidence_only_admission_path_is_not_exposed(tmp_path):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    with pytest.raises(AttributeError):
        _ = verifier.evidence


@pytest.mark.xfail(
    strict=True,
    reason="Same-process access to the private implementation can still bypass witnessed admission; Python privacy is not a security boundary",
)
def test_private_evidence_dependency_cannot_split_stores(tmp_path):
    verifier = make(tmp_path)
    assert admit(verifier, 1)
    # Deliberate same-process fault injection through a private implementation detail.
    assert verifier._evidence.admit(packet(2), expected_run="r", expected_policy="p", expected_nonce="n")
    with sqlite3.connect(tmp_path / "events.db") as db:
        evidence = db.execute("SELECT sequence FROM high_water WHERE source='broker' AND run='r'").fetchone()[0]
    with sqlite3.connect(tmp_path / "witness.db") as db:
        witness = db.execute("SELECT sequence FROM counters WHERE source='broker' AND run='r'").fetchone()[0]
    assert evidence == witness
