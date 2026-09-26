"""The Windows operator probe must exercise refusal, not infer it from the OS."""

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.run_dgaf_operator_selftest import WINDOWS_CUSTODY_PROBE

ROOT = Path(__file__).resolve().parents[1]
UNSUPPORTED_SUBSTRATE = "import os\nif hasattr(os, 'O_NOFOLLOW'): del os.O_NOFOLLOW\n"


def run_probe(mutation=""):
    return subprocess.run(
        [sys.executable, "-c", UNSUPPORTED_SUBSTRATE + mutation + WINDOWS_CUSTODY_PROBE],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_actual_custody_refuses_missing_primitive_without_side_effects():
    result = run_probe()
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "CUSTODY_REFUSAL_VERIFIED"


@pytest.mark.parametrize(
    ("body", "error"),
    [
        ("return parent / attempt_id", "Custody accepted an unsupported substrate"),
        ("raise OSError('unrelated failure')", "Unexpected custody refusal"),
        (
            "(parent / attempt_id).mkdir(); raise OSError('O_NOFOLLOW_REQUIRED')",
            "Custody refusal left filesystem side effects",
        ),
    ],
)
def test_mutated_custody_cannot_earn_pass(body, error):
    mutation = (
        "import scripts.aoss_stage_a.custody as custody\n"
        f"def broken_reservation(parent, attempt_id):\n    {body}\n"
        "custody.reserve_synthetic_attempt = broken_reservation\n"
    )
    result = run_probe(mutation)
    assert result.returncode != 0
    assert error in result.stderr
    assert "CUSTODY_REFUSAL_VERIFIED" not in result.stdout
