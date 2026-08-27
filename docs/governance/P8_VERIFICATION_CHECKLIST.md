# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED
**Current `main`:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
**Current verification boundary:** `ac8ea26…`
**Historical E2b closure:** `d299dd1…` / run `33047380487`

This checklist distinguishes implemented controls from executed verification evidence. Historical candidates and historical verifier runs remain provenance only and must not be substituted for the current verification boundary.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Numeric Boolean values are rejected where integer identifiers/counts are required.
- [x] Artifact/document identity, matrix uniqueness, exact 4×45 blinded balance, durable retention integrity, unblinding bijection, bootstrap uniqueness/finite-input invariants, and recovery-state semantics are covered by corrective tests.

## Current-tree CI evidence

- [ ] Governance CI executed against current verification boundary `ac8ea26…`.
- [ ] P8 analysis tests passed in that execution.
- [ ] P8 artifact-schema/security tests passed in that execution.
- [ ] Compilation passed in that execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Historical E2b evidence

- [x] E2b exact-tree verification completed for `d299dd152…` via run `33047380487`.
- [x] Artifact `9636185725` retained; digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.
- [ ] Current-tree applicability re-verified after the `ac8ea26…` workflow-binding change.

## Runtime verification

- [ ] Authenticated P2 five-case POST matrix executed against exact current candidate/deployment identity.
- [ ] Authenticated P6a four-case CORS matrix executed against the same identity.

## Reproducibility and provenance

- [ ] Executed-tree identity reconciled with all P8 bindings.
- [ ] Canonical protocol blob SHA bound to the current verification boundary.
- [ ] Current E2b/M6 toolchain evidence captured and retained.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for the current candidate.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody and negative state

- [ ] CI logs/artifacts retained at a durable location.
- [ ] Retained artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.
- [ ] M6 machine-retained negative-state artifact proves N=0, no authorization, no pilot, and no unblinding for the current verification run.

## Closure rule

P8 remains open until every applicable unchecked item has current candidate-scoped evidence. A passing implementation review or successful workflow configuration change is not equivalent to executed verification.

**No freeze. No authorization. No unblinding. Empirical N = 0.**
