from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPARER = ROOT / "scripts/prepare_track_a_epoch_002_materialization_receipt.py"


def test_receipt_preparer_exists_and_is_creation_only() -> None:
    source = PREPARER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    constants = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)}

    assert "--write" in constants
    assert "TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json" in source
    assert "expected_receipt" in source
    assert "validate_receipt_object" in source
    assert "validate_no_analysis_successor" in source
    assert "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN" in source

    lowered = source.lower()
    for forbidden in (
        "private_key",
        "passphrase",
        "blinding_secret",
        "run_primary_analysis",
        "primary_analysis_authorized=true",
        "pr merge",
        "gh pr merge",
    ):
        assert forbidden not in lowered


def test_receipt_preparer_fails_closed_before_evidence_admission() -> None:
    result = subprocess.run(
        [sys.executable, str(PREPARER)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "canonical materialization evidence is absent" in combined


def test_receipt_preparer_write_mode_is_explicit() -> None:
    source = PREPARER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    write_mentions = [node for node in ast.walk(tree) if isinstance(node, ast.Constant) and node.value == "--write"]
    assert len(write_mentions) == 1
