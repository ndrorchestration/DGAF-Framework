# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-30
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
current_mainline_tip: 255d76f6775caf40e758de4d41920f9ce40fda0c
current_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
freeze_candidate_sha: NONE — must be explicitly designated after candidate-scoped re-verification
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical provenance and is not current apparatus authority.

The prior experimental verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. The integrated DGAF v1 engineering/production source is `303f4424d2198f0d0cf76305c589263dd1e417dc`, which is an ancestor of the current `main` tip `255d76f6775caf40e758de4d41920f9ce40fda0c`. A comparison of `303f4424…` to current `main` shows only documentation/evidence-surface changes after the engineering integration; no executable apparatus files are changed in that interval.

`2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is also an ancestor of `303f4424…` and therefore is not a competing mainline apparatus tree. References that name `2a80f819…` as the current P8 candidate are superseded lineage references and must not be used as the active verification target.

These identities remain distinct by role:

- `2a80f819…` — historical P8 checklist ancestor;
- `303f4424…` — integrated DGAF v1 engineering/production source and verified runtime deployment source;
- `255d76f6…` — current `main` documentation/evidence tip;
- `ac8ea267…` — prior experimental verification boundary, retained as historical/provenance state;
- **freeze candidate** — not yet designated; must be explicitly established and then verified as one immutable candidate before freeze.

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
| P1 Candidate integrity | OPEN — final freeze candidate not yet designated |
| P2 Execution contract | VERIFIED — exact prior runtime evidence is bound to `303f4424…`; fresh execution is required for any newly designated freeze candidate |
| P3 Artifact contract | IMPLEMENTED / OPEN — fresh candidate-scoped execution evidence required |
| P4 Security / blinding integrity | OPEN |
| P5 Provenance / reproducibility | OPEN |
| P6 Durable evidence custody | BLOCKED / OPEN |
| P6a Runtime/CORS | VERIFIED — exact prior runtime evidence is bound to `303f4424…`; fresh execution is required for any newly designated freeze candidate |
| P7 Scientific target specification | ADOPTED / BINDING PENDING |
| P8 Analysis lock | OPEN / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |

## Verified production provenance

- Production Git commit: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match to production Git commit
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`
- Selected production runtime window: no error or warning entries returned

This closes production source/provenance only. P2 and P6a are separately verified for the exact `303f4424…` runtime boundary as recorded in the current control state; neither result silently transfers to a future freeze candidate.

## Candidate designation rule

The next experimental candidate must be an explicitly designated immutable Git identity after substantive apparatus work is complete. Because the current `main` tip contains only documentation/evidence changes relative to `303f4424…`, those changes do not by themselves establish a new experimental verification candidate; however, the freeze process must still bind one exact immutable candidate and re-execute any predicates whose evidence requires exact SHA matching.

Accordingly, **303f4424… is not being silently promoted to the final experimental freeze**, and `255d76f6…` is not being silently treated as already verified. A new candidate designation must precede downstream closure.

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by current candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate/final apparatus SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
