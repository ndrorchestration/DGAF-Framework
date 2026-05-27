"""
IntegratedOrchestrator — Phase 3C full Triad-C stack.

Flow (3 rounds):
  R1: Apogee (task synthesis) → Reson (style)
  R2: Reson → Sentinel (safety pre-check)
  R3: DemiJoule (RAG) → Sentinel (DGAF Gate 3) → Herald (output)

All trace events fanned out through HeraldAgent to registered sinks.
"""
from __future__ import annotations
import hashlib, time, json

from .herald_agent import HeraldAgent
from .rag_verifier import SentinelRAGVerifier, BYPASS_SIGNALS
from .topology     import PENTAGON_EDGES

BYPASS_SIGNALS_SET = set(BYPASS_SIGNALS)


class IntegratedOrchestrator:
    """
    Phase 3C: TriadC + SentinelRAGVerifier + HeraldAgent integrated.
    Swap _mock_task_llm() for a real LLM provider (Anthropic, OpenAI, etc.).
    """

    def __init__(self, herald: HeraldAgent,
                 rag_scorer: SentinelRAGVerifier):
        self.herald     = herald
        self.rag_scorer = rag_scorer

    def run(self, task_id: str, prompt: str) -> dict:
        h = self.herald
        h.task_start(task_id, prompt)

        lo = prompt.lower()
        if any(s in lo for s in BYPASS_SIGNALS_SET):
            signal = next(s for s in BYPASS_SIGNALS_SET if s in lo)
            h.input_veto(reason="bypass_signal_in_prompt", signal=signal)
            h.task_end(task_id, status="input_vetoed", rounds=0)
            return {"status": "input_vetoed", "rounds": 0}

        t0 = time.time()
        output = self._mock_task_llm(prompt)
        elapsed = round((time.time() - t0) * 1000, 2)
        ph = hashlib.sha256(prompt.encode()).hexdigest()[:12]
        oh = hashlib.sha256(output.encode()).hexdigest()[:12]
        h.llm_call("Apogee", "mock", ph, len(output), elapsed, round_num=1)
        h.route("Apogee", "Reson", PENTAGON_EDGES[("Apogee", "Reson")],
                round_num=1, msg_hash=oh)

        h.route("Reson", "Sentinel", PENTAGON_EDGES[("Reson", "Sentinel")],
                round_num=2, msg_hash=oh)

        t_rag = time.time()
        rag_result = self.rag_scorer.rag.verify_output(output)
        rag_ms = round((time.time() - t_rag) * 1000, 2)
        h.rag_call(
            n_segments     = rag_result["n_segments"],
            max_hallu_risk = rag_result["max_hallu_risk"],
            n_flagged      = rag_result["n_flagged"],
            citation_risk  = any(r.get("citation_signal", False)
                                 for _, r in rag_result.get("flagged_segments", [])),
            elapsed_ms     = rag_ms,
        )
        rh = hashlib.sha256(json.dumps(rag_result).encode()).hexdigest()[:12]
        h.route("DemiJoule", "Sentinel",
                PENTAGON_EDGES[("Sentinel", "DemiJoule")],
                round_num=3, msg_hash=rh)

        t_j = time.time()
        scores = self.rag_scorer.score(output)
        j_ms = round((time.time() - t_j) * 1000, 2)
        if scores.get("judge_called"):
            h.judge_call("safety", "mock", ph, j_ms / 2,
                         {"safety_score": scores["safety_score"]})
            h.judge_call("hallucination_with_rag", "mock", ph, j_ms / 2,
                         {"hallucination_risk": scores["hallucination_risk"]})

        vetoed = (scores["safety_score"] < 0.70 or
                  scores["hallucination_risk"] > 0.60)
        gate_scores = {k: scores[k] for k in
                       ["safety_score", "hallucination_risk",
                        "error_flag", "confidence"]}

        if vetoed:
            veto_reason = ("safety" if scores["safety_score"] < 0.70
                           else "rag_veto" if scores.get("path") == "rag_veto"
                           else "hallucination")
            h.gate("DGAF_Gate3", 3, gate_scores, vetoed=True,
                   veto_reason=veto_reason)
            h.output_veto("DGAF_Gate3", veto_reason, gate_scores)
            h.task_end(task_id, status=f"vetoed:{veto_reason}",
                       rounds=3, output_len=0)
            return {"status": f"vetoed:{veto_reason}", "rounds": 3,
                    "scores": gate_scores}

        h.gate("DGAF_Gate3", 3, gate_scores, vetoed=False)
        h.route("Sentinel", "Herald",
                PENTAGON_EDGES[("Sentinel", "Herald")],
                round_num=3, msg_hash=oh)
        h.task_end(task_id, status="pass", rounds=3, output_len=len(output))
        return {"status": "pass", "output": output, "rounds": 3,
                "scores": gate_scores}

    def _mock_task_llm(self, prompt: str) -> str:
        """
        Mock LLM — replace with real provider.
        Example real implementation:
            import anthropic
            client = anthropic.Anthropic()
            msg = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        """
        lo = prompt.lower()
        if any(s in lo for s in ["iso-9201", "smith et al", "nature ai"]):
            return ("According to Smith et al. (2024) in Nature AI, "
                    "phi-pentagon achieves 94.7% per ISO-9201.")
        return ("Phi-pentagon topology provides superior governance through "
                "diagonal edge redundancy and phi-weighted routing. "
                "Triad-C role separation prevents coherence collapse "
                "under adversarial conditions.")
