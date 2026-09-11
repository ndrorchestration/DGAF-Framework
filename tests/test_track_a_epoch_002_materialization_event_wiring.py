from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_track_a_epoch_002_materialization.py"


def test_validate_event_requires_dataset_lock_evidence_argument() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--validate-event",
            "--evidence",
            "materialization-evidence.json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "--dataset-lock-evidence" in (result.stdout + result.stderr)
