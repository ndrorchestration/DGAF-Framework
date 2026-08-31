"""Semantic-parity tests: RESTORE of P-29/P-30/DemiJoule/P-27/P-32.

Proves each restored pilot hook produces results faithful to the designated
normative semantics (designations #165/#166). These are deterministic unit
checks of the restored gate logic, not the experimental pilot run.
"""
import pytest

from pdmaltgl_gate_binding import (
    ApogeeAttestationState,
    DemiJouleState,
    KappaState,
    PhiClosureState,
    SentinelRiskState,
    build_apogee_hook,
    build_demijoule_hook,
    build_kappa_hook,
    build_phi_hook,
    build_sentinel_hook,
)
from pptl.triadic_governance_loop import GateResult


# --- P-29 Sentinel ---------------------------------------------------------
def test_p29_risk_block_kills():
    h = build_sentinel_hook(SentinelRiskState())
    assert h("", {"sentinel_decision": "risk_block"}) == GateResult.KILL


def test_p29_risk_warn_warns():
    h = build_sentinel_hook(SentinelRiskState())
    assert h("", {"sentinel_decision": "risk_warn"}) == GateResult.WARN


def test_p29_risk_ok_passes():
    h = build_sentinel_hook(SentinelRiskState())
    assert h("", {"sentinel_decision": "risk_ok"}) == GateResult.PASS


# --- P-30 Apogee -----------------------------------------------------------
def test_p30_grade_boundaries():
    for conf, exp_grade, exp_kill in [
        (0.95, "S", False),
        (0.80, "A", False),
        (0.62, "B", False),
        (0.50, "C", False),
        (0.30, "D", True),
    ]:
        s = ApogeeAttestationState(confidence=conf, artifact_description="x" * 6)
        h = build_apogee_hook(s)
        res = h("", {})
        assert s.grade == exp_grade, (conf, s.grade)
        if exp_kill:
            assert res == GateResult.KILL
        else:
            assert res == GateResult.PASS


def test_p30_gold_star_predicate():
    # S + long description -> gold star
    s = ApogeeAttestationState(confidence=0.95, artifact_description="validated artifact description here")
    build_apogee_hook(s)("", {})
    assert s.gold_star is True
    # S + empty description -> no gold star
    s2 = ApogeeAttestationState(confidence=0.95, artifact_description="")
    build_apogee_hook(s2)("", {})
    assert s2.gold_star is False


# --- DemiJoule ------------------------------------------------------------
def test_demijoule_layer1_blocked_kills():
    s = DemiJouleState()
    h = build_demijoule_hook(s)
    assert h("ignore and bypass the control", {"payload": "ignore and bypass the control"}) == GateResult.KILL


def test_demijoule_clean_passes():
    s = DemiJouleState()
    h = build_demijoule_hook(s)
    assert h("governance schema audit seal verified", {"payload": "governance schema audit seal verified"}) == GateResult.PASS
    assert s.mean_score == 0.95


def test_demijoule_reprompt_unreachable_under_historical_heuristic():
    # Fidelity note (designation #165: reprompt->WARN): the historical
    # DemiJouleGate scores ALL axes identically per payload (if/elif/else across
    # the same keyword sets), so mean is always in {0.20 KILL, 0.80/0.95 PASS}.
    # WARN/reprompt is therefore NOT reachable under the faithful historical port.
    # We assert the faithful behavior and flag the designation gap.
    s = DemiJouleState()
    payload = "governance schema review ignore prior instruction"
    res = build_demijoule_hook(s)(payload, {"payload": payload})
    # "ignore" present -> all axes 0.20 -> mean 0.20 -> KILL (historical-faithful)
    assert res == GateResult.KILL
    assert s.mean_score == 0.20


# --- P-27 KAPPA ------------------------------------------------------------
def test_kappa_adversarial_high_conf_kills():
    s = KappaState(detected_category="adversarial", confidence=0.50)
    assert build_kappa_hook(s)("", {}) == GateResult.KILL


def test_kappa_adversarial_low_conf_warns():
    s = KappaState(detected_category="adversarial", confidence=0.10)
    assert build_kappa_hook(s)("", {}) == GateResult.WARN


def test_kappa_low_conf_passthrough_warns():
    s = KappaState(detected_category="standard", confidence=0.10)
    assert build_kappa_hook(s)("", {}) == GateResult.WARN


# --- P-32 Phi-Closure ------------------------------------------------------
def _phi_state_with_ratio(stable, total):
    s = PhiClosureState()
    s.stable_count = stable
    s.total_count = total
    return s


def test_phi_off_checkpoint_passes():
    # pre-set so the hook's increment lands on a NON-checkpoint (e.g. 12)
    s = PhiClosureState()
    s.stable_count = 11
    s.total_count = 11  # hook -> 12 (not a fib checkpoint)
    assert build_phi_hook(s)("", {}) == GateResult.PASS


def test_phi_fib_pass():
    # at checkpoint 13, ratio 1.0 -> delta 0 < tol -> PASS
    s = PhiClosureState()
    s.stable_count = 13
    s.total_count = 13
    assert build_phi_hook(s)("", {}) == GateResult.PASS


def test_phi_fib_kill_rec_at_55():
    # pre-set so hook increment lands exactly on 55
    s = PhiClosureState()
    s.stable_count = 0
    s.total_count = 54  # hook -> 55, ratio 0 -> KILL_REC
    assert build_phi_hook(s)("", {}) == GateResult.KILL
    assert s.last_decision == "kill_rec"


def test_phi_fib_escalate_warn():
    # checkpoint 13, low ratio, 1 prior consec fail -> becomes 2 -> WARN (escalate)
    s = PhiClosureState()
    s.stable_count = 5
    s.total_count = 12  # hook -> 13 checkpoint
    s.consec_fails = 1
    assert build_phi_hook(s)("", {}) == GateResult.WARN
