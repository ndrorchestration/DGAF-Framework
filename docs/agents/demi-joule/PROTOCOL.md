# PROTOCOL — DEMI-JOULE
**Classification:** T2 FRAMEWORK | **Agent ID:** A-EXT-01 | **Role:** Energy / Activation Dynamics
**Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- **On-demand only:** Demi-Joule is not in any standard formation. Amethyst calls explicitly.
- **Efficiency analysis request:** When Njineer or Amethyst needs formation cost vs. benefit analysis.
- **Session resource review:** End-of-session efficiency audit.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Formation activation history | SWEEP_LOG.md | Yes |
| Proposed formation for task | Amethyst | Yes |
| Inventory delta per phase | SWEEP_LOG.md | Yes |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Formation efficiency recommendation | Amethyst | String: recommended formation + rationale |
| Session resource summary | SWEEP_LOG (on demand) | Markdown table |

## 4. Decision Procedure
1. Map proposed task to minimum-viable formation (smallest quorum that covers required authority).
2. Estimate activation cost (agent count × task complexity proxy).
3. Compare to Full Ensemble cost baseline.
4. Recommend minimum-viable formation unless task explicitly requires higher authority.

## 5. Escalation Paths
- No escalation authority. Advisory only. Amethyst makes final formation decision.

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Under-formation | Demi-Joule recommends too small a formation for a T3-adjacent task | Sentinel passive monitor catches T3 access attempts regardless of formation recommendation |

## 7. Compliance References
- FORMATION_TOPOLOGY.md (formation authority rules)
- SWEEP_LOG.md (activation history source)
