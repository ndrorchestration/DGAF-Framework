# Track A Epoch 002 materialization-receipt procedure

Status: **PROSPECTIVE TOOLING ONLY · DATASET LOCK NOT ESTABLISHED · UNBLINDING NOT AUTHORIZED · MATERIALIZATION NOT ESTABLISHED · N=0**

Controller: issue #632. The generic result-record structural and semantic authority is the accepted #618 contract, and the immediately preceding bounded authorization pattern is the accepted #627 unblinding-decision tooling. Historical Epoch 001 materialization code is a pattern source only; no Epoch 001 identity, artifact, key, custody assumption, result, or authorization transfers into Epoch 002.

## Purpose

This procedure defines the validation boundary for a future Track A Epoch 002 `MATERIALIZATION_RECEIPT`. The receipt can only attest that a deterministic materialization event was structurally validated after an accepted bounded `UNBLINDING_DECISION_RECORD`. It is a non-authorizing state-transition record.

This tooling does **not** decrypt protected artifacts, release or persist a mapping, create analysis-ready empirical input, authorize primary analysis, run primary analysis, aggregate outcomes, establish efficacy, establish independent validation, authorize High-Assurance, or increment scientific N.

The current repository contains no canonical Epoch 002 materialization receipt and no accepted Epoch 002 materializer implementation. The future implementation identity reserved by the evidence schema is:

`scripts/materialize_track_a_epoch_002_unblinded_input.py`

That path is an identity contract only. This issue does not create that implementation. A future real materialization event must bind an exact accepted materializer commit and blob before a receipt can validate.

## Canonical future record

Future path:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json`

A future record must conform exactly to `TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json` and `TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json`:

- `record_type = MATERIALIZATION_RECEIPT`;
- `status = PASS`;
- authority class remains `NONAUTHORIZING_STATE_TRANSITION`;
- pass profile is exactly `MATERIALIZATION_PASS`;
- evidence scope is exactly `DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING`;
- the exact predecessor is the accepted PASS `UNBLINDING_DECISION_RECORD`;
- `immutable_subject.commit_sha` binds the accepted unblinding-decision event commit;
- `immutable_subject.workflow_run_id` and `artifact_id` bind the retained materialization-evidence artifact;
- `immutable_subject.sha256` binds the exact materialization-evidence manifest bytes;
- `authorization_effect = REQUIRES_SEPARATE_EXACT_COMMIT`;
- scientific-N increment remains `0`;
- canonical DGAF efficacy remains `NOT_ESTABLISHED`.

The required non-effects are:

- `DOES_NOT_AUTHORIZE_COLLECTION`;
- `DOES_NOT_AUTHORIZE_UNBLINDING` — the receipt grants no new unblinding authority beyond its already accepted bounded predecessor;
- `DOES_NOT_AUTHORIZE_ANALYSIS`;
- `DOES_NOT_INCREMENT_SCIENTIFIC_N`;
- `DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY`;
- `DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION`;
- `DOES_NOT_AUTHORIZE_HIGH_ASSURANCE`.

`UNBLINDING_DECISION_RECORD != MATERIALIZATION_RECEIPT`

`MATERIALIZATION_RECEIPT != PRIMARY_ANALYSIS_AUTHORIZATION_RECORD`

## Required retained materialization evidence

The future materialization receipt is not self-authenticating. Its retained evidence manifest must conform to `TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE_SCHEMA.json` and must bind, at minimum:

1. protocol and Epoch 002 identity;
2. the accepted dataset-lock record ID, event commit, and canonical receipt SHA-256;
3. the exact retained dataset-lock evidence used to establish the public/protected artifact identities;
4. exact public blinded artifact ID, name, archive SHA-256, and manifest SHA-256;
5. exact protected encrypted artifact ID, name, archive SHA-256, ciphertext SHA-256, protected plaintext-tar SHA-256 identity, custody-certificate SHA-256, and custody public-key DER SHA-256;
6. the accepted bounded unblinding-decision record ID, event commit, and exact canonical record SHA-256;
7. deterministic materializer path, accepted materializer commit, and exact materializer blob SHA;
8. materialized analysis-input SHA-256;
9. materialization manifest SHA-256;
10. materialization sidecar SHA-256;
11. exactly 50 paired seed units and exactly 2,250 records;
12. structural validation `PASS`;
13. durable-retention class and a non-secret durable-retention identity;
14. unchanged same-system/non-independent custody classification;
15. explicit false values for secret persistence, outcome aggregation, primary-analysis authorization, primary-analysis execution, historical pooling, Epoch 001 pooling, Epoch 004 substitution, and High-Assurance authorization;
16. scientific-N increment `0` and canonical efficacy `NOT_ESTABLISHED`.

The validator cross-checks public/protected artifact identities against the retained dataset-lock evidence rather than accepting those identities merely because the materialization manifest repeats them.

## Preconditions for a future materialization event

A future materialization receipt is admissible only after all of the following are repository-established and immutable:

1. authorized and completed Epoch 002 collection;
2. accepted structural QC and `QC_LEDGER`;
3. accepted content-addressed `DATASET_LOCK_RECEIPT`;
4. a separately accepted PASS `UNBLINDING_DECISION_RECORD` with bounded scope `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
5. a separately reviewed deterministic Epoch 002 materializer implementation at the exact path reserved by the evidence schema;
6. retained materialization evidence whose external workflow/artifact identity and content digest can be independently re-fetched and verified;
7. retained exact dataset-lock evidence whose public/protected identities can be re-fetched and cross-checked.

No current tooling PR may fabricate any predecessor, materializer, retained evidence artifact, materialized input, or receipt.

## Exact repository event

A future PASS materialization receipt must be a distinct repository transition:

1. exactly one Git parent;
2. exactly one changed path: `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json`;
3. the receipt path must be absent at the parent;
4. the receipt path must have first-and-only history at the event HEAD;
5. the canonical unblinding-decision record must be byte-identical between the event parent and event HEAD;
6. the unblinding-decision record must have exactly one immutable history event;
7. the materialization evidence must bind that exact unblinding event commit and exact canonical record bytes;
8. the canonical dataset-lock receipt must already exist with exactly one immutable history event and must match the dataset-lock identity declared by the materialization evidence;
9. the separately retained dataset-lock evidence must prove that the public/protected artifact and custody identities did not drift;
10. the declared materializer commit must be an ancestor of the event parent, the declared source path must exist at that commit, and its Git blob SHA must match exactly;
11. no primary-analysis authorization record or locked-analysis result may exist at the materialization event;
12. the complete exact-head validation wave must pass before protected-main acceptance.

A pull request passing these checks is only a validated pending state-transition event. Materialization becomes repository-established only if the exact receipt event is accepted into protected `main`. The receipt still does not authorize primary analysis.

## Secret boundary

Neither this validator nor its CI lane may request, accept, reconstruct, upload, or persist:

- a custody private key;
- a custody-key passphrase;
- an encrypted private-key backup;
- a blinding secret;
- a protected plaintext mapping;
- a decrypted mapping payload;
- other recoverable secret-bearing custody material.

The retained materialization evidence contains identities and digests only. A protected plaintext-tar SHA-256 is an identity, not the plaintext itself. Durable-retention metadata must remain non-secret and is rejected when its identifier uses secret-bearing labels.

The CI lane is validation-only and read-only with respect to repository contents. It may retrieve already-retained GitHub Actions evidence artifacts by immutable IDs in a future receipt event, but it does not perform decryption or materialization.

## Analysis boundary

A PASS materialization receipt establishes only the bounded proposition that the materialization event and its retained evidence satisfy this contract. It cannot authorize or run primary analysis.

After a future accepted materialization receipt, a **separate exact commit** containing a valid `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD` is still required before locked primary analysis may run. No analysis result may coexist with or precede the materialization receipt event.

## Tooling-only acceptance

For this issue's implementation PR, acceptance requires all of the following:

- the canonical materialization receipt remains absent;
- the canonical primary-analysis authorization record remains absent;
- the canonical locked-analysis result remains absent;
- no materializer implementation is added by this issue;
- no materialized empirical input is created;
- focused adversarial tests pass;
- the dedicated exact-head CI lane passes;
- the complete repository exact-head validation wave passes.

## Current boundary

Until the real predecessor chain exists and a separate controlled materialization event is accepted, preserve:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

`REPOSITORY_REAL_CUSTODY_V2 = NOT_ESTABLISHED`

`TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`

`UNBLINDING = NOT_AUTHORIZED`

`MATERIALIZATION = NOT ESTABLISHED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
