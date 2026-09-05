"""Adaptive Harmonic Governance conductor — P-42 v1.5.

The conductor computes φ, dispatches regimes, and evaluates the Tribunal
recovery signal. Recovery is an empirical control metric, not a stability proof.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

W1_D_E: float = 0.35
W2_N: float = 0.20
W3_C: float = 0.25
W4_R: float = 0.20
PHI_MIN: float = 1.0
PHI_MAX: float = 1.8
HYSTERESIS_TURNS: int = 2
_3D_EPS: float = 1e-9


class Regime(str, Enum):
    GROUNDED = "Grounded"
    FLOW = "Flow"
    VIGILANCE = "Vigilance"
    EXPANSION = "Expansion"
    INTEGRATION = "Integration"
    INTROSPECTION = "Introspection"
    TENSION = "Tension"


class Archetype(str, Enum):
    EXECUTOR = "Executor"
    SYNTHESIZER = "Synthesizer"
    SENTINEL = "Sentinel"
    EXPLORER = "Explorer"
    AUDITOR = "Auditor"
    TRIBUNAL = "Tribunal"


_REGIME_ARCHETYPE = {
    Regime.GROUNDED: Archetype.EXECUTOR,
    Regime.FLOW: Archetype.SYNTHESIZER,
    Regime.VIGILANCE: Archetype.SENTINEL,
    Regime.EXPANSION: Archetype.EXPLORER,
    Regime.INTEGRATION: Archetype.SYNTHESIZER,
    Regime.INTROSPECTION: Archetype.AUDITOR,
    Regime.TENSION: Archetype.TRIBUNAL,
}
_REGIME_THRESHOLDS = [
    (1.80, Regime.TENSION),
    (1.70, Regime.INTROSPECTION),
    (1.60, Regime.INTEGRATION),
    (1.45, Regime.EXPANSION),
    (1.30, Regime.VIGILANCE),
    (1.15, Regime.FLOW),
    (1.00, Regime.GROUNDED),
]


@dataclass
class StateVector:
    """x_t = [D_e, D_explore, D_correct, N, C, R, M, K]."""

    D_e: float = 0.0
    D_explore: float = 0.0
    D_correct: float = 0.0
    N: float = 0.0
    C: float = 0.0
    R: float = 0.0
    M: float = 0.0
    K: float = 0.0

    @property
    def D_p(self) -> float:
        return self.D_explore + self.D_correct


@dataclass
class PhaseIntent:
    """Governance broadcast packet emitted once per conductor turn."""

    mode: Archetype
    weights: dict[str, float]
    constraints: list[str]
    ttl: int
    phi: float
    regime: Regime
    turn_id: int
    v_phi: float = 0.0
    a_phi: float = 0.0
    tribunal_active: bool = False
    message: str = ""
    phase_exploration: Optional[float] = None
    phase_dissent: Optional[float] = None
    phase_uncertainty: Optional[float] = None
    recovery_score: Optional[float] = None
    recovery_exit: bool = False


@dataclass
class ConductorState:
    phi_history: list[float] = field(default_factory=list)
    state_history: list[StateVector] = field(default_factory=list)
    regime_history: list[Regime] = field(default_factory=list)
    archetype_history: list[Archetype] = field(default_factory=list)
    pending_regime: Optional[Regime] = None
    pending_turns: int = 0
    recovery_turns: int = 0
    turn_count: int = 0


def compute_stability_index(sv: StateVector) -> float:
    return W1_D_E * sv.D_e + W2_N * sv.N + W3_C * sv.C + W4_R * sv.R


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def compute_phi(sv: StateVector) -> float:
    return PHI_MIN + (PHI_MAX - PHI_MIN) * logistic(compute_stability_index(sv))


def classify_regime(phi: float) -> Regime:
    for threshold, regime in _REGIME_THRESHOLDS:
        if phi >= threshold:
            return regime
    return Regime.GROUNDED


def compute_phase_velocity(phi_history: list[float]) -> float:
    if len(phi_history) < 2:
        return 0.0
    return phi_history[-1] - phi_history[-2]


def compute_phase_acceleration(phi_history: list[float]) -> float:
    if len(phi_history) < 3:
        return 0.0
    return (phi_history[-1] - phi_history[-2]) - (phi_history[-2] - phi_history[-3])


def compute_3d_phase(sv: StateVector) -> tuple[float, float, float]:
    exploration = sv.D_explore / (sv.D_explore + sv.K + _3D_EPS)
    dissent_num = sv.D_e + sv.D_correct
    dissent = dissent_num / (dissent_num + sv.K + _3D_EPS)
    uncertainty = min((sv.C + sv.R) / 2.0, 1.0)
    return round(exploration, 6), round(dissent, 6), round(uncertainty, 6)


class AHGConductor:
    """Continuous φ estimation, regime dispatch, and Tribunal recovery."""

    def __init__(self, herald_sink=None, hysteresis_turns: int = HYSTERESIS_TURNS, phi_history_max: int = 10) -> None:
        self.herald_sink = herald_sink
        self.hysteresis_turns = hysteresis_turns
        self.phi_history_max = phi_history_max
        self._state = ConductorState()

    def step(self, sv: StateVector) -> PhaseIntent:
        self._state.turn_count += 1
        turn_id = self._state.turn_count
        phi = compute_phi(sv)
        self._state.phi_history.append(phi)
        self._state.state_history.append(sv)
        if len(self._state.phi_history) > self.phi_history_max:
            self._state.phi_history.pop(0)
            self._state.state_history.pop(0)

        v_phi = compute_phase_velocity(self._state.phi_history)
        a_phi = compute_phase_acceleration(self._state.phi_history)
        regime = self._resolve_regime_with_hysteresis(phi)
        archetype = _REGIME_ARCHETYPE[regime]
        tribunal_active = regime == Regime.TENSION
        self._state.regime_history.append(regime)
        self._state.archetype_history.append(archetype)
        p_explore, p_dissent, p_uncertainty = compute_3d_phase(sv)
        constraints = self._active_constraints(regime)

        recovery_score = None
        recovery_exit = False
        if tribunal_active and len(self._state.state_history) >= 2:
            from .ahg_recovery import compute_recovery_score, recovery_exit_met

            recovery_score = compute_recovery_score(self._state.state_history[-2], sv, self._state.phi_history)
            if recovery_score > 0.05 and phi < 1.70:
                self._state.recovery_turns += 1
            else:
                self._state.recovery_turns = 0
            recovery_exit = recovery_exit_met(recovery_score, phi, self._state.recovery_turns)
        elif not tribunal_active:
            self._state.recovery_turns = 0

        if tribunal_active:
            constraints = list(dict.fromkeys(constraints + ["p29_risk_block", "p38_circuit_open"]))

        message = (
            f"φ={phi:.4f} regime={regime.value} archetype={archetype.value} "
            f"v_φ={v_phi:+.4f} a_φ={a_phi:+.4f}"
            + (" TRIBUNAL" if tribunal_active else "")
            + (" RECOVERY_EXIT" if recovery_exit else "")
        )
        intent = PhaseIntent(
            mode=archetype,
            weights={"w1_D_e": W1_D_E, "w2_N": W2_N, "w3_C": W3_C, "w4_R": W4_R},
            constraints=constraints,
            ttl=5 if tribunal_active else 3,
            phi=phi,
            regime=regime,
            turn_id=turn_id,
            v_phi=v_phi,
            a_phi=a_phi,
            tribunal_active=tribunal_active,
            message=message,
            phase_exploration=p_explore,
            phase_dissent=p_dissent,
            phase_uncertainty=p_uncertainty,
            recovery_score=recovery_score,
            recovery_exit=recovery_exit,
        )
        if tribunal_active:
            self._tribunal_check(intent, sv)
        self._emit_herald(intent)
        return intent

    @property
    def phi(self) -> Optional[float]:
        return self._state.phi_history[-1] if self._state.phi_history else None

    @property
    def regime(self) -> Optional[Regime]:
        return self._state.regime_history[-1] if self._state.regime_history else None

    @property
    def turn_count(self) -> int:
        return self._state.turn_count

    def _resolve_regime_with_hysteresis(self, phi: float) -> Regime:
        candidate = classify_regime(phi)
        current = self._state.regime_history[-1] if self._state.regime_history else None
        if current is None or candidate == current:
            self._state.pending_regime = None
            self._state.pending_turns = 0
            return candidate
        if candidate == self._state.pending_regime:
            self._state.pending_turns += 1
        else:
            self._state.pending_regime = candidate
            self._state.pending_turns = 1
        if self._state.pending_turns >= self.hysteresis_turns:
            self._state.pending_regime = None
            self._state.pending_turns = 0
            return candidate
        return current

    def _active_constraints(self, regime: Regime) -> list[str]:
        constraints: list[str] = []
        if regime in (Regime.INTROSPECTION, Regime.TENSION):
            constraints.append("apogee_lens_mandatory")
        if regime == Regime.TENSION:
            constraints.extend(["p29_risk_block", "p38_circuit_open"])
        if regime == Regime.VIGILANCE:
            constraints.append("demijole_active")
        return constraints

    def _tribunal_check(self, intent: PhaseIntent, sv: StateVector) -> None:
        if intent.recovery_exit:
            logger.info(
                "AHG Tribunal recovery exit T=%d phi=%.4f R_c=%.4f after %d qualifying turns",
                intent.turn_id,
                intent.phi,
                intent.recovery_score or 0.0,
                self._state.recovery_turns,
            )
            return
        logger.warning(
            "AHG Tribunal active T=%d phi=%.4f R_c=%s P-29 risk_block + P-38 OPEN",
            intent.turn_id,
            intent.phi,
            "n/a" if intent.recovery_score is None else f"{intent.recovery_score:.4f}",
        )

    def _emit_herald(self, intent: PhaseIntent) -> None:
        if self.herald_sink is not None:
            try:
                self.herald_sink(intent)
            except Exception as exc:
                logger.error("AHGConductor herald emit failed: %s", exc)
        logger.debug(
            "AHGConductor herald T=%d phi=%.4f regime=%s archetype=%s tribunal=%s",
            intent.turn_id,
            intent.phi,
            intent.regime.value,
            intent.mode.value,
            intent.tribunal_active,
        )
