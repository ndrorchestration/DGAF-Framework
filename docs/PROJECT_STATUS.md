# DGAF/PDMAL Project Status

**Status date:** 2026-09-05  
**Repository main at reconciliation:** `8ae37faee637d3992dfec2f635ea4d1d9252ef2d`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Designated executable runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Candidate deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Pilot status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Empirical N:** 0

## Executive state

DGAF is in pre-freeze closure. The runtime candidate and its deployment remain distinct from later documentation/control-plane commits. P1, P2, P3, P6, and P6a have candidate-scoped verification records. P4 and P5 have current-candidate engineering evidence but retain substantive open requirements. P7 final binding, P8, P9, freeze, and authorization remain open or absent.

None of these engineering states establishes empirical efficacy.

## Gate board

| Gate / control | Status | Evidence / limitation |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| P1 | CLOSED / VERIFIED | exact apparatus/candidate/tree and live deployment identity |
| P2 | CLOSED / VERIFIED | run `33730195621`; retrievable artifact `9883521704`; exact runtime predicates only |
| P3 | CLOSED / VERIFIED | run `33939955138`; artifact-contract evidence |
| P4 | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | synthetic blinding behavior only; real custody/access separation absent |
| P5 | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | final analysis implementation/configuration binding absent |
| P6 | CLOSED / VERIFIED | defined external archive/retrieval/SHA-256 equality contract |
| P6a | CLOSED / VERIFIED | run `33728695806`; retrievable artifact `9882965299`; exact CORS predicates only |
| P7 | ADOPTED / FINAL BINDING OPEN | final scientific identity chain incomplete |
| P8 | OPEN / FAIL-CLOSED | prerequisites and analysis lock incomplete |
| P9 | OPEN | independent final verification not executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## Current execution evidence

On 2026-09-05, both candidate-scoped runtime evidence records were successfully re-retrieved:

- P2 artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This supersedes the earlier retrieval-unconfirmed observation but is not a new runtime execution.

Current-candidate P3/P5 evidence is retained from run `33939955138`. Synthetic P4 evidence is retained from run `33939574283`. The P6 round-trip record covers the finalized P3/P5 and P4 artifact sets within its defined byte-equality scope.

## Current-main deployment state

The production-deployment workflow for `8ae37fa…` failed at Vercel's free-plan daily deployment quota. No deployment exists for that repository-main SHA, and its identity verification, health, and live regression were not executed. Do not transfer the `7c1cc4bb…` deployment result to `8ae37fa…`.

## Evidence boundary

Evidence remains exact-candidate, workflow, artifact, deployment, and predicate scoped. Documentation-only control-plane changes neither reopen valid exact-scope evidence nor inherit it automatically. Archive/retrieval digest equality does not establish immutable custody or independent human control.

## Required closure sequence

`P4 actual custody + final P5 binding → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
