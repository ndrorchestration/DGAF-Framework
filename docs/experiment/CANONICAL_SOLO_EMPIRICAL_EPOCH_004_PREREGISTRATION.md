# Canonical Solo Empirical Epoch 004 — Preregistration Proposal

## Status

`PROPOSAL_ONLY / NOT AUTHORIZED / SCIENTIFIC_N_INCREMENT=0`

This document prospectively specifies a possible fresh Solo empirical test of the canonical DGAF treatment established through PRs #378–#380. It does **not** authorize collection.

## Canonical treatment identity

- Epoch ID: `PDMAL-SOLO-CANONICAL-EPOCH-004`
- Treatment profile: `DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1`
- Profile merge: `c8a07306d212e23cc5a4c1e0d98b7e8f47f45e21`
- Qualification merge: `2fbd54454ad45df26cdd3b51793268ac3e597336`
- Qualification SHA-256: `4d0346f6a05046f03ce5a399d1dd4de2d31b69f683988fe9af20802d2c062d78`
- Qualification class: `DEVELOPER_SELF_ATTESTED_NONINDEPENDENT`
- Treatment-reachability merge: `621356297f803f0a3e8e3319d54878a5bb0282a5`
- Reachability run: `34176977560`
- Reachability artifact: `10037645166`
- Reachability artifact digest: `sha256:814222ba8fad2d1ef7dbd6d620fe0620f31e7a74c27d13b20f054c82efb90aa4`
- Required TGL steps: `{1,2,3,4,5,6,8}`

The treatment uses external source-bound P-30/P-11 11Q qualification verification at TGL step 8. The retired scalar `LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1` is not part of this treatment.

## Experimental matrix

- Conditions: `null`, `simple`, `static`, `dgaf`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0,1,2,3,4,5,6,8,10`
- Fresh prospective seed range: `20261001..20261050`
- Seeds: `50`
- Cells per seed: `4 × 5 × 9 = 180`
- Expected observations: `9,000`

The seed range is fixed before collection. It is disjoint from experiment 001 (`20260819..20260868`) and Epoch 003 (`20260901..20260950`). Prior empirical outcomes were not used to select individual seeds.

## Locked primary analysis

To avoid outcome-driven methodological tuning, the primary statistical contract remains unchanged from the already-frozen PDMAL analysis primitive:

- Source: `experiments/pdmal_pilot/analysis.py`
- Source blob: `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`
- Analysis-config SHA-256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`
- Primary contrast: `dgaf - null`
- Unit: paired seed
- Estimand: mean paired seed-level FFCR difference
- Bootstrap: paired-seed percentile bootstrap, `10,000` resamples
- Bootstrap RNG seed: `20260823`
- Alpha: `0.05`
- Directional support: estimate `> 0` and two-sided 95% bootstrap CI lower bound `> 0`
- Negative directional evidence: estimate `<= 0` and CI upper bound `< 0`
- Otherwise: not supported or inconclusive

No endpoint, exclusion rule, sample size, seed panel, bootstrap rule, or classification rule may be changed after collection begins without invalidating confirmatory interpretation.

## Required pre-collection controls

Before an execution request can be considered:

1. Implement a canonical Epoch 004 runner on a separate branch/PR.
2. Bind the runner to the exact profile, qualification, reachability, protocol, dependencies, and required TGL steps above.
3. Add a treatment-input preflight that exits before collection if any required source/binding is absent, stale, malformed, or mismatched.
4. Demonstrate the preflight and negative controls non-empirically.
5. Freeze the exact runner and analysis identities after complete exact-head CI.
6. Define fresh condition blinding/order and same-system Solo key custody explicitly as non-independent.
7. Define per-seed structural hashes/sidecars and expected complete matrix checks.
8. Require a blinded dataset structural lock before any key release.
9. Require a separate post-lock unblinding authorization.
10. Require empirical execution from an exact frozen commit whose sole change is a machine-readable execution request.

## Historical evidence separation

- Solo Pilot: QC evidence only, N=360.
- Experiment 001: N=9,000 retained apparatus-falsification evidence; not valid intended-efficacy evidence.
- Epoch 002: non-empirical diagnostic, N increment 0.
- Epoch 003: N=9,000 negative evidence for `DGAF-P30-EXPLICIT-0.45` only.

None may be pooled with Epoch 004, used to repair Epoch 004 outcomes, or retrovalidated by a future Epoch 004 result.

## Interpretation ceiling

If eventually authorized and executed, Epoch 004 would be a Solo/developer empirical test. A result could support or fail to support the preregistered canonical DGAF-vs-null FFCR hypothesis under the frozen PDMAL apparatus. It would not by itself establish independent validation, High-Assurance acceptance, production readiness, Confidential Space qualification, or external certification.

## Current boundary

`CANONICAL_TREATMENT_REACHABILITY = VERIFIED_NONEMPIRICALLY`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`EPOCH_004_PREREGISTRATION = PROPOSED_NOT_YET_MERGED`

`EPOCH_004_RUNNER = NOT_YET_IMPLEMENTED_OR_AUTHORIZED`

`EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`HIGH_ASSURANCE = UNCHANGED / NOT_AUTHORIZED / N=0`
