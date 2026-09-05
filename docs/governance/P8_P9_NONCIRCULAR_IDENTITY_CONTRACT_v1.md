# P8/P9 Non-Circular Identity Contract v1

**Status:** PRE-FREEZE CONTROL CONTRACT / NO EXECUTION AUTHORITY  
**Issue:** #280  
**Purpose:** Define a freeze and independent-verification identity model that cannot require an immutable object to contain evidence produced only after that object is finalized.

## Core rule

Post-freeze evidence MUST NOT be embedded into the immutable freeze object it claims to verify.

The final chain therefore uses two separately hashed objects and two externally bound commit identities.

## Object F — immutable freeze

`docs/experiment/PDMAL_IMMUTABLE_FREEZE.json`

Object F is created only after P4 closes and P7 is formally CLOSED. It is committed at exact freeze commit `F_COMMIT`.

Required properties include:

- `schema_version = 1`
- `record_type = PDMAL_IMMUTABLE_FREEZE`
- `freeze_state = FROZEN`
- exact accepted pre-freeze control-plane commit
- exact candidate SHA/tree/deployment
- exact apparatus/protocol/analysis/runner/schema identities
- retained P1/P2/P3/P4/P5/P6/P6a evidence identities/digests
- P4 custody commitments and attributable attestation digests
- pilot authorization still `NOT_GRANTED`
- empirical execution still `NOT_EXECUTED`, `n = 0`
- unblinding still `NOT_EXECUTED`

Object F MUST NOT contain:

- a SHA-256 of its own complete bytes;
- the SHA of the commit whose identity depends on F's own bytes;
- a post-freeze independent-verification record;
- a post-freeze verification-record digest;
- final P9 results;
- pilot authorization granted after P9.

After F is committed, its exact bytes are SHA-256 hashed and that digest is retained outside F.

## Record V — independent P8 freeze verification

`docs/experiment/PDMAL_P8_FREEZE_VERIFICATION.json`

Record V is produced only after an independent verifier retrieves exact commit F and re-hashes object F. V is stored in a descendant verification commit `V_COMMIT`, distinct from F.

Minimum record shape:

```json
{
  "schema_version": 1,
  "record_type": "PDMAL_P8_FREEZE_VERIFICATION",
  "status": "PASS",
  "freeze": {
    "commit_sha": "<F_COMMIT_40_HEX>",
    "path": "docs/experiment/PDMAL_IMMUTABLE_FREEZE.json",
    "expected_sha256": "<64_HEX_EXTERNAL_FREEZE_DIGEST>",
    "retrieved_sha256": "<64_HEX_RECOMPUTED_FREEZE_DIGEST>"
  },
  "verifier_id": "<ATTRIBUTABLE_OR_SYSTEM_VERIFIER_ID>",
  "verification_method": "<NONEMPTY_METHOD_DESCRIPTION>",
  "verified_at": "<RFC3339_TIMESTAMP_WITH_TIMEZONE>"
}
```

For PASS, `expected_sha256` and `retrieved_sha256` MUST be identical.

V's complete bytes are then SHA-256 hashed and that digest is retained outside V.

V MUST NOT contain:

- a hash of its own complete bytes; or
- `V_COMMIT` / the SHA of the commit whose identity depends on V's bytes.

`V_COMMIT` is an external identity supplied to final P9 and verified by exact checkout, just as the byte digest of V is supplied externally and recomputed.

## Commit relationship

The final P9 workflow MUST establish all of the following:

1. `F_COMMIT` and `V_COMMIT` are distinct 40-hex Git commit identities.
2. `F_COMMIT` is an ancestor of `V_COMMIT`.
3. workflow dispatch occurs from exact `V_COMMIT`.
4. F, the frozen candidate manifest, and the final P7 binding are read from exact `F_COMMIT`, not from the mutable branch tip at V.
5. V is read from exact `V_COMMIT`.
6. externally supplied byte digests for both F and V match independently recomputed bytes.

## Verifier immutability

The P9 verifier definition selected during P7 must be frozen at F.

At final P9, the workflow MUST compare the SHA-256 of:

- `scripts/verify_p9_frozen_chain.py`
- `.github/workflows/p9-final-frozen-chain.yml`

between F and V. Any drift MUST fail closed.

This allows V to add the post-freeze verification record while preventing the final-P9 algorithm from changing after the freeze.

## P7 boundary

P7 can close only on pre-freeze inputs. It MUST NOT require values created by P8, P9, or later authorization.

P7 closure blockers include:

- completed real P4 custody/access separation;
- final protocol identity;
- final accepted pre-freeze control-plane commit;
- selected P9 verifier script/workflow identities;
- all already-required candidate/scientific identities.

The following are downstream and may legitimately remain null when P7 closes:

- freeze commit/digest;
- P8 verification commit/digest;
- final P9 evidence;
- pilot authorization.

## P8 boundary

P8 consists of two ordered events:

1. construct immutable F and externally retain F digest;
2. independently verify F and produce externally hashed V without altering F.

P8 cannot close merely because F exists. P8 requires independent verification record V and an externally bound V commit/digest identity.

## P9 boundary

P9 verifies the final frozen integrity chain only after P8 completes. P9 MUST still observe:

- pilot authorization `NOT_GRANTED`;
- empirical execution `NOT_EXECUTED`;
- empirical N `0`;
- unblinding `NOT_EXECUTED`.

P9 PASS is integrity/governance evidence, not efficacy evidence and not authorization.

## Authorization boundary

Only after P9 legitimately closes may a separate explicit pilot authorization record be considered. Authorization is not part of F, V, or P9 PASS.

## Current state

This contract is preparatory. No F or V object has been created for the active experiment.

**P4: OPEN / NOT EXECUTED.**  
**P7: ADOPTED / FINAL BINDING OPEN.**  
**P8: OPEN / FAIL-CLOSED.**  
**P9: NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
