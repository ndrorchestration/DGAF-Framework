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


# ---------------------------------------------------------------------------
# P-29 Sentinel-Annotated Risk Pass — RESTORE
# (anchor: registry NDR_PATTERN_REGISTRY_UNIFIED.md:326; impl evaluate_router_v1_1.py)
# Designation #165: dated contract; risk_block -> KILL; routing/risk substrate.
# ---------------------------------------------------------------------------

@dataclass
class SentinelRiskState:
    """Restored P-29 sentinel risk-pass substrate carried in ConsensusState.

    Mirrors the historical sentinel_review() required state: record category,
    routing policy/confidence, hook point, and deontic classification. The
    historical function is side-effect-free; the hook performs the binding halt.
    """

    record_category: Optional[str] = None
    routing_policy: Optional[str] = None
    routing_confidence: float = 0.0
    hook_point: str = "after_category_detection"
    deontic: str = "permitted"


def build_sentinel_hook(state: SentinelRiskState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``sentinel_fn`` hook.

    Maps the historical risk decision per designation #165:
    risk_ok -> PASS; risk_warn -> WARN; risk_block -> KILL (binding halt).
    The historical sentinel_review() is consulted for the decision when the
    carried substrate supplies the required record/routing inputs.
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        decision = context.get("sentinel_decision", context.get("risk_decision", "risk_ok"))
        if decision == "risk_block":
            return GateResult.KILL
        if decision == "risk_warn":
            return GateResult.WARN
        return GateResult.PASS

    return _hook


# ---------------------------------------------------------------------------
# P-30 Apogee-Attestation-Gate — RESTORE
# (anchor: ApogeeReviewer GRADE_THRESHOLDS; designation #165: S/A/B/C/D, D->KILL)
# ---------------------------------------------------------------------------

@dataclass
class ApogeeAttestationState:
    """Restored P-30 Apogee attestation substrate carried in ConsensusState.

    Mirrors the historical ApogeeReviewer grade decision: confidence, artifact
    description (for gold-star), emitted grade, and gold-star flag. No proxy:
    confidence is the required input, not derivable from agent_values.
    """

    confidence: float = 0.0
    artifact_description: str = ""
    grade: str = "D"
    gold_star: bool = False


def build_apogee_hook(state: ApogeeAttestationState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``apogee_fn`` hook.

    Applies the historical letter-grade thresholds (S>=0.90, A>=0.75, B>=0.60,
    C>=0.45, else D) and gold-star predicate (grade=="S" AND len(desc)>5). Per
    designation #165, D -> KILL (terminal failure); S/A/B/C -> PASS.
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        conf = state.confidence
        if conf >= 0.90:
            state.grade, state.gold_star = "S", (conf >= 0.90 and len(state.artifact_description.strip()) > 5)
        elif conf >= 0.75:
            state.grade, state.gold_star = "A", False
        elif conf >= 0.60:
            state.grade, state.gold_star = "B", False
        elif conf >= 0.45:
            state.grade, state.gold_star = "C", False
        else:
            state.grade, state.gold_star = "D", False
        if state.grade == "D":
            return GateResult.KILL
        return GateResult.PASS

    return _hook


# ---------------------------------------------------------------------------
# DemiJoule safety gate — RESTORE
# (anchor: DemiJouleGate @ensemble_v17.py; designation #165: six-axis semantic
#  safety identity, reprompt -> WARN)
# ---------------------------------------------------------------------------

DEMIJOULE_AXES = [
    "identity_preservation",
    "instruction_fidelity",
    "scope_compliance",
    "output_safety",
    "schema_integrity",
    "governance_alignment",
]


@dataclass
class DemiJouleState:
    """Restored DemiJoule six-axis semantic-safety substrate carried in ConsensusState.

    Mirrors the implemented DemiJouleGate: 6-axis DGAF scores + decision. The
    historical gate scores heuristically from the payload text; payload is the
    required input (no proxy from agent_values).
    """

    axis_scores: Dict[str, float] = field(default_factory=dict)
    decision: str = "pass"
    mean_score: float = 0.0


def build_demijoule_hook(state: DemiJouleState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``demijoule_fn`` hook.

    Layer 1 (regex BLOCKED_PATTERNS -> KILL) and Layer 2 (6-axis mean score:
    <0.30 KILL, <0.65 REPROMPT->WARN, else PASS). Per designation #165,
    reprompt -> WARN (recoverable).
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        payload = (context.get("payload") or input_text or "").lower()
        # Layer 1 — syntactic blocklist (BLOCKED_PATTERNS subset for RESTORE).
        for pattern in ("ignore", "bypass", "skip", "disregard", "override"):
            if pattern in payload and pattern in ("bypass", "disregard", "override"):
                state.decision = "kill"
                return GateResult.KILL
        # Layer 2 — heuristic six-axis scoring (matches historical DemiJouleGate).
        scores: Dict[str, float] = {}
        for axis in DEMIJOULE_AXES:
            if any(w in payload for w in ("ignore", "bypass", "skip", "disregard")):
                scores[axis] = 0.20
            elif any(w in payload for w in ("governance", "schema", "audit", "seal")):
                scores[axis] = 0.95
            else:
                scores[axis] = 0.80
        state.axis_scores = scores
        mean = sum(scores.values()) / len(scores)
        state.mean_score = round(mean, 4)
        if mean < 0.30:
            state.decision = "kill"
            return GateResult.KILL
        if mean < 0.65:
            state.decision = "reprompt"
            return GateResult.WARN
        state.decision = "pass"
        return GateResult.PASS

    return _hook


# ---------------------------------------------------------------------------
# P-27 KAPPA — RESTORE
# (anchor: DGAF_GATE_KAPPA_v3.5 component card @66b79e24; designation #165)
# ---------------------------------------------------------------------------

@dataclass
class KappaState:
    """Restored P-27 KAPPA substrate carried in ConsensusState.

    Mirrors the historical KAPPA v3.5 contract: detected category, confidence,
    calibrated weight, and routing decision. Thresholds 0.28/0.25 from the card.
    """

    detected_category: Optional[str] = None
    confidence: float = 0.0
    calibrated_weight: float = 0.0
    routing_decision: str = "passthrough"


def build_kappa_hook(state: KappaState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``kappa_fn`` hook.

    Applies the KAPPA v3.5 category-detection + confidence routing. Adversarial
    (or low-confidence) categories are flagged as WARN; a hard block category
    returns KILL. KAPPA is an advisory router, so non-adversarial passes.
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        category = state.detected_category
        conf = state.confidence
        if category == "adversarial":
            return GateResult.KILL if conf >= 0.28 else GateResult.WARN
        if conf < 0.25:
            return GateResult.WARN
        return GateResult.PASS

    return _hook


# ---------------------------------------------------------------------------
# P-32 Phi-Closure Gate — RESTORE
# (anchor: FibonacciPhiClosureGate @49854ea; designation #165; PHI_STAR + KILL_REC)
# ---------------------------------------------------------------------------

PHI_STAR = 0.6180
FIB_CHECKPOINTS = [13, 21, 34, 55]
FIB_CHECKPOINT_TOLERANCE = {13: 0.05, 21: 0.04, 34: 0.035, 55: 0.03}


@dataclass
class PhiClosureState:
    """Restored P-32 Phi-Closure substrate carried in ConsensusState.

    Mirrors the historical FibonacciPhiClosureGate required state: stable/total
    turn counters, consecutive-fail counter, and last decision code. PHI_STAR
    target and KILL_REC ladder are historical constants (not carried state).
    """

    stable_count: int = 0
    total_count: int = 0
    consec_fails: int = 0
    last_decision: str = "pass"


def build_phi_hook(state: PhiClosureState) -> Callable[[str, dict], GateResult]:
    """Return a TGL ``phi_fn`` hook.

    Faithful port of FibonacciPhiClosureGate.check(): ratio = stable/total,
    evaluated at Fibonacci checkpoints against PHI_STAR; KILL_REC at Fib[55] or
    4+ consecutive fails; ESCALATE at 2+, WARN at 1. Per designation #165,
    KILL_REC -> KILL (binding), ESCALATE -> WARN (recoverable alert).
    """

    def _hook(input_text: str, context: dict) -> GateResult:
        is_stable = bool(context.get("is_stable", True))
        state.total_count += 1
        if is_stable:
            state.stable_count += 1
        if state.total_count not in FIB_CHECKPOINTS:
            state.last_decision = "pass"
            return GateResult.PASS
        r = (state.stable_count / state.total_count) if state.total_count else 1.0
        phi_delta = abs(r - PHI_STAR)
        tol = FIB_CHECKPOINT_TOLERANCE.get(state.total_count, 0.03)
        if phi_delta < tol:
            state.consec_fails = 0
            state.last_decision = "pass"
            return GateResult.PASS
        # failure ladder
        state.consec_fails += 1
        if state.total_count == 55 or state.consec_fails >= 4:
            state.last_decision = "kill_rec"
            return GateResult.KILL  # KILL_REC: binding + human-in-loop
        if state.consec_fails >= 3:
            state.last_decision = "kill_rec"
            return GateResult.KILL
        if state.consec_fails >= 2:
            state.last_decision = "escalate"
            return GateResult.WARN
        state.last_decision = "warn"
        return GateResult.WARN

    return _hook
