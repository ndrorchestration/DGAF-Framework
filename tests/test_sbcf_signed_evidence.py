"""Synthetic HMAC fixture tests; keys are test secrets, NOT independent trust anchors."""
from copy import deepcopy
from experiments.sbcf.signed_evidence import EvidenceVerifier, sign

KEYS = {"enforcer": b"fake-enforcer-key", "registry": b"fake-registry-key"}
def record(source="enforcer", seq=1):
    r = dict(source=source, run="run-1", policy="policy-1", nonce="nonce-1", sequence=seq, state={"blocked": True})
    r["signature"] = sign(r, KEYS[source])
    return r

def verify(verifier, r):
    return verifier.admit(r, expected_run="run-1", expected_policy="policy-1", expected_nonce="nonce-1")

def test_valid_signature():
    assert verify(EvidenceVerifier(KEYS), record())

def test_replay_denied():
    v = EvidenceVerifier(KEYS)
    r = record()
    assert verify(v, r)
    assert not verify(v, r)

def test_tamper_denied():
    r = record()
    r["state"]["blocked"] = False
    assert not verify(EvidenceVerifier(KEYS), r)

def test_swapped_identity_denied():
    r = record()
    r["source"] = "registry"
    assert not verify(EvidenceVerifier(KEYS), r)

def test_other_run_denied():
    r = record()
    r["run"] = "run-2"
    assert not verify(EvidenceVerifier(KEYS), r)

def test_unknown_source_denied():
    r = record()
    r["source"] = "agent"
    assert not verify(EvidenceVerifier(KEYS), r)

def test_reject_boolean_sequence():
    r = record()
    r["sequence"] = True
    r["signature"] = sign({k:v for k,v in r.items() if k != "signature"}, KEYS["enforcer"])
    assert not verify(EvidenceVerifier(KEYS), r)

def test_reject_extra_field_even_with_valid_signature():
    r = record()
    r["extra"] = "untrusted"
    assert not verify(EvidenceVerifier(KEYS), r)
