---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: 23ab411d6113b3281f011f6891fb9335c7b6972e
---

# PDMAL Current Control State

This is the current pre-authorization gate record. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact tested SHA.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Current main | CURRENT | `23ab411d6113b3281f011f6891fb9335c7b6972e` |
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Corrected runner | CANDIDATE | PR #77 lineage; candidate must be refreshed against current `main` |
| Environment lock | VERIFY | Target Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1 |
| Executor contract | PARTIAL | Test #5 reconciled; fresh CI still required |
| Artifact contract | PARTIAL | Pilot schema exists; runtime validation wiring added on PR #77 branch; fresh candidate verification required |
| Topology provenance | VERIFY | Current-source fingerprints require repository manifest restoration and candidate-scoped verification |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368`; historical operational evidence only |
| Blinding custody | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935`; production key custody still requires operational evidence |
| Security controls | VERIFY | Pre-authorization workflow exists on PR #77; CI execution required |
| Durable retention | OPEN | Implementation/archive destination not yet established on current mainline |
| Primary contrast | OPEN / MUST CLOSE | Explicit methodological adjudication required |
| Analysis implementation | OPEN | Exact implementation/configuration SHA required before unblinding |
| New freeze | NOT CREATED | No corrected apparatus freeze exists |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Canonical predicate taxonomy

P1 Candidate integrity; P2 Execution contract; P3 Artifact contract; P4 Security/blinding integrity; P5 Provenance/reproducibility; P6 Durable evidence custody; P7 Scientific target specification; P8 Analysis lock; P9 Independent verification.

Experimental-design integrity is covered by P5 + P7 and is not a tenth predicate. Authorization is a separate governance transition after freeze verification.

## Historical freeze boundary

`3510b86889cd341f7a7cf9ab684fd37b2fafd758` is historical evidence only. It must not be described as the current freeze of the corrected runner. If candidate verification requires apparatus changes, a new freeze must be created after repair and re-verification.

## Required next evidence events

1. Refresh PR #77 against current `main`.
2. Run fresh candidate CI including the reconciled execution contract, security controls, schema tests, and contract mode.
3. Verify the canonical artifact serializer/validator path on the refreshed candidate.
4. Establish durable evidence custody and direct retrieval/hash verification.
5. Restore/reconcile topology fingerprint provenance on the current candidate.
6. Adjudicate the primary contrast and lock the analysis implementation/configuration.
7. Evaluate P1–P8 from candidate-scoped evidence.
8. Execute P9 independent verification.
9. Create a new freeze and verify that new freeze.
10. Obtain explicit pilot authorization.

**No empirical execution is authorized by this record. N = 0.**
