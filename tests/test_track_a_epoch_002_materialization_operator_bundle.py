from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPERATOR_BUNDLE = ROOT / "scripts" / "prepare_track_a_epoch_002_operator_materialization.py"


def test_operator_materialization_bundle_helper_exists() -> None:
    assert OPERATOR_BUNDLE.is_file(), "operator materialization bundle helper is absent"
