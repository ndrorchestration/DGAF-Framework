from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUSTODY_PATHS = (
    "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem",
    "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json",
)


def test_custody_evidence_paths_disable_git_text_normalization() -> None:
    output = subprocess.check_output(
        ["git", "check-attr", "text", "--", *CUSTODY_PATHS],
        cwd=ROOT,
        text=True,
    )

    for path in CUSTODY_PATHS:
        assert f"{path}: text: unset" in output
