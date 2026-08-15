# Ecosystem Evidence & Discrepancy Ledger — 2026-08-15

## Purpose

Canonical cross-repository ledger for documentation, implementation, test, benchmark, terminology, and epistemic-status discrepancies identified during the 2026-08-15 quality audit.

## Evidence rule

A capability is not promoted to `VERIFIED` merely because a README, test file, CI workflow, benchmark dictionary, or configuration exists. Promotion requires an identifiable current execution path plus reproducible evidence. CI configuration is not the same as a successful CI run; a benchmark definition is not an achieved benchmark; an internal rubric is not external certification.

## Closed findings

| Area | Finding | Disposition |
|---|---|---|
| AHG nomenclature | `AHG` had competing expansions | Canonicalized to **Adaptive Harmonic Governance**; older variants retained only as historical/superseded terminology |
| PDMAL / Zeta-Pell | Systems were thematically similar but not the same system | Explicitly separated; no merger or mutual validation implied |
| Zeta-Pell Hecke terminology | Stochastic threshold was described as a Hecke operator | Classified as misleading metaphor; do not present as a Hecke implementation |
| Zeta-Pell jitter multipliers | 150x/180x/200x claims lacked a defined 1x denominator | Unsupported until reproducibly defined and computed |
| Zeta-Pell 12x multiplier | Arithmetic valid; derivation was not theorem-level | Retain only as an engineering hypothesis/design margin |
| Zeta-Pell silver-ratio theorem | Silver-ratio/Pell identity valid; stability/entropy conclusion not derived | Premise retained; conclusion downgraded to unproven |
| Zeta-Pell benchmark dictionaries | Hardcoded benchmark literals were presented as final evidence | Classified declarative; recomputation required for verification |
| Zeta-Pell 4→2 recovery | Intermediate 4-cycle result is traceable; final derivation not fully audited | Pass 2 pending source notebooks |
| Taxonomy CSV | `Key Feature/Distinction` column was empty | Populate or remove before portfolio release |
| 3D visualization README | Production/cost/runtime claims exceeded available evidence | README corrected; configuration/deployment/runtime evidence explicitly separated |
| KAPPA `HACK` marker | Marker referred to a documented predicate-shadowing correction | Classified historical/implemented fix, not unresolved debt |
| Junior Apogee legacy governance | Legacy `no_hallucination` check is a placeholder | Legacy only; not evidence of current hallucination detection |
| Junior Apogee current stack | Newer evaluation infrastructure exists | Must trace current execution path before promoting capability claims |
| Junior Apogee CI | Workflow definition includes tests/build/release gates | CI configured is verified; particular successful run is not attested from currently accessible evidence |
| ResumeApex CI/benchmark | Workflow and benchmark protocol exist | Benchmark target is not treated as achieved or statistically validated without run evidence |

## Repository status

### Current-facing documentation

Major README sweep completed across the active repository set. Repositories already meeting the epistemic standard were not rewritten unnecessarily. `3d-visualization-hub` required and received a correction.

### Infrastructure / governance

`Acoustic-mesh`, `agent-control-plane`, `ai-governance-frameworks`, and `Gold-star-standards` were checked and found substantially aligned with the evidence model.

### Application / evaluation

`junior-apogee-app`, `resumeapex-eval`, `Driftwatch`, `Amethyst-Governance-Eval-Stack`, `ai-prompt-systems-portfolio`, `phi-calculus-app`, and `sentinel-governance` were brought into the claim-to-evidence review perimeter. Presence of tests/evaluators is not itself treated as capability verification.

## Open items

1. **Zeta-Pell Pass 2** — source-level review of the original notebooks remains pending. Do not promote disputed claims.
2. **Current-path tracing** — finish direct claim → implementation → test → result tracing for application/evaluation repositories where multiple generations coexist.
3. **CI attestation** — obtain valid workflow-run identifiers/logs before describing specific runs as passed.
4. **Benchmark provenance** — distinguish target, computed result, historical result, and independently reproduced result.
5. **Taxonomy CSV** — resolve the empty `Key Feature/Distinction` column.

## Canonical status vocabulary

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

A lower-evidence state must not be silently promoted to a higher state through repetition across documentation.

## Audit boundary

Historical audit documents may preserve erroneous or deprecated terminology when necessary to establish provenance. Current-facing specifications must use canonical terminology and evidence status. Cross-repository association does not establish validation, causality, or implementation equivalence.
