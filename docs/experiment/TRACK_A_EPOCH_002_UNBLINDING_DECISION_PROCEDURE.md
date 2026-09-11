# Track A Epoch 002 unblinding-decision procedure

Status: **PROSPECTIVE TOOLING ONLY · DATASET LOCK NOT ESTABLISHED · UNBLINDING NOT AUTHORIZED · N=0**

Controller: issue #626. The generic result-record structural and semantic authority is the accepted #618 contract. Historical Epoch 001 unblinding/materialization code is a pattern source only; no Epoch 001 identity, key, artifact, custody assumption, or authorization transfers into Epoch 002.

## Purpose

This procedure defines the human-controlled authorization boundary immediately after a future accepted Track A Epoch 002 dataset lock. It validates a future `UNBLINDING_DECISION_RECORD`; it does **not** perform decryption, release a mapping, materialize unblinded analysis input, authorize primary analysis, run empirical work, establish efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

The current repository contains no canonical Epoch 002 unblinding-decision record. Tooling validation must preserve that absence until a real authorized collection has completed, a content-addressed dataset lock has been accepted, and a human separately elects to authorize the bounded unblinding action.

## Canonical record

Future path:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json`

The record must conform to the existing `TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json` and `TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json` contract:

- `record_type = UNBLINDING_DECISION_RECORD`;
- `status = PASS`;
- authority class remains `HUMAN_CONTROLLED_AUTHORIZATION`;
- bounded scope is exactly `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
- `authorization_effect = BOUNDED_RECORD_ONLY`;
- the exact predecessor is the accepted PASS `DATASET_LOCK_RECEIPT`;
- `immutable_subject.commit_sha` binds the dataset-lock event commit;
- `immutable_subject.sha256` binds the exact canonical dataset-lock receipt bytes;
- scientific-N increment remains `0`;
- canonical DGAF efficacy remains `NOT_ESTABLISHED`.

Required non-effects remain:

- `DOES_NOT_AUTHORIZE_COLLECTION`;
- `DOES_NOT_AUTHORIZE_ANALYSIS`;
- `DOES_NOT_INCREMENT_SCIENTIFIC_N`;
- `DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY`;
- `DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION`;
- `DOES_NOT_AUTHORIZE_HIGH_ASSURANCE`.

`DOES_NOT_AUTHORIZE_UNBLINDING` is forbidden on a PASS unblinding decision because this record's only positive authority is the bounded mapping-release/decryption decision itself.

## Preconditions

A future unblinding-decision event is admissible only after all of the following exist as accepted repository evidence:

1. authorized and completed Epoch 002 collection;
2. PASS structural QC through the required `QC_LEDGER`;
3. accepted content-addressed `DATASET_LOCK_RECEIPT`;
4. immutable one-event history for that dataset-lock receipt;
5. exact dataset-lock receipt bytes and event commit available for binding.

No current tooling PR may fabricate any of those predecessor events.

## Exact repository event

A future PASS unblinding decision must be a distinct human-controlled repository transition:

1. exactly one Git parent;
2. exactly one changed path: `TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json`;
3. the path must be absent at the parent;
4. the path must have first-and-only history at the event HEAD;
5. the dataset-lock receipt must be unchanged from the event parent;
6. the dataset-lock receipt must have exactly one immutable history event;
7. the decision must bind that exact event commit and exact receipt-byte SHA-256;
8. the complete exact-head validation wave must pass before protected-main acceptance.

A validated pull request is only a pending authorization event. The bounded unblinding decision becomes repository-established only if that exact event is accepted into protected `main`.

## Secret and materialization boundary

The decision record and validator must not contain or accept:

- custody private keys;
- passphrases;
- encrypted private-key backup copies;
- blinding secrets;
- protected plaintext mappings;
- decrypted mapping payloads;
- other recoverable secret material.

`scripts/validate_track_a_epoch_002_unblinding_decision.py` is validator-only. It exposes no write, decrypt, collection-execution, materialization, or analysis mode.

A future decryption/materialization operation remains a separate controlled step whose evidence is a later `MATERIALIZATION_RECEIPT`. Primary analysis remains separately gated by `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD`. Neither authority is granted by this decision.

## Current boundary

Until the real predecessor chain exists and a separate exact human-controlled unblinding event is accepted, preserve:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

`TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`

`UNBLINDING = NOT_AUTHORIZED`

`MATERIALIZATION = NOT ESTABLISHED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
