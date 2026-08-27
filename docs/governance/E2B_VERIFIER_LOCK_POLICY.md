# E2b Verifier-Policy Dependency Lock

**Status:** Candidate closure implementation; independent verification required before E2b is declared CLOSED.

## Bound inputs

- Source policy: `requirements-epistemic.txt`
- Source SHA-256: `3bcac33804dbadca931bf15667b4eb2eade42c0708ed9d0e0831fd842af869fc`
- Lock: `requirements-epistemic.lock`
- Lock SHA-256: `de37996c4a83c4bf23bfbb42810d57dfbb1f11a20c2536a945540221f3be9ae0`
- Verification workflow: `.github/workflows/e2b-verifier-lock.yml`
- Python target: 3.12

## Closure semantics

E2b is satisfied only when CI verifies all of the following on the same tree:

1. `requirements-epistemic.txt` matches its bound SHA-256.
2. `requirements-epistemic.lock` matches its bound SHA-256.
3. The lock contains exact versions with artifact hashes and installs successfully with `pip --require-hashes`.
4. The verifier workflow is itself present in the same tree and runs successfully.

The workflow computes these fingerprints from the committed files; it does not rely on a generated value from an external or mutable environment.

## Non-recursion rule

This lock governs the verifier-policy dependency surface only. It does not govern the PDMAL experimental candidate, freeze, authorization, unblinding, or empirical data. Changes to the experimental environment must not be silently absorbed into this verifier lock.

**E2b state:** OPEN / CANDIDATE IMPLEMENTATION PENDING INDEPENDENT VERIFICATION.
