# resonant_decay/engine.py
# StructuralContextPruningEngine — core decay + prune loop.
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .model      import ContextToken, Tier
from .math_core  import resonant_decay, tier_base_weight, tif_multiplier
from .governance import validate_token


@dataclass
class PruneEvent:
    token_id:     str
    tier:         str
    reason:       str
    content_hash: str
    timestamp:    float = field(default_factory=time.time)


class StructuralContextPruningEngine:
    """Topological Resonant Decay Engine.

    threshold: resonance floor — tokens scoring below this are pruned
                (T0 axioms are unconditionally exempt).
    """

    def __init__(self, threshold: float = 0.15):
        self.threshold  = threshold
        self._tokens:   List[ContextToken] = []
        self.prune_log: List[PruneEvent]   = []

    # ── ingestion ──────────────────────────────────────────────────────────
    def ingest(self, token: ContextToken) -> None:
        self._tokens.append(token)

    # ── scoring ────────────────────────────────────────────────────────────
    def _score(self, token: ContextToken, now: float) -> float:
        if token.tier == Tier.AXIOM:
            return float("inf")
        delta_t = max(0.0, now - token.inserted_at)
        base    = tier_base_weight(token.tier)
        decay   = resonant_decay(delta_t)
        tif     = tif_multiplier(token.has_trust_edge)
        return base * decay * tif

    # ── prune ──────────────────────────────────────────────────────────────
    def prune(self) -> Dict[str, Any]:
        now     = time.time()
        before  = len(self._tokens)
        kept: List[ContextToken] = []

        # Unconditional anchors: last 3 T2 tokens
        t2_tokens = [t for t in self._tokens if t.tier == Tier.OPERATIONAL]
        t2_anchor = set(id(t) for t in t2_tokens[-3:])

        for token in self._tokens:
            if not validate_token(token):
                self.prune_log.append(PruneEvent(
                    token.token_id, token.tier.name, "hash_violation", token.content_hash))
                continue
            score = self._score(token, now)
            if score >= self.threshold or id(token) in t2_anchor:
                kept.append(token)
            else:
                self.prune_log.append(PruneEvent(
                    token.token_id, token.tier.name, "below_threshold", token.content_hash))

        self._tokens = kept
        after = len(kept)
        pruned = before - after

        tier_counts = {t.name: 0 for t in Tier}
        for tok in kept:
            tier_counts[tok.tier.name] += 1

        return {
            "retained":           after,
            "pruned":             pruned,
            "compression_ratio":  pruned / max(1, before),
            "axiom_count":        tier_counts["AXIOM"],
            "structural_count":   tier_counts["STRUCTURAL"],
            "operational_count":  tier_counts["OPERATIONAL"],
            "exploratory_count":  tier_counts["EXPLORATORY"],
        }

    # ── snapshot ───────────────────────────────────────────────────────────
    def snapshot(self) -> List[Dict[str, Any]]:
        return [
            {"token_id": t.token_id, "tier": t.tier.name,
             "content": t.content[:80], "locked": t.locked}
            for t in self._tokens
        ]
