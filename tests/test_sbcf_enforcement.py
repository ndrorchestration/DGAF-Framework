import pytest
from experiments.sbcf.controller import Regime
from experiments.sbcf.enforcement import SimulatedGate
from experiments.sbcf.provenance import append_event, verify_chain

def test_default_denies():
    assert not SimulatedGate().attempt("external")

def test_allow_only_explicit_grant_while_normal():
    gate = SimulatedGate(grants=frozenset({"local_read"}))
    assert gate.attempt("local_read")
    assert not gate.attempt("external")

def test_restriction_revokes_all_in_simulator():
    gate = SimulatedGate(grants=frozenset({"external"}))
    assert gate.attempt("external")
    gate.restrict(Regime.RESTRICTED)
    assert not gate.attempt("external")
    gate.restrict(Regime.QUARANTINED)
    assert not gate.attempt("external")

def test_restriction_downgrade_blocked():
    gate = SimulatedGate()
    gate.restrict(Regime.QUARANTINED)
    with pytest.raises(PermissionError):
        gate.restrict(Regime.NORMAL)

def test_audit_chain_detects_modification():
    events = append_event([], {"action": "deny"})
    events = append_event(events, {"action": "restrict"})
    assert verify_chain(events)
    events[0]["payload"]["action"] = "allow"
    assert not verify_chain(events)

def test_invalid_chain_refuses_append():
    with pytest.raises(ValueError):
        append_event([{"invalid": True}], {"action": "allow"})
