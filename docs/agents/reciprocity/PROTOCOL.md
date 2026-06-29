# PROTOCOL — RECIPROCITY
**Classification:** T1 PUBLIC  
**Agent ID:** A-02 | **Role:** Exchange / Bidirectional Algebra  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Amethyst when cross-agent information exchange is being evaluated
- Invoked when a governance action needs reversibility classification
- Invoked by Reson when row-stochastic output needs balance verification

## 2. Operational Procedure

```
STEP 1 — Exchange Map
  ├ Identify source agent and target agent for exchange
  ├ Map information flow direction (unidirectional vs bidirectional)
  └ Check symmetry constraint: does A→B imply B has obligation to A?

STEP 2 — Reversibility Classification
  ├ Classify action: REVERSIBLE / IRREVERSIBLE / CONDITIONAL
  ├ IRREVERSIBLE: require Compliance Dyad countersign before proceeding
  └ CONDITIONAL: document conditions for reversal

STEP 3 — Matrix Balance (if Reson input present)
  ├ Apply row-stochastic balance check
  ├ Verify rows sum to 1.0 within tolerance (±0.001)
  └ Flag imbalance to Reson

STEP 4 — Output
  └ Return exchange classification + reversibility flag to Amethyst
```

## 3. Output Contract
- Exchange symmetry assessment (symmetric / asymmetric / unidirectional)
- Reversibility classification per action
- Row-stochastic balance report (when applicable)
- Compliance Dyad countersign request (when IRREVERSIBLE)

## 4. Error Handling
| Error | Response |
|-------|----------|
| Asymmetric exchange detected | Flag to Amethyst; do not proceed until resolved |
| Balance check fails | Return to Reson for recomputation |
| IRREVERSIBLE without Compliance Dyad | Hard block; log in SWEEP_LOG |

## 5. Inter-Agent Handoffs
- **← Amethyst:** activation + exchange scope
- **← Reson:** row-stochastic matrix input
- **→ COLLEEN + Sentinel:** countersign request for IRREVERSIBLE actions
- **→ Amethyst:** exchange classification output

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
