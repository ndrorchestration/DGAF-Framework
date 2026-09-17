# Provider-Neutral External Runtime Adapter Design

**Status:** DESIGN ONLY / NOT RUNTIME AUTHORITY  
**Issue:** #773  
**Depends on:** #772 external-harness boundary  
**Scientific-state effect:** NONE  
**Authorization effect:** NONE

## Purpose

Define the smallest provider-neutral boundary through which an external agent runtime, development harness, workflow engine, or model/tool provider can submit candidate evidence and a requested transition to DGAF without acquiring governance authority.

The adapter is a translation and admission boundary, not a trust shortcut. External provider success, completion, approval, confidence, tool capability, or local authorization must never directly establish DGAF verification, authorization, admissibility, or empirical support.

## Core invariant

> An external system may describe what it observed, attempted, produced, or requests. DGAF alone determines how that information is classified and whether any DGAF transition is admissible.

The adapter therefore MUST NOT upgrade evidence class, verification class, authority class, action class, consequence class, reversibility, or freshness during translation.

## Scope

This design introduces one normalized ingress contract and one deterministic admission result.

In scope:

- external runtime/provider identity;
- event identity and effect identity as distinct concepts;
- normalized source identity;
- evidence envelope and provenance binding;
- requested DGAF transition/action class;
- externally asserted verification class as untrusted input metadata;
- authority presented as evidence to evaluate, not authority automatically accepted;
- consequence and reversibility metadata where required by the requested action class;
- deterministic accept/reject result with machine-readable reason codes;
- resulting DGAF record identity for accepted normalized records;
- replay/duplicate detection aligned with current Action Admission record-vs-effect semantics;
- fail-closed validation for malformed, missing, stale, unsupported, ambiguous, or authority-incompatible inputs.

Out of scope:

- named ECC, LangGraph, OpenAI Agents SDK, Microsoft Agent Framework, or other provider adapters;
- provider authentication implementations;
- durable external runtime stores;
- remote revocation services;
- granting new DGAF action classes;
- production runtime authority;
- changing Track A experimental state;
- changing canonical DGAF efficacy or independent-validation state;
- establishing exactly-once execution.

## Architectural boundary

```text
External runtime / harness
        |
        | provider-specific event
        v
Provider adapter (future)
        |
        | MUST only normalize; MUST NOT upgrade
        v
ExternalRuntimeEnvelope V1
        |
        v
Deterministic DGAF ingress validator
        |
        +--> REJECT + reason codes
        |
        v
NormalizedExternalRuntimeRecord
        |
        v
Existing DGAF evidence / authority / Action Admission machinery
        |
        v
DGAF-owned admissibility decision
```

Provider-specific adapters terminate at `ExternalRuntimeEnvelope V1`. No provider-specific semantics may leak across this boundary as implicit authority.

## ExternalRuntimeEnvelope V1

The canonical representation is a versioned JSON-compatible object with the following required top-level fields:

```json
{
  "schema_version": "DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1",
  "provider": {
    "provider_id": "string",
    "runtime_id": "string",
    "adapter_id": "string",
    "adapter_version": "string"
  },
  "identity": {
    "event_id": "string",
    "effect_id": "string",
    "source_id": "string"
  },
  "evidence": {
    "evidence_class": "string",
    "observed_at": "RFC3339 timestamp",
    "content_digest": "sha256:<hex>",
    "payload": {}
  },
  "provenance": {
    "producer_id": "string",
    "producer_run_id": "string",
    "source_bindings": []
  },
  "request": {
    "action_class": "string",
    "requested_transition": "string"
  },
  "assertions": {
    "verification_class": "string",
    "authority": {}
  },
  "risk": {
    "consequence_class": "string",
    "reversibility": "string"
  }
}
```

### Identity semantics

`event_id` identifies the submitted external event/record occurrence.

`effect_id` identifies the real-world or DGAF-relevant effect the request would cause or claims has occurred. Replay protection for `CONSUME_ONCE` semantics binds to `effect_id`, consistent with the existing Action Admission authority contract. Distinct event records that target the same effect do not become distinct admissible effects merely by changing `event_id`.

`source_id` is the normalized identity of the external source object or source state. It must not be inferred from a provider display name alone.

All identity fields are opaque identifiers after structural validation. Provider-name substitution must not cause two distinct providers, runtimes, effects, or sources to collapse into one identity.

## Trust classification

Every submitted envelope begins as:

`EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED`

The adapter may preserve an external assertion such as `verified`, `approved`, `successful`, or `authorized` only inside the `assertions` field. Such values are claims from the external system, not DGAF state.

The normalized record must retain both:

1. what the external system asserted; and
2. DGAF's independent classification of the submitted evidence and authority.

The two must never share a field whose meaning could be confused.

## Validation order

Validation is deterministic and fail-closed in this order:

1. schema version and required-field completeness;
2. structural type validation;
3. provider/runtime/adapter identity validation;
4. event/effect/source identity validation;
5. evidence digest and provenance binding validation;
6. freshness/staleness validation where the requested class requires it;
7. requested action/transition support validation;
8. authority compatibility validation;
9. consequence/reversibility completeness validation for consequential action classes;
10. replay/duplicate-effect validation;
11. normalized record construction.

A failure at any stage produces a rejection result. Validation must not guess missing values, coerce unsupported action classes, or downgrade a required field to optional because a provider does not supply it.

## Admission result

The validator returns exactly one of two result classes.

Accepted normalization:

```json
{
  "admitted": true,
  "result_version": "DGAF_EXTERNAL_RUNTIME_ADMISSION_V1",
  "record_id": "sha256:<canonical-record-digest>",
  "effect_id": "string",
  "trust_class": "EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED",
  "dgaf_evidence_class": "string",
  "dgaf_verification_class": "string",
  "authority_status": "PRESENTED_NOT_GRANTED",
  "requested_action_class": "string",
  "requested_transition": "string",
  "reason_codes": []
}
```

Rejected normalization:

```json
{
  "admitted": false,
  "result_version": "DGAF_EXTERNAL_RUNTIME_ADMISSION_V1",
  "record_id": null,
  "effect_id": "string-or-null",
  "trust_class": "EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED",
  "reason_codes": ["DGAF_EXT_*"],
  "failed_stage": "string"
}
```

`admitted: true` means only that the external submission was structurally and semantically admissible as a DGAF input record. It does NOT mean the requested action or transition is authorized.

## Minimum rejection taxonomy

The first implementation must define stable machine-readable rejection codes covering at least:

- `DGAF_EXT_SCHEMA_UNSUPPORTED`
- `DGAF_EXT_REQUIRED_FIELD_MISSING`
- `DGAF_EXT_IDENTITY_MALFORMED`
- `DGAF_EXT_SOURCE_IDENTITY_INVALID`
- `DGAF_EXT_EVIDENCE_DIGEST_MISMATCH`
- `DGAF_EXT_PROVENANCE_INVALID`
- `DGAF_EXT_EVIDENCE_STALE`
- `DGAF_EXT_ACTION_CLASS_UNSUPPORTED`
- `DGAF_EXT_TRANSITION_UNSUPPORTED`
- `DGAF_EXT_AUTHORITY_MISMATCH`
- `DGAF_EXT_RISK_METADATA_REQUIRED`
- `DGAF_EXT_DUPLICATE_EFFECT`
- `DGAF_EXT_PROVIDER_SUBSTITUTION`

The implementation may add narrower codes but must not collapse materially different failure causes into a generic success/failure boolean.

## Replay and duplicate semantics

This boundary inherits the current Action Admission distinction between record identity and effect identity.

- duplicate `event_id` + identical canonical envelope: deterministic duplicate record; no second effect admission;
- different `event_id` + same `effect_id` under `CONSUME_ONCE`: reject as duplicate effect;
- same provider display name with different normalized provider/runtime identity: must remain distinct;
- mutated envelope reusing an existing `event_id`: reject identity collision;
- exactly-once execution remains NOT ESTABLISHED.

## Authority semantics

`assertions.authority` is evidence presented for DGAF evaluation. It is never a grant by itself.

The ingress boundary must expose an `authority_status` that begins as `PRESENTED_NOT_GRANTED` unless an existing DGAF authority mechanism independently establishes a stronger state after ingress.

An external framework's local concepts such as approval, allowed tool, successful guardrail, role, permission, capability, or completion must not be mapped directly to a DGAF authorization state.

## Consequence and reversibility

The first implementation supports metadata capture, not a new consequence engine.

For action classes already classified by DGAF as consequential, missing consequence or reversibility metadata is a fail-closed rejection. For non-consequential evidence-only submissions, these fields may use an explicit `NOT_APPLICABLE` value if the schema permits it.

Unknown consequence or reversibility is not silently treated as low risk. Where required, `UNKNOWN` means no admissible consequential transition exists yet.

## Canonicalization and record identity

Accepted normalized records must use deterministic canonical JSON serialization consistent with existing DGAF content-addressed-record conventions where practical.

`record_id` is the SHA-256 digest of the canonical normalized record, excluding runtime-local transient values that are not part of semantic identity.

The exact canonicalization function and excluded fields must be fixed by the implementation and covered by deterministic tests before any provider-specific adapter exists.

## Testing requirements

The first implementation is test-first and must include positive and negative fixtures.

Required negative cases:

1. missing required field;
2. malformed event/effect/source identity;
3. evidence digest mismatch;
4. invalid or missing provenance binding;
5. stale evidence where freshness is required;
6. unsupported action class;
7. unsupported transition;
8. authority mismatch;
9. missing consequence/reversibility metadata for consequential action;
10. same effect submitted under a different event identity;
11. provider-name substitution / provider identity confusion;
12. same event identity with mutated content;
13. external `verified=true` or equivalent assertion attempting to upgrade DGAF verification;
14. external `authorized=true` or equivalent assertion attempting to grant DGAF authority.

Required positive cases:

1. deterministic normalization of the same valid envelope;
2. stable record identity for byte-different but semantically identical canonical input where normalization permits;
3. preservation of external assertions as untrusted metadata;
4. explicit `PRESENTED_NOT_GRANTED` authority state after ingress;
5. successful admission of evidence-only input without authorizing its requested transition.

## Initial implementation surface

The intended first implementation should remain small:

- one schema/contract artifact under `registry/` or the repository's established machine-readable governance-contract location;
- one focused Python validator/canonicalizer module following existing DGAF validation patterns;
- one focused test module with fixture builders and required negative controls;
- this design document plus concise governance documentation linking the boundary to the existing Action Admission authority contract.

Do not add named-provider packages, network calls, external SDK dependencies, durable storage, or runtime execution code in this tranche.

## Acceptance criteria

The design is implemented only when all of the following are true:

- a versioned provider-neutral envelope exists;
- canonicalization and record identity are deterministic;
- event identity and effect identity remain separate;
- external verification/authorization assertions cannot promote DGAF state;
- malformed, stale, unsupported, ambiguous, replayed, and authority-incompatible inputs fail closed;
- rejection reasons are machine-readable;
- tests cover the required negative and positive cases;
- no named provider is treated as trusted by default;
- exactly-once remains NOT ESTABLISHED;
- all existing DGAF governance, truth-layer, regression, quality, and pre-freeze checks remain green;
- PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 and all current Track A boundaries remain unchanged.

## Non-effects

Acceptance of this specification or its future validator does not establish:

- external-provider compatibility;
- external-provider trust;
- runtime authority;
- a durable authority store;
- execution authorization;
- exactly-once execution;
- empirical efficacy;
- independent validation;
- production certification;
- Track A materialization or primary-analysis authorization;
- High-Assurance promotion.
