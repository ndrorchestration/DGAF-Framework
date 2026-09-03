---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_mainline_control_plane_head: 7bbfd8ec5991ce399b8ee58cdeca742040ad272c
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

The current mainline control-plane head is `7bbfd8ec5991ce399b8ee58cdeca742040ad272c`, the merge commit for PR #217. The verified executable runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, with Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to that exact Git SHA.

The `7bbfd8e…` change is control-plane hardening and does not by itself replace the separately scoped verified runtime candidate. PRs #219, #220, and #221 are open control-plane remediation lanes and are not experimental authorization.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Mainline control-plane head | CURRENT | `7bbfd8e…` |
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

## Control-plane hardening state

- PR #217 is merged into current `main`; it hardens pre-freeze runner least privilege and reproducibility.
- PR #219 remains open and hardens completion-controller evidence binding to the exact triggering workflow run rather than selecting the latest matching run.
- PR #220 remains open and requires every blinded condition to contain the identical canonical topology × failure-count matrix.
- PR #221 remains open and adds hash-enforced dry-run dependency installation plus exact-candidate structural evidence-registry emission.
- PR #216 is closed/superseded; its still-valid evidence-registry intent was reworked onto current mainline in #221 without carrying forward stale dependency/checksum history.

These changes are control-plane safeguards. They do not create empirical observations, establish efficacy, authorize a pilot, or create a freeze.

## Evidence boundary

Closed P2/P6a runtime evidence remains scoped to the verified executable runtime identity above. Documentation/control-plane changes do not reopen those predicates unless the runtime surface or their governing acceptance conditions materially change. No empirical efficacy conclusion follows from these runtime checks.

The PDMAL instrumentation workflow is intended to remain isolated from documentation-only changes and retains deliberate `workflow_dispatch` as the route for intentional evidence execution. A successful PR dry run validates workflow/control infrastructure; it does not advance empirical N.

## Closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
