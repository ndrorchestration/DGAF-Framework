"""
IntegratedOrchestrator — PPTL Runtime Core
Anchor: S068 | OI-05: TGL wired as canonical turn harness

Turn execution order (TGL 10-step sequence):
  1.  Intake validation (P-01)
  2.  Procluding premise gate (P-35) — domain premise_check_fn
  3.  Phi-closure gate (HPG)
  4.  Normative constraint check (P-02)
  5.  RAG verification (P-06)
  6.  Attestation gate (P-11)
  7.  Triumvirate mandate check
  8.  Herald audit log emit
  9.  Response synthesis
  10. Phi-convergence closure
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from .triadic_governance_loop import TriadicGovernanceLoop, TGLConfig, TurnContext
from .procluding_premise import ProcludioPremiseGate
from .herald_agent import HeraldAgent

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorConfig:
    """Runtime configuration for IntegratedOrchestrator."""
    session_id: str
    domain: str = "general"                         # "credit", "justice", or "general"
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
    Primary runtime entry point for all PPTL-governed turns.

    The TGL (TriadicGovernanceLoop) is the canonical 10-step harness.
    Every call to orchestrate_turn() runs the full TGL gate sequence
    before any response is synthesized.
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self._resolve_premise_check_fn()

        tgl_config = TGLConfig(
            session_id=config.session_id,
            phi_threshold=config.phi_threshold,
            premise_check_fn=self.config.premise_check_fn,
            herald_sink_url=config.herald_sink_url,
            dry_run=config.dry_run,
        )
        self.tgl = TriadicGovernanceLoop(tgl_config)
        self.herald = HeraldAgent(session_id=config.session_id)
        logger.info(
            "IntegratedOrchestrator ready · session=%s domain=%s dry_run=%s",
            config.session_id, config.domain, config.dry_run,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def orchestrate_turn(self, user_input: str, turn_id: str) -> TurnResult:
        """
        Execute a full governed turn via TGL 10-step sequence.

        Steps 1–10 are delegated to TriadicGovernanceLoop.run().
        Response synthesis only proceeds when TGL gate passes.
        """
        ctx = TurnContext(
            session_id=self.config.session_id,
            turn_id=turn_id,
            user_input=user_input,
            domain=self.config.domain,
        )

        tgl_result = self.tgl.run(ctx)

        if not tgl_result.passed:
            logger.warning(
                "TGL BLOCKED · turn=%s reason=%s",
                turn_id, tgl_result.blocked_at,
            )
            self.herald.emit(
                event="turn_blocked",
                turn_id=turn_id,
                blocked_at=tgl_result.blocked_at,
                gate_records=tgl_result.gate_records,
            )
            return TurnResult(
                session_id=self.config.session_id,
                turn_id=turn_id,
                domain=self.config.domain,
                tgl_passed=False,
                gate_records=tgl_result.gate_records,
                response=None,
                blocked_reason=tgl_result.blocked_at,
                phi_score=tgl_result.phi_score,
            )

        response = self._synthesize_response(user_input, tgl_result)

        self.herald.emit(
            event="turn_complete",
            turn_id=turn_id,
            phi_score=tgl_result.phi_score,
            gate_records=tgl_result.gate_records,
        )

        return TurnResult(
            session_id=self.config.session_id,
            turn_id=turn_id,
            domain=self.config.domain,
            tgl_passed=True,
            gate_records=tgl_result.gate_records,
            response=response,
            phi_score=tgl_result.phi_score,
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
        """
        Placeholder synthesis step.
        In production this delegates to the configured LLM adapter.
        Subclasses override this method.
        """
        return f"[Governed response · phi={tgl_result.phi_score:.3f}] {user_input}"
