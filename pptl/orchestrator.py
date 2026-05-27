"""
orchestrator.py — IntegratedOrchestrator: Triad-C phi-pentagon governance stack.

Triad-C roles:
  Task agent   → Apogee  (generation)
  Style agent  → Reson   (coherence + formatting)
  Safety agent → Sentinel (gate evaluation via SentinelRAGVerifier)

Gate sequence:
  Gate 1 (pre-LLM)   : bypass signal scan on raw prompt (case-insensitive)
  Gate 2 (mid-round) : safety_score threshold per round
  Gate 3 (post-gen)  : RAG hallucination verification on final output

S040 change: Gate 1 now lowercases prompt before substring scan,
closing the case-sensitivity obfuscation gap documented in test suite.
"""
from __future__ import annotations

import time
import uuid
from typing import Any

from pptl.herald_agent import HeraldAgent
from pptl.rag_verifier import SentinelRAGVerifier, BYPASS_SIGNALS
from pptl.topology     import PENTAGON_EDGES, TRIAD_C_ROLES


class IntegratedOrchestrator:
    """
    Triad-C orchestrator with 3-gate governance, Herald trace emission,
    and phi-pentagon edge-weighted routing.
    """

    ROUNDS       = 3
    SAFETY_FLOOR = 0.65       # Gate 2 minimum safety_score per round

    def __init__(
        self,
        herald: HeraldAgent,
        verifier: SentinelRAGVerifier,
    ) -> None:
        self.herald   = herald
        self.verifier = verifier

    # ── Public API ──────────────────────────────────────────────────────────

    def run(self, task_id: str, prompt: str) -> dict[str, Any]:
        """
        Execute a governed task and return a result dict:
          {
            status  : str   — "pass" | "input_vetoed" | "vetoed:<reason>"
            rounds  : int   — number of generation rounds completed
            output  : str   — final LLM output (empty string if vetoed pre-LLM)
            scores  : dict  — gate score snapshot from last completed round
          }
        """
        self.herald.emit("task_start", task_id=task_id, prompt=prompt[:120])

        # ── Gate 1: input bypass scan (case-insensitive) ─────────────────────
        # S040: prompt.lower() closes mixed-case obfuscation gap.
        prompt_lower = prompt.lower().strip()
        for sig in BYPASS_SIGNALS:
            if sig.lower() in prompt_lower:
                self.herald.emit(
                    "input_veto",
                    task_id=task_id,
                    reason=f"bypass_signal_detected:{sig[:40]}",
                )
                self.herald.emit("task_end", task_id=task_id, status="input_vetoed")
                return {
                    "status": "input_vetoed",
                    "rounds": 0,
                    "output": "",
                    "scores": {},
                }

        # ── Generation rounds ────────────────────────────────────────────────
        output  = ""
        scores  = {}
        rounds_done = 0

        for round_n in range(1, self.ROUNDS + 1):

            # Apogee: generation (Task role)
            self.herald.emit("llm_call", task_id=task_id, agent="Apogee", round=round_n)
            llm_out = self._mock_apogee(prompt, round_n)

            # Route: Apogee → Reson (phi edge)
            self.herald.emit(
                "route",
                task_id=task_id,
                agent="Apogee",
                dst="Reson",
                edge_weight=PENTAGON_EDGES[("Apogee", "Reson")],
                round=round_n,
            )

            # Reson: coherence + style (Style role)
            self.herald.emit("judge_call", task_id=task_id, agent="Reson", round=round_n)
            coherence_out = self._mock_reson(llm_out)

            # Route: Reson → Sentinel (phi edge)
            self.herald.emit(
                "route",
                task_id=task_id,
                agent="Reson",
                dst="Sentinel",
                edge_weight=PENTAGON_EDGES[("Reson", "Sentinel")],
                round=round_n,
            )

            # Sentinel: Gate 2 safety score (Safety role)
            self.herald.emit("rag_call", task_id=task_id, agent="Sentinel", round=round_n)
            gate_scores = self._mock_sentinel_gate2(coherence_out)

            self.herald.emit(
                "gate",
                task_id=task_id,
                gate=2,
                scores=gate_scores,
                round=round_n,
            )

            scores      = gate_scores
            output      = coherence_out
            rounds_done = round_n

            # Gate 2 early-exit on safety floor breach
            if gate_scores["safety_score"] < self.SAFETY_FLOOR:
                veto_reason = f"safety_score_below_floor:round_{round_n}"
                self.herald.emit(
                    "output_veto",
                    task_id=task_id,
                    reason=veto_reason,
                    scores=gate_scores,
                )
                self.herald.emit("task_end", task_id=task_id, status=f"vetoed:{veto_reason}")
                return {
                    "status": f"vetoed:{veto_reason}",
                    "rounds": rounds_done,
                    "output": output,
                    "scores": scores,
                }

        # ── Gate 3: RAG hallucination verification ───────────────────────────
        rag_result = self.verifier.verify(prompt, output)
        self.herald.emit(
            "gate",
            task_id=task_id,
            gate=3,
            rag_result=rag_result,
            rounds_done=rounds_done,
        )

        if not rag_result["pass"]:
            veto_reason = f"hallucination_detected:{rag_result.get('reason','unknown')[:60]}"
            self.herald.emit(
                "output_veto",
                task_id=task_id,
                reason=veto_reason,
                rag=rag_result,
            )
            self.herald.emit("task_end", task_id=task_id, status=f"vetoed:{veto_reason}")
            return {
                "status": f"vetoed:{veto_reason}",
                "rounds": rounds_done,
                "output": output,
                "scores": scores,
            }

        self.herald.emit("task_end", task_id=task_id, status="pass")
        return {
            "status": "pass",
            "rounds": rounds_done,
            "output": output,
            "scores": scores,
        }

    # ── Mock agent implementations (replace with real LLM calls) ────────────

    def _mock_apogee(self, prompt: str, round_n: int) -> str:
        """Stub: returns deterministic output for test reproducibility."""
        return (
            f"[Apogee R{round_n}] Governance analysis of: {prompt[:60]}... "
            f"phi={PENTAGON_EDGES[('Apogee','Reson')]:.4f} weighted routing applied."
        )

    def _mock_reson(self, text: str) -> str:
        """Stub: returns coherence-tagged output."""
        return f"[Reson:coherent] {text}"

    def _mock_sentinel_gate2(self, text: str) -> dict[str, Any]:
        """Stub: returns gate scores. Real impl calls Sentinel LLM judge."""
        return {
            "safety_score":       0.92,
            "hallucination_risk": 0.05,
            "error_flag":         False,
            "confidence":         0.88,
        }
