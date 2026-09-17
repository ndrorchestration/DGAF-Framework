# Action Admission and Control-Envelope Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement one narrowly scoped, fail-closed Action Admission Record (AAR) enforcement path without creating a parallel governance plane or changing scientific/experimental authority state.

**Architecture:** Reuse DGAF's existing transition, evidence, authorization, provenance, and fail-closed semantics. Add a versioned consequential-action registry, canonical action identity, machine-readable AAR schema, deterministic validators, commit-time revalidation, and one gateway enforcement adapter. Treat receipts, postconditions, recovery, and assurance testing as separate bounded components. Runtime enforcement begins with one reversible, non-scientific action class only.

**Tech Stack:** Python, JSON Schema 2020-12, existing DGAF governance/runtime modules, pytest, GitHub Actions, existing truth-layer/evidence tooling, optional TLA+/formal checks where already supported.

**Spec:** `docs/superpowers/specs/2026-09-17-action-admission-control-envelope-design.md`

## Global Constraints

- PR #747 is specification/research only; runtime code belongs in a separate implementation PR.
- Preserve `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0` High-Assurance semantics unless a separate authoritative transition establishes otherwise.
- Do not redefine P1-P9, Evidence Card claim classes, evidence maturity, validation status, freeze, materialization, primary-analysis authorization, or efficacy.
- `UNKNOWN`, missing, stale, expired, revoked, identity-mismatched, or inconclusive required predicates never become PASS by default.
- Verification, authorization, execution, postcondition verification, and scientific interpretation remain separate state dimensions.
- Pattern reuse never transfers evidence from another project/repository.
- First enforced action class must be narrow, reversible, non-scientific, and explicitly named before enforcement code is admitted.
- Every behavior-changing task follows RED -> GREEN -> exact-scope verification.

---

### Task 1: Consequential Action Registry

**Files:**
- Create: `governance/action_registry.json`
- Create: `governance/action_registry.schema.json`
- Create: `tools/validate_action_registry.py`
- Test: `tests/test_action_registry.py`

**Interfaces:**
- Consumes: existing DGAF governance identity conventions.
- Produces: `ActionRegistry`, registry version, action-class lookup, `requires_aar(action_class) -> bool`, declared risk/reversibility metadata.

- [ ] **Step 1: Write RED tests** covering schema rejection, duplicate action classes, unknown reversibility class, and a fixture action class that explicitly requires AAR enforcement.
- [ ] **Step 2: Run** `pytest tests/test_action_registry.py -v` and confirm the new tests fail for missing implementation.
- [ ] **Step 3: Implement minimal schema/validator** with required fields: `schema_version`, `registry_version`, `action_classes[]`, `action_class`, `consequential`, `aar_required`, `reversibility_class`, `default_policy_ref`, and `status`.
- [ ] **Step 4: Add explicit registry integrity checks** so duplicate classes, missing policy references for enforced actions, and unsupported reversibility values fail closed.
- [ ] **Step 5: Run** `pytest tests/test_action_registry.py -v` and existing governance schema tests.
- [ ] **Step 6: Commit** with `feat(governance): add consequential action registry`.

### Task 2: Canonical Action Identity

**Files:**
- Create: `governance/action_identity.py`
- Test: `tests/test_action_identity.py`

**Interfaces:**
- Consumes: action class, actor, exact target scope, canonical parameters, intended effect, policy identity, material input identities.
- Produces: deterministic canonical representation and SHA-256 `canonical_action_digest`.

- [ ] **Step 1: Write RED tests** proving semantically identical key ordering yields the same digest while any material target/parameter/policy/input change changes the digest.
- [ ] **Step 2: Run** `pytest tests/test_action_identity.py -v` and confirm RED.
- [ ] **Step 3: Implement deterministic canonicalization** using explicit allowed fields, stable JSON serialization, UTF-8, sorted keys, and rejection of unsupported/non-canonical values.
- [ ] **Step 4: Add substitution tests** for changed target, widened scope, changed policy digest, and changed material input revision.
- [ ] **Step 5: Run** the test file and relevant existing canonicalization tests.
- [ ] **Step 6: Commit** with `feat(governance): bind actions to canonical digests`.

### Task 3: Machine-Readable Action Admission Record

**Files:**
- Create: `governance/action_admission_record.schema.json`
- Create: `governance/action_admission.py`
- Test: `tests/test_action_admission_schema.py`

**Interfaces:**
- Consumes: canonical action identity, registry metadata, authority chain, policy identity, evidence/verifier refs, validity, composition, execution, recovery, provenance, residual-risk fields.
- Produces: parsed/validated AAR and typed validation errors; no authorization side effect.

- [ ] **Step 1: Write RED schema tests** for all required domains from `ALIGNMENT_CONSTRAINT_LEDGER.md` and for `additionalProperties: false` at governance-critical object boundaries.
- [ ] **Step 2: Run** `pytest tests/test_action_admission_schema.py -v` and confirm RED.
- [ ] **Step 3: Implement schema** with workflow state enums kept separate from Evidence Card enums.
- [ ] **Step 4: Implement static validator** that rejects missing required identity, invalid policy binding, unsupported recovery class, malformed validity state, and unknown required predicates.
- [ ] **Step 5: Add fixture records** for one valid draft/admissible record and multiple invalid records.
- [ ] **Step 6: Run tests** plus Evidence Card consistency tests to prove no vocabulary collision.
- [ ] **Step 7: Commit** with `feat(governance): add action admission record schema`.

### Task 4: Authority Chain and Attenuation Validator

**Files:**
- Create: `governance/authority_chain.py`
- Test: `tests/test_authority_chain.py`

**Interfaces:**
- Consumes: ordered delegation chain with parent/child scopes, validity, revocation state, actor identities.
- Produces: `VALID`, `INVALID`, or `INCONCLUSIVE` plus typed reasons. `INCONCLUSIVE` is non-authorizing.

- [ ] **Step 1: Write RED tests** for valid narrowing, added capability, widened target, increased budget, extended duration, missing parent provenance, revoked parent, expired delegation, and identity substitution.
- [ ] **Step 2: Run** `pytest tests/test_authority_chain.py -v` and confirm RED.
- [ ] **Step 3: Implement attenuation checks** enforcing `Authority(child) subseteq Authority(parent)` across action classes, target scope, privilege set, budget, duration, and exception rights.
- [ ] **Step 4: Add separation-of-duties hooks** that return `INCONCLUSIVE` when a policy requires distinct principals but independence evidence is absent.
- [ ] **Step 5: Run tests** and mutation-oriented local checks for inverted subset logic.
- [ ] **Step 6: Commit** with `feat(governance): enforce authority attenuation`.

### Task 5: Admissibility and Defeater Evaluation

**Files:**
- Create: `governance/admissibility.py`
- Test: `tests/test_admissibility.py`

**Interfaces:**
- Consumes: AAR, registry entry, policy ref, evidence/verifier results, active validity/defeater events.
- Produces: `ADMISSIBLE`, `REJECTED`, or `INCONCLUSIVE` with machine-readable reasons. No execution.

- [ ] **Step 1: Write RED tests** for missing evidence, verifier unavailable, stale evidence, active blocker, invalidated assumption, policy mismatch, exact success, and unresolved optional/non-blocking findings.
- [ ] **Step 2: Run** `pytest tests/test_admissibility.py -v` and confirm RED.
- [ ] **Step 3: Implement deterministic decision rules** where every mandatory predicate must be satisfied and every blocking defeater must be absent/resolved.
- [ ] **Step 4: Add metamorphic assertions**: removing evidence, aging evidence, weakening provenance, or marking verifier sources correlated cannot make the decision more permissive.
- [ ] **Step 5: Run tests** and existing truth-layer/evidence consistency tests.
- [ ] **Step 6: Commit** with `feat(governance): add fail-closed action admissibility`.

### Task 6: Commit-Time Revalidation

**Files:**
- Create: `governance/commit_revalidation.py`
- Test: `tests/test_commit_revalidation.py`

**Interfaces:**
- Consumes: prepared action digest, authorization, current authority chain, target identity, current policy/environment/tool identity, rate/budget state, active defeaters.
- Produces: `COMMIT_REVALIDATED` or typed rejection/inconclusive result.

- [ ] **Step 1: Write RED tests** for approval replay, expired authorization, revocation race, target drift, action-digest substitution, policy replacement, environment mismatch, quota failure, active defeater, and verifier outage.
- [ ] **Step 2: Run** `pytest tests/test_commit_revalidation.py -v` and confirm RED.
- [ ] **Step 3: Implement the commit barrier** with no external side effect and no fallback from unavailable required dependency to allow.
- [ ] **Step 4: Add single-use/nonce validation hooks** without yet integrating the real gateway.
- [ ] **Step 5: Run tests** and mutation checks for `DENY -> ALLOW`, `UNKNOWN -> PASS`, ignored expiry, and ignored revocation.
- [ ] **Step 6: Commit** with `feat(governance): add commit-time revalidation`.

### Task 7: Receipt, Replay, and Lineage Model

**Files:**
- Create: `governance/action_receipt.schema.json`
- Create: `governance/action_receipt.py`
- Test: `tests/test_action_receipt.py`

**Interfaces:**
- Consumes: committed action identity, execution attempt, target result, authorization identity, parent lineage/supersession refs.
- Produces: append-oriented receipt with digest identity and explicit lineage state.

- [ ] **Step 1: Write RED tests** for receipt tampering, duplicate replay, lineage fork, supersession, revocation, and historical preservation.
- [ ] **Step 2: Run** `pytest tests/test_action_receipt.py -v` and confirm RED.
- [ ] **Step 3: Implement receipt schema/validator** with action digest, authorization id, execution attempt, result identity, receipt digest, parent digest, lineage id, admission authority, optional signature/attestation ref, and revocation/supersession metadata.
- [ ] **Step 4: Ensure hash-chain validity is not treated as authority** by requiring separate admission-authority fields.
- [ ] **Step 5: Run tests** including replay and fork behavior.
- [ ] **Step 6: Commit** with `feat(governance): add action receipt lineage`.

### Task 8: Postcondition and Recovery Coordinator

**Files:**
- Create: `governance/action_recovery.py`
- Test: `tests/test_action_recovery.py`

**Interfaces:**
- Consumes: executed receipt, expected postcondition, reversibility class, recovery policy.
- Produces: closure/recovery state and, where needed, a proposal for a separately governed rollback/compensation action.

- [ ] **Step 1: Write RED tests** for PASS closure, FAIL on reversible action, FAIL on compensatable action, FAIL/INCONCLUSIVE on irreversible action, and delayed/sampled verification.
- [ ] **Step 2: Run** `pytest tests/test_action_recovery.py -v` and confirm RED.
- [ ] **Step 3: Implement state handling** that never erases `EXECUTED` history after postcondition failure.
- [ ] **Step 4: Implement recovery proposal generation** where rollback/compensation is a new governed action, not an implicit side effect.
- [ ] **Step 5: Run tests** and verify compensation is never labeled rollback.
- [ ] **Step 6: Commit** with `feat(governance): add postcondition and recovery states`.

### Task 9: First Gateway Enforcement Adapter

**Files:**
- Modify: exact gateway/runtime file selected after repository inspection for the first chosen reversible non-scientific action class.
- Test: create a dedicated integration test file adjacent to the existing gateway tests.

**Interfaces:**
- Consumes: validated AAR + commit revalidation result.
- Produces: protected side effect only after exact successful gate; otherwise typed denial and no protected effect.

- [ ] **Step 1: Inspect current gateway/action code** and name one existing reversible non-scientific action class; document why it is safe for first enforcement.
- [ ] **Step 2: Write RED integration tests** proving the current gateway permits or lacks the new AAR check, without weakening any existing control.
- [ ] **Step 3: Run the exact integration tests** and capture RED evidence.
- [ ] **Step 4: Add the smallest adapter** that calls registry -> AAR validation -> admissibility -> commit revalidation before the protected effect.
- [ ] **Step 5: Add negative tests** for missing AAR, invalid digest, revoked authority, expired authorization, replay, stale target, and verifier outage.
- [ ] **Step 6: Run the exact integration tests plus full relevant regression suites** and capture exact-head evidence.
- [ ] **Step 7: Commit** with a message naming the action class and enforcement boundary.

### Task 10: Coverage Auditor and CI Gate

**Files:**
- Create: `tools/audit_action_admission_coverage.py`
- Create or modify: a narrowly scoped GitHub Actions workflow/check selected after existing CI inspection.
- Test: `tests/test_action_admission_coverage.py`

**Interfaces:**
- Consumes: versioned action registry and implementation/enforcement declarations.
- Produces: denominator-bound coverage report and fail-closed result for the specifically enforced scope.

- [ ] **Step 1: Write RED tests** for uncovered required action, duplicate/unknown action class, stale registry version, and explicit known-gap reporting.
- [ ] **Step 2: Run** `pytest tests/test_action_admission_coverage.py -v` and confirm RED.
- [ ] **Step 3: Implement auditor** that reports coverage only relative to the exact registry version and never claims global system coverage.
- [ ] **Step 4: Add CI check** that blocks only the declared enforced scope when required AAR metadata is absent or inconsistent.
- [ ] **Step 5: Run local tests and the workflow validation available in repository tooling.**
- [ ] **Step 6: Commit** with `ci(governance): audit action admission coverage`.

### Task 11: Governance Mutation and Metamorphic Verification

**Files:**
- Extend existing Discovery Harness/governance mutation fixtures where compatible; otherwise create narrowly scoped AAR mutation tests under `tests/` without creating a second harness.

**Interfaces:**
- Consumes: registry, AAR validator, authority validator, admissibility, commit revalidation.
- Produces: evidence that dangerous semantic mutations are killed and monotonicity properties hold.

- [ ] **Step 1: Add dangerous mutants** for `DENY -> ALLOW`, `UNKNOWN -> PASS`, expiry/revocation bypass, digest comparison bypass, delegation widening, required-step omission/reorder, duplicated evidence counted as independent, and policy substitution.
- [ ] **Step 2: Execute the mutation/meta-tests** and record which mutants survive.
- [ ] **Step 3: Add/fix tests until every high-severity targeted mutant is killed or explicitly recorded as an unresolved gap.**
- [ ] **Step 4: Run metamorphic relations** proving weaker/staler/correlated evidence never increases authority/admissibility.
- [ ] **Step 5: Commit** with `test(governance): challenge action admission controls`.

### Task 12: Exact-Scope Evidence and Documentation Reconciliation

**Files:**
- Modify: `docs/governance/ALIGNMENT_CONSTRAINT_LEDGER.md`
- Modify: `docs/research/CONTROL_ENVELOPE_PATTERN_ADOPTION_MATRIX.md`
- Modify only the authoritative current-state surfaces required by existing repository convention after implementation evidence exists.

**Interfaces:**
- Consumes: exact implementation SHA, workflow runs, runtime/integration evidence, unresolved gaps.
- Produces: implementation-status reconciliation without scientific or High-Assurance overclaim.

- [ ] **Step 1: Bind every implementation claim to exact SHA/run/test scope.**
- [ ] **Step 2: Change only the implemented pattern rows from `NEW_IMPLEMENTATION_REQUIRED`/specified-only to exact bounded implementation status.**
- [ ] **Step 3: Keep uncovered action classes and residual risks explicit.**
- [ ] **Step 4: Confirm no documentation claims P1-P9 closure, scientific-N increase, efficacy, independent validation, or complete alignment from this work.**
- [ ] **Step 5: Run doc lint, claim hygiene, truth-layer, governance, and relevant regression checks on the exact final head.**
- [ ] **Step 6: Commit the reconciliation and request review.**

## Self-Review

- Spec coverage: all approved design requirements map to Tasks 1-12.
- Vocabulary: workflow lifecycle remains separate from Evidence Card claim/evidence/validation dimensions.
- Scope: only one first action class is enforced; expansion is subsequent work.
- Recovery: rollback, compensation, and irreversibility are separate.
- Composition: no transitive authorization assumption.
- Authority: delegation can only preserve/reduce scope.
- Evidence: pattern reuse does not transfer evidence.
- Runtime: no enforcement claim exists before Task 9 exact-scope evidence.
- Scientific state: unchanged by this implementation unless a separate authorized scientific transition occurs.
