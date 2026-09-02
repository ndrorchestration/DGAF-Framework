# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Authority:** DGAF/PDMAL experimental-design control  
**Purpose:** Bind the executable primary analysis and its artifact contract to the P7 scientific target before any unblinding or empirical interpretation.

## P7 inputs fixed

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed, paired by root seed identity.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean of complete paired seed effects.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- No outcome-dependent weighting, exclusion, or silent imputation.

## Current verification boundary

The `main` branch is a living documentation/evidence lineage and is not itself the experimental apparatus identity. The current controlled completion candidate is **`a43219b4ed91fff8615f6c655ab3d17ca871fc29`** on branch `completion/2026-09-01-exact-candidate`. Its exact tree is the candidate identity for the current completion verification cycle.

An exact candidate deployment exists for that same source lineage:

- Vercel deployment: `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`
- Deployment URL: `https://dynamicgovernanceagenticformation-lhp3s3sv5-ndrorchestration.vercel.app`
- Target: preview
- Deployment state: READY
- Source branch used for deployment: `deploy/exact-candidate-a43219b`
- Required final external confirmation: deployment Git SHA must be independently confirmed as `a43219b4ed91fff8615f6c655ab3d17ca871fc29` through Vercel dashboard/API.

The deployment is SSO-protected from this environment. Redirects to Vercel SSO on root and API paths are therefore **not** evidence of runtime failure. Until authenticated P2/P6a execution succeeds, this deployment is a deployment identity, not runtime verification evidence.

The previous experimental verification boundary `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` is historical and must not be used as the current P8 candidate boundary.

| Binding | Value | State |
|---|---|---|
| Controlled completion candidate | `a43219b4ed91fff8615f6c655ab3d17ca871fc29` | CURRENT / PRE-FREEZE |
| Completion candidate branch | `completion/2026-09-01-exact-candidate` | CURRENT |
| Exact deployment branch | `deploy/exact-candidate-a43219b` | CURRENT DEPLOYMENT SOURCE |
| Exact Vercel deployment | `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` | READY / PREVIEW |
| Exact deployment URL | `https://dynamicgovernanceagenticformation-lhp3s3sv5-ndrorchestration.vercel.app` | PENDING AUTHENTICATED RUNTIME VERIFICATION |
| Deployment Git SHA confirmation | `a43219b4ed91fff8615f6c655ab3d17ca871fc29` | EXTERNAL CONFIRMATION REQUIRED |
| Historical experimental boundary | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` | HISTORICAL / SUPERSEDED |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | SELECTED / PRE-FREEZE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Governance CI | `.github/workflows/governance-ci.yml` | CURRENT; exact-SHA binding required |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION / PRE-FREEZE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |

## TGL/P-35 prerequisite — verified remediation boundary

The exact completion candidate `a43219b…` was found to have a candidate-scoped P-35 integration defect: the experimental `DGAF_TGLAdapter` did not provide a premise checker, and the pilot task path likewise did not supply one. The generic P-35 implementation treats a missing checker as pass-through, so the candidate did not demonstrate the required premise-hook injection.

PR #188 remediated that defect. The current remediation head is `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`. It requires an explicit callable premise checker through the DGAF adapter and pilot runner, propagates the checker into `TGLHooks`/`ConsensusTask`, handles unexpected checker exceptions fail-closed, and preserves a sealed P-35/KILL audit result on premise violation.

The exact-current-head pre-freeze runner validation run `33590352168` completed successfully for `d83ea74…`. Its contract suite included `test_run_pilot_p35.py`, and the workflow also verified contract-mode execution, pilot-mode failure without freeze/authorization, artifact schema/integrity checks, and PRE-FREEZE manifest emission. Artifact `9831586822` is the uploaded manifest; its workflow artifact digest is `sha256:dedacba56b8430fd995c4230e52fe208d2380f5e5015fa3816073cda3e9d774e`.

This is **pre-freeze engineering verification of the remediation head**, not verification of an experimental candidate. Because `d83ea74…` materially changes the apparatus relative to `a43219b…`, the prior completion-candidate PDMAL/P9 evidence does not transfer. A new exact experimental candidate must be selected after remediation review, followed by fresh candidate-bound P3–P9 and affected P2/P6a verification.

## TGL prerequisite — broader contract

The required contract surface includes:

- established P-35 constructor and `evaluate(..., check_fn=...)` compatibility;
- premise-hook injection actually reaching P-35;
- fail-closed containment of unexpected hook exceptions;
- explicit required versus conditional gate semantics;
- deterministic `PASS/WARN/SKIP/ESCALATE/KILL` reduction;
- distinction between unwired and dependency-suppressed `SKIP`;
- audit seal coverage of the exact returned audit object;
- regression coverage for these semantics.

The remediation now has exact-head pre-freeze evidence for these P-35 integration paths, but that evidence does not itself close P8, alter P7, create a freeze, or authorize the pilot.

## Protocol/candidate separation rule

The executable apparatus and living canonical protocol remain separate provenance objects. A protocol text does not constitute experimental data or authorization. Before freeze, the exact protocol blob, executable tree, analysis implementation/configuration, runner, artifact schema, TGL control-plane contract, and verification evidence must be captured and bound in the freeze manifest.

## Runtime deployment verification boundary

P2 and P6a must target the same exact candidate deployment:

- `candidate_sha`: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`
- `deployment_id`: `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`
- `base_url`: `https://dynamicgovernanceagenticformation-lhp3s3sv5-ndrorchestration.vercel.app`
- deployment source branch: `deploy/exact-candidate-a43219b`
- P6a `expected_allowed_origin`: the exact origin served by the deployment above.

The deployment must first be independently confirmed as serving the exact candidate SHA. P2/P6a workflow evidence is candidate-scoped only when the workflow records the exact deployment identity and candidate binding.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending:

1. Selection of a new exact experimental candidate after the verified P-35 remediation.
2. Re-binding analysis/schema/runner/protocol identities to that resulting candidate verification boundary.
3. Fresh candidate-bound PDMAL/P3–P6 and independent P9 verification.
4. P2 authenticated five-case runtime verification against the exact candidate deployment.
5. P6a authenticated four-case CORS verification against the same deployment identity.
6. Environment/topology reproducibility evidence.
7. Durable evidence retention with direct retrieval and integrity verification.
8. Current-boundary evidence review for E2b/M6, retaining their exact execution boundaries.
9. P7 exact freeze binding and formal closure of the adopted scientific decision record.
10. Independent P9 verification covering the final pre-freeze evidence chain.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.  
**Empirical N:** 0.  
**New freeze:** NOT CREATED.
