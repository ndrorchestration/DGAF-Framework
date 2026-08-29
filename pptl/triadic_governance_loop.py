"""
Triadic Governance Loop (TGL) — canonical 10-step governance sequencer.
DGAF-Framework · pptl · S068

Authority: Triumvirate (P-08/P-09)
  Prime:     Amethyst
  Prefect A: COLLEEN
  Prefect B: Apogee

The TGL is a deterministic gate sequencer. Each step is independently
hookable; an unset hook is recorded as SKIP (never implicit PASS).
"""
from __future__ import annotations

import hashlib
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
    """
    Immutable-at-boundary audit record for one TGL turn.

    Emitted to Herald sink (P-01) on PASS.
    Emitted with KILL status to dead-letter on any terminal failure.
    """
    session_id: str
    turn_index: int
    agent_id: str
    input_hash: str
    gate_records: list[GateRecord]
    final_status: TurnStatus
    timestamp: str
    seal_hash: str = field(default="", init=False)

    def seal(self) -> str:
        gates_payload = "|".join(
            f"{g.step}:{g.pattern}:{g.gate_name}:{g.result.value}:{g.notes}"
            for g in self.gate_records
        )
        payload = (
            f"{self.session_id}|{self.turn_index}|{self.agent_id}|"
            f"{self.input_hash}|{self.final_status}|{self.timestamp}|{gates_payload}"
        )
        self.seal_hash = hashlib.sha256(payload.encode()).hexdigest()
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
    """
    Hook functions wired to each TGL step.
    Each hook: (input_text: str, context: dict) -> GateResult
    None = SKIP (gate not wired in this deployment).

    Minimum viable wiring: premise_gate is always populated.
    All other gates are optional for incremental integration.
    """
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


@dataclass
class TriadicGovernanceLoop:
    session_id: str
    agent_id: str
    hooks: TGLHooks = field(default_factory=TGLHooks)
    turn_counter: int = 0

    def _run_hook(
        self,
        hook_fn: Optional[Callable],
        input_text: str,
        context: dict[str, Any],
        step: int,
        pattern: str,
        gate_name: str,
    ) -> GateRecord:
        if hook_fn is None:
            return GateRecord(step, pattern, gate_name, GateResult.SKIP, "Hook not wired")
        result = hook_fn(input_text, context)
        if not isinstance(result, GateResult):
            result = GateResult(str(result))
        return GateRecord(step, pattern, gate_name, result)

    def run_turn(self, input_text: str, context: Optional[dict[str, Any]] = None) -> TurnAuditRecord:
        if context is None:
            context = {}
        self.turn_counter += 1
        timestamp = datetime.now(timezone.utc).isoformat()
        input_hash = hashlib.sha256(input_text.encode("utf-8")).hexdigest()
        gates: list[GateRecord] = []
        final_status = TurnStatus.PASS

        premise = ProcludingPremiseGate(DGAF_CONSTITUTIONAL_INVARIANTS)
        try:
            premise_result = premise.check(input_text)
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS if premise_result else GateResult.KILL))
            if not premise_result:
                final_status = TurnStatus.KILL_REC
                rec = TurnAuditRecord(self.session_id, self.turn_counter, self.agent_id, input_hash, gates, final_status, timestamp)
                rec.seal()
                if self.hooks.herald_fn:
                    self.hooks.herald_fn(rec.to_dict(), context)
                raise PremiseViolationError("P-35 constitutional invariant violated")
        except PremiseViolationError:
            if not gates:
                gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.KILL))
            final_status = TurnStatus.KILL
            rec = TurnAuditRecord(self.session_id, self.turn_counter, self.agent_id, input_hash, gates, final_status, timestamp)
            rec.seal()
            if self.hooks.herald_fn:
                self.hooks.herald_fn(rec.to_dict(), context)
            raise

        hook_sequence = [
            (1, "P-31", "SCPE_Prune", self.hooks.scpe_fn),
            (2, "P-33", "PDMAL_ConvergenceMonitor", self.hooks.pdmal_fn),
            (3, "N/A", "DemiJoule_SafetyGate", self.hooks.demijoul_fn),
            (4, "P-27", "KAPPA_Router", self.hooks.kappa_fn),
            (5, "P-29", "Sentinel_RiskPass", self.hooks.sentinel_fn),
            (6, "P-32", "PhiClosure_Gate", self.hooks.phi_closure_fn),
        ]

        phi_closure_result = GateResult.SKIP
        for step, pattern, gate_name, hook_fn in hook_sequence:
            rec = self._run_hook(hook_fn, input_text, context, step, pattern, gate_name)
            gates.append(rec)

            if step == 6:
                phi_closure_result = rec.result
                if rec.result == GateResult.KILL:
                    final_status = TurnStatus.KILL_REC
                    break

            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL
                break

        if final_status == TurnStatus.PASS:
            required_skip_steps = [g.step for g in gates if 1 <= g.step <= 6 and g.result == GateResult.SKIP]
            if required_skip_steps:
                final_status = TurnStatus.ESCALATE

        if not any(g.step == 6 and g.result == GateResult.KILL for g in gates):
            if phi_closure_result == GateResult.PASS:
                rec = self._run_hook(
                    self.hooks.hpg_fn,
                    input_text,
                    context,
                    7,
                    "N/A",
                    "HPG_OctaveGate",
                )
            else:
                rec = GateRecord(7, "N/A", "HPG_OctaveGate", GateResult.SKIP, "Phi-Closure did not PASS")
            gates.append(rec)
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL

        if final_status in {TurnStatus.PASS, TurnStatus.WARN, TurnStatus.ESCALATE}:
            rec = self._run_hook(
                self.hooks.apogee_fn,
                input_text,
                context,
                8,
                "P-30",
                "Apogee_AttestationGate",
            )
            gates.append(rec)
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL

        if final_status == TurnStatus.PASS:
            required_skip_steps = [g.step for g in gates if 1 <= g.step <= 8 and g.result == GateResult.SKIP]
            if required_skip_steps:
                final_status = TurnStatus.ESCALATE

        audit = TurnAuditRecord(
            session_id=self.session_id,
            turn_index=self.turn_counter,
            agent_id=self.agent_id,
            input_hash=input_hash,
            gate_records=gates,
            final_status=final_status,
            timestamp=timestamp,
        )

        # Seal the completed governance gate chain before handing the audit to Herald.
        audit.seal()
        herald_rec = self._run_hook(
            self.hooks.herald_fn,
            input_text,
            {**context, "audit_record": audit.to_dict()},
            9, "P-01", "Herald_FanOut",
        )
        if herald_rec.result == GateResult.KILL:
            final_status = TurnStatus.KILL
            audit.final_status = final_status
            audit.seal()
        gates.append(herald_rec)

        return audit
