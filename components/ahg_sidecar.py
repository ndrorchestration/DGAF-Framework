"""
ahg_sidecar.py — AHG Sidecar Monitor
P-42 · Layer 12 — Cognitive Control Plane · v1.4.1
Amethyst × COLLEEN · S072 · 2026-07-02

Spec: docs/theory/AHG_ARCHITECTURE.md v1.2 §4
Pattern card: patterns/P-42_AHG.md v1.3-card

v1.3:   scaffold — heartbeat ingestion, aggregation, conductor flush, herald stub
v1.4:   wire_herald_trace(callback) added; flush() calls herald callback;
        aligned with ahg_herald_trace.py v1.5 AHGHeraldTrace.on_intent()
v1.4.1: StateVector input clip guards — all six signal axes clipped to [0.0, 1.0]
        in to_state_vector(); WARNING log on out-of-range agent signals.
        Closes Apogee Lens AL-PV-01 open item 2.
        Precondition for PV-01 Gold Star: inputs ∈ [0,1] now enforced.

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


def _clip(value: float, lo: float, hi: float, field_name: str, agent_id: str) -> float:
    """Clip value to [lo, hi]. Emits WARNING if out of range so miscalibrated
    agents are visible in the Herald trace. Precondition for φ ∈ (1.0, 1.8).
    """
    if value < lo or value > hi:
        logger.warning(
            "AHGSidecar clip: agent=%s field=%s raw=%.4f clipped to [%.1f, %.1f]. "
            "Miscalibrated heartbeat signal — check agent normalization.",
            agent_id, field_name, value, lo, hi,
        )
        return max(lo, min(hi, value))
    return value


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

        All six signal axes are clipped to [0.0, 1.0] (AL-PV-01 hardening).
        This enforces the precondition required for φ ∈ (1.0, 1.8) by construction
        (AHG_ARCHITECTURE.md §2.2 / Apogee Lens review AL-PV-01).

        WARNING logs are emitted for any out-of-range raw signal so that
        miscalibrated agents are visible in the Herald trace.

        D_explore and D_correct tracked separately (excluded from S(t) in conductor).
        """
        if not self.heartbeats:
            return StateVector()

        n = len(self.heartbeats)
        D_e_raw       = sum(h.D_e_signal       for h in self.heartbeats) / n
        D_explore_raw = sum(h.D_explore_signal for h in self.heartbeats) / n
        D_correct_raw = sum(h.D_correct_signal for h in self.heartbeats) / n
        N_raw         = sum(h.novelty_signal   for h in self.heartbeats) / n
        C_raw         = sum(h.constraint_count for h in self.heartbeats) / max(
                            total_possible_constraints, 1
                        )
        R_raw         = sum(h.revision_count   for h in self.heartbeats) / n / 10.0
        K_raw         = sum(h.coherence_signal for h in self.heartbeats) / n

        agent_ids = ", ".join(sorted({h.agent_id for h in self.heartbeats}))

        D_e       = _clip(D_e_raw,       0.0, 1.0, "D_e",       agent_ids)
        D_explore = _clip(D_explore_raw, 0.0, 1.0, "D_explore", agent_ids)
        D_correct = _clip(D_correct_raw, 0.0, 1.0, "D_correct", agent_ids)
        N         = _clip(N_raw,         0.0, 1.0, "N",         agent_ids)
        C         = _clip(C_raw,         0.0, 1.0, "C",         agent_ids)
        R         = _clip(R_raw,         0.0, 1.0, "R",         agent_ids)
        K         = _clip(K_raw,         0.0, 1.0, "K",         agent_ids)

        return StateVector(
            D_e=D_e, D_explore=D_explore, D_correct=D_correct,
            N=N, C=C, R=R, M=0.0, K=K,
        )


class AHGSidecar:
    """AHG Sidecar Monitor — O(n) heartbeat aggregation and turn-level flush."""

    def __init__(
        self,
        conductor: AHGConductor,
        herald_sink=None,
        total_possible_constraints: int = 10,
    ) -> None:
        self.conductor = conductor
        self._legacy_herald_sink = herald_sink
        self.total_possible_constraints = total_possible_constraints
        self._buffers: dict[int, TurnBuffer] = {}
        self._agent_registry: set[str] = set()
        self._herald_callback: Optional[Callable[[PhaseIntent], None]] = None

    def wire_herald_trace(self, callback: Callable[[PhaseIntent], None]) -> None:
        """Register a herald trace callback."""
        self._herald_callback = callback
        logger.info(
            "AHGSidecar herald trace wired: %s",
            getattr(callback, "__qualname__", repr(callback)),
        )

    def unwire_herald_trace(self) -> None:
        """Remove registered herald callback."""
        self._herald_callback = None
        logger.info("AHGSidecar herald trace unwired.")

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
        """Aggregate heartbeats and emit a PhaseIntent."""
        buffer = self._buffers.pop(turn_id, None)
        if buffer is None:
            logger.warning("AHGSidecar flush: no buffer for turn=%d", turn_id)
            return None

        sv     = buffer.to_state_vector(self.total_possible_constraints)
        intent = self.conductor.step(sv)

        if self._herald_callback is not None:
            try:
                self._herald_callback(intent)
            except Exception as exc:
                logger.error("AHGSidecar herald callback failed: %s", exc)

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
