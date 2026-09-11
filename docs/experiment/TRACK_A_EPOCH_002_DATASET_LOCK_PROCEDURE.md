# Track A Epoch 002 dataset-lock procedure

Status: **PROSPECTIVE TOOLING ONLY · DATASET LOCK NOT ESTABLISHED · UNBLINDING NOT AUTHORIZED · N=0**

Controller: issue #619. Historical issue #483 is a pattern source only; no Epoch 001 identity, artifact, custody, or authorization value transfers into Epoch 002.

## Purpose

This procedure defines the post-collection structural lock boundary for Track A Epoch 002. It is intentionally separate from collection authorization, unblinding authorization, materialization, and primary-analysis authorization.

A valid lock proves only that the already-retained blinded collection has a stable, content-addressed evidence identity and that its public/protected retention surfaces passed the preregistered structural checks. It does **not** inspect or aggregate outcomes for inference, decrypt protected topology mappings, release a mapping, run primary analysis, establish canonical DGAF efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

The current repository has no canonical Epoch 002 dataset-lock receipt. Tooling validation must preserve that absence until a real authorized collection exists.

## Two-layer pattern

Epoch 002 uses two layers instead of placing future artifact metadata directly into the generic result-record envelope.

1. **External dataset-lock evidence manifest**
   - schema: `docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json`
   - canonical inner filename: `track_a_epoch_002_dataset_lock_evidence.json`
   - paired pre-lock ledger filename: `track_a_epoch_002_pre_lock_result_ledger.json`
   - canonical GitHub artifact name: `track-a-epoch-002-dataset-lock-evidence`
   - generated only after a future authorized collection and read-only structural QC
   - content-binds both retained collection artifacts and the PASS `QC_LEDGER` predecessor

2. **Repository dataset-lock receipt**
   - canonical path: `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json`
   - existing generic `record_type`: `DATASET_LOCK_RECEIPT`
   - introduced later as an exact one-parent / one-file / first-history event
   - `immutable_subject.sha256` binds the exact evidence-manifest bytes
   - `immutable_subject.workflow_run_id` and `artifact_id` bind the exact retained evidence artifact
   - `predecessor_record_ids` contains exactly the PASS `QC_LEDGER` record ID
   - `authorization_effect` remains `REQUIRES_SEPARATE_EXACT_COMMIT`

This keeps the #618 structural/semantic envelope stable while allowing the detailed evidence surface to grow without smuggling authority into the result record.

## Required retained collection surfaces

The future collection/QC path must retain these exact artifact classes:

- public artifact: `track-a-epoch-002-public-blinded`
- protected artifact: `track-a-epoch-002-protected-encrypted`
- dataset-lock evidence artifact: `track-a-epoch-002-dataset-lock-evidence`

The public artifact extraction root is `track_a_epoch_002_public/` and contains exactly:

- 50 `track_a_epoch_002_seed_<seed>.json` files;
- 50 matching `.sha256` sidecars;
- `track_a_epoch_002_manifest.json`;
- its matching `.sha256` sidecar.

The lock validator may parse the public files only for structural validation: exact field allowlists, strict boolean endpoint type, blinded topology IDs, seed/failure matrix membership, registered exclusions, and identity bindings. It must not tally, compare, summarize, rank, or interpret `ffcr_success`.

The protected artifact remains encrypted. Its extraction root contains exactly:

- `track_a_epoch_002_custody_cert.pem`;
- `track_a_epoch_002_custody_cert.sha256`;
- `track_a_epoch_002_protected.cms`;
- `track_a_epoch_002_protected_ciphertext.sha256`;
- `track_a_epoch_002_protected_plaintext_tar.sha256`.

No protected plaintext mapping, private custody key, blinding secret, passphrase, or decrypted tar is permitted in the retained protected artifact or in dataset-lock validation.

## Evidence requirements

The external evidence manifest must bind, at minimum:

- exact evidence-workflow run and tooling commit;
- exact collection-workflow run;
- exact collection-authorization commit and frozen candidate;
- accepted custody-receipt blob identity;
- exact PASS `QC_LEDGER` record ID and SHA-256 of the 53-record pre-lock result ledger;
- 50 paired seed units and 2,250 blinded observations;
- public artifact ID, size, archive SHA-256, and whole-epoch manifest SHA-256;
- protected artifact ID, size, archive SHA-256, ciphertext SHA-256, pre-encryption tar commitment, custody-certificate SHA-256, and custody public-key fingerprint;
- structural-QC PASS facts;
- `SAME_SYSTEM_NONINDEPENDENT` custody;
- no outcome inspection for the lock, no aggregation, no unblinding, no primary analysis, no historical pooling, no Epoch-004 substitution, no High-Assurance authorization;
- scientific N increment `0`;
- canonical DGAF efficacy `NOT_ESTABLISHED`.

Future IDs, sizes, and digests are empirical retention facts. They must be recorded only after the corresponding run/artifacts exist. They must never be predicted or placeholder-filled.

## Pre-lock ledger requirement

The pre-lock result ledger must contain exactly 53 records and end with a PASS `QC_LEDGER`:

1. `PRECOLLECTION_GATE_CHECKLIST`
2. `COLLECTION_START_RECEIPT`
3. 50 ordered `PER_SEED_EXECUTION_RECORD` entries
4. `QC_LEDGER`

It must pass both:

- `scripts/validate_track_a_epoch_002_result_ledger.py`
- `scripts/validate_track_a_epoch_002_result_record_semantics.py`

The dataset-lock receipt is the next record in the already-defined order. A failed, blocked, stale, unverified, or otherwise non-PASS predecessor cannot be promoted into a lock.

## Future receipt event

After the real collection and read-only dataset-lock evidence workflow are complete:

1. Retrieve the exact evidence artifact by the future receipt's `immutable_subject.workflow_run_id` and `artifact_id`.
2. Require the evidence workflow to be completed/successful and its exact head to equal the evidence tooling commit named by the receipt.
3. Hash `track_a_epoch_002_dataset_lock_evidence.json` and require equality with `immutable_subject.sha256`.
4. Validate the paired pre-lock ledger and its SHA-256.
5. Resolve the collection run and the exact public/protected artifact IDs named by the evidence manifest.
6. Require both artifacts to be unexpired, exact-name matches, exact-size matches, and exact archive-digest matches.
7. Validate public sidecars/manifest/matrix structure without outcome aggregation.
8. Validate the protected ciphertext/certificate commitments without decrypting protected data or using a private key.
9. Require the repository event to have exactly one parent and exactly one changed path: `TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json`.
10. Require that path to be absent at the parent and have first-and-only history at the event head.
11. Require the receipt to conform to the existing #618 result-record structural schema and semantic policy.
12. Merge only after the complete exact-head repository validation wave is terminal green.

A validated PR means **pending validated merge**, not established lock. The dataset lock becomes repository-established only after the exact one-file event is accepted into protected `main`.

## Authority boundary

Dataset lock and unblinding are different events.

A PASS `DATASET_LOCK_RECEIPT` carries the complete non-effect ceiling and has:

`authorization_effect = REQUIRES_SEPARATE_EXACT_COMMIT`

Therefore it cannot authorize its own successor. Any future `UNBLINDING_DECISION_RECORD` remains a separate human-controlled decision with its own exact commit and bounded scope.

Until the real predecessor evidence exists and the one-file receipt is accepted, preserve:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

`TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`

`UNBLINDING = NOT_AUTHORIZED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
