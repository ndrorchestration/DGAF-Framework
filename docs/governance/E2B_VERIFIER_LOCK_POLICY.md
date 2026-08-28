# E2b Verifier-Policy Dependency Lock

**Status:** Candidate closure implementation; independent verification required before E2b is declared CLOSED.
**Execution boundary note:** This branch is a fresh exact-tree verification candidate rooted at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`; the policy-only amendment does not alter the PDMAL trial implementation.

## Bound inputs

- Source policy: `requirements-epistemic.txt`
- Source SHA-256: `3bcac33804dbadca931bf15667b4eb2eade42c0708ed9d0e0831fd842af869fc`
- Lock: `requirements-epistemic.lock`
- Lock digest: computed and emitted by CI on the exact committed tree
- Verification workflow: `.github/workflows/e2b-verifier-lock.yml`
- Python target: 3.12

## Closure semantics

E2b is satisfied only when CI verifies all of the following on the same tree:

1. `requirements-epistemic.txt` matches its bound SHA-256.
2. `requirements-epistemic.lock` contains exact versions with artifact hashes and installs successfully with `pip --require-hashes`.
3. CI emits the lock SHA-256 and a deterministic E2b dependency fingerprint derived from the source, lock, and workflow files on that exact tree.
4. The verifier workflow is itself present in the same tree and runs successfully.

The workflow derives the lock and combined fingerprints from the committed files. No mutable external state is trusted for the identity of the dependency surface.

## Non-recursion rule

This lock governs the verifier-policy dependency surface only. It does not govern the PDMAL experimental candidate, freeze, authorization, unblinding, or empirical data. Changes to the experimental environment must not be silently absorbed into this verifier lock.

**E2b state:** OPEN / CANDIDATE IMPLEMENTATION PENDING INDEPENDENT VERIFICATION.
