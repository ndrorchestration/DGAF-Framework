# QA Rubric — Agent Reciprocity

**Agent:** Agent Reciprocity  
**Role Domain:** Portfolio + Rollback  
**Formation:** Extended  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Reciprocity's TNR enforcement, version control integrity, feedback loop validation, and rollback path definition. Reciprocity is the trust and rollback authority.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **TNR Enforcement Accuracy** | 25% | ≥ 0.88 | Trust-Neutrality-Reciprocity principles applied consistently across agent interactions. No unilateral escalation without evidence. |
| D2 | **Version Control Integrity** | 25% | ≥ 0.92 | Commit history clean. No force-push without authorization. SHAs traceable to BLG closures. |
| D3 | **Rollback Path Definition** | 20% | ≥ 0.88 | Every P-15 checkpoint 9 includes a valid rollback path. Rollback tested against at least one prior sealed state. |
| D4 | **Feedback Loop Integrity** | 15% | ≥ 0.85 | Inter-agent feedback (Apogee score → Amethyst gate → COLLEEN archive) flows without corruption or dropped signals. |
| D5 | **Portfolio Consistency** | 15% | ≥ 0.85 | Across-session decisions are consistent. No contradictory versioning policies applied across repos. |

**Composite Pass:** ≥ 0.88.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Orphaned rollback path** | P-15 checkpoint 9 committed without a named rollback SHA | Sentinel blocks merge; Reciprocity must designate rollback SHA before re-gate |
| F2 | **Feedback signal drop** | Apogee score not propagated to COLLEEN archive after gate | COLLEEN surfaces at next P-02 as BLG; Reciprocity re-emits signal |
| F3 | **Retroactive TNR revision** *(non-obvious)* | Reciprocity re-interprets a past TNR decision under new framing without Amethyst sign-off | Amethyst flags; original decision preserved in CERTIFICATION_INDEX; revision requires new BLG |

---

## Gate Ownership

| Gate | Reciprocity Role |
|------|------------------|
| P-15 (checkpoint 9) | Rollback path definition |

---

*Rubric authority: Amethyst-Conductor.*
