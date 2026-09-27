from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts/run_dgaf_smoke_v1.py"

pytest.importorskip("pandas")


def load_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dgaf_smoke_v1_runner", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dgaf_smoke_v1_passes_all_required_gates(monkeypatch):
    runner = load_runner()
    monkeypatch.setenv("DGAF_REVISION", "test-revision")
    result = runner.run_smoke()

    assert result["schema"] == runner.SCHEMA
    assert result["revision"] == "test-revision"
    assert result["outcome"] == "PASS"
    assert set(result["gates"]) == {
        "SMOKE_BOOT",
        "SMOKE_ROUTE",
        "SMOKE_EXECUTE",
        "SMOKE_PROVENANCE",
        "SMOKE_DENY",
        "SMOKE_STATE",
    }
    assert all(gate["outcome"] == "PASS" for gate in result["gates"].values())


def test_dgaf_smoke_v1_preserves_nonempirical_boundary():
    runner = load_runner()
    result = runner.run_smoke()

    assert result["fixtures"] == {
        "allow": runner.FIXTURES["allow"],
        "deny": runner.FIXTURES["deny"],
        "ambiguous": runner.FIXTURES["ambiguous"],
    }
    assert result["boundary"] == {
        "scientific_n_increment": 0,
        "authorization_effect": "NONE",
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def test_dgaf_smoke_v1_emits_machine_readable_result(tmp_path, monkeypatch):
    runner = load_runner()
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        ["run_dgaf_smoke_v1.py", "--output", str(output)],
    )

    assert runner.main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"] == runner.SCHEMA
    assert payload["outcome"] == "PASS"
    assert payload["gates"]["SMOKE_DENY"]["rejected"] is True
    assert payload["gates"]["SMOKE_STATE"]["promotion_blocked"] is True
