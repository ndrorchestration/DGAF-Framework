from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_dataset_lock.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_dataset_lock_protected_sidecars", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def _write_sidecar(path: Path, digest: str, target_name: str) -> None:
    path.write_text(f"{digest}  {target_name}\n", encoding="utf-8")


def test_protected_root_accepts_canonical_retained_sidecar_names(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "protected"
    root.mkdir()

    ciphertext = root / "track_a_epoch_002_protected.cms"
    ciphertext.write_bytes(b"ciphertext-fixture")
    ciphertext_digest = hashlib.sha256(ciphertext.read_bytes()).hexdigest()
    _write_sidecar(
        root / "track_a_epoch_002_protected_ciphertext.sha256",
        ciphertext_digest,
        ciphertext.name,
    )

    certificate = root / "track_a_epoch_002_custody_cert.pem"
    certificate.write_bytes(b"certificate-fixture")
    certificate_digest = hashlib.sha256(certificate.read_bytes()).hexdigest()
    _write_sidecar(
        root / "track_a_epoch_002_custody_cert.sha256",
        certificate_digest,
        certificate.name,
    )

    plaintext_digest = "6" * 64
    _write_sidecar(
        root / "track_a_epoch_002_protected_plaintext_tar.sha256",
        plaintext_digest,
        "track_a_epoch_002_protected.tar",
    )

    public_key_digest = "8" * 64
    monkeypatch.setattr(
        validator,
        "certificate_public_key_der_sha256",
        lambda _path: public_key_digest,
    )

    evidence = {
        "protected_artifact": {
            "ciphertext_sha256": ciphertext_digest,
            "plaintext_tar_sha256": plaintext_digest,
            "custody_certificate_sha256": certificate_digest,
            "custody_certificate_public_key_der_sha256": public_key_digest,
        }
    }

    validator.validate_protected_root(root, evidence)
