# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED
**Exact candidate tree for verification:** `e6beeb66335e1b50a239697badab22dab50eb5ba`
**Current `main`:** `bc325486a2986256532e58dccf39a155ed75a72a`

This checklist distinguishes implemented controls from executed verification evidence. Historical candidate references (`2a80f819...`, `94fb6fd...`, PR #77 `b25a914c...`, and pre-correction P8 binding `b681c87...`) are provenance only and must not be substituted for the exact current candidate.

The current `main` contains later documentation/governance synchronization successors. They do not redefine the executable candidate unless a substantive executable/schema/workflow/dependency/protocol/analysis change is identified. Such a change requires candidate transition and affected-predicate re-verification.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Numeric Boolean values are rejected where integer identifiers/counts are required.
- [x] Artifact/document identity, matrix uniqueness, exact 4×45 blinded balance, durable retention integrity, unblinding bijection, bootstrap uniqueness/finite-input invariants, and recovery-state semantics are covered by corrective tests.

## Candidate CI evidence

- [ ] Governance CI executed against exact candidate `e6beeb...`.
- [ ] P8 analysis tests passed in that execution.
- [ ] P8 artifact-schema/security tests passed in that execution.
- [ ] Compilation passed in that execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Runtime verification

- [ ] Authenticated P2 five-case POST matrix executed against the exact candidate/deployment identity.
- [ ] Authenticated P6a four-case CORS matrix executed against the same identity.

## Reproducibility and provenance

- [ ] Executed-tree identity reconciled with all P8 bindings.
- [ ] Canonical protocol blob SHA bound to the current candidate specification.
- [ ] E2b verification-toolchain fingerprint captured and retained.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for the candidate.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody and negative state

- [ ] CI logs/artifacts retained at a durable location.
- [ ] Retained artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.
- [ ] M6 machine-retained negative-state artifact proves N=0, no authorization, no pilot, and no unblinding for the candidate/run.

## Closure rule

P8 remains open until every applicable unchecked item has candidate-scoped evidence. A passing implementation review or successful workflow configuration change is not equivalent to executed verification.

**No freeze. No authorization. No unblinding. Empirical N = 0.**
