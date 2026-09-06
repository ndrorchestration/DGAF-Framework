---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-06
live_source_boundary: 972edd41f16c69c6912af08c7d6c3aa627fdd8a9
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
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded. Evidence is scoped to the exact identities and predicates that produced it. A successful CI, deployment, synthetic, custody-mechanism, or documentation check is not empirical efficacy evidence.

## Candidate-authority reconciliation — 2026-09-06

Merged PR #308 advanced the experimental apparatus to protocol v0.7.6 / artifact schema 1.1 at source boundary `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`. The earlier runtime candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` retain valid exact-scope engineering/governance evidence, but Issue #309 now classifies them as historical provenance rather than the final freeze/N=1 apparatus.

**Final v0.7.6 candidate: NOT DESIGNATED.** Issue #309 is the active reconstruction/evidence-regeneration authority. Neither current `main`, an active PR head, a deployment, nor a documentation checkpoint becomes the final candidate merely by being newer. The consolidated control-state anchor `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` remains the canonical control/provenance anchor for its scope and is not itself a candidate designation.

## Identity boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`.
- Historical runtime-evidence candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.
- Historical runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`.
- Historical candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.
- Live v0.7.6 source boundary: `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`.
- Final v0.7.6 candidate: **NOT DESIGNATED**, tracked by Issue #309.

Later documentation/evaluator/control-plane descendants do not automatically become the final candidate or inherit historical runtime evidence.

## Current gate board

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Historical P1 candidate integrity | CLOSED / VERIFIED | apparatus, `7c1cc4bb…` candidate/tree, and scoped deployment identity; final-candidate transfer/reverification pending #309 |
| Historical P2 runtime | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` five-case runtime predicates; final-candidate transfer/reverification pending #309 |
| Historical P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; candidate-bound structural/matrix/integrity evidence; final-candidate transfer/reverification pending #309 |
| P4 security/blinding | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | H/I/T custody architecture defined; no real custody mode instantiated or verified |
| Historical P5 provenance/reproducibility | CLOSED / VERIFIED | pre-v0.7.6 analysis/config/runner/schema identities and deterministic provenance/reproducibility evidence; final-candidate transfer/reverification pending #309 |
| Historical P6 evidence custody | CLOSED / VERIFIED | defined archive → retrieval → SHA-256 equality contract; final-candidate rebind decision pending #309 |
| Historical P6a CORS | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` four-case CORS predicates; final-candidate transfer/reverification pending #309 |
| Final v0.7.6 candidate | NOT DESIGNATED | Issue #309 |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | final exact scientific/pre-freeze identity chain incomplete |
| P8 analysis lock / freeze readiness | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 independent verification | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no authorized pilot execution |

## P4 custody boundary

PR #286 merged as `a3bafa6f…` and corrected the P4 architecture from a mandatory second-human requirement to effective control separation. Admissible modes are:

- `H`: genuinely distinct human Key Custodian;
- `I`: institutional/third-party custody outside the analyst’s unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No real mode has been instantiated. P4 therefore remains OPEN / NOT EXECUTED.

Issue #285 is completed as the governance-architecture correction. Issue #255 is superseded historical context. Issue #287 is the active design/threat-model lane for a possible zero-human Mode T implementation. Its existence does not establish that GitHub Actions, drand/timelock, or any other proposed mechanism satisfies P4.

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

`complete candidate-relevant P4 apparatus work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent evidence → verified real P4-A custody mode → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

Issue #232 remains the PDMAL completion-control record. Issue #287 is the active solo Mode-T design lane. No current-facing documentation or CI success changes empirical N or self-authorizes the experiment.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
