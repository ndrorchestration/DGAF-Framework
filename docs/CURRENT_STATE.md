---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-29
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `main` is the current documentation/evidence lineage boundary at `087f3d3050085c465a2beda96e12bc33537ca368`. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## 2026-08-29 — DGAF v1 control-plane finalization lane

The viable implementation-oriented subset of the Governed Recursive Control Plane is now being carried on a clean branch created from the current `main` boundary: `feat/dgaf-v1-control-plane-finalize-20260829`.

Candidate implementation modules include `GovernanceEnvelope`, deterministic `ControlPlane`/`TaskState`, `StateRegistry`, `BudgetLedger`, `BranchRegistry`, `CommitGate`, deterministic control-plane tests, TGL lifecycle integration tests, and the dedicated v1 contract workflow. This work is implementation engineering only until exact-head CI and adversarial review establish verified capability.

Canonical architecture records:

- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`
- `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`
- `docs/architecture/DGAF_V1_AGENT_ROLE_MAPPING.md`

The control plane remains generic and substrate-agnostic. PDMAL remains an optional governed experimental substrate below it and is not a hidden dependency.

## Canonical agent-role boundary

The current Notion agent registry is authoritative for role identity/intent, while GitHub remains implementation/evidence truth. Current mapping for v1 is:

- **Sentinel-Phi** is the canonical Sentinel identity; `Sentinel` is historical alias only.
- **Professor Prodigy** remains non-orchestrating and focused on formalization/proof/category discipline.
- **DemiJoule** remains advisory/resource-efficiency focused and has no independent normative authorization.
- **Reciprocity** contributes fairness, affected-party, reciprocal-impact, perspective-equity, and asymmetry analysis within its existing contract.
- **Herald** handles evidence/public-surface publication and classification; it cannot manufacture evidence or approval.
- **Amethyst** coordinates meta-orchestration and lifecycle control; **COLLEEN** maintains continuity, archive, provenance, durable-state, and routing integrity; **Apogee** supports independent evidence/integrity review.

Generic v1 roles (`EXPLOIT`, `DIVERGE`, `VERIFY`, `GOVERN`) are execution contracts and do not create new agents or silently expand existing authority.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | `087f3d3050085c465a2beda96e12bc33537ca368` |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| TGL/P-35 remediation | ENGINEERING CANDIDATE | Superseding remediation work remains subject to exact-head validation |
| DGAF v1 control plane | IMPLEMENTATION CANDIDATE | Clean integration branch; deterministic tests and CI defined; not yet merge-verified |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure remains incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated runtime matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| New immutable freeze | NOT CREATED | No current candidate has crossed freeze boundary |
| Pilot authorization | NOT GRANTED | Separate explicit transition required |
| Empirical data | N = 0 | No authorized empirical pilot has executed |

## Exact current-main → production boundary

The latest Notion operational overlay reports that the observed READY Vercel production deployment is source-bound to `42346ecc34565502ebff02ead55a33b0d74246b8`, while current GitHub `main` is `087f3d3050085c465a2beda96e12bc33537ca368`. Exact current-main → production identity remains OPEN under GitHub Issue #137. This is a provenance/infrastructure execution boundary and does not alter experimental state.

## Experimental authorization boundary

No v1 control-plane implementation, CI result, deployment readiness result, Notion update, synthetic fixture, or expert-panel disposition may be used to infer PDMAL efficacy, create a freeze, grant authorization, unblind data, or increase empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
