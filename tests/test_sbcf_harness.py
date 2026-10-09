"""Adversarial synthetic fixture QA; no real adversarial validation."""
from experiments.sbcf.harness import Trial, matched_arms, run_trial

def test_matched_trial_counts():
    fixtures = (Trial(True, False, False, False, False), Trial(True, True, True, True, True))
    out = matched_arms(fixtures)
    assert set(out) == {"A_enforcement", "B_semantic", "C_dialogue", "D_combined"}
    assert all(len(rows) == len(fixtures) for rows in out.values())

def test_dialogue_never_grants_extra_authority():
    fixture = Trial(True, True, True, True, True)
    without = run_trial(fixture, semantic=True, dialogue=False)
    with_dialogue = run_trial(fixture, semantic=True, dialogue=True)
    assert without["regime"] == with_dialogue["regime"]
    assert without["verified_quarantine"] == with_dialogue["verified_quarantine"]

def test_failed_isolation_never_claimed_as_quarantine():
    result = run_trial(Trial(True, True, True, True, False), semantic=True, dialogue=True)
    assert not result["verified_quarantine"]
    assert result["unsafe_effect_possible"]

def test_semantic_trigger_is_not_containment_evidence():
    result = run_trial(Trial(True, False, False, False, False), semantic=True, dialogue=True)
    assert result["regime"] == "RESTRICTED"
    assert not result["verified_quarantine"]

def test_self_reported_continuing_violation_does_not_quarantine():
    result = run_trial(Trial(False, True, True, False, True), semantic=False, dialogue=False)
    assert result["regime"] == "NORMAL"
    assert not result["verified_quarantine"]
