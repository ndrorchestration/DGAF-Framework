"""Durability and field-binding synthetic QA; not secure remote attestation."""
from experiments.sbcf.durable_evidence import DurableEvidenceVerifier
from experiments.sbcf.signed_evidence import sign

KEYS = {"broker": b"toy-broker", "registry": b"toy-registry"}
FIELDS = {"broker": frozenset({"capabilities"}), "registry": frozenset({"workers"})}
def envelope(source="broker", sequence=1, state=None):
    data = dict(source=source, run="R", policy="P", nonce="N", sequence=sequence, state=state if state is not None else {"capabilities": 0})
    data["signature"] = sign(data, KEYS[source])
    return data
def make(path):
    return DurableEvidenceVerifier(path, KEYS, FIELDS)
def check(v, r):
    return v.admit(r, expected_run="R", expected_policy="P", expected_nonce="N")
def test_restart_replay_rejected(tmp_path):
    path = tmp_path / "replay.db"
    assert check(make(path), envelope())
    assert not check(make(path), envelope())
    assert check(make(path), envelope(sequence=2))
def test_lower_sequence_rejected(tmp_path):
    v = make(tmp_path / "replay.db")
    assert check(v, envelope(sequence=10))
    assert not check(v, envelope(sequence=9))
def test_field_authority_rejected_even_when_signed(tmp_path):
    v = make(tmp_path / "replay.db")
    assert not check(v, envelope(state={"workers": 0}))
def test_registered_registry_field(tmp_path):
    v = make(tmp_path / "replay.db")
    assert check(v, envelope(source="registry", state={"workers": 0}))
def test_duplicate_idempotency_rejected(tmp_path):
    v = make(tmp_path / "replay.db")
    r = envelope()
    assert check(v, r)
    assert not check(v, r)
def test_invalid_signature_does_not_consume_sequence(tmp_path):
    v = make(tmp_path / "replay.db")
    r = envelope()
    r["signature"] = "0" * 64
    assert not check(v, r)
    assert check(v, envelope())
