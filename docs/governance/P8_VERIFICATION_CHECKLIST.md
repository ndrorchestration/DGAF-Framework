# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Current `main`:** documentation/evidence lineage; do not treat the branch tip as experimental apparatus identity.  
**Current post-#151 apparatus candidate:** `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`  
**Candidate designation/control commit:** `02c146d1e0cdc423948ac0dfa11e98f812edfb44`  
**Candidate ref:** `experimental-candidate/2026-08-30-post151`  
**Historical experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Prior pre-remediation candidate:** `c6157158bf0ee4840e99a381a4b99bd2febe2302` (historical/superseded)

This checklist distinguishes implemented controls from executed verification evidence. Historical candidates and historical verifier runs remain provenance only. The post-#151 candidate must receive fresh candidate-scoped evidence before P8 closure.

## Candidate identity reconciliation

- [x] `2a80f819…` / `303f4424…` discrepancy reconciled as ancestry/role distinction.
- [x] `303f4424…` retained as prior engineering/production and P2/P6a evidence boundary.
- [x] `c6157158…` retained as superseded pre-remediation candidate.
- [x] `05fa286…` explicitly designated as the post-#151 apparatus candidate.
- [x] `02c146d1…` recorded as the designation/control commit and kept distinct from apparatus identity.
- [ ] New candidate reaches a verified freeze state.

## TGL/P-35 contract prerequisite

- [x] PR #151 fail-closed remediation merged and establishes the new apparatus cycle.
- [ ] Complete candidate-scoped verification of the resulting TGL/P-35 contract.
- [ ] Premise-hook injection exercised by regression tests for the current candidate.
- [ ] Fail-closed exception containment exercised by regression tests for the current candidate.
- [ ] `PASS/WARN/SKIP/ESCALATE/KILL` reduction semantics explicitly tested for the current candidate.
- [ ] Unwired required-gate `SKIP` distinguished from dependency-caused or intentionally non-applicable `SKIP`.
- [ ] Final audit seal proven to represent exactly the authoritative returned audit state.
- [ ] Current-candidate CI run, SHA, ref, event, logs, and artifacts retained.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Numeric Boolean values are rejected where integer identifiers/counts are required.
- [x] Corrective tests cover artifact/document identity, matrix uniqueness, blinded balance, retention integrity, unblinding bijection, bootstrap invariants, and recovery-state semantics.
- [ ] Fresh current-candidate execution evidence exists for `05fa286…`.

## Repository-native evaluation evidence

Historical repository-native evaluator runs remain supportive synthetic evidence only. They do not establish current candidate efficacy or close P8.

## Current candidate-tree CI evidence

- [ ] Governance CI executed against `05fa286…` or an exact descendant with unchanged executable apparatus and explicit provenance.
- [ ] P8 analysis tests passed in that exact candidate execution.
- [ ] P8 artifact-schema/security tests passed in that exact candidate execution.
- [ ] Compilation passed in that exact candidate execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Historical evidence boundaries

- [x] Historical E2b verification retained as provenance for its recorded execution.
- [ ] Current-candidate E2b applicability re-verified after post-#151 workflow-binding changes.
- [x] Prior P2 evidence retained as exact evidence for `303f4424…` only.
- [x] Prior P6a evidence retained as exact evidence for `303f4424…` only.

## Runtime verification

- [x] Prior authenticated P2 five-case POST matrix: run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`.
- [ ] Fresh authenticated P2 five-case POST matrix executed against `05fa286…` and its exact deployment.
- [x] Prior authenticated P6a four-case CORS matrix: run `33302495240`, artifact `9729387603`, digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`; candidate `303f4424…`.
- [ ] Fresh authenticated P6a four-case CORS matrix executed against `05fa286…` and its exact deployment.

## Reproducibility and provenance

- [ ] Executed candidate-tree identity reconciled with all P8 bindings for `05fa286…`.
- [ ] Canonical protocol blob SHA bound to the eventual frozen candidate identity.
- [ ] Current candidate-bound E2b/M6 toolchain evidence captured and retained.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for `05fa286…`.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody and negative state

- [ ] Candidate-scoped CI logs/artifacts retained at a durable location.
- [ ] Retained candidate artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.
- [ ] M6 machine-retained negative-state artifact proves N=0, no authorization, no pilot, and no unblinding for the current candidate verification run.

## Closure rule

P8 remains open until every applicable unchecked item has current candidate-scoped evidence. Historical or synthetic evidence cannot substitute for current-candidate verification.

**Current apparatus candidate:** `05fa286…`; designation/control commit `02c146d1…`; prior P2/P6a evidence remains scoped to `303f4424…`; P3–P6 evidence-gated; P8 OPEN / FAIL-CLOSED; P9 NOT EXECUTED; no freeze; no authorization; empirical N = 0.
