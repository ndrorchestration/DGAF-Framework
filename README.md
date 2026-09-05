# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.** Engineering verification is not empirical efficacy evidence. Historical evidence remains scoped to the exact candidate, workflow, deployment, artifact, and predicates that produced it.

## Current identity boundary — 2026-09-05

This documentation hygiene reconciliation uses immutable source boundary `a3bafa6fca8599df479a685828f5fdddb6bae589` (PR #286 merge) rather than calling any embedded SHA “current main.” The documentation branch that updates this file is necessarily a later control-plane descendant and does not replace the designated runtime candidate.

| Identity | Role | Status |
|---|---|---|
| `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Corrected apparatus provenance anchor | Historical canonical anchor |
| `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | Immutable P-35 validation boundary | Historical validated boundary |
| `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Designated executable runtime candidate | PRE-FREEZE / not frozen |
| `586c00d6dedb589e52108279f9759be3c4f927e1` | Runtime candidate tree | Exact candidate tree |
| `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Vercel production deployment for `7c1cc4bb…` | READY / exact Git source verified at its scoped evidence boundary |
| `a3bafa6fca8599df479a685828f5fdddb6bae589` | Documentation-hygiene reconciliation source boundary | Control-plane lineage; not the scientific candidate |

Later documentation, evaluator, or control-plane descendants do not automatically replace the designated runtime candidate or inherit its runtime evidence.

## Candidate-scoped runtime evidence

P2 and P6a are **CLOSED / VERIFIED** only for candidate `7c1cc4bb…`, tree `586c00d6…`, deployment `dpl_8Msuf…`, and the exact predicates executed on 2026-09-03.

### P2 — CLOSED / VERIFIED

- run: `33730195621`
- artifact: `9883521704`
- digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`
- scope: five authenticated POST cases against `/api/orchestrate`
- 2026-09-05 retrieval: run and unexpired candidate-bound artifact successfully resolved

### P6a — CLOSED / VERIFIED

- run: `33728695806`
- artifact: `9882965299`
- digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`
- scope: four authenticated CORS POST/preflight cases
- 2026-09-05 retrieval: run and unexpired candidate-bound artifact successfully resolved

Fresh retrieval is not a new runtime execution and does not establish later-main equivalence, general application health, or efficacy.

## Gate state

| Gate / boundary | Current state |
|---|---|
| P-35 implementation | VALIDATED at immutable boundary `643dc77a…` |
| P1 candidate integrity | CLOSED / VERIFIED |
| P2 runtime contract | CLOSED / VERIFIED at exact runtime scope |
| P3 artifact contract | CLOSED / VERIFIED — run `33939955138` |
| P4 security/blinding | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED; no H/I/T custody mode instantiated or verified |
| P5 provenance/reproducibility | CLOSED / VERIFIED within its bounded provenance/reproducibility contract |
| P6 evidence custody | CLOSED / VERIFIED within the defined archive/retrieval/hash contract |
| P6a CORS | CLOSED / VERIFIED at exact runtime scope |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN |
| P8 analysis lock / freeze readiness | OPEN / FAIL-CLOSED |
| P9 independent verification | NOT EXECUTED / OPEN |
| Freeze | NOT ESTABLISHED |
| Pilot authorization | NOT GRANTED |
| Empirical N | 0 |

P5 closure is provenance/reproducibility evidence, not model or scientific efficacy evidence.

### P4 custody interpretation

PR #286 generalized P4 from a mandatory second-human model to **effective control separation**. Three custody modes are admissible in principle:

- `H` — genuinely distinct human custody;
- `I` — institutional/third-party custody outside the analyst’s unilateral control;
- `T` — independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No mode has been instantiated. Issue #285 is completed as the governance-architecture correction; Issue #255 is superseded historical context. Issue #287 is the active design/threat-model lane for a possible zero-human Mode T lifecycle. GitHub Actions + timelock/drand is **not** yet accepted as sufficient P4 custody merely because the design issue exists.

## Evaluation integrity

Issue #32 Task 4 (`audit_hallucination_rate`) was hardened by PR #269, merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`. The evaluator now fails closed unless provenance-controlled ground truth and independently generated corresponding outputs are supplied, and it performs deterministic six-field comparison rather than synthesizing a benchmark-derived score.

That change verifies evaluator mechanics only. No Task-4 model-performance result currently exists; the required fixture/output corpus remains outstanding.

## Engineering quality and merge enforcement

Issue #270 is **CLOSED / COMPLETED**. PR #276 restored a clean current-lineage flake8/Black/isort/mypy baseline and converted those quality checks to fail-closed workflow gates; the Python matrix and deterministic negative controls subsequently passed at the recorded exact boundaries.

A separate repository-administration gap remains: Issue #277 tracks branch-protection/ruleset enforcement. The Python quality workflow is fail-closed when it runs, but the available configuration readback did not establish that its matrix is required before every merge. That distinction must not be collapsed into either “quality is still advisory” or “branch protection is complete.”

## Evidence rules

Evidence does not transfer across candidate SHA, deployment identity, workflow identity, artifact identity, or materially different control state without an explicit provenance relationship. A documentation commit does not create a new experimental candidate. Deployment readiness does not establish runtime behavior. CI and synthetic dry runs are engineering controls, not empirical efficacy evidence.

Historical documents may contain statements that were “current” at their own closure boundary. Those statements remain historical unless explicitly promoted by a later current-state record.

## Current closure sequence

`verified real P4-A custody mode → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

No documentation or CI action in this sequence grants experimental authorization or advances empirical N.
