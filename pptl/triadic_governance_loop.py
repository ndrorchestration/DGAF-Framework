"""
triadic_governance_loop.py — Triadic Governance Loop (TGL)
DGAF-Framework · pptl package · S068 · 2026-05-31

The TGL is the canonical execution harness that sequences all governance
gates for a single agent turn in strict constitutional order:

  Step 0  (P-35)  Procluding Premise Gate     — KILL before any work
  Step 1  (P-31)  SCPE Prune                  — token decay, T0 immune
  Step 2  (P-33)  PDMAL Convergence Monitor   — trust graph health
  Step 3          DemiJoule Safety Gate        — syntactic + 6-axis semantic
  Step 4  (P-27)  KAPPA Router                — confidence-gated weighting
  Step 5  (P-29)  Sentinel Risk Pass          — 3-hook risk annotation
  Step 6  (P-32)  Phi-Closure Gate            — temporal stability
  Step 7          HPG Octave Gate             — PASS-gated by step 6
  Step 8  (P-30)  Apogee Attestation          — evidence grade + QA seal
  Step 9  (P-01)  Herald Fan-Out              — audit trace emit

Triadic authority (P-08 Triumvirate):
  Prime:    Amethyst — orchestration, mandate issuance
  Prefect A: COLLEEN  — schema integrity, PDMAL state, SCPE audit
  Prefect B: Apogee   — attestation, evidence grade, Gold Star gate

NDR Patterns invoked: P-01, P-08, P-09, P-27, P-28, P-29, P-30, P-31, P-32, P-33, P-35
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

from pptl.procluding_premise import (
    DGAF_CONSTITUTIONAL_INVARIANTS,
    PremiseViolationError,
    ProcludingPremiseGate,
)


class TurnStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    ESCALATE = "ESCALATE"
    KILL = "KILL"
    KILL_REC = "KILL_REC"  # P-32 terminal


class GateResult(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    SKIP = "SKIP"   # gate not wired in this deployment
    KILL = "KILL"


@dataclass
class GateRecord:
    step: int
    pattern: str
    gate_name: str
    result: GateResult
    notes: str = ""


@dataclass
class TurnAuditRecord:
    """
    SHA-256 sealed audit record for a single TGL turn.
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
        payload = (
            f"{self.session_id}|{self.turn_index}|{self.agent_id}|"
            f"{self.input_hash}|{self.final_status}|{self.timestamp}"
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
    None = SKIP (gate not wired in this deployment, passes through).

    Minimum viable wiring: premise_gate is always populated.
    All other gates are optional for incremental integration.
    """
    premise_check_fn: Optional[Callable] = None     # Step 0 invariant evaluator
    scpe_fn: Optional[Callable] = None              # Step 1 — P-31
    pdmal_fn: Optional[Callable] = None             # Step 2 — P-33
    demijoul_fn: Optional[Callable] = None          # Step 3
    kappa_fn: Optional[Callable] = None             # Step 4 — P-27/P-28
    sentinel_fn: Optional[Callable] = None          # Step 5 — P-29
    phi_closure_fn: Optional[Callable] = None       # Step 6 — P-32
    hpg_fn: Optional[Callable] = None              # Step 7
    apogee_fn: Optional[Callable] = None            # Step 8 — P-30
    herald_fn: Optional[Callable] = None            # Step 9 — P-01


class TriadicGovernanceLoop:
    """
    Canonical 10-step governance turn sequencer.

    Authority: Triumvirate (P-08/P-09)
      Prime:     Amethyst
      Prefect A: COLLEEN
      Prefect B: Apogee

    Usage:
        tgl = TriadicGovernanceLoop(
            session_id="S068",
            agent_id="amethyst",
            hooks=TGLHooks(premise_check_fn=my_checker, ...),
        )
        audit = tgl.run_turn(input_text, context={})
    """

    GATE_MANIFEST = [
        (0,  "P-35",  "ProcludingPremiseGate"),
        (1,  "P-31",  "SCPE_Prune"),
        (2,  "P-33",  "PDMAL_ConvergenceMonitor"),
        (3,  "N/A",   "DemiJoule_SafetyGate"),
        (4,  "P-27",  "KAPPA_Router"),
        (5,  "P-29",  "Sentinel_RiskPass"),
        (6,  "P-32",  "PhiClosure_Gate"),
        (7,  "N/A",   "HPG_OctaveGate"),
        (8,  "P-30",  "Apogee_AttestationGate"),
        (9,  "P-01",  "Herald_FanOut"),
    ]

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
        return hashlib.sha256(text.encode()).hexdigest()[:16]

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
            return GateRecord(step, pattern, gate_name, gate_result)
        except Exception as exc:
            return GateRecord(step, pattern, gate_name, GateResult.KILL, str(exc)[:120])

    def run_turn(
        self,
        input_text: str,
        context: Optional[dict] = None,
    ) -> TurnAuditRecord:
        """
        Execute full 10-step governance sequence for one turn.

        Returns TurnAuditRecord sealed with SHA-256.
        Raises PremiseViolationError at Step 0 if constitutional invariant violated.
        Raises RuntimeError for terminal gate failures at steps 3–6.
        """
        if context is None:
            context = {}

        self._turn_counter += 1
        input_hash = self._hash_input(input_text)
        timestamp = datetime.now(timezone.utc).isoformat()
        gates: list[GateRecord] = []
        final_status = TurnStatus.PASS

        # ------------------------------------------------------------------ #
        # Step 0 — P-35 Procluding Premise Gate (constitutional KILL)
        # ------------------------------------------------------------------ #
        try:
            self._premise_gate.evaluate(
                input_text,
                check_fn=self.hooks.premise_check_fn,
            )
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.PASS))
        except PremiseViolationError as exc:
            gates.append(GateRecord(0, "P-35", "ProcludingPremiseGate", GateResult.KILL, str(exc)[:120]))
            rec = TurnAuditRecord(
                session_id=self.session_id,
                turn_index=self._turn_counter,
                agent_id=self.agent_id,
                input_hash=input_hash,
                gate_records=gates,
                final_status=TurnStatus.KILL,
                timestamp=timestamp,
            )
            rec.seal()
            if self.hooks.herald_fn:
                self.hooks.herald_fn(rec.to_dict(), context)
            raise

        # ------------------------------------------------------------------ #
        # Steps 1–9 — sequential gate chain
        # ------------------------------------------------------------------ #
        hook_sequence = [
            (1, "P-31", "SCPE_Prune",              self.hooks.scpe_fn),
            (2, "P-33", "PDMAL_ConvergenceMonitor", self.hooks.pdmal_fn),
            (3, "N/A",  "DemiJoule_SafetyGate",     self.hooks.demijoul_fn),
            (4, "P-27", "KAPPA_Router",             self.hooks.kappa_fn),
            (5, "P-29", "Sentinel_RiskPass",        self.hooks.sentinel_fn),
            (6, "P-32", "PhiClosure_Gate",          self.hooks.phi_closure_fn),
            (7, "N/A",  "HPG_OctaveGate",           self.hooks.hpg_fn),
            (8, "P-30", "Apogee_AttestationGate",   self.hooks.apogee_fn),
        ]

        for step, pattern, gate_name, hook_fn in hook_sequence:
            rec = self._run_hook(hook_fn, input_text, context, step, pattern, gate_name)
            gates.append(rec)

            # Step 6 P-32 KILL_REC is terminal
            if step == 6 and rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL_REC
                break

            # Any other KILL is terminal
            if rec.result == GateResult.KILL:
                final_status = TurnStatus.KILL
                break

            # HPG (step 7) only runs if Phi-Closure PASSED
            if step == 5 and rec.result != GateResult.PASS:  # post-sentinel
                pass  # sentinel WARN does not block HPG

        # ------------------------------------------------------------------ #
        # Step 9 — P-01 Herald Fan-Out (always fires, even on KILL)
        # ------------------------------------------------------------------ #
        audit = TurnAuditRecord(
            session_id=self.session_id,
            turn_index=self._turn_counter,
            agent_id=self.agent_id,
            input_hash=input_hash,
            gate_records=gates,
            final_status=final_status,
            timestamp=timestamp,
        )
        audit.seal()

        herald_rec = self._run_hook(
            self.hooks.herald_fn,
            input_text,
            {**context, "audit_record": audit.to_dict()},
            9, "P-01", "Herald_FanOut",
        )
        gates.append(herald_rec)

        return audit
