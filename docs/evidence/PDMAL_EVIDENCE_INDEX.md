---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
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
| Current documentation lineage | CURRENT | `main` | Active control/documentation lineage |
| Current mainline candidate | CURRENT / NOT FROZEN | `7c1cc4bb…` | Current exact candidate after P6a CORS remediation |
| Current exact deployment | VERIFIED | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | READY deployment with exact Git SHA binding |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | Seven-gate restoration/provenance lineage |
| Superseded runtime candidate | HISTORICAL / NON-TRANSFERABLE | `48c12c66…` | Prior candidate cycle |
| Prior completion candidate | HISTORICAL / NON-TRANSFERABLE | `a43219b4…` | Prior completion/P3–P6/P9 evidence remains scoped only to that SHA |
| P2 runtime | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704`; candidate `7c1cc4bb…`; deployment `dpl_8Ms…` | Five-case exact-candidate authenticated runtime evidence |
| P6a CORS runtime | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299`; candidate `7c1cc4bb…`; deployment `dpl_8Ms…` | Four-case exact-candidate authenticated CORS evidence |
| P3 artifact contract | OPEN | Current candidate | Fresh exact-current-candidate artifact evidence required |
| P4 blinding/security | OPEN | Current candidate | Operational blinding/custody closure remains required; prior synthetic evidence does not transfer |
| P5 provenance/reproducibility | OPEN | Current candidate | Current exact candidate, environment, topology and RNG evidence required |
| P6 durable evidence custody | OPEN / FAIL-CLOSED | Current candidate | Durable archive plus independent retrieval/hash proof required |
| P7 scientific target | ADOPTED / BINDING OPEN | Current candidate | Exact scientific/protocol/apparatus binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Current candidate | Final candidate/configuration prerequisites remain required |
| P9 independent verification | OPEN | Current candidate | Fresh independent verification required after current prerequisites are satisfied |
| Empirical execution | NOT EXECUTED | N=0 | No authorized pilot execution |
| Freeze | NOT ESTABLISHED | — | No immutable frozen identity is authoritative |
| Authorization | NOT GRANTED | — | Separate governance transition remains required |

## Current P2 evidence

Run `33730195621` completed successfully for exact candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.

Artifact ID: `9883521704`.  
Artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

The five runtime cases all passed their defined predicates, including expected fail-closed behavior when live audit state was unavailable. This is engineering/runtime evidence, not efficacy evidence.

## Current P6a evidence

Run `33728695806` completed successfully for exact candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.

Artifact ID: `9882965299`.  
Artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

Allowed-origin and disallowed-origin POST/preflight predicates all passed. This is engineering/runtime evidence, not efficacy evidence.

## P3–P6 current-candidate gap

The strongest existing P3/P4/P5/P6 workflow evidence is Run `33572123862`, candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`. It demonstrated structural tests, deterministic reproduction, RNG separation, masked CSV schema validation, checksum sidecar verification, artifact round-trip retrieval, and an evidence registry.

That run is **historical for the current candidate**. P4 and P6 were also explicitly workflow-level/synthetic rather than full operational closure. Therefore the current candidate still requires fresh P3–P6 evidence, with special attention to operational blinding/custody and durable external retention.

## P9 current-candidate requirement

The latest scoped P9 evidence is Run `33572123857` for candidate `a43219b4…`. It is historical/non-transferable to `7c1cc4…`. A fresh independent P9 must follow completion of the current candidate's affected prerequisites.

## Evidence inheritance rule

Historical evidence does not transfer across candidate SHA, deployment identity, workflow identity, or materially different control state. A documentation commit does not create an experimental candidate. A deployment-health result does not constitute runtime verification. CI success and deterministic dry runs are engineering controls, not experimental efficacy evidence.

## Current closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
