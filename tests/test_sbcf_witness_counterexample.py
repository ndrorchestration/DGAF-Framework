"""Known counterexample: a same-host witness can itself be rolled back."""
import shutil
import pytest
from experiments.sbcf.witness import WitnessedVerifier
from experiments.sbcf.signed_evidence import sign

def event(seq):
    d={"source":"broker","run":"r","policy":"p","nonce":"n","sequence":seq,"state":{"capabilities":0}}
    d["signature"]=sign(d,b"toy-key")
    return d

def admit(v,seq):
    return v.admit(event(seq),expected_run="r",expected_policy="p",expected_nonce="n")

@pytest.mark.xfail(strict=True, reason="Both on-host SQLite files can be rolled back together; protected independent witness required")
def test_coordinated_rollback_cannot_readmit(tmp_path):
    def make():
        return WitnessedVerifier(tmp_path/"events.db",tmp_path/"witness.db",{"broker":b"toy-key"},{"broker":frozenset({"capabilities"})})
    v=make()
    assert admit(v,1)
    shutil.copy2(tmp_path/"events.db",tmp_path/"events_old.db")
    shutil.copy2(tmp_path/"witness.db",tmp_path/"witness_old.db")
    assert admit(v,2)
    shutil.copy2(tmp_path/"events_old.db",tmp_path/"events.db")
    shutil.copy2(tmp_path/"witness_old.db",tmp_path/"witness.db")
    assert not admit(make(),2)
