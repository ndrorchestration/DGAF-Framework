from pathlib import Path

import pytest

from scripts import run_track_a_successor_custody_drill as drill

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "run_track_a_successor_custody_drill.ps1"


def test_custody_paths_inside_repository_fail_closed() -> None:
    with pytest.raises(RuntimeError, match="outside the repository"):
        drill.ensure_outside_repository(ROOT / "unsafe-custody")


def test_external_custody_path_is_allowed(tmp_path: Path) -> None:
    drill.ensure_outside_repository(tmp_path / "working")


def test_windows_wrapper_preserves_secret_boundary() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    assert "run_track_a_successor_custody_drill.py" in text
    assert "validate_track_a_successor_solo_custody_receipt.py" in text
    assert "-ValidateOnly" not in text  # switch is declared as $ValidateOnly, not passed to secret tooling
    assert "$ValidateOnly" in text
    assert "SECRET_GENERATION=FALSE" in text
    assert "EMPIRICAL_COLLECTION_AUTHORIZED=FALSE" in text
    assert "--output-dir" in text
    assert "--backup-a" in text
    assert "--backup-b" in text
    assert "--passphrase" not in text
    assert "PDMAL_BLINDING_KEY" not in text
    assert "Read-Host" in text
    assert "Git\\usr\\bin\\openssl.exe" in text


def test_windows_wrapper_executes_receipt_validator() -> None:
    text = WRAPPER.read_text(encoding="utf-8")
    assert "$validatorArguments += $ReceiptValidator" in text
    assert "$validatorArguments += $receipt" in text
    assert "& $pythonCommand.Exe @validatorArguments" in text
    assert "The custody receipt validator failed" in text


def test_windows_wrapper_does_not_embed_secret_material() -> None:
    lowered = WRAPPER.read_text(encoding="utf-8").lower()
    forbidden_assignments = (
        "private_key=",
        "blinding_key=",
        "passphrase=",
        "password=",
    )
    assert not any(token in lowered for token in forbidden_assignments)
