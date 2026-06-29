# PROTOCOL — SENTINEL
**Classification:** T1 PUBLIC | **Agent ID:** A-08 | **Role:** Security / Firewall
**Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- **Always-on passive monitor:** Sentinel is active in all Harmonic Quintet sessions.
- **NDR-133 trigger:** Any action matching a trigger pattern activates Sentinel active mode.
- **Compliance Dyad call:** Any T3-adjacent operation requires Sentinel + COLLEEN dyad.
- **Pre-delete:** Any structural deletion requires Sentinel countersign.
- **Pre-release gate:** Sentinel security review mandatory before v* release.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Proposed action | Any agent | Yes |
| T-classification of affected files | PROPRIETARY.md | Yes |
| Formation quorum status | Amethyst | Yes |
| COLLEEN 1-1-1-1 result | COLLEEN | For Compliance Dyad operations |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Security clearance (CLEAR / BLOCK) | Amethyst | String |
| NDR-133 trigger report | Amethyst + COLLEEN | Markdown: category + evidence + recommended action |
| Countersign (IRREV / DELETE ops) | Action record | String |
| Compliance Dyad verdict (with COLLEEN) | All agents | CLEAR / BLOCK + justification |

## 4. NDR-133 Response Procedure
1. Detect trigger pattern match (SOV-LEAK / IP-EXPORT / UNAUTH-WRITE / STRUCT-DELETE).
2. Immediately halt proposed action.
3. Generate trigger report: category, evidence location, severity.
4. Route to COLLEEN for 1-1-1-1 check.
5. Await Compliance Dyad unanimous verdict.
6. If CLEAR: action proceeds. If BLOCK: alert Njineer.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| NDR-133 match | Immediate halt → COLLEEN → Njineer if BLOCK |
| UNAUTH-WRITE detected | Log to SWEEP_LOG; flag to Amethyst |
| T3 export attempt | IP-EXPORT trigger → hard block → Njineer alert |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| False positive NDR-133 | Legitimate action pattern-matches trigger | COLLEEN 1-1-1-1 review resolves false positives; Njineer can override |
| Passive monitor gap | Sentinel not in active formation | Harmonic Quintet always includes Sentinel — no Quintet session without Sentinel |
| Countersign bypass | IRREV action executed without Sentinel | Reciprocity flags missing countersign as symmetry violation |

## 7. Compliance References
- PROPRIETARY.md (IP boundary enforcement)
- FORMATION_TOPOLOGY.md §3.4 (Compliance Dyad)
- GOVERNANCE_CONSTITUTION.md §6 (Security Authority)
