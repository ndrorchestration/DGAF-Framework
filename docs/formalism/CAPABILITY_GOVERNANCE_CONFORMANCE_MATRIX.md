# DGAF Capability Governance Conformance Matrix

> **Status:** INITIAL / PROSPECTIVE  
> **Purpose:** Bind protocol invariants to executable evidence.

| Invariant | Core requirement | Current evidence | Status |
| --- | --- | --- | --- |
| G1 | No protected side effect without authorization | bounded PEP blocks protected dispatch without active authorization | TESTED-SLICE |
| G2 | Authorization precedes execution | bounded PEP checks authority before dispatcher invocation | TESTED-SLICE |
| G3 | Authorization is scoped | bounded PEP rejects adjacent-resource scope substitution | TESTED-SLICE |
| G4 | No self-approval of exceptions | bounded PEP rejects requester == approver | TESTED-SLICE |
| G5 | Verification != authorization | executable verification/authorization separation tests | TESTED-SLICE |
| G6 | Authorization != execution | execution-state + provider-receipt separation tests | TESTED-SLICE |
| G7 | Material evidence preserves provenance | capability audit schema requires evidence/verifier linkage fields | TESTED-SLICE |
| G8 | Failed required verifier blocks transition | bounded PEP blocks required verifier failure before dispatch | TESTED-SLICE |
| G9 | Revocation blocks future use | executable authorization-status test | TESTED-SLICE |
| G10 | Audit survives success/failure | capability audit schema accepts explicit failed execution records | TESTED-SLICE |
| G11 | Delegation cannot widen authority | executable capability/resource/budget attenuation tests | TESTED-SLICE |
| G12 | Approval is action-digest-bound | canonicalization + substitution + replay-consumption tests | TESTED-SLICE |
| G13 | Commit-time volatile predicates revalidated | executable missing/changed state-guard tests | TESTED-SLICE |
| G14 | Authorization not automatically compositional | workflow composition + sensitive-egress tests | TESTED-SLICE |
| G15 | Postcondition failure does not erase execution | partial/postcondition recovery-state tests | TESTED-SLICE |
| G16 | Weaker evidence cannot increase authority | executable evidence-strength monotonicity tests | TESTED-SLICE |

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

## Bounded reference transaction

`tests/test_capability_reference_transaction.py` now exercises the composed control path across canonical action binding, PEP admission/refusal, dispatcher invocation, execution receipts, postconditions, reconciliation state, and capability audit events. The safe real-bridge integration uses only the read-only `status` action; protected-side-effect paths use injected synthetic dispatch and do not execute operator materialization.

At implementation checkpoint `b04b5a4cef8f`, the relevant local compatibility slice is **91/91 PASS**.

`tests/test_capability_transport_independence.py` additionally validates a second non-MCP mock HTTP/OpenAPI-style path: the alternate manifest conforms to the same capability schema, governed fields for `dgaf.local.status` remain identical across MCP and REST-style adapters, the safe real bridge returns the same bounded status semantics, and unadmitted HTTP routes/extra request fields fail closed.

A row marked TESTED-SLICE means only that the named local test passed for the represented case. It does not establish universal correctness, production assurance, or independent verification.
