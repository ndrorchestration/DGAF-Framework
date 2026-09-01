---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-01
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
runtime_candidate_tree: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` is the distinct production/runtime candidate. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. Git history establishes the corrected apparatus source as the candidate's lineage basis; these identities are not interchangeable.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Identity roles

- `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` — corrected seven-gate apparatus provenance anchor.
- `92ff830b1c67413df745e37087e6447c9c251b9a` — current production/runtime candidate and deployment-workflow repair commit.
- `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` — exact tree of the current runtime candidate.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment identity recorded by both P2 and P6a runtime evidence.
- Pre-correction candidates/deployments remain historical/non-closing and must not be reused as current dispatch inputs.
- Documentation commits advance `main` documentation lineage but do not silently redefine apparatus identity.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for latest source and control documents. |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…`; seven-gate restoration plus complete provenance binding. |
| Runtime candidate identity | CURRENT / NOT FROZEN | `92ff830b…`; exact tree `73cf3ad…`. |
| Candidate lineage | ESTABLISHED | `2a54a67d…` is the ancestor/lineage basis of `92ff830b…`. |
| Deployment identity | CAPTURED IN P2/P6A EVIDENCE | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P2 runtime verification | VERIFIED | Run `33509348174`; artifact `9800942933`; five required cases passed. |
| P6a CORS verification | VERIFIED | Run `33509416955`; artifact `9800972819`; four required checks passed. |
| P3 | IMPLEMENTATION PRESENT / OPEN | Current-candidate evidence remains required. |
| P4 | OPEN | Current-cycle blinding/custody evidence required. |
| P5 | OPEN | Current-cycle environment/topology/RNG reproducibility evidence required. |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required. |
| P7 | ADOPTED / FINAL BINDING OPEN | Bind exact apparatus/candidate/deployment/protocol/analysis/freeze identity. |
| P8 | OPEN / FAIL-CLOSED | TGL/P-35 current-candidate verification required. |
| P9 | NOT EXECUTED | Independent verification remains outstanding. |
| Freeze | NOT ESTABLISHED | No frozen identity is authoritative. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## Current runtime evidence

P2 and P6a both recorded the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

P2's valid-missing-audit case remained correctly fail-closed (`BLOCKED`, HTTP 503). P6a's allowed-origin preflight returned 204 and disallowed-origin preflight returned 403; the POST checks matched their expected results. These are runtime predicate results, not efficacy evidence.

## Historical runtime inputs

Historical candidates, deployment IDs, URLs, and runs remain scoped to their original evidence and are non-closing unless explicitly rebound through a new governance/evidence record. In particular, the pre-correction `d56b5b3c…` / `dpl_76UU8mCm…` boundary remains retired.

## Documentation and provenance control rule

This document distinguishes **main tip, apparatus source, runtime candidate, candidate tree, and deployment identity**. Executable apparatus state changes reset the candidate cycle. Documentation-only commits do not create a candidate. Evidence does not transfer across identities merely because the branch, repository, URL, or documentation lineage is shared.

Older audit records that state inline artifact validation is missing are **historical/stale claims**, not current implementation defects. The current implementation performs inline artifact validation. Historical records remain preserved as historical snapshots; current-state documents state the present implementation and separately track remaining candidate-scoped evidence gaps.

## Assurance boundary

CI success, deterministic tests, deployment readiness, runtime PASS, historical artifacts, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Any unresolved blinding, null-integrity, artifact-custody, reproducibility, analysis, P7 binding, P8, or independent-verification predicate remains FAIL-CLOSED.

## Required closure sequence

`P2/P6a VERIFIED → P3/P4/P5/P6 current-cycle evidence → P7 final candidate binding → P8 TGL/P-35 verification → independent P9 → new immutable freeze → explicit authorization → blinded pilot`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
