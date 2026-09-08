---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-08
canonical_high_assurance_empirical_n: 0
final_candidate_status: NOT_DESIGNATED
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
historical_runtime_evidence_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
historical_runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
solo_epoch_004_status: LOCKED_NEGATIVE_EXACT_TREATMENT_EVIDENCE
seven_gate_treatment_fidelity: NOT_ESTABLISHED
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_protocol: PREREGISTERED
track_a_primary_analysis: LOCKED_NONEMPIRICAL
track_a_runner: UNDER_REVIEW_NOT_AUTHORIZED
track_a_freeze: NOT_ESTABLISHED
track_a_empirical_execution: NOT_AUTHORIZED
b1_profile: IMPLEMENTED
b1_qualification: UNDER_REVIEW
b2_profile: IMPLEMENTED
b2_qualification: MERGED_DEVELOPER_SELF_ATTESTED_NONINDEPENDENT
b2_integration_adjudication: UNDER_REVIEW
b3_profile: IMPLEMENTED
b3_qualification: MERGED_DEVELOPER_SELF_ATTESTED_NONINDEPENDENT
b3_integration_adjudication: UNDER_REVIEW
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded. Evidence is scoped to the exact identities and predicates that produced it. Engineering, diagnostic, Solo empirical, and canonical High-Assurance evidence classes must not be conflated.

## Canonical High-Assurance boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · canonical High-Assurance empirical N = 0.**

The final v0.7.6 High-Assurance candidate is still **NOT DESIGNATED**. The current **apparatus source**, **candidate identity**, and **deployment identity** remain governed by their exact historical/control records and are not rotated by repository `main` recency. Historical runtime evidence remains exact-scoped to the identities that produced it and does not transfer automatically to a later candidate. P4 real custody/admission, final P7 binding, P8 immutable freeze, final independent P9, and explicit authorization remain separate gates.

## Solo Epoch 004 — completed empirical evidence

The bounded Solo track is separate from the canonical High-Assurance sequence.

Epoch `PDMAL-SOLO-CANONICAL-EPOCH-004` executed 50 fresh paired seeds across 4 conditions × 5 topologies × 9 failure levels = **9,000 observations**. The locked primary analysis used the preregistered paired seed-level `DGAF - null` FFCR contrast, 10,000 percentile bootstrap resamples, analysis RNG seed `20260823`, and α=`0.05`.

Locked primary result:

- DGAF FFCR: `0.7337777777777778`
- null FFCR: `0.8275555555555555`
- paired effect: `-0.0937777777777778`
- two-sided 95% CI: `[-0.11822222222222223, -0.07066666666666668]`
- mechanical classification: **`EVIDENCE_AGAINST_DIRECTIONAL_DGAF`**

This result is preserved as negative evidence for the **exact executed restored-binding treatment** under Solo developer/non-independent custody. It is not independent validation, High-Assurance evidence, production-readiness evidence, or a universal claim about DGAF.

## Post-Epoch-004 treatment-fidelity audit

A later source-bound seven-gate audit found that the Epoch 004 execution did not establish canonical treatment fidelity for six constitutive gate bindings:

- P-31 SCPE — **NOT ESTABLISHED**
- P-33 convergence — **NOT ESTABLISHED**
- DemiJoule — **NOT ESTABLISHED**
- P-27 KAPPA — **NOT ESTABLISHED**
- P-29 Sentinel — **NOT ESTABLISHED**
- P-32 Phi Closure — **NOT ESTABLISHED**
- external P-30 / 11Q qualification — **ESTABLISHED**, developer self-attested/non-independent

Therefore:

**`EPOCH_004_PRIMARY_RESULT = PRESERVED`**  
**`SEVEN_GATE_TREATMENT_FIDELITY = NOT_ESTABLISHED`**  
**`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`**

The historical analysis is not recalculated or rewritten.

## Prospective workload-specific evaluation architecture

PR #395 split prospective evaluation into distinct workload tracks:

| Track | Scope | Current boundary |
|---|---|---|
| A | Numeric PDMAL topology robustness | protocol preregistered; primary analysis locked; fail-closed runner under review |
| B1 | Semantic routing and safety | implementation merged; source-bound 11Q qualification under review |
| B2 | Persistent SCPE/Phi context and closure | implementation + 11Q qualification merged; integration-readiness adjudication under review |
| B3 | Persistent P-33 weighted-graph convergence monitoring | implementation + 11Q qualification merged; integration-readiness adjudication under review |
| C | Integrated DGAF system | deferred until component tracks are separately composition-eligible |

Historical Epoch 004 remains immutable exact-treatment provenance and is not silently reused as the prospective integrated Track C identity.

## Track A status

Track A uses neutral algorithm identity `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`.

Completed gates:

- workload architecture merged;
- structural profile merged;
- retained 90-cell structural artifact produced;
- developer self-attested/non-independent P-30/P-11 11Q qualification: **108/110 (98.18%), S-TIER, Q11=9**;
- structural matrix adjudicated: 90/90 unique cells, zero recovery mismatches, zero no-failure phase mismatches, and failure-active changes in all 80 positive-failure cells;
- prospective Track A Epoch 001 preregistration merged as `26077b27ca336454148006e6daf4cd087005b421`;
- primary analysis implementation merged and locked as `e9ea59ad839aef33fbce10ed04c2157358c4326d`, with analysis blob `76bc8e9604c5d7e039e324e73036f353dc8ea31f` and analysis-config SHA-256 `355b164f69e91405819f092d0721b7597b87b06de79394a0c451169410a5ab6d`.

The preregistered scientific panel is fixed at 50 seeds (`20270101..20270150`) × 5 topologies × 9 failure counts = **2,250 observations if later authorized**. The primary endpoint is boolean `ffcr_success`; the confirmatory estimand is the mean paired-seed PDMAL-minus-random-regular FFCR difference, with 10,000 paired percentile bootstrap resamples and bootstrap seed `20270151`.

PR #431 is the current runner implementation lane. Its contract requires exact upstream source/analysis bindings, neutral algorithm identity, procedural topology-label blinding, separate protected topology mapping, per-seed integrity sidecars, whole-epoch manifest, and a future distinct one-file collection authorization commit. PR validation cannot satisfy the authorization predicate and does not execute the scientific 50-seed panel.

Current Track A boundary:

**`TRACK_A_PROTOCOL = PREREGISTERED`**  
**`TRACK_A_PRIMARY_ANALYSIS = LOCKED / NONEMPIRICAL`**  
**`TRACK_A_RUNNER = UNDER REVIEW / NOT AUTHORIZED`**  
**`TRACK_A_FREEZE = NOT ESTABLISHED`**  
**`TRACK_A_EMPIRICAL_EXECUTION = NOT AUTHORIZED`**

## B1 / B2 / B3 status

### B1 — semantic routing and safety

B1 implementation merged as `002f6c7037c7e72c31c39499cba97681da76a962` after 18/18 returned exact-head workflows passed. The source-bound profile exercises clean governance, ambiguous/mixed, adversarial, low-confidence fallback, and a live source-reachable P-10 forbidden fixture. The forbidden path was demonstrated without changing KAPPA/P-10/Sentinel thresholds.

Two current-source limitations remain explicit: the DemiJoule reprompt band is unreachable under its present common six-axis scoring implementation, and P-10 forbidden is reachable only in a narrow KAPPA-derived confidence region. PR #433 is the developer self-attested/non-independent 11Q qualification lane and deliberately deducts for these limitations.

### B2 — persistent context and closure

B2 implementation merged as `9e6971d5c8fc39e46acfe743e6588bbdc127abe8`. P-30/P-11 qualification merged as `a82c56894f1334279dd62adc2b858c924d5ba05f`: **108/110 (98.18%), S-TIER, Q11=9**, developer self-attested/non-independent. PR #428 is the non-empirical integration-readiness adjudication lane.

### B3 — persistent graph convergence

B3 implementation merged as `114312db125439ae861065e36d3b0d37ffe32d14`. P-30/P-11 qualification merged as `68c94a53718915ae909eb2196373283186a95138`: **108/110 (98.18%), S-TIER, Q11=9**, developer self-attested/non-independent. PR #430 is the non-empirical integration-readiness adjudication lane.

None of B1/B2/B3 establishes integrated Track C efficacy, independent verification, empirical authorization, or High-Assurance acceptance.

## Protected-main enforcement development

Live merge attempts on fully green PR #428 now demonstrate preventive merge enforcement that was not present in earlier #277 evidence: merge commits are rejected, and squash merge is blocked unless at least one approving review from a write-access reviewer is present and required `PPTL CI` is satisfied. Exact branch-protection/ruleset readback remains unavailable to the current integration (`403`), so complete configuration and direct-write prevention remain **NOT VERIFIED**.

This repository-administration development is a merge/governance constraint only. It does not establish a scientific gate.

## Current gate board

| Boundary | Status |
|---|---|
| Final v0.7.6 High-Assurance candidate | NOT DESIGNATED |
| P4 real security/blinding custody | OPEN / FAIL-CLOSED |
| P7 final scientific binding | OPEN |
| P8 immutable freeze | OPEN / FAIL-CLOSED |
| Final independent P9 | NOT EXECUTED / OPEN |
| High-Assurance freeze | NOT ESTABLISHED |
| High-Assurance authorization | NOT GRANTED |
| Canonical High-Assurance empirical N | 0 |
| Solo Epoch 004 | COMPLETED / LOCKED NEGATIVE EXACT-TREATMENT EVIDENCE |
| Seven-gate canonical treatment fidelity for Epoch 004 | NOT ESTABLISHED |
| Canonical DGAF efficacy | NOT ESTABLISHED |
| Track A structural matrix | CLOSED / NONEMPIRICAL |
| Track A protocol | PREREGISTERED |
| Track A primary analysis | LOCKED / NONEMPIRICAL |
| Track A runner | UNDER REVIEW / NOT AUTHORIZED |
| Track A freeze | NOT ESTABLISHED |
| Track A empirical execution | NOT AUTHORIZED |
| B1 | IMPLEMENTED / QUALIFICATION UNDER REVIEW |
| B2 | IMPLEMENTED + QUALIFIED / INTEGRATION ADJUDICATION UNDER REVIEW |
| B3 | IMPLEMENTED + QUALIFIED / INTEGRATION ADJUDICATION UNDER REVIEW |
| Integrated Track C | DEFERRED |

## Historical evidence boundary

Experiment 001 remains apparatus-falsification evidence because its intended treatment binding failed. Epoch 003 remains negative evidence for its explicitly synthetic treatment variant. Epoch 004 remains separate, locked evidence for its exact executed treatment. These epochs are not pooled or retroactively relabeled.

The historical runtime candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, consolidated control-state anchor `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`, and immutable P-35 boundary `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` remain valid only at their recorded scopes.

## Repository and documentation hygiene

Current-facing summaries must distinguish:

1. canonical High-Assurance state;
2. bounded Solo empirical evidence;
3. post-hoc fidelity findings that constrain claims without rewriting locked results;
4. prospective Track A/B/C work;
5. merged evidence from changes that are merely green or under review.

Older dated records remain historical evidence. A newer commit, documentation edit, CI success, diagnostic PASS, developer qualification, or Solo result does not itself designate the High-Assurance candidate, establish freeze, grant authorization, or increase canonical High-Assurance empirical N.

**Canonical High-Assurance state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**  
**Canonical DGAF efficacy: NOT ESTABLISHED.**
