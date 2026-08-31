"""RESTORE binding: P-31 SCPE + P-33 Convergence into the PDMAL/TGL pilot.

This module RESTORES the historical P-31 (SCPE) and P-33 (PDMAL Convergence
Monitor) semantics into the current pilot apparatus, integrated cleanly and
proven against the historical reference implementation in
``components/ensemble_v16.py`` (co-located with the v1.0 contracts at
historical commit ``49854ea1e50d9e95e2338b690276635c0cbefb6f``).

Design rules (per operator authorization, RESTORE path):
  * Restore required historical semantic STATE, do not invent a mapping.
  * Reuse the historical engine implementations verbatim as the oracle.
  * Carry state inside ``ConsensusState`` (the adapter is intentionally
    stateless between process-isolated calls).
  * Do NOT change what P-31 / P-33 mean. Preserve modern F1-F3 hardening
    elsewhere.

HONEST SCOPE NOTE: only P-31 and P-33 are wired here. Steps 3,4,5,6,8
(DemiJoule, P-27, P-29, P-32, P-30) remain unwired (None hooks) and still
reduce the turn to ESCALATE -> FAIL_CLOSED. Restoring 2 of 7 required gates
does NOT complete the constitutive treatment and does NOT advance N.
Empirical N remains 0 until the complete constitutive treatment is
executable, verified, frozen, and explicitly authorized.

This module is pre-freeze infrastructure only. It never authorizes pilot
execution, unblinding, or statistical analysis.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from components.ensemble_v16 import (  # noqa: E402
    ConvergenceStatus,
    ContextToken,
    DivergenceEvent,
    PDMALConvergenceMonitor,
    PDMALGraph,
    PruneEvent,
    StructuralContextPruningEngine,
    Tier,
)
from pptl.triadic_governance_loop import GateResult  # noqa: E402

_TIER_MAP = {
    "AXIOM": Tier.AXIOM,
    "STRUCTURAL": Tier.STRUCTURAL,
    "OPERATIONAL": Tier.OPERATIONAL,
    "EXPLORATORY": Tier.EXPLORATORY,
}


@dataclass
class SCPEState:
    """Restored P-31 token/tier substrate carried in ConsensusState."""

    tokens: List[Dict[str, Any]] = field(default_factory=list)
    threshold: float = 0.15
    trust_edge_boost: float = 0.15
    last_k_anchor: int = 3
    # Explicit evaluation anchor closes the hidden wall-clock nondeterminism:
    # candidate/replay callers must provide the instant at which retention is evaluated.
    evaluation_time: Optional[float] = None

    def to_reference_tokens(self) -> List[ContextToken]:
        return [
            ContextToken(
                token_id=t["token_id"],
                content=t.get("content", ""),
                tier=_TIER_MAP[t["tier"]],
                inserted_at=t.get("inserted_at", 0.0),
                has_trust_edge=bool(t.get("has_trust_edge", False)),
            )
            for t in self.tokens
        ]


@dataclass
class ConvergenceState:
    """Restored P-33 weighted-graph substrate carried in ConsensusState."""

    weights: Dict[Tuple[str, str], float] = field(default_factory=dict)
    prev_weights: Dict[Tuple[str, str], float] = field(default_factory=dict)
    alert_thresh: float = 0.08
    conv_thresh: float = 0.02
    n_consec: int = 3
    _consec_divergent: int = 0
    _consec_stable: int = 0
    _turn: int = 0
    _events: List[DivergenceEvent] = field(default_factory=list)

    def to_reference_graph(self) -> PDMALGraph:
        g = PDMALGraph()
        for (src, dst), w in self.weights.items():
            g.add_edge(src, dst, w)
        return g


def build_scpe_hook(scpe_state: SCPEState) -> Callable[[str, dict], GateResult]:
    """Return a TGL hook that executes historical SCPE at an explicit evaluation time."""

    def _hook(input_text: str, context: dict) -> GateResult:
        if scpe_state.tokens and scpe_state.evaluation_time is None:
            raise ValueError("SCPE evaluation_time must be supplied for token-bearing state")
        engine = StructuralContextPruningEngine(threshold=scpe_state.threshold)
        for tok in scpe_state.to_reference_tokens():
            engine.ingest(tok)
        try:
            # The historical implementation calls time.time() internally. Patch only
            # the imported module reference for this bounded invocation so replay uses
            # the frozen/evidence-bound evaluation instant rather than host wall clock.
            if scpe_state.evaluation_time is None:
                engine.prune()
            else:
                import components.ensemble_v16 as reference_module
                original_time = reference_module.time.time
                reference_module.time.time = lambda: scpe_state.evaluation_time  # type: ignore[assignment]
                try:
                    engine.prune()
                finally:
                    reference_module.time.time = original_time
        except Exception:
            return GateResult.KILL
        pruned_ids = {e.token_id for e in engine.prune_log}
        scpe_state.tokens = [
            t for t in scpe_state.tokens if t["token_id"] not in pruned_ids
        ]
        return GateResult.PASS

    return _hook


def build_pdmal_hook(conv_state: ConvergenceState) -> Callable[[str, dict], GateResult]:
    """Return a TGL hook running the historical P-33 Convergence monitor."""

    def _hook(input_text: str, context: dict) -> GateResult:
        graph = conv_state.to_reference_graph()
        monitor = PDMALConvergenceMonitor(
            pdmal_graph=graph,
            alert_thresh=conv_state.alert_thresh,
            conv_thresh=conv_state.conv_thresh,
            n_consec=conv_state.n_consec,
        )
        monitor._prev_weights = dict(conv_state.prev_weights)
        monitor._consec_divergent = conv_state._consec_divergent
        monitor._consec_stable = conv_state._consec_stable
        monitor._turn = conv_state._turn
        monitor._events = list(conv_state._events)
        context_state = context.get("pdmaltgl", {}).get("state", {})
        seed_id = context_state.get("seed_id", "?")
        iteration = context_state.get("iteration", monitor._turn + 1)
        turn_id = f"seed:{seed_id}:iteration:{iteration}"
        try:
            evt = monitor.check(turn_id=turn_id)
        except Exception:
            return GateResult.KILL
        conv_state.prev_weights = dict(monitor._prev_weights)
        conv_state._consec_divergent = monitor._consec_divergent
        conv_state._consec_stable = monitor._consec_stable
        conv_state._turn = monitor._turn
        conv_state._events = list(monitor._events)
        conv_state.weights = dict(monitor._current_weights())
        if evt.status in (ConvergenceStatus.WARN.code, ConvergenceStatus.ALERT.code):
            return GateResult.WARN
        return GateResult.PASS

    return _hook
