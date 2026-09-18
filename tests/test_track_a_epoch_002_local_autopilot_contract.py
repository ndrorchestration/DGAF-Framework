from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "scripts/run_track_a_epoch_002_local_autopilot.py"
POWERSHELL = ROOT / "scripts/run_track_a_epoch_002_local_autopilot.ps1"
EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"


def source_and_tree() -> tuple[str, ast.Module]:
    source = AUTOPILOT.read_text(encoding="utf-8")
    return source, ast.parse(source)


def string_constants(tree: ast.AST) -> set[str]:
    return {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def test_autopilot_stops_at_evidence_admission_boundary() -> None:
    source, tree = source_and_tree()
    strings = string_constants(tree)

    assert "--validate-evidence-admission" in strings
    assert "--validate-receipt-event" not in strings
    assert "pr merge" not in source.lower()
    assert "primary_analysis=not_authorized_not_run" in source.lower()


def test_autopilot_uses_exact_canonical_evidence_path() -> None:
    _, tree = source_and_tree()
    strings = string_constants(tree)

    assert EVIDENCE_REL in strings or "docs/experiment/track_a_runs/" in strings


def test_autopilot_invokes_bounded_bridge_actions() -> None:
    _, tree = source_and_tree()
    actions: set[str] = set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "dispatch":
            continue
        if len(node.args) != 1 or not isinstance(node.args[0], ast.Dict):
            continue
        request = node.args[0]
        if len(request.keys) != 1:
            continue
        key = request.keys[0]
        value = request.values[0]
        if (
            isinstance(key, ast.Constant)
            and key.value == "action"
            and isinstance(value, ast.Constant)
            and isinstance(value.value, str)
        ):
            actions.add(value.value)

    assert actions == {"verify_inputs", "materialize", "get_evidence"}


def test_autopilot_pr_is_draft_and_one_file_guarded() -> None:
    source, _ = source_and_tree()

    assert '"--draft"' in source
    assert "if staged != [EVIDENCE_REL]:" in source
    assert "if latest != baseline:" in source


def test_powershell_wrapper_only_bootstraps_and_invokes_python() -> None:
    source = POWERSHELL.read_text(encoding="utf-8").lower()

    assert "run_track_a_epoch_002_local_autopilot.py" in source
    assert "git push" not in source
    assert "gh pr" not in source
    assert "materialization_receipt" not in source
