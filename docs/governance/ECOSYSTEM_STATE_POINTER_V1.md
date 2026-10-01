# ECOSYSTEM_STATE_POINTER_V1

## Purpose

`ECOSYSTEM_STATE_POINTER_V1` is a cross-surface freshness and authority pointer. It prevents a moving repository, document, mirror, or public projection from being mistaken for a semantic change or for current authoritative state.

The motivating failure mode is concrete: Tektite v0.1 is presently stored inside `DGAF-Framework`, so a display-only Tektite commit advances DGAF protected `main`. AOSS and other assurance lanes can require exact DGAF source provenance. Whole-repository movement therefore must be separated from change to the material source consumed by a particular downstream decision.

## Core rule

**Repository identity is provenance. Consumer-specific semantic-source identity determines material invalidation.**

A repository commit advancing is never ignored. It is recorded as provenance. But downstream consumers do not share one universal semantic subset. AOSS readiness and Tektite public status depend on different source artifacts, so each consumer owns a distinct semantic-source manifest.

If a required binding is absent, incomplete, or cannot be reverified, the state is `UNVERIFIED` and the system fails closed.

## Two-layer model

### Authority pointers

Authority records answer: **which source or state authority was observed?**

Each authority carries:

- `authority_id`
- `surface`
- `role`
- `object_identity`
- `predecessor_object_identity`
- `freshness_state`
- `invalidation_reason`
- `evidence_url`

### Consumer bindings

Consumer records answer: **which material semantic subset does this consumer depend on?**

Each consumer binding carries:

- `consumer_id`
- `authority_ids`
- `manifest_path`
- `manifest_digest_sha256`
- `freshness_state`
- `invalidation_reason`

This separation prevents one authority-level digest from being overloaded across consumers with different material dependencies.

## SEMANTIC_SOURCE_MANIFEST_V1

A semantic-source manifest contains the exact files/blobs/contracts and immutable external authority identities material to one consumer.

The manifest digest is SHA-256 over canonical JSON with:

- keys sorted;
- UTF-8 encoding;
- compact separators;
- `manifest_digest_sha256` omitted from the hashed material.

Each repository artifact binds both path and Git blob SHA-1. Path-only manifests are insufficient.

The first candidate manifests are:

- `AOSS_STAGE_A_READINESS_SEMANTIC_SOURCE_V1`
- `TEKTITE_PUBLIC_STATUS_SEMANTIC_SOURCE_V1`

## AOSS binding

The AOSS Stage-A readiness manifest currently binds:

- ACP measurement mapping;
- artifact replay/receipt contract;
- collection authorization boundary;
- decision policy;
- environment binding;
- executable/destination binding;
- exact ACP source authority identity.

It does not treat the Tektite public shell as material to AOSS readiness.

## Tektite binding

The Tektite public-status manifest currently binds:

- DGAF `docs/CURRENT_STATE.md`;
- Tektite `index.html`, because it contains the projected status claims;
- exact ACP source authority identity.

It deliberately excludes `styles.css`. A styling-only change therefore advances repository provenance without changing the Tektite status semantic digest.

Mutable Notion prose is also not used as a cryptographic semantic dependency for the public snapshot. Notion remains the interpreted-state/routing layer; public current-status claims resolve through the owning source authorities.

## Freshness states

- `CURRENT`: required authority identities and semantic bindings have been reverified.
- `STALE_SOURCE_ADVANCED`: material semantic source changed after the pointer was created.
- `UNVERIFIED`: currentness cannot be established from available bindings.
- `HISTORICAL_SNAPSHOT`: event-time evidence, not eligible to answer current-state questions.

## Invalidation reasons

- `NONE`
- `SEMANTIC_SOURCE_CHANGED`
- `NON_SEMANTIC_REPOSITORY_ADVANCE`
- `DEPENDENCY_ADVANCED`
- `MISSING_BINDING`
- `UNVERIFIED`

`NON_SEMANTIC_REPOSITORY_ADVANCE` is not authorization to continue. It means an authority used by that consumer moved while its material semantic manifest remained byte-identical.

## Comparison algorithm

For previous and newly observed pointers:

1. Compare authority object identities.
2. Resolve the semantic-source manifest for each consumer.
3. Recompute its deterministic digest from authoritative bindings.
4. If the consumer digest changed, classify `SEMANTIC_SOURCE_CHANGED`.
5. If a depended-on authority moved but the consumer digest did not, classify `NON_SEMANTIC_REPOSITORY_ADVANCE`.
6. If neither changed, classify `NONE`.
7. If a binding cannot be established, classify `UNVERIFIED` or `MISSING_BINDING`.
8. Never promote authorization, scientific N, efficacy, independence, or High-Assurance state through freshness reconciliation.

## Tektite release rule

A public Tektite build should publish or embed:

- `observed_at`;
- exact DGAF commit;
- exact ACP commit;
- Tektite semantic-source-manifest digest;
- generated-from pointer identity;
- freshness state.

If a material upstream source changes and the public snapshot is not regenerated/reverified, Tektite must render the snapshot stale or unverified rather than current.

## AOSS rule

AOSS retains the exact DGAF repository commit used for provenance and additionally binds the AOSS-specific semantic-source manifest. A Tektite-only presentation change must not be silently treated as an AOSS apparatus change.

## Fixed non-effects

This control does not establish:

- scientific N increment;
- independent validation;
- canonical DGAF efficacy;
- High-Assurance authorization;
- live repository mutation authorization;
- production executor readiness.

It is freshness and provenance infrastructure only.
