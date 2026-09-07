---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-07
live_source_boundary: 972edd41f16c69c6912af08c7d6c3aa627fdd8a9
live_source_boundary_role: V0_7_6_APPARATUS_INTRODUCTION_BOUNDARY_NOT_CURRENT_HEAD
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
historical_runtime_evidence_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
historical_runtime_evidence_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
historical_runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
final_candidate_status: NOT_DESIGNATED
final_candidate_tracker: 309
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
solo_experiment_001_status: APPARATUS_FALSIFICATION_EVIDENCE
solo_p30_diagnostic_epoch_002_status: PASS_NON_EMPIRICAL_SCIENTIFIC_N_INCREMENT_0
solo_fresh_empirical_epoch_status: NOT_AUTHORIZED
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded. Evidence is scoped to the exact identities and predicates that produced it. A successful CI, deployment, synthetic, custody-mechanism, documentation check, or engineering diagnostic is not empirical efficacy evidence.

## Candidate-authority reconciliation — 2026-09-06

Merged PR #308 advanced the experimental apparatus to protocol v0.7.6 / artifact schema 1.1 at source boundary `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`. The earlier runtime candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` retain valid exact-scope engineering/governance evidence, but Issue #309 now classifies them as historical provenance rather than the final freeze/N=1 apparatus.

**Final v0.7.6 candidate: NOT DESIGNATED.** Issue #309 is the active reconstruction/evidence-regeneration authority. Neither current `main`, an active PR head, a deployment, nor a documentation checkpoint becomes the final candidate merely by being newer. The consolidated control-state anchor `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` remains the canonical control/provenance anchor for its scope and is not itself a candidate designation.

## Separate Solo-track reconciliation — 2026-09-07

The bounded Solo track is distinct from the canonical High-Assurance PDMAL candidate/freeze sequence above.

- Solo final experiment 001 executed 50 seeds / 9,000 observations.
- All 2,250 DGAF-condition cells failed closed before the intended DGAF consensus treatment behavior could be tested because the PDMAL adapter did not populate the required P-30 Apogee confidence substrate. The default `confidence=0.0` produced grade `D`, which maps to `KILL` under the designated P-30 contract.
- Experiment 001 is therefore retained as **apparatus-falsification evidence**, not positive or negative DGAF efficacy evidence. It is not eligible for deletion, repair-in-place, positive relabeling, or pooling with a later empirical epoch.
- PR #366 preregistered and executed the separate `SOLO-P30-DIAGNOSTIC-EPOCH-002` non-empirical engineering diagnostic using the fixed synthetic minimum-passing P-30 fixture `SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1` at exactly `0.45` confidence.
- The diagnostic completed 90/90 trials successfully with 0 attempt failures and no aggregate gate failures. Scientific empirical N increment remained `0`.
- PR #367 retained the diagnostic adjudication and exact run/artifact provenance in-repository.
- The synthetic `0.45` fixture is not a real, observed, estimated, or calibrated Apogee confidence and cannot support an efficacy claim.
- The diagnostic PASS permits only consideration of a separately preregistered fresh blinded Solo proposal. **No fresh empirical Solo epoch is currently authorized.**

This Solo-track evidence does not designate the canonical v0.7.6 High-Assurance candidate, close P4/P7/P8/P9, establish freeze, grant canonical authorization, or change canonical High-Assurance empirical N from `0`.

## Identity boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`.
- Candidate identity status: final v0.7.6 candidate is **NOT DESIGNATED**; Issue #309 controls designation.
- Historical runtime-evidence candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.
- Historical runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`.
- Deployment identity: historical evidence deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is exact-bound to `7c1cc4bb…` at its recorded scope.
- v0.7.6 apparatus-introduction boundary: `972edd41f16c69c6912af08c7d6c3aa627fdd8a9` (legacy `live_source_boundary` metadata name; not current `main`).

Later documentation/evaluator/control-plane descendants do not automatically become the final candidate or inherit historical runtime evidence.

## Current gate board

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Historical P1 candidate integrity | CLOSED / VERIFIED | apparatus, `7c1cc4bb…` candidate/tree, and scoped deployment identity; final-candidate transfer/reverification pending #309 |
| Historical P2 runtime | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` five-case runtime predicates; final-candidate transfer/reverification pending #309 |
| Historical P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; candidate-bound structural/matrix/integrity evidence; final-candidate transfer/reverification pending #309 |
| P4 security/blinding | OPEN / FAIL-CLOSED | Mode-T engineering mechanisms integrated by #326; no real admissible H/I/T custody mode independently accepted/executed |
| Historical P5 provenance/reproducibility | CLOSED / VERIFIED | pre-v0.7.6 analysis/config/runner/schema identities and deterministic provenance/reproducibility evidence; final-candidate transfer/reverification pending #309 |
| Historical P6 evidence custody | CLOSED / VERIFIED | defined archive → retrieval → SHA-256 equality contract; final-candidate rebind decision pending #309 |
| Historical P6a CORS | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` four-case CORS predicates; final-candidate transfer/reverification pending #309 |
| Final v0.7.6 candidate | NOT DESIGNATED | Issue #309 |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | final exact scientific/pre-freeze identity chain incomplete |
| P8 analysis lock / freeze readiness | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 independent verification | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance decision |
| Canonical High-Assurance empirical N | 0 | no authorized canonical pilot execution |
| Solo experiment 001 | APPARATUS-FALSIFICATION EVIDENCE | separate bounded Solo track; not efficacy evidence and not pooled |
| Solo P-30 diagnostic epoch 002 | PASS / NON-EMPIRICAL | 90/90 diagnostic trials; scientific N increment 0; fresh empirical epoch not authorized |

## P4 custody boundary

PR #286 merged as `a3bafa6f…` and corrected the P4 architecture from a mandatory second-human requirement to effective control separation. Admissible modes are:

- `H`: genuinely distinct human Key Custodian;
- `I`: institutional/third-party custody outside the analyst’s unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

PR #326 integrated the validated Mode-T engineering mechanism stack, but no real custody/admission mode has been independently accepted and executed. P4 remains OPEN / FAIL-CLOSED operationally; #316, #320, signer/TrustedRoot/retention, and real Confidential Space admission/reverification remain open.

Issue #285 is completed as the governance-architecture correction and Issue #287 is the historical Mode-T design/threat-model lane. PR #326 later integrated the validated Mode-T engineering stack. That integration is mechanism-level engineering evidence only; it does not establish real P4 custody. Current external/independent blockers include #316, #320, final signer authority, production TrustedRoot/TUF approval/freeze, durable retention/retrieval, and real Confidential Space admission with independently reverified PRE/POST evidence.

## Current P5 closure basis

P5 is CLOSED / VERIFIED for provenance and reproducibility only at the historical `7c1cc4bb…` / protocol 0.7.5 boundary. The analysis-control identities are bound in the canonical historical control record, including the analysis implementation/configuration, runner, schema, protocol, deterministic environment, RNG separation, and topology-determinism evidence. This closure does not establish model/scientific efficacy and does not silently become v0.7.6 final-candidate evidence.

## Runtime evidence retrieval

On 2026-09-05, the P2 and P6a GitHub Actions records were freshly resolved:

- P2 run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

Both artifacts were unexpired and candidate-bound at retrieval. This is retrieval, not re-execution, and does not extend closure beyond the exact runtime predicates or into the future v0.7.6 final candidate.

## Evaluation-integrity update

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` and hardened Issue #32 Task 4 (`audit_hallucination_rate`). The evaluator fails closed without provenance-controlled ground truth plus independently generated outputs and uses deterministic six-field comparison.

No Task-4 performance result exists yet. The fixture/output corpus remains a separate evidence requirement.

## Engineering quality and repository enforcement

Issue #270 is **CLOSED / COMPLETED**. Its remediation established a clean current-lineage flake8/Black/isort/mypy baseline and converted those checks to fail-closed workflow gates, with deterministic negative controls demonstrating rejection of intentional violations.

Issue #277 remains **OPEN** for a different layer: branch-protection/ruleset enforcement. Current protected `main` requires only `PPTL CI`; broader intended merge-critical checks are not yet proven repository-required. Therefore:

- workflow quality behavior: VERIFIED / FAIL-CLOSED when executed;
- broader repository merge enforcement: NOT ESTABLISHED / tracked by #277.

Historical Issue #47 remains a valid exact-tree closure for its own prior execution boundary.

PR #279 merged exact head `1373672b8db03d95d714737c1769d91f2998c164` as `c9765741cf8c3908bf35f81f46fe9a6ab681cd4e` and replaced self-staling “current main” wording in Issue #270 documentation with immutable technical-hardening-boundary language. It did not alter scientific, candidate, freeze, authorization, or empirical state.

## Mathematical hygiene boundary

Current PDMAL mathematical authority keeps the plastic constant and DGAF Platinum Mean separate:

- plastic constant `ρ ≈ 1.3247179572447454`, real root of `x³=x+1`;
- DGAF-specific `pP = 1/(2 sin(π/11)) ≈ 1.774732842`.

For the dodecahedral graph, the corrected exact Cheeger constant is `0.6`. Unweighted Forman–Ricci curvature is `-2` on every edge and therefore has zero discriminating signal on the current unweighted topology. These are engineering/formalization facts, not empirical PDMAL efficacy evidence.

## Remaining substantive closure work

Canonical High-Assurance sequence:

`complete candidate-relevant P4 apparatus work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent evidence → verified real P4-A custody mode → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

Separate Solo sequence:

`retain experiment 001 as apparatus-falsification evidence → retain epoch 002 engineering diagnostic → preregister an exact real P-30 treatment binding for a new epoch → rerun exact-candidate apparatus checks → separate authorization decision → only then consider fresh blinded empirical execution`

Issue #232 remains the canonical PDMAL completion-control record. Issue #287 is historical Mode-T design/threat-model provenance; PR #326 is the later bounded mechanism-integration boundary. Neither constitutes real custody acceptance. No current-facing documentation, Solo diagnostic, or CI success changes canonical High-Assurance empirical N or self-authorizes a new experiment.

**Canonical High-Assurance experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**  
**Separate Solo state: experiment 001 retained as apparatus-falsification evidence; P-30 diagnostic PASS / non-empirical; fresh empirical epoch NOT AUTHORIZED.**
