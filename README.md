# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and the current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment that produced it.

## Current project state — 2026-08-29

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No new experimental freeze exists, pilot authorization has not been granted, and empirical **N = 0**.

`main` is documentation/evidence lineage, not experimental apparatus identity. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Any substantive apparatus change requires a new candidate identity and affected-predicate re-verification.

### Canonical engineering lane

**PR #139** (`feat/dgaf-v1-control-plane-finalize-20260829`) is the current combined engineering candidate for the governed recursive control plane and TGL contract remediation. It is based on current `main` and is non-authorizing.

The candidate covers inherited governance scope, deterministic lifecycle control, state identity, budget/concurrency accounting, branch provenance, explicit CommitGate authorization, TGL integration, adversarial regression coverage, and dedicated CI. It does not rebind PDMAL or authorize experimentation.

### Current TGL contract boundary

The TGL contract is fail-closed:

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure applies;
- HPG is conditional on Phi-Closure and cannot run after terminal failure;
- the final audit seal covers the complete gate set, including Herald;
- gate outcomes are validated rather than silently coerced to PASS.

PR #132 is historical diagnostic material. PR #133 is historical remediation material. PR #134 is superseded by PR #139 and is not a separate current engineering authority.

## Layer-0 human / rights / societal boundary

DGAF treats human dignity, human rights, safety, lawful operation, privacy, non-discrimination, human agency, legitimate oversight, public accountability, and appropriate disclosure as a shared constitutional substrate preceding technical optimization.

The current authority mapping remains:

- Sentinel-Phi — canonical governance/security identity.
- Professor Prodigy — formalization/proof; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis.
- Reciprocity — fairness and affected-party review.
- Herald — evidence/public-surface publication; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity/archive/provenance/routing integrity.
- Apogee — independent evidence/integrity review.

Generic control-plane roles do not create or elevate agent authority.

## Epistemic standard

Claims progress through defined → implemented → computed → verified → attested → authorized → canonical. Similarity, repetition, confidence, deployment readiness, or synthetic tests do not by themselves establish independent validation, efficacy, safety, certification, or legal compliance.

## PDMAL/DGAF status

| Boundary | Status |
|---|---|
| Current `main` | Documentation/evidence lineage |
| Experimental verification boundary | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| P7 scientific decision | Adopted in substance; exact freeze binding open |
| P8 analysis lock | Open / fail-closed |
| P2 runtime verification | Not executed |
| P6a CORS verification | Not executed |
| New immutable freeze | Not created |
| Pilot authorization | Not granted |
| Empirical N | 0 |

## Deployment identity

The observed READY Vercel production deployment is not current-main evidence because its source SHA `42346ecc34565502ebff02ead55a33b0d74246b8` does not equal the current GitHub `main` identity. Issue #137 is the canonical deployment-provenance tracker.

## Evidence boundary

CI results and engineering changes remain exact-head evidence. Historical results are not transferred to later commits without new exact-scope execution. Engineering completion never creates experimental authorization.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
