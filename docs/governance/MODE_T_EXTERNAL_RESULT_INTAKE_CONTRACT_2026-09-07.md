# Mode-T External Result Intake Contract — 2026-09-07

## Status

Status: SOURCE-BOUND INTAKE CONTRACT / EXTERNAL SUBMISSIONS UNVERIFIED / NOT GOVERNANCE ADJUDICATION / NOT AUTHORIZATION

This contract complements the source-bound external-acceptance handoff merged by PR #343. The handoff defines what external parties must produce. This contract defines how the repository may preserve a returned external record without converting that record into a locally verified or governance-accepted result.

The canonical blank envelope is `docs/governance/mode_t_external_result_intake_template.json`. The validator is `scripts/validate_mode_t_external_result_intake.py`.

## Purpose

External Mode-T work crosses trust domains. A review report, retained authority record, Confidential Space run record, or protected-continuity adjudication may be produced outside this repository. Copying such a result into repository prose without a closed intake contract creates avoidable ambiguity about:

- which #343 handoff and reviewed source set the result addresses;
- which exact external obligation from that handoff the submission claims to address;
- who claims to have produced it and what evidence supports that attribution;
- what basis is claimed for reviewer or producer independence;
- whether the result concerns Stage-A apparatus qualification, Stage-B final-candidate acceptance, or another track-specific external step;
- which external record and evidence artifacts were supplied;
- which claims the external party reported as PASS, FAIL, BLOCKED, CONDITIONAL, or UNKNOWN;
- whether the repository has independently retrieved or cryptographically reverified those artifacts;
- whether any separate governance adjudication has occurred.

The intake envelope preserves those distinctions.

## Two allowed record states

### `TEMPLATE`

The checked-in canonical envelope is inert:

- track identity and required output are null;
- producer identity and independence basis are null;
- attribution-evidence references are empty;
- submission identity is null;
- execution state is `NOT_EXECUTED` and execution phase is null;
- external disposition is `UNKNOWN`;
- claims and evidence artifacts are empty;
- all ingestion/adjudication fields remain negative.

A template is not evidence.

### `EXTERNAL_SUBMISSION_UNVERIFIED`

A filled intake envelope may preserve an externally reported result only when it records:

- one exact handoff track: Issue #295, #310, #316, or #320 and its canonical track name;
- the exact `required_output` text carried by that track in the immutable #343 handoff manifest;
- producer name and external identifier;
- at least one producer-attribution evidence reference that resolves to an evidence artifact in the same envelope;
- whether the producer claims independence, without treating that claim as verified;
- a non-empty `independence_basis` whenever independence is claimed;
- second-precision UTC submission time;
- an external record URI and SHA-256 digest;
- execution state `EXECUTED`;
- an execution phase from the closed phase vocabulary;
- at least one structured claim;
- at least one evidence artifact with URI, SHA-256, media type, and description;
- claim-to-artifact references that resolve within the envelope.

The external party may report an external disposition of `PASS`, `FAIL`, `BLOCKED`, `CONDITIONAL`, or `UNKNOWN`. This value is preserved as an external report only.

## Required-output binding

A filled envelope does not invent or paraphrase its obligation. The repository validator resolves the selected issue/track inside the immutable #343 handoff manifest and requires the intake's `required_output` to equal that source value exactly.

This check prevents evidence for one obligation from being structurally filed as another obligation. It does **not** establish that the submitted claims or artifacts are sufficient to satisfy the required output. Sufficiency remains an external-review/reverification/governance-adjudication question downstream of intake.

## Execution-phase binding

The closed execution-phase vocabulary is:

- `STAGE_A_APPARATUS_QUALIFICATION` — pre-candidate apparatus qualification or acceptance work whose result does not designate the final candidate;
- `STAGE_B_FINAL_CANDIDATE_ACCEPTANCE` — later acceptance work explicitly bound to a separately designated final candidate;
- `TRACK_SPECIFIC` — an external track whose semantics do not require the Stage-A/Stage-B distinction.

Issue #310 (`real_confidential_space_admission`) must use either `STAGE_A_APPARATUS_QUALIFICATION` or `STAGE_B_FINAL_CANDIDATE_ACCEPTANCE`; `TRACK_SPECIFIC` is rejected for that track. This prevents real Confidential Space apparatus qualification from being silently conflated with final candidate-bound P4 acceptance.

Recording Stage B in an intake envelope does not prove that a final candidate actually exists. The envelope's fixed scientific state remains `NOT_DESIGNATED`, so Stage-B material cannot be promoted until a separate governance transition under Issue #309 has established the relevant candidate and downstream adjudication has independently accepted the evidence.

## Immutable handoff binding

Every envelope binds to:

- handoff merge `8928a83e93cf9a53f0aeee89a05d57e37b3cc9c2`;
- handoff tree `442fc81d30c311c6e2cd2f89db5276465982e1c5`;
- handoff manifest blob `988f76aeb7313e6c4d149948c0450b682c82e0e1`;
- review base `62e01c37e6e452e0851aa875fa6c709f049be991`;
- review-base tree `f5ac41ccddc785f3e3e52a3c91daeb4513bccc20`.

Repository validation confirms the declared handoff merge/tree, manifest blob, review base, selected track identity, and exact required-output binding. For an external submission, the selected track must originate from the handoff manifest's `NOT_EXECUTED` state.

## Deliberate non-promotion boundary

The intake validator does **not** establish any of the following, even when an external party reports `PASS`:

- producer independence;
- producer attribution authenticity;
- retrieval of referenced artifacts;
- cryptographic authenticity of referenced artifacts;
- independent reverification;
- governance adjudication;
- P4 completion;
- final-candidate designation;
- immutable freeze;
- authorization;
- final P9 completion;
- empirical execution or any increase in N.

Accordingly, every valid intake envelope must retain:

- `attribution_verified=false`;
- `artifacts_retrieved=false`;
- `cryptographic_reverification_status=NOT_EXECUTED`;
- `governance_adjudication_status=NOT_EXECUTED`;
- final candidate `NOT_DESIGNATED`;
- P4 `OPEN_FAIL_CLOSED`;
- P8 `OPEN_FAIL_CLOSED`;
- final P9 `NOT_EXECUTED`;
- freeze `NOT_ESTABLISHED`;
- authorization `NOT_GRANTED`;
- empirical N `0`.

Those later trust transitions require separate evidence and separate governance action. They must not be encoded by editing the intake envelope.

## Track mapping

| Issue | Canonical intake track | External work represented |
| --- | --- | --- |
| #320 | `independent_oidc_security_review` | Independently attributable OIDC/Confidential Space security review |
| #316 | `production_rac_retention_and_authority` | Independently retained production R/A/C, policy, signer, and trust-root authority |
| #310 | `real_confidential_space_admission` | Real Confidential Space admission evidence and independent retrieval/reverification inputs |
| #295 | `protected_continuity_acceptance` | Protected continuity packet, independent retention/re-hash inputs, and external adjudication inputs |

## Evidence-reference rules

Each evidence artifact has a unique `artifact_id`. Each structured claim references zero or more artifact IDs from the same envelope. Producer `attribution_evidence_refs` also reference artifact IDs from that same closed evidence set. Unknown claim or attribution references fail validation.

Artifact SHA-256 values and the external source-record SHA-256 must be lowercase 64-character hexadecimal digests. Digest syntax validation is not artifact retrieval or cryptographic reverification. The intake contract intentionally keeps those later states negative.

## Machine validation

The workflow `Mode T External Result Intake` runs the deterministic tests and validates the checked-in inert template against the repository object graph.

A validator PASS means only:

**the intake contract is structurally closed, source-bound to the #343 handoff, obligation-bound to the selected track, and incapable of promoting its own external report into DGAF acceptance state.**

## Current control boundary

Issue #277 preventive enforcement remains **NOT ESTABLISHED**. Issues #295, #310, #316, and #320 remain external acceptance work. Issue #309 remains the final-candidate designation authority after candidate-relevant P4 decisions are fixed.

**Final v0.7.6 candidate NOT DESIGNATED · P4 OPEN / FAIL-CLOSED · P7 final binding OPEN · P8 OPEN / FAIL-CLOSED · final P9 NOT EXECUTED · PRE-FREEZE · NOT AUTHORIZED · empirical N=0.**
