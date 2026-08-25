# Operating Governance Consistency Statement

**Statement date:** 2026-08-25 (post HEAD `648e838fac0312401154604f2d8e7e4eff058378`)

**Authoritative candidate tree (P8 binding):** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

**Head SHA:** `648e838fac0312401154604f2d8e7e4eff058378` (20 commits ahead of `origin/main`)

**Epistemic boundary:** N=0, NOT GRANTED, PRE-FREEZE — throughout this statement.

**Purpose:** This statement records the current governing state across the P1-P9 predicate matrix as asserted by the authoritative governance documents in this repository. It is a consistency cross-reference, not an execution record. All predicates remain in non-closed states.

**Author identity:** ndrorchestration (repository owner)

**Governing documents referenced:**
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md` (HEAD `648e838`)
- `docs/governance/DELIBERATIVE_OPERATIONAL_POLICIES.md` (HEAD `648e838`)
- `docs/governance/P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` (HEAD `648e838`)
- `docs/governance/STAGE3_VERIFICATION_INVENTORY.md` (HEAD `648e838`)
- `docs/governance/P8_VERIFICATION_CHECKLIST.md` (HEAD `648e838`)
- `docs/governance/P8_ANALYSIS_LOCK.md` (HEAD `648e838`)
- `docs/governance/P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md` (HEAD `648e838`)
- `docs/governance/ADVERSARIAL_PANEL_REVIEW_2026-08-21.md` (HEAD `648e838`)
- `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` (HEAD `648e838`)
- `docs/experiment/P3_P4_P5_P6_FREEZE_READINESS_2026-08-21.md` (HEAD `648e838`)

---

## Per-Predicate Governing State

| Predicate | Status (from governing docs) | Key evidence / basis | OPEN items |
|-----------|------------------------------|---------------------|------------|
| **P1 — Candidate Integrity** | IMPLEMENTED / NOT FROZEN | Candidate `2a80f819...` identified in P8 checklist + analysis lock; 24 CI workflows + 7 test files present at candidate; post-candidate commits are documentation-only | Create immutable freeze; bind source/config/environment/evidence; re-run verification; separate future dev |
| **P2 — Execution Contract** | IMPLEMENTED / NOT CANDIDATE-SCOPED | Runner emits `ffcr_success`; schema requires topology/failure_count; analysis consumes validated artifacts; local test `test_execution_contract.py` passes | Execute against candidate `2a80f819...`; retain run ID/URL/SHA/logs; inspect job logs |
| **P3 — Artifact Contract** | IMPLEMENTED / NOT CANDIDATE-SCOPED | FFCR defined in P7 Decision 5 + P8 lock; `condition_ffcr()` in analysis.py; local test `test_analysis.py` passes | Execute against candidate; retain evidence |
| **P4 — Security / Blinding** | IMPLEMENTED / PARTIAL EVIDENCE | `blinding_operational_test.py` exists; synthetic/control evidence exists; Policy 2 defines 4-part evidence standard | Operational proof: executor isolation, blinded-ID consistency, custody separation, dry-run |
| **P5 — Provenance / Reproducibility** | IMPLEMENTED / NOT CANDIDATE-SCOPED | Topology fingerprints verified locally (P8 checklist item 5 checked); artifact schema requires `artifact_sha` | Candidate-scoped reproduction; environment fingerprint; seed/RNG verification |
| **P6 — Durable Evidence Custody** | OPEN | No archive destination; no retrieval/hash proof; Policy-level document exists | Establish archive; write evidence; retrieve independently; verify integrity; document custody chain |
| **P7 — Scientific Target Specification** | TECHNICALLY ADJUDICATED / FORMALLY OPEN | P7 adjudication record (panel-ready 2026-08-23) presents 11 decisions, all OPEN / PENDING AUTHORITY ADOPTION; primary contrast (DGAF vs null) selected; traceability matrix created | Authority adopts all 11 decisions; verify treatment/reference match; reconcile with protocol + P8 spec SHAs; record authority/date/identity; bind to freeze candidate; update status to CLOSED |
|| P8 | Analysis Lock | IMPLEMENTED / NOT CANDIDATE-SCOPED / FAIL-CLOSED | Analysis lock identifies candidate `2a80f819...`; P7 inputs fixed; 6/20 checklist items checked (artifact contract); 14/20 unchecked | Execute all 14 unchecked items against candidate; retain run ID/URL/SHA/logs/artifacts for each |
| **P9 — Independent Verification** | NOT EXECUTED | Architecture documented; no independent verification executed | Designate independent auditor; reproduce candidate identity, artifact integrity, key analysis, invariants, adversarial failures |

---

## P7 Formal Closure Conditions (from P7 Adjudication Record)

Before P7 can be marked CLOSED, all of the following must be satisfied:

1. [ ] Explicit adoption of all 11 decisions by the designated experimental-control authority
2. [ ] Verification that treatment/reference identifiers match the actual candidate apparatus
3. [ ] Reconciliation of adopted decisions with exact protocol SHA and P8 analysis specification SHA
4. [ ] Recording of authority, date, and adopted decision identity
5. [ ] Binding the adopted record to the exact freeze candidate without silently changing any decision
6. [ ] All 11 decisions classified as P7 scientific vs P8 implementation (in traceability matrix)
7. [ ] P7 record status changed from OPEN to CLOSED with provenance

**Current state:** None of the above conditions are satisfied. P7 remains OPEN.

---

## Cross-Document Consistency Verification

The following status claims were verified consistent across all governing documents:

| Predicate | CURRENT_STATE.md | PDM_CONTROL_STATE.md | P1-P9 MATRIX | DELIBERATIVE POLICIES | CONSISTENT? |
|-----------|-----------------|---------------------|---------------|----------------------|-------------|
| P4 | PARTIAL | PARTIAL | IMPLEMENTED / PARTIAL EVIDENCE | Cited as PARTIAL | ✓ |
| P6 | OPEN | OPEN | OPEN | Cited as OPEN | ✓ |
| P9 | NOT EXECUTED | NOT EXECUTED | NOT EXECUTED | Cited as NOT EXECUTED | ✓ |
| P7 | TECHNICALLY ADJUDICATED / FORMALLY OPEN | TECHNICALLY ADJUDICATED / PROPOSED AUTHORITATIVE SPECIFICATION / FORMALLY OPEN | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Cited as OPEN (11 decisions PENDING) | ✓ |
| P8 | OPEN / FAIL-CLOSED | OPEN / FAIL-CLOSED | IMPLEMENTED / NOT CANDIDATE-SCOPED / FAIL-CLOSED | Cited as OPEN (15 unchecked) | ✓ |
| N=0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| NOT GRANTED | ✓ | ✓ | ✓ | ✓ | ✓ |
| PRE-FREEZE | ✓ | ✓ | ✓ | ✓ | ✓ |

**All cross-document status claims are consistent.** No contradictions remain after the P7 correction (commit `222fb4c`).

---

## P2/P6a Applicability Statement

Per the PDMAL Current Control State and Policy 3, P2/P6a are currently in status **PARTIAL / APPLICABILITY REQUIRED**. Candidate-scoped evidence OR a justified applicability decision is required.

The STAGE3 verification inventory records these as UNCHECKED with applicability decisions pending. Policy 3 defines the three admissible options (A: defer, B: alternative verification, C: retain OPEN). No option has been chosen or recorded as of this statement.

Per panel guidance (Policy 3, Prohibited Action): "unavailable" cannot be converted to "N/A" and then to closed. At least one of Options A, B, or C must be explicitly selected and recorded.

---

## P7 Scientific Decision Boundary

Per the P7 traceability matrix and Policy 1, the following classification holds:

**P7 Scientific Decisions (adjudication-required):**
Reference condition, estimand, unit of analysis, direction of effect, endpoint aggregation, CI convention, directional support criterion, exclusion rules, multiplicity treatment, RNG domain separation, success criterion, falsification criterion

**P8 Implementation Constants:**
Bootstrap resample count (10,000), analysis bootstrap seed (20260823)

**Boundary case:**
- CI alpha level (0.05): Stated as P8 implementation constant in Policy 1 because it is the numeric instantiation of the P7 scientific decision (95% CI convention). Changing alpha independently of the CI convention would constitute a substantive change requiring re-adjudication.

---

## Governance Review Record Reference

The 2026-08-21 Adversarial Expert Panel Review (`docs/governance/ADVERSARIAL_PANEL_REVIEW_2026-08-21.md`) remains the most recent formal governance review on record. Its 10 findings (A1-A10) and required adversarial pre-flight conditions remain applicable.

The 2026-08-24 expert-panel assessment (user-provided, not yet a formal governance record) identified additional weaknesses addressed by the four governance documents committed at HEAD `222fb4c`:
- P7 contradiction → resolved by traceability matrix + control state corrections
- Parameter boundary mismatch → resolved by Policy 1
- P2/P6a applicability gap → resolved by Policy 3
- Post-freeze change ambiguity → resolved by Policy 4
- Adversarial preflight gaps → resolved by Policy 5
- Unblinding procedure gaps → resolved by Policy 6
- Comparative baseline drift → resolved by Policy 7

The 2026-08-24 assessment findings are now incorporated as explicit control items in the governing documents. They have not yet been recorded as a formal governance review record in the repository.

---

## Hygiene Invariant Verification

Per the STAGE3 verification inventory, all 6 hygiene invariants hold:

1. ✓ P8 closure claim requires executed candidate-scoped evidence, not implementation presence
2. ✓ Historical freeze not misrepresented as current freeze (`3510b868...` superseded)
3. ✓ No silent apparatus redefinition (boundary sections in CURRENT_STATE.md + PDM_CONTROL_STATE.md)
4. ✓ Historical evidence retains SHA provenance (6 `4983f44a` references labeled as provenance in manifest)
5. ✓ N=0 and NOT GRANTED preserved across all governing documents
6. ✓ P8 checklist self-verification not allowed as closure (checklist item 21)

---

## Remaining Governance Gaps

1. **No formal governance review record for the 2026-08-24 expert-panel assessment.** The findings are incorporated as control items but not yet recorded as a formal governance artifact with authority, date, and adopted identity.

2. **P2/P6a applicability decision not yet made.** Options A/B/C remain unchosen. This blocks P2 and P6a closure.

3. **No pre-authorization evidence registry.** A structured registry mapping evidence artifacts → predicates → candidate SHA → retention location does not yet exist.

4. **P6 archive destination not established.** Durable custody remains OPEN.

5. **No immutable freeze created.** P1 remains NOT FROZEN.

---

## Epistemic Boundary Statement

**N=0. NOT GRANTED. PRE-FREEZE.**

No empirical execution has occurred. No predicate is closed. Pilot authorization is not granted. The governing state recorded in this statement is derived from the authoritative governance documents at HEAD `648e838fac0312401154604f2d8e7e4eff058378`. Any change to this state must be recorded through an explicit governance action (adoption, evidence execution, or closure) in the repository.

---

*End of operating governance consistency statement.*
