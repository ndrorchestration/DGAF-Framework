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

## Accepted follow-on contracts

PR #903 established the bounded, synthetic-only observation-to-`PolicyInput`
mapping contract and the 16-class synthetic source-driver recipe catalog. That
acceptance does not implement or accept an ACP source-driver executable.

PR #904 is the prospective non-collecting exact-runtime binding candidate. It
does not establish collection readiness unless separately accepted, and even
after acceptance the installed-environment manifest and source-driver binding
remain separate predicates.

## Remaining gates

Collection remains disabled until separate review and acceptance establish:

1. exact source-driver executable binding for the frozen recipe catalog;
2. accepted exact runtime/dependency binding plus the execution environment manifest;
3. executable collector binding and destination identity;
4. retained study/source/normalized/decision/analysis bundle custody;
5. five exact-byte replay passes and their verification booleans;
6. same-host freshness/ingest reference preservation;
7. attempt invalidation and no-retry-after-outcome-inspection behavior.

## Evidence boundary

`OUTCOME_COLLECTION_AUTHORIZED=TRUE` is unchanged.

`COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED`.

`SCIENTIFIC_N_INCREMENT=0`. External validation, canonical DGAF efficacy,
independent validation, production assurance, and High-Assurance remain
unestablished or unauthorized. Track A Epoch 002 remains
`CLOSED_FOR_EXACT_PREREGISTERED_SCOPE`.
