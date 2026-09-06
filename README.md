# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.** Engineering verification is not empirical efficacy evidence. Historical evidence remains scoped to the exact candidate, workflow, deployment, artifact, and predicates that produced it.
>
> **Candidate-authority update — 2026-09-06:** PR #308 introduced protocol v0.7.6 / artifact schema 1.1 at `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`. Later engineering lineage, including the Mode-T stack integrated by PR #326, does not become the scientific candidate merely by being newer or more complete. The prior `7c1cc4bb…` runtime candidate retains valid exact-scope historical evidence; PR #328 made that historical-candidate boundary explicit in the Pre-Freeze workflow. **Final v0.7.6 candidate: NOT DESIGNATED**; Issue #309 governs final-candidate designation and identity-dependent evidence classification/regeneration. The consolidated control-state anchor `89be386b…` remains a control/provenance anchor, not a final-candidate designation.

## Current identity boundary — 2026-09-06

`972edd41f16c69c6912af08c7d6c3aa627fdd8a9` is the **v0.7.6 protocol/schema apparatus-introduction boundary**, not the current repository head and not a final scientific candidate. The engineering lineage has advanced beyond that boundary, including PR #326's integration of the validated Mode-T mechanism stack and later governance/documentation corrections. Newer `main`, PR heads, deployments, evaluators, or documentation descendants do not become the final candidate or inherit historical runtime evidence by recency.

| Identity | Role | Status |
|---|---|---|
| `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Corrected apparatus provenance anchor | Historical canonical anchor |
| `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | Immutable P-35 validation boundary | Historical validated boundary |
| `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | Consolidated control-state anchor | Canonical control/provenance anchor; not a candidate designation |
| `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Historical exact-scope runtime-evidence candidate | Verified for recorded scope; not eligible as final v0.7.6 freeze/N=1 candidate |
| `586c00d6dedb589e52108279f9759be3c4f927e1` | Historical runtime candidate tree | Exact candidate tree for `7c1cc4bb…` evidence |
| `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Vercel production deployment for `7c1cc4bb…` | READY / exact Git source verified at its scoped evidence boundary |
| `972edd41f16c69c6912af08c7d6c3aa627fdd8a9` | v0.7.6 protocol/schema apparatus-introduction boundary | PR #308 merge; historical lineage boundary; not a final-candidate designation |
| `d03f7b4e1c7d58ef73ad163b5da6e4236c0b0146` | Mode-T engineering-lineage integration boundary | PR #326 merge; bounded engineering integration only; not P4 acceptance or candidate designation |
| Issue #309 | Final-candidate reconstruction authority | Final v0.7.6 candidate NOT DESIGNATED |

## Candidate-scoped runtime evidence

P2 and P6a are **CLOSED / VERIFIED** only for historical candidate `7c1cc4bb…`, tree `586c00d6…`, deployment `dpl_8Msuf…`, and the exact predicates executed on 2026-09-03. Those results remain valid provenance but do not automatically close the same predicates for a future v0.7.6 final candidate.

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

Fresh retrieval is not a new runtime execution and does not establish later-main equivalence, general application health, efficacy, or final-candidate closure.

## Gate state

| Gate / boundary | Current state |
|---|---|
| P-35 implementation | VALIDATED at immutable boundary `643dc77a…` |
| Historical P1 candidate integrity | CLOSED / VERIFIED at `7c1cc4bb…` scope; final-candidate transfer/reverification pending #309 |
| Historical P2 runtime contract | CLOSED / VERIFIED at exact `7c1cc4bb…` runtime scope; final-candidate transfer/reverification pending #309 |
| Historical P3 artifact contract | CLOSED / VERIFIED — run `33939955138`; final-candidate transfer/reverification pending #309 |
| P4 security/blinding | OPEN / FAIL-CLOSED; Mode-T engineering mechanisms are integrated, but no real admissible H/I/T custody mode has been independently accepted and executed for the final run |
| Historical P5 provenance/reproducibility | CLOSED / VERIFIED within its bounded pre-v0.7.6 contract; final-candidate transfer/reverification pending #309 |
| Historical P6 evidence custody | CLOSED / VERIFIED within the defined archive/retrieval/hash contract; final-candidate rebind decision pending #309 |
| Historical P6a CORS | CLOSED / VERIFIED at exact `7c1cc4bb…` runtime scope; final-candidate transfer/reverification pending #309 |
| Final v0.7.6 candidate | NOT DESIGNATED — Issue #309 |
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

PR #326 integrated the validated Mode-T engineering stack assembled through #311, #313, #314, #321, #323, and #324. That stack establishes bounded mechanism-level engineering evidence for authenticated attestation verification, lifecycle ordering, key-generation/retention contracts, Sigstore verification, and explicit TrustedRoot digest binding. It does **not** establish real P4 custody or independently accepted production admission.

P4 therefore remains **OPEN / FAIL-CLOSED**. Required external/independent evidence includes #316 independently retained production R/A/C admission-policy evidence, #320 independent OIDC security review, final signer authority, an independently approved/frozen production TrustedRoot/TUF policy, real durable retention/retrieval, and real Confidential Space admission with independently reverified PRE/POST evidence. If those requirements cannot be satisfied for Mode T, an admissible H/I route must be selected rather than treating engineering mechanics as custody acceptance.

## Evaluation integrity

Issue #32 Task 4 (`audit_hallucination_rate`) was hardened by PR #269, merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`. The evaluator now fails closed unless provenance-controlled ground truth and independently generated corresponding outputs are supplied, and it performs deterministic six-field comparison rather than synthesizing a benchmark-derived score.

That change verifies evaluator mechanics only. No Task-4 model-performance result currently exists; the required fixture/output corpus remains outstanding.

## Engineering quality and merge enforcement

Issue #270 is **CLOSED / COMPLETED**. PR #276 restored a clean current-lineage flake8/Black/isort/mypy baseline and converted those quality checks to fail-closed workflow gates; the Python matrix and deterministic negative controls subsequently passed at the recorded exact boundaries.

A separate repository-administration gap remains: Issue #277 tracks branch-protection/ruleset enforcement. The quality and governance workflows are fail-closed when they run, but full repository-level enforcement of the intended merge-critical check set is **NOT ESTABLISHED**. The last readable protected-branch snapshot reported only `PPTL CI` as a required status context; a fresh readable `Main` ruleset (`16909314`) contains only deletion and non-fast-forward rules with no bypass actors, while the direct branch-protection administration endpoint is currently inaccessible to this integration (`403 Resource not accessible by integration`). Green exact-head workflows therefore remain verification evidence, not proof that every intended check is repository-required.

## Evidence rules

Evidence does not transfer across candidate SHA, deployment identity, workflow identity, artifact identity, protocol/schema identity, or materially different control state without an explicit provenance relationship. A documentation commit or newer source SHA does not create a new experimental candidate. Deployment readiness does not establish runtime behavior. CI and synthetic dry runs are engineering controls, not empirical efficacy evidence.

Historical documents may contain statements that were “current” at their own closure boundary. Those statements remain historical unless explicitly promoted by a later current-state record.

## Current closure sequence

`complete candidate-relevant P4 apparatus/external-acceptance work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent P2/P3/P5/P6/P6a evidence → verified real P4 custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

No documentation or CI action in this sequence grants experimental authorization or advances empirical N.
