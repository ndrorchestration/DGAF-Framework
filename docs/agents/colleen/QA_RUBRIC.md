# COLLEEN — QA Rubric

**Agent:** COLLEEN · **Role:** Prefect A / Institutional Anchor / Ethical Gate
**Rubric version:** v1.0 · **Seeded:** S073 · 2026-06-29
**Classification:** T1 PUBLIC

---

## 1-1-1-1 Rubric

COLLEEN's QA rubric is binary per dimension. There is no partial credit. All four must be 1 for COLLEEN FULL GREEN.

---

### C1 — Compliance Alignment

**Score 1 (PASS):**
- All new P-series patterns registered in S073 have at least one compliance mapping (NIST/RMF-600/EU AI Act)
- All new agent specs and governance artifacts include a compliance tag or are explicitly exempt by Njineer authority
- No untagged artifacts in session output

**Score 0 (FAIL — VETO):**
- Any new pattern or artifact with no compliance mapping and no Njineer exemption
- Compliance tag conflicts with known standard definitions

**Remediation:** Amethyst adds compliance mapping; Njineer approves exemption if applicable. COLLEEN re-scores.

---

### C2 — Constitutional Fidelity

**Score 1 (PASS):**
- All session commits, BLG closures, flag resolutions, and artifact modifications are consistent with GOVERNANCE_CONSTITUTION.md v1.0
- No clause violated; no unapproved amendment introduced

**Score 0 (FAIL — HARD BLOCK):**
- Any action contradicts a constitution clause
- An unapproved amendment is introduced (even inadvertently)
- Constitution version referenced is not v1.0 or later ratified version

**Remediation:** Njineer only. COLLEEN cannot self-resolve a constitutional veto.

---

### C3 — Continuity Integrity

**Score 1 (PASS):**
- SESSION_ANCHORS.md is current (sealed or has active session entry)
- No orphaned session references in any doc
- ECOSYSTEM_INVENTORY.md reflects current state
- All prior sealed sessions are immutable

**Score 0 (FAIL — VETO):**
- SESSION_ANCHORS.md not updated at seal point
- Orphaned session reference detected (a session cited in a doc that has no anchor entry)
- ECOSYSTEM_INVENTORY.md stale by more than 1 session

**Remediation:** Amethyst updates anchors and inventory; COLLEEN re-scores.

---

### C4 — Coherence Gate

**Score 1 (PASS):**
- All terms used in session outputs match Vocab Master v1.3 canonical definitions
- No expansion conflicts (e.g., PDMAL not expanded as something other than canonical forms)
- No new abbreviations introduced without Vocab Master registration

**Score 0 (FAIL — VETO):**
- Any term used with a definition conflicting its Vocab Master entry
- Any unregistered abbreviation introduced in a canonical doc
- Semantic drift detected (same term used two different ways in session)

**Remediation:** Amethyst corrects term usage or registers new term in Vocab Master. Apogee attests. COLLEEN re-scores.

---

## VETO Override Conditions

| Condition | Override Authority |
|-----------|-------------------|
| C1 VETO (compliance gap) | Njineer exemption |
| C2 HARD BLOCK (constitutional) | Njineer only — no Amethyst override |
| C3 VETO (continuity) | Amethyst remediation + COLLEEN re-score |
| C4 VETO (coherence) | Amethyst + Apogee attestation + COLLEEN re-score |

---

*QA_RUBRIC.md · COLLEEN · v1.0 · S073 · 2026-06-29*
