# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-31
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
prior_production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
prior_pre_remediation_candidate: c6157158bf0ee4840e99a381a4b99bd2febe2302
prior_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
superseded_post151_apparatus_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
superseded_candidate_designation_commit_sha: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
pre_correction_restored_apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
active_provenance_correction_pr: 172
active_provenance_correction_head: 3c489459e09d2d9fb9d31239d9bae05df4b3548b
current_candidate_status: BLOCKED / PRE-CORRECTION / NOT EXECUTION-VALID
pre_correction_deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
pre_correction_deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
pre_correction_allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the restored apparatus is frozen. The historical implementation freeze at `3510b868…` is retained as provenance only.

PR #170 restored the seven constitutive gates, but adversarial review found that its canonical provenance identity omitted five behavior-affecting restored gate-state substrates. PR #172 is the active correction. Until #172 is validated and merged, `d56b5b3c…` is a pre-correction apparatus source and is not an execution-valid candidate.

If #172 merges, the resulting apparatus SHA creates a new candidate-cycle boundary. The pre-correction deployment and all evidence tied to it become historical/non-closing for that new cycle.

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
| Prior production source provenance | CLOSED / VERIFIED — historical `303f4424…` boundary |
| Seven-gate constitutive restoration | IMPLEMENTED / CORRECTION REQUIRED — provenance identity incomplete in `d56b5b3c…` |
| P1 Candidate integrity | BLOCKED ON #172 |
| P2 Execution contract / runtime | PAUSED — new candidate required after #172 |
| P3 Artifact contract | PAUSED — new candidate required after #172 |
| P4 Security / blinding integrity | PAUSED — new candidate required after #172 |
| P5 Provenance / reproducibility | BLOCKED — identity correction required |
| P6 Durable evidence custody | PAUSED — new candidate required after #172 |
| P6a Runtime/CORS | PAUSED — new candidate required after #172 |
| P7 Scientific target specification | ADOPTED / BINDING PENDING — bind to corrected final candidate/freeze |
| P8 Analysis lock | PAUSED / FAIL-CLOSED |
| P9 Independent verification | PAUSED |

## Provenance correction

The #170 canonicalization bound P-31/P-33 state but omitted the restored P-29 Sentinel, P-30 Apogee, DemiJoule, P-27 KAPPA, and P-32 Phi state. PR #172 binds these states into canonical identity and adds per-gate identity-change regression tests. This is an apparatus integrity correction, not an experimental observation.

## Pre-correction runtime identity

The following values belong only to the pre-correction `d56b5b3c…` deployment and must not close the post-#172 candidate cycle:

- Apparatus source SHA: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Production deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- Production deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Candidate boundary

No execution-valid candidate is designated during the #172 correction hold. A new candidate must be derived from the resulting post-correction apparatus source and its exact production deployment.

## Promotion rule

A true frozen manifest requires current-candidate P1–P8 evidence, independent P9 verification, an exact final apparatus/freeze identity, internally coherent protocol/analysis/retention/blinding/provenance state, and an independently verified freeze. Explicit authorization remains a separate transition.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
