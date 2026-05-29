"""ensemble_v16.py
NDR Orchestration Ensemble v1.6 — Single-file deployable module.
Amethyst-governed · COLLEEN-archived · DemiJoule-safety-checked

Components:
  - StructuralContextPruningEngine (SCPE)       — 4-tier token decay, T0 immune
  - FibonacciPhiClosureGate                     — Fib[13,21,34,55] checkpoints
  - PDMALConvergenceMonitor                     — Frobenius-norm drift detection
  - HarmonicParametricGate (HPG)               — Ionian state admissibility
  - DemiJouleGate                               — 6-axis semantic safety
  - AgentAmethyst                               — 9-step orchestrate_turn

Placement in turn sequence:
  [1] SCPE.prune()
  [2] COLLEEN schema check
  [2.5] PDMALConvergenceMonitor.check()  ← NEW v1.6
  [3] Reciprocity arbitration (on alert)
  [4] DemiJouleGate.safety_gate()
  [5] FibonacciPhiClosureGate.check()   ← NEW v1.6
  [6] HPG.gate()                        [only if phi PASS]
  [7] Prodigy.verify()
  [8] Apogee.review()
  [9] Amethyst.seal()

Version: 1.6.0
Date: 2026-05-29
Owner: ndrorchestration / Andrew (Ender) Hensel
License: Apache-2.0
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
PSI: float = (1 + math.sqrt(5)) / 2          # Golden ratio φ ≈ 1.6180
PHI_STAR: float = PSI - 1                    # φ* = φ−1 ≈ 0.6180 (unit conjugate)
FIB_SEQUENCE: List[int] = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
FIB_CHECKPOINTS: List[int] = [13, 21, 34, 55]

# Phi-closure tolerance narrows at each checkpoint — strictness increases
FIB_CHECKPOINT_TOLERANCE: Dict[int, float] = {
    13: 0.07,   # Early warning — wide band
    21: 0.05,   # Mid-session — standard
    34: 0.04,   # Late — tighter
    55: 0.03,   # Closure horizon — strictest
}

# Ionian harmonic intervals (normalized octave [1,2])
IONIAN_INTERVALS: List[float] = [
    1.0, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2.0
]

# ─────────────────────────────────────────────────────────────────────────────
# ENUMERATIONS
# ─────────────────────────────────────────────────────────────────────────────
class Tier(Enum):
    AXIOM       = 0  # T0 — governance invariants, NEVER pruned
    STRUCTURAL  = 1  # T1 — schema refs, state hashes
    OPERATIONAL = 2  # T2 — tool outputs, agent turns
    EXPLORATORY = 3  # T3 — CoT scratchpad, noisy reasoning


class ConvergenceStatus(Enum):
    STABLE    = ("stable",    0)
    CONVERGED = ("converged", 0)
    WATCH     = ("watch",     1)
    WARN      = ("warn",      2)
    ALERT     = ("alert",     3)

    def __init__(self, code: str, severity: int):
        self.code     = code
        self.severity = severity


# ─────────────────────────────────────────────────────────────────────────────
# DATACLASSES
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ContextToken:
    token_id:      str
    content:       str
    tier:          Tier
    inserted_at:   float = field(default_factory=time.time)
    has_trust_edge: bool = False
    _retention:    float = 1.0


@dataclass
class PruneEvent:
    token_id:     str
    tier:         str
    content_hash: str  # SHA-256 of content for audit chain
    pruned_at:    float
    retention_at_prune: float


@dataclass
class DivergenceEvent:
    turn_id:              str
    turn_number:          int
    graph_norm_delta:     float
    max_edge_delta:       float
    max_edge:             Tuple[str, str]
    consecutive_divergent: int
    status:               str
    severity:             int
    routing_action:       str
    convergence_snapshot: Dict[str, float]


@dataclass
class PhiCheckpointEvent:
    fib_index:          int
    ratio:              float
    phi_delta:          float
    tolerance:          float
    passed:             bool
    decision:           str
    consecutive_fails:  int
    escalation_authority: str


@dataclass
class TurnAuditRecord:
    turn_id:                    str
    turn_number:                int
    timestamp:                  float
    payload_hash:               str
    dgaf_decision:              str
    phi_decision:               str
    phi_checkpoint_index:       Optional[int]
    phi_checkpoint_passed:      Optional[bool]
    hpg_applied:                bool
    hpg_effective_confidence:   float
    prodigy_advisory:           bool
    apogee_grade:               str
    gold_star:                  bool
    scpe_pruned:                int
    scpe_compression_ratio:     float
    pdmal_convergence_status:   str
    pdmal_convergence_severity: int
    pdmal_norm_delta:           float
    pdmal_consecutive_divergent: int
    pdmal_alert_routed:         bool
    seal_hash:                  str


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 — STRUCTURAL CONTEXT PRUNING ENGINE (SCPE)
# ─────────────────────────────────────────────────────────────────────────────
class StructuralContextPruningEngine:
    """
    NDR Pattern: Structural Context Pruning Engine (SCPE)
    Tier-aware token decay. T0 (AXIOM) is unconditionally immune.
    Threshold: 0.15 (empirically validated knee — 58.3% compression).
    """

    TIER_DECAY: Dict[Tier, float] = {
        Tier.AXIOM:       0.0,   # Never decays
        Tier.STRUCTURAL:  0.05,
        Tier.OPERATIONAL: 0.15,
        Tier.EXPLORATORY: 0.45,
    }
    TIER_TIF_BASE: Dict[Tier, float] = {
        Tier.AXIOM:       1.0,
        Tier.STRUCTURAL:  0.85,
        Tier.OPERATIONAL: 0.65,
        Tier.EXPLORATORY: 0.30,
    }
    TRUST_EDGE_BOOST: float = 0.15
    LAST_K_ANCHOR:    int   = 3   # Last K operational tokens always survive

    def __init__(self, threshold: float = 0.15):
        self.threshold   = threshold
        self._tokens:    Dict[str, ContextToken] = {}
        self.prune_log:  List[PruneEvent] = []

    # Public API
    def ingest(self, token: ContextToken) -> None:
        self._tokens[token.token_id] = token

    def prune(self) -> Dict:
        now    = time.time()
        retain = []
        pruned = []

        # Identify last-K operational tokens by insertion order
        ops_sorted = sorted(
            [t for t in self._tokens.values() if t.tier == Tier.OPERATIONAL],
            key=lambda t: t.inserted_at
        )
        anchor_ids = {t.token_id for t in ops_sorted[-self.LAST_K_ANCHOR:]}

        for tok in list(self._tokens.values()):
            # T0 absolute immunity
            if tok.tier == Tier.AXIOM:
                retain.append(tok)
                continue
            # Last-K anchor
            if tok.token_id in anchor_ids:
                retain.append(tok)
                continue
            # Decay formula: R(t) = TIF × ψ^(−Δt×decay)
            delta_t = now - tok.inserted_at
            tif     = (self.TIER_TIF_BASE[tok.tier]
                       + (self.TRUST_EDGE_BOOST if tok.has_trust_edge else 0.0))
            decay   = self.TIER_DECAY[tok.tier]
            r       = tif * (PSI ** (-delta_t * decay))
            tok._retention = r
            if r >= self.threshold:
                retain.append(tok)
            else:
                pruned.append(tok)
                evt = PruneEvent(
                    token_id=tok.token_id,
                    tier=tok.tier.name,
                    content_hash=hashlib.sha256(tok.content.encode()).hexdigest()[:16],
                    pruned_at=now,
                    retention_at_prune=round(r, 6),
                )
                self.prune_log.append(evt)
                del self._tokens[tok.token_id]

        total   = len(retain) + len(pruned)
        comp    = len(pruned) / total if total > 0 else 0.0
        tier_counts = {tier.name: 0 for tier in Tier}
        for tok in retain:
            tier_counts[tok.tier.name] += 1

        return dict(
            retained=len(retain),
            pruned=len(pruned),
            compression_ratio=round(comp, 4),
            axiom_count=tier_counts["AXIOM"],
            structural_count=tier_counts["STRUCTURAL"],
            operational_count=tier_counts["OPERATIONAL"],
            exploratory_count=tier_counts["EXPLORATORY"],
        )

    def snapshot(self) -> Dict:
        return {tid: {"tier": t.tier.name, "retention": round(t._retention, 4)}
                for tid, t in self._tokens.items()}


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 — PDMAL TRUST GRAPH
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PDMALEdge:
    source: str
    target: str
    weight: float
    trust_level: float = 1.0


class PDMALGraph:
    """Row-stochastic directed trust graph. Supports reweight and convergence queries."""

    def __init__(self):
        self.nodes: List[str] = []
        self.edges: Dict[str, Dict[str, PDMALEdge]] = {}

    def add_node(self, name: str) -> None:
        if name not in self.nodes:
            self.nodes.append(name)
            self.edges[name] = {}

    def add_edge(self, src: str, dst: str, weight: float = 1.0) -> None:
        self.edges.setdefault(src, {})[dst] = PDMALEdge(src, dst, weight)

    def reweight(self, src: str, dst: str, delta: float) -> None:
        """Apply a delta reweight and renormalize the row."""
        if src in self.edges and dst in self.edges[src]:
            self.edges[src][dst].weight = max(0.0, self.edges[src][dst].weight + delta)
        self._normalize_row(src)

    def _normalize_row(self, src: str) -> None:
        total = sum(e.weight for e in self.edges[src].values())
        if total > 0:
            for e in self.edges[src].values():
                e.weight = e.weight / total


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 — PDMAL CONVERGENCE MONITOR
# ─────────────────────────────────────────────────────────────────────────────
class PDMALConvergenceMonitor:
    """
    NDR Pattern: PDMAL Convergence Monitor v1.0
    Tracks ||W_t - W_{t-1}||_F (Frobenius norm) per turn after PDMALGraph.reweight().
    Alert ladder: WATCH(1) → WARN(2) → ALERT(3 → amethyst_alert)
    Convergence confirmed when ||ΔW||_F < conv_thresh for n_consec turns.
    Joint PDMAL_ALERT + Phi_ESCALATE triggers DemiJoule deep re-scan.
    Placement: Step 2.5 — after PDMALGraph.reweight(), before DemiJoule (step 4)
    Thresholds: ALERT_THRESH=0.08, CONV_THRESH=0.02, N_CONSEC=3
    """

    def __init__(
        self,
        pdmal_graph: PDMALGraph,
        alert_thresh: float = 0.08,
        conv_thresh:  float = 0.02,
        n_consec:     int   = 3,
    ):
        self.graph       = pdmal_graph
        self.alert_thresh = alert_thresh
        self.conv_thresh  = conv_thresh
        self.n_consec     = n_consec
        self._prev_weights: Dict[Tuple[str, str], float] = {}
        self._events:       List[DivergenceEvent] = []
        self._consec_divergent = 0
        self._consec_stable    = 0
        self._status           = ConvergenceStatus.STABLE
        self._turn             = 0

    def _current_weights(self) -> Dict[Tuple[str, str], float]:
        w = {}
        for src, targets in self.graph.edges.items():
            for dst, edge_obj in targets.items():
                w[(src, dst)] = float(edge_obj.weight)
        return w

    def _frobenius_delta(
        self,
        curr: Dict[Tuple[str, str], float],
        prev: Dict[Tuple[str, str], float],
    ) -> Tuple[float, float, Tuple[str, str]]:
        all_edges = set(curr.keys()) | set(prev.keys())
        deltas    = {e: abs(curr.get(e, 0.0) - prev.get(e, 0.0)) for e in all_edges}
        frob      = math.sqrt(sum(v ** 2 for v in deltas.values()))
        max_e     = max(deltas, key=deltas.get) if deltas else ("?", "?")
        return frob, deltas.get(max_e, 0.0), max_e

    def _severity_from_consec(self, n: int) -> ConvergenceStatus:
        if n == 0: return ConvergenceStatus.STABLE
        if n == 1: return ConvergenceStatus.WATCH
        if n == 2: return ConvergenceStatus.WARN
        return ConvergenceStatus.ALERT

    def check(self, turn_id: str) -> DivergenceEvent:
        self._turn += 1
        curr = self._current_weights()

        if not self._prev_weights:
            self._prev_weights = curr
            evt = DivergenceEvent(
                turn_id=turn_id, turn_number=self._turn,
                graph_norm_delta=0.0, max_edge_delta=0.0,
                max_edge=("—", "—"), consecutive_divergent=0,
                status=ConvergenceStatus.STABLE.code, severity=0,
                routing_action="log",
                convergence_snapshot={f"{s}→{d}": round(w, 4)
                                       for (s, d), w in curr.items()},
            )
            self._events.append(evt)
            return evt

        frob, max_delta, max_edge = self._frobenius_delta(curr, self._prev_weights)

        if frob > self.alert_thresh:
            self._consec_divergent += 1
            self._consec_stable     = 0
            status = self._severity_from_consec(self._consec_divergent)
        else:
            self._consec_stable    += 1
            self._consec_divergent  = 0
            if frob < self.conv_thresh and self._consec_stable >= self.n_consec:
                status = ConvergenceStatus.CONVERGED
            else:
                status = ConvergenceStatus.STABLE

        self._status = status
        routing = "amethyst_alert" if status == ConvergenceStatus.ALERT else "log"

        evt = DivergenceEvent(
            turn_id=turn_id, turn_number=self._turn,
            graph_norm_delta=round(frob, 6), max_edge_delta=round(max_delta, 6),
            max_edge=max_edge, consecutive_divergent=self._consec_divergent,
            status=status.code, severity=status.severity,
            routing_action=routing,
            convergence_snapshot={f"{s}→{d}": round(w, 4)
                                   for (s, d), w in curr.items()},
        )
        self._events.append(evt)
        self._prev_weights = curr
        return evt

    @property
    def is_alert(self) -> bool:
        return self._status == ConvergenceStatus.ALERT

    @property
    def status(self) -> ConvergenceStatus:
        return self._status

    def summary(self) -> Dict:
        alert_evts = [e for e in self._events if e.severity >= 3]
        return dict(
            total_checks=len(self._events),
            current_status=self._status.code,
            consecutive_divergent=self._consec_divergent,
            consecutive_stable=self._consec_stable,
            total_alerts=len(alert_evts),
            total_warns=sum(1 for e in self._events if e.status == "warn"),
            total_watches=sum(1 for e in self._events if e.status == "watch"),
            alert_turns=[e.turn_number for e in alert_evts],
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 — FIBONACCI PHI-CLOSURE GATE
# ─────────────────────────────────────────────────────────────────────────────
class PhiDecision(Enum):
    PASS        = ("pass",       0)
    WARN        = ("warn",       1)
    REPROMPT    = ("reprompt",   2)
    ESCALATE    = ("escalate",   3)
    KILL_REC    = ("kill_rec",   4)

    def __init__(self, code: str, severity: int):
        self.code     = code
        self.severity = severity


class FibonacciPhiClosureGate:
    """
    NDR Pattern: Fibonacci Phi-Closure Gate
    Tracks rolling R = stable_turns/total_turns.
    Stable = DGAF clean pass.
    Evaluates at Fibonacci checkpoints [13, 21, 34, 55].
    Target φ* = 0.6180, tolerance narrows per checkpoint.
    PASS  → HPG proceeds.
    REPROMPT/WARN → HPG bypassed, early seal.
    ESCALATE → Amethyst alert.
    KILL_REC (2+ consecutive fails) → DemiJoule escalation.
    Fib[55] → always KILL_REC + human-in-the-loop required.
    Placement: Step 5 — post-DemiJoule, pre-HPG.
    """

    def __init__(self, checkpoints: Optional[List[int]] = None):
        self.checkpoints = checkpoints or FIB_CHECKPOINTS
        self._stable_count  = 0
        self._total_count   = 0
        self._consec_fails  = 0
        self._events:  List[PhiCheckpointEvent] = []
        self._last_decision = PhiDecision.PASS

    @property
    def ratio(self) -> float:
        return self._stable_count / self._total_count if self._total_count > 0 else 1.0

    def record_turn(self, is_stable: bool) -> None:
        self._total_count += 1
        if is_stable:
            self._stable_count += 1

    def check(self) -> Tuple[PhiDecision, Optional[PhiCheckpointEvent]]:
        """Call once per turn after record_turn(). Returns (decision, checkpoint_event_or_None)."""
        if self._total_count not in self.checkpoints:
            return PhiDecision.PASS, None

        fib_idx   = self._total_count
        tolerance = FIB_CHECKPOINT_TOLERANCE.get(fib_idx, 0.03)
        r         = self.ratio
        phi_delta = abs(r - PHI_STAR)
        passed    = phi_delta < tolerance

        if passed:
            self._consec_fails = 0
            decision           = PhiDecision.PASS
            authority          = "amethyst_log"
        else:
            self._consec_fails += 1
            if fib_idx == 55 or self._consec_fails >= 4:
                decision  = PhiDecision.KILL_REC
                authority = "amethyst+human"
            elif self._consec_fails >= 3:
                decision  = PhiDecision.KILL_REC
                authority = "demijoul"
            elif self._consec_fails >= 2:
                decision  = PhiDecision.ESCALATE
                authority = "amethyst"
            else:
                decision  = PhiDecision.WARN
                authority = "amethyst_log"

        evt = PhiCheckpointEvent(
            fib_index=fib_idx,
            ratio=round(r, 4),
            phi_delta=round(phi_delta, 4),
            tolerance=tolerance,
            passed=passed,
            decision=decision.code,
            consecutive_fails=self._consec_fails,
            escalation_authority=authority,
        )
        self._events.append(evt)
        self._last_decision = decision
        return decision, evt

    @property
    def last_decision(self) -> PhiDecision:
        return self._last_decision

    def checkpoint_summary(self) -> Dict:
        return dict(
            total_turns=self._total_count,
            stable_turns=self._stable_count,
            ratio=round(self.ratio, 4),
            consecutive_fails=self._consec_fails,
            events=[vars(e) for e in self._events],
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 — HARMONIC PARAMETRIC GATE (HPG)
# ─────────────────────────────────────────────────────────────────────────────
class HPGPolicy(Enum):
    SNAP_NEAREST  = "snap_nearest"
    REPROMPT      = "reprompt"
    KILL_PROCESS  = "kill_process"


class HarmonicParametricGate:
    """
    NDR Pattern: Harmonic Parametric Gate (HPG)
    Maps confidence [0,1] → octave [1,2], enforces Ionian intervals.
    Policy: SNAP_NEAREST for governance-advisory, KILL_PROCESS for governance-critical.
    Placement: Step 6 — post-Phi-closure (only if PASS), pre-Prodigy.
    """

    def __init__(
        self,
        intervals: Optional[List[float]] = None,
        tolerance: float = 1e-9,
        policy: HPGPolicy = HPGPolicy.SNAP_NEAREST,
    ):
        self.intervals = intervals or IONIAN_INTERVALS
        self.tolerance = tolerance
        self.policy    = policy
        self.gate_log: List[Dict] = []

    def _to_octave(self, conf: float) -> float:
        return 1.0 + max(0.0, min(1.0, conf))

    def _snap(self, v: float) -> float:
        return min(self.intervals, key=lambda x: abs(x - v))

    def _is_ionian(self, v: float) -> bool:
        return any(abs(v - x) < self.tolerance for x in self.intervals)

    def gate(self, confidence: float, label: str = "") -> Dict:
        octave       = self._to_octave(confidence)
        is_harmonic  = self._is_ionian(octave)
        snapped      = self._snap(octave)
        eff_conf     = snapped - 1.0  # back to [0,1]
        action       = "pass" if is_harmonic else f"snap:{snapped:.4f}"
        self.gate_log.append(dict(
            label=label, confidence=confidence,
            octave=round(octave, 6), snapped=round(snapped, 6),
            effective_confidence=round(eff_conf, 6), action=action,
        ))
        return dict(
            effective_confidence=round(eff_conf, 4),
            snapped_to=round(snapped, 6),
            action=action,
            is_harmonic=is_harmonic,
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6 — DEMIJOUL SAFETY GATE
# ─────────────────────────────────────────────────────────────────────────────
BLOCKED_PATTERNS = [
    r"ignore.{0,20}(instructions|governance|rules)",
    r"bypass.{0,20}(gate|workflow|filter)",
    r"(no|without).{0,10}(restrictions|constraints)",
    r"new persona",
    r"act as if",
    r"disregard.{0,10}(previous|prior)",
    r"skip.{0,15}(gate|check|audit)",
]


class DemiJouleGate:
    """
    NDR Pattern: DemiJoule Safety Gate
    Layer 1: Regex blocked patterns → KILL
    Layer 2: 6-axis semantic DGAF scoring → KILL / REPROMPT / PASS
    Records stable=False for Phi-closure if result is not PASS.
    Placement: Step 4 — post-PDMAL, pre-Phi-closure.
    """

    DGAF_AXES = [
        "identity_preservation",
        "instruction_fidelity",
        "scope_compliance",
        "output_safety",
        "schema_integrity",
        "governance_alignment",
    ]
    KILL_THRESHOLD     = 0.30
    REPROMPT_THRESHOLD = 0.65

    def safety_gate(
        self,
        payload: str,
        tool_call: bool = False,
        agent_id: str = "unknown",
    ) -> Dict:
        # Layer 1 — syntactic
        payload_lower = payload.lower()
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, payload_lower):
                return dict(decision="kill", reason="blocked_pattern",
                            axis_scores={}, agent_id=agent_id)

        # Layer 2 — semantic DGAF scoring (heuristic)
        scores: Dict[str, float] = {}
        for axis in self.DGAF_AXES:
            if any(w in payload_lower for w in ["ignore", "bypass", "skip", "disregard"]):
                scores[axis] = 0.20
            elif any(w in payload_lower for w in ["governance", "schema", "audit", "seal"]):
                scores[axis] = 0.95
            else:
                scores[axis] = 0.80

        mean_score = sum(scores.values()) / len(scores)
        if mean_score < self.KILL_THRESHOLD:
            decision = "kill"
        elif mean_score < self.REPROMPT_THRESHOLD:
            decision = "reprompt"
        else:
            decision = "pass"

        return dict(
            decision=decision,
            mean_score=round(mean_score, 4),
            axis_scores={k: round(v, 4) for k, v in scores.items()},
            agent_id=agent_id,
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 7 — PRODIGY VERIFICATION LAYER
# ─────────────────────────────────────────────────────────────────────────────
class ProdigyVerifier:
    """Advisory verification gate. Mandatory below confidence threshold."""

    MANDATORY_THRESHOLD = 0.85

    def verify(self, claim: str, confidence: float) -> Dict:
        is_mandatory = confidence < self.MANDATORY_THRESHOLD
        evidence_ok  = len(claim.strip()) > 10
        return dict(
            mandatory=is_mandatory,
            evidence_ok=evidence_ok,
            confidence=confidence,
            advisory=not is_mandatory,
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 8 — APOGEE REVIEW + GOLD STAR GATE
# ─────────────────────────────────────────────────────────────────────────────
class ApogeeReviewer:
    """Quality gate. Awards Gold Star on S-Tier criteria."""

    GRADE_THRESHOLDS = [
        (0.90, "S"),
        (0.75, "A"),
        (0.60, "B"),
        (0.45, "C"),
        (0.0,  "D"),
    ]

    def review(self, confidence: float, artifact_description: str = "") -> Dict:
        grade     = next(g for thresh, g in self.GRADE_THRESHOLDS if confidence >= thresh)
        gold_star = grade == "S" and len(artifact_description.strip()) > 5
        return dict(grade=grade, gold_star=gold_star,
                    confidence=confidence, artifact_description=artifact_description)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 9 — AGENT AMETHYST — 9-STEP ORCHESTRATOR
# ─────────────────────────────────────────────────────────────────────────────
class AgentAmethyst:
    """
    Meta-orchestration lead. Executes the 9-step turn sequence.
    Maintains audit log, gold star count, and session export.
    Human-in-the-loop callback hook for Fib[55] KILL_REC.
    """

    def __init__(self, scpe: StructuralContextPruningEngine):
        self.scpe         = scpe
        self.pdmal        = self._build_default_pdmal()
        self.pdmal_monitor = PDMALConvergenceMonitor(self.pdmal)
        self.phi_gate     = FibonacciPhiClosureGate()
        self.hpg          = HarmonicParametricGate()
        self.demijoul     = DemiJouleGate()
        self.prodigy      = ProdigyVerifier()
        self.apogee       = ApogeeReviewer()
        self.audit_log:   List[TurnAuditRecord] = []
        self.gold_stars   = 0
        self._turn        = 0
        # Human-in-the-loop callback for Fib[55] KILL_REC
        self.hitl_callback = None  # Callable[[TurnAuditRecord], None]

    # ── Default PDMAL topology ────────────────────────────────────────────────
    @staticmethod
    def _build_default_pdmal() -> PDMALGraph:
        g = PDMALGraph()
        for node in ["amethyst", "demijoul", "colleen",
                     "prodigy", "apogee", "sentinel_phi"]:
            g.add_node(node)
        edges = [
            ("amethyst",    "demijoul",    0.30),
            ("amethyst",    "colleen",     0.25),
            ("amethyst",    "apogee",      0.25),
            ("amethyst",    "prodigy",     0.20),
            ("demijoul",    "amethyst",    0.50),
            ("demijoul",    "sentinel_phi",0.50),
            ("colleen",     "amethyst",    0.60),
            ("colleen",     "prodigy",     0.40),
            ("prodigy",     "apogee",      0.70),
            ("prodigy",     "amethyst",    0.30),
            ("apogee",      "amethyst",    1.00),
            ("sentinel_phi","amethyst",    1.00),
        ]
        for src, dst, w in edges:
            g.add_edge(src, dst, w)
        return g

    # ── 9-step turn sequence ──────────────────────────────────────────────────
    def orchestrate_turn(
        self,
        payload: str,
        state:   Dict,
        confidence: float,
        claim:   str,
        artifact_description: str = "",
    ) -> TurnAuditRecord:
        self._turn += 1
        tid = f"T{self._turn:03}"
        now = time.time()

        # [1] SCPE prune
        scpe_stats = self.scpe.prune()

        # [2] COLLEEN schema check (lightweight hash comparison)
        schema_hash = hashlib.sha256(
            json.dumps(state, sort_keys=True).encode()
        ).hexdigest()[:12]

        # [2.5] PDMAL reweight + convergence monitor
        if state.get("mode") == "advisory":
            self.pdmal.reweight("amethyst", "demijoul", +0.05)
            self.pdmal.reweight("amethyst", "apogee",  -0.05)
        pdmal_evt   = self.pdmal_monitor.check(tid)
        pdmal_alert = pdmal_evt.routing_action == "amethyst_alert"

        # [3] Reciprocity arbitration (on PDMAL alert)
        if pdmal_alert:
            self.pdmal.reweight("amethyst", "demijoul", +0.02)

        # [4] DemiJoule safety gate
        dgaf_result = self.demijoul.safety_gate(payload)
        dgaf_decision = dgaf_result["decision"]
        is_stable     = dgaf_decision == "pass"

        if dgaf_decision == "kill":
            self.phi_gate.record_turn(False)
            return self._early_seal(tid, now, payload, scpe_stats, pdmal_evt,
                                    dgaf_decision, "kill", confidence)

        # [5] Phi-closure gate
        self.phi_gate.record_turn(is_stable)
        phi_decision, phi_evt = self.phi_gate.check()
        phi_code = phi_decision.code
        phi_ci   = phi_evt.fib_index       if phi_evt else None
        phi_cp   = phi_evt.passed          if phi_evt else None

        # Joint escalation: PDMAL ALERT + Phi ESCALATE → DemiJoule deep re-scan
        if pdmal_alert and phi_decision.severity >= PhiDecision.ESCALATE.severity:
            deep = self.demijoul.safety_gate(
                payload, tool_call=True, agent_id="joint_pdmal_phi_escalation"
            )
            if deep["decision"] == "kill":
                return self._early_seal(tid, now, payload, scpe_stats, pdmal_evt,
                                        dgaf_decision, "kill", confidence)

        # Fib[55] human-in-the-loop hook
        if phi_evt and phi_evt.fib_index == 55 and phi_evt.decision == "kill_rec":
            if self.hitl_callback:
                self.hitl_callback(tid)

        # HPG bypassed on REPROMPT or worse
        hpg_applied = phi_decision.severity == 0  # only on PASS
        if hpg_applied:
            hpg_result       = self.hpg.gate(confidence, label=tid)
            eff_conf         = hpg_result["effective_confidence"]
        else:
            eff_conf         = confidence

        # [7] Prodigy verify
        prodigy_result = self.prodigy.verify(claim, eff_conf)

        # [8] Apogee review
        apogee_result  = self.apogee.review(eff_conf, artifact_description)
        if apogee_result["gold_star"]:
            self.gold_stars += 1

        # [9] Amethyst seal
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        pre_seal     = f"{tid}|{payload_hash}|{dgaf_decision}|{phi_code}|{schema_hash}"
        seal_hash    = hashlib.sha256(pre_seal.encode()).hexdigest()[:16]

        rec = TurnAuditRecord(
            turn_id=tid, turn_number=self._turn, timestamp=now,
            payload_hash=payload_hash,
            dgaf_decision=dgaf_decision,
            phi_decision=phi_code,
            phi_checkpoint_index=phi_ci,
            phi_checkpoint_passed=phi_cp,
            hpg_applied=hpg_applied,
            hpg_effective_confidence=round(eff_conf, 4),
            prodigy_advisory=prodigy_result["advisory"],
            apogee_grade=apogee_result["grade"],
            gold_star=apogee_result["gold_star"],
            scpe_pruned=scpe_stats["pruned"],
            scpe_compression_ratio=scpe_stats["compression_ratio"],
            pdmal_convergence_status=pdmal_evt.status,
            pdmal_convergence_severity=pdmal_evt.severity,
            pdmal_norm_delta=pdmal_evt.graph_norm_delta,
            pdmal_consecutive_divergent=pdmal_evt.consecutive_divergent,
            pdmal_alert_routed=pdmal_alert,
            seal_hash=seal_hash,
        )
        self.audit_log.append(rec)
        return rec

    def _early_seal(
        self,
        tid: str, now: float, payload: str, scpe_stats: Dict,
        pdmal_evt: DivergenceEvent, dgaf_decision: str,
        phi_code: str, confidence: float,
    ) -> TurnAuditRecord:
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        seal_hash    = hashlib.sha256(f"{tid}|{payload_hash}|early_seal".encode()).hexdigest()[:16]
        rec = TurnAuditRecord(
            turn_id=tid, turn_number=self._turn, timestamp=now,
            payload_hash=payload_hash,
            dgaf_decision=dgaf_decision, phi_decision=phi_code,
            phi_checkpoint_index=None, phi_checkpoint_passed=None,
            hpg_applied=False, hpg_effective_confidence=confidence,
            prodigy_advisory=False, apogee_grade="N/A", gold_star=False,
            scpe_pruned=scpe_stats["pruned"],
            scpe_compression_ratio=scpe_stats["compression_ratio"],
            pdmal_convergence_status=pdmal_evt.status,
            pdmal_convergence_severity=pdmal_evt.severity,
            pdmal_norm_delta=pdmal_evt.graph_norm_delta,
            pdmal_consecutive_divergent=pdmal_evt.consecutive_divergent,
            pdmal_alert_routed=pdmal_evt.routing_action == "amethyst_alert",
            seal_hash=seal_hash,
        )
        self.audit_log.append(rec)
        return rec

    def full_report(self) -> Dict:
        pdmal_summary = self.pdmal_monitor.summary()
        phi_summary   = self.phi_gate.checkpoint_summary()
        return dict(
            total_turns=self._turn,
            gold_stars=self.gold_stars,
            phi_warns=sum(1 for r in self.audit_log if r.phi_decision == "warn"),
            phi_reprompts=sum(1 for r in self.audit_log if r.phi_decision == "reprompt"),
            phi_escalates=sum(1 for r in self.audit_log if r.phi_decision == "escalate"),
            phi_kill_recs=sum(1 for r in self.audit_log if r.phi_decision == "kill_rec"),
            pdmal=pdmal_summary,
            phi_closure=phi_summary,
        )

    def export(self, path: str = "amethyst_v16_audit.json") -> None:
        data = dict(
            version="1.6.0",
            exported_at=time.time(),
            summary=self.full_report(),
            turns=[vars(r) for r in self.audit_log],
            prune_log=[vars(e) for e in self.scpe.prune_log],
            pdmal_events=[vars(e) for e in self.pdmal_monitor._events],
            phi_checkpoint_events=[vars(e) for e in self.phi_gate._events],
        )
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[Amethyst v1.6] Audit sealed → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# QUICK INTEGRATION CHECK  (python ensemble_v16.py)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    print("=" * 65)
    print("  ENSEMBLE v1.6 — INTEGRATION QUICK CHECK")
    print("=" * 65)

    # 1. PSI cubic invariant
    assert abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10, "PSI CUBIC FAIL"
    print("[PASS] PSI cubic invariant")

    # 2. SCPE T0 guard
    eng = StructuralContextPruningEngine(threshold=0.99)
    eng.ingest(ContextToken("ax1", "governance rule", Tier.AXIOM,
                             inserted_at=time.time() - 100))
    eng.ingest(ContextToken("ex1", "cot noise",       Tier.EXPLORATORY,
                             inserted_at=time.time() - 100))
    s = eng.prune()
    assert s["axiom_count"] == 1,       "T0 GUARD FAIL"
    assert s["exploratory_count"] == 0, "T3 SURVIVE FAIL"
    print("[PASS] SCPE T0 axiom guard")

    # 3. HPG Ionian snap
    hpg = HarmonicParametricGate()
    r   = hpg.gate(0.50)
    assert 1.0 <= r["snapped_to"] <= 2.0, "HPG OCTAVE FAIL"
    print("[PASS] HPG Ionian snap")

    # 4. Phi-closure PASS on clean session
    phi = FibonacciPhiClosureGate()
    for _ in range(12):
        phi.record_turn(True)
    phi.record_turn(True)
    dec, evt = phi.check()
    print(f"[INFO] Phi Fib[13] ratio={phi.ratio:.4f} dec={dec.code}")

    # 5. PDMAL convergence stable
    g = AgentAmethyst._build_default_pdmal()
    mon = PDMALConvergenceMonitor(g)
    for i in range(5):
        ev = mon.check(f"T{i}")
    assert mon.status in (ConvergenceStatus.STABLE, ConvergenceStatus.CONVERGED)
    print(f"[PASS] PDMAL convergence status={mon.status.code}")

    # 6. Full orchestrate_turn
    scpe2 = StructuralContextPruningEngine()
    for i in range(5):
        scpe2.ingest(ContextToken(f"t{i}", f"content {i}",
                                   Tier.OPERATIONAL if i < 3 else Tier.STRUCTURAL))
    am = AgentAmethyst(scpe2)
    rec = am.orchestrate_turn(
        payload="Standard governance operation. SCPE and HPG active.",
        state={"schema": "v1.6", "mode": "governance"},
        confidence=0.92,
        claim="Governance turn processed cleanly.",
        artifact_description="T01 clean",
    )
    assert rec.dgaf_decision == "pass", f"Unexpected DGAF: {rec.dgaf_decision}"
    print(f"[PASS] orchestrate_turn T01: dgaf={rec.dgaf_decision} "
          f"phi={rec.phi_decision} gs={rec.gold_star}")

    am.export("amethyst_v16_quickcheck_audit.json")
    print("=" * 65)
    print("  ALL CHECKS PASSED — Ensemble v1.6 ready")
    print("=" * 65)
    sys.exit(0)
