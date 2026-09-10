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


def test_each_backup_is_recovered(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    key = tmp_path / "encrypted.pem"
    key.write_bytes(b"synthetic-container")
    backups = (tmp_path / "a.pem", tmp_path / "b.pem")
    for backup in backups:
        backup.write_bytes(key.read_bytes())
    calls = []

    def fake_run(*args: str, **kwargs: object) -> None:
        calls.append(args)
        Path(args[args.index("-out") + 1]).write_bytes(b"synthetic-public-identity")

    monkeypatch.setattr(drill, "run", fake_run)
    results = drill.verify_backups(tmp_path / "cert.pem", key, backups)
    assert len(results) == 2
    assert all(result["recovery_drill"] == "PASS" for result in results)
    recoveries = [call for call in calls if "-in" in call and "recovered-" in call[call.index("-in") + 1]]
    assert len(recoveries) == 2


@pytest.mark.parametrize("failure", ["encrypted_bytes", "public_identity"])
def test_bad_second_backup_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str) -> None:
    key = tmp_path / "encrypted.pem"
    key.write_bytes(b"synthetic-container")
    backups = (tmp_path / "a.pem", tmp_path / "b.pem")
    for backup in backups:
        backup.write_bytes(key.read_bytes())
    if failure == "encrypted_bytes":
        backups[1].write_bytes(b"corrupt-container")

    def fake_run(*args: str, **kwargs: object) -> None:
        output = Path(args[args.index("-out") + 1])
        output.write_bytes(b"wrong-identity" if output.name == "recovered-1.der" else b"public-identity")

    monkeypatch.setattr(drill, "run", fake_run)
    with pytest.raises(RuntimeError, match="backup 2"):
        drill.verify_backups(tmp_path / "cert.pem", key, backups)


def test_local_setup_from_unrelated_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    import sys

    output = tmp_path / "working"
    backup_a = tmp_path / "a"
    backup_b = tmp_path / "b"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(drill.shutil, "which", lambda name: "/synthetic/openssl")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "custody-drill",
            "--output-dir",
            str(output),
            "--backup-a",
            str(backup_a),
            "--backup-b",
            str(backup_b),
            "--backup-a-class",
            "ENCRYPTED_REMOVABLE_ARCHIVE",
            "--backup-b-class",
            "ENCRYPTED_OFFSITE_ARCHIVE",
        ],
    )
    real_run = drill.run

    def fake_crypto(*args: str, **kwargs: object) -> None:
        if args[0] == sys.executable:
            assert Path(args[1]).is_absolute()
            real_run(*args)
        else:
            Path(args[args.index("-out") + 1]).write_bytes(b"synthetic-test-data-not-a-key")

    monkeypatch.setattr(drill, "run", fake_crypto)
    assert drill.main() == 0
    receipt = json.loads((output / "track_a_successor_solo_custody_receipt.json").read_text())
    assert receipt["schema_version"] == 2
    assert len(receipt["backup_refs"]) == 2
    assert receipt["empirical_collection_authorized"] is False
    assert not list(output.glob("*.pending.json"))
