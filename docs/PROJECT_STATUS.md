# DGAF/PDMAL Project Status

**Status date:** 2026-09-03  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Corrected apparatus provenance anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Current mainline candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Current exact deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in post-P6a-remediation, pre-freeze closure. The current mainline candidate is `7c1cc4...`, and the exact production deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is READY with the same Git SHA.

P2 and P6a runtime verification are now both closed for this exact candidate/deployment/environment binding. Historical runtime results for superseded candidates remain provenance only and are not transferable.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical apparatus anchor | HISTORICAL / CANONICAL ANCHOR | `2a54a67d…` |
| Current repository main | CURRENT | `7c1cc4…` |
| Current candidate | PRE-FREEZE / NOT FROZEN | `7c1cc4…` |
| Current production deployment | READY / EXACT SHA | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` |
| P2 | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704`; exact candidate/deployment bound |
| P6a | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299`; exact candidate/deployment bound |
| P3 | VERIFIED AT ENGINEERING/WORKFLOW SCOPE | Current exact-candidate operational closure remains required where specified |
| P4 | OPEN | Current-cycle operational blinding/custody evidence required |
| P5 | OPEN | Final exact-candidate reproducibility closure required |
| P6 | OPEN / FAIL-CLOSED | Durable external archive/retrieval/hash proof required |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact final candidate/protocol/analysis binding required |
| P8 | OPEN / FAIL-CLOSED | Prerequisites and exact final binding required |
| P9 | OPEN | Current-candidate independent verification required |
| Freeze | NOT ESTABLISHED | No immutable frozen identity is authoritative |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | ZERO | No authorized pilot execution |

## Current P2 evidence

Run `33730195621` verified candidate `7c1cc4...` against deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` using base URL `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app`. The five required runtime cases all passed their defined predicates, including expected fail-closed behavior for the valid request without live audit state. Artifact `9883521704` has digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

## Current P6a evidence

Run `33728695806` verified candidate `7c1cc4...` against deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` using base URL `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app` and canonical allowed origin `https://dynamicgovernanceagenticformation.vercel.app`. The allowed/disallowed POST and preflight predicates all passed. Artifact `9882965299` has digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

## Evaluator integrity finding

Completion Controller run `33729094860` succeeded but evaluated `CANDIDATE_SHA=25b6379...`, the head of documentation PR #210, while the controller itself ran from `main` at `7c1cc4...`. This follows the workflow's `workflow_run.head_sha` binding. The evaluator correctly returned `OPEN_GAPS`, so no unsafe promotion occurred; however, the result is not current-main evidence. The event-to-candidate binding requires explicit review before controller results are treated as current-main closure evidence.

## Documentation hygiene finding

PR #210's Claim Hygiene Audit run `33729056884` failed on the enumerated phrase `- is empirically superior;` inside `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`. This is a checker false positive caused by the historical-priority document header not being recognized as historical context. PR #211 adds a narrow context rule and regression coverage; it remains separate from experimental candidate authorization.

## Evidence boundary

Evidence does not transfer across candidate SHA, deployment identity, triggering workflow identity, or materially different control state. Successful CI, deterministic dry runs, deployment readiness, runtime verification, documentation updates, or controller success do not constitute experimental efficacy evidence or pilot authorization.

## Required closure sequence

1. Current-cycle operational P4/P5/P6 evidence and durable custody.
2. Exact final P7 candidate/protocol/analysis binding.
3. P8 prerequisite satisfaction and analysis lock.
4. Current-candidate independent P9.
5. New immutable freeze and independent verification.
6. Explicit pilot authorization.
7. Only then execute the authorized blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
