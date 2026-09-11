# Track A Epoch 002 Dataset-Lock Procedure

Status: **prospective tooling only**. This procedure does not establish a dataset lock, authorize collection or unblinding, authorize or run primary analysis, establish efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

Current controlling state remains:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

## Purpose

After a future separately authorized and completed blinded Epoch 002 collection, preserve a content-addressed structural evidence boundary before any unblinding decision. The lock must be established without reading endpoint outcomes or decrypting protected topology mappings.

The repository uses two distinct surfaces:

1. `TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json` defines the non-authorizing evidence-manifest contract. A future evidence manifest binds the exact collection authorization/candidate/run identities, public and encrypted artifact identities and digests, whole-epoch manifest commitment, ciphertext/pre-encryption commitment, custody-certificate fingerprints, dataset shape, structural QC, and nonpromotion state.
2. `track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json` is the future canonical repository state event. It is not created by this tooling PR. Its `immutable_subject.sha256` must equal the SHA-256 of the exact evidence-manifest bytes supplied to validation.

The evidence manifest is retained separately from the one-file repository transition. It is evidence input, not a second authorization plane.

## Preconditions for a future lock event

A future lock proposal is admissible only after all of the following exist and validate:

- a separately authorized Epoch 002 empirical collection;
- the exact frozen candidate and collection-authorization identities;
- a completed 50-seed / 2,250-blinded-observation retained result ledger through `QC_LEDGER`;
- public blinded artifact identity, archive SHA-256, and whole-epoch manifest SHA-256;
- protected encrypted artifact identity and archive SHA-256;
- protected ciphertext SHA-256 and pre-encryption tar commitment;
- exact custody-certificate byte/public-key fingerprint binding;
- per-seed sidecar and complete-matrix structural QC `PASS`;
- `outcome_values_inspected=false` and `outcome_aggregation_performed=false`;
- same-system/nonindependent custody classification;
- unblinding and primary analysis still unauthorized;
- canonical DGAF efficacy still `NOT_ESTABLISHED` and scientific-N increment still zero.

Future run IDs, job IDs, artifact IDs, sizes, and digests must come from retained collection evidence. They must never be guessed or preregistered as fabricated values.

## Validation sequence

Validate an evidence manifest independently with:

```text
python scripts/validate_track_a_epoch_002_dataset_lock.py --validate-evidence-manifest <manifest.json>
```

A future repository event validator receives the exact evidence manifest and the retained pre-lock result ledger as inputs and verifies the proposed receipt against their content and QC identity. The repository event must have exactly one parent, change only `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json`, introduce that path for the first and only time, and validate against the existing Epoch 002 result-record structural schema and semantic policy.

The future PASS receipt must:

- be `DATASET_LOCK_RECEIPT`;
- directly name the exact predecessor `QC_LEDGER` record ID;
- bind only the exact evidence-manifest SHA-256 through `immutable_subject`;
- preserve the full non-effect ceiling;
- use `authorization_effect=REQUIRES_SEPARATE_EXACT_COMMIT`;
- preserve `empirical_n_increment=0` and canonical efficacy `NOT_ESTABLISHED`.

## Authority boundary

A dataset-lock PASS proves only that the retained blinded collection evidence has been structurally content-bound under the declared contract. It does **not** release a mapping, decrypt protected material, authorize unblinding, authorize primary analysis, inspect or aggregate outcomes, establish efficacy, or create an independent-custody claim.

Any later unblinding decision remains a separate human-controlled exact repository event under the already-established Epoch 002 semantics. Primary-analysis authorization remains later and separate again.

## Current tooling check

Until the future receipt exists, the only repository-state command is:

```text
python scripts/validate_track_a_epoch_002_dataset_lock.py --expect-absent
```

A PASS means only that the canonical dataset-lock receipt remains absent and the tooling boundary itself is intact.
