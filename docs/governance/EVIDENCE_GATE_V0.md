# Evidence Gate v0 — Extraction and Admission Specification

Controller: #1170

## Status

SPECIFICATION ONLY. This document does not establish evidence acceptance for any concrete artifact, authorize any downstream action, change Track A/PDMAL scientific state, or replace existing domain-specific validators.

## Purpose

Extract the smallest reusable evidence-admission contract already latent in DGAF's evidence/provenance controls.

Core abstraction:

```text
evidence object + target identity + provenance + declared claim scope
    -> admission decision + evidence receipt + explicit claim ceiling
```

The reusable core must not depend on Track A epoch state, dataset-lock transitions, unblinding, primary-analysis authority, scientific N, canonical DGAF efficacy, or High-Assurance status.

## Records

### EvidenceObject

Required:

- `evidence_id`
- `evidence_type`
- `digest_algorithm`
- `content_digest`
- `source_class`

Optional:

- `produced_at`
- `observed_at`
- retained reference/location metadata

### EvidenceTarget

Required:

- `target_type`
- `target_id`
- `scope_id`

Optional exact identities:

- source revision / commit
- tree
- build/run
- environment
- configuration

### ProvenanceBinding

Required:

- producer/execution class
- custody/retention class

Optional when known or required by an adapter:

- source identity
- runtime identity
- environment identity
- receipt identity
- manifest identity
- provider/workflow/artifact identity

Identifiers that did not exist must remain absent. The core must never fabricate or infer them solely to satisfy a schema.

### ClaimScope

Required:

- claim ID or claim class
- exact supported scope
- evidence class
- limitations
- non-transfer constraints
- excluded/promoted claims

### AdmissionReceipt

Required:

- admitted boolean
- stable reason code
- evidence ID
- target identity/scope
- verified digest
- performed-check flags
- provenance class
- admitted claim scope
- explicit claim ceiling
- schema version
- `authorization_effect = NONE`

## Stable reason codes

Initial v0 set:

- `EVIDENCE_MISSING_OR_INVALID`
- `DIGEST_MISMATCH`
- `TARGET_IDENTITY_MISMATCH`
- `SOURCE_IDENTITY_MISMATCH`
- `ENVIRONMENT_IDENTITY_MISMATCH`
- `PROVENANCE_CLASS_MISMATCH`
- `RECEIPT_MISMATCH`
- `MANIFEST_MISMATCH`
- `CONTENT_SET_MISMATCH`
- `CUSTODY_REQUIREMENT_UNSATISFIED`
- `CLAIM_SCOPE_MISSING`
- `CLAIM_SCOPE_EXCEEDS_EVIDENCE`
- `HISTORICAL_TRANSFER_NOT_ESTABLISHED`
- `REQUIRED_CHECK_UNAVAILABLE`
- `ADMITTED`

Human-readable detail may be emitted separately; downstream logic should not depend on free-text messages.

## Evaluation order

1. validate record shapes;
2. require concrete evidence bytes/reference when byte verification is part of the contract;
3. verify the content digest;
4. verify target identity and scope;
5. verify configured source/environment identities;
6. verify provenance-class-specific requirements;
7. verify configured receipt/manifest/content-set/custody requirements;
8. compare requested claim scope with admitted evidence class and limitations;
9. enforce historical/non-transfer constraints;
10. emit a non-authorizing receipt with a machine-readable claim ceiling.

The performed-check set is observable contract state. A check not performed must not be represented as successful.

## Fail-closed semantics

- Schema-only validation is never evidence acceptance.
- A digest string is not byte verification when the contract requires retained bytes.
- Known exact identities must match exactly.
- Missing identifiers that never existed remain absent instead of being invented.
- Required checker errors or unavailable required evidence deny admission.
- Historical evidence cannot silently transfer to a changed target.
- A requested claim that exceeds evidence scope/class is denied or ceiling-bounded.
- Evidence admission cannot execute, authorize, enqueue, unlock, deploy, release, analyze, unblind, or otherwise trigger downstream state.

## What admission establishes

An admitted receipt means only:

> The supplied evidence satisfied the declared Evidence Gate v0 contract for the exact recorded target, provenance class, and claim scope.

It does not establish:

- downstream authorization;
- dataset lock or another lifecycle transition;
- deployment/release approval;
- analysis authority;
- independent validation;
- efficacy;
- production readiness;
- security or safety certification;
- legal/regulatory compliance;
- system-wide safety or reliability.

## DGAF adapter requirements

Existing DGAF validators remain authoritative for domain-specific requirements. In particular, Track A operator evidence may require:

- protocol/epoch identities;
- exact archive member allowlists;
- public/protected archive structure;
- custody certificate bindings;
- outcome-inspection prohibitions;
- dataset-lock handoff constraints;
- scientific/non-authorizing boundary fields.

A DGAF adapter may map already-validated facts into the generic core, but Evidence Gate must not replace or weaken those checks.

## Second-consumer portability gate

Do not call the contract reusable until one materially different evidence source:

1. uses the same core schema;
2. uses the same reason codes;
3. passes the same digest/identity/claim-scope rules;
4. does not fork the core contract.

Preferred initial second consumers:

- exact GitHub PR-head CI evidence; or
- a generic local test artifact bound to source revision and runtime/toolchain.

## Minimum conformance cases

- valid exact evidence admits;
- missing evidence denies;
- digest mismatch denies;
- target mismatch denies;
- source identity mismatch denies;
- environment identity mismatch denies when required;
- provenance-class mismatch denies;
- schema-only mode cannot claim admission;
- required receipt mismatch denies;
- required manifest mismatch denies;
- overbroad claim scope denies;
- historical evidence transfer to changed target denies unless explicitly rebound;
- admitted receipt has `authorization_effect = NONE`;
- performed-check flags match actual evaluation.

## Packaging decision

Keep Evidence Gate inside DGAF for the initial extraction and portability experiment. A standalone package or repository is deferred until real outside use demonstrates an independent versioning or dependency boundary.

## Evidence boundary

Current DGAF source demonstrates bounded project-local evidence admission, content addressing, provenance binding, claim-scope discipline, and historical non-transfer controls. This specification does not establish general-purpose correctness, external-runtime portability, independent validation, product-market fit, production security, compliance, or certification.
