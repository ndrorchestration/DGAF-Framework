# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** The repository is currently **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0**. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current execution boundary — 2026-09-03

The repository contains two distinct identities that must not be conflated:

| Identity | Role | Status |
|---|---|---|
| `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Corrected apparatus provenance anchor | Canonical |
| `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | Immutable P-35 validation boundary | Validated |
| `48c12c6660df7decb61f9aac4d8560526a8754eb` | Independently verified executable candidate | PRE-FREEZE / deployment-bound |
| `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` | Vercel deployment for `48c12c...` | READY / verified Git SHA |
| `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389` | Later PR #200 control-plane/documentation head | Not independently deployment-bound |

The verified Vercel deployment reports Git SHA `48c12c...` and branch `candidate/p35-validated-control-state-2026-09-02`. The later `fc45d95e...` commit contains documentation/control-plane changes but does not establish a new deployment-bound candidate. Its dispatch handoff preserves the `48c12c...` execution candidate.

## P2 / P6a runtime boundary

The exact deployment identity is established, but P2 and P6a are **not closed**. Fresh workflow execution must bind the workflow inputs to the same candidate/deployment pair and preserve the resulting provenance artifacts.

### P2

- candidate SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- deployment ID: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- base URL: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- required suite: five authenticated POST cases against `/api/orchestrate`

### P6a

- candidate SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- deployment ID: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- base URL: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- allowed origin: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- required suite: four authenticated CORS POST/preflight checks

The workflows require `VERCEL_AUTOMATION_BYPASS_SECRET`; the secret value is never recorded in repository documentation.

## Gate state

| Gate / boundary | Current state |
|---|---|
| P-35 implementation | VALIDATED at immutable boundary `643dc77a…` |
| Current executable candidate | `48c12c…` / PRE-FREEZE |
| Exact candidate deployment | READY / Git SHA independently verified |
| P2 | OPEN — fresh candidate/deployment-bound workflow execution required |
| P6a | OPEN — fresh candidate/deployment-bound workflow execution required |
| P3 | VERIFIED at applicable engineering scope; operational closure remains required where specified |
| P4 | OPEN — operational blinding/custody closure required |
| P5 | OPEN — full reproducibility closure required |
| P6 | OPEN / FAIL-CLOSED — durable archive/retention closure required |
| P7 | Technically specified; exact final binding remains open |
| P8 | OPEN / FAIL-CLOSED |
| P9 | Historical/scoped evidence retained; fresh final closure remains required |
| Freeze | NOT ESTABLISHED |
| Authorization | NOT GRANTED |
| Empirical N | 0 |

## Evidence rules

Evidence does not transfer across candidate SHA, deployment identity, triggering workflow identity, or materially different control state. A documentation commit does not create a new experimental candidate. A deployment-health result does not constitute runtime verification. CI success and deterministic dry runs are engineering controls, not empirical efficacy evidence.

## Current closure sequence

`P2 + P6a exact runtime → operational P4/P5/P6 → exact P7 binding → P8 → final independent P9 → immutable freeze → explicit authorization → blinded pilot`

No step in this documentation lane grants experimental authorization or advances empirical N.
