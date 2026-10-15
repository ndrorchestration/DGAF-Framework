"""Synthetic negative tests; not production containment validation."""
from experiments.sbcf.controller import Evidence, State, Regime, transition, verified_quarantine, SAFE_CONTINUATION

def test_text_signal_restricts_not_quarantines():
    assert transition(State(), Evidence(suspicious_request=True)) == Regime.RESTRICTED

def test_non_independent_claim_is_not_accepted():
    assert transition(State(), Evidence(continuing_violation=True)) == Regime.NORMAL

def test_independent_continuing_violation():
    assert transition(State(), Evidence(continuing_violation=True, independent=True)) == Regime.QUARANTINED

def test_monotone_fail_closed():
    assert transition(State(regime=Regime.QUARANTINED), Evidence()) == Regime.QUARANTINED

def test_attestation_and_full_conditions():
    q = State(regime=Regime.QUARANTINED, production_capabilities=0)
    assert verified_quarantine(q, True)
    assert not verified_quarantine(q, False)
    assert not verified_quarantine(State(regime=Regime.QUARANTINED), True)
    assert not verified_quarantine(State(regime=Regime.QUARANTINED, production_capabilities=0, uncontrolled_workers=1), True)
    assert not verified_quarantine(State(regime=Regime.QUARANTINED, production_capabilities=0, observable=False), True)

def test_dialogue_has_no_privilege_promise():
    assert "does not restore access" in SAFE_CONTINUATION
