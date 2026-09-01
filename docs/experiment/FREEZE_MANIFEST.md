# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-09-01
corrected_apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
corrected_apparatus_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
runtime_candidate_tree_sha: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
runtime_candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 92ff830b1c67413df745e37087e6447c9c251b9a
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
prior_production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
prior_pre_remediation_candidate: c6157158bf0ee4840e99a381a4b99bd2febe2302
prior_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
superseded_post151_apparatus_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
superseded_candidate_designation_commit_sha: 02c146d1e0cdc423948ac0dfa11e98f812edfb44
invalidated_pre_correction_apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
invalidated_pre_correction_deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
current_candidate_status: CURRENT RUNTIME CANDIDATE / PRE-FREEZE / NOT FROZEN
current_deployment_id: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
current_deployment_url: https://dynamicgovernanceagenticformation-3y3d8o5dp-ndrorchestration.vercel.app
current_allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: NONE
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the current apparatus is frozen. The historical implementation freeze at `3510b868…` is retained as provenance only.

PR #174 merged the provenance-integrity correction as apparatus source `2a54a67d…`. The earlier `d56b5b3c…` apparatus is invalidated as an execution candidate because its canonical identity omitted five restored gate-state substrates.

The current runtime candidate is now distinct from that apparatus source: candidate `92ff830b…`, exact tree `73cf3ad…`. The corrected apparatus source remains the canonical provenance anchor; the runtime candidate is the executable identity used by current runtime evidence.

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
| Corrected apparatus identity | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Runtime candidate identity | CURRENT / NOT FROZEN | `92ff830b…`; tree `73cf3ad…` |
| Candidate lineage | ESTABLISHED | `2a54a67d…` → `92ff830b…` |
| Current deployment identity | CAPTURED | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P1 Candidate integrity | CURRENT-CANDIDATE EVIDENCE OPEN |
| P2 Execution contract / runtime | VERIFIED | Run `33509348174`; artifact `9800942933` |
| P3 Artifact contract | IMPLEMENTED / OPEN | Current-candidate evidence required |
| P4 Security / blinding integrity | OPEN | Current-cycle evidence required |
| P5 Provenance / reproducibility | OPEN | Current-candidate environment/topology/RNG evidence required |
| P6 Durable evidence custody | OPEN / FAIL-CLOSED | Current-cycle proof required |
| P6a Runtime/CORS | VERIFIED | Run `33509416955`; artifact `9800972819` |
| P7 Scientific target specification | ADOPTED / FINAL BINDING PENDING |
| P8 Analysis lock | OPEN / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |
| Freeze | NOT CREATED |
| Authorization | NOT GRANTED |
| Empirical N | 0 |

## Provenance correction

The #170 apparatus `d56b5b3c…` is retained as historical only. PR #174 completed the bounded provenance correction by incorporating all seven restored gate-state substrates into canonical identity and adding regression coverage, including substrate-driven P-29 behavior. The correction establishes apparatus provenance but does not itself constitute runtime evidence.

## Current runtime identity and evidence

P2 and P6a both recorded the same deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact `9800942933` digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`. Five required runtime cases passed, including the required fail-closed missing-audit case.

P6a artifact `9800972819` digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`. Four CORS checks passed, including allowed-origin preflight 204 and disallowed-origin preflight 403.

These are predicate-scoped runtime results. They do not create a freeze, establish efficacy, grant authorization, or cross the empirical boundary.

## Historical documentation classification

Older audit records stating that inline artifact validation is missing are historical/stale observations, not current defects. The current implementation performs inline artifact validation. Historical records remain preserved; current-state records carry the present implementation and current-candidate evidence status.

## Candidate boundary

No execution-valid freeze or authorization exists. P3–P6 remain open as separate current-cycle evidence predicates. P7 requires final exact candidate/protocol/analysis/freeze binding. P8 remains fail-closed until TGL/P-35 candidate verification is complete. P9 remains independent and unexecuted.

## Promotion rule

A true frozen manifest requires current-candidate P1–P8 evidence, independent P9 verification, an exact final apparatus/candidate/freeze identity, coherent protocol/analysis/retention/blinding/provenance state, and an independently verified freeze. Explicit authorization remains a separate transition.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
