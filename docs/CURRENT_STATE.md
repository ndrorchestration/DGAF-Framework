---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-28
applies_to_sha: 1414ab33cd631a737338682faf2686977b8f9a69
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `1414ab33cd631a737338682faf2686977b8f9a69` is the current `main` documentation/evidence lineage boundary. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. E2b is CLOSED/VERIFIED for exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167` via run `33047380487`; the later workflow-binding correction at `ac8ea26…` is a separate verification boundary. M6 is CLOSED/VERIFIED for exact candidate `ac8ea267…` via run `33050398324` and remains scoped to that exact verification workspace/job. P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | `1414ab33cd631a737338682faf2686977b8f9a69` |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| E2b | CLOSED / VERIFIED (historical exact-tree scope) | `d299dd152…`; run `33047380487`; artifact `9636185725`; digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd` |
| M6 | CLOSED / VERIFIED (candidate exact-tree scope) | `ac8ea267…`; run `33050398324`; retained negative-state artifact independently hash-verified; closure does not authorize execution |
| Current-boundary E2b | OPEN / VERIFICATION REQUIRED | Current E2b evidence must be produced against the exact executing workflow boundary used for freeze admissibility |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Scientific decision resolved; exact freeze binding remains open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped implementation/configuration and verification remain incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| Forman–Ricci lattice helper semantics | OPEN / ISSUE #117 | Unweighted dodecahedral `Ric_F(e) = -2` is constant/zero-variance and must produce `NO_DISCRIMINATING_SIGNAL`, not 30 anomaly flags |
| P-38 source integrity | OPEN / ISSUE #122 | `NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md` has a truncated historical tail; history audit confirms the earliest retained version is already truncated |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## E2b provenance boundary

Run `33047380487` is retained as exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`. It passed exact checkout/target assertions, source requirements fingerprint verification, hash-pinned installation, exact-tree provenance emission, and evidence retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure is not retroactively invalidated. It is scoped to the tree that was actually executed. The subsequent `ac8ea26…` workflow change is a separate verification boundary.

## M6 provenance boundary

M6 is CLOSED/VERIFIED for exact candidate/tree `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` via Governance CI run `33050398324`. Checkout SHA, workflow target SHA, and verifier target SHA matched exactly; the hash-pinned verifier environment completed successfully; machine-readable negative-state evidence was emitted and retained; and the retained artifact digest was independently recomputed as `sha256:dabe2f1909535671e795bb8c1cad0ef0840be4732acebff8f1a340c62b4943b6`.

The observed negative state included empirical N = 0, pilot authorization not granted, no protocol/freeze created, pilot mode not selected, blinding key absent, zero pilot seed/summary artifacts, and no pilot invocation in the verification job. M6 proves that observed negative state for that exact verification workspace/job; it does not constitute proof of absence elsewhere and does not authorize execution.

## Current verification boundary

The corrected Governance CI workflow at `ac8ea26…` binds the target candidate SHA to the executing GitHub workflow SHA. Current E2b evidence must be produced and independently checked against the exact executing boundary before it can support current freeze admissibility.

The current `main` tip `1414ab33…` contains subsequent documentation/semantic corrections, including canonical mathematical notation, bounded Hensel/registry claims, historical-audit corrections, AutoInit provenance corrections, and the lattice reproduction notation correction. Those documentation-lineage changes do not retroactively change candidate-scoped verification results and must not be represented as experimental apparatus verification.

The earlier M6 artifact targeting historical `e6beeb663…` and verifier merge-ref `2516f32…` remains **NON-CLOSING** for the current candidate boundary; that historical artifact is not the basis for the closed M6 state above.

## Canonical mathematical notation boundary

`φ` is the conventional symbol for the Golden Ratio, `(1+√5)/2 ≈ 1.618033989`.

`σ_{p,q}` denotes the Spinadel metallic-means family, the positive solution of `x² - px - q = 0`; `σ_n = σ_{n,1}` for the ordinary sequence. `σ_{2,1}` is silver and `σ_{3,1}` is bronze.

`ρ` denotes the mathematical plastic number, `≈1.3247179572447454`, the unique real root of `x³ - x - 1 = 0`. `P` is an attested alternative notation. `ρP` is not the canonical mathematical notation.

`pP` / **Platinum Mean** is intentional DGAF-specific notation for the regular-hendecagon unit-side circumradius, `1/(2 sin(π/11)) ≈ 1.774732842`. It is not a standard member of the quadratic metallic-means family and must not be substituted for `ρ` in plastic-number mathematics.

The authoritative notation policy is `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`. Historical `ρP` references are retained only as provenance/supersession evidence and must not be treated as current mathematical authority.

## Forman–Ricci evidence boundary

For the unweighted regular dodecahedral topology, Forman–Ricci curvature is `Ric_F(e) = -2` for every edge. This is a constant metric with zero variance and therefore **NO_DISCRIMINATING_SIGNAL**. Issue #117 remains open until the helper's output semantics are corrected and regression-tested. Weighted Forman–Ricci remains separately governed as a falsification track; no validation claim follows from the current single-configuration computation.

## P-38 source-integrity boundary

Issue #122 tracks the incomplete P-38 substrate-study tail. A Git history audit on 2026-08-28 confirmed that the earliest retained P-38 commit (`8807dc5c…`, 2026-06-13) already ends at the same `Bit-identical a_n replay va...` boundary. The later correction commit therefore did not remove recoverable source text from the retained history; no authoritative remainder has been reconstructed. The issue remains open pending a provenance-controlled external or otherwise authoritative source. This is documentation/source-integrity remediation only and does not advance experimental gates.

## Authorization boundary

Required before authorization include authenticated P2 and P6a execution on the same deployment identity; blinding custody and unblinding verification; durable archive/retrieval/hash evidence; environment and reproducibility fingerprints; formal P7 exact binding; frozen baseline/negative-control definitions; P8 closure; independent P9 verification; a new immutable freeze; and an explicit authorization decision.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
