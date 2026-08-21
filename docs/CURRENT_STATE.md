---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to the exact SHA/run that produced it. This document describes the moving pre-freeze state and therefore does not hard-code a mutable `main` SHA.

## Authoritative current state

| Gate | Status | Evidence / note |
|---|---|---|
| Current main | CURRENT | Resolve from GitHub `main` at verification time |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` retained unchanged as historical evidence |
| Corrected pilot apparatus | CANDIDATE | Candidate now exists on mainline after engineering hardening; fresh candidate verification required |
| New freeze | NOT CREATED | No corrected-apparatus freeze commit exists |
| Protocol | PRE-FREEZE / BLOCKED | Primary contrast, analysis lock, retention, candidate verification, and freeze remain open |
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

## Candidate boundary

PR #77 remains an historical engineering vehicle and requires refresh/reconciliation against the corrected mainline. The current mainline contains the corrected SHA-binding, artifact-validation, execution-contract, and security-workflow changes, but those changes are not yet freeze-verified.

## Required next evidence events

- run fresh candidate CI and candidate-scoped smoke/contract checks;
- verify canonical artifact serialization and runtime validation;
- establish durable retention and direct retrieval/hash evidence;
- reconcile topology fingerprints and environment identity on the exact candidate;
- adjudicate the primary contrast and lock the analysis;
- derive P1–P8 from candidate-scoped evidence;
- execute P9 independent verification;
- create and verify a new freeze;
- obtain separate pilot authorization.

**No empirical pilot execution is authorized. Empirical N remains 0.**
