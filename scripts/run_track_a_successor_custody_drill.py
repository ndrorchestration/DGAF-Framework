#!/usr/bin/env python3
"""Local-only Track A successor custody setup and recovery drill.

Run this only on the operator's own computer. It creates an encrypted private
key locally, never prints or uploads it, copies the encrypted container to two
operator-chosen directories, verifies recovery from backup A, and emits a
non-secret receipt. It does not authorize collection or establish efficacy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(message: str) -> None:
    raise RuntimeError(message)


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_distinct(*paths: Path) -> None:
    resolved = [path.resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        fail("output and backup directories must be distinct")
    for index, path in enumerate(resolved):
        for other in resolved[index + 1 :]:
            if path in other.parents or other in path.parents:
                fail("output and backup directories must not contain one another")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a local encrypted custody key and prove backup recovery."
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--backup-a", required=True, type=Path)
    parser.add_argument("--backup-b", required=True, type=Path)
    parser.add_argument("--backup-a-id", default="recovery-copy-a")
    parser.add_argument("--backup-b-id", default="recovery-copy-b")
    parser.add_argument(
        "--subject",
        default="/CN=DGAF Track A Successor Custody",
        help="public certificate subject only; do not put personal secrets here",
    )
    args = parser.parse_args()

    if shutil.which("openssl") is None:
        fail("OpenSSL is required but was not found on PATH")

    output = args.output_dir.expanduser().resolve()
    backup_a = args.backup_a.expanduser().resolve()
    backup_b = args.backup_b.expanduser().resolve()
    ensure_distinct(output, backup_a, backup_b)

    for directory in (output, backup_a, backup_b):
        directory.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        fail(f"output directory must be empty: {output}")

    encrypted_key = output / "track_a_successor_private_key_encrypted.pem"
    certificate = output / "track_a_successor_custody_cert.pem"
    receipt = output / "track_a_successor_solo_custody_receipt.json"
    backup_name = encrypted_key.name
    backup_a_key = backup_a / backup_name
    backup_b_key = backup_b / backup_name

    if backup_a_key.exists() or backup_b_key.exists():
        fail("refusing to overwrite an existing backup key file")

    # OpenSSL prompts directly for a passphrase; this program never receives it.
    run(
        "openssl", "genpkey", "-algorithm", "RSA", "-aes-256-cbc",
        "-pkeyopt", "rsa_keygen_bits:3072", "-out", str(encrypted_key),
    )
    run(
        "openssl", "req", "-new", "-x509", "-key", str(encrypted_key),
        "-out", str(certificate), "-days", "3650", "-subj", args.subject,
    )

    shutil.copy2(encrypted_key, backup_a_key)
    shutil.copy2(encrypted_key, backup_b_key)

    # Recovery drill: derive public DER from recovered backup A and certificate.
    with tempfile.TemporaryDirectory(prefix="dgaf-custody-recovery-") as tmp:
        tmp_path = Path(tmp)
        recovered = tmp_path / backup_name
        shutil.copy2(backup_a_key, recovered)
        recovered_der = tmp_path / "recovered-public.der"
        certificate_pem = tmp_path / "certificate-public.pem"
        certificate_der = tmp_path / "certificate-public.der"

        run("openssl", "pkey", "-in", str(recovered), "-pubout", "-outform", "DER", "-out", str(recovered_der))
        run("openssl", "x509", "-in", str(certificate), "-pubkey", "-noout", "-out", str(certificate_pem))
        run("openssl", "pkey", "-pubin", "-in", str(certificate_pem), "-pubout", "-outform", "DER", "-out", str(certificate_der))

        recovered_digest = sha256_file(recovered_der)
        certificate_public_digest = sha256_file(certificate_der)
        if recovered_digest != certificate_public_digest:
            fail("recovery drill failed: recovered backup does not match certificate")

    payload = {
        "record_type": "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "schema_version": 1,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "keypair_created_before_collection": True,
        "private_key_in_repository": False,
        "private_key_in_notion": False,
        "private_key_in_chat": False,
        "encrypted_private_key_sha256": sha256_file(encrypted_key),
        "certificate_sha256": sha256_file(certificate),
        "certificate_public_key_der_sha256": certificate_public_digest,
        "recovered_public_key_der_sha256": recovered_digest,
        "recovery_drill": "PASS",
        "backup_refs": [
            {"class": "ENCRYPTED_LOCAL_ARCHIVE", "nonsecret_id": args.backup_a_id, "encrypted": True, "user_controlled": True},
            {"class": "ENCRYPTED_OFFSITE_ARCHIVE", "nonsecret_id": args.backup_b_id, "encrypted": True, "user_controlled": True},
        ],
        "empirical_collection_authorized": False,
        "scientific_state_effect": "NONE",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    receipt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    run(sys.executable, "scripts/validate_track_a_successor_solo_custody_receipt.py", str(receipt))

    print("LOCAL_CUSTODY_SETUP=PASS")
    print(f"PUBLIC_CERTIFICATE={certificate}")
    print(f"NONSECRET_RECEIPT={receipt}")
    print("Keep every encrypted private-key copy and its passphrase out of GitHub, Notion, chat, and CI.")
    print("This drill does not authorize empirical collection.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"LOCAL_CUSTODY_SETUP=FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
