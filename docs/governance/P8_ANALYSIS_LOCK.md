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

The current `main` branch is a living documentation/evidence lineage and is not itself the experimental apparatus identity. The experimental verification boundary remains candidate-scoped at **`ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`** pending any separately governed candidate transition.

PR #132 exposed a TGL/P-35 control-plane contract regression (41 passed / 2 failed). PR #133 is an isolated remediation candidate. TGL remediation is a prerequisite to reliable candidate verification, not a P8 closure event and not an authorization transition.

| Binding | Value | State |
|---|---|---|
| Experimental verification boundary | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` | CURRENT CANDIDATE BOUNDARY |
| TGL remediation | PR #133 | DRAFT / VALIDATION PENDING |
| Blocked regression | PR #132 | DRAFT / UNMERGED |
| Historical candidate | `e6beeb66335e1b50a239697badab22dab50eb5ba` | HISTORICAL |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | SELECTED / PRE-FREEZE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Governance CI | `.github/workflows/governance-ci.yml` | CURRENT; exact-SHA binding required |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION / PRE-FREEZE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |

## TGL prerequisite

Before candidate-scoped P8 closure, the TGL/P-35 contract must be validated on the exact source tree intended for subsequent candidate binding. The required contract surface includes:

- established P-35 constructor and `evaluate(..., check_fn=...)` compatibility;
- premise-hook injection actually reaching P-35;
- fail-closed containment of unexpected hook exceptions;
- explicit required versus conditional gate semantics;
- deterministic `PASS/WARN/SKIP/ESCALATE/KILL` reduction;
- distinction between unwired and dependency-suppressed `SKIP`;
- audit seal coverage of the exact returned audit object;
- regression coverage for these semantics.

A passing TGL remediation test suite does not itself close P8, alter P7, create a freeze, or authorize the pilot.

## Protocol/candidate separation rule

The executable apparatus and living canonical protocol remain separate provenance objects. A protocol text does not constitute experimental data or authorization. Before freeze, the exact protocol blob, executable tree, analysis implementation/configuration, runner, artifact schema, TGL control-plane contract, and verification evidence must be captured and bound in the freeze manifest.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending:

1. Closure of the TGL/P-35 prerequisite on the exact intended candidate tree.
2. Re-binding analysis/schema/runner/protocol identities to the resulting candidate verification boundary if the apparatus changes.
3. P2 authenticated five-case runtime verification against the exact deployment.
4. P6a authenticated four-case CORS verification against the same deployment identity.
5. Environment/topology reproducibility evidence.
6. Durable evidence retention with direct retrieval and integrity verification.
7. Current-boundary evidence review for E2b/M6, retaining their exact execution boundaries.
8. P7 exact freeze binding and formal closure of the adopted scientific decision record.
9. Independent P9 verification.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.  
**Empirical N:** 0.  
**New freeze:** NOT CREATED.
