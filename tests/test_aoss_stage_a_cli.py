import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_aoss_v0_6_stage_a.py"


def test_collect_is_disabled(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(CLI), "collect"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "COLLECTION_IMPLEMENTATION_NOT_ACCEPTED" in completed.stderr
    assert list(tmp_path.iterdir()) == []
