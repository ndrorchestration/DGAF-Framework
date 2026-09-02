---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
selected_experimental_candidate_sha: 58ba9a072f40e94638b0332eeec19dd882a7ff95
selected_experimental_candidate_tree: abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb
selected_experimental_candidate_pr: 192
selected_experimental_candidate_branch: candidate/p35-integrated-current-20260902
historical_runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
historical_runtime_candidate_tree: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
historical_runtime_deployment: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
active_p35_remediation_pr: 188
pilot_authorization: NOT_GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it. Documentation may advance independently of the experimental candidate; it must not silently transfer experimental evidence.

> **Current control-plane lineage:** `main` = `275756fd81c975f17ae3d16d24e599db0617cf85`.
>
> **Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Selected experimental candidate:** PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`, tree `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`. This is the September 2 pre-freeze verification boundary and is not frozen.
>
> **Historical runtime candidate:** `92ff830b…` / tree `73cf3ad…` with deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` is retained only as prior exact-scoped P2/P6a evidence. It is not the current candidate and its runtime evidence does not transfer.
>
> **Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Current candidate verification

PR #192 integrates the verified P-35 production boundary into a clean candidate derived from current `main`. The exact candidate has 18/18 successful GitHub Actions workflows, including Governance CI `33616403706`, Pre-Freeze Runner Validation `33616403754`, Pre-Authorization Security `33616403843`, Instrumentation Dry Run `33616403724`, and Harness Validation `33616403784`.

Candidate-bound artifacts include pre-freeze runner evidence (`9841238710`, ZIP digest `sha256:4948b6889b2e691d794a6d7dd3b8d600f15b16ccabebec330b44380120dbcf5e`), governance evaluation evidence (`9841231335`, ZIP digest `sha256:0658a9c3acde62fcb9d5634d7ccd7f90d1a209b403bd9db8331f9ac020e962`), freeze-control evidence (`9841228966`, ZIP digest `sha256:14585aae73c232ab8a927623dee3971d4c6e5cfb8abb63dd2907fc522aeaed09`), and instrumentation dry-run evidence (`9841100424`, ZIP digest `sha256:7cfb548a48105571c8a61e27a3af4b579d9d875cfcd94b11d45d8893f9d09841`).

The candidate workflow artifacts may carry GitHub's PR merge-ref execution identity (`fb1f4669…`) internally. That execution identity is retained as workflow provenance and is not substituted for the selected candidate head `58ba9a…`.

## Current deployment boundary

The exact selected candidate has not yet been bound to a READY Vercel deployment. The GitHub combined status reports Vercel `failure` at the build/deployment-rate-limit target. The latest Vercel deployment inventory contains READY deployments for other SHAs, including documentation-branch commits, but none with recorded Git SHA `58ba9a072f40e94638b0332eeec19dd882a7ff95`.

Therefore P2 and P6a remain OPEN and deployment-bound. The historical `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` runtime evidence remains non-transferable.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Selected experimental candidate | CURRENT / NOT FROZEN | PR #192 / `58ba9a…`; tree `abdbc9b…` |
| Exact deployment for selected candidate | NOT ESTABLISHED | No READY deployment with Git SHA `58ba9a…` |
| P2 runtime verification | OPEN / DEPLOYMENT-BOUND | Fresh authenticated 5-case matrix required on exact candidate deployment |
| P6a CORS verification | OPEN / DEPLOYMENT-BOUND | Fresh authenticated 4-case matrix required on same deployment |
| P3 | VERIFIED — ENGINEERING/CONTROL SCOPE | Current candidate CI, artifact, and instrumentation controls pass |
| P4 | OPEN | Current-cycle operational blinding/custody closure required |
| P5 | VERIFIED — VERIFIER/TOOLCHAIN SCOPE | Exact candidate hashes, lock, package/toolchain and deterministic instrumentation retained; full closure remains open |
| P6 | OPEN / FAIL-CLOSED | Durable independent archive/retrieval/hash proof required |
| P7 | EXACT-CANDIDATE BINDING RECORDED PRE-FREEZE | Scientific specification retained; final freeze identity not established |
| P8 | OPEN / FAIL-CLOSED | Requires current-candidate TGL/P-35, analysis, operational, and predecessor predicates |
| P9 | OPEN | Fresh independent final-candidate verification required |
| Freeze | NOT ESTABLISHED | No immutable frozen identity is authoritative |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No authorized pilot execution |

## P-35 remediation boundary

PR #188 remains an engineering remediation lineage. Its verified exact-head evidence establishes the explicit P-35 premise-hook boundary and fail-closed behavior, but the remediation head itself is not the selected experimental candidate and does not create a freeze or authorization state.

The remediation does not define an approved PDMAL-specific constitutional premise policy. That scientific-control decision remains separate.

## Historical evidence boundary

Historical runtime, completion-candidate, remediation, deployment, artifact, and P9 records remain valid only for their exact recorded identities. Earlier records may state `92ff830b…`, `a43219b…`, or other predecessor identities as current within their original temporal scope; such statements are not rewritten into the September 2 current boundary unless they are active control-plane assertions.

The prior `92ff830b…` runtime evidence is specifically preserved as historical P2/P6a evidence for deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. The prior `a43219b…` completion-candidate PDMAL/P9 evidence is likewise historical and non-transferable.

## Assurance boundary

CI success, deterministic dry runs, synthetic evaluator results, deployment readiness for another SHA, historical runtime PASS, or documentation reconciliation do not constitute efficacy evidence or pilot authorization. Current unresolved predicates remain FAIL-CLOSED.

## Required closure sequence

1. Establish an exact READY deployment whose recorded Git SHA equals `58ba9a…`.
2. Run authenticated P2 and P6a against that exact deployment.
3. Complete current-cycle P4 and durable-custody P6 evidence.
4. Preserve the exact P7 binding and close only against the final protocol/analysis/freeze identity.
5. Close P8 from current-candidate evidence.
6. Execute fresh independent P9 verification.
7. Create and independently verify a new immutable freeze.
8. Obtain explicit pilot authorization.
9. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
