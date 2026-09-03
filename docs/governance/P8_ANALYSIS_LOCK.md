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

The `main` branch is a living documentation/evidence lineage and is not itself the experimental apparatus identity. The current successor candidate for the closing cycle is **`48c12c6660df7decb61f9aac4d8560526a8754eb`** on branch `candidate/p35-validated-control-state-2026-09-02` (PR #200). Its exact candidate identity remains PRE-FREEZE / FAIL-CLOSED and is not authorization.

An exact candidate deployment exists for that same source identity:

- Vercel deployment: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- Deployment URL: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- State: READY
- Source branch: `candidate/p35-validated-control-state-2026-09-02`
- Deployment Git SHA: independently verified as `48c12c6660df7decb61f9aac4d8560526a8754eb`

This deployment is a candidate identity and deployment-health record. It does not substitute for authenticated P2/P6a runtime evidence.

The previous experimental/completion candidates remain historical and must not be used as the current P8 boundary merely because the executable structure or protocol is shared.

| Binding | Value | State |
|---|---|---|
| Current successor candidate | `48c12c6660df7decb61f9aac4d8560526a8754eb` | CURRENT / PRE-FREEZE |
| Candidate branch | `candidate/p35-validated-control-state-2026-09-02` | CURRENT |
| Exact Vercel deployment | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` | READY |
| Exact deployment URL | `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app` | CURRENT DEPLOYMENT IDENTITY |
| Deployment Git SHA confirmation | `48c12c6660df7decb61f9aac4d8560526a8754eb` | VERIFIED |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | SELECTED / PRE-FREEZE; RECONFIRM AT CLOSURE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Governance CI | `.github/workflows/governance-ci.yml` | CURRENT; exact-SHA binding required |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION / PRE-FREEZE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |

## TGL/P-35 prerequisite

The immutable P-35 validation boundary is PR #199 at exact SHA `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. PR #200 is the successor candidate derived from that boundary. The current successor passed its own exact-head PR validation wave, including Governance CI and the pre-freeze runner validation. Those results establish engineering/pre-freeze control integrity, not P8 authorization.

The active implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF pilot execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. The checker is propagated through the DGAF pilot path and unexpected premise-checker failures remain governed by the existing fail-closed P-35 path.

The successful PR #200 validation wave included the pre-freeze runner, pre-authorization security, Governance CI, control-state consistency/head binding, truth-layer validation/tests, epistemic evidence validation, DGAF regression, PDMAL harness validation, and instrumentation dry run. No pilot mode, freeze, authorization, or empirical collection was enabled.

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

The exact successor has passed the available engineering/pre-freeze validation controls, but those controls do not themselves close P8.

## Protocol/candidate separation rule

The executable apparatus and living canonical protocol remain separate provenance objects. A protocol text does not constitute experimental data or authorization. Before freeze, the exact protocol blob, executable tree, analysis implementation/configuration, runner, artifact schema, TGL control-plane contract, and verification evidence must be captured and bound in the freeze manifest.

## Runtime deployment verification boundary

P2 and P6a must target the same exact successor deployment:

- `candidate_sha`: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id`: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- P6a `expected_allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`, subject to any explicit `DGAF_ALLOWED_ORIGINS` runtime override.

Candidate/deployment identity must remain exact in all runtime artifacts. The deployment's READY state is necessary infrastructure evidence, not runtime predicate closure.

## Current exact-candidate engineering evidence

The exact successor instrumentation dry run is run `33701204328`, artifact `9873580197`, on candidate `48c12c…`. The artifact ZIP digest is `sha256:8df8c67d694f35c35824ac5511593e72ef9c2f182e835e5dbf5ee2aacb7e6dfa`. The pre-freeze runner produced artifact `9873664736` with digest `sha256:8ebbeeb635fb63d682ba4c95287cf7c6fe0eb9f669f7e1e68e8925bf5bc8ee54` and recorded `empirical_data_collection=false`, `status=pre-freeze`, and exact commit `48c12c66…`.

These artifacts support current engineering/pre-freeze controls and do not constitute P8 closure or experimental evidence.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending:

1. Candidate-bound authenticated P2 five-case runtime verification.
2. Candidate-bound authenticated P6a four-case CORS verification.
3. Final P3 artifact-contract evidence for the closing candidate.
4. Operational P4 blinding/custody evidence, including independent bijection verification and no premature unblinding.
5. Final P5 environment/topology/RNG reproducibility binding.
6. Durable P6 archive/retrieval/hash proof.
7. Exact P7 apparatus/candidate/protocol/analysis authority binding.
8. Fresh independent P9 verification of the same closing candidate and evidence chain.
9. Final freeze creation and independent verification.

A successful CI run, dry run, deployment readiness, or historical verification artifact is necessary supporting evidence but does not by itself close P8.

**Pilot authorization:** NOT GRANTED.  
**Empirical N:** 0.  
**New freeze:** NOT CREATED.
