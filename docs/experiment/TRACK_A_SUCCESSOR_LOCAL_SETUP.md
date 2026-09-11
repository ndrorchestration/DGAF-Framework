# Local Track A Successor Custody Setup

**Status:** local recovery-test tooling only. Running it does **not** authorize collection.

You do not need an existing key. This guide creates a new encrypted key on your own computer and proves that both backups can recover it.

The successor Epoch 002 prospective protocol is now present in the repository, but the real custody drill remains a separate precollection requirement. No private key, passphrase, or recoverable secret material belongs in GitHub, Notion, chat, CI, or workflow inputs.

## Before you begin

Choose three different locations you control:

1. an empty working folder on your computer;
2. encrypted recovery location A (for example, an encrypted USB drive);
3. encrypted recovery location B in a different storage class (for example, a separately encrypted archive you control).

Do not use the repository folder for any of them. The custody script rejects repository-contained output or backup paths. Do not use a chat upload, Notion, GitHub, workflow secret, or public document as a custody location.

## Windows guided path

From a local clone of `DGAF-Framework`, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_track_a_successor_custody_drill.ps1
```

If PowerShell 7 is installed, `pwsh` may be used instead of `powershell.exe`.

The wrapper:

- finds Python 3 through `py -3` or `python`;
- finds OpenSSL on `PATH` or in common Git-for-Windows locations;
- creates a fresh timestamped working folder by default;
- prompts for the two non-secret recovery-location paths and their actual storage classes;
- never requests the key passphrase itself;
- lets OpenSSL prompt for the passphrase directly;
- invokes the repository custody drill and current receipt validator;
- prints only the public certificate and non-secret receipt paths when successful.

The two recovery locations must be genuinely distinct storage classes. Two folders on the same unencrypted disk do not satisfy the intended recovery model.

You can validate that the wrapper and prerequisites are present without creating any key:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_track_a_successor_custody_drill.ps1 -ValidateOnly
```

`-ValidateOnly` performs no secret generation and has no scientific or authorization effect.

## Direct Python path

On macOS, Linux, or any environment where Python 3 and OpenSSL are already available, run from a local clone:

```bash
python3 scripts/run_track_a_successor_custody_drill.py \
  --output-dir "$HOME/DGAF-Custody-Working" \
  --backup-a "/path/to/encrypted-recovery-A" \
  --backup-b "/path/to/encrypted-recovery-B" \
  --backup-a-class ENCRYPTED_REMOVABLE_ARCHIVE \
  --backup-b-class ENCRYPTED_OFFSITE_ARCHIVE
```

OpenSSL will ask you to create and confirm a passphrase. Use a strong unique passphrase and keep it in a password manager or a separate secure record you control. Do not send it to anyone or paste it into a command.

The command creates:

- an encrypted private-key file in the working folder;
- two encrypted copies with the same filename in the two backup locations;
- a public certificate file; and
- a non-secret JSON recovery receipt.

It reads back **both** encrypted backups, checks their exact container hashes, and separately derives each recovered public key for comparison with the collection certificate. OpenSSL may prompt repeatedly; this is expected. A failure for either backup prevents publication of the final receipt.

The emitted current receipt is schema v2. It includes a timezone-qualified recovery timestamp and separate fingerprints/PASS records for both backups. The current validator requires schema v2 for the Epoch 002 successor gate; a legacy schema-v1 receipt may be inspected only through the explicit historical compatibility function and cannot satisfy the current precollection prerequisite.

The local validator checks receipt structure; it does not independently observe storage durability or offsite location. Those remain your attestations. The helper can be launched by absolute path from another directory. If interrupted, keep existing encrypted backups intact and choose fresh empty working/backup destinations for another setup attempt; the script refuses to overwrite backup key files.

## After a successful schema-v2 drill

If the real operator-local drill has already returned `TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECEIPT=PASS_CURRENT_V2` and `TRACK_A_SUCCESSOR_WINDOWS_CUSTODY=PASS_LOCAL`, do not rerun the drill merely to recreate repository evidence.

Preserve the encrypted private key, passphrase, and both encrypted recovery copies unchanged in their operator-controlled locations. Only the exact public certificate and exact non-secret schema-v2 receipt emitted by that successful run are eligible for repository admission.

The canonical repository destinations are:

- `docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem`
- `docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json`

These two paths are configured as Git byte-preserving (`-text`) because the receipt binds the certificate's exact SHA-256. Platform line-ending normalization must not alter the admitted evidence.

Custody evidence admission is a two-file, non-authorizing transition. Do not include a preflight, freeze, closure, collection-authorization record, private key, encrypted backup, passphrase, or blinding secret in the custody-admission commit.

A successful custody-admission validation changes only repository custody-evidence status. It does not authorize collection, does not establish independent custody, and does not change scientific N.

## What you may retain or share

The public certificate and the JSON receipt contain no private key or passphrase. The current successor receipt can be checked with:

```bash
python3 scripts/validate_track_a_successor_solo_custody_receipt.py \
  "$HOME/DGAF-Custody-Working/track_a_successor_solo_custody_receipt.json"
```

Only the public certificate and non-secret receipt are eligible for later repository review. Do **not** commit the encrypted private-key file or either recovery copy.

After this drill passes, successor collection is still not automatically authorized. The project must separately bind the accepted custody receipt and public certificate into the later candidate, review, freeze, and explicit collection-authorization sequence.

OpenSSL's [genpkey documentation](https://docs.openssl.org/3.6/man1/openssl-genpkey/) describes local keypair generation; its [PKCS#8 documentation](https://docs.openssl.org/3.5/man1/openssl-pkcs8/) describes encrypted password-protected private-key containers.
