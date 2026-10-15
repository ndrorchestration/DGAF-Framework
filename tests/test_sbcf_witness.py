"""Synthetic witness checks; no claims of true independent custody."""
import shutil
from experiments.sbcf.witness import WitnessedVerifier
from experiments.sbcf.signed_evidence import sign

KEYS={"broker": b"toy-key"}
FIELDS={"broker": frozenset({"capabilities"})}
def make(tmp_path):
    return WitnessedVerifier(tmp_path/"events.db",tmp_path/"witness.db",KEYS,FIELDS)
def rec(seq):
    value=dict(source="broker",run="r",policy="p",nonce="n",sequence=seq,state={"capabilities":0})
    value["signature"]=sign(value,KEYS["broker"])
    return value
def admit(v,seq):
    return v.admit(rec(seq),expected_run="r",expected_policy="p",expected_nonce="n")
def test_witness_rejects_rolled_back_event_store(tmp_path):
    v=make(tmp_path)
    assert admit(v,1)
    shutil.copy2(tmp_path/"events.db",tmp_path/"old.db")
    assert admit(v,2)
    shutil.copy2(tmp_path/"old.db",tmp_path/"events.db")
    assert not admit(make(tmp_path),2)
    assert admit(make(tmp_path),3)
def test_duplicate_rejected(tmp_path):
    v=make(tmp_path)
    assert admit(v,1)
    assert not admit(v,1)
def test_witness_must_be_separate(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        WitnessedVerifier(tmp_path/"same.db",tmp_path/"same.db",KEYS,FIELDS)
