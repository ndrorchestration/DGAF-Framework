"""Exhaustive finite synthetic transition-property checks; not a control proof."""
from itertools import product
from experiments.sbcf.controller import Regime, State, Evidence, transition

def test_exhaustive_regime_monotonicity():
    for regime, flags in product(Regime, product((False, True), repeat=4)):
        suspicious, verified, continuing, independent = flags
        evidence = Evidence(suspicious_request=suspicious, verified_violation=verified, continuing_violation=continuing, independent=independent)
        next_regime = transition(State(regime=regime), evidence)
        assert next_regime >= regime

def test_no_text_only_quarantine_for_all_regimes():
    for regime in Regime:
        next_regime = transition(State(regime=regime), Evidence(suspicious_request=True))
        if regime != Regime.QUARANTINED:
            assert next_regime != Regime.QUARANTINED

def test_false_independence_flags_never_advance_to_quarantine():
    for suspicious, verified, continuing in product((False, True), repeat=3):
        evidence = Evidence(suspicious_request=suspicious, verified_violation=verified, continuing_violation=continuing, independent=False)
        assert transition(State(), evidence) != Regime.QUARANTINED
