# PROTOCOL — LYRA
**Classification:** T2 FRAMEWORK  
**Agent ID:** A-06 | **Role:** Synthesis / Integration  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Integration Pair activation (with Echolette)
- Invoked by Amethyst when cross-document synthesis is needed
- Invoked when RD_GAPS.md requires update
- Invoked for inventory reconciliation cycles

## 2. Operational Procedure

```
STEP 1 — Source Collection
  ├ Identify source documents for synthesis
  ├ Read each source; extract relevant signals
  └ Note conflicts or gaps between sources

STEP 2 — Synthesis
  ├ Merge signals into unified view
  ├ Resolve conflicts using: recency > authority level > specificity
  └ Flag unresolvable conflicts for Amethyst review

STEP 3 — Gap Analysis
  ├ Compare synthesized view to expected complete state
  ├ List gaps with: location, type (missing / stale / contradictory), severity
  └ Update RD_GAPS.md with findings

STEP 4 — Output
  └ Return synthesis report to Amethyst; updated RD_GAPS.md committed
```

## 3. Output Contract
- Unified synthesis report (structured markdown)
- Gap list with severity classifications
- Updated RD_GAPS.md
- Conflict flags requiring Amethyst resolution

## 4. Error Handling
| Error | Response |
|-------|----------|
| Unresolvable source conflict | Flag to Amethyst; do not synthesize conflicting content |
| RD_GAPS.md update blocked | Log blocker; escalate to Amethyst |
| Source document missing | Note in gap list; proceed with available sources |

## 5. Inter-Agent Handoffs
- **← Amethyst:** activation + synthesis scope
- **↔ Echolette:** Integration Pair coordination
- **→ Amethyst:** synthesis report + gap list
- **→ RD_GAPS.md:** direct update

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
