# N=1 Operational Characterization Gate — 2026-08-30

**Status:** EXECUTION GATE DEFINED / CURRENT APPARATUS PROVISIONAL / CANDIDATE NOT YET EXECUTION-VALID

## Candidate identity

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Corrected apparatus tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- Provenance correction: PR #174 / merge `2a54a67d…`
- Current documentation lineage: `main` — resolve directly
- Pre-correction apparatus source: `d56b5b3c…` — invalidated for candidate use
- Prior candidate: `05fa286…` — superseded historical candidate
- Prior P2/P6a evidence boundary: `303f4424…` — historical scope only
- Current deployment: **NOT YET ESTABLISHED for `2a54a67d…`**
- Pre-correction deployment: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — historical/non-closing
- Configured allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Current candidate hold

`2a54a67d…` is the corrected apparatus source and the basis for the new candidate cycle, but it is **not yet an execution-valid candidate** because an exact source-matched current deployment and fresh candidate-scoped P1–P9 evidence do not yet exist.

No N=1 observation may be run for closure purposes until the candidate identity, deployment, P2/P6a, P3–P8 evidence, independent P9 verification, freeze, and authorization predicates are satisfied.

## Purpose

This gate separates bounded operational characterization from the later full scientific pilot. N=1 does not establish DGAF efficacy.

## Required observation

Execute one bounded PDMAL synchronization run using the exact designated **corrected and frozen** candidate apparatus and governing protocol. Preserve raw output and integrity metadata. Any failure, warning, omission, or anomaly remains observable.

## Acceptance predicates

1. Exact candidate identity is recorded.
2. Execution uses the designated candidate without source modification.
3. The defined procedure completes or terminates under defined failure semantics.
4. Required artifact fields are emitted according to the bound schema.
5. Artifact integrity/hash is recorded.
6. Runtime/environment identity is recorded to the extent available.
7. Deviations are preserved, not silently repaired.
8. The result is classified using the canonical epistemic vocabulary.
9. No efficacy conclusion is derived from N=1.

## Candidate-chain prerequisites

- PR #174 provenance correction is merged and verified.
- Corrected apparatus source `2a54a67d…` is the sole current apparatus basis.
- A new exact production deployment must be built from `2a54a67d…` and source-matched.
- Fresh P2 runtime verification must pass for that exact candidate/deployment.
- Fresh P6a CORS verification must pass for that exact candidate/deployment/origin.
- P3–P8 current-candidate evidence must be retained and provenance-linked.
- P9 must independently verify the current evidence chain.
- A new immutable freeze must be created and independently verified.
- Explicit pilot authorization must be recorded separately.

## Authorization boundary

This document does not grant authorization. Explicit authorization must precede execution.

**Authorization:** NOT GRANTED BY THIS DOCUMENT
**Empirical N:** 0
**Freeze:** NOT CREATED

## Completion condition

N=1 remains 0 until one candidate-scoped observation exists with complete retained evidence under the authorized frozen apparatus. A pre-authorization, pre-correction, or identity-mismatched execution does not advance empirical N.

**Current state:** Corrected apparatus `2a54a67d…` is provisionally established; current deployment, candidate-scoped runtime verification, freeze, and authorization remain pending.
