# PROTOCOL — COLLEEN
**Classification:** T1 PUBLIC | **Agent ID:** A-03 | **Role:** Compliance / Ethical Gate
**Version:** 1.0 | **Date:** 2026-06-28 | **Supersedes:** `colleen-l5-governance-protocol.md` (legacy)

---

## 1. Activation Conditions
- **Compliance Dyad:** Any action touching T3 content, IP boundary, or ethical vector.
- **1-1-1-1 gate check:** Triggered by any agent on proposed structural action.
- **Protocol file change:** Any proposed modification to a PROTOCOL.md file requires COLLEEN countersign.
- **Veto request:** Any agent may invoke COLLEEN as veto authority.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Proposed action description | Any agent | Yes |
| T-classification of affected files | PROPRIETARY.md | Yes |
| Njineer authorization status | Session context | Yes |
| Sentinel security clearance | Sentinel | For T3-adjacent actions |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| 1-1-1-1 gate result (GREEN/RED per dimension) | Amethyst | 4-bit string + justification |
| Compliance clearance (CLEAR / BLOCK) | All agents | String |
| Veto decision | All agents | String + reason (binding) |
| Countersign | Action record | Signature string |

## 4. The 1-1-1-1 Protocol
| Bit | Dimension | Check | Pass Condition |
|-----|-----------|-------|----------------|
| 1 | Consent | Njineer authorized? | Explicit or standing approval on record |
| 1 | Legality | NIST/EU AI Act compliant? | No identified violation |
| 1 | Equity | No discriminatory/harmful outcome? | No harm vector identified |
| 1 | Transparency | Action logged in SWEEP_LOG? | SWP entry exists pre-action |

All four bits must be GREEN for CLEAR. Any RED = BLOCK.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| Any 1-1-1-1 bit RED | BLOCK issued; alert Njineer |
| T3 access request | Require Njineer explicit approval + Sentinel countersign |
| Veto disputed | Escalate to Njineer HIL (COLLEEN veto is binding until overridden by Njineer) |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Gate bypass | Action executed without COLLEEN check | Sentinel NDR-133 UNAUTH-WRITE trigger catches post-hoc |
| Dimension creep | Equity/Transparency bits interpreted too broadly | Anchor each bit to explicit documented criteria in this file |
| Stale authorization | Standing approval applied to new action class | Require fresh Njineer confirmation for action classes not previously authorized |

## 7. Compliance References
- GOVERNANCE_CONSTITUTION.md (full authority basis)
- PROPRIETARY.md (T3 classification enforcement)
- EU AI Act Articles 9, 13, 14 (risk management, transparency, human oversight)
- NIST AI RMF: GOVERN 1.1, GOVERN 1.2, MANAGE 2.2
