#!/usr/bin/env python3
"""Fail-closed local preflight for the Track A Epoch 001 custody private key.

This command verifies that a caller-supplied private key corresponds to the
custody certificate retained inside the exact protected collection artifact.
It never prints, copies, or persists the private key and performs no CMS
decryption of the protected mapping.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import tempfile
import zipfile
from pathlib import Path

PROTECTED_ARTIFACT_ARCHIVE_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
CUSTODY_CERTIFICATE_SHA256 = "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707"
CERT_MEMBER = "track_a_epoch_001_custody_cert.pem"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Track A custody-key preflight refused: {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def openssl_bytes(args: list[str], *, stdin: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["openssl", *args],
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(completed.returncode == 0, "OpenSSL rejected the supplied key or custody certificate")
    return completed.stdout


def preflight(protected_zip: Path, private_key: Path) -> None:
    require(protected_zip.is_file(), "protected artifact ZIP missing")
    require(private_key.is_file(), "custody private key missing")
    require(
        sha256_file(protected_zip) == PROTECTED_ARTIFACT_ARCHIVE_SHA256,
        "protected artifact archive digest mismatch",
    )

    with tempfile.TemporaryDirectory(prefix="track-a-key-preflight-") as temp_name:
        root = Path(temp_name)
        with zipfile.ZipFile(protected_zip) as archive:
            names = set(archive.namelist())
            require(CERT_MEMBER in names, "custody certificate missing from protected artifact")
            cert = root / CERT_MEMBER
            cert.write_bytes(archive.read(CERT_MEMBER))

        require(sha256_file(cert) == CUSTODY_CERTIFICATE_SHA256, "custody certificate digest mismatch")

        private_public_der = openssl_bytes(
            ["pkey", "-in", str(private_key), "-pubout", "-outform", "DER"]
        )
        cert_public_pem = openssl_bytes(["x509", "-in", str(cert), "-pubkey", "-noout"])
        cert_public_der = openssl_bytes(["pkey", "-pubin", "-outform", "DER"], stdin=cert_public_pem)

        require(private_public_der == cert_public_der, "private key does not match retained custody certificate")

    print("TRACK_A_EPOCH_001_CUSTODY_KEY_PREFLIGHT=PASS")
    print("PRIVATE_KEY_PUBLISHED=FALSE")
    print("PROTECTED_MAPPING_DECRYPTED=FALSE")
    print("UNBLINDED_ANALYSIS_INPUT_MATERIALIZED=FALSE")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protected-artifact-zip", type=Path, required=True)
    parser.add_argument("--custody-private-key", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.protected_artifact_zip, args.custody_private_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
