# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED
**Exact candidate tree for verification:** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`
**Documentation update:** `c6f4bbd2e02dc2d6e35b43e5c99a551452378db2` (documentation-only; does not redefine the candidate apparatus)

This checklist distinguishes implemented controls from executed verification evidence. Historical candidate references (`94fb6fd...`, PR #77 `b25a914c...`, and pre-correction P8 binding `b681c87...`) are provenance only and must not be substituted for the exact candidate tree above.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.

## Candidate CI evidence

- [ ] Governance CI executed against exact candidate `2a80f819...`.
- [ ] P8 analysis tests passed in that execution.
- [ ] P8 artifact-schema/security tests passed in that execution.
- [ ] Compilation passed in that execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Reproducibility and provenance

- [ ] Executed-tree identity reconciled with all P8 bindings.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for the candidate.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody

- [ ] CI logs/artifacts retained at a durable location.
- [ ] Retained artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.

## Closure rule

P8 remains open until every applicable unchecked item has candidate-scoped evidence. A passing implementation review or successful workflow configuration change is not equivalent to executed verification.

**No freeze. No authorization. No unblinding. Empirical N = 0.**
