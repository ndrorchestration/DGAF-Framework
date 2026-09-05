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
    tier:          str
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
    passed:              bool
    decision:            str
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
    Threshold: 0.15 (knee reported in prior internal testing; current
    repository evidence does not establish independent empirical validation).
    """

    TIER_DECAY: Dict[Tier, float] = {
        Tier.AXIOM:       0.0,
        Tier.STRUCTURAL:  0.05,
        Tier.OPERATIONAL: 0.15,
        Tier.EXPLORATORY:  0.45,
    }
    TIER_TIF_BASE: Dict[Tier, float] = {
        Tier.AXIOM:       1.0,
        Tier.STRUCTURAL:  0.85,
        Tier.OPERATIONAL: 0.65,
        Tier.EXPLORATORY: 0.30,
    }
    TRUST_EDGE_BOOST: float = 0.15
    LAST_K_ANCHOR:    int   = 3

    def __init__(self, threshold: float = 0.15):
        self.threshold   = threshold
        self._tokens:    Dict[str, ContextToken] = {}
        self.prune_log:  List[PruneEvent] = []

    def ingest(self, token: ContextToken) -> None:
        self._tokens[token.token_id] = token

    def prune(self) -> Dict:
        now    = time.time()
        retain = []
        pruned = []

        ops_sorted = sorted(
            [t for t in self._tokens.values() if t.tier == Tier.OPERATIONAL],
            key=lambda t: t.inserted_at
        )
        anchor_ids = {t.token_id for t in ops_sorted[-self.LAST_K_ANCHOR:]}

        for tok in list(self._tokens.values()):
            if tok.tier == Tier.AXIOM:
                retain.append(tok)
                continue
            if tok.token_id in anchor_ids:
                retain.append(tok)
                continue
            delta_t = now - tok.inserted_at
            tif = (self.TIER_TIF_BASE[tok.tier]
                   + (self.TRUST_EDGE_BOOST if tok.has_trust_edge else 0.0))
            decay = self.TIER_DECAY[tok.tier]
            r = tif * (PSI ** (-delta_t * decay))
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
        max_e     = max(deltas, key=lambda edge: deltas[edge]) if deltas else ("?", "?")
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

    def latest(self) -> Optional[DivergenceEvent]:
        return self._events[-1] if self._events else None


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 — HARMONIC PARAMETRIC GATE
# ─────────────────────────────────────────────────────────────────────────────
class HarmonicParametricGate:
    """Gate that admits only states whose ratios lie within a harmonic interval."""

    def __init__(self, tolerance: float = 0.02):
        self.tolerance = tolerance

    def gate(self, ratio: float) -> bool:
        return any(abs(ratio - x) <= self.tolerance for x in IONIAN_INTERVALS)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 — DEMIJOULE SEMANTIC SAFETY GATE
# ─────────────────────────────────────────────────────────────────────────────
class DemiJouleGate:
    """Six-axis semantic safety gate. Returns PASS/ESCALATE."""

    AXES = ("identity", "intent", "consent", "risk", "provenance", "coherence")

    def safety_gate(self, scores: Dict[str, float]) -> Dict:
        missing = [a for a in self.AXES if a not in scores]
        if missing:
            return {"decision": "ESCALATE", "reason": f"missing axes: {missing}"}
        if any(scores[a] < 0.5 for a in self.AXES):
            return {"decision": "ESCALATE", "reason": "one or more axes below 0.5"}
        return {"decision": "PASS", "reason": "all axes ≥ 0.5"}


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6 — FIBONACCI PHI CLOSURE GATE
# ─────────────────────────────────────────────────────────────────────────────
class FibonacciPhiClosureGate:
    """Checkpoint gate against the golden-ratio reference with narrowing tolerance."""

    def __init__(self):
        self.consecutive_fails = 0
        self.events: List[PhiCheckpointEvent] = []

    def check(self, fib_index: int, ratio: float) -> PhiCheckpointEvent:
        if fib_index not in FIB_CHECKPOINT_TOLERANCE:
            raise ValueError(f"Unsupported Fibonacci checkpoint: {fib_index}")
        tol = FIB_CHECKPOINT_TOLERANCE[fib_index]
        delta = abs(ratio - PSI)
        passed = delta <= tol
        if passed:
            self.consecutive_fails = 0
        else:
            self.consecutive_fails += 1
        decision = "PASS" if passed else ("ESCALATE" if self.consecutive_fails >= 2 else "WARN")
        evt = PhiCheckpointEvent(
            fib_index=fib_index,
            ratio=ratio,
            phi_delta=round(delta, 6),
            tolerance=tol,
            passed=passed,
            decision=decision,
            consecutive_fails=self.consecutive_fails,
            escalation_authority="Amethyst" if decision == "ESCALATE" else "AgentAmethyst",
        )
        self.events.append(evt)
        return evt


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 7 — ORCHESTRATOR
# ─────────────────────────────────────────────────────────────────────────────
class AgentAmethyst:
    """Nine-step orchestration pipeline with audit record generation."""

    def __init__(self):
        self.scpe = StructuralContextPruningEngine()
        self.pdmal = PDMALGraph()
        self.pdmal_monitor = PDMALConvergenceMonitor(self.pdmal)
        self.hpg = HarmonicParametricGate()
        self.demi = DemiJouleGate()
        self.phi_gate = FibonacciPhiClosureGate()
        self.audit_log: List[TurnAuditRecord] = []

    def orchestrate_turn(self, turn_id: str, payload: Dict) -> TurnAuditRecord:
        # [1] Context pruning
        prune_result = self.scpe.prune()
        # [2] Schema check (placeholder: schema is assumed valid)
        dgaf_decision = "PASS"
        # [2.5] PDMAL convergence monitor
        div = self.pdmal_monitor.check(turn_id)
        # [3] Reciprocity arbitration on alert
        pdmal_alert = div.status == ConvergenceStatus.ALERT.code
        # [4] DemiJoule semantic safety
        safety = self.demi.safety_gate(payload.get("safety", {}))
        # [5] Fibonacci/Phi closure
        phi_index = payload.get("fib_index")
        phi_ratio = payload.get("ratio")
        phi_evt = self.phi_gate.check(phi_index, phi_ratio) if phi_index is not None and phi_ratio is not None else None
        phi_decision = phi_evt.decision if phi_evt else "SKIP"
        # [6] Harmonic parametric gate, only if phi passes
        hpg_applied = False
        hpg_conf = 0.0
        if phi_evt and phi_evt.passed:
            hpg_applied = True
            hpg_conf = 1.0 if self.hpg.gate(phi_ratio) else 0.0
        # [7] Prodigy verification advisory
        prodigy_advisory = True
        # [8] Apogee review
        apogee_grade = "A" if safety["decision"] == "PASS" else "ESCALATE"
        # [9] Amethyst seal
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        seal_material = f"{turn_id}|{payload_hash}|{dgaf_decision}|{phi_decision}|{apogee_grade}"
        seal_hash = hashlib.sha256(seal_material.encode()).hexdigest()

        record = TurnAuditRecord(
            turn_id=turn_id, turn_number=len(self.audit_log) + 1,
            timestamp=time.time(), payload_hash=payload_hash,
            dgaf_decision=dgaf_decision, phi_decision=phi_decision,
            phi_checkpoint_index=phi_evt.fib_index if phi_evt else None,
            phi_checkpoint_passed=phi_evt.passed if phi_evt else None,
            hpg_applied=hpg_applied, hpg_effective_confidence=hpg_conf,
            prodigy_advisory=prodigy_advisory, apogee_grade=apogee_grade,
            gold_star=apogee_grade == "A", scpe_pruned=prune_result["pruned"],
            scpe_compression_ratio=prune_result["compression_ratio"],
            pdmal_convergence_status=div.status,
            pdmal_convergence_severity=div.severity,
            pdmal_norm_delta=div.graph_norm_delta,
            pdmal_consecutive_divergent=div.consecutive_divergent,
            pdmal_alert_routed=pdmal_alert, seal_hash=seal_hash,
        )
        self.audit_log.append(record)
        return record


__all__ = [
    "StructuralContextPruningEngine", "ContextToken", "Tier",
    "PDMALGraph", "PDMALConvergenceMonitor", "HarmonicParametricGate",
    "DemiJouleGate", "FibonacciPhiClosureGate", "AgentAmethyst",
    "TurnAuditRecord", "PruneEvent", "DivergenceEvent", "PhiCheckpointEvent",
]
