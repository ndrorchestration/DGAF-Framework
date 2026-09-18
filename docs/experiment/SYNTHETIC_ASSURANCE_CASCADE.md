# Synthetic Assurance Cascade

Status: **AUTHORIZED FOR SYNTHETIC ENGINEERING / NON-EMPIRICAL ONLY**

Issue: #822

Scientific-state effect: **NONE**

`SCIENTIFIC_N_INCREMENT=0`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

## Purpose

DGAF can exercise and measure a large fraction of its engineering, governance,
analysis, orchestration, and fail-closed control surface before the real Track A
Epoch 002 custody-bound materialization is available.

Until real data is deliberately admitted through the existing governed
materialization path, this lane uses only deterministic synthetic or surrogate
inputs.

Synthetic execution is permitted to test code paths that will later process
real data, including the locked primary-analysis implementation. A synthetic
execution of that implementation is a timing/contract test only. It is not the
real primary analysis and cannot satisfy the empirical authorization gate.

## Current cascade

The workflow `.github/workflows/synthetic-assurance-cascade.yml` runs three
stages.

### 1. PDMAL synthetic matrix and timing

It:

- runs contract, execution, task-engine, artifact-schema, security, blinding,
  governance-trace, analysis, and timing tests;
- executes and times the exact 50-seed × 180-trial = 9,000-task synthetic shape;
- times the locked primary-analysis implementation against deterministic
  50-seed synthetic analysis documents;
- retains no scientific outcome from the synthetic task-shape run;
- does not instantiate the real blinding secret or use protected material.

### 2. Track A gate and synthetic falsification tests

It:

- exercises analysis-lock validation;
- exercises materialization and unblinded-materializer adversarial fixtures;
- exercises materialization-receipt preparation behavior;
- exercises primary-analysis authorization contracts and negative controls;
- exercises downstream result-record schema, semantics, and ledger logic;
- runs the preregistered weighted Forman–Ricci synthetic falsification matrix:
  480 trials, split into 240 calibration and 240 held-out trials.

### 3. Measurement sealing

The workflow produces
`SYNTHETIC_ASSURANCE_CASCADE_SUMMARY.json`, which combines:

- JUnit test counts;
- 9,000-task timing measurements;
- component 180-cell matrix timing;
- synthetic locked-analysis timing;
- weighted Forman–Ricci variance-restoration and detector measurements;
- explicit unresolved/NOT-ESTABLISHED boundaries.

The summary fails closed if any input attempts to claim empirical data use,
protected-material use, empirical N above zero, real materialization, real
primary-analysis execution, canonical efficacy, or independent validation.

## Evidence interpretation

A PASS can support statements such as:

- the tested gate rejected the controlled invalid fixture;
- the synthetic execution path completed deterministically;
- the implementation handled the complete intended task shape;
- the analysis implementation executed on a structurally compatible synthetic
  input;
- a measured synthetic runtime or falsification metric had the reported value.

A PASS cannot support statements such as:

- DGAF is empirically effective;
- the real Epoch 002 materialization occurred;
- the real primary analysis ran;
- the empirical result will match the synthetic result;
- the synthetic timing establishes production performance;
- independent validation has occurred.

## Relationship to real Track A Epoch 002

The real chain remains separate:

`controlled local materialization`
→ `non-secret materialization evidence admission`
→ `immutable MATERIALIZATION_RECEIPT`
→ `separate primary-analysis authorization`
→ `real locked primary analysis`
→ `result`
→ `interpretation/adjudication`.

Synthetic assurance is allowed to cascade around that blocked real-data edge,
but it does not jump across it.
