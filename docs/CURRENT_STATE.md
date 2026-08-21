---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: 526a106268cdd744e25a55de8c7384444f6ee72e
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to the exact SHA/run that produced it.

## Authoritative current state

| Gate | Status | Evidence / note |
|---|---|---|
| Current main | CURRENT | `526a106268cdd744e25a55de8c7384444f6ee72e` |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` retained unchanged as historical evidence |
| Corrected pilot apparatus | CANDIDATE | PR #77 lineage; stale relative to current main and must be refreshed before freeze evaluation |
| New freeze | NOT CREATED | No current freeze commit exists for the corrected apparatus |
| Protocol | PRE-FREEZE / BLOCKED | Primary contrast, analysis lock, retention, candidate verification, and freeze remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | Acceptance/characterization observations are non-empirical; pilot N remains 0 |

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

PR #77 currently points to `4983f44a1867d8ab2f18295a1ce23877ff8ea928`. Current main has advanced beyond the PR base and candidate, so the PR must be refreshed/rebased and re-verified before its code can be treated as the current candidate apparatus.

## Required next evidence events

- refresh PR #77 against current main;
- execute fresh candidate CI, including execution-contract, security, schema, and contract-mode checks;
- verify canonical artifact serialization and runtime validation;
- establish durable retention and direct retrieval/hash evidence;
- reconcile topology fingerprints and environment identity on the exact candidate;
- adjudicate the primary contrast and lock analysis;
- derive P1–P8 from candidate-scoped evidence;
- execute P9 independent verification;
- create and verify a new freeze;
- obtain separate pilot authorization.

**No empirical pilot execution is authorized. Empirical N remains 0.**
