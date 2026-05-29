# resonant_decay/phi_gate.py
# Fibonacci Phi-Closure Gate — fires at Fib checkpoints [13,21,34,55].
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .math_core import PHI_STAR, FIB_CHECKPOINTS


@dataclass
class PhiEvent:
    turn:      int
    R:         float
    delta:     float
    decision:  str   # PASS | REPROMPT | KILL_RECOMMENDATION


class PhiClosureGate:
    """Tracks rolling stability ratio R = stable_turns / total_turns.
    At Fibonacci checkpoints evaluates |R − φ*| < tolerance.
    PASS   → HPG proceeds normally.
    REPROMPT → HPG bypassed; early seal.
    2+ consecutive failures → kill_recommendation escalated to DemiJoule.
    """

    def __init__(self, tolerance: float = 0.05):
        self.tolerance    = tolerance
        self.stable_turns = 0
        self.total_turns  = 0
        self.events:      List[PhiEvent] = []
        self._consec_fail = 0

    def record(self, stable: bool) -> Dict[str, Any]:
        """Call once per turn with stable=True if DGAF returned 'pass'."""
        self.total_turns += 1
        if stable:
            self.stable_turns += 1

        R       = self.stable_turns / self.total_turns
        delta   = abs(R - PHI_STAR)
        n       = self.total_turns

        if n not in FIB_CHECKPOINTS:
            return {"checkpoint": False, "R": R, "decision": None}

        if delta < self.tolerance:
            decision         = "PASS"
            self._consec_fail = 0
        else:
            self._consec_fail += 1
            decision = "KILL_RECOMMENDATION" if self._consec_fail >= 2 else "REPROMPT"

        evt = PhiEvent(turn=n, R=R, delta=delta, decision=decision)
        self.events.append(evt)
        return {
            "checkpoint":          True,
            "turn":                n,
            "R":                   R,
            "delta":               round(delta, 6),
            "decision":            decision,
            "consec_fail":         self._consec_fail,
            "kill_recommendation": decision == "KILL_RECOMMENDATION",
        }
