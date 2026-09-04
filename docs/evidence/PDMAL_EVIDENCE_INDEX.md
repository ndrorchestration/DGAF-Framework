---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
main_tip_at_last_reconciliation: 363d203c839746e89a7a6d3f6ba608730d42deea
applies_to_control_plane_head: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
verified_runtime_candidate: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run/artifact/deployment that produced it. Candidate
  verification does not inherit historical verification automatically. A
  repository record of prior verification is distinct from successful current
  retrieval of the underlying Actions evidence. No freeze or authorization is implied.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Consolidated control-state lineage | CURRENT | `89be386b…` | Current documentation/control-state anchor |
| Main tip at last reconciliation | LINEAGE ANCHOR | `363d203c…` | Mainline tip at the last recorded reconciliation; later documentation descendants remain lineage unless executable semantics change |
| Runtime candidate identity | CANDIDATE LINEAGE PRESENT | `7c1cc4bb…` | Candidate identity referenced by prior runtime verification records |
| Deployment identity | HISTORICAL REFERENCE | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Deployment identity previously bound to candidate; not freshly re-verified in this pass |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | Seven-gate restoration/provenance lineage |
| Superseded runtime candidate | HISTORICAL / NON-TRANSFERABLE | `48c12c66…` | Prior candidate cycle |
| Prior completion candidate | HISTORICAL / NON-TRANSFERABLE | `a43219b4…` | Prior completion/P3–P6/P9 evidence remains scoped only to that SHA |
| P2 runtime record | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | Run `33730195621`; artifact `9883521704` | Repository records prior five-case exact-candidate runtime verification; current Actions retrieval did not re-establish the artifact |
| P6a CORS record | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | Run `33728695806`; artifact `9882965299` | Repository records prior four-case exact-candidate CORS verification; current Actions retrieval did not re-establish the artifact |
| P3 artifact contract | OPEN | Current execution candidate | Current-cycle artifact-contract closure required |
| P4 blinding/security | OPEN | Current execution candidate | Operational blinding/custody closure required |
| P5 provenance/reproducibility | OPEN | Current execution candidate | Current toolchain/topology/RNG closure required |
| P6 durable evidence custody | OPEN / FAIL-CLOSED | Current execution candidate | Durable archive plus independent retrieval/hash proof required |
| P7 scientific target | ADOPTED / BINDING OPEN | Current execution candidate | Exact scientific/protocol/apparatus binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Current execution candidate | Final prerequisites and analysis lock remain required |
| P9 independent verification | OPEN | Current execution candidate | Fresh independent verification required |
| Empirical execution | NOT EXECUTED | N=0 | No authorized pilot execution |
| Freeze | NOT ESTABLISHED | — | No immutable frozen identity is authoritative |
| Authorization | NOT GRANTED | — | Separate governance transition remains required |

## Runtime evidence retrievability note

The exact identifiers below remain preserved because they are part of the repository's historical control-plane lineage:

- P2: run `33730195621`, artifact `9883521704`, recorded digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a: run `33728695806`, artifact `9882965299`, recorded digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

In the current verification attempt, the Actions lookup path did not return those runs/artifacts. Consequently, these are retained as historical records, not fresh live verification. Their absence does not by itself prove deletion, invalidity, or tampering; it establishes only that the present verification path could not independently re-retrieve them.

A future current-candidate closure may use them only with an explicit immutable retained copy and independent provenance, or after successful retrieval through a trustworthy verification path.

## Matrix-control disposition

PRs #220, #230, and #231 were closed without merge after review established that their additional matrix-equality assertion was implied by the existing canonical-coordinate membership, exact per-condition cardinality, and duplicate-cell rejection constraints. No active matrix-hardening blocker remains.

## P3–P6 current-cycle boundary

The successful pre-freeze validation demonstrates the harness contract, dependency lock, fail-closed pilot behavior, artifact integrity contract, and pre-freeze manifest generation. It is control-plane/engineering evidence, not empirical efficacy evidence.

Current P3/P4/P5/P6 closure requires fresh candidate-bound evidence. Historical workflow-level/synthetic evidence does not transfer automatically.

## P9 boundary

Historical P9 evidence for `a43219b4…` remains non-transferable. A fresh P9 must inspect the final current evidence chain before freeze.

## Evidence inheritance rule

Historical evidence does not transfer across candidate SHA, deployment identity, workflow identity, or materially different control state. Documentation changes do not create efficacy evidence, authorize a pilot, or advance empirical N.

## Current closure sequence

`P1/P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**