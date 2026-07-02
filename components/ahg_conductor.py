"""
ahg_conductor.py — Adaptive Harmonic Governance Conductor
P-42 · Layer 12 — Cognitive Control Plane · v1.3 scaffold
Amethyst × COLLEEN · S072 · 2026-07-02

Spec: docs/theory/AHG_ARCHITECTURE.md v1.2
Pattern card: patterns/P-42_AHG.md v1.3-card

Status: SCAFFOLD — φ computation, regime dispatch, and hysteresis
        are implemented. Tribunal recovery protocol and Phase Intent
        broadcast are stubbed for v1.4 wiring to live agent stack.
"""

from __future__ import annotations

import math
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants — canonical weights from AHG_ARCHITECTURE.md §2.2
# ---------------------------------------------------------------------------

W1_D_E: float = 0.35   # Destabilizing Entropy weight
W2_N: float   = 0.20   # Novelty weight
W3_C: float   = 0.25   # Constraint Pressure weight
W4_R: float   = 0.20   # Revision Pressure weight

PHI_MIN: float = 1.0
PHI_MAX: float = 1.8

# Hysteresis: archetype transition requires φ to cross band edge for
# this many consecutive turns before dispatch changes (§2.4)
HYSTERESIS_TURNS: int = 2


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Regime(str, Enum):
    GROUNDED      = "Grounded"       # φ 1.00–1.15
    FLOW          = "Flow"           # φ 1.15–1.30
    VIGILANCE     = "Vigilance"      # φ 1.30–1.45
    EXPANSION     = "Expansion"      # φ 1.45–1.60
    INTEGRATION   = "Integration"    # φ 1.60–1.70  ← NDR-STASIS φ=1.618
    INTROSPECTION = "Introspection"  # φ 1.70–1.80
    TENSION       = "Tension"        # φ > 1.80


class Archetype(str, Enum):
    EXECUTOR      = "Executor"
    SYNTHESIZER   = "Synthesizer"
    SENTINEL      = "Sentinel"
    EXPLORER      = "Explorer"
    AUDITOR       = "Auditor"
    TRIBUNAL      = "Tribunal"


# Regime → primary archetype mapping (§3 regime table)
_REGIME_ARCHETYPE: dict[Regime, Archetype] = {
    Regime.GROUNDED:      Archetype.EXECUTOR,
    Regime.FLOW:          Archetype.SYNTHESIZER,
    Regime.VIGILANCE:     Archetype.SENTINEL,
    Regime.EXPANSION:     Archetype.EXPLORER,
    Regime.INTEGRATION:   Archetype.SYNTHESIZER,  # + Auditor secondary
    Regime.INTROSPECTION: Archetype.AUDITOR,
    Regime.TENSION:       Archetype.TRIBUNAL,
}

# φ lower-bound for each regime (upper bound = next regime's lower bound)
_REGIME_THRESHOLDS: list[tuple[float, Regime]] = [
    (1.80, Regime.TENSION),
    (1.70, Regime.INTROSPECTION),
    (1.60, Regime.INTEGRATION),
    (1.45, Regime.EXPANSION),
    (1.30, Regime.VIGILANCE),
    (1.15, Regime.FLOW),
    (1.00, Regime.GROUNDED),
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class StateVector:
    """x_t = [D_e, D_explore, D_correct, N, C, R, M, K] — AHG_ARCHITECTURE §2.1"""
    D_e:       float = 0.0  # Destabilizing Entropy
    D_explore: float = 0.0  # Exploratory Divergence
    D_correct: float = 0.0  # Corrective Dissent
    N:         float = 0.0  # Novelty
    C:         float = 0.0  # Constraint Pressure
    R:         float = 0.0  # Revision Pressure
    M:         float = 0.0  # Governance Momentum (hysteresis EMA)
    K:         float = 0.0  # Coherence

    @property
    def D_p(self) -> float:
        """Productive Divergence = D_explore + D_correct (2-subtype model)"""
        return self.D_explore + self.D_correct


@dataclass
class PhaseIntent:
    """I_t broadcast packet — AHG_ARCHITECTURE §2.5"""
    mode:        Archetype
    weights:     dict[str, float]
    constraints: list[str]
    ttl:         int  # turns
    phi:         float
    regime:      Regime
    turn_id:     int


@dataclass
class ConductorState:
    """Internal rolling state for hysteresis and velocity tracking."""
    phi_history:      list[float]   = field(default_factory=list)
    regime_history:   list[Regime]  = field(default_factory=list)
    archetype_history: list[Archetype] = field(default_factory=list)
    pending_regime:   Optional[Regime] = None
    pending_turns:    int = 0
    turn_count:       int = 0


# ---------------------------------------------------------------------------
# Core: φ computation
# ---------------------------------------------------------------------------

def compute_stability_index(sv: StateVector) -> float:
    """S(t) = w1·D_e + w2·N + w3·C + w4·R  (AHG_ARCHITECTURE §2.2)
    Only D_e enters S(t); D_explore and D_correct are excluded.
    """
    return W1_D_E * sv.D_e + W2_N * sv.N + W3_C * sv.C + W4_R * sv.R


def logistic(x: float) -> float:
    """Standard logistic σ(x) = 1 / (1 + e^(-x))"""
    return 1.0 / (1.0 + math.exp(-x))


def compute_phi(sv: StateVector) -> float:
    """φ(t) = 1 + 0.8 · σ(S(t))  →  φ ∈ [1.0, 1.8] by construction.
    Canonical normalization from AHG_ARCHITECTURE §2.2 v1.2.
    """
    s = compute_stability_index(sv)
    return PHI_MIN + (PHI_MAX - PHI_MIN) * logistic(s)


def classify_regime(phi: float) -> Regime:
    """Map φ scalar to Regime via threshold table (AHG_ARCHITECTURE §3)."""
    for threshold, regime in _REGIME_THRESHOLDS:
        if phi >= threshold:
            return regime
    return Regime.GROUNDED


def compute_phase_velocity(phi_history: list[float]) -> float:
    """v_φ(t) = φ_t − φ_{t−1}  (AHG_ARCHITECTURE §2.3)"""
    if len(phi_history) < 2:
        return 0.0
    return phi_history[-1] - phi_history[-2]


def compute_phase_acceleration(phi_history: list[float]) -> float:
    """a_φ(t) = v_φ(t) − v_φ(t−1)  (AHG_ARCHITECTURE §2.3)"""
    if len(phi_history) < 3:
        return 0.0
    v_t   = phi_history[-1] - phi_history[-2]
    v_t_1 = phi_history[-2] - phi_history[-3]
    return v_t - v_t_1


# ---------------------------------------------------------------------------
# AHGConductor
# ---------------------------------------------------------------------------

class AHGConductor:
    """
    AHG Conductor — continuous φ estimation and archetype dispatch.

    Usage:
        conductor = AHGConductor(herald_sink=my_herald)
        intent = conductor.step(state_vector)

    v1.3 scaffold:
        - φ computation: IMPLEMENTED
        - Regime dispatch + hysteresis: IMPLEMENTED
        - Phase velocity + acceleration: IMPLEMENTED
        - Phase Intent broadcast: STUBBED (herald_sink hook present)
        - Tribunal recovery protocol: STUBBED (calls _tribunal_stub)
        - MPHG optimizer (v2.0): NOT IMPLEMENTED
    """

    def __init__(
        self,
        herald_sink=None,           # P-01 Herald fan-out sink — wired in v1.4
        hysteresis_turns: int = HYSTERESIS_TURNS,
        phi_history_max: int = 10,
    ) -> None:
        self.herald_sink = herald_sink
        self.hysteresis_turns = hysteresis_turns
        self.phi_history_max = phi_history_max
        self._state = ConductorState()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def step(self, sv: StateVector) -> PhaseIntent:
        """
        Ingest one StateVector, compute φ, dispatch archetype, emit
        PhaseIntent.  Call once per governance turn.
        """
        self._state.turn_count += 1
        turn_id = self._state.turn_count

        phi = compute_phi(sv)
        self._state.phi_history.append(phi)
        if len(self._state.phi_history) > self.phi_history_max:
            self._state.phi_history.pop(0)

        v_phi = compute_phase_velocity(self._state.phi_history)
        a_phi = compute_phase_acceleration(self._state.phi_history)

        regime   = self._resolve_regime_with_hysteresis(phi)
        archetype = _REGIME_ARCHETYPE[regime]

        self._state.regime_history.append(regime)
        self._state.archetype_history.append(archetype)

        intent = PhaseIntent(
            mode=archetype,
            weights={"w1_D_e": W1_D_E, "w2_N": W2_N, "w3_C": W3_C, "w4_R": W4_R},
            constraints=self._active_constraints(regime),
            ttl=5 if regime == Regime.TENSION else 3,
            phi=phi,
            regime=regime,
            turn_id=turn_id,
        )

        logger.info(
            "AHGConductor turn=%d phi=%.4f v_phi=%.4f a_phi=%.4f "
            "regime=%s archetype=%s",
            turn_id, phi, v_phi, a_phi, regime.value, archetype.value,
        )

        if regime == Regime.TENSION:
            self._tribunal_stub(intent, phi, v_phi, a_phi, sv)

        self._emit_herald(intent, phi, v_phi, a_phi)

        return intent

    @property
    def phi(self) -> Optional[float]:
        """Most recent φ value, or None if no steps taken."""
        return self._state.phi_history[-1] if self._state.phi_history else None

    @property
    def regime(self) -> Optional[Regime]:
        return self._state.regime_history[-1] if self._state.regime_history else None

    @property
    def turn_count(self) -> int:
        return self._state.turn_count

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_regime_with_hysteresis(self, phi: float) -> Regime:
        """
        Hysteresis band: transition fires only if φ has crossed the band
        edge for >= HYSTERESIS_TURNS consecutive turns (AHG_ARCHITECTURE §2.4).
        """
        candidate = classify_regime(phi)
        current   = self._state.regime_history[-1] if self._state.regime_history else None

        if current is None or candidate == current:
            self._state.pending_regime = None
            self._state.pending_turns  = 0
            return candidate

        if candidate == self._state.pending_regime:
            self._state.pending_turns += 1
        else:
            self._state.pending_regime = candidate
            self._state.pending_turns  = 1

        if self._state.pending_turns >= self.hysteresis_turns:
            self._state.pending_regime = None
            self._state.pending_turns  = 0
            return candidate

        return current

    def _active_constraints(self, regime: Regime) -> list[str]:
        """Return active governance constraints for the current regime."""
        constraints = []
        if regime in (Regime.INTROSPECTION, Regime.TENSION):
            constraints.append("apogee_lens_mandatory")
        if regime == Regime.TENSION:
            constraints.append("p29_risk_block")
            constraints.append("p38_circuit_open")
        if regime == Regime.VIGILANCE:
            constraints.append("demijole_active")
        return constraints

    def _tribunal_stub(
        self,
        intent: PhaseIntent,
        phi: float,
        v_phi: float,
        a_phi: float,
        sv: StateVector,
    ) -> None:
        """
        STUB — Tribunal recovery protocol (AHG_ARCHITECTURE §5).

        v1.3: logs intent and 3D phase position for diagnosis.
        v1.4: wire to P-29 risk_block + P-38 OPEN + recovery R_c loop.

        3D phase position heuristic (AHG_ARCHITECTURE §2.7):
          Deadlock:            Low N, High D_e, High sv.R
          Hallucination spiral: High D_e, High N, low K
          False consensus:     Low D_e, Low sv.D_explore, High K
        """
        logger.warning(
            "AHGConductor TRIBUNAL activated: phi=%.4f v_phi=%.4f a_phi=%.4f. "
            "P-29 risk_block + P-38 OPEN stubs fired. "
            "D_e=%.3f N=%.3f K=%.3f — recovery protocol STUBBED v1.3.",
            phi, v_phi, a_phi, sv.D_e, sv.N, sv.K,
        )
        # TODO v1.4: self.herald_sink.emit({"event": "TRIBUNAL", ...})
        # TODO v1.4: fire P-29 risk_block
        # TODO v1.4: fire P-38 OPEN signal
        # TODO v1.4: begin R_c recovery loop

    def _emit_herald(
        self,
        intent: PhaseIntent,
        phi: float,
        v_phi: float,
        a_phi: float,
    ) -> None:
        """
        STUB — emit PhaseIntent event to P-01 Herald trace sink.
        v1.4: replace with live herald_sink.emit() call.
        """
        if self.herald_sink is not None:
            # v1.4 wiring point
            pass
        logger.debug(
            "AHGConductor herald stub: turn=%d phi=%.4f regime=%s archetype=%s",
            intent.turn_id, phi, intent.regime.value, intent.mode.value,
        )
