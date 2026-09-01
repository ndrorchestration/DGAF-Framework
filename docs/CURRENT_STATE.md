---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-01
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
runtime_candidate_tree: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
latest_completion_candidate_sha: 562753b3053b3566b0fcad1b0b1df151d7de119a
latest_completion_candidate_branch: completion/2026-09-01-exact-candidate
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` is the current production/runtime candidate recorded by the current mainline state. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`.
>
> **Latest completion candidate:** `562753b3053b3566b0fcad1b0b1df151d7de119a` is the exact candidate checked by P9 run `33567199896` on branch `completion/2026-09-01-exact-candidate`. It is a controlled completion candidate and must not be silently substituted for the current mainline runtime candidate.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Identity roles

- `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` — corrected seven-gate apparatus provenance anchor.
- `92ff830b1c67413df745e37087e6447c9c251b9a` — current production/runtime candidate on the mainline control-state record; exact tree `73cf3ad…`.
- `562753b3053b3566b0fcad1b0b1df151d7de119a` — latest completion candidate used for scoped P9 independent verification; branch `completion/2026-09-01-exact-candidate`.
- `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` — exact tree of the current mainline runtime candidate.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment identity recorded by both P2 and P6a runtime evidence for `92ff830b…`.
- Pre-correction candidates/deployments remain historical/non-closing and must not be reused as current dispatch inputs.
- Documentation commits advance `main` documentation lineage but do not silently redefine apparatus or completion-candidate identity.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for latest source and control documents. |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…`; seven-gate restoration plus complete provenance binding. |
| Runtime candidate identity | CURRENT / NOT FROZEN | `92ff830b…`; exact tree `73cf3ad…`. |
| Latest completion candidate | CONTROLLED / NOT FROZEN | `562753b…`; P9 scoped-verification target on completion branch. |
| Candidate lineage | ESTABLISHED | `2a54a67d…` is the recorded lineage basis of the current runtime candidate. |
| Deployment identity | CAPTURED IN P2/P6A EVIDENCE | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P2 runtime verification | VERIFIED | Run `33509348174`; artifact `9800942933`; five required cases passed for the current runtime candidate/deployment. |
| P6a CORS verification | VERIFIED | Run `33509416955`; artifact `9800972819`; four required checks passed for the current runtime candidate/deployment. |
| P3 | IMPLEMENTATION PRESENT / OPEN | Current completion-candidate evidence remains required. |
| P4 | OPEN | Current-cycle blinding/custody evidence required. |
| P5 | OPEN | Current-cycle environment/topology/RNG reproducibility evidence required. |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required. |
| P7 | ADOPTED / FINAL BINDING OPEN | Bind exact apparatus/candidate/deployment/protocol/analysis/freeze identity for the intended pilot cycle. |
| P8 | OPEN / FAIL-CLOSED | TGL/P-35 current-candidate verification required. |
| P9 | SCOPED PASS / BROADER CLOSURE OPEN | Run `33567199896` independently verified exact candidate identity, alternate canonicalization/hash path, and authority-identity regression for candidate `562753b…`; broader P9 closure remains conditional on the full evidence-chain requirements. |
| Freeze | NOT ESTABLISHED | No frozen identity is currently authoritative for pilot execution. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## Latest P9 scoped evidence

Run `33567199896` completed successfully on 2026-09-01 for candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`.

Verified in that run:

- `git rev-parse HEAD` matched `GITHUB_SHA` for the exact candidate checkout;
- a separate `jq -S -c` + `sha256sum` path reproduced the deterministic-case digest;
- `tests/test_agent_authority_matrix.py` returned `4 passed` against the exact candidate;
- P9 evidence JSON and SHA-256 sidecar were uploaded with `if-no-files-found: error`.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.

P9 artifact: `9823570326`, digest `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This is **scoped independent verification evidence**, not a declaration that all P9 prerequisites are closed. It does not establish durable external archive, candidate-scoped P2/P6a for `562753b…`, experimental authorization, empirical execution, or efficacy.

## Current runtime evidence

P2 and P6a both recorded the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

P2's valid-missing-audit case remained correctly fail-closed (`BLOCKED`, HTTP 503). P6a's allowed-origin preflight returned 204 and disallowed-origin preflight returned 403; the POST checks matched their expected results. These are runtime predicate results, not efficacy evidence.

## Historical runtime inputs

Historical candidates, deployment IDs, URLs, and runs remain scoped to their original evidence and are non-closing unless explicitly rebound through a new governance/evidence record. In particular, the pre-correction `d56b5b3c…` / `dpl_76UU8mCm…` boundary remains retired.

## Documentation and provenance control rule

This document distinguishes **main tip, apparatus source, runtime candidate, completion candidate, candidate tree, and deployment identity**. Executable apparatus state changes reset the candidate cycle. Documentation-only commits do not create a candidate. Evidence does not transfer across identities merely because the branch, repository, URL, or documentation lineage is shared.

Older audit records that state inline artifact validation is missing are **historical/stale claims**, not current implementation defects. Historical records remain preserved as historical snapshots; current-state documents state the present implementation and separately track remaining candidate-scoped evidence gaps.

## Historical-priority boundary

The historical review has been reconciled separately in `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

Current position: DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, organizational authority, veto/escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining hypothesis is a potentially distinctive **cross-domain integration** coupling formation-state governance to candidate-bound experimental verification and authorization. This is not an absolute novelty claim.

## Assurance boundary

CI success, deterministic tests, deployment readiness, runtime PASS, historical artifacts, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Any unresolved blinding, null-integrity, artifact-custody, reproducibility, analysis, P7 binding, P8, broader P9, freeze, or authorization predicate remains FAIL-CLOSED.

## Required closure sequence

`Current candidate selection → current-cycle P3/P4/P5/P6 evidence → P7 final binding → P8 verification → scoped P9 checks + broader P9 evidence-chain closure → new immutable freeze → explicit authorization → blinded pilot`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
