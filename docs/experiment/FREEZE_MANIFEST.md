# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-31
current_apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
current_apparatus_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
prior_production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
prior_pre_remediation_candidate: c6157158bf0ee4840e99a381a4b99bd2febe2302
prior_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
superseded_post151_apparatus_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
superseded_candidate_designation_commit_sha: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
invalidated_pre_correction_apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
invalidated_pre_correction_deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
current_candidate_status: PROVISIONAL / POST-PROVENANCE-CORRECTION / NOT EXECUTION-VALID
current_deployment_id: NONE_YET
current_deployment_url: NONE_YET
current_allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the current apparatus is frozen. The historical implementation freeze at `3510b868…` is retained as provenance only.

PR #174 merged the provenance-integrity correction as apparatus source `2a54a67d…`. The earlier `d56b5b3c…` apparatus is invalidated as an execution candidate because its canonical identity omitted five restored gate-state substrates.

The current apparatus source is therefore `2a54a67d…`. No current deployment has yet been authoritatively bound to that source, so no execution-valid candidate is designated and no P2/P6a evidence may be generated yet.

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
| Historical freeze | HISTORICAL / SUPERSEDED |
| Seven-gate constitutive restoration | IMPLEMENTED / PROVENANCE COMPLETE |
| Current apparatus identity | PROVISIONAL / PRE-FREEZE | `2a54a67d…` |
| Current deployment identity | NOT ESTABLISHED | Must be READY + exact source-SHA matched |
| P1 Candidate integrity | BLOCKED UNTIL DEPLOYMENT |
| P2 Execution contract / runtime | BLOCKED — fresh candidate required |
| P3 Artifact contract | PAUSED — current candidate evidence required |
| P4 Security / blinding integrity | PAUSED — current-cycle evidence required |
| P5 Provenance / reproducibility | BLOCKED — current deployment identity required |
| P6 Durable evidence custody | PAUSED — current-cycle proof required |
| P6a Runtime/CORS | BLOCKED — fresh candidate required |
| P7 Scientific target specification | ADOPTED / BINDING PENDING |
| P8 Analysis lock | PAUSED / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |
| Freeze | NOT CREATED |
| Authorization | NOT GRANTED |
| Empirical N | 0 |

## Provenance correction

The #170 apparatus `d56b5b3c…` is retained as historical only. PR #174 completed the bounded provenance correction by incorporating all seven restored gate-state substrates into canonical identity and adding regression coverage, including substrate-driven P-29 behavior. The correction does not itself create candidate evidence.

## Current candidate runtime identity

A fresh deployment must be created from exact apparatus source `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. Its deployment ID and URL must be captured from Vercel, and Vercel's Git source SHA must exactly equal `2a54a67d…` before P2/P6a can execute.

The old `dpl_76UU8mCm…` deployment is bound to invalidated `d56b5b3c…` and is non-closing.

## Candidate boundary

No execution-valid candidate is frozen or authorized. Candidate promotion requires exact source/deployment binding plus fresh P1–P9 evidence and independent P9 verification.

## Promotion rule

A true frozen manifest requires current-candidate P1–P8 evidence, independent P9 verification, an exact final apparatus/freeze identity, coherent protocol/analysis/retention/blinding/provenance state, and an independently verified freeze. Explicit authorization remains a separate transition.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
