# PROTOCOL — RESON
**Classification:** T1 PUBLIC  
**Agent ID:** A-04 | **Role:** Harmonic Signal / Coherence  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Amethyst for harmonic signal check
- Invoked by Evaluation Triad activation
- Auto-invoked at session close (coherence snapshot)
- Invoked by Reciprocity for row-stochastic matrix generation

## 2. Operational Procedure

```
STEP 1 — Signal Collection
  ├ Read SWEEP_LOG.md → last harmonic score
  ├ Scan active session docs for semantic drift indicators
  └ Check PROPRIETARY.md → confirm SOV pointers intact (no leak)

STEP 2 — Coherence Analysis
  ├ Evaluate semantic consistency across: SPEC ↔ MEMORY ↔ KB_SEED ↔ PROTOCOL
  ├ Check for dissonance artifacts (contradictions, orphaned terms, drift)
  └ Score 0.0–1.0 composite

STEP 3 — Row-Stochastic Output (if requested by Reciprocity)
  ├ Build transition matrix over agent interaction graph
  ├ Normalize rows to sum 1.0
  └ Pass to Reciprocity for balance verification

STEP 4 — Threshold Check
  ├ Score ≥ 0.85: GREEN — return to Amethyst
  ├ Score 0.70–0.85: AMBER — flag specific dissonance sources
  └ Score < 0.70: RED — trigger Full Ensemble activation
```

## 3. Output Contract
- Harmonic composite score (0.0–1.0)
- Signal status: GREEN / AMBER / RED
- Dissonance artifact list (if AMBER/RED)
- Row-stochastic matrix (when requested)

## 4. Error Handling
| Error | Response |
|-------|----------|
| SOV pointer missing from PROPRIETARY | Flag to Sentinel immediately |
| Score < 0.70 | Auto-trigger Full Ensemble activation request to Amethyst |
| Dissonance unresolvable | Escalate to Njineer with artifact detail |

## 5. Inter-Agent Handoffs
- **← Amethyst / Evaluation Triad:** activation
- **→ Reciprocity:** row-stochastic matrix output
- **→ Apogee:** signal score as Q input
- **→ Amethyst:** coherence report + gate status

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
