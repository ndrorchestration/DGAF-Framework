# P1-P9 Deliberative Predicate Evidence Matrix

**Purpose:** Map each of the 9 Deliberative Predicates to its required claim, exact evidence, current status, and notes. This is a planning artifact — it records what evidence is needed and what state each predicate is currently in. It does NOT constitute executed evidence.

**Current HEAD SHA:** `222fb4c9832b77c88791363ad7923646801b9a4a` (19 commits ahead of `origin/main`; 1 new commit since candidate — governance documentation incorporation)

**Exact candidate tree (P8 binding):** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

**Date compiled:** 2026-08-24 (post-PR #83,#84,#76 integration)

**Epistemic boundary:** N=0, NOT GRANTED, PRE-FREEZE. No empirical execution has occurred. No predicate is closed. Pilot authorization is not granted.

**Reference documents:**
- P3/P4/P5/P6 Freeze Readiness (2026-08-21)
- P8 Analysis Lock (governance)
- P8 Verification Checklist (governance)
- PDMAL Protocol Matrix Amendment v0.7.5 (experiment)
- PDMAL Task Spec v0.7.4 (experiment)
- PDMAL Current Control State (experiment)
- P7 Adjudication Record — Panel-Ready (governance)

---

## Matrix

| Predicate | Required claim | Exact evidence | Status | Notes |
|-----------|---------------|----------------|--------|-------|
| **P1 — Candidate Integrity** | Exact candidate identified and hash-anchored; after freeze, no reinterpretation of the candidate is allowed; any substantive change invalidates and requires a new freeze cycle | Candidate tree `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is identified in P8 checklist and P8 analysis lock. 24 CI workflows + 7 test files present at candidate. Post-candidate commits verified as documentation-only (no substantive change). | **IMPLEMENTED / NOT FROZEN** | Candidate identified but not frozen. Historical freeze `3510b868...` explicitly superseded in CURRENT_STATE.md and PDMAL_CURRENT_CONTROL_STATE.md. Post-candidate documentation-only commits do not redefine apparatus. |
| **P2 — Execution Contract** | Runner emits `ffcr_success`; schema requires `topology` and `failure_count`; analysis consumes only validated seed artifacts; no repair or imputation of missing outcomes | Runner `run_pilot.py` (blob `21a40aeb...`) emits `ffcr_success`, `topology`, `failure_count`. Schema `pilot_artifact_schema.py` (blob `36c147c...`) requires these fields. Analysis `analysis.py` consumes validated artifacts, rejects incomplete/duplicate matrices. Local test: `test_execution_contract.py` (200 lines, 2 tests) passes locally. | **IMPLEMENTED / NOT CANDIDATE-SCOPED** | Implementation verified locally. Not executed against exact candidate `2a80f819` in CI. Per panel: must run Governance CI + python-tests against candidate, retain run ID/URL/SHA/logs, and inspect job logs. |
| **P3 — Artifact Contract** | Successful trial = `ffcr_success=true` AND consensus_quality threshold met; FFCR computed per (condition, topology) pair; seed-level paired effect `Delta_s`; analysis resamples seed effects (not individual trials) | FFCR defined in P7 Decision 5 and P8 analysis lock. `condition_ffcr()` in `analysis.py` computes per-condition FFCR. `primary_estimate()` computes mean paired seed effects. `decision()` implements support rule. Local tests: `test_analysis.py` (7 tests) pass locally. | **IMPLEMENTED / NOT CANDIDATE-SCOPED** | Implementation verified locally. Not executed against candidate. P8 checklist CI evidence section + evidence custody section require candidate-scoped evidence. |
| **P4 — Security / Blinding Integrity** | Blinding key as env var NOT hardcoded; executor cannot recover key from binary/env; blinded IDs used in artifacts; unblinding map custody separated; operational proof required (not just synthetic); key distribution mechanism documented | `blinding_operational_test.py` implements blinding. Current control state: "synthetic/control evidence exists; operational custody and unblinding procedure remain evidence-bound." P4 status: PARTIAL. | **IMPLEMENTED / PARTIAL EVIDENCE** | Synthetic/control evidence exists. Operational proof missing: executor cannot-access-key proof, blinded-ID consistency proof, custody separation proof, dry-run exercise. Per panel: must demonstrate all four (a-d) operationally, not just synthetically. Policy 2 in DELIBERATIVE_OPERATIONAL_POLICIES.md defines required behavior. |
| **P5 — Provenance / Reproducibility** | Every artifact has SHA256 digest and source; reproducibility verified by independent recreation; environment fingerprint recorded; topology fingerprints deterministic | `topology_utils.py` defines 5 topology fingerprints (consistent with P8 checklist items 4, 29, 31 — CHECKED locally). Artifact schema requires `artifact_sha` field. Current control state: "bindings exist; candidate-scoped reproduction and environment evidence remain incomplete." P5 status: PARTIAL. | **IMPLEMENTED / NOT CANDIDATE-SCOPED** | Topology fingerprints verified locally (P8 checklist artifact-contract item 5 checked; reproducibility items require candidate-scoped evidence). Full reproducibility + environment fingerprint + topology fingerprints + seed/RNG separation not executed against candidate. P8 checklist reproducibility items (executed-tree identity reconciled, environment fingerprint, deterministic topology fingerprints, seed/RNG separation) require candidate-scoped evidence. |
| **P6 — Durable Evidence Custody** | Evidence archived to durable location; independently retrievable; integrity verified (hash check); custody chain documented | No archive destination established. No retrieval/hash proof exists. Current control state: "Durable retention | OPEN — Archive destination plus independent retrieval/hash proof required." P6 status: OPEN. | **OPEN** | Policy-level document exists but no operational evidence. Per panel: must demonstrate evidence written → retained → independently retrieved → integrity verified. Retention policy alone is insufficient. |
| **P7 — Scientific Target Specification** | 11 scientific decisions formally adjudicated and adopted; estimand/estimator separated; estimand ≠ estimator; non-support ≠ evidence against; planning thresholds ≠ success thresholds; exclusions objectively defined | P7 Adjudication Record (panel-ready 2026-08-23) presents 11 decisions. All 11 are OPEN / PENDING AUTHORITY ADOPTION. Primary contrast (DGAF vs null) selected in prior reconciliation. Formal authority adoption NOT occurred. Adopted record NOT bound to candidate. | **TECHNICALLY ADJUDICATED / FORMALLY OPEN** | Contradiction resolved: CURRENT_STATE.md and PDMAL_CURRENT_CONTROL_STATE.md previously said "ADOPTED" — corrected to "TECHNICALLY ADJUDICATED / FORMALLY OPEN." P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md created with full 11-decision breakdown. Per panel: must resolve before P8 can claim scientific derivation. Formal closure requires 5 conditions (identity, verification, reconciliation, recording, binding). |
| **P8 — Analysis Lock** | Analysis implementation bound to exact candidate; P7 inputs fixed; Governance CI executed against candidate; all 20 checklist items addressed; 14 unchecked items have candidate-scoped evidence | P8 analysis lock identifies candidate `2a80f819...`; P7 inputs fixed; 6/20 checklist items checked (artifact contract: `[x]` items 1-6 from `P8_VERIFICATION_CHECKLIST.md` lines 11-16, locally verified); 14/20 unchecked (CI evidence: `[ ]` items 7-12; reproducibility: `[ ]` items 13-16; evidence custody: `[ ]` items 17-20, from `P8_VERIFICATION_CHECKLIST.md` lines 20-39). P8 status: OPEN / FAIL-CLOSED. | **IMPLEMENTED / NOT CANDIDATE-SCOPED** | Implementation ready. Zero candidate-scoped evidence executed. P8 checklist closure rule: "P8 remains open until every applicable unchecked item has candidate-scoped evidence." Per jurisdiction: execute Governance CI against exact candidate; inspect and retain all artifacts; fill ALL 14 unchecked boxes across CI evidence (6), reproducibility (4), and evidence custody (4) sections. STAGE3_VERIFICATION_INVENTORY.md catalogs all 24 workflows + 7 test files against candidate. |
| **P9 — Independent Verification** | Independent auditor verifies frozen candidate and evidence package without using same schema/analysis/hashes/assumptions as candidate self-validation; reproduces at minimum: candidate identity, artifact integrity, key analysis calculations, critical invariants, relevant adversarial failures | No independent verification has been executed. Current control state: "P9 independent verification | NOT EXECUTED — Must be independent of candidate self-validation." P9 status: NOT EXECUTED. | **NOT EXECUTED** | Architecture documented but no execution. Per panel: must demonstrate independence — auditor must not simply repeat candidate self-validation through same assumptions. Must independently reproduce candidate identity, artifact integrity, key analysis calculations, critical invariants, and adversarial failures. |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **IMPLEMENTED** | Code, configuration, or policy exists that satisfies the required claim. Does NOT mean candidate-scoped evidence has been executed. |
| **TESTED** | Local tests or synthetic/demo evidence exists. Does NOT mean candidate-scoped evidence has been executed. |
| **VERIFIED** | Implementation has been checked against source documents or locally verified. Not candidate-scoped CI evidence. |
| **PARTIAL** | Some evidence exists (e.g., synthetic, local, or partial) but operational/candidate-scoped evidence is missing. |
| **OPEN** | No evidence exists. Predicate requires execution before it can be closed. |
| **NOT EXECUTED** | No evidence of any kind has been produced. |
| **NOT FROZEN** | Candidate identified but freeze has not been created. |
| **FAIL-CLOSED** | P8 is fail-closed: implementation presence does NOT close it; candidate-scoped evidence required. |

**IMPORTANT:** None of these statuses constitute closure. All predicates remain in non-closed states. A predicate becomes closed only when candidate-scoped evidence is executed, retained, and independently verified against the exact candidate tree.

---

## Summary by Status

| Status | Count | Predicates |
|--------|-------|------------|
| IMPLEMENTED | 7 | P1, P2, P3, P4, P5, P7, P8 |
| TESTED (local) | 4 | P2, P3, P5, (P1 artifact‑contract sub‑items) |
| PARTIAL | 3 | P4 (synthetic only), P5 (bindings only), P2/P6a (applicability pending) |
| OPEN | 2 | P6 (no archive), P7 (formally OPEN — authority adoption pending) |
| NOT EXECUTED | 1 | P9 |
| NOT FROZEN | 1 | P1 (candidate identified, freeze not created) |
| FAIL-CLOSED | 1 | P8 (implementation present, evidence absent) |

**No predicate is CLOSED.** Every predicate requires additional evidence before closure.

---

## Residual OPEN Items (must be resolved before any predicate is closed)

### P1 — Freeze
- Create immutable freeze commit after pre-freeze closure
- Bind source, analysis config, environment, and verification evidence to freeze
- Re-run required verification against immutable reference
- Separate future development from frozen experimental apparatus

### P2/P6a — Runtime Verification
- Execute candidate runtime verification OR select justified alternative OR retain OPEN with defined conditions
- Per panel: cannot convert "unavailable" → "N/A" → closed
- Must record choice (A/B/C) and rationale in evidence matrix

### P4 — Blinding Operational
- Demonstrate executor cannot obtain unblinding key under any execution path
- Demonstrate blinded IDs consistently applied across artifacts
- Demonstrate custody of unblinding mapping is separated from executor and analysis
- Execute dry-run that exercises unblinding procedure without compromising pilot
- Document key distribution mechanism

### P5 — Full Reproducibility
- Execute candidate-scoped reproduction: same inputs → same outputs
- Capture environment fingerprint
- Verify topology fingerprints are deterministic for candidate
- Verify seed/RNG separation and trial ordering

### P6 — Durable Custody
- Establish archive destination
- Write evidence to archive
- Retrieve independently
- Verify integrity (hash check against recorded value)
- Document custody chain

### P7 — Formal Scientific Adjudication
- Authority adopts all 11 decisions explicitly
- Verify treatment/reference identifiers match candidate apparatus
- Reconcile adopted decisions with protocol SHA and P8 analysis spec SHA
- Record authority, date, adopted decision identity
- Bind adopted record to exact freeze candidate without silently changing any decision
- Update status from OPEN to CLOSED in P7 record
- Update CURRENT_STATE.md and PDMAL_CURRENT_CONTROL_STATE.md accordingly

### P8 — Candidate-Scoped CI Evidence
- Execute all 14 unchecked checklist items against exact candidate `2a80f819...`:
  - **CI evidence section (6 items):** Governance CI, P8 analysis tests, P8 artifact-schema/security tests, compilation, run ID/URL/SHA/ref/event retention, job logs inspected
  - **Reproducibility section (4 items):** Executed-tree identity reconciled, environment fingerprint, deterministic topology fingerprints, seed/RNG separation and trial ordering
  - **Evidence custody section (4 items):** CI logs/artifacts retained at durable location, retained artifacts retrieved independently, retrieval hashes verified, blinding custody boundary documented

For each: retain run ID, URL, exact SHA/ref/event, job logs (inspected, not inferred), and artifact integrity values.

### P9 — Independent Verification
- Designate independent auditor (not using candidate's own schema/analysis/hashes/assumptions)
- Independently reproduce: candidate identity, artifact integrity, key analysis calculations, critical invariants, adversarial failures
- Record findings and resolution

---

## Verification Statement

> **This matrix is a planning artifact. It does not constitute executed evidence.**
>
> All OPEN items require candidate-scoped execution against the exact candidate tree `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` before they can be closed.
>
> **N=0. NOT GRANTED. PRE-FREEZE.** No empirical execution has occurred. No predicate is closed. Pilot authorization is not granted.

---

## Standards Reference

- P3/P4/P5/P6 Freeze Readiness assessment (2026-08-21): `docs/experiment/P3_P4_P5_P6_FREEZE_READINESS_2026-08-21.md`
- P8 Analysis Lock: `docs/governance/P8_ANALYSIS_LOCK.md`
- P8 Verification Checklist: `docs/governance/P8_VERIFICATION_CHECKLIST.md`
- P7 Adjudication Record: `docs/governance/P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`
- P7 Traceability Matrix: `docs/governance/P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md`
- PDMAL Current Control State: `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`
- PDMAL Protocol Matrix Amendment v0.7.5: `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`
- PDMAL Task Spec v0.7.4: `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md`
- Deliberative Operational Policies: `docs/governance/DELIBERATIVE_OPERATIONAL_POLICIES.md`
- Stage 3 Verification Inventory: `docs/governance/STAGE3_VERIFICATION_INVENTORY.md`

---

*End of P1-P9 Deliberative Predicate Evidence Matrix.*
