# AOSS v0.6 Stage-A collector foundation

**Controller:** #890  
**Accepted design:** #896 / `007274d7af33fd4ebff1ef62d7f2e5ab83565fb2`  
**Implementation:** #900  
**Classification:** NON-COLLECTING DEVELOPMENT FOUNDATION

## Purpose

This tranche implements only the pre-execution foundation accepted by #896:

- read-only verification of frozen DGAF and ACP source identities;
- fail-closed verification of the accepted Stage-A authorization and pre-collection receipt lineage;
- synthetic-only, exclusive attempt/custody primitives for development tests;
- a preflight CLI that emits static evidence only;
- a `collect` command that is deliberately disabled.

It does not execute ACP, generate a Stage-A study episode, retain an accepted-study
artifact, run replay, or perform Stage-A analysis.

## Interface

Static preflight:

```bash
python scripts/run_aoss_v0_6_stage_a.py preflight \
  --dgaf-root . \
  --acp-root ../agent-control-plane
```

The report is limited to static identity evidence. A PASS does not establish
collection execution readiness.

Collection stop:

```bash
python scripts/run_aoss_v0_6_stage_a.py collect
```

This command is expected to exit nonzero with
`COLLECTION_IMPLEMENTATION_NOT_ACCEPTED`. It has no output-destination
parameter and does not import or execute an ACP source driver.

## Fail-closed checks

The preflight rejects, at minimum:

- a missing or wrong ACP checkout;
- shallow repositories;
- Git replacement refs;
- dirty or untracked worktrees;
- authorization or receipt lineage drift, including the exact authorization parent and direct-child receipt relation;
- authorization/receipt event-history mutation even when bytes are later restored;
- frozen contract or executable blob mismatch, including the replay-receipt contract and schema;
- authorization/receipt byte drift;
- invalid accepted authorization/receipt boundary fields.

The accepted authorization permits the bounded study. It does not waive these
execution-readiness checks.

## Synthetic custody boundary

Synthetic custody uses exclusive directory/file creation, `O_NOFOLLOW`,
content-addressed SHA-256 objects, canonical JSON bytes, explicit file and
directory-entry `fsync`, and an explicit `SYNTHETIC_TEST_ONLY` marker. Incomplete
reservations are retained rather than cleaned and reused.

These primitives are development apparatus only. They are not the accepted
five-bundle study custody/replay implementation.

## Remaining gates

Collection remains disabled until separate review and acceptance establish:

1. exact telemetry-to-`PolicyInput` mapping;
2. concrete source-driver recipes for all frozen episode classes;
3. an exact runtime/dependency lock;
4. executable collector binding and destination identity;
5. retained study/source/normalized/decision/analysis bundle custody;
6. five exact-byte replay passes and their verification booleans;
7. same-host freshness/ingest reference preservation;
8. attempt invalidation and no-retry-after-outcome-inspection behavior.

## Evidence boundary

`OUTCOME_COLLECTION_AUTHORIZED=TRUE` is unchanged.

`COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED`.

`SCIENTIFIC_N_INCREMENT=0`. External validation, canonical DGAF efficacy,
independent validation, production assurance, and High-Assurance remain
unestablished or unauthorized. Track A Epoch 002 remains
`CLOSED_FOR_EXACT_PREREGISTERED_SCOPE`.
