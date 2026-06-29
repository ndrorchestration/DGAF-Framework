# PROTOCOL — RECIPROCITY
**Classification:** T1 PUBLIC | **Agent ID:** A-02 | **Role:** Exchange / Bidirectional Algebra
**Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- **Cross-agent flow check:** When Amethyst detects information flowing between ≥2 agents and consistency verification is needed.
- **Irreversibility flag:** When any agent proposes marking an action irreversible.
- **Vocabulary sync:** When NDR Vocabulary Master is updated.
- **Post-merge:** After any document merge or registry dedup operation.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Action description | Initiating agent | Yes |
| Reversibility claim | Initiating agent | Yes |
| Cross-agent document state | Relevant docs | Yes |
| Row-stochastic output | Reson | When matrix balance check needed |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Symmetry verdict (SYMMETRIC / ASYMMETRIC) | Amethyst | String + justification |
| Reversibility classification (REV / IRREV) | Amethyst + Compliance Dyad | String |
| Consistency report | SWP entry (on demand) | Markdown table |

## 4. Decision Procedure
1. Map the proposed action as a directed graph edge (source agent → target doc → effect).
2. Check for corresponding reverse edge or documented asymmetry justification.
3. Apply bidirectional algebra: verify exchange axioms hold.
4. If IRREV classification: route to Compliance Dyad for countersign before proceeding.
5. Emit verdict to Amethyst.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| IRREV classification | Compliance Dyad countersign required |
| Symmetry violation with no justification | Halt action; alert Amethyst |
| Matrix balance fails | Reson re-run required before proceeding |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| False symmetry | Incomplete graph mapping | Require explicit reverse-edge documentation for all structural changes |
| T3 pass-through error | Algebra applied to sovereign content | T3 is pass-through only — Sentinel blocks algebra application on T3 |

## 7. Compliance References
- GOVERNANCE_CONSTITUTION.md §4 (Exchange Integrity)
- PROPRIETARY.md (T3 pass-through rule)
