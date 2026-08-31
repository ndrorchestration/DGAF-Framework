# N=1 Operational Characterization Gate — 2026-08-30

**Status:** EXECUTION GATE DEFINED / AUTHORIZATION STILL EXTERNAL

## Candidate identity
- Apparatus / candidate source SHA: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Candidate designation/control record: `docs/experiment/NEW_CANDIDATE_MANIFEST.md` (current post-#170 control surface)
- Current documentation lineage: `main` — resolve directly
- Prior candidate: `05fa286…` — superseded post-#151 candidate
- Prior P2/P6a evidence boundary: `303f4424…` — historical scope only
- Candidate deployment: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` (READY / production)
- Candidate deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Purpose

This gate separates bounded operational characterization from the later full scientific pilot. N=1 does not establish DGAF efficacy.

## Required observation

Execute one bounded PDMAL synchronization run using the exact designated candidate apparatus and governing protocol. Preserve raw output and integrity metadata. Any failure, warning, omission, or anomaly remains observable.

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

- Fresh P2 runtime verification must be completed for the exact candidate SHA, deployment ID, and deployment URL.
- Fresh P6a CORS verification must be completed for the exact candidate SHA, deployment ID, deployment URL, and allowed origin.
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

N=1 remains 0 until one candidate-scoped observation exists with complete retained evidence under the authorized frozen apparatus. A pre-authorization or identity-mismatched execution does not advance empirical N.

**Current state:** Post-#170 restored apparatus identified; exact deployment identity and CORS origin are known; fresh candidate runtime verification, freeze, and authorization remain pending.
