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
candidate_status: DESIGNATED / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical provenance and is not current apparatus authority.

`2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is an ancestor of `303f4424…` and represents earlier P8 checklist lineage. `303f4424d2198f0d0cf76305c589263dd1e417dc` is the integrated DGAF v1 engineering/production source and the exact source bound by prior verified P2/P6a runtime evidence. The `main` tip observed during reconciliation was `255d76f6775caf40e758de4d41920f9ce40fda0c`, a descendant of `303f4424…`, with documentation/evidence-surface changes in the compared interval.

The next experimental evidence cycle is explicitly designated at `c6157158bf0ee4840e99a381a4b99bd2febe2302` on `experimental-candidate/2026-08-30-reconciled`. This designation does not create a freeze. Prior P2/P6a evidence at `303f4424…` remains exact prior-candidate evidence and cannot be silently transferred.

## Identity roles

- `2a80f819…` — historical P8 checklist ancestor;
- `303f4424…` — integrated engineering/production source and prior P2/P6a runtime evidence boundary;
- `255d76f6…` — mainline documentation/evidence tip observed during reconciliation;
- `ac8ea267…` — prior experimental verification boundary, historical/provenance only;
- `c6157158…` — designated current pre-freeze candidate, not frozen and not yet execution-verified.

No value in this file authorizes pilot execution.

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
- security/adversarial controls;
- exact production source/deployment identity where runtime predicates apply.

## Current evidence state

| Predicate | State |
|---|---|
| E2b verifier-toolchain provenance | CLOSED / VERIFIED for recorded exact executions |
| M6 negative-state observability | CLOSED / VERIFIED for recorded exact executions |
| Production source provenance | CLOSED / VERIFIED — `303f4424…` → Vercel `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` |
| P1 Candidate integrity | OPEN / CURRENT CANDIDATE DESIGNATED |
| P2 Execution contract | PRIOR VERIFIED / CURRENT CANDIDATE OPEN |
| P3 Artifact contract | IMPLEMENTED / OPEN — fresh candidate-scoped execution evidence required |
| P4 Security / blinding integrity | OPEN |
| P5 Provenance / reproducibility | OPEN |
| P6 Durable evidence custody | BLOCKED / OPEN |
| P6a Runtime/CORS | PRIOR VERIFIED / CURRENT CANDIDATE OPEN |
| P7 Scientific target specification | ADOPTED / BINDING PENDING |
| P8 Analysis lock | OPEN / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |

## Verified prior production provenance

- Production Git commit: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match to production Git commit
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`

This closes production source/provenance only for `303f4424…`. It does not establish current-candidate runtime verification.

## Current candidate execution boundary

The designated candidate is `c6157158bf0ee4840e99a381a4b99bd2febe2302`. A candidate-specific Vercel deployment must reach `READY` and report exact Git source SHA `c6157158…` before current-candidate P2/P6a runtime evidence can be accepted.

The first observed Vercel deployment for this candidate, `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`, was still `BUILDING` during inspection. No current-candidate runtime completion is therefore claimed.

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by current candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate/final apparatus SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
