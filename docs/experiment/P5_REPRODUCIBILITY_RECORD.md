# P5 Reproducibility / Provenance Record

## Status

**PENDING FRESH CANDIDATE EXECUTION.**

This document is a record template and boundary statement. The historical dry-run evidence previously recorded here belonged to an earlier candidate and is intentionally not transferred to the current controlled candidate.

## Current evidence rule

A P5 verification claim is admissible only when the fresh source workflow records the exact candidate SHA under test and binds the resulting run, artifact ID, and artifact digest to that same candidate. Historical evidence may remain useful as background but must not be promoted as current-candidate evidence.

## Required reproducibility checks

1. **RNG stream separation:** `experiments/pdmal_topology/seeds.py` derives named streams from `pdmal-v1|<master_seed>|<stream>` using SHA-256, with distinct topology and failure streams used by the graph harness.
2. **Determinism:** the same seed/topology/failure-count case must be executed twice and both canonical JSON output and digest must match.
3. **Artifact integrity:** the instrumentation artifact must pass schema and checksum validation, survive upload/download custody, and have its recorded SHA-256 independently recomputed.
4. **Exact-candidate binding:** the evidence registry must record the same candidate SHA, workflow run, artifact ID, and artifact digest used by the completion controller.

## Fresh execution record

Populate this section only from a successful run against the current controlled candidate:

- Candidate SHA: `<fresh candidate SHA>`
- Source workflow: `<workflow name>`
- Source run: `<run ID>`
- Instrumentation artifact: `<artifact ID>`
- Instrumentation artifact digest: `sha256:<digest>`
- Evidence-registry artifact: `<artifact ID>`
- Evidence-registry digest: `sha256:<digest>`

## Boundary

P5 must remain **OPEN** until the fresh candidate-bound execution succeeds. This record does not authorize freeze, pilot execution, production deployment, or empirical experiment execution. Empirical execution remains unauthorized and empirical N remains zero.
