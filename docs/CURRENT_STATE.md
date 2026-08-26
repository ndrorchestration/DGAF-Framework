---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: e6beeb66335e1b50a239697badab22dab50eb5ba
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `e6beeb66335e1b50a239697badab22dab50eb5ba` remains the executable verification candidate. Documentation successors on `main` do **not** redefine the apparatus. The candidate is pre-freeze; P7 is technically adjudicated but formally open; P8 remains open/fail-closed; empirical **N = 0**; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions are resolved; authority adoption and exact binding remain open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Corrective implementation work is present; formal runtime verification and binding remain incomplete |
| Exact verification candidate | IDENTIFIED | `e6beeb66335e1b50a239697badab22dab50eb5ba` is the executable candidate |
| Latest documentation successors | NON-APPARATUS | Baseline/negative-control/publication documentation only; do not redefine the apparatus |
| Vercel production deployment | READY | `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5` is bound to `e6beeb...`; `/api/health` passed |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| New immutable freeze | NOT CREATED | Candidate has not crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | P2/P6a, P4 custody, P5 fingerprint, P6 durable custody, and P9 remain open |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Documentation successor record

The following `main` commits are documentation-only and do not advance the executable apparatus candidate:

- `93b10d084ddb563d88b11818baad8b40565cb0ce` — negative-control matrix.
- `3d8b769aef2386efd8041d65eb187e61e6a7e7d1` — current-state candidate/documentation reconciliation.
- `340457c006610996eea0f89064ed64fa4e3a16c2` — H1–H3 publication mapping draft.
- `70b4b14805ad00668f9132b496a457f3f6bc4ba4` — H1–H3 preauthorization mapping and controls.
- `80ae53ab522bcbb64df0c60d172b3ff13626fc33` — current-state synchronization.
- `4e886d55402d138c6b399e5b25601440698c8316` — final H1–H3 mapping reconciliation.
- `0175b2270f71c02802ffdba7454eef93b5ba58b2` — P7 adjudication candidate-binding correction.
- `0b2f79e96fbc2d26b7722ce2b220d71ac112420b` — protocol candidate-binding correction.
- `2b6deed5706b74c302b500e5effd157b06669fe3` — README candidate synchronization.
- `9a6b26247d7ae727e4d65442bad5a8d4f6e7f260` — project-status candidate/deployment synchronization.
- `af0b14299aa82349fdc7fd10e2630de6bba0fd8e` — consolidated P8/P9/freeze readiness control.

Any executable change after `e6beeb...` would require candidate transition and fresh verification.

## Authorization boundary

Required before authorization:

- authenticated P2 runtime verification against the exact READY deployment;
- P6a CORS verification against the same deployment identity;
- blinding custody and unblinding procedure verification;
- durable archive/retrieval/hash evidence;
- environment fingerprint and reproducibility evidence;
- formal P7 authority adoption and exact binding;
- frozen baseline and negative-control definitions;
- frozen endpoints and statistical analysis plan;
- independent P9 verification;
- new immutable freeze creation and verification;
- explicit authorization decision.

The consolidated checklist is [`docs/governance/P8_P9_FREEZE_READINESS_2026-08-26.md`](governance/P8_P9_FREEZE_READINESS_2026-08-26.md).

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
