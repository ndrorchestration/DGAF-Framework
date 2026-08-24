# Current-State Documentation Hygiene Sweep — 2026-08-24

## Scope

This sweep reconciles the repository's living control documents with the latest candidate-scoped P8 boundary and the current scientific/operational distinctions. It is a documentation reconciliation, not a gate-closing event.

## Corrections incorporated

- P7 scientific specification is recorded as **ADOPTED** in the current control record; adoption is explicitly separated from authorization and empirical execution.
- P8 remains **OPEN / PRE-FREEZE / FAIL-CLOSED**.
- The exact P8 verification candidate is `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`, as named by the current P8 verification checklist.
- Later documentation-only commits do not silently redefine the candidate apparatus.
- Historical SHAs remain historical provenance and are not rewritten merely to satisfy stale-reference searches.
- Implemented controls are distinguished from executed candidate-scoped evidence.
- Freeze, independent verification, authorization, execution, and empirical efficacy remain separate state transitions.

## Hygiene invariants checked

1. No current-state document should claim P8 closure without executed candidate-scoped evidence.
2. No historical freeze should be represented as the corrected-apparatus freeze.
3. No documentation update may silently change the identity of the apparatus under verification.
4. Historical evidence must retain the identity of the SHA/run/deployment actually examined.
5. `N = 0` and `NOT GRANTED` remain authoritative until an authorized empirical pilot occurs.
6. A checklist or implementation change cannot self-authorize predicate closure.

## Follow-up sweep targets

The repository contains dated historical status reports and evidence logs. They should retain their historical snapshots rather than be rewritten as living state. Future hygiene passes should update living documents and cross-reference them to the canonical current-state and candidate-scoped verification records, while preserving historical artifacts unchanged.

## Non-claims

This sweep does **not**:

- close P8;
- create an immutable freeze;
- establish P9 independent verification;
- grant pilot authorization;
- execute empirical trials; or
- establish any empirical efficacy claim.

**Authoritative boundary after this sweep: P8 remains OPEN, the candidate remains pre-freeze, authorization is NOT GRANTED, and empirical N remains 0.**
