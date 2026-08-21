# PDMAL Experiment — Freeze Manifest

---
status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-21
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
candidate_sha: TBD — refreshed candidate required
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**, not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical evidence and is superseded for the corrected pilot apparatus.

A new freeze commit must be created only after the blocking predicates are satisfied and independently verified. No value in this file authorizes pilot execution.

## Current repository identity

- Current `main`: `23ab411d6113b3281f011f6891fb9335c7b6972e`
- PR #77 candidate: `4983f44a1867d8ab2f18295a1ce23877ff8ea928` before refresh
- Candidate relationship: PR #77 is stale relative to current `main` and must be refreshed/re-verified.

## Experimental design

- Conditions: `null`, `simple`, `static`, `dgaf`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- Trials per seed: 180
- Planned seeds: 50
- Planned raw trial records: 9,000
- Primary endpoint: FFCR per condition per seed
- Primary contrast: OPEN — see `PRIMARY_CONTRAST_ADJUDICATION.md`
- Iterations: 100 fixed; no convergence-based early stopping

## Candidate provenance requirements

The future freeze manifest must record the exact candidate SHA and the exact blob/file identities for:

- experiment protocol and task specification;
- pilot runner and executor;
- artifact schema and canonical serializer;
- dependency lock;
- topology generators and fingerprint manifest;
- failure model and stopping rules;
- blinding controls and custody procedure;
- retention implementation and archive policy;
- analysis implementation and configuration;
- security/adversarial controls.

## Current evidence state

| Predicate | State |
|---|---|
| P1 Candidate integrity | PARTIAL |
| P2 Execution contract | PARTIAL |
| P3 Artifact contract | PARTIAL |
| P4 Security / blinding integrity | PARTIAL |
| P5 Provenance / reproducibility | PARTIAL |
| P6 Durable evidence custody | OPEN |
| P7 Scientific target specification | PARTIAL / contrast OPEN |
| P8 Analysis lock | OPEN |
| P9 Independent verification | NOT EXECUTED |

Experimental-design integrity is covered by P5 + P7. Authorization is a separate governance transition after freeze verification.

## Historical evidence

Historical characterization and acceptance evidence remains scoped to its exact runs and SHAs. It does not transfer automatically to the corrected candidate and does not constitute empirical efficacy evidence.

## Promotion rule

This manifest may be promoted to a true frozen manifest only when:

1. P1–P8 are supported by candidate-scoped evidence;
2. P9 independently verifies the required evidence chain;
3. the resulting candidate SHA is committed and recorded here;
4. the protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. a separate authorization decision is still required after freeze verification.

**Pilot authorization: NOT GRANTED. Empirical N: 0.**
