---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization gate record. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact tested SHA. This document describes the moving pre-freeze state and therefore does not pin a mutable main SHA.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Corrected runner | CANDIDATE | Exact-SHA gating and pilot artifact validation are now present on mainline; fresh candidate verification required |
| Environment lock | VERIFY | Target Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1 |
| Executor contract | PARTIAL | Stale test reconciled; fresh CI required |
| Artifact contract | PARTIAL | Pilot schema and inline validator/sidecar checks present; fresh candidate verification required |
| Topology provenance | VERIFY | Current-source fingerprint manifest restored; final candidate re-computation required |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Historical Run #14; non-empirical |
| Blinding custody | CLOSED FOR SYNTHETIC VERIFICATION | Historical synthetic custody evidence; production key custody still requires operational evidence |
| Security controls | VERIFY | Pre-authorization workflow/tests present; fresh CI required |
| Durable retention | OPEN | Archive destination and direct retrieval/hash proof not established |
| Primary contrast | OPEN / MUST CLOSE | Explicit methodological adjudication required |
| Analysis implementation | OPEN | Exact implementation/configuration SHA required before unblinding |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Canonical predicate taxonomy

P1 Candidate integrity; P2 Execution contract; P3 Artifact contract; P4 Security/blinding integrity; P5 Provenance/reproducibility; P6 Durable evidence custody; P7 Scientific target specification; P8 Analysis lock; P9 Independent verification.

Experimental-design integrity is covered by P5 + P7 and is not a tenth predicate. Authorization is a separate governance transition after freeze verification.

## Historical freeze boundary

`3510b86889cd341f7a7cf9ab684fd37b2fafd758` is historical evidence only. It must not be described as the current freeze of the corrected runner. If verification identifies a defect requiring an apparatus change, a new freeze must be established after repair and re-verification.

## Required next evidence events

1. Run fresh candidate CI and smoke/contract checks.
2. Verify canonical artifact serialization and runtime validation.
3. Establish durable evidence custody and direct retrieval/hash evidence.
4. Reconcile topology fingerprints and environment identity on the exact candidate.
5. Adjudicate the primary contrast and lock the analysis.
6. Derive P1–P8 from candidate-scoped evidence.
7. Execute P9 independent verification.
8. Create and verify a new freeze.
9. Obtain separate pilot authorization.

**No empirical execution is authorized by this record. N = 0.**
