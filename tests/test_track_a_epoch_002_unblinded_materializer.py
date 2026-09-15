from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts" / "materialize_track_a_epoch_002_unblinded_input.py"


def test_accepted_materializer_path_exists() -> None:
    assert MATERIALIZER.is_file(), "accepted Stage-1 materializer path is absent"


def test_source_preserves_operator_secret_and_analysis_boundary() -> None:
    text = MATERIALIZER.read_text(encoding="utf-8")
    assert "--custody-private-key" in text
    assert "--passphrase" not in text
    assert "--private-key-passphrase" not in text
    assert "track_a_epoch_002_analysis" not in text
    assert "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN" in text
