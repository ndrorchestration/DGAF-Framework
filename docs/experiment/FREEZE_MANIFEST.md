# PDMAL Experiment — Freeze Manifest

---

status: ACTIVE
state: PRE-FREEZE / BLOCKED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-27
historical_freeze_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
current_verification_boundary: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
current_documentation_tip: 8390e53747da61d839c32dbbab1db3478c8b2e10
freeze_commit_sha: NONE
freeze_timestamp_utc: NONE
freeze_author: Ndr Orchestration
---

## State boundary

This file is the **pre-freeze manifest**. It is not evidence that the corrected apparatus is frozen. The historical implementation freeze at `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is retained as historical provenance and is not current apparatus authority.

The current experimental verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Documentation-only successors do not silently redefine that evidence boundary. A future freeze packet must bind every final control/protocol/analysis identity explicitly to the exact frozen Git tree.

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
- security/adversarial controls.

## Current evidence state

| Predicate | State |
|---|---|
| E2b verifier-toolchain provenance | CLOSED / VERIFIED |
| M6 negative-state observability | CLOSED / VERIFIED |
| P1 Candidate integrity | OPEN |
| P2 Execution contract | BLOCKED / OPEN — authenticated verification required |
| P3 Artifact contract | OPEN |
| P4 Security / blinding integrity | OPEN |
| P5 Provenance / reproducibility | OPEN |
| P6 Durable evidence custody | BLOCKED / OPEN |
| P6a Runtime/CORS | BLOCKED / OPEN — authenticated verification required |
| P7 Scientific target specification | ADOPTED / BINDING PENDING |
| P8 Analysis lock | OPEN / FAIL-CLOSED |
| P9 Independent verification | NOT EXECUTED |

## Verified control evidence

- M6 Governance CI run: `33050398324` against `ac8ea267…`.
- M6 retained artifact digest: `sha256:dabe2f1909535671e795bb8c1cad0ef0840be4732acebff8f1a340c62b4943b6`.
- P7 adoption record: documentation/governance commit `98db6563aad9a7afb45cdd064172efa7f221ef0d`.
- Exact current production deployment: `dpl_DND15HJ45s1d5eFcGmVr4SWNpGaC`, source-bound to `ac8ea267…`; runtime health evidence is separate from P2/P6a authenticated closure.

## Promotion rule

A true frozen manifest requires:

1. P1–P8 supported by candidate-scoped evidence;
2. P9 independently verifies the evidence chain;
3. the exact candidate SHA is committed and recorded;
4. protocol, analysis, retention, blinding, and provenance state are internally coherent;
5. freeze verification succeeds;
6. authorization remains a separate decision.

**Pilot authorization: NOT GRANTED. Empirical N: 0.**
