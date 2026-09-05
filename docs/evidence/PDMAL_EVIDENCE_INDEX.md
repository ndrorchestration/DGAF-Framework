---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
main_at_last_reconciliation: 8ae37faee637d3992dfec2f635ea4d1d9252ef2d
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
runtime_candidate: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
experimental_state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Evidence Index

This is a control-plane index, not empirical evidence, external certification, or a self-authorizing freeze record.

## Current inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | seven-gate restoration/provenance lineage |
| P-35 validation | VALIDATED | `643dc77a…` | immutable validation boundary |
| Consolidated control-state lineage | CURRENT | `89be386b…` | documentation/control-state anchor |
| Repository main at reconciliation | CONTROL-PLANE LINEAGE | `8ae37fa…` | not a replacement runtime candidate |
| Runtime candidate | DESIGNATED | `7c1cc4bb…`; tree `586c00d6…` | exact executable identity |
| Deployment identity | VERIFIED FOR P1 SCOPE | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Vercel reported READY production deployment sourced from `7c1cc4bb…` |
| P2 runtime | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704` | exact candidate/deployment five-case runtime predicates |
| P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; artifacts `9961526468`, `9961526662` | structural, identity, matrix, deterministic, and specified adversarial checks |
| P4 blinding/security | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | run `33939574283`; artifacts `9961339739`, `9961339938` | synthetic mock-key behavior only; actual custody separation absent |
| P5 provenance/reproducibility | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | run `33939955138` | final analysis implementation/configuration binding absent |
| P6 evidence custody | CLOSED / VERIFIED | Google Drive archive and recorded retrieval hashes | equality of compared ZIP bytes within defined round-trip contract |
| P6a CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299` | exact candidate/deployment four-case CORS predicates |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | designated candidate | exact final identity chain incomplete |
| P8 analysis lock | OPEN / FAIL-CLOSED | designated candidate | prerequisites and final analysis lock incomplete |
| P9 independent verification | OPEN | final bound chain | not executed |
| Freeze | NOT ESTABLISHED | — | no immutable pilot identity |
| Authorization | NOT GRANTED | — | separate governance transition |
| Empirical execution | NOT EXECUTED | N = 0 | no empirical observations |

## Fresh runtime-record retrieval

On 2026-09-05, the GitHub Actions API successfully resolved the P2 and P6a runs and unexpired candidate-bound artifacts:

- P2: run `33730195621`; artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a: run `33728695806`; artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This supersedes the 2026-09-04 retrieval-unconfirmed observation. It does not constitute a new runtime execution, extend the tested predicates, or establish current-main equivalence.

## Current-candidate engineering evidence

- P3 is closed at artifact-contract scope by run `33939955138`.
- P4 remains open because synthetic blinding evidence does not establish real human/key custody or access separation.
- P5 remains open because final analysis implementation/configuration binding is absent.
- P6 is closed within its defined external archive → retrieval → SHA-256 equality contract.

The P6 result establishes equality for the compared bytes at retrieval time. It does not establish immutable storage, independent human custody, authenticity against a compromised producer, or a complete tamper-proof chain.

## Current-main deployment limitation

The deployment workflow for repository main `8ae37fa…` failed because Vercel's daily deployment quota was exceeded. No deployment was created for that SHA, so deployment identity, health, and live regression are NOT EXECUTED for current repository main.

## Non-transfer rule

Evidence does not transfer across candidate SHA, deployment, workflow, artifact, protocol, or materially different control state without an explicit provenance relationship. Documentation changes do not create efficacy evidence, authorize a pilot, or advance empirical N.

## Remaining path

`P4 actual custody + final P5 binding → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
