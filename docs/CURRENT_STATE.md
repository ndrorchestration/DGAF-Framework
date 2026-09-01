---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-01
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
runtime_candidate_tree: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
latest_completion_candidate_sha: a43219b4ed91fff8615f6c655ab3d17ca871fc29
latest_completion_candidate_branch: completion/2026-09-01-exact-candidate
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` is the current production/runtime candidate recorded by the current mainline state. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`.
>
> **Latest completion candidate:** `a43219b4ed91fff8615f6c655ab3d17ca871fc29` is the current exact candidate on branch `completion/2026-09-01-exact-candidate`. It has fresh successful PDMAL and scoped P9 verification runs. The superseded candidate `562753b3053b3566b0fcad1b0b1df151d7de119a` remains historical.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Identity roles

- `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` — corrected seven-gate apparatus provenance anchor.
- `92ff830b1c67413df745e37087e6447c9c251b9a` — current production/runtime candidate on the mainline control-state record; exact tree `73cf3ad…`.
- `a43219b4ed91fff8615f6c655ab3d17ca871fc29` — current controlled completion candidate; exact-candidate PDMAL/P9 verification target.
- `562753b3053b3566b0fcad1b0b1df151d7de119a` — superseded completion candidate with historical scoped P9 verification.
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
| Latest completion candidate | CONTROLLED / NOT FROZEN | `a43219b…`; exact-candidate verification target on completion branch. |
| Candidate lineage | ESTABLISHED | `2a54a67d…` is the recorded lineage basis of the current runtime candidate. |
| Deployment identity | CAPTURED IN P2/P6A EVIDENCE | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P2 runtime verification | VERIFIED — MAINLINE ONLY | Run `33509348174`; artifact `9800942933`; five required cases passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P6a CORS verification | VERIFIED — MAINLINE ONLY | Run `33509416955`; artifact `9800972819`; four required checks passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P3 | VERIFIED — COMPLETION CANDIDATE | Run `33572123862`; artifact `9825367738`; exact candidate `a43219b…`; 19-test suite and artifact contract checks passed. |
| P4 | WORKFLOW-LEVEL VERIFIED / OPERATIONAL CLOSURE OPEN | Run `33572123862`; blinding secret presence verified without disclosure and masked dry-run produced. Full operational custody/separation remains required. |
| P5 | VERIFIED — COMPLETION CANDIDATE | Run `33572123862`; exact artifact binding, RNG stream separation, deterministic digest, and environment fingerprint recorded. |
| P6 | WORKFLOW-LEVEL VERIFIED / DURABLE ARCHIVE OPEN | Run `33572123862`; artifact download plus inner checksum re-verification passed. Durable external archive closure remains required. |
| P7 | ADOPTED / FINAL BINDING OPEN | Bind exact apparatus/candidate/deployment/protocol/analysis/freeze identity for intended pilot cycle. |
| P8 | OPEN / FAIL-CLOSED | TGL/P-35 current-candidate analysis-lock verification required. |
| P9 | SCOPED PASS / BROADER CLOSURE OPEN | Run `33572123857` passed exact identity, independent `jq -S -c`/`sha256sum` check, and 4-test authority regression for `a43219b…`; broader P9 evidence-chain closure remains open. |
| Freeze | NOT ESTABLISHED | No frozen identity is currently authoritative for pilot execution. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## Current exact-candidate PDMAL evidence

Run `33572123862` completed successfully on 2026-09-01 for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The run verified exact checkout identity, presence of the withheld blinding secret, deterministic smoke reproduction, P5 RNG-stream separation, a `19 passed` structural/artifact suite, masked one-seed CSV generation, schema validation, CSV checksum integrity, artifact download round-trip, and inner-CSV checksum re-verification.

The run emitted an evidence registry marking P3/P4/P5/P6 `VERIFIED` for this exact candidate and a controller evaluation that kept P2/P7/P8/P9 blocking. P4 and P6 are explicitly workflow-level/synthetic custody evidence rather than full operational closure.

PDMAL artifact: `9825367738`.  
Artifact ZIP digest: `sha256:51b89e5321674ff19eecc53a4445237677025649fe36ed5ddc762835a24c2c6c`.  
Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.

## Current exact-candidate P9 evidence

Run `33572123857` completed successfully on 2026-09-01 for candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Verified:

- `git rev-parse HEAD` matched `GITHUB_SHA`;
- independent `jq -S -c` canonicalization plus `sha256sum` matched the deterministic-case digest;
- `tests/test_agent_authority_matrix.py` returned `4 passed`;
- evidence represented authorization as external and empirical execution as explicitly false;
- independent P9 evidence JSON and SHA-256 sidecar were successfully uploaded.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.  
P9 artifact: `9825316781`, digest `sha256:15e5ba72dd524f90b0bb3499c9b0b3f7de602f0e1905b0734183e830c22af671`.

This is **scoped independent verification evidence**, not full P9 closure. It does not establish P2/P6a for the completion candidate, P7 exact freeze binding, P8 analysis lock, durable external archive, experimental authorization, empirical execution, or efficacy.

## Superseded P9 evidence

Run `33567199896` remains scoped to superseded candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`. Its artifact was `9823570326` with ZIP digest `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`. This historical evidence does not transfer to `a43219b…`.

## Current runtime evidence

P2 and P6a both recorded the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

These runtime results are not transferable to `a43219b…` merely because the repository/workflows are shared.

## Documentation and provenance control rule

This document distinguishes **main tip, apparatus source, runtime candidate, completion candidate, candidate tree, and deployment identity**. Executable apparatus state changes reset the candidate cycle. Documentation-only commits do not silently redefine apparatus behavior. Evidence does not transfer across identities merely because the branch, repository, URL, or documentation lineage is shared.

Older audit records that state inline artifact validation is missing are **historical/stale claims**, not current implementation defects. Historical records remain preserved as historical snapshots; current-state documents state the present implementation and separately track remaining candidate-scoped evidence gaps.

## Historical-priority boundary

The historical review has been reconciled separately in `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

Current position: DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, organizational authority, veto/escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining hypothesis is a potentially distinctive **cross-domain integration** coupling formation-state governance to candidate-bound experimental verification and authorization. This is not an absolute novelty claim.

## Assurance boundary

CI success, deterministic tests, deployment readiness, runtime PASS, historical artifacts, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Any unresolved blinding, null-integrity, artifact-custody, reproducibility, analysis, P7 binding, P8, broader P9, freeze, or authorization predicate remains FAIL-CLOSED.

## Required closure sequence

`Current candidate selection → bind/reverify P2/P6a if needed → operational P3/P4/P5/P6 closure → P7 final binding → P8 verification → broader P9 evidence-chain closure → new immutable freeze → explicit authorization → blinded pilot`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
