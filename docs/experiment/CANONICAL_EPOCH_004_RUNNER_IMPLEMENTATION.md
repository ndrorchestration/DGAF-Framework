# Canonical Solo Empirical Epoch 004 — Runner Implementation Boundary

## Status

`RUNNER IMPLEMENTED FOR VALIDATION / RUN REQUEST ABSENT / EMPIRICAL EXECUTION NOT AUTHORIZED / N INCREMENT = 0`

This increment implements the collection machinery required by the frozen Epoch 004 collection contract. It does not itself authorize a run and does not add `docs/experiment/solo_runs/CANONICAL_EPOCH_004_RUN_REQUEST.json`.

## Authorization identity

A run-request file cannot contain the SHA of the same commit that contains the request, because that creates an impossible self-reference. The authorization contract therefore uses two identities:

1. `authorized_runner_parent_sha` — the already-known exact runner commit from which the run branch is created;
2. the actual frozen run SHA — the subsequent authorization commit, verified by GitHub to change **exactly one file**, `docs/experiment/solo_runs/CANONICAL_EPOCH_004_RUN_REQUEST.json`.

The runner independently requires `PDMAL_FROZEN_COMMIT_SHA` to equal the checked-out authorization commit. This binds execution to the exact one-file authorization commit without circular hashing.

## Fail-closed execution predicates

A future run requires all of the following simultaneously:

- branch matching `solo-canonical-epoch-004/run-*`;
- exact one-file authorization commit;
- request JSON exactly matching the frozen Epoch 004 epoch/matrix/analysis/governance fields;
- request `authorized_runner_parent_sha` equal to `HEAD^`;
- `PDMAL_MODE=solo_canonical_epoch_004`;
- protocol frozen flag;
- explicit Solo Epoch 004 authorization flag;
- Solo limitations acknowledgement;
- High-Assurance authorization not asserted;
- unblinding authorization not asserted;
- exact frozen commit equality;
- canonical qualification bytes/digest valid;
- locked analysis blob unchanged;
- treatment-input preflight re-run successfully before key generation;
- fresh protected blinding key and durable archive root.

Any missing or mismatched predicate aborts before empirical collection.

## Treatment runtime identity

The runner uses an Epoch 004-specific canonical TGL adapter identity (`pdmal-canonical-epoch-004`) rather than carrying the earlier non-empirical diagnostic agent identity into the treatment runtime. Step 8 still verifies the exact external P-11/11Q qualification artifact; the retired scalar Apogee confidence gate is not reintroduced.

## Blinding and lock behavior

On a future authorized run, the workflow will:

1. validate the one-file request;
2. install the hash-locked environment;
3. re-run treatment-input preflight;
4. generate a fresh 256-bit-class random blinding key;
5. collect the fixed 50-seed / 9,000-observation matrix;
6. structurally verify seed identities, sidecars, blinded arm balance, matrix uniqueness/completeness, frozen SHA, and environment fingerprint **without reading or aggregating outcome fields**;
7. emit a `LOCKED_BLINDED` dataset-lock manifest;
8. upload the blinded dataset and blinding key as separate same-system artifacts.

The workflow does not authorize unblinding or execute the locked primary analysis.

## Current boundary

`RUN_REQUEST = ABSENT`

`EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`SCIENTIFIC_N_INCREMENT = 0`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = UNCHANGED / NOT_AUTHORIZED / N=0`
