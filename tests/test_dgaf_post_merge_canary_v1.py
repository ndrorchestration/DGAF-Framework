from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts/run_dgaf_post_merge_canary_v1.py"


def load_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dgaf_post_merge_canary_v1_runner", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def smoke_result(revision: str, outcome: str = "PASS") -> dict[str, object]:
    return {
        "schema": "dgaf.smoke.v1",
        "revision": revision,
        "outcome": outcome,
        "gates": {},
        "boundary": {},
    }


def test_canary_passes_only_when_all_composed_checks_pass():
    runner = load_runner()
    result = runner.build_result(
        expected_revision="abc123",
        actual_revision="abc123",
        predecessor="def456",
        smoke_result=smoke_result("abc123"),
        head_binding_returncode=0,
        head_binding_output="control-state HEAD reconciliation: PASS",
    )

    assert result["outcome"] == "PASS"
    assert all(gate["outcome"] == "PASS" for gate in result["gates"].values())


def test_canary_fails_on_smoke_revision_mismatch():
    runner = load_runner()
    result = runner.build_result(
        expected_revision="abc123",
        actual_revision="abc123",
        predecessor="def456",
        smoke_result=smoke_result("wrong-revision"),
        head_binding_returncode=0,
        head_binding_output="control-state HEAD reconciliation: PASS",
    )

    assert result["outcome"] == "FAIL"
    assert result["gates"]["CANARY_SMOKE"]["outcome"] == "FAIL"


def test_canary_fails_on_control_state_reconciliation_failure():
    runner = load_runner()
    result = runner.build_result(
        expected_revision="abc123",
        actual_revision="abc123",
        predecessor="def456",
        smoke_result=smoke_result("abc123"),
        head_binding_returncode=1,
        head_binding_output="control-state reconciliation drift",
    )

    assert result["outcome"] == "FAIL"
    assert result["gates"]["CANARY_CONTROL_STATE"]["outcome"] == "FAIL"


def test_canary_preserves_nonpromoting_boundary():
    runner = load_runner()
    result = runner.build_result(
        expected_revision="abc123",
        actual_revision="abc123",
        predecessor="def456",
        smoke_result=smoke_result("abc123"),
        head_binding_returncode=0,
        head_binding_output="PASS",
    )

    assert result["boundary"] == {
        "scientific_n_increment": 0,
        "authorization_effect": "NONE",
        "deployment_health": "NOT_ESTABLISHED",
        "production_readiness": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
