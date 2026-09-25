# DGAF Capability Governance Conformance Matrix

> **Status:** INITIAL / PROSPECTIVE  
> **Purpose:** Bind protocol invariants to executable evidence.

| Invariant | Core requirement | Current evidence | Status |
|---|---|---|---|
| G1 | No protected side effect without authorization | Schema/design only | OPEN |
| G2 | Authorization precedes execution | Transition spec | OPEN |
| G3 | Authorization is scoped | authorization schema | PARTIAL |
| G4 | No self-approval of exceptions | transition spec | OPEN |
| G5 | Verification != authorization | transition spec | PARTIAL |
| G6 | Authorization != execution | receipt schema | PARTIAL |
| G7 | Material evidence preserves provenance | audit fields/design | PARTIAL |
| G8 | Failed required verifier blocks transition | transition spec | OPEN |
| G9 | Revocation blocks future use | executable authorization-status test | TESTED-SLICE |
| G10 | Audit survives success/failure | receipt/reconciliation schemas | PARTIAL |
| G11 | Delegation cannot widen authority | executable capability/resource/budget attenuation tests | TESTED-SLICE |
| G12 | Approval is action-digest-bound | canonicalization + substitution + replay-consumption tests | TESTED-SLICE |
| G13 | Commit-time volatile predicates revalidated | executable missing/changed state-guard tests | TESTED-SLICE |
| G14 | Authorization not automatically compositional | workflow schema + threat T7 | PARTIAL |
| G15 | Postcondition failure does not erase execution | receipt/reconciliation schema | PARTIAL |
| G16 | Weaker evidence cannot increase authority | transition spec | OPEN |
## Existing executable evidence

`tests/test_capability_governance_contracts.py` currently verifies:
- all four bounded local MCP capability manifests validate;
- five core schemas are themselves valid Draft 2020-12 JSON Schemas;
- canonical action digest is deterministic;
- object key ordering does not alter digest;
- material recipient substitution changes digest;
- non-finite JSON values fail canonicalization;
- malformed action digests are rejected by authorization schema;
- EXECUTION_OUTCOME_UNKNOWN is representable without pretending success/failure.

These tests establish only the tested structural properties.

## Next conformance tests

Highest-priority additions:
1. delegation attenuation evaluator: T1 / G11;
2. effective-authority intersection: T2;
3. approval consumption/replay protection: T4;
4. commit-state guard mutation: T6 / G13;
5. revocation-at-commit: T10 / G9;
6. workflow sensitive-read -> external-write denial: T7 / G14;
7. policy self-broadening denial: T11 / G4;
8. partial execution + compensation trace: T13 / G15;
9. provider receipt != postcondition: T14 / G6/G15;
10. capability visibility distinct from invocation: T15.

## Evidence boundary

A row marked TESTED-SLICE means only that the named local test passed for the represented case. It does not establish universal correctness, production assurance, or independent verification.
