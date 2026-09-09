# Local Track A Successor Custody Setup

**Status:** local recovery-test tooling only. Running it does **not** authorize collection.

You do not need an existing key. This guide creates a new encrypted key on your own computer and proves that one backup can recover it.

## Before you begin

Choose three different locations you control:

1. an empty working folder on your computer;
2. encrypted recovery location A (for example, an encrypted USB drive);
3. encrypted recovery location B in a different storage class (for example, an encrypted archive you control).

Do not use the repository folder for any of them. Do not use a chat upload, Notion, GitHub, workflow secret, or public cloud document.

## Run

From a local clone of DGAF-Framework:

```bash
python3 scripts/run_track_a_successor_custody_drill.py \
  --output-dir "$HOME/DGAF-Custody-Working" \
  --backup-a "/path/to/encrypted-recovery-A" \
  --backup-b "/path/to/encrypted-recovery-B"
```

OpenSSL will ask you to create and confirm a passphrase. Use a strong unique passphrase and keep it in a password manager or a separate secure record you control. Do not send it to anyone or paste it into a command.

The command will create:

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

Do **not** commit the encrypted private-key file or its copies. Before any future collection, the project still needs the separate prospective protocol, candidate, custody review, freeze, and explicit authorization gates.

OpenSSL's [genpkey documentation](https://docs.openssl.org/3.6/man1/openssl-genpkey/) describes local keypair generation; its [PKCS#8 documentation](https://docs.openssl.org/3.5/man1/openssl-pkcs8/) describes encrypted password-protected private-key containers.
