# DGAF Adversarial Pre-Freeze Assurance Matrix — 2026-08-31

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Purpose

This matrix is an adversarial review surface for foreseeable failure modes that could invalidate candidate identity, treatment/reference contrast, runtime integrity, evidence integrity, analysis, or independent verification. Each risk is assigned a control strategy: PREVENT, DETECT, BOUND, or ACCEPT.

## Assurance matrix

| Risk | Strategy | Control | Gate / owner | Fail-closed condition |
|---|---|---|---|---|
| Candidate SHA drift | PREVENT + DETECT | Bind apparatus SHA + tree SHA into candidate identity and every runtime/evidence artifact | P1/P3 | Any artifact source identity differs from candidate |
| Deployment/source mismatch | DETECT | Require deployment ID and Vercel Git source SHA to match candidate SHA | P2/P6a/P5 | Mismatch or unverifiable deployment source |
| Deployment environment drift | BOUND | Record runtime/build/dependency/environment fingerprint where available | P5 | Required fingerprint missing or inconsistent |
| Manual dispatch transcription error | DETECT | P2/P6a validate exact SHA, deployment ID, URL, and origin before execution | P2/P6a | Any input missing or malformed |
| Null-condition contamination | PREVENT + DETECT | Maintain explicit treatment/reference separation and adversarial null-integrity checks | P7/P8 | Null invokes treatment-specific semantics or receives disallowed information |
| Information leakage / future-state access | PREVENT + DETECT | Record allowed information boundary; prohibit future/downstream outcome access | P7/P8 | Any prohibited information enters treatment or reference path |
| Blinding failure | PREVENT | Opaque condition IDs, custody separation, no premature mapping release | P4 | Condition mapping exposed before authorized unblinding |
| Artifact mutation / corruption | DETECT | Emit cryptographic digest, preserve raw artifact, independently retrieve and re-hash | P3/P6 | Hash mismatch or incomplete custody |
| Protocol drift | DETECT + BOUND | Hash/identify governing protocol and retain deviation record | P5/P7/P8 | Unrecorded protocol deviation |
| Analysis drift / p-hacking | PREVENT | Lock primary endpoint, estimand, direction, inference method before freeze | P7/P8 | Primary analysis changed after freeze without governed amendment |
| Exploratory-to-primary leakage | BOUND | Separate locked primary analysis from clearly labeled exploratory work | P8 | Exploratory result substituted for predefined primary endpoint |
| P9 monoculture | PREVENT + DETECT | Independent verifier recomputes identity, hashes, primary statistic, and adversarial cases | P9 | Verification not meaningfully independent |
| Freeze binds wrong object | DETECT | Freeze self-check compares candidate, tree, protocol, dependency, deployment, P1–P9 status | Freeze control | Any identity/state inconsistency |
| Documentation drift | PREVENT + DETECT | Machine-readable control state plus synchronized human-facing documents | Control plane | Critical document contradicts machine-readable state |
| DemiJoule WARN unreachable | ACCEPT / BOUND | Document nominal vs reachable states; do not alter historical heuristic merely to manufacture WARN | Gate semantics | Documentation claims WARN was exercised when it was not |
| Vercel platform quota / availability | BOUND | Treat platform limit as infrastructure constraint; do not substitute preview health for runtime evidence | P2/P6a | Required authenticated runtime evidence unavailable |
| Runtime passive health appears clean | ACCEPT / BOUND | Use only as operational signal; never treat absence of errors as efficacy evidence | Deployment ops | Passive health is presented as scientific evidence |
| N=1 overinterpretation | PREVENT | Define N=1 as one valid paired observation, not efficacy | N=1 checkpoint | Any efficacy conclusion derived from N=1 alone |
| Unknown unknowns | ACCEPT / DETECT | Adversarial P9, explicit stopping rule, preserve anomalies and deviations | P9 / governance | Unresolved issue could plausibly invalidate validity predicates |

## Layered defense model

### L0 — Identity

Candidate, apparatus, deployment, protocol, and provenance identities must remain distinct and explicitly bound.

### L1 — Treatment integrity

The seven constitutive gates, null integrity, and information-access boundaries must be correct before scientific execution.

### L2 — Execution integrity

P2, P6a, P3, P4, P5, and P6 establish runtime, artifact, blinding, reproducibility, and custody controls.

### L3 — Scientific integrity

P7, P8, and P9 establish target definition, analysis lock, and independent verification.

### L4 — Governance integrity

Freeze and explicit execution authorization remain separate from all engineering and CI success.

## Universal control rule

Any layer may fail closed. No lower layer overrides a higher-layer failure. Passing one layer is not evidence that another layer has passed.

## Stopping rule

Further hardening stops when no unresolved issue remains that could plausibly invalidate candidate identity, treatment/reference contrast, primary endpoint, blinding, reproducibility, artifact integrity, primary analysis, or independent verification. Residual limitations must be recorded before freeze and may not be silently reclassified.

## Current residual accepted limitations

1. Vercel platform availability/quota is external infrastructure and cannot be made mathematically immutable by repository code.
2. Manual dispatch remains an operational dependency until a validated dispatch-capable integration exists.
3. DemiJoule WARN is a nominally defined but historically unreachable branch under the preserved heuristic.
4. Unknown unknowns cannot be eliminated; they are bounded through adversarial verification and the stopping rule.

**This matrix does not authorize execution or increase empirical N.**
