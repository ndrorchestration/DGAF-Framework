---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-27
applies_to_sha: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` is the current `main` verification boundary. E2b is CLOSED/VERIFIED for exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167` via run `33047380487`; the later workflow-binding correction at `ac8ea26…` requires current-tree execution before that evidence can be used as current-tree freeze evidence. M6 remains open. P7 is technically adjudicated but formally open; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| E2b | CLOSED / VERIFIED (historical exact-tree scope) | `d299dd152…`; run `33047380487`; artifact `9636185725`; digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd` |
| Current-tree E2b/M6 binding | READY / VERIFICATION PENDING | Governance CI binds `PDMAL_TARGET_CANDIDATE_SHA` to `${{ github.sha }}` at `ac8ea26…` |
| M6 | OPEN / CURRENT-TREE VERIFICATION REQUIRED | Historical `e6beeb…` evidence is non-closing; current-tree evidence not yet observed |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions resolved; authority adoption and exact binding remain open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped implementation/configuration and verification remain incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## E2b provenance boundary

Run `33047380487` is retained as exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`. It passed exact checkout/target assertions, source requirements fingerprint verification, hash-pinned installation, exact-tree provenance emission, and evidence retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure is not retroactively invalidated. It is simply scoped to the tree that was actually executed. The subsequent `ac8ea26…` workflow change is a new verification boundary.

## Current-tree verification boundary

The corrected Governance CI workflow at `ac8ea26…` binds the target candidate SHA to the executing GitHub workflow SHA. This removes the previous hard-coded historical-candidate rebinding path. Current-tree M6/E2b evidence must be produced and independently checked before it can support current freeze admissibility.

The earlier M6 artifact targeting historical `e6beeb663…` and verifier merge-ref `2516f32…` remains **NON-CLOSING** for the current tree.

## Authorization boundary

Required before authorization include authenticated P2 and P6a execution on the same deployment identity; blinding custody and unblinding verification; durable archive/retrieval/hash evidence; environment and reproducibility fingerprints; formal P7 adoption/binding; frozen baseline/negative-control definitions; P8 closure; independent P9 verification; a new immutable freeze; and an explicit authorization decision.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
