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

    python -m scripts.airp_b_fixed_workflow path/to/disposable-plan.json

The CLI only reads the plan and writes JSON to stdout. Snapshot mutations are single-process-serialized and staged until the existing validator succeeds. This is not multi-process transactional durability. No external side effect or protected state modification is supported.

## Registry traceability (research-only candidate mapping)

DGAF orchestration: P-PIER-001 fixed sequence; P-DURABLE-001 log/replay conceptual analog only, since the runner is not durable; P-TX-001 transaction-boundary inspiration; P-CB-001 bounded stop.

Pattern Commons: PC-GOV-001 capability is not authority; PC-EVP-002 exact revision; PC-EPI-001 correlated evidence caution; PC-EVP-004 synthetic quarantine; PC-EXEC-006 no authority transfer; PC-GOV-004 fail-closed ambiguity handling.

NDR P-37 and P-40 are separate family entries, not equivalent or aliases of DGAF P-SAGA-001 or P-TX-001. No pattern promotion.


## 2026-11-10 — Phase 2 exact-head implementation and CI evidence (non-admitting)

**Source-tested executable head:** [e70ac83f9c58919d9642354c48c4ab0f3edc5ab2](https://github.com/ndrorchestration/DGAF-Framework/commit/e70ac83f9c58919d9642354c48c4ab0f3edc5ab2) of [draft PR #1582](https://github.com/ndrorchestration/DGAF-Framework/pull/1582). **Protected-main base:** 1a95b94332dffb404c5a3ce026d70781a8c10b90 (unchanged). This entry is a historical exact-head snapshot; a later documentation-only commit does not inherit the label "tested exact head" without its own checks.

| Evidence lane | Outcome at source-tested head | Bounded meaning |
| --- | --- | --- |
| [Python 3.10 job](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337449/job/129644281628) | SUCCESS; 20/20 new AIRP tests passed; 2070 pytest passed, 5 skipped, 64 subtests passed | Internal synthetic engineering checks only |
| [Python 3.11 job](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337449/job/129644281789) | SUCCESS; 20/20 new tests passed; 2070 pytest passed, 5 skipped, 64 subtests passed | Internal synthetic engineering checks only |
| [Python 3.12 job](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337449/job/129644281477) | SUCCESS; 20/20 new tests passed; 2070 pytest passed, 5 skipped, 64 subtests passed, 7 warnings | Internal synthetic engineering checks only |
| Integration tests | SUCCESS | Not a scientific or independent review |
| Changed-file flake8, Black, isort, mypy; Bandit blocking threshold | PASS | Does not clear installed dependency risk |
| [Python Tests & Quality Checks](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337449) | **FAIL** at security-scan installed-environment pip-audit, 19 reported vulnerabilities in five packages | No waiver; dependency remediation separately scoped |
| [PDMAL Harness](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337463) | **FAIL** at Python 3.12.0 setup before contract tests | Do not infer code failure or inheritance from main |
| [PDMAL Pre-Freeze Runner](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/42760337538) | **FAIL** at Python 3.12.0 setup before contract tests | Do not infer code failure or inheritance from main |
| Other associated workflow families | 17 SUCCESS, 3 FAILURE, 0 PENDING at last settled snapshot | Overall PR is **NOT GREEN** |

**Disposition:** 20 synthetic positive/negative checks passed on each of three Python environments; B-FIXED is **ENGINEERING-TESTED IN DRAFT SCOPE**. No agents were evaluated, no C-INSTRUMENT was implemented, no A/B/C equivalence was demonstrated and no independent receiver or custody was established. An in-process version/replay record is not a durable cross-invocation transaction. Git SHA-1 blob locking uses \`usedforsecurity=False\` to identify historic source bytes, not to authenticate producers or establish independent provenance.

**Outstanding go/no-go criteria:** classify 19 dependency findings and separately fix/test without bypassing the gate; resolve/disposition Python 3.12.0 setup failures in their owning PDMAL CI lanes; perform full capability-equivalence contract review for A-DIRECT vs B-FIXED; source-lock and prospective-freeze new held-out evaluation tasks/oracles before any future scientific work; preserve PR draft/unmerged and no governance promotion. Prior synthetic fixtures are development-visible and are **not** held-out evaluation cases. There is no authorization to run an efficacy study.

**Related research branches:** [terminology/protocol draft PR #1570](https://github.com/ndrorchestration/DGAF-Framework/pull/1570) and [synthetic A/B ClaimGraph smoke draft PR #1575](https://github.com/ndrorchestration/DGAF-Framework/pull/1575) remain separate draft/unmerged lanes; current heads must be inspected independently. The existing structural validation, Evidence Gate and attribution query remain the owning implementations.

**Research-state invariants:** \`SCIENTIFIC_N_INCREMENT=0\`; \`INDEPENDENT_VALIDATION=NOT_ESTABLISHED\`; \`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED\`; \`HIGH_ASSURANCE=NOT_AUTHORIZED\`; \`AUTHORIZATION_EFFECT=NONE\`; \`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED\`. No permission to merge, deploy, release, mutate canonical evidence or change DGAF governance.

## Acceptance and blockers

The positive and negative test module covers all six steps, branch isolation, stale versions, exact retry and collision, Evidence Gate digest rejection, malformed evidence bytes, no unauthorized tools, attribution classification, unmodified snapshots, source drift and stop-on-error. See the exact-head evidence ledger below. Do not transfer test results automatically to newer commits or conflate passing pytest subjobs with a green workflow.

This is not an operational equivalence study. A-DIRECT and future C-INSTRUMENT still need strictly matched model, permissions, source locks, task budget, evaluator, data and oracle. There is no held-out agent trial, durability, independent evidence identity attestation, measured benefit, or scientific N increment.

**Global boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED; AUTHORIZATION_EFFECT=NONE. No merge or release implied.

References: [Agent Instrument research owner](https://app.notion.com/p/413f5bad238b8141a3e8f322404fc2dd), [Pattern Commons promotion rules](https://app.notion.com/p/3ebf5bad238b81999758d01a0b793eb5), [DGAF orchestration registry](https://github.com/ndrorchestration/DGAF-Framework/blob/main/registry/PATTERN_REGISTRY_v2.md).
