"""
ahg_sidecar.py — AHG Sidecar Monitor
Pattern: P-42 — Adaptive Harmonic Governance, Layer 12 — Cognitive Control Plane
Version: 1.3 (scaffold)
Authors: Amethyst x COLLEEN | 2026-06-29

Responsibilities:
  - Accept per-agent HeartbeatVector submissions (O(n) — never parses full context)
  - Aggregate heartbeats per turn
  - Pass aggregated signals to AHGConductor for phi computation and archetype dispatch
  - Route PhaseIntent back to agents / Phase-1 Herald trace sink (P-01)
  - Provide async-compatible interface for future live-wiring

Architecture:
  Agents --> Sidecar.submit_heartbeat() --> AHGConductor.observe() --> PhaseIntent
  Sidecar never reads full agent context — only compressed HeartbeatVector fields.
  This separation keeps state estimation O(n), not O(n * context_length).

P-01 Integration (planned v1.4):
  PhaseIntent events will be routed through the Herald Fan-Out Trace Sink
  once the sidecar is wired to the live trace infrastructure.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Callable, Optional

from components.ahg_conductor import (
    AHGConductor,
    HeartbeatVector,
    PhaseIntent,
    Archetype,
)

logger = logging.getLogger("ahg.sidecar")


# ---------------------------------------------------------------------------
# Sidecar Monitor
# ---------------------------------------------------------------------------

class AHGSidecar:
    """O(n) Sidecar Monitor — separates state estimation from governance control.

    Usage:
        conductor = AHGConductor()
        sidecar = AHGSidecar(conductor=conductor)

        # Each agent submits its heartbeat:
        sidecar.submit_heartbeat(HeartbeatVector(agent_id="Herald", turn_id=5, ...))
        sidecar.submit_heartbeat(HeartbeatVector(agent_id="DemiJoule", turn_id=5, ...))

        # When all agents for a turn have submitted, flush:
        intent = sidecar.flush_turn(turn_id=5)
        # intent is the PhaseIntent to broadcast to all agents
    """

    def __init__(
        self,
        conductor: AHGConductor,
        expected_agents: Optional[list[str]] = None,
        auto_flush: bool = False,
        intent_callback: Optional[Callable[[PhaseIntent], None]] = None,
    ):
        """
        Args:
            conductor: AHGConductor instance (PSC).
            expected_agents: If set, flush_turn() will validate all expected agents submitted.
            auto_flush: If True, automatically flush when all expected_agents have submitted.
            intent_callback: Optional callback invoked with PhaseIntent after each flush.
                             Use this to route intents to P-01 Herald trace sink.
        """
        self.conductor = conductor
        self.expected_agents = set(expected_agents) if expected_agents else None
        self.auto_flush = auto_flush
        self.intent_callback = intent_callback

        # turn_id -> list of HeartbeatVector
        self._pending: dict[int, list[HeartbeatVector]] = defaultdict(list)
        self._intent_log: list[PhaseIntent] = []
        self._last_coherence_delta: float = 0.0

        logger.info("AHGSidecar initialised (P-42 v1.3)")

    # ------------------------------------------------------------------
    # Primary interface
    # ------------------------------------------------------------------

    def submit_heartbeat(self, hb: HeartbeatVector) -> Optional[PhaseIntent]:
        """Accept a heartbeat from one agent for a given turn.

        Returns PhaseIntent if auto_flush is enabled and all expected agents
        have submitted; otherwise returns None.
        """
        self._pending[hb.turn_id].append(hb)
        logger.debug(f"[Sidecar] HB received: agent={hb.agent_id} turn={hb.turn_id} D_e={hb.d_e:.3f}")

        if self.auto_flush and self.expected_agents:
            submitted = {h.agent_id for h in self._pending[hb.turn_id]}
            if submitted >= self.expected_agents:
                return self.flush_turn(hb.turn_id)

        return None

    def flush_turn(
        self,
        turn_id: int,
        coherence_delta: float = 0.0,
    ) -> PhaseIntent:
        """Aggregate heartbeats for turn_id and dispatch to conductor.

        Args:
            turn_id: The turn to flush.
            coherence_delta: Change in collective coherence K this turn (positive = improving).

        Returns:
            PhaseIntent from the conductor.

        Raises:
            ValueError: If no heartbeats exist for turn_id.
        """
        heartbeats = self._pending.get(turn_id)
        if not heartbeats:
            raise ValueError(f"[Sidecar] No heartbeats for turn {turn_id}")

        if self.expected_agents:
            submitted = {h.agent_id for h in heartbeats}
            missing = self.expected_agents - submitted
            if missing:
                logger.warning(f"[Sidecar] Missing heartbeats for turn {turn_id}: {missing}")

        intent = self.conductor.observe(
            heartbeats=heartbeats,
            turn_id=turn_id,
            coherence_delta=coherence_delta,
        )

        self._intent_log.append(intent)
        del self._pending[turn_id]

        # Route to P-01 callback (Herald trace sink) if wired
        if self.intent_callback:
            try:
                self.intent_callback(intent)
            except Exception as exc:
                logger.error(f"[Sidecar] intent_callback failed: {exc}")

        # Log Tribunal events prominently
        if intent.tribunal_active:
            logger.warning(
                f"[Sidecar T{turn_id}] TRIBUNAL | phi={intent.phi:.4f} | {intent.message}"
            )
        elif intent.archetype == Archetype.INTEGRATOR:
            ndr_dist = abs(intent.phi - 1.6180339)
            logger.info(
                f"[Sidecar T{turn_id}] INTEGRATION (NDR-STASIS dist={ndr_dist:.4f}) | phi={intent.phi:.4f}"
            )
        else:
            logger.info(f"[Sidecar T{turn_id}] {intent.archetype.value} | phi={intent.phi:.4f}")

        return intent

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    def intent_history(self, n: int = 10) -> list[PhaseIntent]:
        """Return the last n PhaseIntent records."""
        return self._intent_log[-n:]

    def pending_turns(self) -> list[int]:
        """Return turn_ids with pending (unflushed) heartbeats."""
        return list(self._pending.keys())

    def phi_series(self, n: int = 10) -> list[float]:
        """Return the last n phi values from intent log."""
        return [i.phi for i in self._intent_log[-n:]]

    def set_coherence_delta(self, delta: float) -> None:
        """Update the coherence delta to use on the next flush."""
        self._last_coherence_delta = delta

    # ------------------------------------------------------------------
    # P-01 wiring (v1.4)
    # ------------------------------------------------------------------

    def wire_herald_trace(self, callback: Callable[[PhaseIntent], None]) -> None:
        """Wire the PhaseIntent callback to the P-01 Herald Fan-Out Trace Sink.
        Call this once during system boot to route governance events to the audit log.
        (v1.4 — full P-01 integration pending.)
        """
        self.intent_callback = callback
        logger.info("[Sidecar] Herald trace sink wired (P-01 integration)")
