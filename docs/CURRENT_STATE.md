---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-29
applies_to_ref: main
---
# DGAF / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain governed by the project's formal process. Historical evidence stays scoped to the exact SHA, run, deployment, environment, and artifact that produced it.

## At a glance

| Boundary | Current state |
|---|---|
| Engineering | **ACTIVE — PR #139** |
| Current `main` | Documentation/evidence lineage; not automatically the experimental apparatus identity |
| Experimental candidate | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| PDMAL | **PRE-FREEZE / FAIL-CLOSED** |
| Pilot authorization | **NOT GRANTED** |
| New immutable freeze | **NOT CREATED** |
| Empirical N | **0** |

## Current engineering lane

PR #139 is the current DGAF engineering lane. It consolidates governed control-plane work, authority inheritance, bounded execution, deterministic lifecycle behavior, provenance, authorization barriers, and TGL hardening.

Its substantive implementation checkpoint `a728ce3ee8a024646c0971c9d4f392abaa3d691a` completed dedicated control-plane/TGL/adversarial/capability-boundary verification with **41/41 tests passing** in run `33247361730`. Later commits on the PR are documented as documentation, governance, CI, and provenance-hardening changes; the 41/41 result remains scoped to the exact checkpoint.

Earlier TGL remediation PRs #132 and #133 are historical remediation records. The current engineering narrative should use PR #139 unless a forensic record specifically requires the earlier history.

## Experimental boundary

PDMAL remains separately governed from the engineering track. The current candidate is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`.

No new freeze has been created. Pilot authorization has not been granted. No authorized empirical pilot has been executed; **N = 0**.

Documentation or engineering changes do not rebind the experimental apparatus. A substantive apparatus change requires a new candidate identity and the applicable predicate re-verification.

## Gate board

| Gate / control | Status | Meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b868…` remains provenance only |
| E2b | CLOSED / VERIFIED | Exact historical tree `d299dd152…`; run `33047380487` |
| M6 | CLOSED / VERIFIED | Exact candidate `ac8ea267…`; run `33050398324` |
| Current-boundary E2b | OPEN | Verification against the executing workflow boundary remains required where freeze admissibility depends on it |
| TGL contract | ENGINEERING / HARDENING | Current work is in PR #139; earlier #132/#133 records are historical |
| P2 runtime verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| P6a CORS verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| P4 security / blinding | OPEN | Current custody verification required |
| P5 provenance / reproducibility | OPEN | Current execution packet required |
| P6 durable evidence custody | OPEN | Current archive/retrieval/hash proof required |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure required |
| P9 independent verification | NOT EXECUTED | Independent review required |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate explicit governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## TGL / P-35 review

A prior remediation sequence exposed a substantive TGL → P-35 contract regression. The associated **41-pass / 2-fail** result is a diagnostic finding scoped to the historical candidate that produced it; it is not a current system-wide failure rate or efficacy measurement.

The review identified constructor/method compatibility, premise-hook injection, exception containment, deterministic `PASS / WARN / SKIP / ESCALATE / KILL` reduction, required-versus-conditional `SKIP` semantics, and audit-seal sequencing as areas requiring hardening.

See [`governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md`](governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md) for the forensic record and PR #139 for the current engineering lane.

## Verification boundaries

### E2b

Run `33047380487` remains exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`. Its retained artifact is scoped to that execution. Later workflow or source changes require their own verification where applicable.

### M6

Run `33050398324` remains candidate-scoped evidence for `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Its closure demonstrates the observed negative-state controls for that exact verification workspace/job; it does not authorize execution or prove absence outside that scope.

## Deployment boundary

A previously identified READY production deployment remains supporting operational evidence. Formal P2 and P6a claims require authenticated execution against the exact deployment identity. Deployment readiness and a live health response do not substitute for those verification predicates.

## Mathematical notation

`φ` denotes the Golden Ratio, `(1+√5)/2 ≈ 1.618033989`.

`ρ` denotes the mathematical plastic number, approximately `1.3247179572447454`, the unique real root of `x³ - x - 1 = 0`.

`pP` / **Platinum Mean** is intentional DGAF-specific notation for `1/(2 sin(π/11)) ≈ 1.774732842`. It is not presented as a universal mathematical symbol or as a member of the quadratic metallic-means family. It must not replace `ρ` in plastic-number convergence mathematics.

See [`governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md) for the authoritative notation policy.

## Other tracked boundaries

- **Issue #117:** unweighted dodecahedral Forman–Ricci curvature is constant (`Ric_F(e) = -2`) and therefore represents `NO_DISCRIMINATING_SIGNAL`; implementation/output semantics remain open.
- **Issue #122:** P-38 source-integrity record has an incomplete historical tail; provenance-controlled reconstruction remains open.
- **Issue #137:** deployment/source-provenance gate remains part of the engineering closure path.

## Expert review

The cross-agent expert review disposition remains **PROCEED, FAIL-CLOSED**. Its purpose is to support evidence review, risk containment, provenance, mathematical review, and governance coordination; it does not create technical or experimental authority by itself.

## Authorization boundary

Authorization requires completion of the applicable runtime, security/blinding, provenance, durable-custody, P7, P8, and independent-verification requirements; creation and verification of a new immutable freeze; and an explicit authorization decision.

**Current conclusion: engineering is active. PDMAL remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N = 0.**

## Documentation controls

Public and project-facing documentation follows [`governance/DOCUMENTATION_STYLE_GUIDE.md`](governance/DOCUMENTATION_STYLE_GUIDE.md) and [`governance/PUBLIC_SURFACE_QA_STANDARD.md`](governance/PUBLIC_SURFACE_QA_STANDARD.md). Detailed evidence and forensic history belong in their canonical lower-level records rather than being duplicated in this summary.
