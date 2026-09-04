---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_mainline_control_plane_head: fc8976e5c5a1077a37ea6e7abd9cca92e436c05f
candidate identity: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
deployment identity: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
verified_runtime_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The current mainline control-plane head is `fc8976e5c5a1077a37ea6e7abd9cca92e436c05f`, a documentation reconciliation commit following the control-plane merges. The earlier `028771c3…` merge of PR #223 remains the substantive TLA+ supply-chain remediation point; the later `fc8976e…` commit only reconciles current documentation state. The TLA+ v1.8.0 digest is `16b8cd970e07147ff91f126baecba7edd98202e5ab33220a42f8f4358ee94b2b`.

The verified executable runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, with Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to that exact Git SHA. The current mainline control-plane head must not be conflated with that separately scoped runtime identity.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Mainline control-plane head | CURRENT | `fc8976e…` |
| Verified executable runtime candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Candidate deployment | VERIFIED READY | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to `7c1cc4…` |
| P2 | CLOSED / VERIFIED | run `33730195621`, artifact `9883521704` |
| P6a | CLOSED / VERIFIED | run `33728695806`, artifact `9882965299` |
| P3 | OPEN / CURRENT EVIDENCE REQUIRED | artifact-contract closure |
| P4 | OPEN | operational blinding/custody |
| P5 | OPEN | reproducibility/provenance closure |
| P6 | OPEN / FAIL-CLOSED | durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | exact final candidate/protocol/analysis binding |
| P8 | OPEN / FAIL-CLOSED | analysis lock and prerequisites |
| P9 | OPEN | independent verification |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized pilot execution |

## Current P2 / P6a evidence

P2 run `33730195621` verified the exact candidate/deployment pair with all five required runtime predicates passing; artifact `9883521704` has digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

P6a run `33728695806` verified the same exact candidate/deployment binding using the canonical production origin; all four POST/preflight predicates passed. Artifact `9882965299` has digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

## Control-plane remediation state

- **PR #223 — MERGED:** TLA+ v1.8.0 digest corrected to the exact official release-asset digest. Authoritative Governance CI passed; no experimental authorization or execution was introduced.
- **PR #219 — MERGED:** completion-controller evidence is bound to the exact triggering `workflow_run.id` and artifact rather than selecting the latest matching run. Squash merge `ce1820f5b39c36c6e3012ae5a559015761db32b7`.
- **PR #221 — MERGED:** dry-run dependency installation uses hash enforcement, persisted Git credentials are disabled, and an exact-candidate structural evidence registry is emitted. Squash merge `8c4f1fa960119c4f7757376bc778a1516485c0af`.
- **PR #222 — MERGED:** scheduled live regression uses the established Vercel automation bypass path and fails closed when the credential is absent. Squash merge `01b37b1fe6fc63e28faf6c1bab1e5c9d68a43327`.
- **PR #220 — CLOSED / SUPERSEDED:** the proposed canonical-matrix assertion was not merged because the stated failure mode is already implied by existing constraints: canonical 45-cell membership, exactly 45 records per condition, and duplicate-cell rejection together force each condition to contain the complete canonical matrix.
- **PR #230 — CLOSED / SUPERSEDED:** current-mainline attempt of the same redundant matrix control.
- **PR #231 — CLOSED / NOT MERGED:** reproduced the proposal on current mainline, then closed after invariant analysis showed the added assertion and adversarial mutation were redundant with the existing validator contract.
- **PR #217 — MERGED:** pre-freeze runner least-privilege and reproducibility hardening.
- **PR #216 — CLOSED / SUPERSEDED.** Its still-valid evidence-registry intent was reworked into #221 without carrying forward stale checksum history.

The #220/#230/#231 sequence is retained as control-history and an explicit invariant analysis, not as an active experimental blocker.

## Documentation / provenance hygiene

Current mainline identity, verified runtime identity, candidate branches, deployments, workflow runs, and evidence artifacts are deliberately represented as separate provenance objects. A current documentation commit is not itself an experimental candidate, and historical evidence does not transfer across SHAs merely because the implementation intent is similar.

The TLA+ release pin is currently `v1.8.0` with official digest `16b8cd970e07147ff91f126baecba7edd98202e5ab33220a42f8f4358ee94b2b`. Successful Governance CI validation is evidence for the corrected CI supply chain; it is not efficacy evidence.

The pilot-artifact validator already constrains topology and failure-count coordinates to the canonical 45-cell universe, requires exactly 45 records per blinded condition, and rejects duplicate `(condition, topology, failure_count)` cells. Under those constraints, a condition containing 45 valid unique canonical cells is necessarily the complete canonical matrix; a separate matrix-equality assertion would be redundant.

## Evidence boundary

Closed P2/P6a runtime evidence remains scoped to the verified executable runtime identity above. Documentation/control-plane changes do not reopen those predicates unless the runtime surface or their governing acceptance conditions materially change. No empirical efficacy conclusion follows from runtime or CI checks.

The PDMAL instrumentation workflow is isolated from documentation-only changes and retains deliberate `workflow_dispatch` as the route for intentional evidence execution. A successful structural or dry-run workflow validates workflow/control infrastructure; it does not advance empirical N.

## Closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
