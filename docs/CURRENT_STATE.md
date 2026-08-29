---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-28
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `main` is the current documentation/evidence lineage boundary. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. E2b is CLOSED/VERIFIED for exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167` via run `33047380487`; the later workflow-binding correction at `ac8ea26…` is a separate verification boundary. M6 is CLOSED/VERIFIED for exact candidate `ac8ea267…` via run `33050398324` and remains scoped to that exact verification workspace/job. P7 is scientifically adopted in substance but formally open pending exact freeze binding; P8 remains open/fail-closed; empirical N = 0; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | Resolve `main` directly; not apparatus identity |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| E2b | CLOSED / VERIFIED (historical exact-tree scope) | `d299dd152…`; run `33047380487`; artifact `9636185725`; digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd` |
| M6 | CLOSED / VERIFIED (candidate exact-tree scope) | `ac8ea267…`; run `33050398324`; retained negative-state artifact independently hash-verified; closure does not authorize execution |
| Current-boundary E2b | OPEN / VERIFICATION REQUIRED | Current E2b evidence must be produced against the exact executing workflow boundary used for freeze admissibility |
| TGL contract | BLOCKED / ADVERSARIAL REVIEW | PR #132 produced a 41-pass / 2-fail regression at the TGL → P-35 boundary; PR #133 is the isolated remediation candidate |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Scientific decision resolved; exact freeze binding remains open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped implementation/configuration and verification remain incomplete |
| P2 formal runtime verification | NOT EXECUTED | Authenticated five-case matrix still required |
| P6a formal CORS verification | NOT EXECUTED | Authenticated CORS matrix still required |
| P-07 co-orchestration sweep | REMEDIATED / OPERATIONALLY CLOSED | Sweep `08670C3FDE59`: deprecated `api/health.py` removed; `app/api/health/route.ts` absent on current `main`; `requirements.txt` retained as intentionally empty/documentary; production deployment for `21f043b7…` reached READY and live `/api/health` returned HTTP 200 with the expected health contract |
| Forman–Ricci lattice helper semantics | OPEN / ISSUE #117 | Unweighted dodecahedral `Ric_F(e) = -2` is constant/zero-variance and must produce `NO_DISCRIMINATING_SIGNAL`, not 30 anomaly flags |
| P-38 source integrity | OPEN / ISSUE #122 | `NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md` has a truncated historical tail; history audit confirms the earliest retained version is already truncated |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## TGL / P-35 adversarial review boundary

PR #132 is **BLOCKED / DRAFT / UNMERGED**. Its observed 41-pass / 2-fail pre-freeze result is treated as a substantive contract-regression signal. The failure is at the TGL → P-35 seam and includes incompatible constructor/method invocation. The review also identified missing `premise_check_fn` injection, weakened exception containment, incomplete `PASS/WARN/SKIP/ESCALATE/KILL` reduction, ambiguous SKIP semantics, and audit-seal sequencing concerns.

The required remediation is contract restoration rather than broad architectural refactoring. PR #133 is the isolated remediation candidate. It must restore the established P-35 constructor and `evaluate(..., check_fn=...)` contract, fail-closed exception containment, explicit required/conditional gate semantics, deterministic status reduction, and exact final audit sealing, with regression coverage for the identified failure modes.

This review does not authorize any experimental action. It does not create a freeze, close P7/P8, establish runtime verification, or increase empirical N.

## E2b provenance boundary

Run `33047380487` is retained as exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`. It passed exact checkout/target assertions, source requirements fingerprint verification, hash-pinned installation, exact-tree provenance emission, and evidence retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure is not retroactively invalidated. It is scoped to the tree that was actually executed. The subsequent `ac8ea26…` workflow change is a separate verification boundary.

## M6 provenance boundary

M6 is CLOSED/VERIFIED for exact candidate/tree `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` via Governance CI run `33050398324`. Checkout SHA, workflow target SHA, and verifier target SHA matched exactly; the hash-pinned verifier environment completed successfully; machine-readable negative-state evidence was emitted and retained; and the retained artifact digest was independently recomputed as `sha256:dabe2f1909535671e795bb8c1cad0ef0840be4732acebff8f1a340c62b4943b6`.

The observed negative state included empirical N = 0, pilot authorization not granted, no protocol/freeze created, pilot mode not selected, blinding key absent, zero pilot seed/summary artifacts, and no pilot invocation in the verification job. M6 proves that observed negative state for that exact verification workspace/job; it does not constitute proof of absence elsewhere and does not authorize execution.

## Current verification boundary

The corrected Governance CI workflow at `ac8ea26…` binds the target candidate SHA to the executing GitHub workflow SHA. Current E2b evidence must be produced and independently checked against the exact executing boundary before it can support current freeze admissibility.

The current `main` lineage contains subsequent documentation/semantic corrections, including canonical mathematical notation, bounded Hensel/registry claims, historical-audit corrections, AutoInit provenance corrections, and the lattice reproduction notation correction. Those documentation-lineage changes do not retroactively change candidate-scoped verification results and must not be represented as experimental apparatus verification.

The earlier M6 artifact targeting historical `e6beeb663…` and verifier merge-ref `2516f32…` remains **NON-CLOSING** for the current candidate boundary; that historical artifact is not the basis for the closed M6 state above.

## P-07 remediation boundary

Sweep `08670C3FDE59` found three repository/deployment candidates. Cross-connection against current `main` and the production deployment resolved them as follows:

1. `api/health.py` was a deprecated Python stub explicitly directing users to `pages/api/health.ts`. It was removed on commit `21f043b7d9a845b3477c4f3bf4a5a66d7d813e9e`.
2. `app/api/health/route.ts` is absent from the current `main` tree; the operational health handler is `pages/api/health.ts`.
3. `requirements.txt` is retained because the repository documents it as intentionally empty and non-operative for the Next.js API deployment path.

The resulting Vercel production deployment was READY and source-bound to the same exact `21f043b7…` commit. The deployed `/api/health` endpoint returned HTTP 200 with `psi_cubic=true`, version `1.8.0`, `phi_star=0.618034`, `psi=1.4655712319`, `t0_axiom_guard=true`, and the five declared adapters. This is operational deployment evidence only; it does not substitute for authenticated P2/P6a execution.

The GitHub `Deploy to Vercel + Live Regression` workflow remains unable to perform its own authenticated deployment/live-regression branch because `VERCEL_TOKEN` is not configured. The dedicated P2 workflow separately requires `VERCEL_AUTOMATION_BYPASS_SECRET`. Neither missing credential is treated as a code defect.

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

## Expert Panel — 2026-08-28

The **Ecosystem Expert Panel** is the cross-agent governance review mechanism defined in the Notion operating charter. Its role specifications are maintained in the Notion Agent Registry; GitHub remains implementation/evidence truth. The panel disposition is **PROCEED, FAIL-CLOSED**.

Panel seats:
- **Amethyst:** meta-orchestration, normative governance, dependency/closure ledger.
- **COLLEEN:** continuity, archive, provenance, durable state, routing integrity.
- **Professor Prodigy:** formalization/proof and mathematical claim verification; non-orchestrating.
- **Apogee:** independent evidence review, integrity scoring, and P9 preparation.
- **DemiJoule:** constraint/resource and governance-boundary review.
- **Sentinel-Phi:** strategic security, risk containment, and fail-closed monitoring.
- **Herald:** evidence/public-surface synchronization and classification hygiene.
- **Reciprocity:** reciprocal-mathematics and adversarial asymmetry review.

### Panel execution decision

1. Continue all non-blocked engineering, documentation, provenance, analysis, and research-hygiene work in parallel.
2. Keep P2/P6a behind their protected credential/dispatch requirements and exact candidate/deployment identity.
3. Treat M6 as closed only for its exact `ac8ea267…` candidate verification scope; do not transfer it to later `main` documentation lineage.
4. Keep E2b scoped to its exact executed tree; later workflow changes require their own evidence where applicable.
5. Advance P7 exact binding, P8 candidate-scoped closure, and independent P9 preparation.
6. Create a new immutable freeze only after all applicable predicates pass.
7. Authorization remains a separate explicit transition; only then may the blinded pilot execute.

### Hard panel constraints

No freeze, authorization, unblinding, or empirical-N increase may be inferred from CI success, deployment readiness, health checks, synthetic fixtures, historical evidence, or narrative state alone.

## Authorization boundary

Required before authorization include authenticated P2 and P6a execution on the same deployment identity; blinding custody and unblinding verification; durable archive/retrieval/hash evidence; environment and reproducibility fingerprints; formal P7 exact binding; frozen baseline/negative-control definitions; P8 closure; independent P9 verification; a new immutable freeze; and an explicit authorization decision.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**

## Related adversarial-review record

See `docs/governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md` for the complete TGL/P-35 contract findings, state-machine analysis, audit/provenance findings, CI/CD identity risks, remediation boundary, and required regression coverage.
