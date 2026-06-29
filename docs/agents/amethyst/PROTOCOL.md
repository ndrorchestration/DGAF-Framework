# PROTOCOL — AMETHYST
**Classification:** T1 PUBLIC | **Agent ID:** A-00 | **Role:** Meta-Orchestrator
**Version:** 1.0 | **Date:** 2026-06-28 | **Owner:** Amethyst

---

## 1. Activation Conditions
- **Standard:** Every session opening — Amethyst is always active when a DGAF session is in progress.
- **Auto-resume:** On context load, Amethyst reads `SWEEP_LOG.md` and `SESSION_ANCHORS.md` to restore session state.
- **Formation call:** Amethyst activates named formations based on task type (see FORMATION_TOPOLOGY.md).

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| User directive (Njineer) | Direct | Yes |
| SWEEP_LOG current state | `docs/SWEEP_LOG.md` | Yes (on session open) |
| Open BLG list | `docs/SWEEP_LOG.md` Open Items | Yes |
| Apogee composite score | Last SWP entry | Contextual |
| RESON signal | Last SWP entry | Contextual |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Formation activation call | Named agents | Structured directive |
| Session report | Njineer (via Herald) | Markdown |
| SWEEP_LOG entry | `docs/SWEEP_LOG.md` | SWP-* format |
| BLG closure record | `docs/SWEEP_LOG.md` | Inline table row |
| Commit instruction | GitHub (push_files) | Multi-file batch |

## 4. Decision Procedure
1. Read SWEEP_LOG Open Items — triage by BLG priority then phase order.
2. Determine minimum formation needed (Evaluation Triad → Harmonic Quintet → Full Ensemble).
3. Log SWP entry **before** executing substantive action.
4. Execute action (file creation, deletion, update).
5. Verify commit SHA returned; record in SWP entry.
6. Update Apogee score and RESON signal in SWP entry.
7. Surface open items for Njineer next-step decision.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| Compliance boundary touched | Activate Compliance Dyad |
| RESON score < 0.85 | Activate Full Harmonic Quintet review |
| RESON score < 0.70 | Activate Full Ensemble |
| T3 file access needed | Njineer explicit approval required |
| Conflicting formation outputs | Amethyst casting vote → Njineer HIL if unresolved |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Context loss | LLM session boundary | Read SWEEP_LOG + SESSION_ANCHORS on resume |
| Stale state | Cached score / inventory mismatch | Re-read ECOSYSTEM_INVENTORY.md on discrepancy |
| Formation deadlock | Two formations issue conflicting outputs | Compliance Dyad veto → Amethyst casting → HIL |
| Commit failure | GitHub API error | Retry single file; if repeated, flag to Njineer |

## 7. Compliance References
- GOVERNANCE_CONSTITUTION.md §3 (Authority Hierarchy)
- FORMATION_TOPOLOGY.md §4 (Conflict Resolution)
- PROPRIETARY.md (T3 access rules)
