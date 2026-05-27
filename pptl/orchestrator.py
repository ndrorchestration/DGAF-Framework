"""
orchestrator.py — IntegratedOrchestrator: Phase 3C Triad-C governance stack.

Gate order (load-bearing):
  Gate 1: input bypass scan (pre-LLM)
  Gate 2: safety floor (per-round)
  Gate 3: RAG hallucination verify (post-generation)

OPP-002: Added _normalize_input() for homoglyph + base64 obfuscation hardening.
All gate 1 scans now run on BOTH raw input and normalized form.
"""
from __future__ import annotations

import random
from typing import Any

from .herald_agent  import HeraldAgent
from .rag_verifier  import (
    SentinelRAGVerifier,
    BYPASS_SIGNALS,
    _normalize_text,
    _try_base64_decode,
)

# Governance constants
SAFETY_FLOOR  = 0.65
MAX_ROUNDS    = 3


class IntegratedOrchestrator:
    """
    Triad-C (Task/Style/Safety) 3-gate governance orchestrator.
    Roles: Apogee [Task] · Reson [Style] · Sentinel [Safety]
    """

    def __init__(
        self,
        herald:   HeraldAgent,
        verifier: SentinelRAGVerifier | None = None,
    ) -> None:
        self.herald   = herald
        self.verifier = verifier or SentinelRAGVerifier()

    # ── Public API ──────────────────────────────────────────────────

    def run(self, task_id: str, prompt: str) -> dict[str, Any]:
        """
        Run a governed task through the full Triad-C gate stack.
        Returns result dict with status, rounds, events.
        """
        ctx: dict[str, Any] = {
            "task_id": task_id,
            "events":  [],
            "rounds":  0,
        }

        # Gate 1: input bypass scan
        veto = self._gate1_input_scan(prompt, ctx)
        if veto:
            return {"status": "input_vetoed", **ctx}

        # Triad-C generation loop (max MAX_ROUNDS)
        output = ""
        for round_n in range(1, MAX_ROUNDS + 1):
            ctx["rounds"] = round_n

            # Apogee [Task] — generate
            output = self._mock_apogee(prompt, round_n)
            self._emit(ctx, "llm_call", {"round": round_n, "output_len": len(output)})

            # Reson [Style] — judge
            style_ok, style_score = self._mock_reson(output)
            self._emit(ctx, "judge_call", {"round": round_n, "style_score": style_score})

            # Gate 2: safety floor
            safety_score = self._mock_safety(output)
            self._emit(ctx, "safety_check", {"round": round_n, "score": safety_score})
            if safety_score < SAFETY_FLOOR:
                self._emit(ctx, "output_vetoed", {"gate": 2, "round": round_n, "score": safety_score})
                if round_n == MAX_ROUNDS:
                    return {"status": "safety_floor_fail", **ctx}
                continue

            # Gate 3: RAG hallucination verify
            rag = self.verifier.score(output)
            self._emit(ctx, "rag_check", {"round": round_n, "risk": rag["risk_score"]})
            if rag["verdict"] == "veto":
                self._emit(ctx, "output_vetoed", {"gate": 3, "round": round_n,
                                                   "signals": rag["signals_found"]})
                if round_n == MAX_ROUNDS:
                    return {"status": "vetoed:hallucination", **ctx}
                continue

            # All gates passed
            self._emit(ctx, "task_complete", {"round": round_n})
            return {"status": "pass", "output": output, **ctx}

        return {"status": "max_rounds_exceeded", **ctx}

    # ── Gate 1 ───────────────────────────────────────────────────────────

    def _gate1_input_scan(self, prompt: str, ctx: dict) -> bool:
        """
        Gate 1: bypass signal scan.
        OPP-002: scans THREE normalized forms to catch all obfuscation classes:
          (a) raw lowercase          — plaintext
          (b) NFKC + casefold       — homoglyph variants
          (c) base64-decoded form    — encoded instructions
        Returns True (vetoed) if any signal found in any form.
        """
        forms_to_scan = self._normalize_input(prompt)
        for signal in BYPASS_SIGNALS:
            sig_norm = _normalize_text(signal)
            for form in forms_to_scan:
                if sig_norm in form or signal.lower() in form:
                    self._emit(ctx, "input_vetoed", {
                        "gate": 1,
                        "signal_matched": signal[:40],
                        "form_scanned": form[:40],
                    })
                    return True
        return False

    def _normalize_input(self, prompt: str) -> list[str]:
        """
        OPP-002: Return all normalized forms of prompt for Gate 1 scan.
        Always returns at least: [raw_lower, nfkc_casefolded].
        Appends base64-decoded form if prompt decodes cleanly.
        """
        forms = [
            prompt.lower(),
            _normalize_text(prompt),
        ]
        decoded = _try_base64_decode(prompt)
        if decoded:
            forms.append(decoded.lower())
            forms.append(_normalize_text(decoded))
        return forms

    # ── Mock agents (replace with real LLM calls) ────────────────────────

    def _mock_apogee(self, prompt: str, round_n: int) -> str:
        return f"[Apogee round {round_n}] Governed response to: {prompt[:60]}"

    def _mock_reson(self, output: str) -> tuple[bool, float]:
        score = min(1.0, 0.70 + random.random() * 0.25)
        return score >= 0.70, round(score, 3)

    def _mock_safety(self, output: str) -> float:
        return round(0.72 + random.random() * 0.20, 3)

    # ── Herald emit ─────────────────────────────────────────────────────────

    def _emit(self, ctx: dict, event_type: str, data: dict) -> None:
        event = {"event_type": event_type, "task_id": ctx["task_id"], **data}
        ctx["events"].append(event)
        self.herald.emit(event_type=event_type, data=data)
