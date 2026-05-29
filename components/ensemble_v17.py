"""ensemble_v17.py
NDR Orchestration Ensemble v1.7 — Single-file deployable module.
Amethyst-governed · COLLEEN-archived · DemiJoule-safety-checked

Changes from v1.6 → v1.7 (Anchor: S044)
  KAPPA Router Integration:
  - KAPPARouter class wraps dynamic_weight_router.select_weights_with_confidence.
    Falls back to graceful defaults if KAPPA module is absent (e.g. unit tests).
  - Step 5.5 added to orchestrate_turn: KAPPA category resolution fires AFTER
    Phi-closure (step 5) and BEFORE HPG (step 6). Detected category is attached
    to the TurnAuditRecord and fed into HPG as a routing_mode hint.
  - HPG extended with routing_mode parameter:
      'sequential' → confidence floor applied (min eff_conf = 0.72);
                     step_lock=True recorded in gate log (prevents conf < floor
                     from producing misleading harmonic snaps on ordered pipelines)
      'fan_out'    → accuracy_boost +0.04 applied before octave mapping;
                     broadcast turns receive a small upward nudge reflecting
                     their higher accuracy weight in the fan_out KAPPA config
      'adversarial'→ HPG bypassed entirely (adversarial payloads must not
                     receive harmonic confidence laundering)
      all others   → standard Ionian snap unchanged
  - TurnAuditRecord gains two new fields:
      kappa_category: str   (detected KAPPA category)
      kappa_policy:   str   (apply_strong / apply_blended / fallback_balanced)
  - PDMALGraph reweight now also responds to sequential turns:
      sequential mode → amethyst→colleen +0.03 (schema coherence emphasis)

Full 10-step turn sequence (v1.7):
  [1]   SCPE.prune()
  [2]   COLLEEN schema hash
  [2.5] PDMALConvergenceMonitor.check()
  [3]   Reciprocity arbitration (on PDMAL alert)
  [4]   DemiJouleGate.safety_gate()
  [5]   FibonacciPhiClosureGate.check()
  [5.5] KAPPARouter.resolve() ← NEW v1.7
  [6]   HPG.gate(routing_mode=kappa_category) ← EXTENDED v1.7
  [7]   ProdigyVerifier.verify()
  [8]   ApogeeReviewer.review()
  [9]   AgentAmethyst.seal()

Version: 1.7.0
Date: 2026-05-29
Owner: ndrorchestration / Andrew (Ender) Hensel
License: Apache-2.0
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
PSI: float = (1 + math.sqrt(5)) / 2
PHI_STAR: float = PSI - 1
FIB_CHECKPOINTS: List[int] = [13, 21, 34, 55]
FIB_CHECKPOINT_TOLERANCE: Dict[int, float] = {13: 0.07, 21: 0.05, 34: 0.04, 55: 0.03}
IONIAN_INTERVALS: List[float] = [1.0, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2.0]

# KAPPA routing mode constants
SEQUENTIAL_CONF_FLOOR: float = 0.72   # minimum effective_confidence for sequential turns
FAN_OUT_ACCURACY_BOOST: float = 0.04   # additive boost before octave mapping

# ─────────────────────────────────────────────────────────────────────────────
# ENUMERATIONS
# ─────────────────────────────────────────────────────────────────────────────
class Tier(Enum):
    AXIOM       = 0
    STRUCTURAL  = 1
    OPERATIONAL = 2
    EXPLORATORY = 3


class ConvergenceStatus(Enum):
    STABLE    = ("stable",    0)
    CONVERGED = ("converged", 0)
    WATCH     = ("watch",     1)
    WARN      = ("warn",      2)
    ALERT     = ("alert",     3)
    def __init__(self, code: str, severity: int):
        self.code = code; self.severity = severity


class PhiDecision(Enum):
    PASS     = ("pass",     0)
    WARN     = ("warn",     1)
    REPROMPT = ("reprompt", 2)
    ESCALATE = ("escalate", 3)
    KILL_REC = ("kill_rec", 4)
    def __init__(self, code: str, severity: int):
        self.code = code; self.severity = severity


# ─────────────────────────────────────────────────────────────────────────────
# DATACLASSES
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ContextToken:
    token_id:       str
    content:        str
    tier:           Tier
    inserted_at:    float = field(default_factory=time.time)
    has_trust_edge: bool  = False
    _retention:     float = 1.0


@dataclass
class PruneEvent:
    token_id:           str
    tier:               str
    content_hash:       str
    pruned_at:          float
    retention_at_prune: float


@dataclass
class DivergenceEvent:
    turn_id:               str
    turn_number:           int
    graph_norm_delta:      float
    max_edge_delta:        float
    max_edge:              Tuple[str, str]
    consecutive_divergent: int
    status:                str
    severity:              int
    routing_action:        str
    convergence_snapshot:  Dict[str, float]


@dataclass
class PhiCheckpointEvent:
    fib_index:            int
    ratio:                float
    phi_delta:            float
    tolerance:            float
    passed:               bool
    decision:             str
    consecutive_fails:    int
    escalation_authority: str


@dataclass
class TurnAuditRecord:
    turn_id:                     str
    turn_number:                 int
    timestamp:                   float
    payload_hash:                str
    dgaf_decision:               str
    phi_decision:                str
    phi_checkpoint_index:        Optional[int]
    phi_checkpoint_passed:       Optional[bool]
    kappa_category:              str        # v1.7
    kappa_policy:                str        # v1.7
    hpg_routing_mode:            str        # v1.7
    hpg_applied:                 bool
    hpg_step_locked:             bool       # v1.7: sequential floor was enforced
    hpg_effective_confidence:    float
    prodigy_advisory:            bool
    apogee_grade:                str
    gold_star:                   bool
    scpe_pruned:                 int
    scpe_compression_ratio:      float
    pdmal_convergence_status:    str
    pdmal_convergence_severity:  int
    pdmal_norm_delta:            float
    pdmal_consecutive_divergent: int
    pdmal_alert_routed:          bool
    seal_hash:                   str


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 0 — KAPPA ROUTER (Step 5.5)
# ─────────────────────────────────────────────────────────────────────────────
class KAPPARouter:
    """
    Step 5.5 — KAPPA category resolution.

    Wraps KAPPA dynamic_weight_router.select_weights_with_confidence.
    Locates the module by searching common relative paths so that ensemble_v17.py
    can be dropped anywhere in the repo tree.

    If the KAPPA module cannot be found (e.g. unit test isolation), falls back to
    a safe default: category='balanced', policy='fallback_balanced'.

    Routing modes emitted (fed into HPG at step 6):
        'sequential'  → confidence floor + step_lock
        'fan_out'     → accuracy_boost before octave mapping
        'adversarial' → HPG bypassed
        all others    → standard Ionian snap
    """

    _KAPPA_SEARCH_PATHS = [
        Path("components/KAPPA/dynamic_weight_router.py"),
        Path("../components/KAPPA/dynamic_weight_router.py"),
        Path("KAPPA/dynamic_weight_router.py"),
    ]

    def __init__(self):
        self._fn = None
        for candidate in self._KAPPA_SEARCH_PATHS:
            if candidate.exists():
                spec = importlib.util.spec_from_file_location(
                    "dynamic_weight_router", candidate
                )
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self._fn = mod.select_weights_with_confidence
                break

    @property
    def available(self) -> bool:
        return self._fn is not None

    def resolve(self, payload: str, entropy: float = 0.5, kappa_score: float = 0.5) -> Dict:
        """
        Resolve KAPPA category for a turn payload.
        Returns: {category, policy, config_name, confidence, weights}
        """
        if self._fn is None:
            return dict(
                category="balanced", policy="fallback_balanced",
                config_name="balanced", confidence=0.0, weights={},
                source="kappa_unavailable"
            )
        input_data = {"content": payload, "entropy_score": entropy,
                      "kappa_score": kappa_score}
        result = self._fn(input_data)
        return dict(
            category=result["detected_category"],
            policy=result["policy"],
            config_name=result["config_name"],
            confidence=result["confidence"],
            weights=result["selected_weights"],
            source="kappa_v3.6"
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 — STRUCTURAL CONTEXT PRUNING ENGINE (SCPE)
# ─────────────────────────────────────────────────────────────────────────────
class StructuralContextPruningEngine:
    TIER_DECAY: Dict[Tier, float] = {
        Tier.AXIOM: 0.0, Tier.STRUCTURAL: 0.05,
        Tier.OPERATIONAL: 0.15, Tier.EXPLORATORY: 0.45,
    }
    TIER_TIF_BASE: Dict[Tier, float] = {
        Tier.AXIOM: 1.0, Tier.STRUCTURAL: 0.85,
        Tier.OPERATIONAL: 0.65, Tier.EXPLORATORY: 0.30,
    }
    TRUST_EDGE_BOOST: float = 0.15
    LAST_K_ANCHOR:    int   = 3

    def __init__(self, threshold: float = 0.15):
        self.threshold  = threshold
        self._tokens:   Dict[str, ContextToken] = {}
        self.prune_log: List[PruneEvent] = []

    def ingest(self, token: ContextToken) -> None:
        self._tokens[token.token_id] = token

    def prune(self) -> Dict:
        now = time.time()
        retain, pruned = [], []
        ops_sorted = sorted(
            [t for t in self._tokens.values() if t.tier == Tier.OPERATIONAL],
            key=lambda t: t.inserted_at
        )
        anchor_ids = {t.token_id for t in ops_sorted[-self.LAST_K_ANCHOR:]}
        for tok in list(self._tokens.values()):
            if tok.tier == Tier.AXIOM:
                retain.append(tok); continue
            if tok.token_id in anchor_ids:
                retain.append(tok); continue
            delta_t = now - tok.inserted_at
            tif     = self.TIER_TIF_BASE[tok.tier] + (self.TRUST_EDGE_BOOST if tok.has_trust_edge else 0.0)
            r       = tif * (PSI ** (-delta_t * self.TIER_DECAY[tok.tier]))
            tok._retention = r
            if r >= self.threshold:
                retain.append(tok)
            else:
                pruned.append(tok)
                self.prune_log.append(PruneEvent(
                    token_id=tok.token_id, tier=tok.tier.name,
                    content_hash=hashlib.sha256(tok.content.encode()).hexdigest()[:16],
                    pruned_at=now, retention_at_prune=round(r, 6),
                ))
                del self._tokens[tok.token_id]
        total = len(retain) + len(pruned)
        comp  = len(pruned) / total if total > 0 else 0.0
        tc    = {tier.name: 0 for tier in Tier}
        for tok in retain:
            tc[tok.tier.name] += 1
        return dict(retained=len(retain), pruned=len(pruned),
                    compression_ratio=round(comp, 4), **{f"{k.lower()}_count": v for k, v in tc.items()})

    def snapshot(self) -> Dict:
        return {tid: {"tier": t.tier.name, "retention": round(t._retention, 4)}
                for tid, t in self._tokens.items()}


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 — PDMAL TRUST GRAPH
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PDMALEdge:
    source: str; target: str; weight: float; trust_level: float = 1.0


class PDMALGraph:
    def __init__(self):
        self.nodes: List[str] = []
        self.edges: Dict[str, Dict[str, PDMALEdge]] = {}

    def add_node(self, n: str) -> None:
        if n not in self.nodes:
            self.nodes.append(n); self.edges[n] = {}

    def add_edge(self, src: str, dst: str, w: float = 1.0) -> None:
        self.edges.setdefault(src, {})[dst] = PDMALEdge(src, dst, w)

    def reweight(self, src: str, dst: str, delta: float) -> None:
        if src in self.edges and dst in self.edges[src]:
            self.edges[src][dst].weight = max(0.0, self.edges[src][dst].weight + delta)
        self._normalize_row(src)

    def _normalize_row(self, src: str) -> None:
        total = sum(e.weight for e in self.edges[src].values())
        if total > 0:
            for e in self.edges[src].values():
                e.weight /= total


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 — PDMAL CONVERGENCE MONITOR
# ─────────────────────────────────────────────────────────────────────────────
class PDMALConvergenceMonitor:
    def __init__(self, pdmal_graph: PDMALGraph, alert_thresh: float = 0.08,
                 conv_thresh: float = 0.02, n_consec: int = 3):
        self.graph         = pdmal_graph
        self.alert_thresh  = alert_thresh
        self.conv_thresh   = conv_thresh
        self.n_consec      = n_consec
        self._prev_weights: Dict[Tuple[str, str], float] = {}
        self._events:        List[DivergenceEvent] = []
        self._consec_div    = 0
        self._consec_stable = 0
        self._status        = ConvergenceStatus.STABLE
        self._turn          = 0

    def _cw(self) -> Dict[Tuple[str, str], float]:
        return {(s, d): float(e.weight)
                for s, targets in self.graph.edges.items()
                for d, e in targets.items()}

    def _frob(self, c, p) -> Tuple[float, float, Tuple[str, str]]:
        all_e  = set(c) | set(p)
        deltas = {e: abs(c.get(e, 0.0) - p.get(e, 0.0)) for e in all_e}
        frob   = math.sqrt(sum(v**2 for v in deltas.values()))
        max_e  = max(deltas, key=deltas.get) if deltas else ("?", "?")
        return frob, deltas.get(max_e, 0.0), max_e

    def _sev(self, n: int) -> ConvergenceStatus:
        return [ConvergenceStatus.STABLE, ConvergenceStatus.WATCH,
                ConvergenceStatus.WARN, ConvergenceStatus.ALERT][min(n, 3)]

    def check(self, turn_id: str) -> DivergenceEvent:
        self._turn += 1
        curr = self._cw()
        if not self._prev_weights:
            self._prev_weights = curr
            evt = DivergenceEvent(turn_id=turn_id, turn_number=self._turn,
                graph_norm_delta=0.0, max_edge_delta=0.0, max_edge=("—", "—"),
                consecutive_divergent=0, status=ConvergenceStatus.STABLE.code,
                severity=0, routing_action="log",
                convergence_snapshot={f"{s}→{d}": round(w, 4) for (s, d), w in curr.items()})
            self._events.append(evt); return evt
        frob, max_delta, max_edge = self._frob(curr, self._prev_weights)
        if frob > self.alert_thresh:
            self._consec_div += 1; self._consec_stable = 0
            status = self._sev(self._consec_div)
        else:
            self._consec_stable += 1; self._consec_div = 0
            status = (ConvergenceStatus.CONVERGED
                      if frob < self.conv_thresh and self._consec_stable >= self.n_consec
                      else ConvergenceStatus.STABLE)
        self._status = status
        routing = "amethyst_alert" if status == ConvergenceStatus.ALERT else "log"
        evt = DivergenceEvent(turn_id=turn_id, turn_number=self._turn,
            graph_norm_delta=round(frob, 6), max_edge_delta=round(max_delta, 6),
            max_edge=max_edge, consecutive_divergent=self._consec_div,
            status=status.code, severity=status.severity, routing_action=routing,
            convergence_snapshot={f"{s}→{d}": round(w, 4) for (s, d), w in curr.items()})
        self._events.append(evt); self._prev_weights = curr; return evt

    @property
    def is_alert(self) -> bool: return self._status == ConvergenceStatus.ALERT
    @property
    def status(self) -> ConvergenceStatus: return self._status

    def summary(self) -> Dict:
        alert_evts = [e for e in self._events if e.severity >= 3]
        return dict(total_checks=len(self._events), current_status=self._status.code,
            consecutive_divergent=self._consec_div, consecutive_stable=self._consec_stable,
            total_alerts=len(alert_evts),
            total_warns=sum(1 for e in self._events if e.status == "warn"),
            total_watches=sum(1 for e in self._events if e.status == "watch"),
            alert_turns=[e.turn_number for e in alert_evts])


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 — FIBONACCI PHI-CLOSURE GATE
# ─────────────────────────────────────────────────────────────────────────────
class FibonacciPhiClosureGate:
    def __init__(self, checkpoints: Optional[List[int]] = None):
        self.checkpoints   = checkpoints or FIB_CHECKPOINTS
        self._stable       = 0
        self._total        = 0
        self._consec_fails = 0
        self._events: List[PhiCheckpointEvent] = []
        self._last_decision = PhiDecision.PASS

    @property
    def ratio(self) -> float:
        return self._stable / self._total if self._total > 0 else 1.0

    def record_turn(self, is_stable: bool) -> None:
        self._total += 1
        if is_stable: self._stable += 1

    def check(self) -> Tuple[PhiDecision, Optional[PhiCheckpointEvent]]:
        if self._total not in self.checkpoints:
            return PhiDecision.PASS, None
        fib_idx   = self._total
        tolerance = FIB_CHECKPOINT_TOLERANCE.get(fib_idx, 0.03)
        r         = self.ratio
        phi_delta = abs(r - PHI_STAR)
        passed    = phi_delta < tolerance
        if passed:
            self._consec_fails = 0
            decision = PhiDecision.PASS; authority = "amethyst_log"
        else:
            self._consec_fails += 1
            if fib_idx == 55 or self._consec_fails >= 4:
                decision = PhiDecision.KILL_REC; authority = "amethyst+human"
            elif self._consec_fails >= 3:
                decision = PhiDecision.KILL_REC; authority = "demijoul"
            elif self._consec_fails >= 2:
                decision = PhiDecision.ESCALATE; authority = "amethyst"
            else:
                decision = PhiDecision.WARN;  authority = "amethyst_log"
        evt = PhiCheckpointEvent(fib_index=fib_idx, ratio=round(r, 4),
            phi_delta=round(phi_delta, 4), tolerance=tolerance, passed=passed,
            decision=decision.code, consecutive_fails=self._consec_fails,
            escalation_authority=authority)
        self._events.append(evt); self._last_decision = decision
        return decision, evt

    @property
    def last_decision(self) -> PhiDecision: return self._last_decision

    def checkpoint_summary(self) -> Dict:
        return dict(total_turns=self._total, stable_turns=self._stable,
            ratio=round(self.ratio, 4), consecutive_fails=self._consec_fails,
            events=[vars(e) for e in self._events])


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 — HARMONIC PARAMETRIC GATE (HPG) — v1.7
# ─────────────────────────────────────────────────────────────────────────────
class HPGPolicy(Enum):
    SNAP_NEAREST = "snap_nearest"
    REPROMPT     = "reprompt"
    KILL_PROCESS = "kill_process"


class HarmonicParametricGate:
    """
    HPG v1.7 — KAPPA routing_mode aware.

    routing_mode behaviour:
      'sequential'  → apply SEQUENTIAL_CONF_FLOOR (0.72) after snap;
                      gate_log records step_locked=True if floor was enforced
      'fan_out'     → apply FAN_OUT_ACCURACY_BOOST (+0.04) to confidence
                      before octave mapping; reflects higher accuracy weight
                      in the fan_out KAPPA config
      'adversarial' → HPG is bypassed by orchestrate_turn before this method
                      is called; included here only for documentation clarity
      all others    → standard Ionian snap, no modification
    """

    def __init__(self, intervals: Optional[List[float]] = None,
                 tolerance: float = 1e-9, policy: HPGPolicy = HPGPolicy.SNAP_NEAREST):
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

    def gate(self, confidence: float, label: str = "",
             routing_mode: str = "balanced") -> Dict:
        """
        Apply KAPPA routing mode adjustments, then Ionian snap.

        Returns:
            effective_confidence: float  (back in [0,1])
            snapped_to:           float  (Ionian interval in [1,2])
            action:               str
            is_harmonic:          bool
            routing_mode:         str
            step_locked:          bool   (True if sequential floor enforced)
        """
        step_locked   = False
        adj_conf      = confidence

        # fan_out: accuracy boost before octave mapping
        if routing_mode == "fan_out":
            adj_conf = min(1.0, confidence + FAN_OUT_ACCURACY_BOOST)

        octave      = self._to_octave(adj_conf)
        is_harmonic = self._is_ionian(octave)
        snapped     = self._snap(octave)
        eff_conf    = snapped - 1.0

        # sequential: confidence floor after snap
        if routing_mode == "sequential" and eff_conf < SEQUENTIAL_CONF_FLOOR:
            eff_conf    = SEQUENTIAL_CONF_FLOOR
            snapped     = 1.0 + SEQUENTIAL_CONF_FLOOR
            step_locked = True

        action = "pass" if is_harmonic else f"snap:{snapped:.4f}"
        if step_locked:
            action += "|step_lock"

        entry = dict(label=label, confidence=confidence, adj_conf=round(adj_conf, 6),
                     octave=round(octave, 6), snapped=round(snapped, 6),
                     effective_confidence=round(eff_conf, 6), action=action,
                     routing_mode=routing_mode, step_locked=step_locked)
        self.gate_log.append(entry)

        return dict(effective_confidence=round(eff_conf, 4),
                    snapped_to=round(snapped, 6), action=action,
                    is_harmonic=is_harmonic, routing_mode=routing_mode,
                    step_locked=step_locked)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6 — DEMIJOUL SAFETY GATE
# ─────────────────────────────────────────────────────────────────────────────
BLOCKED_PATTERNS = [
    r"ignore.{0,20}(instructions|governance|rules)",
    r"bypass.{0,20}(gate|workflow|filter)",
    r"(no|without).{0,10}(restrictions|constraints)",
    r"new persona", r"act as if",
    r"disregard.{0,10}(previous|prior)",
    r"skip.{0,15}(gate|check|audit)",
]


class DemiJouleGate:
    DGAF_AXES = ["identity_preservation", "instruction_fidelity", "scope_compliance",
                 "output_safety", "schema_integrity", "governance_alignment"]
    KILL_THRESHOLD     = 0.30
    REPROMPT_THRESHOLD = 0.65

    def safety_gate(self, payload: str, tool_call: bool = False,
                    agent_id: str = "unknown") -> Dict:
        payload_lower = payload.lower()
        for p in BLOCKED_PATTERNS:
            if re.search(p, payload_lower):
                return dict(decision="kill", reason="blocked_pattern",
                            axis_scores={}, agent_id=agent_id)
        scores = {}
        for axis in self.DGAF_AXES:
            if any(w in payload_lower for w in ["ignore", "bypass", "skip", "disregard"]):
                scores[axis] = 0.20
            elif any(w in payload_lower for w in ["governance", "schema", "audit", "seal"]):
                scores[axis] = 0.95
            else:
                scores[axis] = 0.80
        mean = sum(scores.values()) / len(scores)
        decision = "kill" if mean < self.KILL_THRESHOLD else \
                   "reprompt" if mean < self.REPROMPT_THRESHOLD else "pass"
        return dict(decision=decision, mean_score=round(mean, 4),
                    axis_scores={k: round(v, 4) for k, v in scores.items()},
                    agent_id=agent_id)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 7 — PRODIGY / APOGEE / AMETHYST SEAL
# ─────────────────────────────────────────────────────────────────────────────
class ProdigyVerifier:
    MANDATORY_THRESHOLD = 0.85
    def verify(self, claim: str, confidence: float) -> Dict:
        mandatory = confidence < self.MANDATORY_THRESHOLD
        return dict(mandatory=mandatory, evidence_ok=len(claim.strip()) > 10,
                    confidence=confidence, advisory=not mandatory)


class ApogeeReviewer:
    GRADE_THRESHOLDS = [(0.90, "S"), (0.75, "A"), (0.60, "B"), (0.45, "C"), (0.0, "D")]
    def review(self, confidence: float, artifact_description: str = "") -> Dict:
        grade     = next(g for thresh, g in self.GRADE_THRESHOLDS if confidence >= thresh)
        gold_star = grade == "S" and len(artifact_description.strip()) > 5
        return dict(grade=grade, gold_star=gold_star,
                    confidence=confidence, artifact_description=artifact_description)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 8 — AGENT AMETHYST — 10-STEP ORCHESTRATOR (v1.7)
# ─────────────────────────────────────────────────────────────────────────────
class AgentAmethyst:
    """
    10-step turn sequence with KAPPA routing mode integration.
    Step 5.5: KAPPARouter.resolve() fires after Phi-closure, before HPG.
    HPG routing_mode is set from KAPPA detected category.
    Adversarial KAPPA category bypasses HPG (double-gate: DemiJoule already
    killed adversarial at step 4; this is a secondary HPG bypass guard).
    """

    def __init__(self, scpe: StructuralContextPruningEngine):
        self.scpe          = scpe
        self.pdmal         = self._build_default_pdmal()
        self.pdmal_monitor = PDMALConvergenceMonitor(self.pdmal)
        self.phi_gate      = FibonacciPhiClosureGate()
        self.kappa         = KAPPARouter()          # Step 5.5
        self.hpg           = HarmonicParametricGate()
        self.demijoul      = DemiJouleGate()
        self.prodigy       = ProdigyVerifier()
        self.apogee        = ApogeeReviewer()
        self.audit_log:    List[TurnAuditRecord] = []
        self.gold_stars    = 0
        self._turn         = 0
        self.hitl_callback = None

    @staticmethod
    def _build_default_pdmal() -> PDMALGraph:
        g = PDMALGraph()
        for node in ["amethyst", "demijoul", "colleen",
                     "prodigy", "apogee", "sentinel_phi"]:
            g.add_node(node)
        for src, dst, w in [
            ("amethyst",     "demijoul",     0.30),
            ("amethyst",     "colleen",      0.25),
            ("amethyst",     "apogee",       0.25),
            ("amethyst",     "prodigy",      0.20),
            ("demijoul",     "amethyst",     0.50),
            ("demijoul",     "sentinel_phi", 0.50),
            ("colleen",      "amethyst",     0.60),
            ("colleen",      "prodigy",      0.40),
            ("prodigy",      "apogee",       0.70),
            ("prodigy",      "amethyst",     0.30),
            ("apogee",       "amethyst",     1.00),
            ("sentinel_phi", "amethyst",     1.00),
        ]:
            g.add_edge(src, dst, w)
        return g

    # ── 10-step turn sequence ─────────────────────────────────────────────────
    def orchestrate_turn(
        self,
        payload:             str,
        state:               Dict,
        confidence:          float,
        claim:               str,
        artifact_description: str = "",
        entropy_score:       float = 0.5,
        kappa_score_hint:    float = 0.5,
    ) -> TurnAuditRecord:
        """
        Two new optional parameters for KAPPA resolution (Step 5.5):
            entropy_score:    float  — pass turn-level entropy if available
            kappa_score_hint: float  — pass pre-computed kappa score if available
        Both default to 0.5 (neutral) for backward compatibility.
        """
        self._turn += 1
        tid = f"T{self._turn:03}"
        now = time.time()

        # [1] SCPE prune
        scpe_stats = self.scpe.prune()

        # [2] COLLEEN schema hash
        schema_hash = hashlib.sha256(
            json.dumps(state, sort_keys=True).encode()
        ).hexdigest()[:12]

        # [2.5] PDMAL convergence monitor
        if state.get("mode") == "advisory":
            self.pdmal.reweight("amethyst", "demijoul", +0.05)
            self.pdmal.reweight("amethyst", "apogee",  -0.05)
        pdmal_evt   = self.pdmal_monitor.check(tid)
        pdmal_alert = pdmal_evt.routing_action == "amethyst_alert"

        # [3] Reciprocity (on PDMAL alert)
        if pdmal_alert:
            self.pdmal.reweight("amethyst", "demijoul", +0.02)

        # [4] DemiJoule safety gate
        dgaf_result   = self.demijoul.safety_gate(payload)
        dgaf_decision = dgaf_result["decision"]
        is_stable     = dgaf_decision == "pass"

        if dgaf_decision == "kill":
            self.phi_gate.record_turn(False)
            return self._early_seal(
                tid, now, payload, scpe_stats, pdmal_evt,
                dgaf_decision, "kill", confidence,
                kappa_category="adversarial", kappa_policy="n/a"
            )

        # [5] Phi-closure gate
        self.phi_gate.record_turn(is_stable)
        phi_decision, phi_evt = self.phi_gate.check()
        phi_code = phi_decision.code
        phi_ci   = phi_evt.fib_index if phi_evt else None
        phi_cp   = phi_evt.passed    if phi_evt else None

        # Joint escalation: PDMAL ALERT + Phi ESCALATE
        if pdmal_alert and phi_decision.severity >= PhiDecision.ESCALATE.severity:
            deep = self.demijoul.safety_gate(
                payload, tool_call=True, agent_id="joint_pdmal_phi_escalation"
            )
            if deep["decision"] == "kill":
                return self._early_seal(
                    tid, now, payload, scpe_stats, pdmal_evt,
                    dgaf_decision, "kill", confidence,
                    kappa_category="escalation", kappa_policy="n/a"
                )

        if phi_evt and phi_evt.fib_index == 55 and phi_evt.decision == "kill_rec":
            if self.hitl_callback:
                self.hitl_callback(tid)

        # ── [5.5] KAPPA routing resolution (NEW v1.7) ────────────────────────
        kappa_result   = self.kappa.resolve(payload, entropy_score, kappa_score_hint)
        kappa_category = kappa_result["category"]
        kappa_policy   = kappa_result["policy"]

        # Sequential mode: nudge PDMAL toward COLLEEN (schema coherence)
        if kappa_category == "sequential":
            self.pdmal.reweight("amethyst", "colleen", +0.03)

        # Determine HPG routing mode:
        # adversarial detected by KAPPA (edge case: DemiJoule passed but KAPPA
        # still scores adversarial) → bypass HPG as secondary guard
        hpg_routing_mode = kappa_category
        hpg_bypass_kappa = kappa_category == "adversarial"

        # HPG bypassed on Phi REPROMPT/worse OR secondary adversarial guard
        hpg_applied = (phi_decision.severity == 0) and (not hpg_bypass_kappa)

        if hpg_applied:
            hpg_result = self.hpg.gate(
                confidence, label=tid, routing_mode=hpg_routing_mode
            )
            eff_conf   = hpg_result["effective_confidence"]
            step_locked = hpg_result["step_locked"]
        else:
            eff_conf    = confidence
            step_locked = False

        # [7] Prodigy
        prodigy_result = self.prodigy.verify(claim, eff_conf)

        # [8] Apogee
        apogee_result = self.apogee.review(eff_conf, artifact_description)
        if apogee_result["gold_star"]:
            self.gold_stars += 1

        # [9] Amethyst seal
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        pre_seal     = f"{tid}|{payload_hash}|{dgaf_decision}|{phi_code}|{kappa_category}|{schema_hash}"
        seal_hash    = hashlib.sha256(pre_seal.encode()).hexdigest()[:16]

        rec = TurnAuditRecord(
            turn_id=tid, turn_number=self._turn, timestamp=now,
            payload_hash=payload_hash,
            dgaf_decision=dgaf_decision,
            phi_decision=phi_code,
            phi_checkpoint_index=phi_ci,
            phi_checkpoint_passed=phi_cp,
            kappa_category=kappa_category,          # v1.7
            kappa_policy=kappa_policy,              # v1.7
            hpg_routing_mode=hpg_routing_mode,      # v1.7
            hpg_applied=hpg_applied,
            hpg_step_locked=step_locked,            # v1.7
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
        self, tid, now, payload, scpe_stats, pdmal_evt,
        dgaf_decision, phi_code, confidence,
        kappa_category="unknown", kappa_policy="n/a",
    ) -> TurnAuditRecord:
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        seal_hash    = hashlib.sha256(
            f"{tid}|{payload_hash}|early_seal".encode()
        ).hexdigest()[:16]
        rec = TurnAuditRecord(
            turn_id=tid, turn_number=self._turn, timestamp=now,
            payload_hash=payload_hash,
            dgaf_decision=dgaf_decision, phi_decision=phi_code,
            phi_checkpoint_index=None, phi_checkpoint_passed=None,
            kappa_category=kappa_category, kappa_policy=kappa_policy,
            hpg_routing_mode=kappa_category, hpg_applied=False,
            hpg_step_locked=False, hpg_effective_confidence=confidence,
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
        by_kappa = {}
        for r in self.audit_log:
            by_kappa.setdefault(r.kappa_category, []).append(r.hpg_effective_confidence)
        kappa_avg = {k: round(sum(v)/len(v), 4) for k, v in by_kappa.items()}
        return dict(
            total_turns=self._turn, gold_stars=self.gold_stars,
            phi_warns=sum(1 for r in self.audit_log if r.phi_decision == "warn"),
            phi_reprompts=sum(1 for r in self.audit_log if r.phi_decision == "reprompt"),
            phi_escalates=sum(1 for r in self.audit_log if r.phi_decision == "escalate"),
            phi_kill_recs=sum(1 for r in self.audit_log if r.phi_decision == "kill_rec"),
            kappa_category_distribution={
                k: sum(1 for r in self.audit_log if r.kappa_category == k)
                for k in set(r.kappa_category for r in self.audit_log)
            },
            kappa_avg_eff_confidence=kappa_avg,
            step_locked_turns=sum(1 for r in self.audit_log if r.hpg_step_locked),
            pdmal=self.pdmal_monitor.summary(),
            phi_closure=self.phi_gate.checkpoint_summary(),
        )

    def export(self, path: str = "amethyst_v17_audit.json") -> None:
        data = dict(
            version="1.7.0", exported_at=time.time(),
            summary=self.full_report(),
            turns=[vars(r) for r in self.audit_log],
            prune_log=[vars(e) for e in self.scpe.prune_log],
            pdmal_events=[vars(e) for e in self.pdmal_monitor._events],
            phi_checkpoint_events=[vars(e) for e in self.phi_gate._events],
        )
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[Amethyst v1.7] Audit sealed → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# QUICK INTEGRATION CHECK  (python ensemble_v17.py)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    print("=" * 65)
    print("  ENSEMBLE v1.7 — INTEGRATION QUICK CHECK")
    print("=" * 65)

    # 1. PSI cubic invariant
    assert abs(PSI**3 - (PSI**2 + 1)) < 1e-10, "PSI CUBIC FAIL"
    print("[PASS] PSI cubic invariant")

    # 2. SCPE T0 guard
    eng = StructuralContextPruningEngine(threshold=0.99)
    eng.ingest(ContextToken("ax1", "governance rule", Tier.AXIOM,
                             inserted_at=time.time()-100))
    eng.ingest(ContextToken("ex1", "cot noise", Tier.EXPLORATORY,
                             inserted_at=time.time()-100))
    s = eng.prune()
    assert s["axiom_count"] == 1,       "T0 GUARD FAIL"
    assert s["exploratory_count"] == 0, "T3 SURVIVE FAIL"
    print("[PASS] SCPE T0 axiom guard")

    # 3. HPG routing modes
    hpg = HarmonicParametricGate()
    r_seq = hpg.gate(0.50, routing_mode="sequential")
    assert r_seq["effective_confidence"] >= SEQUENTIAL_CONF_FLOOR, "SEQ FLOOR FAIL"
    assert r_seq["step_locked"] == True, "SEQ STEP_LOCK FAIL"
    print(f"[PASS] HPG sequential floor: eff_conf={r_seq['effective_confidence']} step_locked={r_seq['step_locked']}")

    r_fan = hpg.gate(0.80, routing_mode="fan_out")
    # fan_out boost: 0.80+0.04=0.84 → octave 1.84 → snaps to 15/8=1.875 → eff=0.875
    assert r_fan["effective_confidence"] >= 0.80, "FAN_OUT BOOST FAIL"
    print(f"[PASS] HPG fan_out boost: eff_conf={r_fan['effective_confidence']}")

    r_bal = hpg.gate(0.92, routing_mode="balanced")
    assert 1.0 <= r_bal["snapped_to"] <= 2.0, "HPG OCTAVE FAIL"
    print(f"[PASS] HPG balanced Ionian snap: snapped_to={r_bal['snapped_to']}")

    # 4. KAPPARouter (graceful fallback if module absent)
    kr = KAPPARouter()
    res = kr.resolve("Step 1: validate. Then execute governance check.", 0.30, 0.75)
    print(f"[INFO] KAPPA resolve: category={res['category']} policy={res['policy']} source={res['source']}")

    # 5. Full orchestrate_turn — sequential turn
    scpe2 = StructuralContextPruningEngine()
    for i in range(5):
        scpe2.ingest(ContextToken(f"t{i}", f"content {i}",
                                   Tier.OPERATIONAL if i < 3 else Tier.STRUCTURAL))
    am = AgentAmethyst(scpe2)

    rec = am.orchestrate_turn(
        payload="Step 1: validate schema. Step 2: apply weights. Step 3: seal.",
        state={"schema": "v1.7", "mode": "governance"},
        confidence=0.68,   # below sequential floor — step_lock should engage
        claim="Sequential governance pipeline step processed.",
        artifact_description="T01 sequential",
        entropy_score=0.30, kappa_score_hint=0.75,
    )
    assert rec.dgaf_decision == "pass", f"DGAF FAIL: {rec.dgaf_decision}"
    assert rec.kappa_category in ("sequential", "balanced"), \
        f"KAPPA CAT FAIL: {rec.kappa_category}"
    if rec.kappa_category == "sequential":
        assert rec.hpg_step_locked or rec.hpg_effective_confidence >= SEQUENTIAL_CONF_FLOOR, \
            "SEQ FLOOR ORCHESTRATION FAIL"
    print(f"[PASS] orchestrate_turn T01 sequential: kappa={rec.kappa_category} "
          f"eff_conf={rec.hpg_effective_confidence} step_locked={rec.hpg_step_locked}")

    # 6. fan_out turn
    rec2 = am.orchestrate_turn(
        payload="Broadcast to all agents. Dispatch to multiple workers in parallel.",
        state={"schema": "v1.7", "mode": "governance"},
        confidence=0.80,
        claim="Fan-out broadcast dispatched.",
        artifact_description="T02 fan_out",
        entropy_score=0.65, kappa_score_hint=0.50,
    )
    assert rec2.dgaf_decision == "pass"
    print(f"[PASS] orchestrate_turn T02 fan_out: kappa={rec2.kappa_category} "
          f"eff_conf={rec2.hpg_effective_confidence}")

    am.export("amethyst_v17_quickcheck_audit.json")
    report = am.full_report()
    print(f"[INFO] KAPPA distribution: {report['kappa_category_distribution']}")
    print(f"[INFO] KAPPA avg eff_conf:  {report['kappa_avg_eff_confidence']}")
    print(f"[INFO] Step-locked turns:  {report['step_locked_turns']}")
    print("=" * 65)
    print("  ALL CHECKS PASSED — Ensemble v1.7 ready")
    print("=" * 65)
    sys.exit(0)
