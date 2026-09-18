from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PREPARER = ROOT / "scripts/prepare_track_a_epoch_002_materialization_receipt.py"


def test_receipt_preparer_exists_and_is_creation_only() -> None:
    source = PREPARER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    ast_constants = [node for node in ast.walk(tree) if isinstance(node, ast.Constant)]
    constants = {node.value for node in ast_constants if isinstance(node.value, str)}

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


def test_receipt_preparer_fails_closed_before_evidence_admission(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    spec = importlib.util.spec_from_file_location(
        "epoch002_materialization_receipt_preparer_test",
        PREPARER,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    monkeypatch.setattr(
        module.validator,
        "MATERIALIZATION_EVIDENCE_PATH",
        tmp_path / "missing-materialization-evidence.json",
    )
    monkeypatch.setattr(
        module.validator,
        "PRIMARY_ANALYSIS_AUTH_PATH",
        tmp_path / "missing-primary-analysis-authorization.json",
    )
    monkeypatch.setattr(
        module.validator,
        "LOCKED_ANALYSIS_RESULT_PATH",
        tmp_path / "missing-locked-analysis-result.json",
    )

    with pytest.raises(SystemExit, match="canonical materialization evidence is absent"):
        module.build_receipt("2026-09-18T15:00:00Z")


def test_receipt_preparer_write_mode_is_explicit() -> None:
    source = PREPARER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    write_mentions = [node for node in ast.walk(tree) if isinstance(node, ast.Constant) and node.value == "--write"]
    assert len(write_mentions) == 1
