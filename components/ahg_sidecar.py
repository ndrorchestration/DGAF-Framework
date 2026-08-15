"""AHG Sidecar — Agent heartbeat aggregation + conductor bridge.

P-42 · Layer 12 — Cognitive Control Plane
Amethyst × COLLEEN · v1.4 · 2026-07-02

Collects AgentHeartbeat signals, maintains per-turn buffers, converts them
into StateVector instances, and delegates to AHGConductor.  Optional Herald
callback wiring is isolated so sink failures cannot break the control loop.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

from components.ahg_conductor import AHGConductor, PhaseIntent, StateVector

logger = logging.getLogger(__name__)


@dataclass
class AgentHeartbeat:
    agent_id: str
    turn_id: int
    D_e_signal: float = 0.0
    N_signal: float = 0.0
    C_signal: float = 0.0
    R_signal: float = 0.0
    D_explore_signal: float = 0.0
    D_correct_signal: float = 0.0
    K_signal: float = 0.0
    constraint_violations: int = 0


@dataclass
class TurnBuffer:
    turn_id: int
    heartbeats: list[AgentHeartbeat] = field(default_factory=list)

    def ingest(self, heartbeat: AgentHeartbeat) -> None:
        self.heartbeats.append(heartbeat)

    def to_state_vector(self, total_possible_constraints: int = 1) -> StateVector:
        if not self.heartbeats:
            return StateVector()

        n = len(self.heartbeats)
        total_constraints = sum(h.constraint_violations for h in self.heartbeats)
        denominator = max(total_possible_constraints * n, 1)

        return StateVector(
            D_e=sum(h.D_e_signal for h in self.heartbeats) / n,
            N=sum(h.N_signal for h in self.heartbeats) / n,
            C=min(total_constraints / denominator, 1.0),
            R=sum(h.R_signal for h in self.heartbeats) / n,
            D_explore=sum(h.D_explore_signal for h in self.heartbeats) / n,
            D_correct=sum(h.D_correct_signal for h in self.heartbeats) / n,
            K=sum(h.K_signal for h in self.heartbeats) / n,
        )


class AHGSidecar:
    def __init__(
        self,
        conductor: Optional[AHGConductor] = None,
        total_possible_constraints: int = 1,
        herald_sink: Optional[Callable[[PhaseIntent], None]] = None,
    ) -> None:
        self.conductor = conductor or AHGConductor()
        self.total_possible_constraints = total_possible_constraints
        self._buffers: dict[int, TurnBuffer] = {}
        self._agent_registry: set[str] = set()
        self._herald_callback: Optional[Callable[[PhaseIntent], None]] = None
        self._legacy_herald_sink = herald_sink

    def wire_herald_trace(self, callback: Callable[[PhaseIntent], None]) -> None:
        self._herald_callback = callback

    def unwire_herald_trace(self) -> None:
        self._herald_callback = None

    def ingest(self, heartbeat: AgentHeartbeat) -> None:
        self._agent_registry.add(heartbeat.agent_id)
        buffer = self._buffers.setdefault(
            heartbeat.turn_id,
            TurnBuffer(turn_id=heartbeat.turn_id),
        )
        buffer.ingest(heartbeat)

    def flush(self, turn_id: int) -> Optional[PhaseIntent]:
        buffer = self._buffers.pop(turn_id, None)
        if buffer is None:
            logger.warning("AHGSidecar flush: no buffer for turn=%d", turn_id)
            return None

        sv = buffer.to_state_vector(self.total_possible_constraints)
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
