---
status: ADOPTED_PENDING_BINDING
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
base_sha: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
empirical_n: 0
adopted_by: ndrorchestration
adopted_on: 2026-08-27
adoption_basis: explicit experimental-control instruction in ChatGPT session
binding_status: PENDING_EXACT_FREEZE_IDENTITY
---

# P7 Completion Adjudication — Adopted Decision Record

## Authority boundary
This record is now **adopted** by the designated experimental-control authority for the scientific decision. Adoption does not itself create a freeze, authorize the pilot, or constitute empirical validation.

## Primary decision

**Primary contrast: full `dgaf` condition versus `null` condition on FFCR.**

Candidates B (PDMAL vs Ring) and C (condition × topology interaction) remain secondary/exploratory and are not promoted to the primary endpoint.

## Decision record

1. **Treatment:** configured `dgaf` condition under the frozen apparatus.
2. **Reference/null:** configured `null` condition under the same apparatus, with the DGAF intervention absent as defined by the condition registry/runner.
3. **Unit of analysis:** one root seed; treatment/reference observations are paired by identical root seed and matched frozen matrix coordinates.
4. **Primary endpoint:** FFCR (failure-free completion proportion), calculated per condition per seed from the complete topology × failure-count matrix. `ffcr_success` is the explicit execution outcome; it is not reconstructed from `final_std`.
5. **Estimand:** mean paired seed-level effect, `theta = mean(FFCR_dgaf(seed) - FFCR_null(seed))`.
6. **Direction:** higher FFCR is better; positive theta favors DGAF.
7. **Primary inference:** two-sided 95% percentile paired-bootstrap CI over complete seed-level paired effects.
8. **Bootstrap binding:** 10,000 resamples, bootstrap RNG seed `20260823`, alpha `0.05`.
9. **Secondary/exploratory contrasts:** PDMAL-vs-Ring and condition × topology interaction, plus other non-primary contrasts explicitly classified by P8.
10. **Multiplicity:** no adjustment for the single primary estimand; confirmatory secondary claims require a P8-specified multiplicity procedure, otherwise remain exploratory/descriptive.
11. **Exclusion/missingness:** a seed is analyzable only when both primary paired condition-level FFCR values are computable from records satisfying the frozen artifact schema and matrix-completeness rules. No outcome-aware exclusion is permitted. Infrastructure/protocol failures must not be silently converted into efficacy outcomes or selectively dropped.
12. **Success criterion:** valid authorized dataset + positive primary estimate + two-sided 95% CI wholly above zero.
13. **Falsification/non-support:** CI including zero or non-positive estimate does not support the directional hypothesis; a CI wholly below zero opposes it under the frozen conditions.

## Current exact-tree boundary
Current verified implementation/evidence tree: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`.

Historical candidate references, including `e6beeb…`, `83e1678…`, and earlier freeze candidates, remain provenance only.

## Closure status
P7 scientific content is **ADOPTED**. Formal P7 closure remains **PENDING** until the adopted decision is cryptographically bound to the exact frozen protocol, runner/apparatus, analysis specification, and freeze manifest identity.

## Governance boundary
- No freeze created.
- No pilot authorization.
- No unblinding.
- No pilot execution.
- Empirical N remains 0.

P7 adoption is a governance decision; it is not empirical evidence.
