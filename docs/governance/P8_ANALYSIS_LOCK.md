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

An exact candidate deployment now exists for that same source lineage:

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

## TGL/P-35 prerequisite — CURRENT FINDING

The exact candidate exposes the established P-35 interface and the TGL core correctly calls `ProcludingPremiseGate.evaluate(..., check_fn=...)`. However, the experimental `DGAF_TGLAdapter` currently constructs `TGLHooks` without assigning `premise_check_fn`. Because the P-35 implementation treats a missing `check_fn` as pass-through, the adapter path does not demonstrate the required premise-hook injection. The pilot `ConsensusTask._dgaf_update` likewise instantiates the adapter without a premise checker.

This is a **candidate-scoped implementation defect / closure blocker**, not a runtime efficacy result.

The exact candidate tests corroborate the gap: TGL unit tests explicitly exercise injected premise hooks, while `experiments/pdmal_pilot/test_dgaf_tgl_adapter.py` exercises the adapter without supplying a premise hook and has no assertion that adapter-level P-35 injection actually occurs.

The remediation must establish, on a new exact candidate derived from the current candidate or its approved successor:

- an explicit, non-implicit `premise_check_fn` path into `DGAF_TGLAdapter`;
- propagation of that function into `TGLHooks.premise_check_fn`;
- fail-closed handling of unexpected premise-hook exceptions;
- a candidate-bound regression proving that a deliberately failing premise hook produces a P-35 KILL rather than silent pass-through;
- confirmation that the pilot task path supplies the intended premise checker rather than relying on the P-35 default;
- fresh exact-candidate PDMAL/P9 verification after remediation.

Until those conditions are demonstrated, P8 remains fail-closed and the current candidate must not be promoted to freeze.

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

A passing TGL/control-plane remediation test suite does not itself close P8, alter P7, create a freeze, or authorize the pilot.

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

1. Remediation and exact-candidate verification of the P-35 premise-hook defect identified above.
2. Re-binding analysis/schema/runner/protocol identities to the resulting candidate verification boundary if the apparatus changes.
3. P2 authenticated five-case runtime verification against deployment `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`.
4. P6a authenticated four-case CORS verification against the same deployment identity.
5. Environment/topology reproducibility evidence.
6. Durable evidence retention with direct retrieval and integrity verification.
7. Current-boundary evidence review for E2b/M6, retaining their exact execution boundaries.
8. P7 exact freeze binding and formal closure of the adopted scientific decision record.
9. Independent P9 verification covering the final pre-freeze evidence chain.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.  
**Empirical N:** 0.  
**New freeze:** NOT CREATED.
