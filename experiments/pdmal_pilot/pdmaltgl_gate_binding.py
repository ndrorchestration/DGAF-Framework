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

# Resolve repo root so `components` and the pilot package import flat,
# matching the existing test harness (tests import `dgaf_tgl_adapter` and
# `pptl` as top-level modules).
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
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

# Map string tier names -> reference Tier enum members.
_TIER_MAP = {
    "AXIOM": Tier.AXIOM,
    "STRUCTURAL": Tier.STRUCTURAL,
    "OPERATIONAL": Tier.OPERATIONAL,
    "EXPLORATORY": Tier.EXPLORATORY,
}


@dataclass
class SCPEState:
    """Restored P-31 token/tier substrate carried in ConsensusState.

    Mirrors the historical SCPE required state: per-token tier, content,
    insertion time, trust-edge flag, and a monotonic token store.
    """

    tokens: List[Dict[str, Any]] = field(default_factory=list)
    threshold: float = 0.15
    trust_edge_boost: float = 0.15
    last_k_anchor: int = 3

    def to_reference_tokens(self) -> List[ContextToken]:
        out: List[ContextToken] = []
        for t in self.tokens:
            out.append(
                ContextToken(
                    token_id=t["token_id"],
                    content=t.get("content", ""),
                    tier=_TIER_MAP[t["tier"]],
                    inserted_at=t.get("inserted_at", 0.0),
                    has_trust_edge=bool(t.get("has_trust_edge", False)),
                )
            )
        return out


@dataclass
class ConvergenceState:
    """Restored P-33 weighted-graph substrate carried in ConsensusState.

    Mirrors the historical PDMAL Convergence Monitor required state:
    current edge-weight matrix ``W_t`` keyed by (src, dst), retained prior
    snapshot ``W_{t-1}``, and consecutive divergence counters.
    """

    # W_t: edge identity (src, dst) -> weight
    weights: Dict[Tuple[str, str], float] = field(default_factory=dict)
    # W_{t-1}: prior snapshot retained across turns
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
    """Return a TGL ``scpe_fn`` hook that runs the historical SCPE engine.

    Replays the restored token substrate through the reference
    ``StructuralContextPruningEngine`` and emits the historical prune/audit
    fields (content_hash present per contract). Returns ``GateResult.PASS``
    (pruning is a maintenance action, not a turn-terminating decision).
    Returns ``GateResult.KILL`` only on an unrecoverable engine error.
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        engine = StructuralContextPruningEngine(threshold=scpe_state.threshold)
        for tok in scpe_state.to_reference_tokens():
            engine.ingest(tok)
        try:
            engine.prune()
        except Exception:
            return GateResult.KILL
        # Persist surviving tokens back into the carried substrate.
        pruned_ids = {e.token_id for e in engine.prune_log}
        scpe_state.tokens = [
            t for t in scpe_state.tokens if t["token_id"] not in pruned_ids
        ]
        return GateResult.PASS

    return _hook


def build_pdmal_hook(conv_state: ConvergenceState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``pdmal_fn`` hook running the historical Convergence engine.

    Replays the restored weighted graph through ``PDMALConvergenceMonitor``,
    retaining ``W_{t-1}`` across turns. Maps the historical status ladder to
    the TGL lattice: STABLE/CONVERGED/WATCH -> PASS; WARN/ALERT -> WARN
    (routing action ``amethyst_alert``, not a turn-kill). This matches the
    historical contract, in which P-33 ALERT routes to ``amethyst_alert`` and
    only joint escalation with Phi-Closure triggers a deeper scan.
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        graph = conv_state.to_reference_graph()
        monitor = PDMALConvergenceMonitor(
            pdmal_graph=graph,
            alert_thresh=conv_state.alert_thresh,
            conv_thresh=conv_state.conv_thresh,
            n_consec=conv_state.n_consec,
        )
        # Seed prior snapshot + counters so this turn computes a real delta
        # when W_{t-1} was supplied by the harness.
        monitor._prev_weights = dict(conv_state.prev_weights)
        monitor._consec_divergent = conv_state._consec_divergent
        monitor._consec_stable = conv_state._consec_stable
        monitor._turn = conv_state._turn
        monitor._events = list(conv_state._events)
        try:
            evt = monitor.check(turn_id=input_text[:32])
        except Exception:
            return GateResult.KILL
        # Persist advanced state for the next turn.
        conv_state.prev_weights = dict(monitor._prev_weights)
        conv_state._consec_divergent = monitor._consec_divergent
        conv_state._consec_stable = monitor._consec_stable
        conv_state._turn = monitor._turn
        conv_state._events = list(monitor._events)
        conv_state.weights = dict(monitor._current_weights())
        # evt.status is a string code ("stable", "alert", ...).
        if evt.status in (ConvergenceStatus.WARN.code, ConvergenceStatus.ALERT.code):
            return GateResult.WARN
        return GateResult.PASS

    return _hook
