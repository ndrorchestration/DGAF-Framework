# Track A Epoch 002 operator collection admission procedure

Status: **COLLECTION COMPLETE · OPERATOR PROVENANCE NOT YET ADMITTED · DATASET LOCK NOT ESTABLISHED**

Controller: issue #679.

## Purpose

Admit the already completed, authorized Track A Epoch 002 collection executed in a user-controlled GitHub Codespace into the content-addressed dataset-lock evidence chain without fabricating GitHub Actions collection identities or re-running the experiment.

This admission is provenance only. It does not inspect or aggregate outcomes, decrypt protected mappings, authorize unblinding, authorize primary analysis, establish canonical DGAF efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

## Fixed execution identity

The admitted collection must bind:

- collection authorization commit `563152fdb254b8ee948a693c287126a8bf8314b8`;
- execution class `OPERATOR_CODESPACE`;
- Python `3.12.3`;
- requirements-lock blob `00c1f779e97030f9b25ae494642edb31b5b09de5`;
- 50 paired seed units;
- 2,250 blinded observations;
- `SAME_SYSTEM_NONINDEPENDENT` custody.

The operator path must not contain a GitHub Actions collection workflow-run ID or Actions artifact ID. Those identifiers do not exist for this execution and must not be invented or borrowed.

## Required retained surfaces

The operator must retain two separately content-addressed archives:

1. `track-a-epoch-002-public-blinded`
2. `track-a-epoch-002-protected-encrypted`

The public retention surface contains only the blinded collection outputs and their integrity sidecars/manifest. The protected retained surface contains only:

- `track_a_epoch_002_custody_cert.pem`;
- `track_a_epoch_002_custody_cert.sha256`;
- `track_a_epoch_002_protected.cms`;
- `track_a_epoch_002_protected_ciphertext.sha256`;
- `track_a_epoch_002_protected_plaintext_tar.sha256`.

Protected plaintext, the private custody key, passphrase, blinding secret, or a decrypted mapping must not appear in the admitted retained archive.

## Non-secret execution receipt

Before admission, create a small non-secret receipt containing only execution/provenance facts needed to distinguish this run from a GitHub Actions collection. At minimum it records:

- protocol and epoch identity;
- exact collection-authorization commit;
- exact frozen candidate/tree identity;
- Python version;
- requirements-lock blob identity;
- execution class `OPERATOR_CODESPACE`;
- completion status corresponding to the runner terminal result `TRACK_A_EPOCH_002_COLLECTION_COMPLETE: 50 seeds; 2250 observations`;
- 50 paired seed units / 2,250 blinded observations;
- no unblinding, analysis, pooling, Epoch-004 substitution, or High-Assurance authority.

The receipt must contain no secret and no endpoint values. Its exact bytes are SHA-256 bound by the operator-admission record.

## Admission record

The canonical admission record conforms to:

`docs/experiment/TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION_SCHEMA.json`

Validation is performed by:

`scripts/validate_track_a_epoch_002_operator_collection_admission.py`

The record content-addresses the public/protected retained archives and the non-secret execution receipt. It explicitly carries `collection_execution_class = OPERATOR_CODESPACE` and rejects GitHub Actions collection/artifact identities.

## Dataset-lock handoff

A PASS operator admission does not establish dataset lock. The next layer must perform the existing read-only structural QC over the admitted retained bytes and produce the 53-record pre-lock ledger ending in PASS `QC_LEDGER` plus the dataset-lock evidence manifest.

The eventual repository `DATASET_LOCK_RECEIPT` remains a separate exact one-parent / one-file / first-history event with `authorization_effect = REQUIRES_SEPARATE_EXACT_COMMIT`.

## Authority boundary

After operator admission but before dataset-lock receipt merge, preserve:

`TRACK_A_EPOCH_002_COLLECTION = COMPLETE`

`TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`

`UNBLINDING = NOT_AUTHORIZED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED`
