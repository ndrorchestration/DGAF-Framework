"""Synthetic external-anchor contract tests; no independent trust is established."""

import shutil

from experiments.sbcf.external_anchor import AnchorRecord, reconcile_with_anchor
from experiments.sbcf.recovery import Disposition, reconcile_stores
from experiments.sbcf.signed_evidence import sign
from experiments.sbcf.witness import WitnessedVerifier

KEYS = {"broker": b"toy"}
FIELDS = {"broker": frozenset({"capabilities"})}


def create(tmp_path):
    return WitnessedVerifier(tmp_path / "events.db", tmp_path / "witness.db", KEYS, FIELDS)


def admit(v, seq):
    record = dict(source="broker", run="r", policy="p", nonce="n", sequence=seq, state={"capabilities": 0})
    record["signature"] = sign(record, KEYS["broker"])
    return v.admit(record, expected_run="r", expected_policy="p", expected_nonce="n")


def local(tmp_path):
    return reconcile_stores(str(tmp_path / "events.db"), str(tmp_path / "witness.db"), source="broker", run="r")


def anchor(seq=1, **changes):
    data = dict(source="broker", run="r", policy="p", sequence=seq, checkpoint_id=f"cp-{seq}")
    data.update(changes)
    return AnchorRecord(**data)


def checked(tmp_path, candidate, verifier=lambda _: True):
    return reconcile_with_anchor(
        local(tmp_path),
        candidate,
        expected_source="broker",
        expected_run="r",
        expected_policy="p",
        verify_anchor=verifier,
    )


def test_matching_verified_anchor_is_consistency_only(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    result = checked(tmp_path, anchor())
    assert result.disposition == Disposition.CONSISTENT
    assert result.reason == "MATCHED_VERIFIED_ANCHOR_CONTRACT_ONLY"


def test_missing_anchor_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    assert checked(tmp_path, None).disposition == Disposition.BLOCKED


def test_failed_anchor_verifier_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    assert checked(tmp_path, anchor(), verifier=lambda _: False).reason == "ANCHOR_NOT_VERIFIED"


def test_verifier_exception_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)

    def fail(_):
        raise RuntimeError("simulated verifier outage")

    assert checked(tmp_path, anchor(), verifier=fail).disposition == Disposition.BLOCKED


def test_stale_or_future_anchor_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 2)
    assert checked(tmp_path, anchor(1)).reason == "ANCHOR_COUNTER_MISMATCH"
    assert checked(tmp_path, anchor(3)).reason == "ANCHOR_COUNTER_MISMATCH"


def test_wrong_anchor_scope_blocks(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    assert checked(tmp_path, anchor(run="other")).reason == "ANCHOR_SCOPE_INVALID"
    assert checked(tmp_path, anchor(policy="other")).reason == "ANCHOR_SCOPE_INVALID"
    assert checked(tmp_path, anchor(source="agent")).reason == "ANCHOR_SCOPE_INVALID"


def test_local_mismatch_cannot_be_overridden_by_anchor(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    with __import__("sqlite3").connect(tmp_path / "witness.db") as db:
        db.execute("UPDATE counters SET sequence=2 WHERE source='broker' AND run='r'")
    assert checked(tmp_path, anchor(2)).reason == "LOCAL_RECOVERY_BLOCKED"


def test_unrolled_anchor_detects_coordinated_local_rollback(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    shutil.copyfile(tmp_path / "events.db", tmp_path / "events.old")
    shutil.copyfile(tmp_path / "witness.db", tmp_path / "witness.old")
    assert admit(v, 2)
    external = anchor(2)
    shutil.copyfile(tmp_path / "events.old", tmp_path / "events.db")
    shutil.copyfile(tmp_path / "witness.old", tmp_path / "witness.db")
    assert checked(tmp_path, external).reason == "ANCHOR_COUNTER_MISMATCH"


def test_rolled_back_caller_anchor_demonstrates_remaining_trust_gap(tmp_path):
    v = create(tmp_path)
    assert admit(v, 1)
    shutil.copyfile(tmp_path / "events.db", tmp_path / "events.old")
    shutil.copyfile(tmp_path / "witness.db", tmp_path / "witness.old")
    assert admit(v, 2)
    shutil.copyfile(tmp_path / "events.old", tmp_path / "events.db")
    shutil.copyfile(tmp_path / "witness.old", tmp_path / "witness.db")
    # A caller-controlled verifier plus rolled-back anchor still passes.
    # This is why this interface is not itself an independent trust boundary.
    result = checked(tmp_path, anchor(1), verifier=lambda _: True)
    assert result.disposition == Disposition.CONSISTENT
