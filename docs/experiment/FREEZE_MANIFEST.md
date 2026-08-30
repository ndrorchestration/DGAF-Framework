# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-30
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
mainline_tip_at_reconciliation: 255d76f6775caf40e758de4d41920f9ce40fda0c
prior_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
pre_freeze_candidate_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
pre_freeze_candidate_ref: experimental-candidate/2026-08-30-reconciled
candidate_deployment_id: dpl_8iYrzqsf729RSZRXj698pa4ptbWZ
candidate_deployment_state: READY
candidate_deployment_source_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
candidate_status: DESIGNATED / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical provenance and is not current apparatus authority.

`2a80f819…` is earlier P8 checklist lineage. `303f4424…` is the integrated DGAF v1 engineering/production source and prior P2/P6a runtime evidence boundary. `255d76f6…` was the mainline documentation/evidence tip observed during reconciliation. `ac8ea267…` is the historical experimental verification boundary. None is silently promoted to the current freeze.

The current experimental evidence cycle is explicitly designated at `c6157158bf0ee4840e99a381a4b99bd2febe2302` on `experimental-candidate/2026-08-30-reconciled`. Its Vercel deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` is now `READY` and reports an exact Git source SHA match to `c6157158…`. This satisfies deployment/source provenance but does not itself execute P2/P6a or create a freeze.

## Experimental design

- Conditions: `null`, `simple`, `static`, `dgaf`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- Trials per seed: 180
- Planned seeds: 50
- Planned raw trial records: 9,000
- Primary endpoint: FFCR per condition per seed
- Primary contrast: adopted P7 decision — `dgaf` vs `null`
- Iterations: 100 fixed; no convergence-based early stopping

## Current evidence state

| Predicate | State |
|---|---|
| E2b verifier-toolchain provenance | CLOSED / VERIFIED for recorded exact executions |
| M6 negative-state observability | CLOSED / VERIFIED for recorded exact executions |
| Production source provenance | CLOSED / VERIFIED — `303f4424…` → `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` |
| Candidate deployment provenance | CLOSED / VERIFIED — `c6157158…` → `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` (`READY`) |
| P1 Candidate integrity | OPEN / CURRENT CANDIDATE DESIGNATED |
| P2 Execution contract | PRIOR VERIFIED / CURRENT CANDIDATE OPEN |
| P3 Artifact contract | IMPLEMENTED / OPEN |
| P4 Security / blinding integrity | OPEN |
| P5 Provenance / reproducibility | OPEN |
| P6 Durable evidence custody | BLOCKED / OPEN |
| P6a Runtime/CORS | PRIOR VERIFIED / CURRENT CANDIDATE OPEN |
| P7 Scientific target specification | ADOPTED / BINDING PENDING |
| P8 Analysis lock | OPEN / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |

## Prior verified runtime evidence

P2 run `33300481208`, job `99227568599`, artifact `9728767844`, and P6a run `33302495240` remain exact evidence for candidate `303f4424…` and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. They are not silently transferred to `c6157158…`.

## Candidate deployment provenance

- Candidate SHA: `c6157158bf0ee4840e99a381a4b99bd2febe2302`
- Deployment: `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`
- Target: `production`
- State: `READY`
- Vercel Git source SHA: exact match

This closes candidate deployment/source provenance only. No current-candidate P2/P6a runtime completion is recorded.

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by current candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate/final apparatus SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
