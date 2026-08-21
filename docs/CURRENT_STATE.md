---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: 23ab411d6113b3281f011f6891fb9335c7b6972e
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to the exact SHA/run that produced it.

## Authoritative current state

| Gate | Status | Evidence / note |
|---|---|---|
| Current main | CURRENT | `23ab411d6113b3281f011f6891fb9335c7b6972e` (v1.8.0 pre-authorization hardening release) |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` retained unchanged as historical evidence |
| Corrected pilot apparatus | CANDIDATE | PR #77 lineage; candidate must be refreshed against current `main` before any freeze evaluation |
| New freeze | NOT CREATED | No current freeze commit exists for the corrected apparatus |
| Protocol | PRE-FREEZE / BLOCKED | Primary contrast, analysis lock, retention, candidate verification, and freeze remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | Acceptance/characterization observations are non-empirical; pilot N remains 0 |

## Canonical pre-freeze predicates

1. Candidate integrity — PARTIAL
2. Execution contract — PARTIAL
3. Artifact contract — PARTIAL
4. Security / blinding integrity — PARTIAL
5. Provenance / reproducibility — PARTIAL
6. Durable evidence custody — OPEN
7. Scientific target specification — PARTIAL / primary contrast OPEN
8. Analysis lock — OPEN
9. Independent verification — NOT YET EXECUTED

All nine are required to be supported by candidate-scoped evidence before a new freeze is eligible.

## Historical boundary

`3510b86889cd341f7a7cf9ab684fd37b2fafd758` is the historical implementation freeze. It must not be described as the current freeze of the corrected pilot apparatus. Any apparatus change that requires a new freeze must produce a new immutable freeze commit.

## Candidate branch boundary

PR #77 currently points to `4983f44a1867d8ab2f18295a1ce23877ff8ea928` and is open/draft. Current `main` has since advanced to `23ab411d6113b3281f011f6891fb9335c7b6972e`; therefore PR #77 must be refreshed/rebased and re-verified before its changes can be treated as the current candidate apparatus.

## Experimental design boundary

The pilot matrix remains 4 conditions × 5 topologies × 9 failure-count levels = 180 trials per seed, 50 planned seeds, 9,000 planned raw trial records. Experimental-design integrity is covered by the provenance/reproducibility and scientific-target predicates; it is not a separate tenth gate.

## Required next evidence events

- refresh the corrected candidate against current `main`;
- reconcile stale tests and workflow permissions;
- wire the canonical pilot artifact validator into the runtime write path;
- reconcile canonical serialization/hash computation;
- establish durable retention implementation and archive destination;
- adjudicate the primary contrast and complete the analysis lock;
- execute fresh CI and candidate-scoped operational checks;
- perform independent verification;
- only then create and verify a new freeze;
- obtain separate pilot authorization.

**No empirical pilot execution is authorized. Empirical N remains 0.**
