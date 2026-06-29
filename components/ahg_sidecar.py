"""
ahg_sidecar.py — AHG Sidecar Observability Layer (v1.5)
Pattern: P-42 — Adaptive Harmonic Governance, Layer 12 — Cognitive Control Plane
Version: 1.5
Authors: Amethyst × COLLEEN | 2026-06-29

Responsibilities:
  - Accept per-agent HeartbeatVectors each turn (submit_heartbeat)
  - Aggregate heartbeats and call AHGConductor.observe() on flush_turn()
  - Broadcast resulting PhaseIntent to all registered trace callbacks
  - v1.5: wire_herald_trace() fully wired — accepts live AHGHeraldTrace.on_intent
    Supports multiple callbacks (multi-subscriber fan-out)

Change log:
  v1.3: Initial scaffold — wire_herald_trace() stub (no-op)
  v1.4: In-memory buffer + auto-flush on expected_agents submitted
  v1.5: wire_herald_trace() fully operational — stores callbacks in list,
        broadcasts PhaseIntent to all subscribers on every flush_turn()
        Added: unregister_herald_trace(), list_herald_traces(), broadcast stats
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, List, Optional

logger = logging.getLogger("ahg.sidecar")

try:
    from components.ahg_conductor import AHGConductor, HeartbeatVector, PhaseIntent, AggregatedSignals
    _CONDUCTOR_AVAILABLE = True
except ImportError:
    _CONDUCTOR_AVAILABLE = False
    AHGConductor = None  # type: ignore
    HeartbeatVector = None  # type: ignore
    PhaseIntent = None  # type: ignore
    AggregatedSignals = None  # type: ignore


# ---------------------------------------------------------------------------
# Turn Buffer
# ---------------------------------------------------------------------------

@dataclass
class TurnBuffer:
    """Accumulates HeartbeatVectors for a single turn before flush."""
    turn_id: int
    heartbeats: List = field(default_factory=list)

    def add(self, hb) -> None:
        self.heartbeats.append(hb)

    @property
    def agent_ids(self) -> List[str]:
        return [hb.agent_id for hb in self.heartbeats]

    def aggregate(self) -> "AggregatedSignals":
        """Aggregate all heartbeats for this turn into AggregatedSignals."""
        if not self.heartbeats:
            raise ValueError(f"TurnBuffer T{self.turn_id}: no heartbeats to aggregate")
        n = len(self.heartbeats)
        return AggregatedSignals(
            d_e=sum(hb.d_e for hb in self.heartbeats) / n,
            d_explore=sum(hb.d_explore for hb in self.heartbeats) / n,
            d_correct=sum(hb.d_correct for hb in self.heartbeats) / n,
            novelty=sum(hb.novelty for hb in self.heartbeats) / n,
            constraint_compliance=(
                sum(hb.constraint_count for hb in self.heartbeats) /
                max(1, sum(hb.total_constraints for hb in self.heartbeats))
            ),
            revision_load=(
                sum(hb.revision_count for hb in self.heartbeats) /
                max(1, sum(hb.total_turns for hb in self.heartbeats))
            ),
        )


# ---------------------------------------------------------------------------
# AHGSidecar
# ---------------------------------------------------------------------------

class AHGSidecar:
    """O(n) Observability Layer for the Adaptive Harmonic Governance system.

    Separates state estimation (heartbeat aggregation) from governance control
    (AHGConductor.observe). Agents submit lightweight HeartbeatVectors each turn;
    AHGSidecar aggregates and drives the conductor, then fans out the resulting
    PhaseIntent to all registered herald trace callbacks.

    v1.5: wire_herald_trace() fully operational with multi-subscriber fan-out.

    Usage:
        conductor = AHGConductor()
        sidecar = AHGSidecar(conductor=conductor, expected_agents=["A", "B", "C"])

        # Wire P-01 Herald trace (v1.5)
        from components.ahg_herald_trace import AHGHeraldTrace
        trace = AHGHeraldTrace(session_id="S077")
        sidecar.wire_herald_trace(trace.on_intent)

        # Each agent submits heartbeat
        sidecar.submit_heartbeat(HeartbeatVector(agent_id="A", turn_id=1, ...))
        sidecar.submit_heartbeat(HeartbeatVector(agent_id="B", turn_id=1, ...))
        sidecar.submit_heartbeat(HeartbeatVector(agent_id="C", turn_id=1, ...))
        # Auto-flush fires when all 3 agents submitted
        intent = sidecar.last_intent  # PhaseIntent for T1
    """

    def __init__(
        self,
        conductor: Optional["AHGConductor"] = None,
        expected_agents: Optional[List[str]] = None,
        auto_flush: bool = True,
    ):
        """
        Args:
            conductor: AHGConductor instance. Required for live operation.
            expected_agents: List of agent IDs expected each turn.
                             Auto-flush triggers when all have submitted.
                             If None, manual flush_turn() required.
            auto_flush: Enable automatic flush when all expected_agents submitted.
        """
        if not _CONDUCTOR_AVAILABLE:
            logger.warning("[AHGSidecar] ahg_conductor not available — sidecar in stub mode")

        self.conductor = conductor
        self.expected_agents = set(expected_agents) if expected_agents else set()
        self.auto_flush = auto_flush

        self._buffers: dict[int, TurnBuffer] = {}  # turn_id → TurnBuffer
        self._herald_callbacks: List[Callable] = []  # v1.5 multi-subscriber
        self._broadcast_count = 0
        self._broadcast_errors = 0
        self.last_intent: Optional["PhaseIntent"] = None
        self._turn_history: List["PhaseIntent"] = []  # rolling last-100

        logger.info(
            f"[AHGSidecar] v1.5 ready — "
            f"auto_flush={auto_flush} "
            f"expected_agents={sorted(self.expected_agents) if self.expected_agents else 'manual'}"
        )

    # ------------------------------------------------------------------
    # Heartbeat ingestion
    # ------------------------------------------------------------------

    def submit_heartbeat(self, hb: "HeartbeatVector") -> None:
        """Accept a per-agent HeartbeatVector for the current turn.

        Thread-safe for sequential per-turn submission.
        Triggers auto-flush if all expected_agents have submitted.
        """
        if hb.turn_id not in self._buffers:
            self._buffers[hb.turn_id] = TurnBuffer(turn_id=hb.turn_id)
        self._buffers[hb.turn_id].add(hb)
        logger.debug(
            f"[AHGSidecar] Heartbeat T{hb.turn_id} from '{hb.agent_id}' "
            f"d_e={hb.d_e:.3f} novelty={hb.novelty:.3f}"
        )

        # Auto-flush when all expected agents have submitted
        if self.auto_flush and self.expected_agents:
            submitted = set(self._buffers[hb.turn_id].agent_ids)
            if self.expected_agents.issubset(submitted):
                logger.debug(f"[AHGSidecar] Auto-flush T{hb.turn_id} — all agents submitted")
                self.flush_turn(hb.turn_id)

    # ------------------------------------------------------------------
    # Flush
    # ------------------------------------------------------------------

    def flush_turn(self, turn_id: int) -> "PhaseIntent":
        """Aggregate heartbeats for turn_id, drive AHGConductor, broadcast PhaseIntent.

        Raises:
            ValueError: if no heartbeats found for turn_id.
            RuntimeError: if conductor not configured.
        """
        if turn_id not in self._buffers:
            raise ValueError(f"[AHGSidecar] flush_turn({turn_id}): no heartbeats in buffer")

        buf = self._buffers.pop(turn_id)
        if not buf.heartbeats:
            raise ValueError(f"[AHGSidecar] flush_turn({turn_id}): empty buffer")

        if self.conductor is None:
            raise RuntimeError("[AHGSidecar] flush_turn: conductor not configured")

        signals = buf.aggregate()
        intent: PhaseIntent = self.conductor.observe(signals)

        self.last_intent = intent
        self._turn_history.append(intent)
        if len(self._turn_history) > 100:
            self._turn_history = self._turn_history[-100:]

        # Fan-out to all herald callbacks (v1.5)
        self._broadcast(intent)

        logger.debug(
            f"[AHGSidecar] Flushed T{turn_id} → "
            f"phi={intent.phi:.4f} archetype={intent.archetype.value} "
            f"tribunal={intent.tribunal_active} "
            f"callbacks_fired={len(self._herald_callbacks)}"
        )
        return intent

    def _broadcast(self, intent: "PhaseIntent") -> None:
        """Fan-out PhaseIntent to all registered herald callbacks."""
        for cb in self._herald_callbacks:
            try:
                cb(intent)
                self._broadcast_count += 1
            except Exception as exc:
                self._broadcast_errors += 1
                logger.error(
                    f"[AHGSidecar] Herald callback error "
                    f"({cb.__qualname__ if hasattr(cb, '__qualname__') else repr(cb)}): {exc}"
                )

    # ------------------------------------------------------------------
    # Herald trace wiring (v1.5 — fully operational)
    # ------------------------------------------------------------------

    def wire_herald_trace(self, callback: Callable) -> None:
        """Register a callback to receive every PhaseIntent after flush_turn().

        Supports multiple subscribers (fan-out). Call wire_herald_trace() multiple
        times to register additional callbacks. All are invoked in registration order.

        Primary use: AHGHeraldTrace.on_intent from components.ahg_herald_trace

        Args:
            callback: Callable that accepts a PhaseIntent instance.
                      Must not raise — exceptions are caught and logged.

        Example:
            trace = AHGHeraldTrace(session_id="S077")
            sidecar.wire_herald_trace(trace.on_intent)
        """
        if callback in self._herald_callbacks:
            logger.warning(
                f"[AHGSidecar] wire_herald_trace: callback already registered — "
                f"{getattr(callback, '__qualname__', repr(callback))}"
            )
            return
        self._herald_callbacks.append(callback)
        logger.info(
            f"[AHGSidecar] Herald trace registered "
            f"({getattr(callback, '__qualname__', repr(callback))}) — "
            f"total callbacks: {len(self._herald_callbacks)}"
        )

    def unregister_herald_trace(self, callback: Callable) -> bool:
        """Remove a previously registered herald callback. Returns True if removed."""
        try:
            self._herald_callbacks.remove(callback)
            logger.info(
                f"[AHGSidecar] Herald trace unregistered — "
                f"{getattr(callback, '__qualname__', repr(callback))}"
            )
            return True
        except ValueError:
            return False

    def list_herald_traces(self) -> List[str]:
        """Return list of registered callback names (for diagnostics)."""
        return [
            getattr(cb, "__qualname__", repr(cb))
            for cb in self._herald_callbacks
        ]

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    def intent_history(self, n: int = 20) -> List["PhaseIntent"]:
        """Return last n PhaseIntents from turn history."""
        return self._turn_history[-n:]

    def broadcast_stats(self) -> dict:
        return {
            "registered_callbacks": len(self._herald_callbacks),
            "callback_names": self.list_herald_traces(),
            "total_broadcasts": self._broadcast_count,
            "broadcast_errors": self._broadcast_errors,
        }
