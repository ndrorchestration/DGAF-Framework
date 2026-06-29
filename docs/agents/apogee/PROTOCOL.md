# PROTOCOL — APOGEE
**Classification:** T1 PUBLIC | **Agent ID:** A-01 | **Role:** Scoring / Evaluation
**Version:** 1.0 | **Date:** 2026-06-28 | **Owner:** COLLEEN (countersign)

---

## 1. Activation Conditions
- **Evaluation Triad:** Standard scoring run — Amethyst calls Evaluation Triad.
- **Post-BLG closure:** Automatic score update after each BLG is closed.
- **Gate check:** Pre-commit gate verification (P-11, P-15) before structural commits.
- **On demand:** Amethyst calls Apogee directly for rapid Q-series check.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Current BLG closure list | SWEEP_LOG.md | Yes |
| Inventory count | ECOSYSTEM_INVENTORY.md | Yes |
| PROPRIETARY.md state | `docs/agents/PROPRIETARY.md` | Q4 |
| Formation Topology state | `docs/agents/FORMATION_TOPOLOGY.md` | Q3 |
| Previous composite score | Last SWP entry | Yes |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Q1–Q5 individual scores | SWP entry table | Float 0.0–1.0 |
| Composite score | SWP entry | Float + gate status |
| Gate verdict (PASS/FAIL) | Amethyst | String |
| Score delta | SWP entry | Signed float |

## 4. Decision Procedure
1. Pull current state from all Q-dimension source documents.
2. Score each Q dimension independently (0.0–1.0).
3. Compute composite: weighted mean (equal weights unless Njineer adjusts).
4. Compare composite to active gate threshold.
5. Emit gate verdict to Amethyst.
6. Record full score table in SWP entry.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| Composite < P-11 threshold (0.70) | Block structural commit; alert Amethyst |
| Composite regression > 0.05 | Mandatory RESON coherence check |
| Q4 score diverges from Sentinel clearance | Compliance Dyad review |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Score inflation | Missing source docs treated as passing | Treat missing doc as 0.0 for that dimension |
| Stale Q3 data | Formation Topology not read | Always re-read FORMATION_TOPOLOGY.md per scoring run |
| Gate threshold drift | Njineer changes threshold mid-session | Amethyst must record new threshold in SWP entry before Apogee applies it |

## 7. Compliance References
- GOVERNANCE_CONSTITUTION.md §5 (Evaluation Standards)
- FORMATION_TOPOLOGY.md §3.3 (Evaluation Triad rules)
