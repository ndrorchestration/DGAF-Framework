# Track A Successor — Recoverable Solo-Custody Contract

Status: **DESIGN / RECOVERY-TEST TOOLING ONLY / EMPIRICAL COLLECTION NOT AUTHORIZED**

Controller: #523

## Why this exists

Track A Epoch 001 completed blinded collection, but its CMS private key was not recoverably escrowed for the actual solo-operator model. Because the protected topology mapping and fresh blinding-key custody record were retained only inside the CMS-encrypted protected bundle, Epoch 001 cannot be honestly unblinded from retained evidence.

The successor must preserve blinding while proving **recoverability before collection**.

## Custody model

This is intentionally classified as:

`SAME_SYSTEM_NONINDEPENDENT`

Recoverability is not independent custody. A solo operator can prove that a secret can later be recovered without claiming that another actor independently controlled it.

## Required sequence before any successor collection authorization

1. Create the successor epoch/protocol identity without reusing Epoch 001 identity.
2. Freeze the successor scientific design prospectively. Preserve the existing primary endpoint/estimand/matrix unless a change is separately justified without reference to unseen Epoch 001 outcomes.
3. Select fresh seeds and verify no collision with Epoch 001.
4. Generate a fresh asymmetric custody keypair locally, outside the repository, before collection.
5. Store the private key only in encrypted PKCS#8 form protected by a strong secret known to the operator.
6. Create at least two durable, encrypted, user-controlled recovery copies in distinct storage classes.
7. Keep the private key, passphrase, recovery material, and recoverable secret data out of GitHub, Notion, chat, committed files, workflow inputs, command-line arguments, logs, and CI artifacts.
8. Retain only the public certificate/public key for collection.
9. Perform a precollection recovery drill from **each** retained encrypted copy:
   - recover/decrypt the private key locally;
   - derive its public key;
   - derive the public key from the certificate intended for collection;
   - require exact byte identity of the two public DER encodings;
   - clean up transient plaintext key material.
10. Emit a non-secret recovery receipt containing only fingerprints, non-secret backup classifications/identifiers, recovery PASS, and the same-system/nonindependent classification.
11. Validate that receipt with `scripts/validate_track_a_successor_solo_custody_receipt.py`.
12. Only a later, separate immutable authorization event may authorize successor empirical collection.

## Required receipt invariants

The recovery receipt must establish all of the following without containing secret material:

- fresh keypair created before collection;
- encrypted private-key container SHA-256 recorded;
- certificate SHA-256 recorded;
- certificate public-key DER SHA-256 recorded;
- recovered private-key-derived public DER SHA-256 recorded;
- recovered public DER exactly matches the intended collection certificate public DER;
- at least two distinct encrypted, user-controlled recovery copies exist;
- private key is not stored in repository, Notion, or chat;
- custody classification is `SAME_SYSTEM_NONINDEPENDENT`;
- independent custody is false;
- recovery drill is `PASS`;
- empirical collection authorization remains false;
- scientific state effect is `NONE`;
- canonical DGAF efficacy remains `NOT_ESTABLISHED`.

## Receipt version and evidence limits

The current helper emits schema v2: a timezone-qualified recovery timestamp and per-backup encrypted-container hash, recovered public-key DER hash, and recovery PASS. It requires explicit, distinct operator-declared storage classes; it does not infer offsite location from a path. The final receipt appears only after structural validation succeeds.

The validator retains schema-v1 compatibility for older records. A v1 validation is not evidence that both backups were tested. A structurally valid receipt is self-attested evidence, not independent observation of secret recovery, storage location, or durability. No real receipt is established by synthetic CI tests.

## Synthetic CI boundary

CI may create ephemeral synthetic keys solely to test validator/preflight mechanics. Synthetic keys are not successor custody material and cannot satisfy the real recovery receipt or authorize collection.

No workflow should generate the real successor custody private key. The real private key must originate in the user-controlled local custody environment.

## Epoch 001 isolation

Epoch 001 remains historical blinded evidence and an apparatus/custody failure record. Its blinded observations must not be pooled into the successor analysis, used to tune successor thresholds, or treated as efficacy evidence.

## Current authority boundary

`TRACK_A_EPOCH_001_PRIMARY_ANALYSIS = UNANALYZABLE / NOT_RUN`

`SUCCESSOR_TRACK_A_EMPIRICAL_COLLECTION = NOT_AUTHORIZED`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED`
