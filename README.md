# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** The repository is currently **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0**. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current execution boundary — 2026-09-03

The current mainline candidate is the exact commit below. Earlier candidate/deployment pairs remain historical and must not be transferred.

| Identity | Role | Status |
|---|---|---|
| `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Corrected apparatus provenance anchor | Historical canonical anchor |
| `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | Immutable P-35 validation boundary | Historical validated boundary |
| `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Current mainline candidate after P6a CORS remediation | PRE-FREEZE / not frozen |
| `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Vercel deployment for `7c1cc4...` | READY / exact Git SHA |
| `48c12c6660df7decb61f9aac4d8560526a8754eb` | Superseded executable candidate | Historical / non-transferable |
| `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` | Superseded deployment | Historical / non-transferable |

The current mainline commit adds the canonical production origin to the middleware CORS allowlist. The exact deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is the deployment used by the current P6a verification.

## P2 / P6a runtime boundary

P2 and P6a are now verified against the same exact current candidate/deployment binding. Historical P2/P6a results for superseded candidates remain provenance only.

### P2 — CLOSED / VERIFIED

- candidate SHA: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- deployment ID: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- base URL: `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app`
- run: `33730195621`
- artifact: `9883521704`
- artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`
- required suite: five authenticated POST cases against `/api/orchestrate`; all five passed their defined predicates, including expected fail-closed behavior when live audit state was absent

### P6a — CLOSED / VERIFIED

- candidate SHA: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- deployment ID: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- base URL: `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app`
- allowed origin: `https://dynamicgovernanceagenticformation.vercel.app`
- run: `33728695806`
- artifact: `9882965299`
- artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`
- required suite: four authenticated CORS POST/preflight checks; all four passed their expected predicates

## Gate state

| Gate / boundary | Current state |
|---|---|
| P-35 implementation | VALIDATED at immutable boundary `643dc77a…` |
| Current mainline candidate | `7c1cc4…` / PRE-FREEZE |
| Exact candidate deployment | READY / exact Git SHA verified |
| P2 | CLOSED / VERIFIED — run `33730195621` |
| P6a | CLOSED / VERIFIED — run `33728695806` |
| P3 | VERIFIED at applicable engineering/workflow scope; current exact-candidate operational closure remains required where specified |
| P4 | OPEN — operational blinding/custody closure required |
| P5 | OPEN — final exact-candidate reproducibility closure required |
| P6 | OPEN / FAIL-CLOSED — durable archive/retrieval/hash proof required |
| P7 | ADOPTED / FINAL BINDING OPEN |
| P8 | OPEN / FAIL-CLOSED |
| P9 | OPEN — current-candidate independent verification required |
| Freeze | NOT ESTABLISHED |
| Authorization | NOT GRANTED |
| Empirical N | 0 |

## Evaluator integrity finding

The completion controller is a `workflow_run` evaluator and deliberately treats candidate SHA as data. On 2026-09-03, run `33729094860` executed from `main` but received `CANDIDATE_SHA=25b6379...`, the head of documentation PR #210, because the workflow uses `${{ github.event.workflow_run.head_sha }}`. Its result was correctly `OPEN_GAPS`, but that result is evidence about the triggering workflow's candidate, not automatically about current `main`.

This control-plane binding behavior requires explicit review before a completion-controller result is used as current-main closure evidence. It does not authorize freeze, pilot execution, unblinding, or empirical collection.

## Evidence rules

Evidence does not transfer across candidate SHA, deployment identity, triggering workflow identity, or materially different control state. A documentation commit does not create a new experimental candidate. A deployment-health result does not constitute runtime verification. CI success and deterministic dry runs are engineering controls, not empirical efficacy evidence.

## Current closure sequence

`operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

No step in this documentation lane grants experimental authorization or advances empirical N.
