# ECOSYSTEM_STATE_POINTER_V1

## Purpose

`ECOSYSTEM_STATE_POINTER_V1` is a cross-surface freshness and authority pointer. It prevents a moving repository, document, mirror, or public projection from being mistaken for a semantic change or for current authoritative state.

The motivating failure mode is concrete: Tektite v0.1 is presently stored inside `DGAF-Framework`, so a display-only Tektite commit advances DGAF protected `main`. AOSS and other assurance lanes can require exact DGAF source provenance. Whole-repository movement therefore must be separated from change to the material source consumed by a particular downstream decision.

## Core rule

**Repository identity is provenance. Consumer-specific semantic-source identity determines material invalidation.**

A repository commit advancing is never ignored. It is recorded as provenance. But downstream consumers do not share one universal semantic subset. AOSS readiness and Tektite public status depend on different source artifacts, so each consumer owns a distinct semantic-source manifest.

If a required binding is absent, incomplete, or cannot be reverified, the state is `UNVERIFIED` and the system fails closed.

### Observation trust boundary

The v1 pointer validator is a consistency validator over supplied source observations. It verifies pointer structure, manifest structure, deterministic digests, authority references, and fixed non-promotion ceilings.

Repository artifact bindings receive an additional Git-object verification layer. `scripts/verify_semantic_source_git_bindings.py` resolves each declared `repository_commit:path` against local full Git history, requires the resolved object to be a blob, and fails if the actual blob identity differs from `git_blob_sha1`. CI runs this check for the AOSS and Tektite semantic-source manifests with `fetch-depth: 0`.

This closes the repository path/blob trust gap but does **not** autonomously verify external authorities such as GitHub repositories, Notion, Drive, or runtime state. Those observations still require their own producer/reconciliation evidence.

An embedded pointer is an immutable observation snapshot, not an autonomous freshness oracle. The legacy filename `ecosystem_state_pointer.current.json` means "latest embedded pointer artifact," not "self-proving current repository tip."

For an in-repository pointer, live repository-tip currentness requires external reconciliation evidence. The embedded artifact records the source observation commit, while its own container commit is bound externally after commit creation. If a producer cannot establish live currentness, it must fail closed rather than infer it from the embedded file.

## Three-way repository identity

An in-repository freshness pointer must distinguish three identities:

1. **source observation commit** — the repository state evaluated when the pointer was produced;
2. **container commit** — the immutable commit that contains the pointer snapshot; this is necessarily bound externally because writing it into the same file would create a new commit;
3. **live reconciliation observation** — an external or CI observation used when claiming current repository-tip state.

The pointer therefore sets `container_commit=null` and `container_commit_binding=EXTERNAL_ONLY`. Its embedded `live_reconciliation` status is `NOT_EMBEDDED`.

This avoids the fixed-point error where a file attempts to contain the SHA of the commit that contains that same file.

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
- `semantic_material_digest_sha256`
- `freshness_state`
- `invalidation_reason`

This separation prevents one authority-level digest from being overloaded across consumers with different material dependencies.

## SEMANTIC_SOURCE_MANIFEST_V1

A semantic-source manifest contains the exact files/blobs/contracts and immutable external authority identities material to one consumer.

The `semantic_material_digest_sha256` is SHA-256 over canonical JSON containing only:

- `consumer`;
- `artifacts`;
- `external_authorities`;
- `non_effects`.

Keys are sorted, encoding is UTF-8, and compact JSON separators are used.

The provenance envelope — including `schema_version`, `manifest_id`, `observed_at`, `repository`, and `repository_commit` — is deliberately excluded from the semantic-material digest. A timestamp refresh or repository-only advance therefore cannot manufacture a semantic change.

Each repository artifact binds both path and Git blob SHA-1. Path-only manifests are insufficient.

The first candidate manifests are:

- `AOSS_STAGE_A_READINESS_SEMANTIC_SOURCE_V1`
- `TEKTITE_PUBLIC_STATUS_SEMANTIC_SOURCE_V1`

## AOSS binding

The AOSS Stage-A readiness manifest uses a conservative transitive semantic closure.

Its closure basis is:

- the pre-data readiness validator itself;
- every repository/schema artifact read directly by that validator;
- executable comparator and decision-policy sources whose Git blobs are checked by the validator;
- the ACP adapter source referenced by the readiness evidence record;
- the previously bound collection-authorization, environment, and executable/destination records, retained so an earlier guarded boundary is not silently dropped;
- exact ACP source authority identity.

A 2026-10-01 transitive audit found the earlier six-artifact manifest under-bound this consumer. The correction is classified as `SEMANTIC_SOURCE_CHANGED` because the manifest's material set changed, not because scientific evidence, external validation, or authorization changed.

It does not treat the Tektite public shell as material to AOSS readiness.

## Tektite binding

The Tektite public-status manifest binds the material public-status closure:

- DGAF `docs/CURRENT_STATE.md`;
- Tektite `public/index.html`, because it contains the rendered projected status claims;
- `status.seed.json`, because the public shell describes itself as a projection of static status seed artifacts;
- `evidence-ledger.seed.json`, because it carries public evidence-to-claim semantics;
- `case-studies/ACP_PR_145.md`, because the public shell links it as bounded case-study detail;
- exact ACP source authority identity.

It deliberately excludes `styles.css`. The audited stylesheet contains presentation rules only and no content-hiding, generated-text, or status-dependent logic. A styling-only change therefore advances repository provenance without changing the Tektite status semantic digest. If future CSS or client-side code can suppress, reveal, generate, or reinterpret governance status, that artifact becomes semantic material and must be added before release.

Mutable Notion prose is also not used as a cryptographic semantic dependency for the public snapshot. Notion remains the interpreted-state/routing layer; public current-status claims resolve through the owning source authorities.

## Freshness states

- `CURRENT`: valid only in externally reconciled live-state evidence; an embedded in-repository pointer must not use it to claim repository-tip currentness.
- `STALE_SOURCE_ADVANCED`: material semantic source changed after the pointer was created.
- `UNVERIFIED`: currentness cannot be established from available bindings.
- `HISTORICAL_SNAPSHOT`: event-time or embedded snapshot evidence, not by itself eligible to answer live repository-tip current-state questions.

## Invalidation reasons

- `NONE`
- `SEMANTIC_SOURCE_CHANGED`
- `NON_SEMANTIC_REPOSITORY_ADVANCE`
- `DEPENDENCY_ADVANCED`
- `MISSING_BINDING`
- `UNVERIFIED`

`NON_SEMANTIC_REPOSITORY_ADVANCE` is not authorization to continue. It means an authority used by that consumer moved while its material semantic manifest remained byte-identical.

## Comparison algorithm

Consumer presence is itself part of the freshness contract. If a consumer binding exists on only one side of a comparison, the result is `MISSING_BINDING`, not `DEPENDENCY_ADVANCED`. Addition or disappearance of a binding therefore fails closed until the consumer is explicitly reconciled.

For previous and newly observed pointers:

1. Compare authority object identities.
2. Resolve the semantic-source manifest for each consumer.
3. Recompute its deterministic semantic-material digest from authoritative bindings, excluding provenance-envelope fields.
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

## Embedded snapshot rule

The checked-in pointer is intentionally an immutable historical snapshot. It must:

- record `snapshot_provenance.source_observation_commit`;
- keep `snapshot_provenance.container_commit=null`;
- declare `container_commit_binding=EXTERNAL_ONLY`;
- keep embedded live-reconciliation fields null;
- use `HISTORICAL_SNAPSHOT` for embedded authority and consumer freshness states;
- require external/CI reconciliation before claiming repository-tip currentness.

The validator accepts `--live-repository-commit` and `--container-commit` only as external runtime evidence. If the live repository commit differs from the source observation commit, the embedded pointer fails closed as not repository-tip current. The container commit must never be substituted for the source observation commit.

This refinement preserves the consumer-specific semantic-material model. It changes only the semantics of embedded currentness claims.
