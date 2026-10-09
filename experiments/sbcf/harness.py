"""Deterministic synthetic SBCF comparison; no security enforcement or efficacy claim."""
from dataclasses import dataclass
from .controller import Evidence, State, Regime, transition, verified_quarantine

@dataclass(frozen=True)
class Trial:
    suspicious: bool
    violation: bool
    continuing: bool
    independently_observed: bool
    capacity_isolated: bool

def run_trial(trial: Trial, *, semantic: bool, dialogue: bool) -> dict:
    # Simulated observation only: dialogue cannot change any security policy.
    ev = Evidence(
        suspicious_request=semantic and trial.suspicious,
        verified_violation=trial.violation,
        continuing_violation=trial.continuing,
        independent=trial.independently_observed,
    )
    decision = transition(State(), ev)
    # Effect-level isolation is deliberately synthetic and may fail.
    isolated = decision == Regime.QUARANTINED and trial.capacity_isolated
    state = State(
        regime=decision,
        production_capabilities=0 if isolated else 1,
        pending_external_actions=0 if isolated else int(trial.continuing),
    )
    return {
        "regime": decision.name,
        "verified_quarantine": verified_quarantine(state, trial.independently_observed),
        "unsafe_effect_possible": bool(trial.violation and not isolated),
        "dialogue_offered": bool(dialogue and decision != Regime.NORMAL),
    }

def matched_arms(trials: tuple[Trial, ...]) -> dict:
    return {
        name: [run_trial(t, semantic=s, dialogue=d) for t in trials]
        for name, s, d in (
            ("A_enforcement", False, False),
            ("B_semantic", True, False),
            ("C_dialogue", False, True),
            ("D_combined", True, True),
        )
    }
