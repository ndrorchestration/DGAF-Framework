# Track A Epoch 002 materialization-receipt procedure

Status: **CORRECTIVE TOOLING · DATASET LOCK ESTABLISHED · BOUNDED UNBLINDING AUTHORIZED · MATERIALIZATION NOT ESTABLISHED · PRIMARY ANALYSIS NOT AUTHORIZED / NOT RUN · N=0**

Controller: issue #632. Accepted tooling PR #703 established the first current-lineage materialization validator, but post-acceptance review found that its future real-event path still assumed GitHub Actions workflow/artifact IDs. Accepted Epoch 002 custody and dataset-lock evidence are instead `OPERATOR_CODESPACE` and content-addressed. This procedure defines the corrected model.

The accepted dataset-lock event is `e7ba2fe6fc6b3587957c59231da81ae107cacab2`. The accepted bounded unblinding event is `bf6279b9989f211e324ff3e9012788bed95e5c84`. Historical Epoch 001 materialization code is a pattern source only; no Epoch 001 identity, artifact, key, custody assumption, result, or authorization transfers into Epoch 002.

## Purpose

The materialization boundary is deliberately split into three different things:

1. **materializer implementation** — separately reviewed deterministic code at `scripts/materialize_track_a_epoch_002_unblinded_input.py`;
2. **operator materialization evidence** — a non-secret content-addressed JSON record produced after operator-side controlled decryption/materialization;
3. **repository materialization receipt** — a later one-file, non-authorizing state-transition record that binds the exact admitted evidence bytes.

None of these steps authorizes primary analysis. A future accepted `MATERIALIZATION_RECEIPT` remains only a prerequisite for a separate `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD` under issue #633.

## Secret and execution boundary

Real Epoch 002 decryption/materialization must execute under `OPERATOR_CODESPACE` or an equivalently operator-controlled environment outside GitHub Actions. The custody private key or passphrase must never enter repository contents, pull-request text, issue comments, CI variables, Actions artifacts, or ChatGPT/plugin messages.

The repository validator and CI lane are validation-only. They do not:

- request, accept, reconstruct, decrypt with, or persist a custody private key;
- request or persist a passphrase or blinding secret;
- persist the protected plaintext mapping or decrypted mapping payload;
- construct the materialized empirical dataset;
- inspect or aggregate empirical outcomes;
- authorize or execute primary analysis;
- increment scientific N;
- establish canonical DGAF efficacy, independent validation, or High-Assurance authorization.

## Accepted predecessor chain

All materialization states fail closed unless the existing accepted predecessors remain intact:

1. `TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json` exists, is `PASS`, preserves its non-effects, and has exactly one immutable history event.
2. `TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json` exists, is `PASS`, retains scope `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`, and has exactly one immutable history event.
3. The unblinding decision names the accepted dataset-lock record as its sole predecessor.
4. The unblinding immutable subject binds the exact dataset-lock event commit and SHA-256 of the canonical dataset-lock receipt bytes.
5. The accepted unblinding event descends from the accepted dataset-lock event.

These facts authorize only bounded mapping release/decryption. They do not establish materialization or analysis authority.

## Operator materialization evidence contract

The future non-secret evidence object must conform to `TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE_SCHEMA.json`.

Required provenance includes:

- `evidence_execution_class = OPERATOR_CODESPACE`;
- SHA-256 of a non-secret operator execution receipt;
- exact evidence-tooling commit identity;
- exact separately accepted materializer path, commit, and Git blob SHA;
- accepted dataset-lock record ID, event commit, and canonical receipt SHA-256;
- accepted bounded-unblinding record ID, event commit, and canonical record SHA-256;
- exact public blinded source name, byte size, archive SHA-256, and manifest SHA-256;
- exact protected encrypted source name, byte size, archive SHA-256, ciphertext SHA-256, protected plaintext-tar identity SHA-256, custody-certificate SHA-256, and certificate public-key DER SHA-256;
- materialized-input, materialization-manifest, and materialization-sidecar SHA-256 values;
- exactly 50 paired seed units and 2,250 records;
- structural validation `PASS`;
- non-secret durable-retention metadata;
- unchanged `SAME_SYSTEM_NONINDEPENDENT` custody classification;
- explicit non-effects preserving no outcome aggregation, no primary-analysis authority/execution, no pooling/substitution, no High-Assurance authority, `scientific_n_increment = 0`, and `canonical_dgaf_efficacy = NOT_ESTABLISHED`.

GitHub Actions workflow IDs and artifact IDs are not valid substitutes for these operator/content-addressed identities and are rejected by the operator materialization evidence schema.

The validator cross-checks public/protected names, byte sizes, and digests against the already accepted canonical dataset-lock evidence rather than trusting repeated values in the materialization evidence.

## Stage 1 — separately accept the materializer implementation

Before any real decryption/materialization, the deterministic Epoch 002 materializer implementation must be reviewed and accepted separately at:

`scripts/materialize_track_a_epoch_002_unblinded_input.py`

That implementation may follow the structural lessons of the historical Epoch 001 materializer, but it must use Epoch 002 identities and must preserve the current custody boundary. Acceptance of the implementation does not execute it and does not establish materialization.

## Stage 2 — controlled operator materialization

Only after Stage 1 is accepted may the operator use the accepted bounded unblinding authority to perform controlled local decryption/materialization.

The execution must:

1. use the exact accepted materializer commit/blob;
2. verify exact locked source identities before use;
3. keep custody private-key/passphrase material outside repository and CI surfaces;
4. avoid outcome aggregation or primary analysis;
5. produce deterministic materialized input plus non-secret manifest/sidecar identities;
6. produce a non-secret materialization evidence JSON conforming to the schema;
7. retain the materialized output and execution evidence under an explicitly identified durable operator-controlled location.

No repository state transition is established merely because the operator execution succeeds.

## Stage 3 — creation-only repository evidence admission

Canonical future evidence path:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json`

The admission event must satisfy all of the following:

1. exactly one Git parent;
2. exactly one changed path: the canonical materialization evidence JSON;
3. the evidence path is absent at the parent;
4. the path has first-and-only history at the admission HEAD;
5. the canonical materialization receipt remains absent;
6. no primary-analysis authorization or analysis result exists;
7. the materialization evidence validates against the accepted dataset-lock evidence;
8. the evidence binds the exact accepted unblinding record commit and bytes;
9. the declared materializer and evidence-tooling commits are ancestors of the admission parent and the materializer blob identity matches exactly.

Acceptance of this event means only that **materialization evidence has been admitted**. It does not establish the repository materialization receipt and does not authorize analysis.

## Stage 4 — direct one-file materialization receipt

Canonical future receipt path:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json`

The receipt event must directly follow the accepted evidence-admission event and satisfy:

1. exactly one Git parent;
2. exactly one changed path: the canonical receipt JSON;
3. the receipt path is absent at the parent and has first-and-only history at the receipt HEAD;
4. the materialization evidence path has exactly one immutable history event;
5. the receipt parent is exactly that evidence-admission commit, preventing intervening repository drift;
6. the evidence-admission event itself changed only the canonical materialization evidence path;
7. all predecessor, source-artifact, materializer, and non-effect validations still pass;
8. no primary-analysis authorization or result exists.

The receipt must conform to the shared result-record schema and semantic policy:

- `record_type = MATERIALIZATION_RECEIPT`;
- `status = PASS`;
- evidence scope `DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING`;
- predecessor exactly the accepted bounded `UNBLINDING_DECISION_RECORD`;
- `immutable_subject.commit_sha` exactly the evidence-admission commit;
- `immutable_subject.sha256` exactly the canonical admitted materialization-evidence bytes;
- no workflow-run or artifact ID requirement;
- `authorization_effect = REQUIRES_SEPARATE_EXACT_COMMIT`;
- scientific-N increment remains `0`;
- canonical DGAF efficacy remains `NOT_ESTABLISHED`.

Required receipt non-effects remain:

- `DOES_NOT_AUTHORIZE_COLLECTION`;
- `DOES_NOT_AUTHORIZE_UNBLINDING`;
- `DOES_NOT_AUTHORIZE_ANALYSIS`;
- `DOES_NOT_INCREMENT_SCIENTIFIC_N`;
- `DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY`;
- `DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION`;
- `DOES_NOT_AUTHORIZE_HIGH_ASSURANCE`.

A receipt PR that passes CI is only a validated pending transition. Materialization becomes repository-established only if that exact one-file receipt event is accepted into protected `main`.

## Stage 5 — primary-analysis authorization remains separate

Only after an accepted materialization receipt may issue #633 proceed to a separate exact-commit primary-analysis authorization decision. The materialization receipt itself cannot authorize or run analysis.

`UNBLINDING_DECISION_RECORD != MATERIALIZATION_EVIDENCE`

`MATERIALIZATION_EVIDENCE != MATERIALIZATION_RECEIPT`

`MATERIALIZATION_RECEIPT != PRIMARY_ANALYSIS_AUTHORIZATION_RECORD`

## CI modes

The dedicated workflow resolves exactly one state from repository contents:

- `tooling_only`: neither canonical materialization evidence nor receipt exists;
- `evidence_admission`: evidence exists and receipt is absent;
- `receipt_event`: evidence and receipt both exist.

There is no Actions-artifact retrieval mode. All real evidence required for repository validation is content-addressed and admitted through the canonical repository evidence record.

For the current corrective #632 tooling PR, the exact changed-file scope is limited to the workflow, evidence schema, procedure, validator, original adversarial test suite, and focused operator-provenance test suite. No materializer or empirical artifact is added.

## Current boundary

Until a separately accepted evidence-admission event and later receipt event exist, preserve:

`TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`

`UNBLINDING = AUTHORIZED_BOUNDED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`

`MATERIALIZATION = NOT_ESTABLISHED`

`PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN`

`SCIENTIFIC_N_INCREMENT = 0`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

Broader High-Assurance governance remains:

`PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0`
