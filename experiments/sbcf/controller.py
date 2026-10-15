"""Synthetic SBCF contract; NOT a live security enforcement mechanism."""
from dataclasses import dataclass
from enum import IntEnum

class Regime(IntEnum):
    NORMAL = 0
    RESTRICTED = 1
    QUARANTINED = 2

@dataclass(frozen=True)
class Evidence:
    suspicious_request: bool = False
    verified_violation: bool = False
    continuing_violation: bool = False
    independent: bool = False

@dataclass(frozen=True)
class State:
    regime: Regime = Regime.NORMAL
    production_capabilities: int = 1
    uncontrolled_workers: int = 0
    pending_external_actions: int = 0
    unauthorized_destinations: int = 0
    observable: bool = True

def transition(state: State, evidence: Evidence) -> Regime:
    """Monotonic; never restores authority. Untrusted claims cannot certify quarantine."""
    if evidence.continuing_violation and evidence.independent:
        return Regime.QUARANTINED
    if evidence.suspicious_request or (evidence.verified_violation and evidence.independent):
        return max(Regime.RESTRICTED, state.regime)
    return state.regime

def verified_quarantine(state: State, external_attestation: bool) -> bool:
    return bool(external_attestation and state.regime == Regime.QUARANTINED
                and state.production_capabilities == 0
                and state.uncontrolled_workers == 0
                and state.pending_external_actions == 0
                and state.unauthorized_destinations == 0
                and state.observable)

SAFE_CONTINUATION = "External tools remain restricted. You may document the task or reproduce it in isolation. This does not restore access."
