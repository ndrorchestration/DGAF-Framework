# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED
**Current `main`:** resolve the `main` branch directly; documentation lineage is not apparatus identity.
**Experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
**Latest repository-native evaluation evidence:** `061286b1…` / Governance CI `33162492796`

This checklist distinguishes implemented controls from executed verification evidence. Historical candidates and historical verifier runs remain provenance only and must not be substituted for the experimental verification boundary.

## TGL/P-35 contract prerequisite

- [ ] TGL/P-35 contract blocker resolved by an isolated remediation candidate.
- [ ] Established P-35 constructor and `evaluate(..., check_fn=...)` contract restored and tested.
- [ ] Premise-hook injection exercised by regression tests.
- [ ] Fail-closed exception containment exercised by regression tests.
- [ ] `PASS/WARN/SKIP/ESCALATE/KILL` reduction semantics explicitly tested.
- [ ] Unwired required-gate `SKIP` distinguished from dependency-caused or intentionally non-applicable `SKIP`.
- [ ] Final audit seal proven to represent exactly the authoritative returned audit state.
- [ ] Exact remediation-head CI run, SHA, ref, event, logs, and artifacts retained.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Numeric Boolean values are rejected where integer identifiers/counts are required.
- [x] Artifact/document identity, matrix uniqueness, exact 4×45 blinded balance, durable retention integrity, unblinding bijection, bootstrap uniqueness/finite-input invariants, and recovery-state semantics are covered by corrective tests.

## Repository-native evaluation evidence

- [x] Issue #32 deterministic slices executed and retained on exact tree `061286b1…` via Governance CI `33162492796`.
- [x] Issue #64 deterministic evaluation-integrity fixture suite executed and retained on exact tree `061286b1…` via Governance CI `33162492796`.
- [x] These results are synthetic, repository-authored evaluator-mechanism evidence only; they are not candidate-bound experimental efficacy evidence and do not close P8.

## Current candidate-tree CI evidence

- [ ] Governance CI executed against the experimental verification boundary `ac8ea267…`.
- [ ] P8 analysis tests passed in that exact candidate execution.
- [ ] P8 artifact-schema/security tests passed in that exact candidate execution.
- [ ] Compilation passed in that exact candidate execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained for that candidate execution.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Historical E2b evidence

- [x] Historical E2b exact-tree verification completed for `d299dd152…` via run `33047380487`.
- [x] Historical artifact retained with its recorded digest.
- [ ] Current candidate-bound E2b applicability re-verified after the later workflow-binding changes.

## Runtime verification

- [ ] Authenticated P2 five-case POST matrix executed against exact current candidate/deployment identity.
- [x] Authenticated P6a four-case CORS matrix executed against the same production candidate/deployment boundary; run `33302495240`, artifact `9729387603`, digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`.

## Reproducibility and provenance

- [ ] Executed candidate-tree identity reconciled with all P8 bindings.
- [ ] Canonical protocol blob SHA bound to the eventual frozen candidate identity.
- [ ] Current candidate-bound E2b/M6 toolchain evidence captured and retained.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for the current candidate.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody and negative state

- [ ] Candidate-scoped CI logs/artifacts retained at a durable location.
- [ ] Retained candidate artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.
- [ ] M6 machine-retained negative-state artifact proves N=0, no authorization, no pilot, and no unblinding for the current candidate verification run.

## Closure rule

P8 remains open until every applicable unchecked item has current candidate-scoped evidence. Repository-native synthetic evaluator verification is supportive evidence only and does not itself establish candidate efficacy or close P8.

**P6a runtime evidence verified. P2 remains unverified. No freeze. No authorization. No unblinding. Empirical N = 0.**
