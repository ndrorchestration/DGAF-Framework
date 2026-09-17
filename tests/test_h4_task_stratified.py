from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "pptl/experiments/h4_task_stratified.py"


def load_h4():
    package = types.ModuleType("pptl")
    package.__path__ = [str(ROOT / "pptl")]
    topology = types.ModuleType("pptl.topology")
    topology.PHI = (1 + 5**0.5) / 2

    previous_package = sys.modules.get("pptl")
    previous_topology = sys.modules.get("pptl.topology")
    sys.modules["pptl"] = package
    sys.modules["pptl.topology"] = topology
    try:
        spec = importlib.util.spec_from_file_location("h4_task_stratified_test_module", MODULE_PATH)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if previous_package is None:
            sys.modules.pop("pptl", None)
        else:
            sys.modules["pptl"] = previous_package
        if previous_topology is None:
            sys.modules.pop("pptl.topology", None)
        else:
            sys.modules["pptl.topology"] = previous_topology


h4 = load_h4()


def summary_rows(
    *,
    task1: tuple[float, float, float] = (0.680, 0.672, 0.683),
    task2: tuple[float, float, float] = (0.671, 0.668, 0.674),
    task3: tuple[float, float, float] = (0.631, 0.628, 0.695),
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task, values in (
        ("task1_analytical", task1),
        ("task2_creative", task2),
        ("task3_adversarial", task3),
    ):
        for mode, value in zip(h4.MODES, values, strict=True):
            rows.append(
                {
                    "mode": mode,
                    "task": task,
                    "noise": 0.30,
                    "mean_composite": value,
                    "n": 20,
                }
            )
    return rows


def test_h4_full_verdict_requires_task1_and_task2_non_dominance(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(h4, "OUTPUT_DIR", tmp_path)

    verdict = h4.evaluate_h4(summary_rows())

    assert "H4-Part1 (C > A,B on TASK3): CONFIRMED" in verdict
    assert "H4-Part2 (C not dominant on TASK1/TASK2): CONFIRMED" in verdict
    assert "H4 FULL VERDICT: CONFIRMED" in verdict


def test_h4_rejects_task2_specific_dominance(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(h4, "OUTPUT_DIR", tmp_path)

    verdict = h4.evaluate_h4(summary_rows(task2=(0.60, 0.61, 0.70)))

    assert "H4-Part1 (C > A,B on TASK3): CONFIRMED" in verdict
    assert "H4-Part2 (C not dominant on TASK1/TASK2): REJECTED" in verdict
    assert "H4 FULL VERDICT: PARTIAL" in verdict


def test_h4_checks_both_comparison_triads_for_non_dominance(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(h4, "OUTPUT_DIR", tmp_path)

    verdict = h4.evaluate_h4(summary_rows(task1=(0.69, 0.60, 0.70)))

    assert "H4-Part2 (C not dominant on TASK1/TASK2): REJECTED" in verdict
    assert "H4 FULL VERDICT: PARTIAL" in verdict


def test_h4_missing_required_cell_fails_closed(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(h4, "OUTPUT_DIR", tmp_path)
    summary = [row for row in summary_rows() if not (row["mode"] == "triad_b" and row["task"] == "task2_creative")]

    with pytest.raises(ValueError, match="missing H4 summary cell"):
        h4.evaluate_h4(summary)

    assert not (tmp_path / "h4_verdict.txt").exists()
