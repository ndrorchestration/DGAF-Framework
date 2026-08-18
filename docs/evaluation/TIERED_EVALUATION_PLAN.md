# DGAF Tiered Evaluation Plan

**Status:** Active implementation plan

DGAF evaluation is divided into evidence tiers so that deterministic tests, synthetic simulations, integration behavior, empirical model evaluation, and comparative experiments cannot be conflated.

## Tier A — Deterministic unit validation

Purpose: verify local functions and pure transformations.

Examples:
- schema validation;
- evidence-tier ordering;
- deterministic hashing/replay;
- gate decision functions;
- topology invariants.

Permitted evidence: implementation/test correctness only.

## Tier B — Synthetic structural validation

Purpose: test system behavior under controlled synthetic fixtures.

Examples:
- generated malformed requests;
- controlled agent disagreement;
- synthetic graph failures;
- synthetic governance traces.

Permitted evidence: behavior under the specified synthetic conditions.

Prohibited interpretation: real-world or model-performance claims.

## Tier C — Integration validation

Purpose: verify assembled runtime paths.

Required path:

`request → schema → governance gates → decision → trace → evidence envelope → response`

Permitted evidence: integration correctness for the tested deployment/environment.

Prohibited interpretation: empirical effectiveness or generalization.

## Tier D — Empirical model evaluation

Purpose: measure real model/system behavior on frozen datasets or workloads.

Required metadata:
- model identifier/version;
- inference configuration;
- dataset/workload version;
- run identifier;
- seeds/randomness policy;
- environment;
- exact prompts/fixtures or reproducible generation procedure;
- observed failures and exclusions;
- artifact hashes;
- uncertainty and analysis method.

Permitted evidence: bounded empirical statements about the tested conditions.

## Tier E — Comparative validation

Purpose: test whether DGAF provides incremental benefit relative to predeclared baselines.

Required systems:
- NULL;
- SIMPLE_AGENT;
- STATIC_RULES;
- DGAF;
- DGAF_PDMAL.

Primary endpoints and comparison rules must be frozen before confirmatory execution.

## Promotion rules

- A lower tier cannot satisfy a higher-tier claim.
- Schema validation cannot establish operational effectiveness.
- Integration success cannot establish empirical improvement.
- Empirical results from one workload cannot automatically establish general superiority.
- Historical results remain historical unless the same claim is reverified.
- Any post-hoc metric or analysis is exploratory unless explicitly documented as a preregistered amendment.

## Current state

Tier A: **in progress**  
Tier B: **substantial coverage exists**  
Tier C: **partially implemented; runtime trace remains incomplete**  
Tier D: **not yet established for DGAF effectiveness claims**  
Tier E: **design defined; execution pending**
