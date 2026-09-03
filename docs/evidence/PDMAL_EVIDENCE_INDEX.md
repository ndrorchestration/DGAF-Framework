---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_control_plane_head: 637023b28492783f50d77550d4ed8e0867cbcc3d
verified_runtime_candidate: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run/artifact/deployment that produced it. Candidate
  verification does not inherit historical verification automatically. No
  freeze or authorization is implied.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current control-plane lineage | CURRENT | `637023b2…` | Mainline documentation/control-plane head |
| Verified executable runtime candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4bb…` | Runtime candidate for closed P2/P6a evidence |
| Verified exact deployment | VERIFIED | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | READY deployment bound to `7c1cc4bb…` |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | Seven-gate restoration/provenance lineage |
| Superseded runtime candidate | HISTORICAL / NON-TRANSFERABLE | `48c12c66…` | Prior candidate cycle |
| Prior completion candidate | HISTORICAL / NON-TRANSFERABLE | `a43219b4…` | Prior completion/P3–P6/P9 evidence remains scoped only to that SHA |
| P2 runtime | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704` | Five-case exact-candidate authenticated runtime evidence |
| P6a CORS runtime | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299` | Four-case exact-candidate authenticated CORS evidence |
| P3 artifact contract | OPEN | Current execution candidate | Current-cycle artifact-contract closure required |
| P4 blinding/security | OPEN | Current execution candidate | Operational blinding/custody closure required |
| P5 provenance/reproducibility | OPEN | Current execution candidate | Current toolchain/topology/RNG closure required |
| P6 durable evidence custody | OPEN / FAIL-CLOSED | Current execution candidate | Durable archive plus independent retrieval/hash proof required |
| P7 scientific target | ADOPTED / BINDING OPEN | Current execution candidate | Exact scientific/protocol/apparatus binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Current execution candidate | Final prerequisites and analysis lock remain required |
| P9 independent verification | OPEN | Current execution candidate | Fresh independent verification required after prerequisites |
| Empirical execution | NOT EXECUTED | N=0 | No authorized pilot execution |
| Freeze | NOT ESTABLISHED | — | No immutable frozen identity is authoritative |
| Authorization | NOT GRANTED | — | Separate governance transition remains required |

## Closed runtime predicates

P2 and P6a remain closed for the exact executable runtime identity `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. The later `637023…` change is control-plane/documentation reconciliation and does not reopen those predicates.

## P3–P6 current-cycle boundary

The successful pre-freeze validation on PR #214 demonstrates the harness contract, dependency lock, fail-closed pilot behavior, artifact integrity contract, and pre-freeze manifest generation. It is control-plane/engineering evidence for that PR candidate, not current empirical efficacy evidence.

The strongest historical completion run remains `33572123862` for `a43219b4…`. Its P4/P6 artifacts were workflow-level/synthetic and remain historical. Current P4/P6 closure therefore still requires operational blinding/custody and durable external round-trip evidence.

## P9 boundary

Run `33572123857` is historical scoped P9 evidence for `a43219b4…`. A fresh P9 must inspect the final current evidence chain before freeze.

## Evidence inheritance rule

Historical evidence does not transfer across candidate SHA, deployment identity, workflow identity, or materially different control state. Documentation changes do not create efficacy evidence, authorize a pilot, or advance empirical N.

## Current closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
