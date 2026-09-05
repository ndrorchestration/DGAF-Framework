---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
main_at_last_reconciliation: 8ae37faee637d3992dfec2f635ea4d1d9252ef2d
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded. Evidence is scoped to the exact identities and predicates that produced it. A successful CI, deployment, synthetic, or custody check is not empirical efficacy evidence.

## Identity boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`.
- Candidate identity — designated runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.
- Runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`.
- Deployment identity — candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.
- Repository main at reconciliation: `8ae37faee637d3992dfec2f635ea4d1d9252ef2d`.

Later documentation/control-plane descendants do not automatically replace the designated runtime candidate or inherit its runtime evidence.

## Current gate board

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| P1 candidate integrity | CLOSED / VERIFIED | apparatus, candidate/tree, and live deployment identity |
| P2 runtime | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` five-case runtime predicates |
| P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; candidate-bound structural/matrix/integrity evidence |
| P4 security/blinding | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | synthetic behavior passes; actual human/key custody and access separation unestablished |
| P5 provenance/reproducibility | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | deterministic/environment evidence present; final analysis implementation/configuration binding open |
| P6 evidence custody | CLOSED / VERIFIED | defined archive → retrieval → SHA-256 equality contract |
| P6a CORS | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` four-case CORS predicates |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | final exact candidate/protocol/analysis/freeze binding required |
| P8 analysis lock | OPEN / FAIL-CLOSED | prerequisites and final analysis binding incomplete |
| P9 independent verification | OPEN | final bound-chain verification not executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate human governance decision |
| Empirical N | 0 | no authorized pilot execution |

## Runtime evidence retrieval

On 2026-09-05, the P2 and P6a GitHub Actions records were freshly resolved:

- P2 run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

Both artifacts were unexpired and candidate-bound. This supersedes the earlier retrieval-unconfirmed observation; it does not constitute a new execution or extend closure beyond the exact runtime predicates.

## Current-main operational limitation

The Vercel deployment workflow for `8ae37fa…` failed because the free-plan daily deployment limit was exceeded. No deployment was created for that SHA. Exact deployment identity, provenance upload, health, and live regression were therefore not executed for repository main. The separately verified `7c1cc4bb…` deployment remains candidate-scoped evidence only.

The post-fix Completion Controller has not yet been exercised by a new producer → controller cycle. Its post-fix operational status remains NOT EXECUTED / UNKNOWN.

## Remaining substantive closure work

`P4 actual custody + final P5 binding → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`

Issue #232 is the active completion-control record. Instrument conflicts in #226 remain separately fail-closed where applicable.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
