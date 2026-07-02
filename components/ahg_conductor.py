"""
ahg_conductor.py — Adaptive Harmonic Governance Conductor
P-42 · Layer 12 — Cognitive Control Plane · v1.4
Amethyst × COLLEEN · S072 · 2026-07-02

Spec: docs/theory/AHG_ARCHITECTURE.md v1.2
Pattern card: patterns/P-42_AHG.md v1.3-card

v1.3: scaffold — φ computation, regime dispatch, hysteresis, stubs
v1.4: PhaseIntent enriched (v_phi, a_phi, tribunal_active, message,
      3D phase space axes); _emit_herald passes full PhaseIntent;
      interfaces now aligned with ahg_herald_trace.py v1.5
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

W1_D_E: float = 0.35
W2_N:   float = 0.20
W3_C:   float = 0.25
W4_R:   float = 0.20

PHI_MIN: float = 1.0
PHI_MAX: float = 1.8

HYSTERESIS_TURNS: int = 2

_3D_EPS: float = 1e-9  # prevent division by zero in 3D axis normalization


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
    EXECUTOR    = "Executor"
    SYNTHESIZER = "Synthesizer"
    SENTINEL    = "Sentinel"
    EXPLORER    = "Explorer"
    AUDITOR     = "Auditor"
    TRIBUNAL    = "Tribunal"


_REGIME_ARCHETYPE: dict[Regime, Archetype] = {
    Regime.GROUNDED:      Archetype.EXECUTOR,
    Regime.FLOW:          Archetype.SYNTHESIZER,
    Regime.VIGILANCE:     Archetype.SENTINEL,
    Regime.EXPANSION:     Archetype.EXPLORER,
    Regime.INTEGRATION:   Archetype.SYNTHESIZER,
    Regime.INTROSPECTION: Archetype.AUDITOR,
    Regime.TENSION:       Archetype.TRIBUNAL,
}

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
    D_e:       float = 0.0
    D_explore: float = 0.0
    D_correct: float = 0.0
    N:         float = 0.0
    C:         float = 0.0
    R:         float = 0.0
    M:         float = 0.0
    K:         float = 0.0

    @property
    def D_p(self) -> float:
        return self.D_explore + self.D_correct


@dataclass
class PhaseIntent:
    """
    I_t broadcast packet — AHG_ARCHITECTURE §2.5

    v1.4 additions (aligned with ahg_herald_trace.py v1.5 AHGTraceRecord):
      v_phi, a_phi         — phase velocity and acceleration
      tribunal_active      — True when regime == TENSION
      message              — human-readable governance summary
      phase_exploration    — Axis 1: Exploration [0,1] (AHG_ARCHITECTURE §2.7)
      phase_dissent        — Axis 2: Dissent [0,1]
      phase_uncertainty    — Axis 3: Uncertainty [0,1]
    """
    mode:              Archetype
    weights:           dict[str, float]
    constraints:       list[str]
    ttl:               int
    phi:               float
    regime:            Regime
    turn_id:           int
    # v1.4 enrichment
    v_phi:             float = 0.0
    a_phi:             float = 0.0
    tribunal_active:   bool  = False
    message:           str   = ""
    phase_exploration: Optional[float] = None  # Axis 1: Exploration ↔ Exploitation
    phase_dissent:     Optional[float] = None  # Axis 2: Consensus ↔ Dissent
    phase_uncertainty: Optional[float] = None  # Axis 3: Confidence ↔ Uncertainty


@dataclass
class ConductorState:
    phi_history:       list[float]    = field(default_factory=list)
    regime_history:    list[Regime]   = field(default_factory=list)
    archetype_history: list[Archetype] = field(default_factory=list)
    pending_regime:    Optional[Regime] = None
    pending_turns:     int = 0
    turn_count:        int = 0


# ---------------------------------------------------------------------------
# φ computation
# ---------------------------------------------------------------------------

def compute_stability_index(sv: StateVector) -> float:
    """S(t) = w1·D_e + w2·N + w3·C + w4·R — only D_e enters, not D_explore/D_correct."""
    return W1_D_E * sv.D_e + W2_N * sv.N + W3_C * sv.C + W4_R * sv.R


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def compute_phi(sv: StateVector) -> float:
    """φ(t) = 1 + 0.8·σ(S(t)) → φ ∈ [1.0, 1.8] by construction."""
    return PHI_MIN + (PHI_MAX - PHI_MIN) * logistic(compute_stability_index(sv))


def classify_regime(phi: float) -> Regime:
    for threshold, regime in _REGIME_THRESHOLDS:
        if phi >= threshold:
            return regime
    return Regime.GROUNDED


def compute_phase_velocity(phi_history: list[float]) -> float:
    """v_φ(t) = φ_t − φ_{t−1}"""
    if len(phi_history) < 2:
        return 0.0
    return phi_history[-1] - phi_history[-2]


def compute_phase_acceleration(phi_history: list[float]) -> float:
    """a_φ(t) = v_φ(t) − v_φ(t−1)"""
    if len(phi_history) < 3:
        return 0.0
    v_t   = phi_history[-1] - phi_history[-2]
    v_t_1 = phi_history[-2] - phi_history[-3]
    return v_t - v_t_1


# ---------------------------------------------------------------------------
# 3D Cognitive Phase Space — AHG_ARCHITECTURE §2.7
# ---------------------------------------------------------------------------

def compute_3d_phase(sv: StateVector) -> tuple[float, float, float]:
    """
    Compute 3D Cognitive Phase Space axes from StateVector.
    All axes normalized to [0.0, 1.0].

    Axis 1 — Exploration ↔ Exploitation:
        High D_explore = Exploration; high K (coherence) = Exploitation.
        phase_exploration = D_explore / (D_explore + K + ε)

    Axis 2 — Consensus ↔ Dissent:
        High D_e + D_correct = Dissent; high K = Consensus.
        phase_dissent = (D_e + D_correct) / (D_e + D_correct + K + ε)

    Axis 3 — Confidence ↔ Uncertainty:
        High C (constraint pressure) + R (revision) = Uncertainty.
        phase_uncertainty = (C + R) / 2
        Clipped to [0.0, 1.0].

    Returns: (phase_exploration, phase_dissent, phase_uncertainty)
    """
    exploration = sv.D_explore / (sv.D_explore + sv.K + _3D_EPS)
    dissent_num = sv.D_e + sv.D_correct
    dissent     = dissent_num / (dissent_num + sv.K + _3D_EPS)
    uncertainty = min((sv.C + sv.R) / 2.0, 1.0)
    return round(exploration, 6), round(dissent, 6), round(uncertainty, 6)


# ---------------------------------------------------------------------------
# AHGConductor
# ---------------------------------------------------------------------------

class AHGConductor:
    """
    AHG Conductor — continuous φ estimation and archetype dispatch.

    v1.3: scaffold — φ computation, regime dispatch, hysteresis
    v1.4: PhaseIntent enriched with v_phi, a_phi, tribunal_active,
          message, 3D Cognitive Phase Space axes; _emit_herald passes
          full PhaseIntent; aligned with ahg_herald_trace.py v1.5
    """

    def __init__(
        self,
        herald_sink=None,
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
        """Ingest one StateVector, compute φ, dispatch archetype, emit PhaseIntent."""
        self._state.turn_count += 1
        turn_id = self._state.turn_count

        phi = compute_phi(sv)
        self._state.phi_history.append(phi)
        if len(self._state.phi_history) > self.phi_history_max:
            self._state.phi_history.pop(0)

        v_phi = compute_phase_velocity(self._state.phi_history)
        a_phi = compute_phase_acceleration(self._state.phi_history)

        regime    = self._resolve_regime_with_hysteresis(phi)
        archetype = _REGIME_ARCHETYPE[regime]
        tribunal_active = (regime == Regime.TENSION)

        self._state.regime_history.append(regime)
        self._state.archetype_history.append(archetype)

        # 3D Cognitive Phase Space (AHG_ARCHITECTURE §2.7)
        p_explore, p_dissent, p_uncertainty = compute_3d_phase(sv)

        constraints = self._active_constraints(regime)

        message = (
            f"φ={phi:.4f} regime={regime.value} archetype={archetype.value} "
            f"v_φ={v_phi:+.4f} a_φ={a_phi:+.4f}"
            + (" ⚠️ TRIBUNAL" if tribunal_active else "")
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
        )

        logger.info(
            "AHGConductor T=%d φ=%.4f v_φ=%+.4f a_φ=%+.4f "
            "regime=%s archetype=%s tribunal=%s "
            "3D=[exp=%.3f dis=%.3f unc=%.3f]",
            turn_id, phi, v_phi, a_phi,
            regime.value, archetype.value, tribunal_active,
            p_explore, p_dissent, p_uncertainty,
        )

        if tribunal_active:
            self._tribunal_stub(intent, sv)

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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_regime_with_hysteresis(self, phi: float) -> Regime:
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
        constraints = []
        if regime in (Regime.INTROSPECTION, Regime.TENSION):
            constraints.append("apogee_lens_mandatory")
        if regime == Regime.TENSION:
            constraints.append("p29_risk_block")
            constraints.append("p38_circuit_open")
        if regime == Regime.VIGILANCE:
            constraints.append("demijole_active")
        return constraints

    def _tribunal_stub(self, intent: PhaseIntent, sv: StateVector) -> None:
        """
        STUB — Tribunal recovery protocol (AHG_ARCHITECTURE §5).
        v1.4: 3D phase position logged for diagnosis.
        v1.5+: wire to P-29 risk_block + P-38 OPEN + R_c recovery loop.
        """
        logger.warning(
            "AHGConductor TRIBUNAL T=%d φ=%.4f v_φ=%+.4f a_φ=%+.4f "
            "3D=[exp=%.3f dis=%.3f unc=%.3f] "
            "P-29 risk_block + P-38 OPEN stubs fired.",
            intent.turn_id, intent.phi, intent.v_phi, intent.a_phi,
            intent.phase_exploration, intent.phase_dissent, intent.phase_uncertainty,
        )
        # TODO v1.5: fire P-29 risk_block
        # TODO v1.5: fire P-38 OPEN signal
        # TODO v1.5: begin R_c recovery loop with 3D-informed recovery path

    def _emit_herald(self, intent: PhaseIntent) -> None:
        """Emit full enriched PhaseIntent to herald_sink (v1.4 — aligned with
        ahg_herald_trace.py v1.5 AHGHeraldTrace.on_intent interface)."""
        if self.herald_sink is not None:
            try:
                self.herald_sink(intent)
            except Exception as exc:
                logger.error("AHGConductor herald emit failed: %s", exc)
        logger.debug(
            "AHGConductor herald: T=%d φ=%.4f regime=%s archetype=%s "
            "tribunal=%s 3D=[%.3f %.3f %.3f]",
            intent.turn_id, intent.phi, intent.regime.value, intent.mode.value,
            intent.tribunal_active,
            intent.phase_exploration or 0.0,
            intent.phase_dissent or 0.0,
            intent.phase_uncertainty or 0.0,
        )
