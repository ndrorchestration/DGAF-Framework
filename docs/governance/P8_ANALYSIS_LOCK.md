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

The `main` branch is a living documentation/evidence lineage and is not itself the experimental apparatus identity. The active remediation/completion candidate is **`fb485e9e0fd253be03e6937a448f4818eb8d54a1`** on branch `remediation/p35-minimal-mainline-2026-09-02`, PR #199. It was created directly from current `main` `275756fd81c975f17ae3d16d24e599db0617cf85`.

The previous completion candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29` and previous runtime candidate `92ff830b1c67413df745e37087e6447c9c251b9a` remain historical evidence boundaries. Their evidence is not transferred to the active remediated candidate.

No deployment is currently claimed for PR #199. The previously recorded deployments remain bound to their original candidates and must not be substituted for the active candidate's runtime evidence.

| Binding | Value | State |
|---|---|---|
| Active completion/remediation candidate | `fb485e9e0fd253be03e6937a448f4818eb8d54a1` | CURRENT / PRE-FREEZE |
| Candidate branch | `remediation/p35-minimal-mainline-2026-09-02` | CURRENT |
| Candidate PR | `#199` | OPEN / DRAFT |
| Current `main` base | `275756fd81c975f17ae3d16d24e599db0617cf85` | BASE |
| Candidate deployment | none claimed | PENDING |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Analysis configuration | selected pre-freeze configuration | RE-BIND AT P8 CLOSURE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Governance CI | `.github/workflows/governance-ci.yml` | CURRENT; exact-SHA binding required |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION / PRE-FREEZE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |

## TGL/P-35 prerequisite — active remediation boundary

The previous completion candidate was found to omit an explicit `premise_check_fn` at the DGAF adapter boundary, while the underlying P-35 gate permits a missing checker to pass through. The pilot task path likewise did not supply one.

PR #199 is the current-mainline remediation. It requires an explicit callable `PDMAL_PREMISE_CHECKER` for DGAF pilot execution, rejects missing/malformed/unloadable/non-callable configuration, requires an explicit checker for `ConsensusTask(condition="dgaf")`, and propagates the checker through `DGAF_TGLAdapter` into `TGLHooks`. Regression coverage exercises the runner/task/adapter/TGL boundary and premise KILL behavior.

The active candidate has not yet received the exact-head pre-freeze runner evidence required for formal P-35 adjudication. Therefore P8 remains OPEN / FAIL-CLOSED.

No PDMAL-specific constitutional policy is invented by this remediation. Pilot execution remains blocked until the experimental-control design supplies and approves the appropriate checker.

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

The remediation implements the P-35 boundary but does not itself close P8.

## Protocol/candidate separation rule

The executable apparatus and living canonical protocol remain separate provenance objects. A protocol text does not constitute experimental data or authorization. Before freeze, the exact protocol blob, executable tree, analysis implementation/configuration, runner, artifact schema, TGL control-plane contract, and verification evidence must be captured and bound in the freeze manifest.

## Runtime deployment verification boundary

P2 and P6a must target the same exact candidate deployment after PR #199 is selected as the experimental candidate. The previously recorded deployments for `92ff830b…` and `a43219b…` are historical and cannot satisfy this requirement for `fb485e9e…`.

The exact deployment identity, source SHA, and authenticated P2/P6a results must be captured before P8 closure.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending:

1. Exact-head pre-freeze validation and formal P-35 adjudication for PR #199.
2. Selection of the resulting exact experimental candidate.
3. Re-binding analysis/schema/runner/protocol identities to that candidate.
4. Fresh candidate-bound PDMAL/P3–P6 and independent P9 verification.
5. P2 authenticated five-case runtime verification against the exact candidate deployment.
6. P6a authenticated four-case CORS verification against the same deployment identity.
7. Environment/topology reproducibility evidence.
8. Durable evidence retention with direct retrieval and integrity verification.
9. Current-boundary evidence review for E2b/M6, retaining their exact execution boundaries.
10. P7 exact freeze binding and formal closure of the adopted scientific decision record.
11. Independent P9 verification covering the final pre-freeze evidence chain.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.  
**Empirical N:** 0.  
**New freeze:** NOT CREATED.
