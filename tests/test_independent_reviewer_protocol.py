"""Tests for the independent reviewer execution protocol."""

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/run_independent_reviewer_protocol.py"

spec = importlib.util.spec_from_file_location("independent_reviewer_protocol", MODULE_PATH)
assert spec and spec.loader
protocol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(protocol)


def test_classify_reproduced_requires_all_frozen_checks() -> None:
    assert (
        protocol.classify_result(
            commit_matches=True,
            tests_returncode=0,
            bundle_matches=True,
        )
        == "REPRODUCED"
    )


def test_classify_mismatch_preserves_negative_result() -> None:
    assert (
        protocol.classify_result(
            commit_matches=True,
            tests_returncode=1,
            bundle_matches=True,
        )
        == "MISMATCH"
    )
    assert (
        protocol.classify_result(
            commit_matches=True,
            tests_returncode=0,
            bundle_matches=False,
        )
        == "MISMATCH"
    )


def test_classify_blocked_on_identity_or_execution_blocker() -> None:
    assert (
        protocol.classify_result(
            commit_matches=False,
            tests_returncode=None,
            bundle_matches=None,
        )
        == "BLOCKED"
    )
    assert (
        protocol.classify_result(
            commit_matches=True,
            tests_returncode=None,
            bundle_matches=None,
            blocker="dependency unavailable",
        )
        == "BLOCKED"
    )


def test_creation_only_record_refuses_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "record.json"
    protocol.creation_only_write(path, {"status": "BLOCKED"})
    first = path.read_bytes()

    try:
        protocol.creation_only_write(path, {"status": "REPRODUCED"})
    except FileExistsError:
        pass
    else:
        raise AssertionError("creation-only reviewer record unexpectedly allowed overwrite")

    assert path.read_bytes() == first
    assert json.loads(first)["status"] == "BLOCKED"


def test_protocol_covers_complete_current_handoff_suite() -> None:
    expected = {
        "tests/test_governance_benchmark_review_bundle.py",
        "tests/test_governance_benchmark_strong_policy.py",
        "tests/test_governance_benchmark_semantic_equivalence.py",
        "tests/test_governance_benchmark_configuration_scaling.py",
        "tests/test_governance_benchmark_recovery_composition.py",
        "tests/test_governance_benchmark_provenance_custody.py",
        "tests/test_standards_risk_crosswalk.py",
    }
    assert expected.issubset(set(protocol.TEST_PATHS))
