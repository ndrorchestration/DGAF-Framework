# Track A Epoch 002 dataset-lock procedure

Status: **COLLECTION COMPLETE · OPERATOR RETAINED-BYTE ADMISSION PENDING · DATASET LOCK NOT ESTABLISHED · UNBLINDING NOT AUTHORIZED · SCIENTIFIC-N INCREMENT 0**

Current controller: issue #679. Historical issue #619 owns the original prospective dataset-lock tooling lineage; issue #483 is an Epoch 001 pattern source only. No Epoch 001 identity, artifact, custody, authorization, or scientific state transfers into Epoch 002.

## Purpose

This procedure defines the post-collection structural lock boundary for Track A Epoch 002. It is intentionally separate from collection authorization, empirical execution, unblinding authorization, materialization, primary-analysis authorization, and efficacy adjudication.

A valid lock proves only that the already-retained blinded collection has a stable, content-addressed evidence identity and that its public/protected retention surfaces passed the declared structural checks. It does **not** inspect or aggregate outcomes for inference, decrypt protected topology mappings, release a mapping, run primary analysis, establish canonical DGAF efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

Track A Epoch 002 collection is already complete at 50 paired seed units / 2,250 blinded observations. The actual retained bytes remain in the operator-controlled environment. Repository tooling does not substitute for retained-byte admission.

## Provenance classes

The dataset-lock evidence schema supports two evidence-provenance paths.

### Legacy GitHub Actions evidence

The original path remains valid for evidence produced and retained as GitHub Actions artifacts. It binds:

- the exact evidence workflow run;
- the exact evidence artifact;
- the exact collection workflow run;
- exact public/protected collection artifact IDs and content identities.

The later receipt therefore carries `workflow_run_id`, `artifact_id`, and the evidence SHA-256 in its immutable subject.

### Operator Codespace evidence

The actual Epoch 002 collection used operator-controlled retained bytes rather than GitHub Actions collection artifacts. This path must not synthesize Actions run or artifact IDs.

Operator evidence therefore declares:

- `evidence_execution_class = OPERATOR_CODESPACE`;
- `collection_execution_class = OPERATOR_CODESPACE`;
- exact operator admission-record SHA-256;
- exact collection execution-receipt SHA-256;
- exact retained public/protected archive sizes and SHA-256 identities;
- exact public manifest, encrypted ciphertext, plaintext-tar commitment, custody certificate, and custody public-key commitments;
- exact 53-record pre-lock ledger SHA-256 and terminal PASS `QC_LEDGER` identity;
- `SAME_SYSTEM_NONINDEPENDENT` custody and the complete fail-closed non-promotion ceiling.

For this class, `evidence_workflow_run_id`, `collection_workflow_run_id`, and public/protected Actions `artifact_id` values are prohibited.

## Operator sequence

The operator path is deliberately split into distinct transitions.

1. **Retained-byte operator admission**
   - run the accepted #687 preparer against the actual retained archives outside the repository;
   - require a successful dry run before persistent write;
   - retain the non-secret admission record and execution receipt outside the repository;
   - do not expose private keys, passphrases, protected plaintext, decrypted mappings, or blinding secrets.

2. **Retrospective blinded pre-lock ledger**
   - run the accepted #688 preparer only after hardened retained-byte admission succeeds;
   - produce exactly 53 records: gate checklist, collection-start receipt, 50 per-seed records, terminal PASS `QC_LEDGER`;
   - preserve `authorization_effect = NONE`, scientific-N increment 0, and efficacy `NOT_ESTABLISHED` throughout.

3. **Read-only local structural QC / operator evidence generation**
   - validate public and protected retained archive bytes against their exact digests;
   - verify public sidecars, manifest identity, seed panel, matrix counts, schema allowlists, and strict endpoint type without tallying or interpreting endpoint values;
   - verify protected ciphertext/certificate commitments without decryption or private-key use;
   - produce the non-secret dataset-lock evidence manifest with `evidence_execution_class = OPERATOR_CODESPACE`.

   After the #687 → #688 → #689 retained-byte sequence has produced all required non-secret outputs, prepare the repository evidence-admission delta in dry-run mode first:

   ```bash
   python scripts/prepare_track_a_epoch_002_operator_evidence_admission.py \
     --retention-dir "$HOME/DGAF-Epoch002-Retention"
   ```

   Require:

   `TRACK_A_EPOCH_002_OPERATOR_EVIDENCE_ADMISSION_PREPARER=PASS_DRY_RUN_NOT_WRITTEN`

   Only after that succeeds, prepare the exact two-file working-tree delta:

   ```bash
   python scripts/prepare_track_a_epoch_002_operator_evidence_admission.py \
     --retention-dir "$HOME/DGAF-Epoch002-Retention" --write
   ```

   Require:

   `TRACK_A_EPOCH_002_OPERATOR_EVIDENCE_ADMISSION_PREPARER=PASS_NONAUTHORIZING_DELTA_PREPARED`

   This helper validates and copies the already-produced non-secret evidence bytes only. It does not stage, commit, push, merge, establish dataset lock, authorize unblinding, or run analysis.

4. **Repository evidence admission — separate non-authorizing event**
   - admit exactly two non-secret files:
     - `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json`
     - `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRE_LOCK_RESULT_LEDGER.json`
   - both paths must be creation-only, first-history files in the same one-parent event;
   - the evidence manifest and ledger must pass the dataset-lock schema plus structural/semantic ledger validation;
   - collection authorization and evidence-tooling commits must already exist in repository history;
   - this event does **not** establish dataset lock.

5. **Repository dataset-lock receipt — later separate one-file event**
   - canonical path: `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json`;
   - the event changes exactly that one file, with one parent and first-and-only history;
   - for operator provenance, the receipt immutable subject binds the exact repository evidence-admission commit plus exact evidence-manifest SHA-256;
   - no Actions workflow/artifact identity is invented or required;
   - merge only after the complete exact-head repository validation wave is terminal green.

   Only after the exact two-file evidence-admission event has been accepted into protected `main`, prepare the receipt in dry-run mode:

   ```bash
   python scripts/prepare_track_a_epoch_002_operator_dataset_lock_receipt.py
   ```

   Require:

   `TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_RECEIPT_PREPARER=PASS_DRY_RUN_NOT_WRITTEN`

   Only after that succeeds, prepare the exact one-file receipt delta:

   ```bash
   python scripts/prepare_track_a_epoch_002_operator_dataset_lock_receipt.py --write
   ```

   Require:

   `TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_RECEIPT_PREPARER=PASS_NONAUTHORIZING_DELTA_PREPARED`

   This helper derives the unique accepted evidence-admission commit from Git history, binds the exact admitted evidence SHA-256, constructs and validates the canonical receipt, and writes only the receipt path. It does not stage, commit, push, merge, authorize unblinding, materialize protected mappings, or run primary analysis.

A validated receipt PR means **pending validated merge**, not established lock. The dataset lock becomes repository-established only after the exact one-file receipt event is accepted into protected `main`.

## Required retained collection surfaces

The operator-local retained public surface contains exactly:

- 50 `track_a_epoch_002_seed_<seed>.json` files;
- 50 matching `.sha256` sidecars;
- `track_a_epoch_002_manifest.json`;
- its matching `.sha256` sidecar.

The lock validator may parse public files only for structural validation: exact field allowlists, strict boolean endpoint type, blinded topology IDs, seed/failure matrix membership, registered exclusions, and identity bindings. It must not tally, compare, summarize, rank, or interpret `ffcr_success`.

The protected retained surface remains encrypted and contains the declared custody certificate, certificate sidecar, encrypted CMS payload, ciphertext sidecar, and pre-encryption tar commitment. No protected plaintext mapping, private custody key, blinding secret, passphrase, or decrypted tar is permitted in repository evidence or dataset-lock validation.

## Pre-lock ledger bindings

The pre-lock ledger must contain exactly 53 records and end with a PASS `QC_LEDGER`:

1. `PRECOLLECTION_GATE_CHECKLIST`
2. `COLLECTION_START_RECEIPT`
3. 50 ordered `PER_SEED_EXECUTION_RECORD` entries
4. `QC_LEDGER`

The dataset-lock validator additionally requires the ledger to bind:

- the accepted frozen candidate commit and tree;
- the exact collection-authorization commit;
- for operator collection, the exact collection execution-receipt SHA-256;
- for operator collection, the exact operator admission-record SHA-256;
- the terminal QC record ID carried by the evidence manifest.

It must pass both existing result-ledger structural and semantic validators. A failed, blocked, stale, unverified, or otherwise non-PASS predecessor cannot be promoted into a lock.

## Repository evidence admission is not independent verification

The operator evidence manifest is generated from operator-controlled retained bytes and admitted by the same project/operator lineage. Its custody/evidence class remains `SAME_SYSTEM_NONINDEPENDENT`.

Repository admission creates durable, reviewable, content-addressed provenance. It does not transform same-system evidence into independent verification and does not allow stronger claims than the underlying retained-byte validation supports.

## Authority boundary

Dataset lock and unblinding are different events.

A PASS `DATASET_LOCK_RECEIPT` carries the complete non-effect ceiling and has:

`authorization_effect = REQUIRES_SEPARATE_EXACT_COMMIT`

Therefore it cannot authorize its own successor. Any future `UNBLINDING_DECISION_RECORD` remains a separate human-controlled decision with its own exact commit and bounded scope.

Until retained-byte admission, operator evidence admission, and the later one-file dataset-lock receipt are separately completed and accepted, preserve:

`TRACK_A_EPOCH_002_COLLECTION = COMPLETE`

`TRACK_A_EPOCH_002_OPERATOR_PROVENANCE = PENDING_RETAINED_BYTE_ADMISSION`

`TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`

`UNBLINDING = NOT_AUTHORIZED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN`

`SCIENTIFIC_N_INCREMENT = 0`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED`
