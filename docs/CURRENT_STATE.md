---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_mainline_control_plane_head: 028771c3a40bce5e78984c13e91ef102066de6fa
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

The current mainline control-plane head is `028771c3a40bce5e78984c13e91ef102066de6fa`, the merge commit for PR #223. PR #223 corrected the TLA+ Tools v1.8.0 checksum metadata to the current official release-asset digest `16b8cd970e07147ff91f126baecba7edd98202e5ab33220a42f8f4358ee94b2b`; its authoritative Governance CI passed before merge. That change is CI supply-chain remediation only.

The verified executable runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, with Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to that exact Git SHA. The current mainline control-plane head must not be conflated with that separately scoped runtime identity.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Mainline control-plane head | CURRENT | `028771c3…` |
| Verified executable runtime candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Candidate deployment | VERIFIED READY | `dpl_8Msuf…` bound to `7c1cc4…` |
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
- **PR #219 — OPEN / REBASED / CURRENT-MAIN VALIDATION:** completion-controller evidence is bound to the exact triggering `workflow_run.id` and artifact rather than selecting the latest matching run. Current head `43d53f79067bd0ef6c8a0d3a344f13edcff62b7c`.
- **PR #220 — OPEN / REBASED / CURRENT-MAIN VALIDATION:** every blinded condition must contain the identical canonical 5-topology × 9-failure pilot matrix. Current head `a82a56030be6a6bd3125014d1155a972fc207643`.
- **PR #221 — OPEN / REBASED / CURRENT-MAIN VALIDATION:** dry-run dependency installation uses hash enforcement, persisted Git credentials are disabled, and an exact-candidate structural evidence registry is emitted. Current head `512340b57905fb01ff320d8c1f14724de897051a`.
- **PR #222 — OPEN / REBASED / CURRENT-MAIN VALIDATION:** scheduled live regression uses the established Vercel automation bypass path and fails closed when the credential is absent. Current head `10209402423c8c7c4b75717e88c1f6a8fcae8e32`.
- **PR #217 — MERGED:** pre-freeze runner least-privilege and reproducibility hardening.
- **PR #216 — CLOSED / SUPERSEDED.** Its still-valid evidence-registry intent was reworked into #221 without carrying forward stale checksum history.

The four open remediation PRs are separate control-plane changes. They do not create empirical observations, establish efficacy, authorize a pilot, or create a freeze.

## Documentation / provenance hygiene

Current mainline identity, verified runtime identity, candidate branches, deployments, workflow runs, and evidence artifacts are deliberately represented as separate provenance objects. A current documentation commit is not itself an experimental candidate, and historical evidence does not transfer across SHAs merely because the implementation intent is similar.

The TLA+ release pin is currently `v1.8.0` with official digest `16b8cd970e07147ff91f126baecba7edd98202e5ab33220a42f8f4358ee94b2b`. The successful Governance CI run that validated the remediation is evidence for the corrected CI supply chain; it is not efficacy evidence.

## Evidence boundary

Closed P2/P6a runtime evidence remains scoped to the verified executable runtime identity above. Documentation/control-plane changes do not reopen those predicates unless the runtime surface or their governing acceptance conditions materially change. No empirical efficacy conclusion follows from runtime or CI checks.

The PDMAL instrumentation workflow is isolated from documentation-only changes and retains deliberate `workflow_dispatch` as the route for intentional evidence execution. A successful structural or dry-run workflow validates workflow/control infrastructure; it does not advance empirical N.

## Closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
