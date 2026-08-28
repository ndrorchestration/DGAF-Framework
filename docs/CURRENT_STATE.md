---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-28
applies_to_sha: 3f2d16a45871b25cd98cd5f7ae69451abc523543
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `3f2d16a45871b25cd98cd5f7ae69451abc523543` is the current `main` documentation/evidence lineage boundary. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. E2b is CLOSED/VERIFIED for exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167` via run `33047380487`; the later workflow-binding correction at `ac8ea26…` requires current-tree execution before that evidence can be used as current-tree freeze evidence. M6 remains open. P7 is technically adjudicated but formally open; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | `3f2d16a45871b25cd98cd5f7ae69451abc523543` |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| E2b | CLOSED / VERIFIED (historical exact-tree scope) | `d299dd152…`; run `33047380487`; artifact `9636185725`; digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd` |
| Current-tree E2b/M6 binding | READY / VERIFICATION PENDING | Governance CI binds the candidate target to the executing workflow SHA at `ac8ea26…`; exact current-boundary execution remains required |
| M6 | OPEN / CURRENT-TREE VERIFICATION REQUIRED | Historical `e6beeb…` evidence is non-closing; current-tree evidence not yet observed |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions resolved; authority adoption and exact binding remain open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped implementation/configuration and verification remain incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| Forman–Ricci lattice helper semantics | OPEN / ISSUE #117 | Unweighted dodecahedral `Ric_F(e) = -2` is constant/zero-variance and must produce `NO_DISCRIMINATING_SIGNAL`, not 30 anomaly flags |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## E2b provenance boundary

Run `33047380487` is retained as exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`. It passed exact checkout/target assertions, source requirements fingerprint verification, hash-pinned installation, exact-tree provenance emission, and evidence retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure is not retroactively invalidated. It is simply scoped to the tree that was actually executed. The subsequent `ac8ea26…` workflow change is a new verification boundary.

## Current-tree verification boundary

The corrected Governance CI workflow at `ac8ea26…` binds the target candidate SHA to the executing GitHub workflow SHA. This removes the previous hard-coded historical-candidate rebinding path. Current-tree M6/E2b evidence must be produced and independently checked before it can support current freeze admissibility.

The current `main` tip `3f2d16a…` contains subsequent documentation/semantic corrections, including the Platinum Mean terminology correction and the open Forman–Ricci helper semantics issue. Those documentation-lineage changes do not retroactively change the candidate-scoped verification result for `ac8ea26…` and must not be represented as experimental apparatus verification.

The earlier M6 artifact targeting historical `e6beeb663…` and verifier merge-ref `2516f32…` remains **NON-CLOSING** for the current candidate boundary.

## Semantic correction boundary

`pP` / **Platinum Mean** is intentional DGAF notation for the regular-hendecagon unit-side circumradius, `1/(2 sin(π/11)) ≈ 1.774732842`. `ρP` / **plastic constant** is `1.3247179572447454`, the real root of `x³ = x + 1`. The notation is intentional; the correction is that `1.7747…` must not be misidentified as the plastic constant in mathematical convergence claims.

For the unweighted regular dodecahedral topology, Forman–Ricci curvature is `Ric_F(e) = -2` for every edge. This is a constant metric with zero variance and therefore **NO_DISCRIMINATING_SIGNAL**. Issue #117 remains open until the helper's output semantics are corrected and regression-tested. Weighted Forman–Ricci remains separately governed as a falsification track; no validation claim follows from the current single-configuration computation.

## Authorization boundary

Required before authorization include authenticated P2 and P6a execution on the same deployment identity; blinding custody and unblinding verification; durable archive/retrieval/hash evidence; environment and reproducibility fingerprints; formal P7 adoption/binding; frozen baseline/negative-control definitions; P8 closure; independent P9 verification; a new immutable freeze; and an explicit authorization decision.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
