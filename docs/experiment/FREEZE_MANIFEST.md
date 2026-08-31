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
current_restored_apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
current_restored_apparatus_tree_sha: 8c13900c4ce2a503414f9dddf1d7ef7debead57e
current_candidate_status: PROVISIONAL / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
current_deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
current_deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
current_allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the restored apparatus is frozen. The historical implementation freeze at `3510b868…` is retained as provenance only.

PR #170 introduced the completed seven-gate constitutive restoration and provenance integration. The merge commit `d56b5b3c…` is the current restored apparatus/source identity. Later documentation-only commits may advance the `main` tip without changing that apparatus source.

The superseded `05fa286…` candidate cycle and the `02c146d1…` designation record remain historical. Their runtime/experimental evidence does not transfer to `d56b5b3c…`.

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
| Seven-gate constitutive restoration | IMPLEMENTED / PRE-FREEZE VALIDATED — `d56b5b3c…` |
| Candidate deployment provenance | IDENTIFIED — `dpl_76UU8mCm…` / production / READY |
| P1 Candidate integrity | OPEN — fresh candidate evidence required |
| P2 Execution contract / runtime | NEW CANDIDATE OPEN — fresh run required |
| P3 Artifact contract | IMPLEMENTED / OPEN — fresh candidate-scoped evidence required |
| P4 Security / blinding integrity | OPEN — current-cycle operational evidence required |
| P5 Provenance / reproducibility | OPEN — current-cycle evidence required |
| P6 Durable evidence custody | OPEN / FAIL-CLOSED — current-cycle archive/retrieval/hash proof required |
| P6a Runtime/CORS | NEW CANDIDATE OPEN — fresh run required |
| P7 Scientific target specification | ADOPTED / BINDING PENDING — bind to final candidate/freeze |
| P8 Analysis lock | OPEN / FAIL-CLOSED — current-cycle exact-candidate evidence required |
| P9 Independent verification | NOT EXECUTED — independent verification required |

## Current runtime identity

- Apparatus source SHA: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Apparatus tree SHA: `8c13900c4ce2a503414f9dddf1d7ef7debead57e`
- Production deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- Production deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

These values are candidate inputs, not evidence of P2/P6a success. P2/P6a workflows must verify them at execution time and emit retained provenance artifacts.

## Historical runtime evidence

P2 run `33300481208` / artifact `9728767844` and P6a run `33302495240` / artifact `9729387603` remain exact evidence for the historical `303f4424…` source/deployment boundary. They are not evidence for `d56b5b3c…`.

## Candidate boundary

Current provisional experimental candidate basis:

`d56b5b3c44e39ddb8c883259584432ab39259306`

This is intentionally distinct from the mutable `main` documentation tip and from the eventual immutable freeze identity.

## Promotion rule

A true frozen manifest requires current-candidate P1–P8 evidence, independent P9 verification, an exact final apparatus/freeze identity, internally coherent protocol/analysis/retention/blinding/provenance state, and an independently verified freeze. Explicit authorization remains a separate transition.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
