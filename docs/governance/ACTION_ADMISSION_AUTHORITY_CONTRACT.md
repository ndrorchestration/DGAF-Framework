# Action Admission Authority Contract — Provider-Neutral Design Boundary

## Status

This document defines a **design-only, provider-neutral authority contract** for future Action Admission hardening. It does not admit a provider, durable store, revocation service, issuer, key-management system, credential, schema, environment binding, action class, or runtime authority.

The current accepted runtime remains bounded to `AAR_V1` for `AUDIT_COUNTER_UPDATE_V1`. Its replay memory is process-local, revocation is record-local, the trust anchor is a server-side HMAC environment secret, and no production issuer is established.

## Replay authority

The target guarantee is **at-most-once authorized effect** for a given admitted effect identity. Exactly-once is not established.

A future durable replay authority must implement an atomic `CONSUME_ONCE` operation over the **effect identity**, not merely over a caller-controlled record ID. Record identity and effect identity are distinct:

- **Record identity** supports duplicate-record detection and includes `record_id` together with the consequential AAR semantics.
- **Effect identity** is the replay-consume key for at-most-once protection and intentionally excludes `record_id`, so minting a fresh record ID cannot re-admit the same authorized consequential effect.

The canonical record identity fields are:

1. `version`
2. `record_id`
3. `action_class`
4. `target`
5. `policy_id`
6. `authorization.authorization_id`
7. `action_digest`

The canonical effect identity fields are:

1. `version`
2. `action_class`
3. `target`
4. `policy_id`
5. `authorization.authorization_id`
6. `action_digest`

The authority outcome vocabulary is `CONSUMED`, `REPLAY`, `UNAVAILABLE`, and `CONFLICTED`. Only `CONSUMED` permits progression. `REPLAY`, `UNAVAILABLE`, and `CONFLICTED` fail closed.

### Crash window

If replay consumption succeeds but the protected side effect does not complete, the system must not automatically retry the same admitted effect. The required state is `NO_AUTOMATIC_RETRY_MANUAL_RECOVERY_REQUIRED` until a separately governed recovery mechanism is established.

This contract intentionally does not claim cross-system exactly-once semantics. Exactly-once would require stronger transactional coupling, effect-ledger semantics, or an equivalent atomicity mechanism spanning replay consumption and the protected effect. No such mechanism is currently established.

## Revocation authority

A future authoritative revocation source must expose the commit-time states:

- `ACTIVE`
- `REVOKED`
- `UNAVAILABLE`
- `CONFLICTED`

Only `ACTIVE` permits progression. `REVOKED`, `UNAVAILABLE`, and `CONFLICTED` fail closed where authoritative revocation is required.

Revocation must be revalidated **immediately before replay consumption and the protected side effect**. The lookup must be bound to the authorization/AAR identity and applicable effective-time semantics rather than trusting only the record-local `revoked` field.

Revocation is prospective for future use. Historical execution and postcondition receipts remain immutable event-time provenance and are not retroactively rewritten when an authorization or trust anchor is later revoked.

## Issuer and trust-anchor lifecycle

Current `AAR_V1` is bounded and has no explicit issuer identity or key identity. Those fields must not be silently added while retaining the same semantic version.

A future record version, provisionally `AAR_V2`, is required before issuer ID and key ID become normative Action Admission fields. Its exact schema remains separately gated.

The provider-neutral trust-anchor lifecycle vocabulary is:

- `ACTIVE`
- `OVERLAP_VERIFY_ONLY`
- `RETIRED`
- `COMPROMISED`
- `UNAVAILABLE`
- `CONFLICTED`

Verification may succeed only for `ACTIVE` and `OVERLAP_VERIFY_ONLY` anchors. `RETIRED`, `COMPROMISED`, `UNAVAILABLE`, and `CONFLICTED` deny admission.

Issuance authority must remain separate from request-path verification. A request handler may verify a trusted record, but that verification capability does not itself grant minting authority. This specification does not choose a KMS, HSM, secret manager, database, queue, or hosting provider.

### Operation-specific trust interpretation — proposed AAR_V2 clarification

The proposed operation matrix is design-only: it does not extend \`AAR_V1\`,
grant issuance rights, enroll keys, select a provider, authorize a protected
action, or establish independent custody. Source-of-truth: the additive
\`issuer_and_trust_anchor.candidate_operation_semantics\` record in
\`registry/action_admission_authority_contract.json\`. This distinction
requires non-author security and methodology review before any runtime use.

| Proposed operation | Trust anchor states that may satisfy **only the key-state prerequisite** |
| --- | --- |
| \`VERIFY_HISTORICAL_SIGNATURE\` | \`ACTIVE\`, \`OVERLAP_VERIFY_ONLY\` |
| \`ISSUE_NEW_ATTESTATION\` | \`ACTIVE\` |
| \`ADMIT_NEW_PROTECTED_EFFECT\` | \`ACTIVE\` |

All other named states—\`RETIRED\`, \`COMPROMISED\`, \`UNAVAILABLE\`,
and \`CONFLICTED\`—fail the corresponding prerequisite. Even
\`VERIFY_HISTORICAL_SIGNATURE\` is allowed only if the key is sourced from
an **admitted external trust registry**, the applicable event-time and
compromise semantics are established, and the signed bytes verify. A
receipt- or request-supplied \`key_id\` is not self-admitting. A compromised
or retired key must not be silently restored to trusted historical status
by an old signature.

A successfully checked historical receipt **does not authorize a fresh
protected action**. New issuance also requires an independently authorized
issuer with custody separation; a verifier, user-facing agent, or receipt
holder has no minting authority merely because verification succeeds.
For a new protected effect, \`ACTIVE\` is **necessary but insufficient**:
typed input, fresh narrowly scoped authorization, commit-time revocation,
atomic consumption of the consequential effect identity, and a trusted
effect gate remain separately required. A correct signature is not a
verified postcondition, an effect receipt, or proof of non-dispatch.

\`OVERLAP_VERIFY_ONLY\` permits historical verification only within an
applicable approved overlap window; it is **not** permission to issue
or admit fresh effects. Historical event-time evidence remains immutable
on prospective revocation, while confidence in historical authenticity
may still need revision after actual key compromise. This design matrix
does not establish the overlap window, key-custody protocol, effective-time
proof, or revocation infrastructure.

### Historical proof-of-existence (candidate rule; not implemented)

A valid signature over a self-declared issued_at field does not independently
establish when that signature was created. A trusted timestamp applied only
to the unsigned receipt payload might establish earlier existence of the
payload, not the signature. To establish that specific signed evidence existed
no later than a witness time, a separately admitted time/proof authority
must attest the exact signature bytes and admitted signing-key identity,
with validated imprint, authority, temporal policy, key usage and
compromise/revocation history.

Even genuine evidence of this type supplies a latest possible signing time,
not proof of the exact signing instant, effect truth, or present authorization.

| Presented evidence | Permissible timing claim |
| --- | --- |
| Self-declared time plus valid signature | HISTORICAL_TIME_NOT_ESTABLISHED |
| Timestamp binding only unsigned payload | Signature existence time NOT_ESTABLISHED |
| Missing, untrusted, invalid or conflicting proof | HISTORICAL_TIME_NOT_ESTABLISHED |
| Trusted witness bound to exact signature and signer | Conditional SIGNATURE_EXISTED_NO_LATER_THAN_TRUSTED_WITNESS_TIME |

This proposed, non-authorizing clarification is controlled under issue #758
and uses the historical negative-control evidence in issue #1022.
RFC 3161 is relevant prior art, not evidence of a deployed DGAF timestamp
authority. No runtime, provider, key, issued AAR, or scientific/authorization
claim is created by this proposal.

## Commit ordering

The normative provider-neutral ordering is:

1. `STRUCTURAL_AND_ATTESTATION_VALIDATION`
2. `COMMIT_TIME_REVOCATION_REVALIDATION`
3. `ATOMIC_REPLAY_CONSUME`
4. `PROTECTED_SIDE_EFFECT`
5. `POSTCONDITION_AND_EXECUTION_RECEIPT`

The ordering prevents a side effect from preceding authoritative revocation and replay decisions. It does not erase the crash window between replay consumption and the protected side effect.

## Dependency-admission prerequisites

Any future implementation for replay, revocation, issuing, or key custody must pass the existing external-dependency admission contract before becoming runtime authority. Where applicable, that includes:

- owning project/program and accountable authority;
- provider resource identity;
- source dependency declaration and lock/custody evidence;
- environment-variable and deployment scope;
- credential class, least privilege, rotation ownership, and rollback/removal path;
- schema/migration custody and retention semantics when persistence is used;
- ACL/RLS/object-level authorization evidence when applicable;
- atomicity, consistency, concurrency, and failure-mode evidence required by the claimed guarantee;
- negative tests for unavailable, conflicted, replayed, revoked, stale-key, and unauthorized issuance conditions.

Provider availability, prior ecosystem use, hosting affinity, or a source comment is not dependency-admission evidence.

## Failure and recovery semantics

Missing, malformed, unavailable, conflicted, revoked, replayed, compromised, or otherwise non-admissible authority evidence must fail closed where that authority is required. Recovery from an ambiguous or partially committed operation requires an explicit recovery path and evidence; it must not be inferred from retries alone.

No component may upgrade `NOT ESTABLISHED` to an affirmative runtime property merely because this design contract exists.

## Non-effects

This specification is architecture/documentation only. It establishes no durable replay implementation, authoritative revocation implementation, production issuer, trust-anchor lifecycle implementation, action-class expansion, materialization authority, primary-analysis authority, efficacy result, independent validation, certification, or High-Assurance promotion.

The controlling scientific/governance boundary remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**. Primary analysis remains **NOT AUTHORIZED / NOT RUN**; canonical efficacy and independent validation remain **NOT ESTABLISHED**.

## Post-execution authority boundary

An execution receipt records what happened; it is evidence, not continuing authority. Every DGAF execution receipt therefore carries:

- `authority_effect: NONE`
- `follow_on_authority: FRESH_ADJUDICATION_REQUIRED`

A successful execution, verified postcondition, provider receipt, or closed transaction does not authorize a subsequent consequential action. Any follow-on action must enter a fresh admission/adjudication path with its own current evidence, policy identity, scope, authorization, commit-time revalidation, and replay controls.

Unknown, partial, failed, or inconclusive outcomes remain subject to reconciliation/recovery rules and likewise cannot be treated as inherited authority.
