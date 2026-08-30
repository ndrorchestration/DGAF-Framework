# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-30
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
production_engineering_source: 303f4424d2198f0d0cf76305c589263dd1e417dc
current_experimental_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
current_documentation_tip: 59955f03794bc4203585a83e6ad46801e9825095
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical provenance and is not current apparatus authority.

The prior experimental verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. The merged DGAF v1 engineering/production source is `303f4424d2198f0d0cf76305c589263dd1e417dc`. These identities are not silently interchangeable: a new experimental apparatus/freeze must explicitly bind the final protocol, runner, artifact schema, analysis, environment, topology/RNG, security/custody, and evidence identities to one exact immutable Git tree.

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
| P1 Candidate integrity | OPEN |
| P2 Execution contract | BLOCKED / OPEN — authenticated verification required |
| P3 Artifact contract | IMPLEMENTED / OPEN — fresh execution evidence required |
| P4 Security / blinding integrity | OPEN |
| P5 Provenance / reproducibility | OPEN |
| P6 Durable evidence custody | BLOCKED / OPEN |
| P6a Runtime/CORS | BLOCKED / OPEN — authenticated verification required |
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

This closes production source/provenance only. It does not close P2/P6a, P7/P8/P9, create a freeze, grant authorization, or increase empirical N.

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by current candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate/final apparatus SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0. Freeze: NOT CREATED.**
