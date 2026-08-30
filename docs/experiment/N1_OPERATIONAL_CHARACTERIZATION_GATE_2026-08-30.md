# N=1 Operational Characterization Gate — 2026-08-30

**Status:** EXECUTION GATE DEFINED / AUTHORIZATION STILL EXTERNAL

## Candidate identity
- Apparatus / candidate source SHA: `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
- Candidate designation/control commit: `02c146d1e0cdc423948ac0dfa11e98f812edfb44` (control record only)
- Current documentation lineage: `main` — resolve directly
- Prior candidate: `c6157158…` — superseded pre-remediation
- Prior P2/P6a evidence boundary: `303f4424…` — historical scope only
- Candidate deployment: exact post-#151 deployment identity must be verified before current-candidate runtime closure

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

## Authorization boundary

This document does not grant authorization. Explicit authorization must precede execution.

**Authorization:** NOT GRANTED BY THIS DOCUMENT
**Empirical N:** 0
**Freeze:** NOT CREATED

## Completion condition

N=1 remains 0 until one candidate-scoped observation exists with complete retained evidence under the authorized frozen apparatus. A pre-authorization or identity-mismatched execution does not advance empirical N.

**Current state:** Post-#151 candidate designated; runtime identity verification and N=1 execution remain pending.
