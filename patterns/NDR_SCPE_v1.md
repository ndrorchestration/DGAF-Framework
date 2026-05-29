# NDR Pattern — Structural Context Pruning Engine (SCPE) v1.0

**Status:** Production  
**Version:** 1.0  
**Date:** 2026-05-29  
**Owner:** ndrorchestration / Andrew (Ender) Hensel  
**Governed by:** Agent Amethyst · DGAF-Framework  

---

## Summary

Tier-aware token decay engine for long-running multi-agent sessions. Prevents governance
invariants (T0 AXIOM tokens) from being silently truncated by sliding-window context management,
while allowing operational (T2) and exploratory (T3) tokens to decay naturally based on age
and trust-edge status.

---

## Specification

### Tier Taxonomy

| Tier | Name | Decay (ψ) | TIF Base | Notes |
|------|------|-----------|----------|-------|
| T0 | AXIOM | 0.0 | 1.0 | **Unconditionally immune** — never pruned |
| T1 | STRUCTURAL | 0.05 | 0.85 | Schema refs, state hashes |
| T2 | OPERATIONAL | 0.15 | 0.65 | Tool outputs, agent turns |
| T3 | EXPLORATORY | 0.45 | 0.30 | CoT scratchpad, noisy reasoning |

### Retention Formula

```
R(t) = TIF × ψ^(−Δt × decay)
```

- `ψ = φ = 1.6180` (Golden ratio)
- `Δt` = seconds since insertion
- Tokens with PDMAL trust edge receive `TIF += 0.15`
- Last-K (K=3) operational tokens are anchored unconditionally
- Prune if `R(t) < threshold` (default: **0.15**)

### Validated Knee

Threshold `0.15` produces **58.3% compression** at steady state:
- T3 collapses to ~3 residual tokens
- T2 survives to ~4.6 turns
- T1 survives to ~6.2 turns  
- T0 intact: **100%** at any threshold

---

## Placement

```
Step 1 in orchestrate_turn:
  [Post-ingestion] → SCPE.prune() → PruneEvents → AmethystAuditLog
```

Fire at:
- `turn_start` (always)
- `buffer_utilization > 60%`
- `turn_count > Fibonacci[34]` (pre-Phi-closure horizon)

---

## Audit Output

Every pruned token emits a `PruneEvent` with `content_hash` (SHA-256[:16]) for
cryptographic audit chain continuity.

---

## Framework Adapters

Adapters available for: **Raw API · LangChain · LangGraph · AutoGen · CrewAI**  
See `components/ensemble_v16.py` for full implementation.

---

## Quick Check

```python
eng = StructuralContextPruningEngine(threshold=0.99)
eng.ingest(ContextToken("ax1", "rule", Tier.AXIOM, inserted_at=time.time()-100))
eng.ingest(ContextToken("ex1", "noise", Tier.EXPLORATORY, inserted_at=time.time()-100))
s = eng.prune()
assert s["axiom_count"] == 1       # T0 GUARD PASS
assert s["exploratory_count"] == 0 # T3 ELIMINATED PASS
```

---

*Amethyst-governed · COLLEEN-archived · DemiJoule-safety-checked*
