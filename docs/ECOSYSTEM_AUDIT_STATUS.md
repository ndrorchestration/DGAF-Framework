# Ecosystem Audit Status

## Purpose

This document is the operational index for the current repository-wide epistemic/documentation audit. It complements `EPISTEMIC_SUPERSESSION_REGISTER.md` and records what has been checked, corrected, or remains outstanding.

## Canonical evidence rule

Repository-local implementation evidence takes precedence over inherited labels, historical claims, generated prose, or cross-repository attribution.

Use this status ladder:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

A repository relationship does not transfer verification status from one project to another.

## Completed README corrections

The following repositories have had their top-level README epistemic framing reconciled during this audit:

- `DGAF-Framework`
- `Acoustic-mesh`
- `AHG-Zeta-Pell-Autonomous-Lattice`
- `phi-calculus-app`
- `agent-control-plane`
- `Driftwatch`
- `ai-governance-frameworks`
- `Amethyst-Governance-Eval-Stack`
- `Gold-star-standards`
- `junior-apogee-app`
- `sentinel-governance`
- `resumeapex-eval`
- `AI-Prompt-Engineer` — explicitly classified as a historical portfolio archive

The exact commit history remains the authoritative record of individual edits.

## AHG Zeta-Pell audit

`AHG-Zeta-Pell-Autonomous-Lattice` remains a separate track from PDMAL.

Known Pass 1 findings include:

- conflicting AHG acronym expansions;
- misleading use of “Hecke Operator” for a stochastic admission threshold;
- unsupported 150x/180x/200x jitter claims;
- hardcoded benchmark values lacking in-place derivation;
- theorem-style claims exceeding their mathematical premises;
- incomplete traceability for the 7 → 4 → 2 recovery history.

The outstanding Pass 2 scope is the chaos/FML mitigation section and Three-Regime Governor, plus direct tracing of the recovery claim.

## PDMAL boundary

PDMAL is treated as its own track. Its confirmed lattice work is represented by `lattice_harness.py` and `lattice_formalization_corrected.md`.

Do not infer that AHG Zeta-Pell's silver-ratio control model and PDMAL's dodecahedral topology are one system merely because both use convergence/stability language.

## Historical records

Older issues, commits, and archived repositories may contain superseded certification, governance, benchmark, or production-readiness claims. They should be preserved as historical evidence unless there is a specific reason and permission to remove them.

Historical presence does not constitute current verification.

## Remaining work

### High priority

1. Audit remaining repository READMEs and major documentation for inherited terminology.
2. Sweep non-README documentation for stale certification, “validated,” “production-ready,” “industry first,” and unsupported numerical claims.
3. Complete AHG Zeta-Pell Pass 2.
4. Audit taxonomy/vocabulary artifacts for canonical meanings and epistemic status.
5. Reconcile GitHub repository descriptions/metadata where a repository-settings write path is available.

### Verification requirement

Do not mark an item `VERIFIED` merely because a README, benchmark dictionary, issue, or generated report says it is verified. Verification requires an inspectable method and evidence appropriate to the claim.

## Audit principle

**Preserve evidence. Classify claims. Correct current surfaces. Retain historical provenance. Require new evidence before upgrading status.**
