# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Authority:** DGAF/PDMAL experimental-design control  
**Purpose:** Bind the executable primary analysis and its artifact contract to the designated runtime candidate before any unblinding or empirical interpretation.

## Current authoritative boundary

The `main` branch is a living documentation/evidence lineage and is not itself the experimental runtime identity.

| Binding | Value | State |
|---|---|---|
| Current `main` | `8ae37faee637d3992dfec2f635ea4d1d9252ef2d` | DOCUMENTATION / CONTROL-PLANE LINEAGE |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | CURRENT / PRE-FREEZE |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | CURRENT |
| Exact Vercel deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | READY / PRODUCTION / EXACT-CANDIDATE VERIFIED |
| Candidate deployment URL | `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app` | CURRENT-CANDIDATE RUNTIME SURFACE |
| Historical completion candidate | `a43219b4ed91fff8615f6c655ab3d17ca871fc29` | HISTORICAL / SUPERSEDED |
| Historical preview deployment | `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` | HISTORICAL / SUPERSEDED |

The candidate/deployment tuple above is the same tuple used by the successful authenticated P2 and P6a runs below. Historical candidate evidence remains non-transferable unless an explicit provenance relation binds it.

## P7 scientific inputs selected

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed, paired by root seed identity.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean of complete paired seed effects.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- No outcome-dependent weighting, exclusion, or silent imputation.
- Bootstrap: 10,000 paired-seed percentile resamples.
- Deterministic bootstrap seed: `20260823`.
- Confidence interval: two-sided 95%, `alpha=0.05`.
- Directional support rule: estimate > 0 and CI lower bound > 0.

These choices are selected pre-freeze design inputs. They are not empirical results and do not authorize execution.

## P5 analysis implementation/configuration identity binding

The designated candidate already contains the locked primary-analysis implementation and deterministic configuration. This record binds their current exact identities so no additional analysis implementation should be created merely to satisfy provenance bookkeeping.

| Analysis object | Exact identity | State |
|---|---|---|
| Analysis implementation path | `experiments/pdmal_pilot/analysis.py` | CURRENT-CANDIDATE |
| Analysis implementation Git blob SHA | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | BOUND |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | BOUND |
| Pilot runner path | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-CANDIDATE |
| Pilot runner Git blob SHA | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | BOUND |
| Pilot artifact schema path | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-CANDIDATE |
| Pilot artifact schema Git blob SHA | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | BOUND |
| Protocol version encoded by runner | `0.7.5` | SELECTED / PRE-FREEZE |

The analysis implementation consumes validated pilot seed artifacts; it does not execute trials, regenerate observations, silently repair data, or authorize unblinding. The deterministic analysis configuration serializes the primary contrast, estimand, bootstrap method/resamples/seed, confidence level, secondary-policy marker, topology set, and failure-count set.

**P5 disposition after this reconciliation:** exact analysis implementation/configuration identities are recorded and candidate-scoped. P5 must not be promoted to CLOSED solely because this documentation branch exists; closure requires this binding to land on the authoritative control plane and pass the normal consistency/review checks.

## P2 authenticated runtime matrix — CLOSED / VERIFIED

Exact-candidate workflow run `33730195621`:

- candidate SHA: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`;
- deployment ID: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`;
- protected Vercel automation bypass credential present, value withheld;
- all five predeclared runtime cases matched their expected HTTP/decision outcomes;
- artifact: `9883521704`;
- artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

The valid request's expected HTTP 503 / `BLOCKED` result reflects fail-closed behavior because live audit state is not wired into `/api/orchestrate`. It is not application-health or efficacy evidence.

## P6a authenticated CORS matrix — CLOSED / VERIFIED

Exact-candidate workflow run `33728695806`:

- candidate SHA: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`;
- deployment ID: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`;
- allowed origin: `https://dynamicgovernanceagenticformation.vercel.app`;
- allowed-origin POST: PASS;
- disallowed-origin POST: PASS;
- allowed-origin preflight: PASS, HTTP 204 with required origin/method/header coverage;
- disallowed-origin preflight: PASS, HTTP 403 without allow-origin header;
- artifact: `9882965299`;
- artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This evidence is scoped only to the tested endpoint, deployment, environment, and configured origins. It is not efficacy evidence.

## P3/P4/P6 context

- **P3 — CLOSED / VERIFIED** for the designated candidate's structural/artifact contract. This is contract evidence, not empirical efficacy evidence.
- **P4 — OPEN / EVIDENCE PRESENT.** Synthetic mock-key blinding/bijection/leakage/freeze-order checks pass, but actual human/key custody and access separation remain unestablished. CI cannot substitute for that operational requirement.
- **P6 — CLOSED / VERIFIED** for the retained current-candidate evidence set through independent archive/retrieval/hash equality.

## P7/P8/P9 boundary

P7's scientific target is adopted, but final exact binding remains open until the candidate/protocol/analysis/schema/runner identities and all prerequisite evidence are accepted together at the freeze boundary.

P8 remains **OPEN / FAIL-CLOSED**. This document records the analysis-lock identities but does not itself create the immutable freeze.

P9 remains **NOT EXECUTED** for the final bound chain. Independent verification must occur after the final pre-freeze packet is complete; it must not be replaced by the same repository asserting its own closure.

## Remaining closure blockers

1. Establish real P4 human/key custody and access separation.
2. Land and verify the P5 exact analysis implementation/configuration identity binding recorded above.
3. Bind P7 exactly to candidate, tree, protocol, analysis implementation/configuration, runner, schema, runtime evidence, and durable-custody identities.
4. Close P8 only after all prerequisites are exact-bound and the immutable freeze is independently verified.
5. Execute fresh independent P9 verification of the final bound chain.
6. Record separate pilot authorization only after freeze verification.
7. Only then permit blinded empirical execution.

## Protocol/candidate separation rule

The executable apparatus, living canonical protocol, control-plane documentation, deployment state, and empirical artifacts are separate provenance objects. A protocol text, green CI run, READY deployment, synthetic blinding result, or archive success does not constitute experimental data or authorization.

Before freeze, the exact protocol blob/version, executable candidate/tree, analysis implementation/configuration, runner, artifact schema, TGL control-plane contract, runtime evidence, custody evidence, and independent verification evidence must be captured and bound in the freeze manifest.

## Explicit non-claims

This reconciliation does **not**:

- create a freeze;
- authorize a pilot;
- unblind any condition;
- increase empirical N;
- convert deployment health into runtime efficacy evidence;
- convert synthetic P4 evidence into human-custody evidence;
- transfer evidence from a superseded candidate without exact provenance.

**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Unblinding: NOT EXECUTED.**  
**Empirical N: 0.**
