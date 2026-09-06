# P4 Mode T Synthetic Timing Study Design — 2026-09-05

**Status:** PARTIAL SYNTHETIC TIMING HARNESS / NONCANONICAL / NO W PROPOSAL  
**Issue:** #293  
**Parent:** #287  
**Stacked design dependency:** draft PR #292  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Measure bounded operational durations that are necessary, but not sufficient, to later choose a conservative Mode-T analysis-lock window `W`.

This tranche deliberately does **not** choose `W`, freeze a protocol, authorize a pilot, execute empirical work, instantiate a real blinding secret, or treat synthetic timing as efficacy evidence.

The controlling draft invariant remains:

`release_round = first_round_at_or_after(T_C + W)`

with analysis lock valid only when externally verified `T_L < release_time`.

## Exact computational shapes measured

The timing harness imports the same repository-native constants and execution classes used by the current pilot and locked analysis rather than copying a parallel matrix definition.

### Full pilot-shape deterministic task matrix

For each timing repetition it executes:

- 5 topology identities from `harness_contract.TOPOLOGY_SPECS`;
- 4 condition identities from `task_engine.CONDITION_VALUES`;
- 9 failure counts from `run_pilot.FAILURE_COUNTS`;
- exactly 180 deterministic `ConsensusTask` executions.

Only execution status and elapsed monotonic-clock duration are retained. Consensus values, primary outcomes, condition effects, and other scientific result fields are not serialized into timing evidence.

### Locked primary-analysis shape

For each timing repetition the harness builds a deterministic, non-empirical, schema-shaped fixture with:

- 50 synthetic seed identities;
- all 5 × 4 × 9 matrix cells per seed;
- blinded fixture identifiers unrelated to any real blinding mapping;
- 10,000 paired bootstrap resamples using the locked analysis seed.

The locked analysis functions are executed, but their estimated effect and confidence interval are not emitted. Only elapsed duration is retained.

## Supply-chain prerequisite

The workflow independently re-downloads the fixed `drand/tlock` v1.2.0 Linux amd64 release asset and its `checksums.txt` manifest and requires both the published and locally recomputed digest to equal:

`0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57`

This is a runtime re-verification of the exact asset already accepted at the PR #291 checksum boundary. The timing harness refuses the CI evidence run when that re-verification is absent or mismatched.

The workflow now measures synthetic tlock encryption after verifying the quicknet chain hash, scheme, and public key. It retains only timings and ciphertext byte sizes, then deletes synthetic payloads and ciphertexts. Strict-chain post-release decryption remains separate in #295.

## Evidence fields

The emitted JSON records:

- exact PR-head evidence SHA;
- workflow/helper/dependency-lock hashes;
- hashes of `analysis.py`, `run_pilot.py`, and `task_engine.py`;
- hosted-runner class;
- repetition count;
- full-shape matrix timing distribution (`min`, `p50`, `p95`, `max`, `mean`);
- locked-analysis timing distribution with the same statistics;
- exact tlock asset re-verification status;
- explicit stage coverage statuses;
- explicit scientific-control booleans.

A SHA-256 sidecar protects the JSON bytes. The Actions artifact is named with the PR-head evidence SHA rather than GitHub's synthetic pull-request merge SHA.

## Required end-to-end stages

The evidence contract contains six required stages:

1. exact tlock asset re-verification;
2. full synthetic matrix timing;
3. locked primary-analysis timing;
4. synthetic timelock-encryption timing with explicit verified quicknet identity;
5. external transparency / durable-retention timing using the finally selected P6 mechanism;
6. artifact-publication transport timing (deletable storage, not durable custody).

External transparency / durable-retention timing remains `NOT_EXECUTED` (#296). Encryption and publication transport may report PASS only after their run-bound records validate.

Therefore it must emit:

```text
coverage_complete = false
w_proposal_eligible = false
numeric_w_selected = false
proposed_w_seconds = null
```

A regression test enforces that partial coverage cannot become a W proposal.

## What these measurements cannot establish

Even after this partial workflow passes, it does not establish:

- a conservative full-workflow `W`;
- drand threshold-network security;
- beacon availability or delayed-round behavior;
- independently retained transparency timing;
- hosted-runner live-memory independence;
- P4-T custody sufficiency;
- canonical P4/P7/P8/P9 mode-specific predicates;
- freeze or authorization;
- empirical performance or efficacy.

## Publication transport timing (#297)

The upload fixture is deterministic public padding with an explicit synthetic evidence label. Its size is the maximum ciphertext byte size from the same run's synthetic encryption samples. No ciphertext is uploaded. Compression is disabled so the padding does not collapse into an unrepresentative tiny compressed payload.

The workflow records monotonic time immediately around the pinned upload action. The interval includes runner step-transition overhead and excludes the subsequent API verification. The action's returned ID, name, URL, and ZIP digest are checked against GitHub artifact metadata, including exact run and head binding. Run attempt is bound in the fixture name and timing record. Missing or mismatched metadata fails closed.

The dummy artifact has one-day retention; the local fixture is removed even on failure. The separate timing evidence has a SHA-256 sidecar and is included in the existing 30-day evidence upload. The combined study loads this record only after checking its digest, execution identity, timing interval, and non-authorizing controls.

This is one publication sample per workflow run. It does not establish a distribution, independent retention, end-to-end timing, degraded-condition performance, or an eligible W proposal. GitHub artifacts remain deletable. No Rekor submission is performed.

## Promotion rule

No numeric W may be proposed until every required timing stage has accepted synthetic evidence, ordinary and predeclared degraded-but-accepted repetitions are available, and a separate pre-freeze review defines the bound/quantile plus safety-margin rule.

Completion of timing coverage still does not automatically select W. The evidence schema is designed so `coverage_complete` and `w_proposal_eligible` are separate concepts.

## Current boundary

This lane is an engineering measurement apparatus only. It is intentionally stacked on draft #292 and must remain reviewable independently from the custody design itself.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**

