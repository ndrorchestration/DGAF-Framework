from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts" / "materialize_track_a_epoch_002_unblinded_input.py"


def test_accepted_materializer_path_exists() -> None:
    assert MATERIALIZER.is_file(), "accepted Stage-1 materializer path is absent"
