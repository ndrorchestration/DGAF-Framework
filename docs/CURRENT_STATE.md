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

**Final v0.7.6 candidate: NOT DESIGNATED.** Issue #309 is the active reconstruction/evidence-regeneration authority. Neither current `main`, an active PR head, a deployment, nor a documentation checkpoint becomes the final candidate merely by being newer.

The consolidated control-state anchor `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` remains the canonical control/provenance anchor for its scope and is not itself a candidate designation.

## Identity boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`.
- Historical runtime-evidence candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` / tree `586c00d6dedb589e52108279f9759be3c4f927e1`.
- Historical candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.
- Live v0.7.6 source boundary: `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`.
- Final candidate: **NOT DESIGNATED**, tracked by Issue #309.

## Current gate board

| Boundary | Status | Scope |
|---|---|---|
| Historical P1/P2/P3/P5/P6/P6a evidence | CLOSED / VERIFIED AT RECORDED `7c1cc4bb…` SCOPE | remains valid provenance; transfer/reverification classification pending #309 |
| Final v0.7.6 candidate | NOT DESIGNATED | exact immutable SHA/tree must be selected explicitly under #309 |
| P4 security/blinding | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | H/I/T custody architecture defined; no real custody mode instantiated or verified |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | final exact scientific/pre-freeze identity chain incomplete |
| P8 analysis lock / freeze readiness | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 independent verification | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no authorized pilot execution |

## Historical exact-scope evidence

The following remain valid for their exact `7c1cc4bb…` evidence boundary and are not erased by the v0.7.6 correction:

- P2 run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.
- P3/P5 candidate-bound structural/provenance evidence including run `33939955138`.
- P6 byte-retention/retrieval evidence within its recorded archive/hash scope.

Issue #309 governs whether each historical record is transferable by construct, historical only, requires source/structure reverification, requires runtime/deployment reverification, requires re-archive/rebind, or is not yet executable. No evidence transfers solely because test logic appears unchanged.

## P4 custody boundary

PR #286 corrected the P4 architecture from a mandatory second-human requirement to effective control separation. Admissible modes are:

- `H`: genuinely distinct human Key Custodian;
- `I`: institutional/third-party custody outside the analyst’s unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No real mode has been instantiated. P4 therefore remains OPEN / NOT EXECUTED. Current Mode-T work, including green draft CI, is mechanism/synthetic evidence only and does not establish real Confidential Space admission or P4 custody.

## Engineering quality and repository enforcement

Issue #270 is **CLOSED / COMPLETED**. Its remediation established a clean current-lineage flake8/Black/isort/mypy baseline and converted those checks to fail-closed workflow gates.

Issue #277 remains **OPEN** for repository merge enforcement. Current protected `main` requires only `PPTL CI`; broader quality/security checks are not yet proven repository-required before merge.

PR #279 merged exact head `1373672b8db03d95d714737c1769d91f2998c164` as `c9765741cf8c3908bf35f81f46fe9a6ab681cd4e` and replaced self-staling “current main” wording in Issue #270 documentation with immutable technical-hardening-boundary language. It did not alter scientific, candidate, freeze, authorization, or empirical state.

## Remaining substantive closure work

`complete candidate-relevant P4 apparatus work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent evidence → close real P4-A custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

Issue #232 remains the canonical completion-control record. No current-facing documentation, draft CI success, or source advancement changes empirical N or self-authorizes the experiment.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
