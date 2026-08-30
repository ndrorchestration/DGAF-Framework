# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment that produced it.

## Current project state — 2026-08-29

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No new experimental freeze exists, pilot authorization has not been granted, and empirical **N = 0**.

`main` is documentation/evidence lineage, not experimental apparatus identity. The experimental verification boundary remains candidate-scoped at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Any substantive apparatus change requires a new candidate identity and affected-predicate re-verification.

## Canonical engineering lane

**PR #139** is the current combined engineering candidate for DGAF v1 recursive control-plane implementation and TGL contract remediation. Earlier PRs #132/#133/#134 are historical or superseded records and are not separate current execution authorities.

The candidate covers inherited governance scope, deterministic lifecycle control, state identity, budget/concurrency accounting, branch provenance, explicit CommitGate authorization, fail-closed TGL semantics, complete audit sealing, adversarial regression coverage, and dedicated CI. It does not rebind PDMAL or authorize experimentation.

## Current TGL contract boundary

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure applies;
- HPG is conditional on Phi-Closure and cannot run after terminal failure;
- terminal failures stop downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid gate outcomes do not silently become PASS.

## Canonical agent-role boundary

- Sentinel-Phi — canonical governance/security identity.
- Professor Prodigy — formalization/proof; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis; no independent normative authorization.
- Reciprocity — fairness and affected-party review.
- Herald — evidence/public-surface publication; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity/archive/provenance/routing integrity.
- Apogee — independent evidence/integrity review.

Generic execution roles do not create or elevate agent authority.

## Experimental gate state

| Boundary | Status |
|---|---|
| Experimental verification boundary | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| P7 scientific decision | Adopted in substance; exact freeze binding open |
| P8 analysis lock | Open / fail-closed |
| P2 runtime verification | Not executed |
| P6a CORS verification | Not executed |
| New immutable freeze | Not created |
| Pilot authorization | Not granted |
| Empirical N | 0 |

## Deployment identity

The observed READY Vercel production deployment is not exact-current-main evidence because its source SHA `42346ecc34565502ebff02ead55a33b0d74246b8` does not equal the current GitHub `main` identity. Issue #137 remains the canonical deployment-provenance tracker.

## Evidence boundary

Engineering CI success, synthetic fixtures, deployment readiness, or documentation updates do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence is not transferable across SHA/run/deployment boundaries without fresh exact-scope evidence.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
