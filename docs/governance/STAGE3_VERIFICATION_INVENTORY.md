# DGAF/PDMAL Stage 3 Verification Inventory

**Purpose:** Explicit reconciliation of every CI workflow and test suite against the exact candidate tree identified by the P8 checklist. No verification is assumed from documentation — each item is mapped to the actual workflow/test file present in the candidate tree, with applicability explicitly marked.

**Candidate tree (P8 checklist binding):** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

**Current HEAD:** `222fb4c9832b77c88791363ad7923646801b9a4a` (19 commits ahead of candidate; 1 new commit since candidate — governance documentation incorporation; all post-candidate commits are documentation/control reconciliation — no substantive apparatus change)

**Date compiled:** 2026-08-24

**Note on HEAD vs candidate:** The candidate tree and current HEAD contain identical CI workflow files and Python source files. The 18 commits between candidate and HEAD are documentation/control reconciliation commits (PR #83, PR #84, PR #76, and the local readiness report update). No substantive code, protocol, or apparatus change has occurred. Verification inventory is therefore the same for both trees, but must be recorded against the candidate SHA per P8 fail-closed rules.

---

## Section 1: CI Workflow Inventory (from candidate tree)

There are **24 CI workflow files** in the candidate tree `.github/workflows/`. Each is listed below with its intended verification category, current applicability, and whether it has been executed against the candidate.

| # | Workflow file | Verification category | Applicability to candidate | Executed against candidate? | Notes |
|---|--------------|----------------------|---------------------------|-----------------------------|-------|
| 1 | `truth-layer.yml` | Truth Layer Tests | **APPLICABLE** | NO — not executed against `2a80f819` | Verifies truth-layer integrity; part of P8 artifact contract |
| 2 | `truth-layer-tests.yml` | Truth Layer Tests | **APPLICABLE** | NO — not executed against `2a80f819` | Test suite for truth layer; complementary to truth-layer.yml |
| 3 | `epistemic-evidence-validation.yml` | Epistemic Evidence Validation | **APPLICABLE** | NO — not executed against `2a80f819` | Validates evidence against epistemic criteria |
| 4 | `pdmal-harness-validation.yml` | PDMAL Harness Validation | **APPLICABLE** | NO — not executed against `2a80f819` | Validates harness contract including FFCR semantics |
| 5 | `pdmal-pre-freeze-runner.yml` | PDMAL Pre-Freeze Runner Validation | **APPLICABLE** | NO — not executed against `2a80f819` | Validates runner before freeze; part of P8 artifact contract |
| 6 | `pdmal-blinding-operational-test.yml` | Blinding Operational Verification | **APPLICABLE** | NO — not executed against `2a80f819` | Operational blinding test; distinct from synthetic/control evidence |
| 7 | `pdmal-instrumentation-dry-run.yml` | Instrumentation Dry-Run | **APPLICABLE** | NO — not executed against `2a80f819` | Dry-run instrumentation; validates data collection path |
| 8 | `pdmal-preauth-security.yml` | PDMAL Pre-Authorization Security | **APPLICABLE** | NO — not executed against `2a80f819` | Security controls pre-authorization check |
| 9 | `pdmal-runtime-characterization.yml` | PDMAL Runtime Characterization | **APPLICABLE** | NO — not executed against `2a80f819` | Runtime characterization for P6a evidence |
| 10 | `p2-runtime-verification.yml` | P2 Live Runtime Verification | **CONDITIONAL** — applicability depends on deployment environment | NO — not executed against `2a80f819` | Per panel: must choose (1) candidate runtime succeeds, (2) justified alternative, or (3) remains OPEN with defined conditions |
| 11 | `p6a-cors-verification.yml` | P6a CORS Verification | **CONDITIONAL** — applicability depends on deployment environment | NO — not executed against `2a80f819` | Part of runtime-dependent verification |
| 12 | `governance-ci.yml` | Governance CI | **APPLICABLE** | NO — not executed against `2a80f819` | Core governance CI; candidate-scoped evidence requirement |
| 13 | `python-tests.yml` | Python Test Suite | **APPLICABLE** | NO — not executed against `2a80f819` | Runs test_*.py files against candidate |
| 14 | `pptl-ci.yml` | PPTL CI | **APPLICABLE** | NO — not executed against `2a80f819` | CI for PPTL dependency; part of environment verification |
| 15 | `regression.yml` | Regression | **APPLICABLE** | NO — not executed against `2a80f819` | Regression testing against candidate |
| 16 | `doc-lint.yml` | Documentation Lint | **APPLICABLE** | NO — not executed against `2a80f819` | Docs lint; not P8 evidence but hygiene |
| 17 | `doc-lint-pr-scope.yml` | PR-Scoped Documentation Lint | **NOT APPLICABLE to candidate** (PR-scoped, not candidate-scoped) | N/A | Only runs on PR diffs; not a candidate verification workflow |
| 18 | `claim-hygiene.yml` | Claim Hygiene | **APPLICABLE** (hygiene, not evidence) | NO — not executed against `2a80f819` | Claims hygiene check |
| 19 | `ecosystem-audit.yml` | Ecosystem Audit | **APPLICABLE** (dependency hygiene) | NO — not executed against `2a80f819` | Dependency ecosystem audit |
| 20 | `full-repo-audit.yml` | Full Repository Audit | **APPLICABLE** | NO — not executed against `2a80f819` | Comprehensive repo audit |
| 21 | `governance-sweep.yml` | Governance Sweep | **APPLICABLE** (hygiene/control) | NO — not executed against `2a80f819` | Governance sweep; control verification |
| 22 | `ip-hygiene.yml` | IP Hygiene | **APPLICABLE** (hygiene) | NO — not executed against `2a80f819` | IP hygiene check |
| 23 | `propagation-consistency.yml` | Propagation Consistency | **APPLICABLE** (propagation/plasticity) | NO — not executed against `2a80f819` | Propagation consistency check; plasticity evidence |
| 24 | `deploy.yml` | Deployment | **CONDITIONAL** — deployment status, not verification evidence | YES (Vercel deployment check exists for some commits) | Deployment check confirms deployment capability but is NOT scientific/CI closure evidence |

---

## Section 2: Test Suite Inventory (from candidate tree)

There are **7 tracked Python test files** in `experiments/pdmal_pilot/`:

| # | Test file | What it tests | Lines (approx) | P8 relevance | Executed against candidate? |
|---|-----------|---------------|----------------|--------------|-----------------------------|
| 1 | `test_security_controls.py` | FFCR contract, blinding, runtime ceiling, artifact substitution | ~660 | **HIGH** — P8 artifact/security contract | NO — not executed against candidate (only run locally) |
| 2 | `test_analysis.py` | FFCR computation, bootstrap CI, decision rule, exclusion rules | ~300 | **HIGH** — P8 analysis verification | NO — not executed against candidate |
| 3 | `test_durable_retention.py` | Archive round-trip, checksum verification | ~300 | **MEDIUM** — P6 durable custody | NO — not executed against candidate |
| 4 | `test_harness_contract.py` | Harness contract fields, topology fingerprints, stream fingerprints | ~1000 | **HIGH** — P8 harness/artifact contract | NO — not executed against candidate |
| 5 | `test_task_engine.py` | Task engine sequencing, retry, timeout, failure classification | ~1400 | **MEDIUM** — P2/P6a runtime contract | NO — not executed against candidate |
| 6 | `test_dgaf_tgl_adapter.py` | DGAF TGL adapter behavior, consensus determinism | ~200 | **MEDIUM** — P2/P6a, PPTL dependency | NO — not executed against candidate |
| 7 | `test_execution_contract.py` | Execution contract invariants | ~200 | **MEDIUM** — P2 execution contract | NO — not executed against candidate |

**Total test count:** 43 tests (44th skipped due to missing `pptl` dependency in local environment)

---

## Section 3: P8 Checklist Reconciliation

The P8 verification checklist (`P8_VERIFICATION_CHECKLIST.md`) has **21 items**, of which **6 are checked** (artifact contract) and **15 are unchecked** (remaining verification categories).

### Checked items (artifact contract — already verified locally, not candidate-scoped):

| Checklist # | Item | Status | Local verification | Candidate-scoped evidence? |
|-------------|------|---------|-------------------|---------------------------|
| 1 | Analysis implementation matches P7 estimand/estimator | CHECKED | Verified: `analysis.py` consistent with P7 record | NO — local verification only |
| 2 | Artifact schema validates FFCR contract | CHECKED | Verified: artifact schema enforces `ffcr_success`, completeness | NO — local verification only |
| 3 | Runner emits required sidecar fields | CHECKED | Verified: `run_pilot.py` emits runtime_id, seed_id, etc. | NO — local verification only |
| 4 | FFCR contract fields are required and semantically fail-closed | CHECKED | Verified: `harness_contract.py` defines required fields | NO — local verification only |
| 5 | Topology fingerprint definitions are consistent | CHECKED | Verified: 5 topologies, fingerprint constants consistent | NO — local verification only |
| 6 | Run metadata fields are present and non-nullable | CHECKED | Verified: runtime_id, seed_id, condition_id, topology_id, failure_count, ffcr_success, matrix_checksum, artifact_sha | NO — local verification only |

### Unchecked items (candidate-scoped evidence required):

| Checklist # | Item | Required evidence | Corresponds to workflow/test | Status |
|-------------|------|-------------------|------------------------------|--------|
| 7 | Governance CI against exact candidate tree | Run ID, workflow name, pass/fail, retained logs | `governance-ci.yml` | **UNCHECKED** |
| 8 | Python test suite against exact candidate | Test run ID, pass/fail per test, coverage | `python-tests.yml` + 7 test files | **UNCHECKED** |
| 9 | Analysis reproducibility (deterministic output from same inputs) | Reproduction run ID, identical output hash | `pdmal-pre-freeze-runner.yml`, `analysis.py` | **UNCHECKED** |
| 10 | Artifact schema validation in CI | Schema validation run ID, pass/fail | `pdmal-harness-validation.yml` | **UNCHECKED** |
| 11 | FFCR contract enforcement in CI | Contract test run ID, pass/fail | `pdmal-harness-validation.yml`, `test_security_controls.py` | **UNCHECKED** |
| 12 | Truth layer integrity check | Truth layer run ID, pass/fail | `truth-layer.yml`, `truth-layer-tests.yml` | **UNCHECKED** |
| 13 | Epistemic evidence validation | Evidence validation run ID, pass/fail | `epistemic-evidence-validation.yml` | **UNCHECKED** |
| 14 | Blinding operational test | Blinding test run ID, pass/fail, key custody verification | `pdmal-blinding-operational-test.yml` | **UNCHECKED** |
| 15 | Runtime characterization | Characterization run ID, metrics, pass/fail | `pdmal-runtime-characterization.yml` | **UNCHECKED** |
| 16 | P2 runtime verification (applicability decision required) | Per panel: (1) succeeds, (2) justified alternative, or (3) OPEN with conditions | `p2-runtime-verification.yml` | **UNCHECKED — applicability decision pending** |
| 17 | P6a CORS verification (applicability decision required) | Same tripartite choice as P2 | `p6a-cors-verification.yml` | **UNCHECKED — applicability decision pending** |
| 18 | Instrumentation dry-run | Dry-run run ID, data collection path validation | `pdmal-instrumentation-dry-run.yml` | **UNCHECKED** |
| 19 | Pre-authorization security check | Security check run ID, pass/fail | `pdmal-preauth-security.yml` | **UNCHECKED** |
| 20 | PPL/PPtL environment verification | Environment check run ID, dependency versions, pass/fail | `pptl-ci.yml` | **UNCHECKED** |
| 21 | Regression test suite | Regression run ID, pass/fail, any failures | `regression.yml` | **UNCHECKED** |

---

## Section 4: Summary — Gap Between Implemented and Evidenced

| Category | Implemented (code/config exists) | Evidenced (executed against candidate, retained) | Gap |
|----------|----------------------------------|--------------------------------------------------|-----|
| P8 artifact contract (6 checklist items) | YES | NO — local verification only | Must execute Governance CI + python-tests against `2a80f819` |
| P8 analysis verification (items 7-13) | YES — analysis.py, CI workflows exist | NO — none executed against candidate | 7 workflows + test suite need execution |
| P8 blinding (item 14) | YES — blinding_operational_test.py exists | NO — not executed against candidate | Dry-run needed |
| P8 runtime (items 15-17) | YES — characterization + P2/P6a workflows exist | NO — not executed; applicability decisions pending for P2/P6a | Characterization + applicability decisions needed |
| P8 instrumentation (item 18) | YES — dry-run workflow exists | NO — not executed | Dry-run needed |
| P8 security (item 19) | YES — preauth-security.yml exists | NO — not executed | Security check needed |
| P8 environment (item 20) | YES — pptl-ci.yml exists | NO — not executed | Environment check needed |
| P8 regression (item 21) | YES — regression.yml exists | NO — not executed | Regression run needed |
| P6 durable custody | Policy document exists | NO — no archive destination + retrieval/hash proof | Operational proof needed |
| P2/P6a runtime | Workflows exist | NO — not executed; applicability decisions pending | Applicability decision + execution or OPEN with conditions |
| P9 independent verification | Architecture documented | NO — not executed | Must be independent of candidate self-validation |

**Key finding (confirms panel's assessment):** The system has **implemented controls** (code, CI workflows, test suites, policy documents) but has **zero executed candidate-scoped evidence**. Every P8 checklist item from 7-21 is UNCHECKED. A successful CI run against `2a80f819` is necessary evidence, not by itself P8 closure.

---

## Section 5: Hygiene Invariant Verification

Per PR #84 and the panel's framing, the following 6 hygiene invariants should hold. Verified against current documents:

| # | Invariant | Status | Evidence |
|---|-----------|--------|----------|
| 1 | P8 closure claim requires executed candidate-scoped evidence, not implementation presence | **VERIFIED** | P8 checklist item 21 explicitly says: "A successful CI run is necessary evidence, not by itself P8 closure." `PDMAL_CURRENT_CONTROL_STATE.md`: "Candidate implementation work... does not close P8 until the applicable checklist items have executed candidate-scoped evidence." |
| 2 | Historical freeze not misrepresented as current freeze | **VERIFIED** | `CURRENT_STATE.md`: "Historical implementation freeze | HISTORICAL / SUPERSEDED." `PDMAL_CURRENT_CONTROL_STATE.md`: "Historical freeze | HISTORICAL / SUPERSEDED." Both explicitly identify `3510b868...` as superseded. |
| 3 | No silent apparatus redefinition | **VERIFIED** | Both documents contain explicit boundary sections: "Documentation-only commits after that candidate may clarify verification records but do not redefine the apparatus. A substantive protocol, analysis, runner, artifact, or evidence change creates a new candidate cycle." |
| 4 | Historical evidence retains its SHA provenance | **VERIFIED** | `CANDIDATE_MANIFEST_2026-08-21.json` retains 6 historical `4983f44a` references explicitly labeled as provenance. `CURRENT_STATE.md`: "Historical SHA references... remain provenance where they describe what was actually examined; they are not current-state assertions." |
| 5 | N=0 and NOT GRANTED preserved | **VERIFIED** | `CURRENT_STATE.md`: "Empirical data | N = 0" and "Pilot authorization | NOT GRANTED." `PDMAL_CURRENT_CONTROL_STATE.md`: "N = 0. Authorization is NOT GRANTED." `P7_ADJUDICATION_RECORD...md`: "Empirical N: 0. New freeze: NOT CREATED." |
| 6 | P8 checklist self-verification not allowed as closure | **VERIFIED** | `P8_VERIFICATION_CHECKLIST.md`: "Checklist status is not evidence of execution." The checklist tracks what needs evidence; it cannot close itself. |

**All 6 hygiene invariants hold.**

---

## Section 6: Remaining Documentation Issues Found

### Issue 1: CURRENT_STATE.md does NOT reference `P8_VERIFICATION_CHECKLIST.md` — reference was spurious

Earlier draft suggested CURRENT_STATE.md referenced `P8_VERIFICATION_CHECKLIST.md` at line 28. Verification shows no such reference exists in the current HEAD version. The P8 checklist is referenced by `P8_ANALYSIS_LOCK.md` and `PDMAL_CURRENT_CONTROL_STATE.md`, and the checklist itself names `2a80f819` as the exact candidate tree. No stale reference to remove.

`P8_VERIFICATION_CHECKLIST.md` exists at HEAD (blob `080e069dd2b25c48e8a5c52d07170b87c8ac9dc8`) and is unchanged by the integration.

### Issue 2 (RESOLVED earlier): P7 contradiction in CURRENT_STATE.md and PDMAL_CURRENT_CONTROL_STATE.md

Both documents previously stated "P7 scientific specification | ADOPTED" which contradicted the P7 adjudication record (all 11 decisions OPEN / PENDING AUTHORITY ADOPTION). This has been corrected:

- `CURRENT_STATE.md` now reads: "P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN"
- `PDMAL_CURRENT_CONTROL_STATE.md` now reads: "P7 scientific specification | TECHNICALLY ADJUDICATED / PROPOSED AUTHORITATIVE SPECIFICATION / FORMALLY OPEN"
- `P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` created with full 11-decision breakdown
- Both documents now correctly distinguish P7 "technically adjudicated / proposed" from P7 "formally closed / adopted"

### Issue 3: No `P8_CLOSURE_REPORTING_TERMS.md` found at HEAD on 2026-08-24

The panel's review mentioned a possible `P8_CLOSURE_REPORTING_TERMS.md` document. Verification shows no such file exists at HEAD in `docs/governance/`. The P8 closure vocabulary is instead embedded in `P8_VERIFICATION_CHECKLIST.md` (Section: "Closure rule") and `P8_ANALYSIS_LOCK.md` (Section: "Analysis boundaries").

If the panel requires a dedicated closure reporting terms document, it should be created as a new governance artifact. For now, the existing checklist and lock documents sufficiently define the closure vocabulary.

---\n\n*End of Stage 3 verification inventory.*
