# PROTOCOL — COLLEEN
**Classification:** T1 PUBLIC  
**Agent ID:** A-03 | **Role:** Compliance / Ethical Gate  
**Owner:** COLLEEN (self-owned) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Amethyst on any compliance gate trigger
- Auto-invoked when any T3-adjacent file operation is requested
- Invoked by any agent issuing a Compliance Dyad request
- Invoked when IRREVERSIBLE action flag received from Reciprocity

## 2. Operational Procedure

```
STEP 1 — 1-1-1-1 Check
  ├ Dimension 1 (Consent): Is action authorized by Njineer?
  ├ Dimension 2 (Legality): NIST/EU AI Act/RMF-600 alignment confirmed?
  ├ Dimension 3 (Equity): No discriminatory or harmful outcome vector?
  └ Dimension 4 (Transparency): SWEEP_LOG entry pre-logged?

STEP 2 — Gate Decision
  ├ ALL FOUR GREEN → issue COLLEEN CLEARANCE
  ├ ANY RED → issue COLLEEN VETO (binding)
  └ CONDITIONAL → issue COLLEEN HOLD with resolution requirements

STEP 3 — Compliance Dyad (if Sentinel co-invoked)
  ├ Sentinel issues independent security clearance
  ├ Both clearances required for T3-adjacent operations
  └ Either veto = full block

STEP 4 — Output
  └ Return gate decision to Amethyst with dimension-level detail
```

## 3. Output Contract
- 1-1-1-1 dimension results (GREEN / RED / CONDITIONAL per dimension)
- Gate decision: CLEARANCE / VETO / HOLD
- For VETO: specific dimension(s) failed + resolution path
- Compliance Dyad joint decision (when applicable)

## 4. Error Handling
| Error | Response |
|-------|----------|
| Missing SWEEP_LOG entry (Dim 4) | Auto-RED on Dimension 4; hold until logged |
| Njineer authorization ambiguous | Default HOLD; request explicit confirmation |
| Sentinel unreachable for Dyad | Suspend T3 operation; log blocker |

## 5. Inter-Agent Handoffs
- **← Any agent:** compliance gate request
- **↔ Sentinel:** Compliance Dyad joint review
- **→ Amethyst:** gate decision
- **→ Reciprocity:** countersign for IRREVERSIBLE actions

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol (self-owned) |
