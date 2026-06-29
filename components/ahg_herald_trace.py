"""
ahg_herald_trace.py — P-01 Herald Fan-Out Trace Sink — AHG Integration (v1.4 stub)
Pattern: P-42 — Adaptive Harmonic Governance, Layer 12 — Cognitive Control Plane
Version: 1.4-stub
Authors: Amethyst x COLLEEN | 2026-06-29

Responsibilities:
  - Receive PhaseIntent events from AHGSidecar
  - Route to P-01 Herald Fan-Out Trace Sink for audit archival
  - Provide structured trace records for COLLEEN episode archival
  - Expose a simple callback interface for AHGSidecar.wire_herald_trace()

P-01 Integration status:
  v1.3: wire_herald_trace() stub present in AHGSidecar
  v1.4 (this file): structured trace record + in-memory + file sink implemented
  v1.5 (planned): live P-01 Herald HTTP/queue push wired

Usage:
    from components.ahg_herald_trace import AHGHeraldTrace
    from components.ahg_sidecar import AHGSidecar
    from components.ahg_conductor import AHGConductor

    conductor = AHGConductor()
    trace = AHGHeraldTrace(session_id="S077", output_dir=Path("logs/ahg"))
    sidecar = AHGSidecar(conductor=conductor)
    sidecar.wire_herald_trace(trace.on_intent)

    # Now every flush_turn() auto-routes PhaseIntent to trace sink
"""

from __future__ import annotations

import json
import logging
import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger("ahg.herald_trace")

# Guard: PhaseIntent import is optional (P-42 v1.3 may not be installed in all envs)
try:
    from components.ahg_conductor import PhaseIntent
    _CONDUCTOR_AVAILABLE = True
except ImportError:
    _CONDUCTOR_AVAILABLE = False
    PhaseIntent = None  # type: ignore


# ---------------------------------------------------------------------------
# Trace Record
# ---------------------------------------------------------------------------

@dataclass
class AHGTraceRecord:
    """Structured trace record for one PhaseIntent event.
    COLLEEN-archivable. Routes to P-01 Herald Fan-Out in v1.5.
    """
    record_id:       str
    session_id:      str
    turn_id:         int
    timestamp_utc:   str
    archetype:       str
    regime:          str
    phi:             float
    v_phi:           float
    a_phi:           float
    tribunal_active: bool
    ttl:             int
    message:         str
    # Phase space context (optional — from HeartbeatVector.phase_space)
    phase_exploration:  Optional[float] = None
    phase_dissent:      Optional[float] = None
    phase_uncertainty:  Optional[float] = None
    # NDR-STASIS proximity
    ndr_stasis_delta:   Optional[float] = None  # abs(phi - 1.6180339...)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ---------------------------------------------------------------------------
# Herald Trace Sink
# ---------------------------------------------------------------------------

class AHGHeraldTrace:
    """P-01 Herald Fan-Out Trace Sink for AHG PhaseIntent events.

    Implements the callback interface expected by AHGSidecar.wire_herald_trace().
    Maintains an in-memory log and optionally writes JSONL to disk.

    v1.4: In-memory + file sink.
    v1.5 (planned): HTTP/queue push to live P-01 Herald infrastructure.

    Usage:
        trace = AHGHeraldTrace(session_id="S077", output_dir=Path("logs/ahg"))
        sidecar.wire_herald_trace(trace.on_intent)
    """

    NDR_STASIS_PHI = 1.6180339887498949

    def __init__(
        self,
        session_id: str = "unknown",
        output_dir: Optional[Path] = None,
        max_memory_records: int = 10_000,
        emit_tribunal_alerts: bool = True,
        emit_ndr_stasis_alerts: bool = True,
        ndr_stasis_tolerance: float = 0.02,
    ):
        """
        Args:
            session_id: DGAF session ID — stamped on every trace record.
            output_dir: If set, writes JSONL trace file to this directory.
            max_memory_records: Rolling in-memory buffer limit.
            emit_tribunal_alerts: Log WARNING when Tribunal activates.
            emit_ndr_stasis_alerts: Log INFO when phi is within tolerance of NDR-STASIS anchor.
            ndr_stasis_tolerance: phi distance from 1.618 to trigger NDR-STASIS alert.
        """
        self.session_id = session_id
        self.output_dir = Path(output_dir) if output_dir else None
        self.max_memory_records = max_memory_records
        self.emit_tribunal_alerts = emit_tribunal_alerts
        self.emit_ndr_stasis_alerts = emit_ndr_stasis_alerts
        self.ndr_stasis_tolerance = ndr_stasis_tolerance

        self._records: list[AHGTraceRecord] = []
        self._jsonl_path: Optional[Path] = None

        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            fname = f"ahg_trace_{session_id}_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
            self._jsonl_path = self.output_dir / fname
            logger.info(f"[AHGHeraldTrace] JSONL trace file: {self._jsonl_path}")

        logger.info(
            f"[AHGHeraldTrace] Initialised — session={session_id} "
            f"file_sink={'enabled' if self._jsonl_path else 'disabled'}"
        )

    # ------------------------------------------------------------------
    # Primary callback — wired to AHGSidecar via wire_herald_trace()
    # ------------------------------------------------------------------

    def on_intent(self, intent) -> None:
        """Receive a PhaseIntent and route to trace sinks.
        This is the callback provided to AHGSidecar.wire_herald_trace().
        """
        if not _CONDUCTOR_AVAILABLE:
            logger.warning("[AHGHeraldTrace] ahg_conductor not available — skipping trace")
            return

        ndr_delta = abs(intent.phi - self.NDR_STASIS_PHI)

        record = AHGTraceRecord(
            record_id=f"{self.session_id}-T{intent.turn_id}-{intent.archetype.value}",
            session_id=self.session_id,
            turn_id=intent.turn_id,
            timestamp_utc=datetime.datetime.utcnow().isoformat(),
            archetype=intent.archetype.value,
            regime=intent.regime.value,
            phi=intent.phi,
            v_phi=intent.v_phi,
            a_phi=intent.a_phi,
            tribunal_active=intent.tribunal_active,
            ttl=intent.ttl,
            message=intent.message,
            ndr_stasis_delta=round(ndr_delta, 6),
        )

        # In-memory buffer (rolling)
        self._records.append(record)
        if len(self._records) > self.max_memory_records:
            self._records = self._records[-self.max_memory_records:]

        # File sink (JSONL)
        if self._jsonl_path:
            try:
                with open(self._jsonl_path, "a") as f:
                    f.write(record.to_json().replace("\n", " ") + "\n")
            except Exception as exc:
                logger.error(f"[AHGHeraldTrace] File write failed: {exc}")

        # Alerts
        if self.emit_tribunal_alerts and intent.tribunal_active:
            logger.warning(
                f"[AHGHeraldTrace] ⚠️ TRIBUNAL ACTIVE — T{intent.turn_id} phi={intent.phi:.4f}"
            )

        if self.emit_ndr_stasis_alerts and ndr_delta <= self.ndr_stasis_tolerance:
            logger.info(
                f"[AHGHeraldTrace] 🔷 NDR-STASIS proximity — T{intent.turn_id} phi={intent.phi:.4f} "
                f"delta={ndr_delta:.4f} (Integration regime — peak productive phase)"
            )

        # v1.5 hook (planned): push to live P-01 Herald Fan-Out queue
        # self._push_to_p01_queue(record)

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    def records(self, n: int = 20) -> list[AHGTraceRecord]:
        """Return the last n trace records."""
        return self._records[-n:]

    def tribunal_events(self) -> list[AHGTraceRecord]:
        """Return all records where tribunal_active=True."""
        return [r for r in self._records if r.tribunal_active]

    def ndr_stasis_events(self, tolerance: Optional[float] = None) -> list[AHGTraceRecord]:
        """Return records where phi is within tolerance of NDR-STASIS anchor (1.618...)."""
        tol = tolerance or self.ndr_stasis_tolerance
        return [r for r in self._records if r.ndr_stasis_delta is not None and r.ndr_stasis_delta <= tol]

    def phi_series(self, n: int = 50) -> list[float]:
        """Return last n phi values from trace."""
        return [r.phi for r in self._records[-n:]]

    def summary(self) -> dict:
        """Return a summary dict for COLLEEN episode archival."""
        if not self._records:
            return {"session_id": self.session_id, "total_records": 0}
        phis = [r.phi for r in self._records]
        return {
            "session_id": self.session_id,
            "total_records": len(self._records),
            "phi_min": round(min(phis), 4),
            "phi_max": round(max(phis), 4),
            "phi_mean": round(sum(phis) / len(phis), 4),
            "tribunal_events": len(self.tribunal_events()),
            "ndr_stasis_events": len(self.ndr_stasis_events()),
            "archetype_distribution": {
                a: sum(1 for r in self._records if r.archetype == a)
                for a in {r.archetype for r in self._records}
            },
            "jsonl_path": str(self._jsonl_path) if self._jsonl_path else None,
        }

    # ------------------------------------------------------------------
    # v1.5 P-01 queue push (planned)
    # ------------------------------------------------------------------

    def _push_to_p01_queue(self, record: AHGTraceRecord) -> None:
        """
        v1.5 (planned): Push trace record to P-01 Herald Fan-Out queue.
        Wire to live Herald HTTP endpoint or message queue.
        Stub raises NotImplementedError to prevent accidental premature use.
        """
        raise NotImplementedError(
            "P-01 Herald Fan-Out live push not implemented. "
            "Wire in v1.5 when Herald HTTP endpoint is available."
        )
