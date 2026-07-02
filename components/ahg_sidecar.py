"""
ahg_sidecar.py — AHG Sidecar Monitor
P-42 · Layer 12 — Cognitive Control Plane · v1.4
Amethyst × COLLEEN · S072 · 2026-07-02

Spec: docs/theory/AHG_ARCHITECTURE.md v1.2 §4
Pattern card: patterns/P-42_AHG.md v1.3-card

v1.3: scaffold — heartbeat ingestion, aggregation, conductor flush, herald stub
v1.4: wire_herald_trace(callback) added — replaces herald_sink stub pattern;
      flush() calls registered herald callback with enriched PhaseIntent;
      aligned with ahg_herald_trace.py v1.5 AHGHeraldTrace.on_intent() interface

Architecture:
  [Agent_1 Heartbeat] ──┐
  [Agent_2 Heartbeat] ──┤──► AHGSidecar ──► AHGConductor ──► PhaseIntent
  [Agent_N Heartbeat] ──┘         │
                                   └──► AHGHeraldTrace.on_intent() (v1.4)
                                         ├── in-memory buffer
                                         ├── JSONL file sink
                                         └── P-01 HTTP push (if configured)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

from .ahg_conductor import AHGConductor, PhaseIntent, StateVector

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Heartbeat payload — mirrors schemas/ahg_heartbeat.json
# ---------------------------------------------------------------------------

@dataclass
class AgentHeartbeat:
    agent_id:          str
    turn_id:           int
    D_e_signal:        float = 0.0
    D_explore_signal:  float = 0.0
    D_correct_signal:  float = 0.0
    novelty_signal:    float = 0.0
    constraint_count:  int   = 0
    revision_count:    int   = 0
    coherence_signal:  float = 0.0


# ---------------------------------------------------------------------------
# Turn buffer
# ---------------------------------------------------------------------------

@dataclass
class TurnBuffer:
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
        D_explore and D_correct tracked separately (excluded from S(t) in conductor).
        """
        if not self.heartbeats:
            return StateVector()

        n = len(self.heartbeats)

        D_e       = sum(h.D_e_signal       for h in self.heartbeats) / n
        D_explore = sum(h.D_explore_signal for h in self.heartbeats) / n
        D_correct = sum(h.D_correct_signal for h in self.heartbeats) / n
        N         = sum(h.novelty_signal   for h in self.heartbeats) / n
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

    Usage (v1.4 — with Herald trace):
        from components.ahg_herald_trace import AHGHeraldTrace

        conductor = AHGConductor()
        trace     = AHGHeraldTrace(session_id="S072", output_dir=Path("logs/ahg"))
        sidecar   = AHGSidecar(conductor=conductor)
        sidecar.wire_herald_trace(trace.on_intent)  # ← v1.4 wiring

        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1, ...))
        sidecar.ingest(AgentHeartbeat(agent_id="COLLEEN",  turn_id=1, ...))
        intent = sidecar.flush(turn_id=1)
        # PhaseIntent now routes: conductor → on_intent → memory/JSONL/HTTP
    """

    def __init__(
        self,
        conductor: AHGConductor,
        herald_sink=None,           # retained for backward compat (v1.3)
        total_possible_constraints: int = 10,
    ) -> None:
        self.conductor = conductor
        self._legacy_herald_sink = herald_sink  # v1.3 compat
        self.total_possible_constraints = total_possible_constraints
        self._buffers: dict[int, TurnBuffer] = {}
        self._agent_registry: set[str] = set()
        self._herald_callback: Optional[Callable[[PhaseIntent], None]] = None

    # ------------------------------------------------------------------
    # v1.4 Herald wiring
    # ------------------------------------------------------------------

    def wire_herald_trace(self, callback: Callable[[PhaseIntent], None]) -> None:
        """
        Register a herald trace callback — called with each PhaseIntent
        after conductor.step(). Designed for AHGHeraldTrace.on_intent.

        Usage:
            trace = AHGHeraldTrace(session_id="S072")
            sidecar.wire_herald_trace(trace.on_intent)
        """
        self._herald_callback = callback
        logger.info(
            "AHGSidecar herald trace wired: %s",
            getattr(callback, "__qualname__", repr(callback)),
        )

    def unwire_herald_trace(self) -> None:
        """Remove registered herald callback."""
        self._herald_callback = None
        logger.info("AHGSidecar herald trace unwired.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, heartbeat: AgentHeartbeat) -> None:
        turn_id = heartbeat.turn_id
        self._agent_registry.add(heartbeat.agent_id)

        if turn_id not in self._buffers:
            self._buffers[turn_id] = TurnBuffer(turn_id=turn_id)

        self._buffers[turn_id].add(heartbeat)
        logger.debug(
            "AHGSidecar ingested: agent=%s turn=%d D_e=%.3f",
            heartbeat.agent_id, turn_id, heartbeat.D_e_signal,
        )

    def flush(self, turn_id: int) -> Optional[PhaseIntent]:
        """
        Aggregate heartbeats for turn_id → StateVector → AHGConductor.step()
        → emit PhaseIntent to registered herald callback (v1.4).
        """
        buffer = self._buffers.pop(turn_id, None)
        if buffer is None:
            logger.warning("AHGSidecar flush: no buffer for turn=%d", turn_id)
            return None

        sv     = buffer.to_state_vector(self.total_possible_constraints)
        intent = self.conductor.step(sv)

        # v1.4: call registered herald callback
        if self._herald_callback is not None:
            try:
                self._herald_callback(intent)
            except Exception as exc:
                logger.error("AHGSidecar herald callback failed: %s", exc)

        # v1.3 compat: legacy herald_sink
        elif self._legacy_herald_sink is not None:
            try:
                self._legacy_herald_sink(intent)
            except Exception as exc:
                logger.error("AHGSidecar legacy herald_sink failed: %s", exc)

        return intent

    def flush_all_pending(self) -> dict[int, Optional[PhaseIntent]]:
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

    @property
    def herald_wired(self) -> bool:
        """True if a v1.4 herald callback is registered."""
        return self._herald_callback is not None
