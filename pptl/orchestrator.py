"""
IntegratedOrchestrator — PPTL Runtime Core
Anchor: S068 | OI-05: TGL wired as canonical turn harness

This is a convenience wrapper around the verified TriadicGovernanceLoop
interface. The experimental adapter contract remains direct TGL.run_turn().
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from .triadic_governance_loop import (
    GateRecord,
    GateResult,
    TGLHooks,
    TriadicGovernanceLoop,
)
from .procluding_premise import PremiseViolationError
from .herald_agent import HeraldAgent

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorConfig:
    """Runtime configuration for IntegratedOrchestrator."""
    session_id: str
    domain: str = "general"  # "credit", "justice", or "general"
    premise_check_fn: Optional[Callable[[str], bool]] = None
    phi_threshold: float = 0.618
    herald_sink_url: Optional[str] = None
    dry_run: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TurnResult:
    """Structured result returned from orchestrate_turn()."""
    session_id: str
    turn_id: str
    domain: str
    tgl_passed: bool
    gate_records: list
    response: Optional[str]
    blocked_reason: Optional[str] = None
    phi_score: Optional[float] = None


class IntegratedOrchestrator:
    """
    Primary convenience entry point for PPTL-governed turns.

    The canonical TGL contract is:
        TriadicGovernanceLoop(session_id, agent_id, hooks).run_turn(input, context)

    This wrapper adapts OrchestratorConfig into that interface without
    introducing a second TGL configuration model.
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self._resolve_premise_check_fn()
        self.herald = HeraldAgent(session_id=config.session_id)
        self.tgl = TriadicGovernanceLoop(
            session_id=config.session_id,
            agent_id="integrated-orchestrator",
            hooks=TGLHooks(
                premise_check_fn=self.config.premise_check_fn,
            ),
        )
        logger.info(
            "IntegratedOrchestrator ready · session=%s domain=%s dry_run=%s",
            config.session_id,
            config.domain,
            config.dry_run,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def orchestrate_turn(self, user_input: str, turn_id: str) -> TurnResult:
        """Execute one governed turn through the current TGL API."""
        context = {
            "turn_id": turn_id,
            "domain": self.config.domain,
            "dry_run": self.config.dry_run,
            **self.config.extra,
        }

        try:
            audit = self.tgl.run_turn(user_input, context=context)
        except PremiseViolationError as exc:
            logger.warning("TGL BLOCKED at premise gate · turn=%s", turn_id)
            return TurnResult(
                session_id=self.config.session_id,
                turn_id=turn_id,
                domain=self.config.domain,
                tgl_passed=False,
                gate_records=[
                    GateRecord(
                        step=0,
                        pattern="P-35",
                        gate_name="ProcludingPremiseGate",
                        result=GateResult.KILL,
                        notes=str(exc)[:120],
                    )
                ],
                response=None,
                blocked_reason=str(exc),
                phi_score=None,
            )

        blocked_reason = None
        for gate in audit.gate_records:
            if gate.result == GateResult.KILL:
                blocked_reason = gate.notes or gate.gate_name
                break

        tgl_passed = audit.final_status.value in {"PASS", "WARN", "ESCALATE"}
        response = (
            self._synthesize_response(user_input, audit)
            if tgl_passed
            else None
        )

        return TurnResult(
            session_id=self.config.session_id,
            turn_id=turn_id,
            domain=self.config.domain,
            tgl_passed=tgl_passed,
            gate_records=audit.gate_records,
            response=response,
            blocked_reason=blocked_reason,
            phi_score=None,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_premise_check_fn(self) -> None:
        """Auto-wire domain-specific premise_check_fn if not explicitly provided."""
        if self.config.premise_check_fn is not None:
            return

        domain = self.config.domain
        if domain == "credit":
            from .corpus.inv03_credit_signals import premise_check_fn_credit

            self.config.premise_check_fn = premise_check_fn_credit
            logger.info("Auto-wired premise_check_fn: credit (INV-03)")
        elif domain == "justice":
            from .corpus.inv03_justice_signals import premise_check_fn_justice

            self.config.premise_check_fn = premise_check_fn_justice
            logger.info("Auto-wired premise_check_fn: justice (INV-03)")
        else:
            self.config.premise_check_fn = lambda _text: False
            logger.info("Domain '%s': premise_check_fn set to pass-through", domain)

    def _synthesize_response(self, user_input: str, tgl_result: Any) -> str:
        """Placeholder synthesis step; production subclasses may override."""
        return f"[Governed response] {user_input}"
