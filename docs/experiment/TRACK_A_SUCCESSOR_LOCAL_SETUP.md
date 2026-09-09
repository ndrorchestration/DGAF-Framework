# Local Track A Successor Custody Setup

**Status:** local recovery-test tooling only. Running it does **not** authorize collection.

You do not need an existing key. This guide creates a new encrypted key on your own computer and proves that one backup can recover it.

The successor Epoch 002 prospective protocol is now present in the repository, but the real custody drill remains a separate precollection requirement. No private key, passphrase, or recoverable secret material belongs in GitHub, Notion, chat, CI, or workflow inputs.

## Before you begin

Choose three different locations you control:

1. an empty working folder on your computer;
2. encrypted recovery location A (for example, an encrypted USB drive);
3. encrypted recovery location B in a different storage class (for example, a separately encrypted archive you control).

Do not use the repository folder for any of them. The custody script now rejects repository-contained output or backup paths. Do not use a chat upload, Notion, GitHub, workflow secret, or public document as a custody location.

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
- prompts you only for the two non-secret recovery-location paths;
- never requests the key passphrase itself;
- lets OpenSSL prompt for the passphrase directly;
- invokes the repository custody drill and receipt validator;
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
  --backup-b "/path/to/encrypted-recovery-B"
```

OpenSSL will ask you to create and confirm a passphrase. Use a strong unique passphrase and keep it in a password manager or a separate secure record you control. Do not send it to anyone or paste it into a command.

The command creates:

- an encrypted private-key file in the working folder;
- two encrypted copies with the same filename in the two backup locations;
- a public certificate file; and
- a non-secret JSON recovery receipt.

It then proves that the private key recovered from backup A derives exactly the same public key as the certificate.

## What you may retain or share

The public certificate and the JSON receipt contain no private key or passphrase. The receipt can be checked with:

```bash
python3 scripts/validate_track_a_successor_solo_custody_receipt.py \
  "$HOME/DGAF-Custody-Working/track_a_successor_solo_custody_receipt.json"
```

Only the public certificate and non-secret receipt are eligible for later repository review. Do **not** commit the encrypted private-key file or either recovery copy.

After this drill passes, successor collection is still not automatically authorized. The project must separately bind the accepted custody receipt and public certificate into the later candidate, review, freeze, and explicit collection-authorization sequence.

OpenSSL's [genpkey documentation](https://docs.openssl.org/3.6/man1/openssl-genpkey/) describes local keypair generation; its [PKCS#8 documentation](https://docs.openssl.org/3.5/man1/openssl-pkcs8/) describes encrypted password-protected private-key containers.
