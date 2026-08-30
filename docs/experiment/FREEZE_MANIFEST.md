# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-30
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
prior_pre_remediation_candidate: c6157158bf0ee4840e99a381a4b99bd2febe2302
prior_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
post151_apparatus_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
candidate_designation_commit_sha: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
candidate_designation_ref: experimental-candidate/2026-08-30-post151
candidate_status: DESIGNATED / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the post-#151 apparatus is frozen. The historical implementation freeze at `3510b868…` is retained as provenance only.

PR #151 introduced substantive apparatus changes and merged as `05fa286…`. That merge commit is the apparatus/source identity for the new candidate cycle. The later `02c146d1…` commit is the candidate-designation/control record and MUST NOT be conflated with the apparatus identity.

The prior `c6157158…` cycle is superseded for experimental purposes. Its P3–P9 records remain historical/pre-remediation evidence and do not transfer to the post-#151 candidate.

## Experimental design

- Conditions: `null`, `simple`, `static`, `dgaf`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- Trials per seed: 180
- Planned seeds: 50
- Planned raw trial records: 9,000
- Primary endpoint: FFCR per condition per seed
- Primary contrast: `dgaf` vs `null`
- Iterations: 100 fixed; no convergence-based early stopping

## Current evidence state

| Predicate | State |
|---|---|
| E2b verifier-toolchain provenance | CLOSED / VERIFIED for recorded exact executions |
| M6 negative-state observability | CLOSED / VERIFIED for recorded exact executions |
| Prior production source provenance | CLOSED / VERIFIED — `303f4424…` boundary |
| Post-#151 apparatus designation | CLOSED AS DESIGNATION | `05fa286…` designated via `02c146d1…` |
| Candidate deployment provenance | REQUIRES FRESH EXACT-SOURCE CHECK | Must bind to `05fa286…` |
| P1 Candidate integrity | OPEN | Reconcile final component identities for `05fa286…` |
| P2 Execution contract / runtime | PRIOR VERIFIED / NEW CANDIDATE OPEN | Prior evidence remains bound to `303f4424…` |
| P3 Artifact contract | IMPLEMENTED / OPEN | Fresh candidate-scoped evidence required |
| P4 Security / blinding integrity | OPEN | Current-cycle operational evidence required |
| P5 Provenance / reproducibility | OPEN | Current-cycle evidence required |
| P6 Durable evidence custody | BLOCKED / OPEN | Current-cycle archive/retrieval/hash proof required |
| P6a Runtime/CORS | PRIOR VERIFIED / NEW CANDIDATE OPEN | Prior evidence remains bound to `303f4424…` |
| P7 Scientific target specification | ADOPTED / BINDING PENDING | Must bind to final candidate/freeze |
| P8 Analysis lock | OPEN / FAIL-CLOSED | Must be current-cycle and exact-candidate scoped |
| P9 Independent verification | NOT EXECUTED | Must independently verify the new evidence chain |

## Historical runtime evidence

P2 run `33300481208` / artifact `9728767844` and P6a run `33302495240` / artifact `9729387603` remain exact evidence for `303f4424…`. They are not evidence for `05fa286…`.

## Candidate boundary

Current experimental candidate:

`05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`

Designation/control commit:

`02c146d1e0cdc423948ac0dfa11e98f812edfb44`

These are intentionally distinct identities.

## Promotion rule

A true frozen manifest requires current-candidate P1–P8 evidence, independent P9 verification, an exact final apparatus/freeze identity, internally coherent protocol/analysis/retention/blinding/provenance state, and an independently verified freeze. Authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
