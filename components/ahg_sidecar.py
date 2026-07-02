"""
ahg_sidecar.py — AHG Sidecar Monitor
P-42 · Layer 12 — Cognitive Control Plane · v1.3 scaffold
Amethyst × COLLEEN · S072 · 2026-07-02

Spec: docs/theory/AHG_ARCHITECTURE.md v1.2 §4
Pattern card: patterns/P-42_AHG.md v1.3-card

The Sidecar Monitor is O(n) scalable — it reads only compressed Heartbeat
signals from each agent, never full context. Aggregates per-agent signals
each turn, flushes to AHGConductor for φ computation.

Architecture:
  [Agent_1 Heartbeat] ──┐
  [Agent_2 Heartbeat] ──┤──► AHGSidecar ──► AHGConductor ──► PhaseIntent
  [Agent_N Heartbeat] ──┘          │
                                    └──► P-01 Herald Trace (stub, v1.4)

Status: SCAFFOLD
  - Heartbeat ingestion: IMPLEMENTED
  - Turn-level aggregation → StateVector: IMPLEMENTED
  - AHGConductor flush: IMPLEMENTED
  - P-01 Herald trace routing: STUBBED (v1.4)
  - Async transport: STUBBED (v1.4)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from .ahg_conductor import AHGConductor, PhaseIntent, StateVector

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Heartbeat payload — mirrors schemas/ahg_heartbeat.json
# ---------------------------------------------------------------------------

@dataclass
class AgentHeartbeat:
    """
    Compressed per-agent signal payload emitted each governance turn.
    Schema: schemas/ahg_heartbeat.json
    """
    agent_id:          str
    turn_id:           int
    D_e_signal:        float = 0.0  # Destabilizing Entropy contribution
    D_explore_signal:  float = 0.0  # Exploratory Divergence contribution
    D_correct_signal:  float = 0.0  # Corrective Dissent contribution
    novelty_signal:    float = 0.0  # Novelty contribution
    constraint_count:  int   = 0    # Active blocking constraints
    revision_count:    int   = 0    # Self-corrections this turn
    coherence_signal:  float = 0.0  # Semantic similarity to other agents


# ---------------------------------------------------------------------------
# Turn buffer
# ---------------------------------------------------------------------------

@dataclass
class TurnBuffer:
    """Collects all heartbeats for a single turn before flush."""
    turn_id:    int
    heartbeats: list[AgentHeartbeat] = field(default_factory=list)

    def add(self, hb: AgentHeartbeat) -> None:
        if hb.turn_id != self.turn_id:
            raise ValueError(
                f"Heartbeat turn_id {hb.turn_id} does not match "
                f"buffer turn_id {self.turn_id}"
            )
        self.heartbeats.append(hb)

    def to_state_vector(self, total_possible_constraints: int = 10) -> StateVector:
        """
        Aggregate per-agent heartbeats into a single StateVector.

        Aggregation rules:
          D_e:  mean of D_e_signal across agents   (shared entropy level)
          N:    mean of novelty_signal              (collective novelty)
          C:    total constraint_count / total_possible_constraints
          R:    mean(revision_count) normalised to [0,1] via /10 clip
          M:    0.0 (updated by Conductor EMA — not agent-reported)
          K:    mean of coherence_signal
          D_explore / D_correct: mean of respective signals
        """
        if not self.heartbeats:
            return StateVector()

        n = len(self.heartbeats)

        D_e       = sum(h.D_e_signal for h in self.heartbeats) / n
        D_explore = sum(h.D_explore_signal for h in self.heartbeats) / n
        D_correct = sum(h.D_correct_signal for h in self.heartbeats) / n
        N         = sum(h.novelty_signal for h in self.heartbeats) / n
        C         = sum(h.constraint_count for h in self.heartbeats) / max(
                        total_possible_constraints, 1
                    )
        R         = min(
                        sum(h.revision_count for h in self.heartbeats) / n / 10.0,
                        1.0
                    )
        K         = sum(h.coherence_signal for h in self.heartbeats) / n

        return StateVector(
            D_e=D_e, D_explore=D_explore, D_correct=D_correct,
            N=N, C=C, R=R, M=0.0, K=K,
        )


# ---------------------------------------------------------------------------
# AHGSidecar
# ---------------------------------------------------------------------------

class AHGSidecar:
    """
    AHG Sidecar Monitor — O(n) heartbeat aggregation and turn-level flush.

    Usage:
        conductor = AHGConductor()
        sidecar   = AHGSidecar(conductor=conductor)

        # Each agent emits once per turn:
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1, ...))
        sidecar.ingest(AgentHeartbeat(agent_id="COLLEEN",  turn_id=1, ...))

        # At turn end, flush to conductor:
        intent = sidecar.flush(turn_id=1)

    v1.3 scaffold:
        - Heartbeat ingestion + turn buffer: IMPLEMENTED
        - StateVector aggregation: IMPLEMENTED
        - AHGConductor flush: IMPLEMENTED
        - P-01 Herald routing: STUBBED
        - Async transport: STUBBED
    """

    def __init__(
        self,
        conductor: AHGConductor,
        herald_sink=None,
        total_possible_constraints: int = 10,
    ) -> None:
        self.conductor = conductor
        self.herald_sink = herald_sink
        self.total_possible_constraints = total_possible_constraints
        self._buffers: dict[int, TurnBuffer] = {}
        self._agent_registry: set[str] = set()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, heartbeat: AgentHeartbeat) -> None:
        """
        Accept a single AgentHeartbeat. Thread-safe ingestion is deferred
        to v1.4 (asyncio / threading.Lock wrapper).
        """
        turn_id = heartbeat.turn_id
        self._agent_registry.add(heartbeat.agent_id)

        if turn_id not in self._buffers:
            self._buffers[turn_id] = TurnBuffer(turn_id=turn_id)

        self._buffers[turn_id].add(heartbeat)
        logger.debug(
            "AHGSidecar ingested heartbeat agent=%s turn=%d D_e=%.3f",
            heartbeat.agent_id, turn_id, heartbeat.D_e_signal,
        )

    def flush(self, turn_id: int) -> Optional[PhaseIntent]:
        """
        Aggregate all heartbeats for turn_id into a StateVector,
        flush to AHGConductor, emit herald trace (stub), return PhaseIntent.
        Cleans up the turn buffer after flush.
        """
        buffer = self._buffers.pop(turn_id, None)
        if buffer is None:
            logger.warning(
                "AHGSidecar flush called for turn=%d but no buffer found.",
                turn_id,
            )
            return None

        sv     = buffer.to_state_vector(self.total_possible_constraints)
        intent = self.conductor.step(sv)

        self._emit_herald_trace(turn_id, sv, intent)

        return intent

    def flush_all_pending(self) -> dict[int, Optional[PhaseIntent]]:
        """
        Flush all buffered turns in ascending turn_id order.
        Used for end-of-session cleanup or replay.
        """
        results = {}
        for turn_id in sorted(self._buffers.keys()):
            results[turn_id] = self.flush(turn_id)
        return results

    @property
    def registered_agents(self) -> set[str]:
        return set(self._agent_registry)

    @property
    def pending_turns(self) -> list[int]:
        return sorted(self._buffers.keys())

    # ------------------------------------------------------------------
    # Herald trace stub
    # ------------------------------------------------------------------

    def _emit_herald_trace(
        self,
        turn_id: int,
        sv: StateVector,
        intent: PhaseIntent,
    ) -> None:
        """
        STUB — emit aggregated turn event to P-01 Herald fan-out sink.
        v1.4: replace stub with live herald_sink.emit() call.

        Payload schema (for v1.4 wiring):
        {
          "event": "ahg_turn",
          "turn_id": int,
          "phi": float,
          "regime": str,
          "archetype": str,
          "D_e": float,
          "D_p": float,
          "N": float,
          "K": float,
          "agent_count": int,
          "pattern_id": "P-42"
        }
        """
        if self.herald_sink is not None:
            # v1.4 wiring point
            pass
        logger.debug(
            "AHGSidecar herald stub: turn=%d phi=%.4f regime=%s archetype=%s "
            "agents=%d D_e=%.3f D_p=%.3f N=%.3f K=%.3f",
            turn_id, intent.phi, intent.regime.value, intent.mode.value,
            len(self._agent_registry),
            sv.D_e, sv.D_p, sv.N, sv.K,
        )
