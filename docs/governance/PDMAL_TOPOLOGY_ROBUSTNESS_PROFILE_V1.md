# PDMAL Topology Robustness Profile v1

**Status:** NONEMPIRICAL CANDIDATE PROFILE  
**Controller:** Issue #398  
**Scientific N increment:** 0  
**Empirical authorization:** FALSE

## Purpose

Track A isolates numeric topology and failure-recovery mechanics from semantic DGAF governance.

The profile uses the existing deterministic PDMAL graph construction, failure selection and reference neighbor-mean update mechanics, but exposes a new neutral public algorithm identity:

`REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`

The historical internal `null` condition name is an implementation-reuse detail only. It is not emitted as a treatment axis and does not become the scientific label of this profile.

## Structural probe

The PR-only probe uses two diagnostic-only seeds:

- `20261201`
- `20261202`

Across:

- five topologies;
- nine failure counts;
- 90 total structural cells.

For each cell, the retained artifact contains only:

- seed;
- topology;
- failure count;
- topology fingerprint;
- selected failure nodes;
- initial-state hash;
- hashes of one deterministic reference update under pre-failure, failure-active and recovered neighbor states.

It does not retain numerical consensus outcomes.

## Explicitly forbidden artifact content

The structural artifact must not contain:

- FFCR;
- `final_std`;
- `consensus_success`;
- treatment effects;
- confidence intervals;
- p-values;
- governance traces;
- any condition axis;
- any DGAF treatment label.

## Gate disposition

Semantic governance gates are not represented as default PASS values.

- P-31: out of scope.
- P-33: separate B3 monitor-fidelity track.
- DemiJoule: out of scope.
- P-27/P-28: out of scope.
- P-29: out of scope.
- P-32: out of scope.
- P-30: future external profile qualification only.

## Claim ceiling

This profile can establish only that the Track A workload identity, topology/failure matrix and reference numeric update path are structurally coherent and reproducible.

It cannot establish topology superiority, failure robustness, DGAF efficacy, High-Assurance acceptance or production readiness.

## Next gate

After exact-head validation and merge:

1. source-bound P-30/11Q qualification of this profile;
2. separate non-empirical matrix adjudication;
3. only then consider a fresh preregistered empirical Track A proposal.

`TRACK_A_EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`
