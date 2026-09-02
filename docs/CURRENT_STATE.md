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
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.
>
> **Runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` is the current production/runtime candidate recorded by the current mainline state. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`.
>
> **Latest completion candidate:** `a43219b4ed91fff8615f6c655ab3d17ca871fc29` is the current exact candidate on branch `completion/2026-09-01-exact-candidate`. It has fresh successful PDMAL and scoped P9 verification runs. An exact-candidate Vercel preview deployment exists as `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`; deployment Git-SHA confirmation remains an external verification step.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Identity roles

- `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` — corrected seven-gate apparatus provenance anchor.
- `92ff830b1c67413df745e37087e6447c9c251b9a` — current production/runtime candidate on the mainline control-state record; exact tree `73cf3ad…`.
- `a43219b4ed91fff8615f6c655ab3d17ca871fc29` — current controlled completion candidate; exact-candidate PDMAL/P9 verification target.
- `562753b3053b3566b0fcad1b0b1df151d7de119a` — superseded completion candidate with historical scoped P9 verification.
- `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` — exact tree of the current mainline runtime candidate.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — current production deployment identity recorded by both P2 and P6a runtime evidence for `92ff830b…`.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — exact-candidate preview deployment created from `deploy/exact-candidate-a43219b`; READY; pending independent Vercel Git-SHA confirmation and authenticated P2/P6a verification.
- PR #188 / branch `remediation/p35-premise-hook-2026-09-01` — candidate-scoped engineering remediation for the P-35 premise-hook injection defect found on `a43219b…`; not a new experimental candidate and not authorization.
- Pre-correction candidates/deployments remain historical/non-closing and must not be reused as current dispatch inputs.
- Documentation commits advance `main` documentation lineage but do not silently redefine apparatus or completion-candidate identity.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for latest source and control documents. |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…`; seven-gate restoration plus complete provenance binding. |
| Runtime candidate identity | CURRENT / NOT FROZEN | `92ff830b…`; exact tree `73cf3ad…`. |
| Latest completion candidate | CONTROLLED / NOT FROZEN | `a43219b…`; exact-candidate verification target on completion branch. |
| Exact completion deployment | READY / PREVIEW / PENDING VERIFICATION | `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`; source branch `deploy/exact-candidate-a43219b`; Vercel Git SHA still requires independent confirmation. |
| P2 runtime verification | VERIFIED — MAINLINE ONLY | Run `33509348174`; artifact `9800942933`; five required cases passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P6a CORS verification | VERIFIED — MAINLINE ONLY | Run `33509416955`; artifact `9800972819`; four required checks passed for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. |
| P3 | VERIFIED — COMPLETION CANDIDATE WORKFLOW SCOPE | Run `33572123862`; artifact `9825740072`; exact candidate `a43219b…`; structural/artifact checks passed. |
| P4 | WORKFLOW-LEVEL VERIFIED / OPERATIONAL CLOSURE OPEN | Run `33572123862`; blinding secret presence verified without disclosure and masked dry-run produced. Full operational custody/separation remains required. |
| P5 | WORKFLOW-LEVEL VERIFIED / FULL CLOSURE OPEN | Run `33572123862`; exact artifact binding, RNG stream separation, deterministic digest, and environment fingerprint recorded. Full reproducibility closure remains required. |
| P6 | WORKFLOW-LEVEL VERIFIED / DURABLE ARCHIVE OPEN | Run `33572123862`; artifact download plus inner checksum re-verification passed. Durable external archive closure remains required. |
| P7 | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Adopted/final freeze binding is not yet evidenced; exact apparatus/candidate/protocol/analysis authority binding remains required. |
| P8 | OPEN / FAIL-CLOSED | `a43219b…` exposed a concrete P-35 adapter wiring defect; PR #188 supplies the scoped remediation, but fresh candidate verification and all remaining P8 predicates are outstanding. |
| P9 | SCOPED PASS / REMEDIATION-BOUND REVERIFY REQUIRED | Run `33572123857` passed exact identity, independent `jq -S -c`/`sha256sum` check, and 4-test authority regression for `a43219b…`; after a material remediation, the resulting candidate requires fresh P9 evidence. |
| Freeze | NOT ESTABLISHED | No frozen identity is currently authoritative for pilot execution. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## P-35 integration finding and remediation

The exact completion candidate `a43219b…` was audited against the established P-35/TGL interface. The TGL core passes `premise_check_fn` into `ProcludingPremiseGate.evaluate`, but the experimental `DGAF_TGLAdapter` did not previously provide a premise checker. The underlying P-35 implementation permits a missing checker to pass through all constitutional invariants, so the adapter boundary did not actually enforce premise-hook injection.

This was classified as a **candidate-scoped implementation defect / P8 closure blocker**, not experimental failure. The pilot task path also instantiated the DGAF task without a premise checker.

PR #188 (`remediation/p35-premise-hook-2026-09-01`) addresses the defect by:

- requiring an explicit callable `premise_check_fn` at the adapter boundary;
- propagating it into `TGLHooks.premise_check_fn`;
- requiring the checker for `ConsensusTask(condition="dgaf")`;
- containing unexpected P-35 checker exceptions as a sealed `KILL` rather than permitting bypass;
- adding regression coverage for missing-checker refusal, injection, premise KILL, and checker-exception containment.

No PDMAL-specific constitutional policy is invented by this remediation. A real pilot remains blocked until the experimental-control design supplies and approves the appropriate premise checker. The remediation branch is therefore engineering evidence only; it does not replace the current completion candidate or create a freeze.

## Current exact-candidate PDMAL evidence

Run `33572123862` completed successfully on 2026-09-01 for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The run verified exact checkout identity, presence of the withheld blinding secret, deterministic smoke reproduction, P5 RNG-stream separation, a `19 passed` structural/artifact suite, masked one-seed CSV generation, schema validation, CSV checksum integrity, artifact download round-trip, and inner-CSV checksum re-verification.

The run emitted an evidence registry marking P3/P4/P5/P6 `VERIFIED` at workflow scope and a controller evaluation that kept P2/P7/P8/P9 blocking. P4 and P6 are explicitly workflow-level/synthetic custody evidence rather than full operational closure; P5 is also not full closure until the remaining reproducibility and candidate-binding requirements are satisfied.

Latest PDMAL artifact: `9825740072`.  
Artifact ZIP digest: `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae`.  
Evidence registry artifact: `9825740649`; ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.  
Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.

## Current exact-candidate P9 evidence

Run `33572123857` completed successfully on 2026-09-01 for candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Verified:

- `git rev-parse HEAD` matched `GITHUB_SHA`;
- independent `jq -S -c` canonicalization plus `sha256sum` matched the deterministic-case digest;
- `tests/test_agent_authority_matrix.py` returned `4 passed`;
- evidence represented authorization as external and empirical execution as explicitly false;
- independent P9 evidence JSON and SHA-256 sidecar were successfully uploaded.

Latest P9 artifact: `9825660346`, ZIP digest `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.

This is **scoped independent verification evidence**, not full P9 closure. Because PR #188 materially changes the P-35 adapter/task boundary, its P9 evidence cannot certify the remediated tree; fresh exact-candidate P9 evidence is required after the remediation becomes the selected candidate.

## Exact completion-candidate deployment

Deployment `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` was created from the exact-candidate deployment branch `deploy/exact-candidate-a43219b`, which points to `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

The deployment reports **READY** with target **preview**. Its URL is `https://dynamicgovernanceagenticformation-lhp3s3sv5-ndrorchestration.vercel.app`.

Unauthenticated root and API paths receive Vercel SSO redirects. This is treated as a deployment-authentication property, not runtime failure. The remaining deployment predicate is independent confirmation that Vercel's recorded Git source SHA is exactly `a43219b…`, followed by authenticated P2/P6a workflow execution against this deployment.

## Current runtime evidence

P2 and P6a both recorded the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

These runtime results are not transferable to `a43219b…` or to any remediated successor candidate merely because repository/workflow structure is shared.

## Historical-priority boundary

The historical review has been reconciled separately and is now explicitly parked for later resumption in `docs/research/DGAF_HISTORICAL_RESEARCH_PARKED_2026-09-01.md`.

Current position: DGAF is not established as first in the individual mechanisms of agent governance, dynamic formation, organizational authority, veto/escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification. The remaining hypothesis is a potentially distinctive **cross-domain integration** coupling formation-state governance to candidate-bound experimental verification and authorization. This is not an absolute novelty claim.

## Assurance boundary

CI success, deterministic tests, deployment readiness, runtime PASS, historical artifacts, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Any unresolved blinding, null-integrity, artifact-custody, reproducibility, analysis, P7 binding, P8, broader P9, freeze, or authorization predicate remains FAIL-CLOSED.

## Required closure sequence

1. Complete PR #188 remediation review and candidate-bound tests.
2. Select a resulting exact candidate and rerun PDMAL instrumentation/P3–P6 and P9.
3. Independently confirm the exact Vercel deployment Git SHA.
4. Execute authenticated P2/P6a against the same exact candidate/deployment.
5. Complete current-cycle P4/P5/P6 operational evidence.
6. Resolve P7 as the external scientific decision and bind it exactly.
7. Close P8 only from current-candidate evidence.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the authorized blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
