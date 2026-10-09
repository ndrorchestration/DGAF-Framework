"""Additional negative QA for persistent evidence admission and rollback limitations."""
import shutil
import pytest
from experiments.sbcf.durable_evidence import DurableEvidenceVerifier
from experiments.sbcf.signed_evidence import sign

KEY = {"broker": b"synthetic-only-key"}
FIELDS = {"broker": frozenset({"capabilities"})}
def envelope(sequence, state=None, policy="P"):
    value = {"source": "broker", "run": "R", "policy": policy, "nonce": "N", "sequence": sequence, "state": {"capabilities": 0} if state is None else state}
    value["signature"] = sign(value, KEY["broker"])
    return value

def verifier(path):
    return DurableEvidenceVerifier(path, KEY, FIELDS)

def accept(v, record, policy="P"):
    return v.admit(record, expected_run="R", expected_policy=policy, expected_nonce="N")

def test_source_field_exclusion(tmp_path):
    v = verifier(tmp_path / "state.sqlite")
    assert not accept(v, envelope(1, {"workers": 0}))

def test_modified_payload_fails_signature(tmp_path):
    v = verifier(tmp_path / "state.sqlite")
    r = envelope(1)
    r["state"]["capabilities"] = 99
    assert not accept(v, r)

def test_high_water_survives_reopen(tmp_path):
    p = tmp_path / "state.sqlite"
    assert accept(verifier(p), envelope(10))
    assert not accept(verifier(p), envelope(9))

@pytest.mark.xfail(strict=True, reason="Known limitation: restoring a prior DB snapshot rolls back replay state; independent anti-rollback anchor required")
def test_snapshot_restore_must_not_readmit_old_event(tmp_path):
    p = tmp_path / "state.sqlite"
    backup = tmp_path / "backup.sqlite"
    v = verifier(p)
    assert accept(v, envelope(1))
    shutil.copy2(p, backup)
    assert accept(v, envelope(2))
    shutil.copy2(backup, p)
    assert not accept(verifier(p), envelope(2))
