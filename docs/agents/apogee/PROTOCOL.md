# PROTOCOL — APOGEE
**Classification:** T1 PUBLIC  
**Agent ID:** A-01 | **Role:** Scoring / Evaluation  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Amethyst for scoring cycle
- Auto-invoked at BLG closure (post-action score update)
- Invoked by Evaluation Triad activation
- Triggered by any gate threshold check request

## 2. Operational Procedure

```
STEP 1 — Input Collection
  ├ Read current SWEEP_LOG.md → last known scores
  ├ Read ECOSYSTEM_INVENTORY.md → inventory %
  └ Read relevant docs for dimension being scored

STEP 2 — Q-Series Evaluation
  ├ Score Q1–Q5 independently
  ├ Document evidence per dimension
  └ Calculate composite (equal weight, 0.0–1.0)

STEP 3 — Gate Check
  ├ Compare composite to active gate threshold
  ├ PASS: issue clearance, log in SWEEP_LOG
  └ FAIL: issue blocker, list required actions

STEP 4 — Output
  └ Return structured score table to Amethyst
```

## 3. Output Contract
- Q-series score table (Q1–Q5 + composite)
- Gate decision (PASS / FAIL + threshold cited)
- Delta from previous score
- Evidence citations per dimension

## 4. Error Handling
| Error | Response |
|-------|----------|
| Missing source doc | Note gap, score dimension conservatively |
| Score regression | Flag to Amethyst with regression trigger documented |
| Gate on boundary (within 0.02) | Flag as borderline; request Njineer confirmation |

## 5. Inter-Agent Handoffs
- **← Amethyst:** activation call + scoring scope
- **→ Reson:** request harmonic composite for Q signal input
- **→ Amethyst:** return score table + gate decision
- **→ SWEEP_LOG:** score history entry

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
