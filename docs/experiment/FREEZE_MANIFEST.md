# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-21
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
candidate_sha: CURRENT_MAIN_CANDIDATE_AT_VERIFICATION
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical evidence and is superseded for the corrected pilot apparatus.

A new freeze commit may be created only after the blocking predicates are satisfied and independently verified. No value in this file authorizes pilot execution.

## Current candidate identity

The candidate is the current mainline tree at the time of the freeze-readiness evaluation. A final freeze packet must replace `CURRENT_MAIN_CANDIDATE_AT_VERIFICATION` with the exact immutable Git SHA of the tree being frozen.

PR #77 remains a historical engineering vehicle; its earlier head must not be treated as the current freeze candidate without refresh/re-verification.

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

The future freeze manifest must record exact immutable identities for:

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

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0.**
