# Current-Candidate Evidence Registry Contract v1

**Status:** CONTROL SPECIFICATION / NON-AUTHORITATIVE UNTIL EXECUTED
**Date:** 2026-09-04
**Scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0

## Purpose

Define one self-contained provenance contract for current-candidate evidence so P1/P3/P5/P6/P8 can reason over the same immutable source identity instead of reconstructing identity from separate narrative fields.

This specification does not create evidence. It defines what a producing workflow must emit before its output can be considered candidate-bound evidence.

## Immutable source tuple

Every evidence registry must carry:

```text
candidate_sha
candidate_tree_sha
apparatus_source_sha
protocol_identity
protocol_blob_sha
workflow_name
workflow_run_id
workflow_event
workflow_action
workflow_conclusion
artifact_name
artifact_id
artifact_digest
artifact_content_digest
execution_timestamp
```

The tuple is immutable for the registry instance. Any mismatch between tuple members is a hard failure.

## Registry-level invariants

1. `candidate_sha` is a full 40-character commit SHA.
2. `candidate_tree_sha` is the tree actually executed by the producing workflow.
3. `workflow_run_id` identifies the exact producing run; no latest-match lookup is permitted as a substitute.
4. `artifact_id` and `artifact_digest` identify the exact retained GitHub artifact object.
5. `artifact_content_digest` is recomputed from downloaded artifact content where technically feasible.
6. `workflow_name`, event, action, conclusion, candidate SHA, and run ID agree with the GitHub run metadata.
7. The registry's own candidate identity is repeated on every predicate record; predicate identity must never be left null or inferred solely from the parent object.
8. Structural dry-run status cannot promote a predicate from OPEN/FAIL_CLOSED to VERIFIED/CLOSED.
9. Freeze authorization, pilot authorization, unblinding, and empirical execution flags remain explicit booleans and default to false.
10. A registry cannot be used as current evidence when any upstream identity is historical, unresolved, or unverifiable.

## Predicate record contract

Each predicate entry must include:

```text
predicate_id
candidate_sha
status
required
scope
producer_workflow_run_id
producer_artifact_id
producer_artifact_digest
epistemic_status
```

`candidate_sha` must equal the registry-level `candidate_sha` exactly.

## Suggested epistemic statuses

Use the repository's existing lifecycle vocabulary without collapsing distinct meanings:

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → VALIDATED`

Historical, unsupported, or structurally demonstrated records must remain explicitly classified rather than silently promoted.

## P3/P5/P6/P8 relationship

- **P1:** proves the identity tuple is internally coherent.
- **P3:** proves the artifact satisfies the declared schema and canonical structural invariants.
- **P5:** proves the execution environment, implementation, protocol, dependencies, seeds, and tree identity are reproducible.
- **P6:** proves the retained artifact survives an independent archive/retrieval/hash round trip.
- **P8:** freezes the exact tuple plus analysis identity and prerequisite state before any unblinding.

None of these predicates is closed merely because another predicate shares the same candidate SHA.

## Completion-controller handoff

A producing workflow should emit its registry with its own run identity. The completion controller should then:

1. consume only the triggering `workflow_run.id`;
2. retrieve exactly the declared artifact from that run;
3. verify the immutable source tuple against GitHub metadata;
4. verify registry-level and predicate-level candidate identities agree;
5. reject missing, duplicate, expired, or mismatched artifacts;
6. retain the evidence decision without substituting another run.

## Anti-transfer rule

A registry is not transferable between candidates, deployments, protocol revisions, apparatus sources, or analysis implementations. Matching filenames, equivalent prose, successful prior runs, or later documentation commits are insufficient for transfer.

## Security rule

This contract must never contain the blinding key, authorization credential, or other secret material. It may record the existence and custody state of such controls, but not their values.

## Current DGAF disposition

This specification is an engineering/governance hardening artifact. It does not close P1/P3/P4/P5/P6/P7/P8/P9, establish freeze, grant authorization, or increase empirical N.

**Next implementation target:** make the PDMAL dry-run registry emit this contract directly, then validate it in CI before relying on the registry for automated completion decisions.
