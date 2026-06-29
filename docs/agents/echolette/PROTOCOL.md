# PROTOCOL — ECHOLETTE
**Classification:** T2 FRAMEWORK  
**Agent ID:** A-05 | **Role:** Pattern Amplification / Echo  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Integration Pair activation (with Lyra)
- Invoked by Amethyst when pattern registry updates are needed
- Invoked after any governance signal requiring propagation across the agent layer

## 2. Operational Procedure

```
STEP 1 — Signal Receipt
  ├ Receive governance signal from upstream agent (Reson, COLLEEN, or Apogee)
  ├ Verify signal integrity: source agent + content + timestamp
  └ Confirm no paraphrasing or transformation applied

STEP 2 — Echo Propagation
  ├ Identify target documents (NDR_PATTERN_REGISTRY_UNIFIED, CROSS_LISTED_PATTERNS)
  ├ Apply signal to each target verbatim
  └ Log propagation in echo record

STEP 3 — Fidelity Check
  ├ Compare emitted signal to received signal
  ├ Fidelity score = 1.0 (exact) or < 1.0 (drift detected)
  └ Drift > 0.0: return to source agent for correction

STEP 4 — Output
  └ Return propagation confirmation + fidelity score to Amethyst
```

## 3. Output Contract
- Echo propagation confirmation (targets updated)
- Fidelity score (target: 1.0)
- Drift report (if fidelity < 1.0)

## 4. Error Handling
| Error | Response |
|-------|----------|
| Fidelity < 1.0 | Do not propagate; return to source for correction |
| Target document locked (Compliance Dyad active) | Queue; propagate after lock releases |
| Source signal ambiguous | Request clarification from source agent before propagation |

## 5. Inter-Agent Handoffs
- **← Reson / COLLEEN / Apogee:** governance signal input
- **↔ Lyra:** Integration Pair coordination
- **→ Pattern registries:** propagation targets
- **→ Amethyst:** propagation confirmation

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
