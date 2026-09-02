"""
Triadic Governance Loop (TGL) — canonical 10-step governance sequencer.
DGAF-Framework · pptl

The TGL is a deterministic gate sequencer. Unwired required gates are
recorded as SKIP and reduce the turn to ESCALATE; SKIP is never implicit PASS.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

from .procluding_premise import (
    DGAF_CONSTITUTIONAL_INVARIANTS,
    PremiseViolationError,
    ProcludingPremiseGate,
)


class GateResult(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    KILL = "KILL"
    SKIP = "SKIP"


class TurnStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    ESCALATE = "ESCALATE"
    KILL = "KILL"
    KILL_REC = "KILL_REC"


@dataclass(frozen=True)
class GateRecord:
    step: int
    pattern: str
    gate_name: str
    result: GateResult
    notes: str = ""


@dataclass
class TurnAuditRecord:
    """Audit record whose final cryptographic seal covers the complete gate set."""

    session_id: str
    turn_index: int
    agent_id: str
    input_hash: str
    gate_records: list[GateRecord]
    final_status: TurnStatus
    timestamp: str
    seal_hash: str = field(default="", init=False)

    def _canonical_payload(self) -> bytes:
        payload = {
            "session_id": self.session_id,
            "turn_index": self.turn_index,
            "agent_id": self.agent_id,
            "input_hash": self.input_hash,
            "final_status": self.final_status.value,
            "timestamp": self.timestamp,
            "gates": [
                {
                    "step": g.step,
                    "pattern": g.pattern,
                    "gate": g.gate_name,
                    "result": g.result.value,
                    "notes": g.notes,
                }
                for g in self.gate_records
            ],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def seal(self) -> str:
        """Seal the exact current audit contents, including every gate record."""
        self.seal_hash = hashlib.sha256(self._canonical_payload()).hexdigest()
        return self.seal_hash

    def to_dict(self) -> dict[str, Any]:
        self.seal()
        return {
            "event_type": "TGL_TURN_AUDIT",
            "session_id": self.session_id,
            "turn_index": self.turn_index,
            "agent_id": self.agent_id,
            "input_hash": self.input_hash,
            "final_status": self.final_status.value,
            "timestamp": self.timestamp,
            "seal_hash": self.seal_hash,
            "gates": [
                {
                    "step": g.step,
                    "pattern": g.pattern,
                    "gate": g.gate_name,
                    "result": g.result.value,
                    "notes": g.notes,
                }
                for g in self.gate_records
            ],
        }


@dataclass
class TGLHooks:
    """Hook functions for each TGL step. None means the gate is unwired/SKIP."""

    premise_check_fn: Optional[Callable] = None
    scpe_fn: Optional[Callable] = None
    pdmal_fn: Optional[Callable] = None
    demijoul_fn: Optional[Callable] = None
    kappa_fn: Optional[Callable] = None
    sentinel_fn: Optional[Callable] = None
    phi_closure_fn: Optional[Callable] = None
    hpg_fn: Optional[Callable] = None
    apogee_fn: Optional[Callable] = None
    herald_fn: Optional[Callable] = None


class TriadicGovernanceLoop:
    """Canonical 10-step governance turn sequencer."""

    GATE_MANIFEST = [
        (0, "P-35", "ProcludingPremiseGate"),
        (1, "P-31", "SCPE_Prune"),
        (2, "P-33", "PDMAL_ConvergenceMonitor"),
        (3, "N/A", "DemiJoule_SafetyGate"),
        (4, "P-27", "KAPPA_Router"),
        (5, "P-29", "Sentinel_RiskPass"),
        (6, "P-32", "PhiClosure_Gate"),
        (7, "N/A", "HPG_OctaveGate"),
        (8, "P-30", "Apogee_AttestationGate"),
        (9, "P-01", "Herald_FanOut"),
    ]

    # Required gates. Step 7 is conditional on Phi-Closure PASS.
    REQUIRED_STEPS = frozenset({1, 2, 3, 4, 5, 6, 8})

    def __init__(
        self,
        session_id: str,
        agent_id: str,
        hooks: TGLHooks,
        turn_counter: int = 0,
    ) -> None:
        self.session_id = session_id
        self.agent_id = agent_id
        self.hooks = hooks
        self._turn_counter = turn_counter
        self._premise_gate = ProcludingPremiseGate(
            invariants=DGAF_CONSTITUTIONAL_INVARIANTS,
            session_id=session_id,
            agent_id=agent_id,
        )

    @property
    def turn_counter(self) -> int:
        return self._turn_counter

    def _hash_input(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _run_hook(
        self,
        hook_fn: Optional[Callable],
        input_text: str,
        context: dict,
        step: int,
        pattern: str,
        gate_name: str,
    ) -> GateRecord:
        if hook_fn is None:
            return GateRecord(step, pattern, gate_name, GateResult.SKIP, "not wired")
        try:
            result = hook_fn(input_text, context)
            gate_result = GateResult(result) if isinstance(result, str) else result
            if not isinstance(gate_result, GateResult):
                return GateRecord(step, pattern, gate_name, GateResult.KILL, "invalid gate result")
            return GateRecord(step, pattern, gate_name, gate_result)
        except Exception as exc:
            return GateRecord(step, pattern, gate_name, GateResult.KILL, str(exc)[:120])

    @staticmethod
    def _reduce_status(gates: list[GateRecord], initial: TurnStatus = TurnStatus.PASS) -> TurnStatus:
        """Apply the monotonic gate lattice: KILL > ESCALATE > WARN > PASS."""
        if any(g.result == GateResult.KILL for g in gates):
            return TurnStatus.KILL
        if any(g.step in TriadicGovernanceLoop.REQUIRED_STEPS and g.result == GateResult.SKIP for g in gates):
            return TurnStatus.ESCALATE
        if any(g.result == GateResult.WARN for g in gates):
            return TurnStatus.WARN
        return initial

    def _emit_herald_and_seal(
        self,
        audit: TurnAuditRecord,
        context: dict,
        
    ) -> TurnAuditRecord:
        """Publish a pre-Herald snapshot, append Herald result, reduce again, then final-seal the complete set."""
        herald_record = self._run_hook(
            self.hooks.herald_fn,
            "",
            {**context, "audit_record": audit.to_dict(), "seal_scope": "pre_herald"},
            9,
            "P-01",
            "Herald_FanOut",
        )
        audit.gate_records.append(herald_record)
        audit.final_status = self._reduce_status(audit.gate_records, initial=audit.final_status)
        audit.seal()
        return audit

    def run_turn(
        self,
        input_text: str,
        context: Optional[dict] = None,
    ) -> TurnAuditRecord:
        """Execute the TGL sequence and return an audit sealed over the final gate set."""
        context = {} if context is None else context
        self._turn_counter += 1
        input_hash = self._hash_input(input_text)
        timestamp = datetime.now(timezone.utc).isoformat()
        gates: list[GateRecord] = []

        try:
            self._premise_gate.evaluate(input_text, check_fn=self.hooks.premise_check_fn)
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS))
        except PremiseViolationError as exc:
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.KILL, str(exc)[:120]))
            audit = TurnAuditRecord(
                self.session_id, self._turn_counter, self.agent_id, input_hash,
                gates, TurnStatus.KILL, timestamp,
            )
            self._emit_herald_and_seal(audit, context)
            return audit
        except Exception as exc:
            # P-35 is fail-closed even when the supplied checker itself fails.
            # An unexpected checker exception becomes a sealed KILL audit rather
            # than bypassing the constitutional gate or escaping the TGL boundary.
            gates.append(
                GateRecord(
                    0,
                    "P-35",
                    "ProcludingPremiseGate",
                    GateResult.KILL,
                    f"premise-check-exception:{type(exc).__name__}: {exc}"[:120],
                )
            )
            audit = TurnAuditRecord(
                self.session_id, self._turn_counter, self.agent_id, input_hash,
                gates, TurnStatus.KILL, timestamp,
            )
            return self._emit_herald_and_seal(audit, context)

        hook_sequence = [
            (1, "P-31", "SCPE_Prune", self.hooks.scpe_fn),
            (2, "P-33", "PDMAL_ConvergenceMonitor", self.hooks.pdmal_fn),
            (3, "N/A", "DemiJoule_SafetyGate", self.hooks.demijoul_fn),
            (4, "P-27", "KAPPA_Router", self.hooks.kappa_fn),
            (5, "P-29", "Sentinel_RiskPass", self.hooks.sentinel_fn),
            (6, "P-32", "PhiClosure_Gate", self.hooks.phi_closure_fn),
        ]

        terminated = False
        phi_closure_result = GateResult.SKIP
        for step, pattern, gate_name, hook_fn in hook_sequence:
            rec = self._run_hook(hook_fn, input_text, context, step, pattern, gate_name)
            gates.append(rec)
            if step == 6:
                phi_closure_result = rec.result
            if rec.result == GateResult.KILL:
                terminated = True
                break

        # Conditional HPG: only after a PASS from Phi-Closure.
        if not terminated:
            if phi_closure_result == GateResult.PASS:
                gates.append(self._run_hook(self.hooks.hpg_fn, input_text, context, 7, "N/A", "HPG_OctaveGate"))
            else:
                gates.append(GateRecord(7, "N/A", "HPG_OctaveGate", GateResult.SKIP, "conditional on Phi-Closure PASS"))

        # Apogee step 8 is only reachable if no prior KILL and all required gates are wired.
        if not terminated:
            gates.append(self._run_hook(self.hooks.apogee_fn, input_text, context, 8, "P-30", "Apogee_AttestationGate"))

        final_status = self._reduce_status(gates)
        audit = TurnAuditRecord(
            self.session_id, self._turn_counter, self.agent_id, input_hash,
            gates, final_status, timestamp,
        )
        return self._emit_herald_and_seal(audit, context)
