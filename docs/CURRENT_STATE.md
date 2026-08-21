---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document intentionally does not hard-code a mutable `main` SHA.

## Authoritative current state

| Gate | Status | Evidence / note |
|---|---|---|
| Current main | CURRENT | Resolve from GitHub `main` at verification time |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` retained unchanged as historical evidence |
| Corrected pilot apparatus | CANDIDATE | Apparatus and governance controls exist on mainline; exact-candidate verification remains required |
| New freeze | NOT CREATED | No corrected-apparatus freeze commit exists |
| Protocol | PRE-FREEZE / BLOCKED | Candidate execution evidence, durable retention, primary contrast, analysis lock, P9, and freeze remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Canonical predicates

P1 Candidate integrity — PARTIAL
P2 Execution contract — PARTIAL
P3 Artifact contract — PARTIAL
P4 Security / blinding integrity — PARTIAL
P5 Provenance / reproducibility — PARTIAL
P6 Durable evidence custody — OPEN
P7 Scientific target specification — PARTIAL / primary contrast OPEN
P8 Analysis lock — OPEN
P9 Independent verification — NOT EXECUTED

Experimental-design integrity is covered by P5 + P7 and is not a separate tenth predicate. Authorization is a separate governance transition.

## Historical boundary

`3510b86889cd341f7a7cf9ab684fd37b2fafd758` is the historical implementation freeze. It must not be described as the current freeze of the corrected pilot apparatus.

Historical P2/P6a evidence is likewise scoped to its exact tested source/deployment/run. In particular, P6a `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` / `e1f077f...` remains historical and does not certify current mainline behavior.

## Documentation vocabulary boundary

`FLAG-02` is a historical identifier associated with the former 340% coordination-gain claim. The current canonical evaluation-mode terminology is **qualitative**. Historical records may retain FLAG-02 when needed to preserve provenance, but living documents must not use it as a current label.

The former 340% coordination-gain result is not a current verified result. Any current recurrence must be qualified according to the propagation/provenance controls.

## Required next evidence events

- execute the full repository audit against an immutable candidate and retain the coverage manifest;
- run fresh candidate unit/contract/determinism/invariant tests;
- verify canonical artifact serialization and runtime validation;
- execute current-candidate P2 and P6a runtime checks;
- complete synthetic operational blinding verification;
- establish durable retention and direct retrieval/hash evidence;
- reconcile topology fingerprints and environment identity on the exact candidate;
- adjudicate the primary contrast and lock the analysis;
- derive P1–P8 from candidate-scoped evidence;
- execute P9 independent verification;
- create and verify a new freeze;
- obtain separate pilot authorization.

**No empirical pilot execution is authorized. Empirical N remains 0.**
