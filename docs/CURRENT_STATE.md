---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
runtime_candidate_tree: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
latest_completion_candidate_sha: a43219b4ed91fff8615f6c655ab3d17ca871fc29
latest_completion_candidate_branch: completion/2026-09-01-exact-candidate
latest_completion_candidate_deployment: dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17
active_p35_remediation_branch: remediation/p35-premise-hook-2026-09-01
active_p35_remediation_pr: 188
active_p35_remediation_head: 61f1be8233a30afd7c155851eba16fb4084ec465
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` is the current production/runtime candidate recorded by the current mainline state. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`.
>
> **Latest completion candidate:** `a43219b4ed91fff8615f6c655ab3d17ca871fc29` remains the controlled exact candidate on branch `completion/2026-09-01-exact-candidate`. Its prior PDMAL/P9 evidence remains scoped to that exact tree and is not transferred to the remediation branch.
>
> **Active remediation:** PR #188 / branch `remediation/p35-premise-hook-2026-09-01` is currently at `61f1be8233a30afd7c155851eba16fb4084ec465`. Earlier remediation evidence on `cf84ca30cf34dce406ba80ab624ff24e38b181d3` is historical to that exact SHA. The current branch contains the pre-freeze runner workflow and documentation reconciliation, but no current-head pre-freeze runner result has been established.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Identity roles

- `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` — corrected seven-gate apparatus provenance anchor.
- `92ff830b1c67413df745e37087e6447c9c251b9a` — current production/runtime candidate on the mainline control-state record; exact tree `73cf3ad…`.
- `a43219b4ed91fff8615f6c655ab3d17ca871fc29` — controlled completion candidate; exact-candidate PDMAL/P9 verification target.
- `562753b3053b3566b0fcad1b0b1df151d7de119a` — superseded completion candidate with historical scoped P9 verification.
- `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` — exact tree of the current mainline runtime candidate.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — production deployment identity recorded by P2/P6a evidence for `92ff830b…`.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — exact-candidate preview deployment for `a43219b…`; READY / PREVIEW, with independent Git-SHA confirmation and authenticated P2/P6a verification still required.
- PR #188 / branch `remediation/p35-premise-hook-2026-09-01` — candidate-scoped engineering remediation for the P-35 premise-hook injection defect; current head `61f1be82…`; not a new experimental candidate and not authorization.
- `cf84ca30cf34dce406ba80ab624ff24e38b181d3` — prior remediation head with fresh CI evidence; historical and non-authoritative for the current PR head.
- Pre-correction candidates/deployments remain historical/non-closing and must not be reused as current dispatch inputs.
- Documentation commits advance `main` documentation lineage but do not silently redefine apparatus or completion-candidate identity.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for latest source and control documents. |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…`; seven-gate restoration plus complete provenance binding. |
| Runtime candidate identity | CURRENT / NOT FROZEN | `92ff830b…`; exact tree `73cf3ad…`. |
| Latest completion candidate | CONTROLLED / NOT FROZEN | `a43219b…`; prior exact-candidate evidence remains scoped to that tree. |
| Active P-35 remediation | OPEN / ENGINEERING ONLY | PR #188, current head `61f1be82…`; no freeze or authorization effect. |
| Pre-freeze runner implementation | PRESENT / UNVERIFIED ON CURRENT HEAD | Workflow exists and includes the P-35 runner regression; exact current-head execution and manifest are not established. |
| P2 runtime verification | VERIFIED — MAINLINE ONLY | Run `33509348174`; artifact `9800942933`; five required cases passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P6a CORS verification | VERIFIED — MAINLINE ONLY | Run `33509416955`; artifact `9800972819`; four required checks passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P3 | VERIFIED — HISTORICAL COMPLETION-CANDIDATE SCOPE | Run `33572123862`; artifact `9825740072`; exact candidate `a43219b…`; not transferable to PR #188 or a successor candidate. |
| P4 | WORKFLOW-LEVEL VERIFIED / OPERATIONAL CLOSURE OPEN | Prior completion-candidate evidence only; fresh current-candidate operational evidence remains required. |
| P5 | WORKFLOW-LEVEL VERIFIED / FULL CLOSURE OPEN | Prior completion-candidate evidence only; fresh current-candidate reproducibility closure remains required. |
| P6 | WORKFLOW-LEVEL VERIFIED / DURABLE ARCHIVE OPEN | Prior completion-candidate evidence only; durable external archive closure remains required. |
| P7 | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Exact apparatus/candidate/protocol/analysis authority binding remains required. |
| P8 | OPEN / FAIL-CLOSED | P-35 adapter defect was identified; remediation exists but has not become a verified experimental candidate. |
| P9 | HISTORICAL SCOPED PASS / CURRENT REMEDIATION REVERIFY REQUIRED | Run `33572123857` verified `a43219b…`; remediation changes require fresh exact-candidate P9 evidence. |
| Freeze | NOT ESTABLISHED | No frozen identity is currently authoritative for pilot execution. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## P-35 integration finding and remediation

The exact completion candidate `a43219b…` was audited against the established P-35/TGL interface. The TGL core passes `premise_check_fn` into `ProcludingPremiseGate.evaluate`, but the experimental `DGAF_TGLAdapter` did not previously provide a premise checker. The underlying P-35 implementation permits a missing checker to pass through all constitutional invariants, so the adapter boundary did not actually enforce premise-hook injection.

This was classified as a **candidate-scoped implementation defect / P8 closure blocker**, not experimental failure. The pilot task path also instantiated the DGAF task without a premise checker.

PR #188 addresses the defect by requiring explicit callable injection, propagating it through `TGLHooks` and `ConsensusTask`, sealing unexpected checker exceptions as `KILL`, and adding regression coverage for missing-checker refusal, injection, premise KILL, and checker-exception containment. The current branch also includes `test_run_pilot_p35.py` in the pre-freeze contract suite.

No PDMAL-specific constitutional policy is invented by this remediation. A real pilot remains blocked until the experimental-control design supplies and approves the appropriate premise checker. The remediation branch is engineering evidence only; it does not replace the current completion candidate or create a freeze.

## Current remediation verification boundary

Fresh CI was established for remediation head `cf84ca30…`, including repository coverage, truth-layer validation/tests, epistemic evidence validation, PDMAL instrumentation dry run, and P9 independent verification. Because the remediation branch subsequently advanced to `61f1be82…`, those runs are now historical evidence for `cf84ca30…` and must not be represented as current-head validation.

The current branch contains `.github/workflows/pdmal-pre-freeze-runner.yml`. That workflow is structurally appropriate: it requires a genuine hash-locked environment, runs the contract suite including `test_run_pilot_p35.py`, verifies contract mode, verifies pilot mode fails without freeze/authorization, checks artifact integrity, and emits a `PRE-FREEZE` manifest. However, no exact-current-head successful runner execution or manifest has been established in the audit record.

The current `61f1be82…` commit also carries a Vercel status failure explicitly described as **deployment rate limited — retry in 24 hours**. This is infrastructure/deployment evidence and is not classified as a P-35 code failure. Deployment verification remains incomplete.

## Current exact-candidate PDMAL evidence

Run `33572123862` completed successfully on 2026-09-01 for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The run verified exact checkout identity, presence of the withheld blinding secret, deterministic smoke reproduction, P5 RNG-stream separation, a `19 passed` structural/artifact suite, masked one-seed CSV generation, schema validation, CSV checksum integrity, artifact download round-trip, and inner-CSV checksum re-verification.

These results remain historical completion-candidate evidence and cannot certify the remediated branch.

Latest PDMAL artifact: `9825740072`.  
Artifact ZIP digest: `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae`.  
Evidence registry artifact: `9825740649`; ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.  
Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.

## Current exact-candidate P9 evidence

Run `33572123857` completed successfully on 2026-09-01 for candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Verified exact identity, independent `jq -S -c` canonicalization plus `sha256sum`, authority regression, external authorization representation, and explicit non-execution representation. This is **historical scoped independent verification evidence** for `a43219b…`. It cannot certify PR #188 or a successor candidate after material P-35 remediation.

Latest P9 artifact: `9825660346`, ZIP digest `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.

## Exact completion-candidate deployment

Deployment `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` remains the exact-candidate preview deployment associated with `a43219b…`. It reports READY / PREVIEW. Independent Vercel Git-SHA confirmation and authenticated P2/P6a workflow execution against that deployment remain required.

## Current runtime evidence

P2 and P6a both recorded production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

These runtime results are not transferable to `a43219b…`, PR #188, or any remediated successor candidate merely because repository/workflow structure is shared.

## Historical-priority boundary

The historical review is parked in `docs/research/DGAF_HISTORICAL_RESEARCH_PARKED_2026-09-01.md`.

Current position: DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, organizational authority, veto/escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining hypothesis is a potentially distinctive **cross-domain integration** coupling formation-state governance to candidate-bound experimental verification and authorization. This is not an absolute novelty claim.

## Assurance boundary

CI success, deterministic tests, deployment readiness, runtime PASS, historical artifacts, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Any unresolved blinding, null-integrity, artifact-custody, reproducibility, analysis, P7 binding, P8, broader P9, freeze, or authorization predicate remains FAIL-CLOSED.

## Required closure sequence

1. Complete PR #188 remediation review and current-head contract verification.
2. Establish a successful exact-current-head pre-freeze runner execution and manifest.
3. Select a resulting exact experimental candidate and rerun PDMAL instrumentation/P3–P6 and P9.
4. Independently confirm the exact Vercel deployment Git SHA.
5. Execute authenticated P2/P6a against the same exact candidate/deployment.
6. Complete current-cycle P4/P5/P6 operational evidence.
7. Resolve P7 as the external scientific decision and bind it exactly.
8. Close P8 only from current-candidate evidence.
9. Create and independently verify a new immutable freeze.
10. Obtain explicit pilot authorization.
11. Only then execute the authorized blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
