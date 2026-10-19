"""Contract tests preventing premature matched-comparator claims."""

import copy
import json
from pathlib import Path

import pytest

from experiments.sbcf.comparator_gate import evaluate_readiness, validate_manifest

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "matched_comparator_readiness_v1.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_manifest_is_explicitly_not_ready():
    result = evaluate_readiness(load())
    assert not result.ready
    assert "matched_runtime_effect_evidence_for_all" in result.blockers
    assert "common_effect_semantics_frozen" in result.blockers
    assert "outside_operator_assigned" in result.blockers
    assert "statistics_preregistered" in result.blockers


def test_system_versions_are_exactly_bound():
    manifest = load()
    assert manifest["systems"]["sbcf"]["version"] == "97371dcd42b6cae5f88e2883d4adb24d65c5ad9f"
    assert manifest["systems"]["acs"]["version"] == "9c05f0402d76dea6b67a12a93672c2131137e572"
    assert manifest["systems"]["openshell"]["version"] == "5a7728c304b5528e954e9ae900cf21f84e1a12b1"


def test_unknown_gate_is_rejected():
    manifest = load()
    manifest["gates"]["invented_gate"] = True
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_integer_is_not_boolean_gate():
    manifest = load()
    manifest["gates"]["statistics_preregistered"] = 1
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_missing_system_is_rejected():
    manifest = load()
    del manifest["systems"]["openshell"]
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_empty_effect_boundary_is_rejected():
    manifest = load()
    manifest["systems"]["sbcf"]["effect_boundary"] = ""
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_manual_gate_flip_cannot_upgrade_nonmatched_runtime_evidence():
    manifest = load()
    for gate in manifest["gates"]:
        manifest["gates"][gate] = True

    result = evaluate_readiness(manifest)

    assert not result.ready
    assert result.blockers == (
        "matched_runtime_effect_missing:acs",
        "matched_runtime_effect_missing:sbcf",
    )


def test_reference_runtime_is_not_enforced_runtime():
    manifest = load()
    for gate in manifest["gates"]:
        manifest["gates"][gate] = True
    manifest["systems"]["sbcf"]["matched_effect_tier"] = "reference_runtime_effect"

    result = evaluate_readiness(manifest)

    assert not result.ready
    assert result.blockers == (
        "matched_runtime_effect_missing:acs",
        "matched_runtime_effect_missing:sbcf",
    )


def test_future_enforced_runtime_evidence_can_satisfy_structural_gate():
    manifest = load()
    for gate in manifest["gates"]:
        manifest["gates"][gate] = True
    manifest["systems"]["sbcf"]["matched_effect_tier"] = "enforced_runtime_effect"
    manifest["systems"]["acs"]["matched_effect_tier"] = "enforced_runtime_effect"

    result = evaluate_readiness(manifest)

    assert result.ready
    assert result.blockers == ()


def test_unreproduced_system_blocks_even_when_other_gates_true():
    manifest = load()
    for gate in manifest["gates"]:
        manifest["gates"][gate] = True
    manifest["systems"]["sbcf"]["matched_effect_tier"] = "enforced_runtime_effect"
    manifest["systems"]["acs"]["matched_effect_tier"] = "enforced_runtime_effect"
    manifest["systems"]["acs"]["reproduced"] = False

    result = evaluate_readiness(manifest)

    assert not result.ready
    assert result.blockers == ("system_not_reproduced:acs",)


def test_unexpected_system_field_is_rejected():
    manifest = load()
    manifest["systems"]["sbcf"]["independent"] = False
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_unexpected_top_level_field_is_rejected():
    manifest = load()
    manifest["claim"] = "parity"
    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_readiness_is_deterministic():
    manifest = load()
    assert evaluate_readiness(manifest) == evaluate_readiness(copy.deepcopy(manifest))
