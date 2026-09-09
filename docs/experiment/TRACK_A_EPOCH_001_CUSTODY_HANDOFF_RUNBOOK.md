# Track A Epoch 001 custody handoff and materialization runbook

Status: **NON-SECRET OPERATING PROCEDURE · DOES NOT AUTHORIZE PRIMARY ANALYSIS**

This runbook operationalizes issue #496 using only the already-merged fail-closed tooling. It does not contain, locate, reconstruct, request publication of, or persist the CMS custody private key.

## Hard boundary

Before this procedure starts:

- Track A empirical collection is COMPLETE.
- Dataset lock is ESTABLISHED.
- Unblinding is AUTHORIZED.
- The matching custody private-key handoff is NOT ESTABLISHED.
- The unblinded analysis input is NOT YET MATERIALIZED.
- Primary analysis is NOT AUTHORIZED / NOT RUN.
- Canonical DGAF efficacy is NOT ESTABLISHED.
- High-Assurance is NOT AUTHORIZED.

The custody private key MUST remain local/ephemeral. Never paste, commit, upload, log, attach, or copy the key into GitHub, Notion, issue comments, PR descriptions, workflow inputs, shell history, or repository files.

## Accepted source identities

Use the exact retained Track A Epoch 001 source artifacts governed by issue #496:

- public archive SHA-256: `32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231`
- protected archive SHA-256: `f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f`
- protected CMS ciphertext SHA-256: `15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614`
- protected pre-encryption tar SHA-256: `ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35`
- custody certificate SHA-256: `cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707`
- controlled materializer merge: `f92c251bb8fcf068c644db04ae9d2f855c382caa`
- controlled materializer blob: `d4dd3551dda6413ee4d0b195c6d726e17cb2481a`
- custody preflight blob: `564c2c75b6e2c6ff10ba5759950f67a99c2cb274`
- unblinded-input receipt validator blob: `80ef872280713193ba4fbae4299c6558fe43d7c1`

If any required source identity does not match, STOP. Do not substitute another archive, certificate, key, materializer, dataset, epoch, or historical artifact.

## 1. Prepare the local handoff environment

Use a trusted local machine and a workspace outside the repository for secret-bearing paths. The repository checkout may contain tooling, but the custody key itself must not be copied into the repository tree.

Set local paths without echoing secret contents:

```bash
PUBLIC_ZIP=/secure/nonrepo/track-a-public.zip
PROTECTED_ZIP=/secure/nonrepo/track-a-protected.zip
CUSTODY_KEY=/secure/nonrepo/custody-private-key.pem
OUTPUT=/secure/nonrepo/TRACK_A_EPOCH_001_UNBLINDED_ANALYSIS_INPUT.json
```

Confirm that `$CUSTODY_KEY` is a local file and that the destination is not under the Git repository.

## 2. Run the custody-key preflight

From repository `main`, run:

```bash
python scripts/preflight_track_a_epoch_001_custody_key.py \
  --protected-artifact-zip "$PROTECTED_ZIP" \
  --custody-private-key "$CUSTODY_KEY"
```

Required output includes:

```text
TRACK_A_EPOCH_001_CUSTODY_KEY_PREFLIGHT=PASS
PRIVATE_KEY_PUBLISHED=FALSE
PROTECTED_MAPPING_DECRYPTED=FALSE
UNBLINDED_ANALYSIS_INPUT_MATERIALIZED=FALSE
PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
```

Any other result is a STOP condition. Do not attempt materialization after a failed or ambiguous preflight.

## 3. Materialize the locked unblinded input

Only after the exact preflight PASS, run:

```bash
python scripts/materialize_track_a_epoch_001_unblinded_input.py \
  --public-artifact-zip "$PUBLIC_ZIP" \
  --protected-artifact-zip "$PROTECTED_ZIP" \
  --custody-private-key "$CUSTODY_KEY" \
  --output "$OUTPUT"
```

Required terminal state includes:

```text
TRACK_A_EPOCH_001_UNBLINDED_INPUT_MATERIALIZED: 50 seeds; 2250 records
PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
OUTCOME_AGGREGATION=NOT_PERFORMED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
```

The materializer must emit `$OUTPUT.sha256`. Preserve the exact output bytes and sidecar. Do not inspect, summarize, aggregate, score, or otherwise analyze outcomes during this step.

## 4. Verify and retain the materialized input

Verify the sidecar locally:

```bash
sha256sum "$OUTPUT"
cat "$OUTPUT.sha256"
sha256sum "$OUTPUT.sha256"
```

Retain the output and sidecar through one accepted non-secret durable-retention class supported by the receipt validator:

- `GITHUB_ACTIONS_ARTIFACT`
- `GITHUB_RELEASE_ASSET`
- `LOCAL_CUSTODY_ARCHIVE`

The durable-retention identity recorded later must identify the retained unblinded input/sidecar, not the custody private key. Never retain the private key as part of this evidence packet.

Record locally, for the future receipt only:

- materialized input SHA-256;
- sidecar SHA-256;
- durable retention type;
- durable non-secret retention identifier.

## 5. End secret handling before repository mutation

After successful materialization and durable retention:

- remove any temporary decrypted protected material if present;
- ensure the private key remains outside the repository and outside any evidence artifact;
- do not commit the materialized dataset itself unless an explicitly accepted retention policy requires that exact mechanism;
- do not place the private key in shell transcripts, screenshots, issue comments, Notion, PR bodies, or CI variables.

The repository transition that follows must contain only non-secret receipt metadata.

## 6. Create the immutable unblinded-input receipt

Create exactly one new file:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_001_UNBLINDED_INPUT_RECEIPT.json`

The receipt must conform exactly to the merged validator schema and bind the actual materialized-input SHA-256, sidecar SHA-256, and durable-retention identity. It must preserve:

- `paired_seed_units = 50`
- `record_count = 2250`
- `structure_validation = "PASS"`
- `custody_class = "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT"`
- `independent_custody = false`
- `private_key_published = false`
- `primary_analysis_authorized = false`
- `primary_analysis_run = false`
- `outcome_aggregation_performed = false`
- `historical_pooling_allowed = false`
- `epoch_004_substitution_allowed = false`
- `high_assurance_authorized = false`
- `canonical_dgaf_efficacy = "NOT_ESTABLISHED"`

The receipt commit must be a one-parent event changing exactly that one previously absent receipt file. Run the merged receipt validator before merge.

## 7. Primary-analysis authorization remains separate

A valid receipt does not authorize analysis. Only after the receipt event is merged and independently validated may the separate primary-analysis authorization gate be constructed using the already-merged authorization tooling.

Until that later one-file authorization record is established:

```text
PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
OUTCOME_AGGREGATION=NOT_PERFORMED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

## Stop conditions

STOP immediately if any of the following occurs:

- source archive/ciphertext/certificate digest mismatch;
- custody-key preflight does not emit exact PASS;
- materialization reports any record-count, topology, seed, failure-matrix, candidate, protocol, algorithm, sidecar, or plaintext-digest mismatch;
- temporary protected plaintext cannot be shown to have been removed;
- the output or sidecar cannot be durably retained and re-identified;
- receipt construction would require storing secret material;
- receipt validation fails;
- any step would analyze outcomes before separate primary-analysis authorization.

A STOP leaves issue #496 open and preserves the fail-closed scientific state.
