# Pre-Authorization Evidence Registry (PRER)

**File:** `docs/governance/CANDIDATE_PRER_FREEZE_CANDIDATE_EXCLUSION_REGISTER.md`

**Purpose:** Registry of all evidence artifacts required before a new freeze candidate can be considered for pre-authorization. This is a planning and tracking artifact — it records what MUST exist, who is responsible for creating it, and what criteria it must satisfy. It does NOT assert that any registry item is currently complete.

**Candidate tree (P8 binding):** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

**Head SHA (as of registry creation):** `648e838fac0312401154604f2d8e7e4eff058378`

**Epistemic boundary:** N=0, NOT GRANTED, PRE-FREEZE. No empirical execution has occurred. No predicate is closed. Pilot authorization is not granted.

**Status:** DRAFT — registry created but no entries have been verified complete. All entries remain in PENDING status until the responsible agent produces the evidence and marks it VERIFIED.

**Authority:** This registry is a proposed governance artifact. It requires formal adoption by the governance authority before it is binding.

---

## Registry

| # | Evidence artifact | Type | Purpose | Responsible agent | Gating predicate(s) | Required status | Exotic control (if any) | Acceptance criteria | Current state |
|---|-------------------|------|---------|-------------------|---------------------|-----------------|------------------------|---------------------|---------------|
| 1 | Governance CI run against candidate `2a80f819...` | CI execution artifact | Demonstrate that the governance CI workflow executes successfully against the exact candidate tree | CI system + workflow maintainer | P2, P8 | VERIFIED | Fail-closed on missing candidate SHA | Run ID, URL, exact SHA/ref/event, job logs inspected (not inferred), pass/fail outcome | PENDING |
| 2 | Python test suite execution against candidate | CI execution artifact | Demonstrate that all 7 test files pass against the exact candidate tree | CI system + test suite maintainer | P2, P3, P5, P8 | VERIFIED | Fail-closed on missing candidate SHA | Run ID, URL, pass/fail per test, any failures documented | PENDING |
| 3 | Analysis reproducibility run | CI execution artifact | Demonstrate deterministic output from same inputs (candidate SHA + seed) | CI system + analysis maintainer | P5, P8 | VERIFIED | Reproduce → identical output hash | Reproduction run ID, identical output hash compared to original | PENDING |
| 4 | Artifact schema validation artifact | CI execution artifact | Demonstrate that the pilot artifact schema validates correctly in CI | CI system + schema maintainer | P3, P8 | VERIFIED | Fail-closed on schema violation | Schema validation run ID, pass/fail | PENDING |
| 5 | FFCR contract enforcement artifact | CI execution artifact | Demonstrate that the FFCR contract fields are required and semantically fail-closed in CI | CI system + security maintainer | P2, P3, P8 | VERIFIED | Fail-closed on missing/invalid FFCR fields | Contract test run ID, pass/fail | PENDING |
| 6 | Truth layer integrity check artifact | CI execution artifact | Demonstrate that the truth layer integrity check passes in CI | CI system + truth layer maintainer | P8 | VERIFIED | Fail-closed on truth layer violation | Truth layer run ID, pass/fail | PENDING |
| 7 | Epistemic evidence validation artifact | CI execution artifact | Demonstrate that epistemic evidence validation passes in CI | CI system + epistemic maintainer | P8 | VERIFIED | Fail-closed on epistemic violation | Evidence validation run ID, pass/fail | PENDING |
| 8 | Blinding operational test artifact | CI execution artifact (operational dry-run) | Demonstrate operational blinding: executor cannot access key, blinded IDs applied, custody separated, dry-run exercises procedure | Blinding custodian + CI system | P4, P8 | VERIFIED | Operational proof (not synthetic); dry-run on surrogate data; key distribution documented | Blinding test run ID, pass/fail, key custody verification, dry-run results | PENDING |
| 9 | Runtime characterization artifact | CI execution artifact | Demonstrate runtime characterization metrics for the candidate | CI system + runtime maintainer | P6a, P8 | VERIFIED | Characterization run ID, metrics, pass/fail | Runtime characterization run ID, metrics recorded, pass/fail outcome | PENDING |
| 10 | P2 runtime verification (or applicability decision) | CI execution artifact OR applicability record | Demonstrate candidate runtime verification OR record justified applicability decision | Runtime maintainer + governance authority | P2, P6a | VERIFIED (if executed) OR APPLICABILITY DECIDED (if not) | Option A/B/C selection recorded; if B, 3-component limitations recorded | Runtime verification result OR applicability decision with rationale and limitations | PENDING |
| 11 | P6a CORS verification (or applicability decision) | CI execution artifact OR applicability record | Demonstrate P6a CORS verification OR record justified applicability decision | CORS maintainer + governance authority | P6a | VERIFIED (if executed) OR APPLICABILITY DECIDED (if not) | Same tripartite choice as P2 | CORS verification result OR applicability decision with rationale and limitations | PENDING |
| 12 | Instrumentation dry-run artifact | CI execution artifact | Demonstrate instrumentation dry-run validates data collection path | CI system + instrumentation maintainer | P6a, P8 | VERIFIED | Dry-run run ID, data collection path validation | Dry-run run ID, data collection path validated, pass/fail | PENDING |
| 13 | Pre-authorization security check artifact | CI execution artifact | Demonstrate pre-authorization security check passes | CI system + security maintainer | P4, P8 | VERIFIED | Security check run ID, pass/fail | Security check run ID, pass/fail outcome | PENDING |
| 14 | PPTL environment verification artifact | CI execution artifact | Demonstrate PPTL environment verification (dependency versions, pass/fail) | CI system + environment maintainer | P5, P8 | VERIFIED | Environment check run ID, dependency versions recorded, pass/fail | Environment check run ID, dependency versions, pass/fail | PENDING |
| 15 | Regression test suite artifact | CI execution artifact | Demonstrate regression test suite passes against candidate | CI system + regression maintainer | P2, P3, P5, P8 | VERIFIED | Regression run ID, pass/fail, any failures documented | Regression run ID, pass/fail, any failures recorded | PENDING |
| 16 | P6 durable evidence custody artifact | Archive + retrieval + hash verification | Demonstrate evidence written → retained → independently retrieved → integrity verified → custody chain documented | Durable custody custodian | P6 | VERIFIED | Archive destination established; retrieval evidence; hash verification; custody chain record | Archive destination set; evidence written; independent retrieval performed; hash verified against recorded value; custody chain documented | PENDING |
| 17 | P7 formal closure record | Governance record | Formal adoption of all 11 P7 decisions by designated authority, with verification, reconciliation, recording, and binding to freeze candidate | Governance authority | P7 | VERIFIED | All 5 closure conditions satisfied; status changed from OPEN to CLOSED | Explicit adoption record (authority, date, adopted identity); treatment/reference verification; protocol + P8 spec SHA reconciliation; binding to freeze candidate without silent change | PENDING |
| 18 | P1 immutable freeze commit | Git commit | Create immutable freeze commit that binds source, analysis config, environment, and verification evidence to exact candidate | Governance authority + repository maintainer | P1 | VERIFIED | Freeze commit created; new verification re-run against immutable reference; future dev separated | Freeze commit SHA; re-run verification result; development separation documented | PENDING |
| 19 | P9 independent verification artifact | Independent verification execution | Demonstrate independent auditor verifies frozen candidate without using same schema/analysis/hashes/assumptions as candidate self-validation | Independent auditor (separate from candidate authors) | P9 | VERIFIED | Independence proven; reproduces at minimum: candidate identity, artifact integrity, key analysis calculations, critical invariants, adversarial failures | Independent auditor identity; reproduction results; findings and resolution recorded | PENDING |
| 20 | Adversarial preflight artifacts | Resistance-to-error testing execution | Demonstrate all 4 preflight checks completed: candidate SHA vs deployment, artifact substitution detection, blinding-key leakage test, runtime ceiling enforcement | Adversarial preflight team | P1, P4, P8 (resistance-to-error) | VERIFIED | All 4 checks performed; findings resolved or explicitly bounded | Preflight check results (passed/failed/bounded) for all 4; any bounded findings with scope limitation stated | PENDING |
| 21 | Unblinding procedure record | Governance record | Document formal unblinding procedure: custodian role, authorizing authority, preconditions, execution sequence, recording requirements | Governance authority + blinding custodian | P4 (operational) | VERIFIED | Roles TBD at authorization time; 3 preconditions defined; recording requirements specified; emergency path defined | Unblinding procedure document with all required elements; roles designated at authorization time | PENDING |
| 22 | Comparative baseline schedule | Governance record | Document explicit schedule for post-pilot comparisons: null, simple, static, DGAF, DGAF+PDMAL | Governance authority | P7 (comparative, not gating) | VERIFIED | Each comparison scheduled; protocol before data collection; not retroactive prerequisite | Comparison schedule with target timeframes; protocol specifications for each comparison | PENDING |
| 23 | Documentation-only post-freeze change log | Repository history / auditable log | Record all post-freeze documentation corrections with date, author, description | Repository maintainer | P1 (post-freeze governance) | VERIFIED (when corrections occur) | Each correction recorded; no substantive change applied without new candidate cycle | Per-correction record: date, author, description; substantive changes require new candidate SHA + verification + freeze | PENDING (no post-freeze corrections exist yet) |

---

## Summary

**Total registry items:** 23

**By current state:**
- PENDING: 23 (none have been verified complete)

**By gating predicate:**
- P1: items 18, 23 (freeze, post-freeze change log)
- P2: items 1, 2, 10, 15, 20 (governance CI, python tests, P2 runtime, regression, adversarial preflight)
- P3: items 2, 4, 5, 15 (python tests, schema validation, FFCR contract, regression)
- P4: items 8, 10, 13, 20, 21 (blinding operational, P2 runtime, pre-auth security, adversarial preflight, unblinding procedure)
- P5: items 2, 3, 14, 15 (python tests, reproducibility, PPTL env, regression)
- P6: item 16 (durable custody)
- P6a: items 9, 11, 12 (runtime characterization, P6a CORS, instrumentation dry-run)
- P7: items 17, 22 (formal closure record, comparative baseline schedule)
- P8: items 1-15, 20 (all CI evidence items + adversarial preflight)
- P9: item 19 (independent verification)

---

## Exotic Controls Reference

Some registry items require exotic controls — controls that are not standard CI/CD practice but are required for the epistemic integrity of the DGAF/PDMAL freeze apparatus:

1. **Fail-closed on missing candidate SHA** (items 1-5, 7-9, 13-15): The CI workflow must verify that the exact candidate SHA is present in the execution context. If the SHA is missing or mismatched, the workflow must fail (not pass with a warning). This prevents candidate drift from producing false-green results.

2. **Reproduce → identical output hash** (item 3): The reproducibility run must produce output that is byte-for-byte identical to the original analysis output (or hash-identical if the output is deterministic but not byte-identical). Any divergence must be investigated and explained.

3. **Operational proof, not synthetic** (item 8): The blinding operational test must demonstrate actual operational behavior (executor cannot access key, blinded IDs in artifacts, custody separated) not merely a synthetic or demo procedure. A dry-run on surrogate data is acceptable but must exercise the actual procedure, not a simplified version.

4. **Option A/B/C recording** (items 10, 11): If candidate runtime verification is not executed, the applicability decision must follow the tripartite structure defined in Policy 3. "Unavailable → N/A → closed" is prohibited.

5. **Independence requirement** (item 19): The independent auditor must not use the same schema, analysis implementation, expected hashes, or assumptions as the candidate. The auditor must independently reproduce candidate identity, artifact integrity, key analysis calculations, critical invariants, and adversarial failures.

6. **Dry-run on surrogate data** (item 12): The instrumentation dry-run must use surrogate or synthetic data that exercises the actual data collection path, not a simplified or mocked version.

7. **Mapping hash, not key** (item 21): The unblinding record must include the mapping hash (a verifiable record that the released mapping matches the custodian's map) without revealing the map itself to the record.

---

## What This Registry Does NOT Assert

1. **No evidence is complete.** All 23 items remain PENDING. No registry entry has been verified as complete.

2. **No predicate is closed.** The registry maps evidence to predicates; it does not close any predicate. A predicate closes only when its required evidence is produced, retained, and independently verified.

3. **No execution is authorized.** The registry records what evidence is required for pre-authorization; it does not authorize any execution.

4. **The candidate is not frozen.** Item 18 (immutable freeze commit) is PENDING. The candidate `2a80f819...` is identified but not frozen.

5. **N=0.** No empirical execution has occurred. No pilot data exists.

6. **NOT GRANTED.** Pilot authorization is not granted.

7. **PRE-FREEZE.** The registry is a planning artifact created before any freeze. It may be updated before freeze. After freeze, changes must follow the documentation-only post-freeze policy (Policy 4).

---

## Update Procedure

This registry may be updated as evidence is produced:

1. When an entry's evidence is produced and verified, change its Current State from PENDING to VERIFIED and record the verification date, verifying agent, and any relevant artifact references (run ID, URL, SHA, etc.).

2. If an entry cannot be produced (e.g., runtime verification unavailable), record the applicability decision per Policy 3 (Option A/B/C) and update the Current State accordingly.

3. After freeze, only documentation-only corrections (Policy 4) may be applied to this registry without creating a new candidate cycle.

4. Any substantive change to this registry after freeze (e.g., adding a new required evidence item, changing acceptance criteria) invalidates the candidate and requires a new freeze cycle.

---

*End of Pre-Authorization Evidence Registry.*
