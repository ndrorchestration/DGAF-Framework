"""
Triadic Governance Loop (TGL) — canonical 10-step governance sequencer.
DGAF-Framework · pptl · S068

Authority: Triumvirate (P-08/P-09)
  Prime:     Amethyst
  Prefect A: COLLEEN
  Prefect B: Apogee

The TGL is a deterministic gate sequencer. Each step is independently
hookable; an unset hook is recorded as SKIP and never implicit PASS.
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
    """Audit record for one TGL turn; sealed after the complete recorded chain exists."""
    session_id: str
    turn_index: int
    agent_id: str
    input_hash: str
    gate_records: list[GateRecord]
    final_status: TurnStatus
    timestamp: str
    seal_hash: str = field(default="", init=False)

    def _canonical_gate_payload(self) -> list[dict[str, Any]]:
        return [
            {
                "step": g.step,
                "pattern": g.pattern,
                "gate": g.gate_name,
                "result": g.result.value,
                "notes": g.notes,
            }
            for g in self.gate_records
        ]

    def seal(self) -> str:
        """Seal the exact returned audit contents using deterministic canonical JSON."""
        payload = {
            "session_id": self.session_id,
            "turn_index": self.turn_index,
            "agent_id": self.agent_id,
            "input_hash": self.input_hash,
            "final_status": self.final_status.value,
            "timestamp": self.timestamp,
            "gates": self._canonical_gate_payload(),
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.seal_hash = hashlib.sha256(canonical).hexdigest()
        return self.seal_hash

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "TGL_TURN_AUDIT",
            "session_id": self.session_id,
            "turn_index": self.turn_index,
            "agent_id": self.agent_id,
            "input_hash": self.input_hash,
            "final_status": self.final_status.value,
            "timestamp": self.timestamp,
            "seal_hash": self.seal_hash,
            "gates": self._canonical_gate_payload(),
        }


@dataclass
class TGLHooks:
    """Hook functions for TGL steps; None means the gate is not wired."""
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
    REQUIRED_GATE_STEPS = frozenset({1, 2, 3, 4, 5, 6, 7, 8})

    def __init__(self, session_id: str, agent_id: str, hooks: TGLHooks, turn_counter: int = 0) -> None:
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
        context: dict[str, Any],
        step: int,
        pattern: str,
        gate_name: str,
    ) -> GateRecord:
        if hook_fn is None:
            return GateRecord(step, pattern, gate_name, GateResult.SKIP, "Hook not wired")
        try:
            result = hook_fn(input_text, context)
            gate_result = GateResult(result) if isinstance(result, str) else result
            if not isinstance(gate_result, GateResult):
                raise ValueError(f"Invalid gate result: {gate_result!r}")
            return GateRecord(step, pattern, gate_name, gate_result)
        except Exception as exc:
            return GateRecord(step, pattern, gate_name, GateResult.KILL, str(exc)[:120])

    @staticmethod
    def _reduce_status(current: TurnStatus, result: GateResult, *, required_skip: bool = False) -> TurnStatus:
        if result == GateResult.KILL:
            return TurnStatus.KILL
        if required_skip:
            if current in {TurnStatus.KILL, TurnStatus.KILL_REC}:
                return current
            return TurnStatus.ESCALATE
        if result == GateResult.WARN:
            if current in {TurnStatus.KILL, TurnStatus.KILL_REC, TurnStatus.ESCALATE}:
                return current
            return TurnStatus.WARN
        return current

    def _seal_and_emit_terminal_premise_failure(
        self,
        input_text: str,
        gates: list[GateRecord],
        input_hash: str,
        timestamp: str,
        context: dict[str, Any],
    ) -> None:
        """Record P-35 terminal state and contain any Herald failure."""
        rec = TurnAuditRecord(
            self.session_id,
            self._turn_counter,
            self.agent_id,
            input_hash,
            gates,
            TurnStatus.KILL,
            timestamp,
        )
        herald_rec = self._run_hook(
            self.hooks.herald_fn,
            input_text,
            {**context, "audit_record": rec.to_dict()},
            9,
            "P-01",
            "Herald_FanOut",
        )
        gates.append(herald_rec)
        rec.seal()

    def run_turn(self, input_text: str, context: Optional[dict[str, Any]] = None) -> TurnAuditRecord:
        """Execute the governed 10-step sequence with fail-closed contract semantics."""
        if context is None:
            context = {}

        self._turn_counter += 1
        input_hash = self._hash_input(input_text)
        timestamp = datetime.now(timezone.utc).isoformat()
        gates: list[GateRecord] = []
        final_status = TurnStatus.PASS

        try:
            self._premise_gate.evaluate(input_text, check_fn=self.hooks.premise_check_fn)
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS))
        except PremiseViolationError:
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.KILL))
            self._seal_and_emit_terminal_premise_failure(input_text, gates, input_hash, timestamp, context)
            raise
        except Exception as exc:
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.KILL, str(exc)[:120]))
            self._seal_and_emit_terminal_premise_failure(input_text, gates, input_hash, timestamp, context)
            raise RuntimeError("P-35 governance failure") from exc

        hook_sequence = [
            (1, "P-31", "SCPE_Prune", self.hooks.scpe_fn),
            (2, "P-33", "PDMAL_ConvergenceMonitor", self.hooks.pdmal_fn),
            (3, "N/A", "DemiJoule_SafetyGate", self.hooks.demijoul_fn),
            (4, "P-27", "KAPPA_Router", self.hooks.kappa_fn),
            (5, "P-29", "Sentinel_RiskPass", self.hooks.sentinel_fn),
            (6, "P-32", "PhiClosure_Gate", self.hooks.phi_closure_fn),
        ]

        phi_closure_result = GateResult.SKIP
        terminal = False
        for step, pattern, gate_name, hook_fn in hook_sequence:
            rec = self._run_hook(hook_fn, input_text, context, step, pattern, gate_name)
            gates.append(rec)
            if step == 6:
                phi_closure_result = rec.result
                if rec.result == GateResult.KILL:
                    final_status = TurnStatus.KILL_REC
                    terminal = True
                    break
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL
                terminal = True
                break
            final_status = self._reduce_status(final_status, rec.result)

        if not terminal:
            if phi_closure_result == GateResult.PASS:
                rec = self._run_hook(self.hooks.hpg_fn, input_text, context, 7, "N/A", "HPG_OctaveGate")
            else:
                rec = GateRecord(7, "N/A", "HPG_OctaveGate", GateResult.SKIP, "Phi-Closure did not PASS")
            gates.append(rec)
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL
                terminal = True
            elif rec.result == GateResult.SKIP and phi_closure_result == GateResult.PASS:
                final_status = self._reduce_status(final_status, rec.result, required_skip=True)
            else:
                final_status = self._reduce_status(final_status, rec.result)

        if not terminal and final_status in {TurnStatus.PASS, TurnStatus.WARN, TurnStatus.ESCALATE}:
            rec = self._run_hook(self.hooks.apogee_fn, input_text, context, 8, "P-30", "Apogee_AttestationGate")
            gates.append(rec)
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL
                terminal = True
            elif rec.result == GateResult.SKIP:
                final_status = self._reduce_status(final_status, rec.result, required_skip=True)
            else:
                final_status = self._reduce_status(final_status, rec.result)

        # Any required gate that is genuinely unwired prevents PASS.
        # Dependency-caused HPG SKIP is handled above and is not itself treated as unwired.
        for gate in gates:
            if gate.step in self.REQUIRED_GATE_STEPS and gate.result == GateResult.SKIP:
                if gate.step == 7 and gate.notes == "Phi-Closure did not PASS":
                    continue
                final_status = self._reduce_status(final_status, GateResult.SKIP, required_skip=True)

        audit = TurnAuditRecord(
            session_id=self.session_id,
            turn_index=self._turn_counter,
            agent_id=self.agent_id,
            input_hash=input_hash,
            gate_records=gates,
            final_status=final_status,
            timestamp=timestamp,
        )

        # Herald receives the complete pre-Herald governance audit. Its own record
        # is appended to the returned chain, then the exact returned object is sealed.
        herald_rec = self._run_hook(
            self.hooks.herald_fn,
            input_text,
            {**context, "audit_record": audit.to_dict()},
            9,
            "P-01",
            "Herald_FanOut",
        )
        gates.append(herald_rec)
        if herald_rec.result == GateResult.KILL:
            audit.final_status = TurnStatus.KILL

        audit.seal()
        return audit
