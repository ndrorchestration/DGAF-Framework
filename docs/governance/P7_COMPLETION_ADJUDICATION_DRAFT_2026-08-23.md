---
status: FORMALLY_OPEN
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
base_sha: e6beeb66335e1b50a239697badab22dab50eb5ba
empirical_n: 0
---

# P7 Completion Adjudication Draft — 2026-08-23

## Purpose and authority boundary

This is a proposed authoritative decision record, not evidence of execution and not pilot authorization. P7 is technically adjudicated but remains formally open until the designated experimental-control authority adopts the record and it is bound to the exact frozen protocol/apparatus identity.

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
8. **Bootstrap binding:** 10,000 resamples, bootstrap RNG seed `20260823`, alpha `0.05`, as specified in the current pre-freeze protocol. These bindings remain subject to final P8 lock and candidate-scoped verification.
9. **Secondary/exploratory contrasts:** PDMAL-vs-Ring and condition × topology interaction, plus other non-primary contrasts explicitly classified by P8.
10. **Multiplicity:** no adjustment for the single primary estimand; confirmatory secondary claims require a P8-specified multiplicity procedure, otherwise remain exploratory/descriptive.
11. **Exclusion/missingness:** a seed is analyzable only when both primary paired condition-level FFCR values are computable from records satisfying the frozen artifact schema and matrix-completeness rules. No outcome-aware exclusion is permitted. Infrastructure/protocol failures must not be silently converted into efficacy outcomes or selectively dropped.
12. **Success criterion:** valid authorized dataset + positive primary estimate + two-sided 95% CI wholly above zero.
13. **Falsification/non-support:** CI including zero or non-positive estimate does not support the directional hypothesis; a CI wholly below zero opposes it under the frozen conditions.

## Candidate and protocol binding

The current executable verification candidate is `e6beeb66335e1b50a239697badab22dab50eb5ba`.

Earlier candidate `83e1678f55d16f32b5ce363e091ac74479cbfe1f` is historical provenance only. Subsequent executable integrity corrections advanced the apparatus through a documented candidate chain culminating in `e6beeb...`; documentation-only successors do not redefine the executable candidate.

The current protocol is `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`. It remains **PRE-FREEZE** and records applicability to the current candidate. The protocol blob SHA must be bound explicitly by the P8 analysis lock; a moving branch/reference is insufficient.

This P7 record is not itself a freeze identity. Any material change to treatment/reference definitions, estimand, endpoint, exclusion rules, or statistical method requires re-adjudication.

## Closure matrix

| Requirement | Resolution | State |
|---|---|---|
| Primary contrast | DGAF vs null | Resolved |
| Reference definition | Configured null condition | Resolved pending exact freeze binding |
| Estimand | Mean paired seed-level FFCR difference | Resolved |
| Unit/pairing | Root seed; matched matrix | Resolved |
| Direction | Higher FFCR is better | Resolved |
| Aggregation | Equal-weight seed-level condition FFCR | Resolved |
| CI method | Two-sided 95% paired percentile bootstrap | Resolved pending P8 lock |
| Bootstrap | 10,000; seed `20260823` | Resolved pending P8 lock |
| Secondary contrasts | Topology/interaction exploratory | Resolved |
| Multiplicity | Primary unadjusted; secondary P8-defined | Resolved pending P8 lock |
| Exclusion/missingness | Pre-specified pair-completeness/audit rules | Resolved |
| Success criterion | Positive estimate + CI above zero | Resolved |
| Falsification | Non-support if non-positive/inconclusive; below-zero CI opposes | Resolved |
| Authority/adoption | Explicit adoption required | OPEN |
| Exact freeze identity | Must be bound at freeze | OPEN |

## Formal closure conditions

P7 **must remain OPEN** until:

1. the designated experimental-control authority explicitly adopts this decision record;
2. treatment/reference identifiers are verified against the exact frozen apparatus;
3. the adopted record is cryptographically bound to the exact protocol, runner/apparatus, analysis specification, and freeze manifest identities.

P7 closure does not authorize the pilot. P8, freeze, independent verification, and explicit pilot authorization remain separate gates. Empirical N remains **0**.
