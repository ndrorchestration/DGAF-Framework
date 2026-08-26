# DGAF-Framework — Baseline Audit Record — 2026-08-26

**Purpose:** Establish a single primary-source baseline before further repository or governance modifications. This record captures the verified state available through the GitHub API and explicitly records information that could not be independently retrieved.

## 1. Repository identity

- Repository: `ndrorchestration/DGAF-Framework`
- Default branch: `main`
- **Current main SHA:** `6ace79f0883da7829263b975a10a8877c270109a`
- Main commit message: `ci: gate unexpected registry divergence while permitting documented migration`
- Current main status exposed through the available GitHub status endpoint: `success`
- Observed Vercel status on current main: `success`

## 2. Experimental candidate identity

- **Exact P8 verification candidate:** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`
- Candidate remains the P8 binding and is not redefined by later documentation or unrelated mainline changes.
- The current main SHA is newer than the historical documentation references to `39c138bb29697a561b49ef206c9f9a185e8a9c7b`; therefore those references are now historical metadata unless explicitly updated.
- Current main contains at least one substantive CI/control change after the `39c138bb...` documentation snapshot: registry-consistency migration gating in `scripts/registry_consistency_check.py`.

## 3. Epistemic / experimental boundary

- PDMAL state: **PRE-FREEZE**
- Pilot authorization: **NOT GRANTED**
- Experimental N: **0**
- New freeze: **NOT CREATED**
- P8: **OPEN / FAIL-CLOSED**
- P9 independent verification: **NOT EXECUTED**
- Historical freeze `3510b86889cd341f7a7cf9ab684fd37b2fafd758`: provenance only / superseded

## 4. P7 state

The current P7 traceability record and PDMAL control record identify P7 as **TECHNICALLY ADJUDICATED / FORMALLY OPEN / PENDING AUTHORITY ADOPTION**. The primary contrast is recorded as DGAF versus null, but formal adoption of all 11 P7 decisions is not evidenced by the current control records.

A conflicting stale statement exists in `docs/PROJECT_STATUS.md`, which currently says P7 primary scientific adjudication is adopted. This discrepancy is recorded as a documentation-hygiene issue requiring reconciliation; it is not resolved by this baseline.

## 5. Required P8 candidate evidence

The current P8 checklist remains fail-closed. Candidate-scoped evidence is still unchecked for:

- Governance CI execution against `2a80f819...`
- P8 analysis tests in that execution
- artifact-schema/security tests
- compilation
- retained run identity, URL, SHA, ref, and event
- inspected job logs
- executed-tree reconciliation
- environment fingerprint
- deterministic topology fingerprints
- seed/RNG separation and trial ordering
- durable retention
- independent retrieval
- retrieval hash verification
- blinding-custody evidence

## 6. Pull-request baseline

### PR #85

- State: open
- Head: `0760f6a553ea5f41cccf8ba516e06ea311287d7c`
- Base: `main` at recorded PR base `284e6406b11c7e850ef477488de13a55536eb6a2`
- Scope: 5 documentation/publication files, `+577/-0`
- Purpose: publication/provenance spine
- Current API mergeability: previously observed as mergeable in current metadata; final merge decision requires current checks and terminology review.

### PR #74

- State: open
- Scope: dependency maintenance in PDMAL pilot/topology requirements
- Declared upgrades: setuptools `82.0.0 -> 83.0.0`; pytest `8.4.1 -> 9.0.3` in the identified groups
- Current API mergeability: observed as mergeable in current metadata; candidate-scoped reproducibility/lock validation remains required.

### PR #42

- State: open
- Head: `2a1c90d8098b3fd9449bbf2f17a20cf43b761fef`
- Scope: one additive STASIS draft document, `+667/-0`
- Epistemic boundary: project-local draft; not canonical authority; evidence ladder preserved in PR body.

## 7. Branch protection / required checks

The direct branch-protection endpoint is **not currently retrievable through the available GitHub integration** (403 from the branch-protection API). Therefore:

- Required-check configuration: **UNVERIFIED at baseline**.
- Previously reported dangling context: `pptl pytest — governance`.
- Manual repository-owner confirmation is required before recording branch-protection closure.
- No cosmetic workflow should be created solely to satisfy an unverified/stale context.

## 8. Observed workflow surface

The `main` branch currently exposes governance/reproducibility workflows including:

- `claim-hygiene.yml`
- `deploy.yml`
- `doc-lint-pr-scope.yml`
- `doc-lint.yml`
- `ecosystem-audit.yml`
- `epistemic-evidence-validation.yml`
- `full-repo-audit.yml`
- `governance-ci.yml`
- `governance-sweep.yml`
- `ip-hygiene.yml`
- `p2-runtime-verification.yml`
- `p6a-cors-verification.yml`
- `pdmal-blinding-operational-test.yml`

The Stage 3 inventory records a total of 24 workflow files at the P8 candidate tree. The full emitted-check context set has not been independently enumerated in this baseline because the available integration does not expose the full branch-protection/run-context surface.

## 9. Known live issues requiring reconciliation

- **Issue #79:** candidate runtime verification remains blocked by Vercel authentication-path constraints; it explicitly prohibits substitution of historical deployment evidence and keeps pilot/freeze closed.
- **Issue #80:** primary scientific contrast is selected as DGAF versus null, but 11 remaining P7 fields still require explicit recording/adoption before P7 can close.

## 10. Documentation provenance observations

Current authoritative candidate documents still contain older `CURRENT_STATE`/control metadata applying to `39c138bb...`. The current main SHA is now `6ace79f...`; therefore any current-state document whose front matter still identifies `39c138bb...` requires a targeted provenance reconciliation rather than silent global replacement.

The authoritative P8 candidate remains `2a80f819...`.

## 11. Primary-source precedence rule

When records disagree, use this precedence:

1. GitHub live objects, current checks, and exact fetched git objects.
2. Repository files at the exact SHA being evaluated.
3. Retained evidence artifacts tied to that SHA/run/deployment.
4. Notion operational records.
5. Previous reports, summaries, or conversation handoffs.

Secondary summaries must never override a current primary-source object.

## 12. Exit criteria for Phase 0

- [x] Current main SHA captured.
- [x] Exact P8 candidate captured.
- [x] Current epistemic boundary captured.
- [x] PR #85/#74/#42 identities and scope captured.
- [x] Issues #79/#80 captured as open control items.
- [x] Branch-protection retrieval limitation explicitly recorded.
- [x] Documentation SHA discrepancy identified rather than silently rewritten.
- [ ] Full required-check configuration independently verified through an authorized GitHub surface.

**Baseline conclusion:** Repository integrity and experimental governance remain **OPEN / FAIL-CLOSED**. No freeze or authorization is created by this record. The baseline exists to prevent further stale-state propagation and to anchor all subsequent candidate-scoped verification to the exact intended evidence target.
