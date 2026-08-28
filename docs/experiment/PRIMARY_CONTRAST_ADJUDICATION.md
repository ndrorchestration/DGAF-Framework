---
status: ADOPTED_PENDING_EXACT_BINDING
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-28
applies_to_sha: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
---

# PDMAL Primary Contrast Adjudication

## Status

**CANDIDATE A SELECTED — SCIENTIFIC CONTENT ADOPTED; EXACT FREEZE BINDING OPEN**

The designated experimental-control authority adopted **Candidate A: DGAF vs null** for the current FFCR experiment on 2026-08-27. The adopted decision record is `docs/governance/P7_COMPLETION_ADJUDICATION_DRAFT_2026-08-23.md`. This record is synchronized to that decision and does not create a freeze, authorize the pilot, or constitute empirical validation.

## Authorized primary contrast

- **Primary contrast:** DGAF condition vs null condition.
- **Primary endpoint:** FFCR.
- **Statistical unit:** one root seed.
- **Primary comparison:** paired treatment/reference observations at identical root seeds and matched frozen matrix coordinates.
- **Primary estimand:** `theta = mean(FFCR_dgaf(seed) - FFCR_null(seed))` across complete analyzable paired seeds.
- **Direction:** higher FFCR is better; positive theta favors DGAF.
- **Primary inference:** two-sided 95% percentile paired-bootstrap CI over complete seed-level paired effects.
- **Bootstrap:** 10,000 resamples; RNG seed `20260823`; alpha `0.05`.
- **Success criterion:** valid authorized dataset + positive primary estimate + two-sided 95% CI wholly above zero.
- **Non-support/falsification:** CI including zero or non-positive estimate does not support the directional hypothesis; a CI wholly below zero opposes it under the frozen conditions.

### Secondary/exploratory contrasts

PDMAL-vs-Ring and condition × topology interaction remain secondary/exploratory. Confirmatory secondary claims require an explicitly bound multiplicity procedure; otherwise they remain exploratory/descriptive.

## Scientific scope

Candidate A tests the direct intervention-vs-control question: whether the configured DGAF condition changes FFCR relative to the null condition under the same execution contract. No historical PDMAL-vs-Ring result is inherited as a current hypothesis, expected direction, or empirical evidence.

## Exclusion and missingness rule

A seed is analyzable only when both primary paired condition-level FFCR values are computable from records satisfying the frozen artifact schema and matrix-completeness rules. No outcome-aware exclusion is permitted. Infrastructure/protocol failures must not be silently converted into efficacy outcomes or selectively dropped.

## Exact binding still required

The scientific P7 decision is adopted, but formal closure remains pending cryptographic binding to the exact admissible freeze identity, including the frozen protocol, runner/apparatus, artifact schema, analysis implementation/configuration, candidate identity, and freeze manifest.

The experimental verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Current `main` documentation/evidence changes must not be silently substituted for that candidate boundary.

## Governance boundary

- No freeze created.
- No pilot authorization.
- No unblinding.
- No pilot execution.
- Empirical data remain `N = 0`.
