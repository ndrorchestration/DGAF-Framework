# Track A Epoch 002 Precollection Preflight Procedure

## Status

Status: PROCEDURE ONLY / NON-AUTHORIZING / PRE-FREEZE / N=0

This procedure prepares and validates the retained precollection preflight required by the
Track A Epoch 002 successor gate chain. It does not establish freeze and cannot authorize
empirical collection, unblinding, primary analysis, High-Assurance operation, or any
scientific-N increment.

Controller: issue #523.

## Required order

The gate order is intentionally strict:

1. the schema-v2 successor custody recovery drill is completed locally;
2. only the public certificate and non-secret recovery receipt are admitted to Git together;
3. their exact bytes, public-key fingerprint, receipt contract, history, and source bindings pass;
4. the accepted repository head becomes the Epoch 002 candidate;
5. the preflight record is generated against that exact candidate;
6. a preflight-only pull request validates the record against its exact PR base;
7. only after accepted preflight may a separate immutable-freeze action be considered.

Do not combine custody evidence admission, preflight, freeze, closure, verification, or
collection authorization into one commit or pull request.

## Secret boundary

The repository preflight helper accepts no private-key path and no passphrase input. It must
never generate a keypair or read recoverable secret material. The encrypted private key,
its recovery copies, and the passphrase remain outside GitHub, CI, Notion, chat, and other
project documentation.

The public certificate and schema-v2 recovery receipt are deliberately non-secret evidence.
Their admission does not make custody independent; the required classification remains
`SAME_SYSTEM_NONINDEPENDENT`.

## 1. Admit the custody evidence

After the local custody-v2 drill has passed, create a pull request that changes exactly:

```text
docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json
docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem
```

The two files must be introduced together in one immutable commit. The preflight workflow
checks the exact PR delta, validates the schema-v2 receipt, recomputes the certificate
SHA-256, derives and hashes the certificate public key with OpenSSL, verifies the recovered
public-key fingerprint, confirms the two evidence files share one introduction commit, and
rechecks the locked Epoch 002 source bindings.

A passing custody-admission check means only:

```text
CUSTODY_EVIDENCE_ACCEPTED_FOR_PREFLIGHT_PREPARATION
INDEPENDENT_CUSTODY=FALSE
TRACK_A_FREEZE=NOT_ESTABLISHED
SUCCESSOR_COLLECTION_AUTHORIZED=FALSE
SCIENTIFIC_N_INCREMENT=0
```

## 2. Prepare the preflight record

After the custody-evidence pull request is accepted and `main` is refreshed to that exact
merge, run from a clean repository checkout:

```bash
python scripts/prepare_track_a_epoch_002_precollection_preflight.py --write
```

The helper binds the preflight to the current `HEAD` candidate and its exact tree. It refuses
to overwrite an existing preflight, refuses missing or invalid custody evidence, rejects
source drift, rejects weakened custody or authorization contract state, and refuses any
already-present downstream Epoch 002 gate.

The only intended new file is:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json
```

## 3. Validate in a preflight-only pull request

Commit only the generated preflight record and open a pull request against the exact
candidate that generated it. CI validates it with the PR base as the required candidate SHA.

The validator requires the PR delta to contain only the preflight record. The record must
match the exact structure consumed by `run_track_a_epoch_002.py`, including:

- protocol, algorithm, matrix, analysis-lock, and analysis identities;
- candidate commit and tree;
- custody receipt and certificate Git blob identities;
- encrypted-private-key SHA-256 identity only, never the key itself;
- certificate byte SHA-256 and public-key DER SHA-256;
- `SAME_SYSTEM_NONINDEPENDENT` custody classification;
- recovery drill `PASS`;
- all authorization booleans false;
- scientific-N increment equal to zero.

## 4. Post-acceptance boundary

A merged preflight establishes only **precollection readiness for later freeze review**.
The next gate is a separate immutable Epoch 002 freeze manifest. Freeze itself must remain
separate from collection authorization.

Controlling state until those later gates are explicitly satisfied:

```text
PRE-FREEZE
FAIL-CLOSED
SUCCESSOR COLLECTION NOT AUTHORIZED
N=0
CANONICAL DGAF EFFICACY NOT ESTABLISHED
```
