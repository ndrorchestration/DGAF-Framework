# PROTOCOL — RESON
**Classification:** T1 PUBLIC | **Agent ID:** A-04 | **Role:** Harmonic Signal / Coherence
**Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- **Post-structural commit:** Reson runs a coherence check after every file creation/deletion batch.
- **Evaluation Triad:** Called by Amethyst alongside Apogee for quality sweeps.
- **Dissonance alert:** Any agent may invoke Reson if semantic contamination is suspected.
- **Pre-release gate:** Mandatory Reson check before any v* release tag.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| All modified documents (diff) | Git commit | Yes |
| NDR Vocabulary Master | `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` | Yes |
| Ionian Modal Matrix | `docs/agents/IONIAN_MODAL_HARMONIC_MATRIX.md` | Yes |
| Previous harmonic score | Last SWP entry | Yes |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Harmonic composite score (0.0–1.0) | SWP entry | Float |
| Dissonance report (if any) | Amethyst | Markdown: artifact ID + location + severity |
| Row-stochastic matrix output | Reciprocity | Matrix (sovereign math pointer only in T1) |
| Signal status (CLEAN / DISSONANT) | SWP entry | String |

## 4. Decision Procedure
1. Diff modified files against NDR Vocabulary Master for semantic drift.
2. Check structural alignment against Ionian Modal Matrix.
3. Compute harmonic composite (sovereign formula — SOV-001/002 pointer).
4. If DISSONANT: generate artifact report with location and severity.
5. Emit score and status to SWP entry via Amethyst.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| Score < 0.85 | Harmonic Quintet mandatory review |
| Score < 0.70 | Full Ensemble activation |
| Sovereign content detected in T1 file | NDR-133 SOV-LEAK → Sentinel immediate halt |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Score inflation | Diff not run against full vocabulary | Always diff against full NDR Vocabulary Master, not subset |
| False CLEAN | Semantic contamination in new terminology not yet in vocabulary | Reson flags new undefined terms as provisional dissonance |
| Sovereign formula exposure | SOV-001/002 referenced inline | T1 files contain pointer-only references; actual formula in Drive |

## 7. Compliance References
- PROPRIETARY.md SOV-001, SOV-002 (sovereign math pointers)
- IONIAN_MODAL_HARMONIC_MATRIX.md (modal alignment)
- NDR_INTERNAL_VOCABULARY_MASTER.md (semantic ground truth)
