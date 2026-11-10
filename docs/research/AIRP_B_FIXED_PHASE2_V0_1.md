# AIRP Phase 2 — B-FIXED source-locked synthetic baseline (research only)

**Status:** isolated draft implementation; not a scientific experiment, independent validation, accepted DGAF implementation, or authorization mechanism.

**Protected-main source anchor:** 1a95b94332dffb404c5a3ce026d70781a8c10b90. Source locks are checked against local Git blob content at initialization; blob identifiers are not authenticity signatures. **Research branch:** research/airp-b-fixed-phase2-20261110.

## Minimum implementation

- scripts/airp_b_fixed_workflow.py — deterministic predeclared plan runner, with in-process versioned graph copies; delegates to the existing ClaimGraph validator, Evidence Gate and read-only attribution query.
- tests/test_airp_b_fixed_workflow.py — synthetic positive/negative and replay/branch safety tests.
- No new ClaimGraph, evidence store, policy or authority plane, external effects, persistent database, adaptive agent, model invocation, or C-INSTRUMENT interface.

## Protected-main source locks

| Path | Git blob SHA-1 (source identity only) |
| --- | --- |
| docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json | ebea3130335c50716352e7aa6c749069bbd8b832 |
| docs/research/STRUCTURAL_EPISTEMICS_CLAIM_RECORD_SCHEMA.json | bed1d9a57ef25a94a70379b9af99d2d0fcbb54a6 |
| docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json | 77f097d261289d9f595e8c4ae465b97d5b3ce64a |
| scripts/validate_structural_epistemics_claim_graph.py | d24e2798e305f76beca5b9ecfcb91ba8fa6ba847 |
| scripts/claimgraph_attribution_query.py | e3ed75a9e3a0eb6b4a01754894df32bf10985b2a |
| components/evidence_gate.py | 5878aa314813cd0770754c3c6fe14311ee8b117c |

## Fixed workflow operations

| Operation | Underlying DGAF reuse | Baseline behavior and explicit limit |
| --- | --- | --- |
| add_claim | Existing ClaimRecord schema/validator | Copy synthetic claim, reset PROPOSED/NOT_VERIFIED/NONE, validate and stage memory-only revision |
| attach_evidence | Existing Evidence Gate and ClaimGraph schema | SHA-256 check synthetic bytes for exact reference target; add DERIVATION node and SUPPORTS relation only if gate and structural checks pass; admission does not prove producer identity |
| challenge | Existing contradiction/defeater validator | Link existing synthetic COUNTEREVIDENCE, trigger defeater and set CHALLENGED; no truth decision |
| fork | Existing graph snapshots and validator | Copy exact branch version into a named in-process branch, not external rollback or durable storage |
| inspect | Existing ClaimGraph and attribution query | Return synthetic snapshot, fingerprint and optional caller-supplied attribution classifications, not independent verification |
| compare | Existing graph validator | Diff IDs, changed content and deterministic fingerprints, not a semantic oracle |

A plan is a JSON object with exactly record_type=AIRP_B_FIXED_PLAN, schema_version=1, source_commit=the protected-main SHA above, and steps (1–50). A step has exactly op, branch, expected_version, request_id, and args. The initial in-memory branch is base at version 0. Stale revision and conflicting idempotency keys reject; identical retries return the original receipt. The predeclared plan stops on the first rejection.

Run the tests in an isolated checkout with dependencies installed:

    python -m pytest -q tests/test_airp_b_fixed_workflow.py

Execute a disposable plan:

    python scripts/airp_b_fixed_workflow.py path/to/disposable-plan.json

The CLI only reads the plan and writes JSON to stdout. Snapshot mutations are single-process-serialized and staged until the existing validator succeeds. This is not multi-process transactional durability. No external side effect or protected state modification is supported.

## Registry traceability (research-only candidate mapping)

DGAF orchestration: P-PIER-001 fixed sequence; P-DURABLE-001 log/replay conceptual analog only, since the runner is not durable; P-TX-001 transaction-boundary inspiration; P-CB-001 bounded stop.

Pattern Commons: PC-GOV-001 capability is not authority; PC-EVP-002 exact revision; PC-EPI-001 correlated evidence caution; PC-EVP-004 synthetic quarantine; PC-EXEC-006 no authority transfer; PC-GOV-004 fail-closed ambiguity handling.

NDR P-37 and P-40 are separate family entries, not equivalent or aliases of DGAF P-SAGA-001 or P-TX-001. No pattern promotion.

## Acceptance and blockers

The positive and negative test module covers all six steps, branch isolation, stale versions, exact retry and collision, Evidence Gate digest rejection, malformed evidence bytes, no unauthorized tools, attribution classification, unmodified snapshots, source drift and stop-on-error. Verify final branch-head CI, and distinguish passing pytest subjobs from security-scan or environment setup failures.

This is not an operational equivalence study. A-DIRECT and future C-INSTRUMENT still need strictly matched model, permissions, source locks, task budget, evaluator, data and oracle. There is no held-out agent trial, durability, independent evidence identity attestation, measured benefit, or scientific N increment.

**Global boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED; AUTHORIZATION_EFFECT=NONE. No merge or release implied.

References: [Agent Instrument research owner](https://app.notion.com/p/413f5bad238b8141a3e8f322404fc2dd), [Pattern Commons promotion rules](https://app.notion.com/p/3ebf5bad238b81999758d01a0b793eb5), [DGAF orchestration registry](https://github.com/ndrorchestration/DGAF-Framework/blob/main/registry/PATTERN_REGISTRY_v2.md).
