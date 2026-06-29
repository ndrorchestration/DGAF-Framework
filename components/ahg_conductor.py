"""
ahg_conductor.py — AHG Phi Stability Controller (PSC)
Pattern: P-42 — Adaptive Harmonic Governance, Layer 12 — Cognitive Control Plane
Version: 1.3 (scaffold)
Authors: Amethyst x COLLEEN | 2026-06-29

Responsibilities:
  - Receive HeartbeatVector entries from AHGSidecar
  - Compute Stability Index S(t) and canonical phi(t) via logistic normalization
  - Track phase velocity v_phi and acceleration a_phi for predictive switching
  - Dispatch Conductor Archetype with hysteresis (>= 2 consecutive turns to transition)
  - Broadcast PhaseIntent to the multi-agent collective
  - Manage Tribunal activation, Recovery Score, and graduated de-escalation

Formalism (AHG_ARCHITECTURE.md v1.2):
  S(t) = w1*D_e + w2*N + w3*C + w4*R
  phi(t) = 1 + 0.8 * sigma(S(t))       phi in [1.0, 1.8]
  v_phi(t) = phi(t) - phi(t-1)
  a_phi(t) = v_phi(t) - v_phi(t-1)
"""

from __future__ import annotations

import math
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger("ahg.conductor")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default S(t) weights
W1_D_E = 0.35   # destabilizing entropy
W2_N   = 0.20   # novelty
W3_C   = 0.25   # constraint pressure
W4_R   = 0.20   # revision pressure

# phi regime boundaries (7-state, v1.2)
PHI_GROUNDED_MAX    = 1.15
PHI_FLOW_MAX        = 1.30
PHI_VIGILANCE_MAX   = 1.45
PHI_EXPANSION_MAX   = 1.60
PHI_INTEGRATION_MAX = 1.70   # NDR-STASIS anchor phi=1.618 sits here
PHI_INTROSPECTION_MAX = 1.80 # Tribunal threshold
PHI_TENSION_FLOOR   = 1.80

# NDR-STASIS canonical anchor
NDR_STASIS_PHI = (1 + math.sqrt(5)) / 2  # 1.6180339...

# Hysteresis: turns phi must persist in new band before archetype transition fires
HYSTERESIS_TURNS = 2

# Anticipatory governance: if a_phi >= this threshold AND phi rising toward Tension, pre-empt
ACCEL_PREEMPT_THRESHOLD = 0.08

# Tribunal exit: phi must drop below this for >= 2 turns
TRIBUNAL_EXIT_PHI = 1.70
TRIBUNAL_EXIT_TURNS = 2


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Archetype(str, Enum):
    EXECUTOR      = "Executor"       # phi 1.00-1.15  | Grounded
    SYNTHESIZER   = "Synthesizer"    # phi 1.15-1.30  | Flow
    SENTINEL      = "Sentinel"       # phi 1.30-1.45  | Vigilance
    EXPLORER      = "Explorer"       # phi 1.45-1.60  | Expansion
    INTEGRATOR    = "Integrator"     # phi 1.60-1.70  | Integration (NDR-STASIS band)
    AUDITOR       = "Auditor"        # phi 1.70-1.80  | Introspection
    TRIBUNAL      = "Tribunal"       # phi > 1.80     | Tension


class Regime(str, Enum):
    GROUNDED      = "Grounded"
    FLOW          = "Flow"
    VIGILANCE     = "Vigilance"
    EXPANSION     = "Expansion"
    INTEGRATION   = "Integration"    # NDR-STASIS phi=1.618 anchor
    INTROSPECTION = "Introspection"
    TENSION       = "Tension"


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class HeartbeatVector:
    """Compressed cognitive signal emitted by each agent to the Sidecar.
    Only D_e (destabilizing entropy) enters S(t).
    D_explore and D_correct are tracked separately and excluded from phi.
    """
    agent_id:         str
    turn_id:          int
    d_e:              float  # destabilizing entropy signal [0.0, 1.0]
    d_explore:        float  # exploratory divergence [0.0, 1.0] -- excluded from S(t)
    d_correct:        float  # corrective dissent [0.0, 1.0] -- excluded from S(t)
    novelty:          float  # [0.0, 1.0]
    constraint_count: int    # active blocking constraints
    total_constraints: int   # total constraints defined (for C fraction)
    revision_count:   int    # self/other corrections this turn
    total_turns:      int    # total turns so far (for R rate)


@dataclass
class AggregatedSignals:
    """Turn-level signals aggregated across all agents."""
    turn_id:   int
    D_e:       float  # mean destabilizing entropy
    D_explore: float  # mean exploratory divergence (tracked, not in S)
    D_correct: float  # mean corrective dissent (Apogee fuel, not in S)
    N:         float  # mean novelty
    C:         float  # constraint pressure fraction
    R:         float  # revision rate


@dataclass
class PhaseIntent:
    """Broadcast packet from Conductor to all agents."""
    turn_id:     int
    archetype:   Archetype
    regime:      Regime
    phi:         float
    v_phi:       float
    a_phi:       float
    weights:     dict
    constraints_active: int
    ttl:         int          # turns this intent is valid
    tribunal_active: bool
    message:     str


@dataclass
class ConductorState:
    """Mutable conductor state persisted across turns."""
    phi_history:       list[float] = field(default_factory=list)
    v_phi_history:     list[float] = field(default_factory=list)
    archetype_history: list[Archetype] = field(default_factory=list)
    regime_history:    list[Regime] = field(default_factory=list)
    pending_archetype: Optional[Archetype] = None
    pending_turns:     int = 0
    tribunal_active:   bool = False
    tribunal_turns:    int = 0
    tribunal_exit_turns_met: int = 0
    momentum:          float = 0.0   # governance momentum M (EMA of archetype stability)
    turn_count:        int = 0


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def _sigma(x: float) -> float:
    """Standard logistic function."""
    return 1.0 / (1.0 + math.exp(-x))


def compute_stability_index(
    D_e: float,
    N: float,
    C: float,
    R: float,
    w1: float = W1_D_E,
    w2: float = W2_N,
    w3: float = W3_C,
    w4: float = W4_R,
) -> float:
    """Compute S(t) = w1*D_e + w2*N + w3*C + w4*R.
    Note: only D_e enters S(t). D_explore and D_correct are excluded.
    """
    return w1 * D_e + w2 * N + w3 * C + w4 * R


def compute_phi(S: float) -> float:
    """Canonical phi: phi(t) = 1 + 0.8 * sigma(S(t)). Range [1.0, 1.8]."""
    return 1.0 + 0.8 * _sigma(S)


def classify_regime(phi: float) -> Regime:
    """Map phi to the 7-state harmonic regime."""
    if phi < PHI_GROUNDED_MAX:
        return Regime.GROUNDED
    elif phi < PHI_FLOW_MAX:
        return Regime.FLOW
    elif phi < PHI_VIGILANCE_MAX:
        return Regime.VIGILANCE
    elif phi < PHI_EXPANSION_MAX:
        return Regime.EXPANSION
    elif phi < PHI_INTEGRATION_MAX:
        return Regime.INTEGRATION   # NDR-STASIS phi=1.618 sits here
    elif phi < PHI_INTROSPECTION_MAX:
        return Regime.INTROSPECTION
    else:
        return Regime.TENSION


def regime_to_archetype(regime: Regime) -> Archetype:
    """Map regime to default Conductor Archetype."""
    return {
        Regime.GROUNDED:      Archetype.EXECUTOR,
        Regime.FLOW:          Archetype.SYNTHESIZER,
        Regime.VIGILANCE:     Archetype.SENTINEL,
        Regime.EXPANSION:     Archetype.EXPLORER,
        Regime.INTEGRATION:   Archetype.INTEGRATOR,
        Regime.INTROSPECTION: Archetype.AUDITOR,
        Regime.TENSION:       Archetype.TRIBUNAL,
    }[regime]


def aggregate_heartbeats(heartbeats: list[HeartbeatVector], turn_id: int) -> AggregatedSignals:
    """Aggregate per-agent heartbeats into turn-level signals."""
    if not heartbeats:
        raise ValueError(f"No heartbeats for turn {turn_id}")

    n = len(heartbeats)
    D_e       = sum(h.d_e for h in heartbeats) / n
    D_explore = sum(h.d_explore for h in heartbeats) / n
    D_correct = sum(h.d_correct for h in heartbeats) / n
    N         = sum(h.novelty for h in heartbeats) / n

    # C: fraction of active constraints across all agents
    total_c = sum(h.total_constraints for h in heartbeats)
    active_c = sum(h.constraint_count for h in heartbeats)
    C = (active_c / total_c) if total_c > 0 else 0.0

    # R: revision rate
    total_t = sum(h.total_turns for h in heartbeats)
    total_r = sum(h.revision_count for h in heartbeats)
    R = (total_r / total_t) if total_t > 0 else 0.0

    return AggregatedSignals(
        turn_id=turn_id,
        D_e=D_e, D_explore=D_explore, D_correct=D_correct,
        N=N, C=C, R=R
    )


def compute_recovery_score(
    delta_D_e: float,
    delta_K: float,
    delta_v_phi: float,
    r1: float = 0.40,
    r2: float = 0.35,
    r3: float = 0.25,
) -> float:
    """R_c = r1*delta_D_e + r2*delta_K + r3*delta_v_phi.
    Positive values indicate recovery (D_e falling, K rising, v_phi decelerating).
    """
    return r1 * delta_D_e + r2 * delta_K + r3 * delta_v_phi


# ---------------------------------------------------------------------------
# Conductor class
# ---------------------------------------------------------------------------

class AHGConductor:
    """Phi Stability Controller (PSC).

    Usage:
        conductor = AHGConductor()
        intent = conductor.observe(heartbeats, turn_id)
        # broadcast intent to all agents
    """

    def __init__(
        self,
        w1: float = W1_D_E,
        w2: float = W2_N,
        w3: float = W3_C,
        w4: float = W4_R,
        hysteresis_turns: int = HYSTERESIS_TURNS,
        accel_preempt_threshold: float = ACCEL_PREEMPT_THRESHOLD,
        intent_ttl: int = 3,
    ):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.hysteresis_turns = hysteresis_turns
        self.accel_preempt_threshold = accel_preempt_threshold
        self.intent_ttl = intent_ttl
        self._state = ConductorState()
        logger.info("AHGConductor initialised (P-42 v1.3)")

    # ------------------------------------------------------------------
    # Primary interface
    # ------------------------------------------------------------------

    def observe(
        self,
        heartbeats: list[HeartbeatVector],
        turn_id: int,
        coherence_delta: float = 0.0,   # delta K for recovery score
    ) -> PhaseIntent:
        """Process one turn of heartbeats and return a PhaseIntent.

        Args:
            heartbeats: list of HeartbeatVector from all agents this turn.
            turn_id: monotonic turn counter.
            coherence_delta: change in collective coherence K (positive = improving).

        Returns:
            PhaseIntent to be broadcast to all agents.
        """
        s = self._state
        s.turn_count += 1

        # 1. Aggregate
        signals = aggregate_heartbeats(heartbeats, turn_id)

        # 2. Stability Index
        S = compute_stability_index(signals.D_e, signals.N, signals.C, signals.R,
                                     self.w1, self.w2, self.w3, self.w4)

        # 3. phi
        phi = compute_phi(S)
        s.phi_history.append(phi)

        # 4. Phase velocity and acceleration
        v_phi = phi - s.phi_history[-2] if len(s.phi_history) >= 2 else 0.0
        s.v_phi_history.append(v_phi)
        a_phi = s.v_phi_history[-1] - s.v_phi_history[-2] if len(s.v_phi_history) >= 2 else 0.0

        # 5. Update governance momentum (decaying EMA)
        s.momentum = 0.85 * s.momentum + 0.15 * phi

        # 6. Classify regime
        regime = classify_regime(phi)
        target_archetype = regime_to_archetype(regime)

        # 7. Anticipatory governance: pre-empt Tension if accelerating hard
        if (
            not s.tribunal_active
            and a_phi >= self.accel_preempt_threshold
            and phi > PHI_EXPANSION_MAX
        ):
            logger.warning(
                f"[AHG] Anticipatory Tribunal pre-empt: phi={phi:.4f} a_phi={a_phi:.4f}"
            )
            target_archetype = Archetype.TRIBUNAL
            regime = Regime.TENSION

        # 8. Hysteresis: require HYSTERESIS_TURNS consecutive turns in new band
        current_archetype = s.archetype_history[-1] if s.archetype_history else None
        if target_archetype != current_archetype:
            if s.pending_archetype == target_archetype:
                s.pending_turns += 1
            else:
                s.pending_archetype = target_archetype
                s.pending_turns = 1

            if s.pending_turns >= self.hysteresis_turns:
                dispatched_archetype = target_archetype
                s.pending_archetype = None
                s.pending_turns = 0
                logger.info(f"[AHG] Archetype transition: {current_archetype} -> {dispatched_archetype} (phi={phi:.4f})")
            else:
                # Hold current archetype
                dispatched_archetype = current_archetype or target_archetype
        else:
            dispatched_archetype = target_archetype
            s.pending_archetype = None
            s.pending_turns = 0

        # 9. Tribunal activation / management
        if dispatched_archetype == Archetype.TRIBUNAL:
            if not s.tribunal_active:
                s.tribunal_active = True
                s.tribunal_turns = 0
                s.tribunal_exit_turns_met = 0
                logger.warning(f"[AHG] TRIBUNAL ACTIVATED at turn {turn_id} (phi={phi:.4f})")
            s.tribunal_turns += 1
        elif s.tribunal_active:
            # Check exit condition: phi < TRIBUNAL_EXIT_PHI for TRIBUNAL_EXIT_TURNS
            if phi < TRIBUNAL_EXIT_PHI:
                s.tribunal_exit_turns_met += 1
            else:
                s.tribunal_exit_turns_met = 0

            if s.tribunal_exit_turns_met >= TRIBUNAL_EXIT_TURNS:
                s.tribunal_active = False
                s.tribunal_turns = 0
                logger.info(f"[AHG] Tribunal exit: phi={phi:.4f} -> graduated de-escalation")

        # 10. Record
        s.archetype_history.append(dispatched_archetype)
        s.regime_history.append(regime)

        # 11. Build PhaseIntent
        intent = PhaseIntent(
            turn_id=turn_id,
            archetype=dispatched_archetype,
            regime=regime,
            phi=phi,
            v_phi=v_phi,
            a_phi=a_phi,
            weights={"w1_D_e": self.w1, "w2_N": self.w2, "w3_C": self.w3, "w4_R": self.w4},
            constraints_active=signals.C,
            ttl=self.intent_ttl,
            tribunal_active=s.tribunal_active,
            message=self._compose_message(dispatched_archetype, phi, v_phi, a_phi, signals),
        )

        logger.debug(
            f"[AHG T{turn_id}] S={S:.4f} phi={phi:.4f} v={v_phi:.4f} a={a_phi:.4f} "
            f"regime={regime.value} archetype={dispatched_archetype.value} "
            f"D_e={signals.D_e:.3f} D_exp={signals.D_explore:.3f} D_cor={signals.D_correct:.3f}"
        )

        return intent

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    @property
    def phi(self) -> Optional[float]:
        return self._state.phi_history[-1] if self._state.phi_history else None

    @property
    def regime(self) -> Optional[Regime]:
        return self._state.regime_history[-1] if self._state.regime_history else None

    @property
    def archetype(self) -> Optional[Archetype]:
        return self._state.archetype_history[-1] if self._state.archetype_history else None

    @property
    def tribunal_active(self) -> bool:
        return self._state.tribunal_active

    def phi_history(self, n: int = 10) -> list[float]:
        return self._state.phi_history[-n:]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _compose_message(self, archetype: Archetype, phi: float, v_phi: float, a_phi: float, signals: AggregatedSignals) -> str:
        regime = classify_regime(phi)
        ndr_note = " [NDR-STASIS anchor]" if abs(phi - NDR_STASIS_PHI) < 0.02 else ""
        tribunal_note = " [TRIBUNAL ACTIVE]".format() if self._state.tribunal_active else ""
        return (
            f"{archetype.value} | {regime.value}{ndr_note}{tribunal_note} | "
            f"phi={phi:.4f} v={v_phi:+.4f} a={a_phi:+.4f} | "
            f"D_e={signals.D_e:.3f} D_exp={signals.D_explore:.3f} D_cor={signals.D_correct:.3f} | "
            f"N={signals.N:.3f} C={signals.C:.3f} R={signals.R:.3f}"
        )
