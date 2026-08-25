# Governance CI Execution Control

## Purpose

Make the Governance CI execution state explicit and prevent absence of a workflow run from being interpreted as success.

## Required states

- `NOT_EXECUTED`: no completed candidate-scoped Governance CI run is evidenced.
- `EXECUTING`: a candidate-scoped run exists but is incomplete.
- `PASS`: the candidate-scoped run completed successfully and required evidence artifacts are retained.
- `FAIL`: the candidate-scoped run completed unsuccessfully.

## Candidate binding

A Governance CI result is candidate-scoped only when all of the following are recorded in the run/evidence:

- repository;
- commit SHA;
- workflow name/path;
- workflow run ID;
- job name;
- completion conclusion;
- required artifact names and retention state.

## Trigger contract

The canonical workflow must support:

- pushes to `main`;
- pull requests targeting `main`;
- explicit `workflow_dispatch` recovery/manual execution.

A successful P2 runtime check, Vercel deployment, or historical Governance CI run MUST NOT be substituted for a current candidate-scoped Governance CI result.

## Fail-closed rule

If no current candidate-scoped Governance CI result exists, the governance state is `NOT_EXECUTED`, not `PASS`.

If a run fails, the state is `FAIL` until a later candidate-scoped run demonstrates a corrected `PASS`.

## Evidence requirements

The workflow should retain machine-readable evidence containing the candidate SHA and run ID and should expose the execution conclusion in the workflow summary/check surface.

## Current state

As of 2026-08-25, the workflow configuration supports `push`, `pull_request`, and `workflow_dispatch`. The latest candidate has verified P2 runtime evidence, but a completed candidate-scoped Governance CI result has not yet been established.

**Governance CI state: NOT_EXECUTED**  
**P8: OPEN**  
**Pilot authorization: NOT GRANTED**  
**Empirical N: 0**
