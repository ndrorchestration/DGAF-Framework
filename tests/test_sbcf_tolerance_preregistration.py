"""Closed-schema tests for prospective distribution-free calibration count."""

import json
from fractions import Fraction
from pathlib import Path

import pytest

from experiments.sbcf.tolerance_preregistration import (
    evaluate_tolerance_preregistration,
    minimum_positive_control_samples,
    tolerance_preregistration_digest,
    validate_tolerance_preregistration,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "tolerance_preregistration_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def mock_frozen(coverage="0.95", confidence="0.95"):
    """A hypothetical test fixture; never a real registration or study target."""
    contract = load()
    contract["status"] = "FROZEN"
    contract["target"] = {
        "status": "PROSPECTIVELY_SELECTED",
        "coverage_p": coverage,
        "confidence_gamma": confidence,
        "scientific_rationale": "Hypothetical unit-test target only, not a research selection",
    }
    contract["sampling_assumptions"] = {
        **contract["sampling_assumptions"],
        "status": "DOCUMENTED_UNVERIFIED",
        "sampling_design_id": "hypothetical-test-design-not-verified",
    }
    n = minimum_positive_control_samples(coverage, confidence)
    contract["sample_plan"].update({"samples_per_system": n, "maximum_allowed_samples": n})
    return contract


def test_unselected_targets_and_no_samples_remain_not_ready():
    result = evaluate_tolerance_preregistration(load())
    assert not result.ready
    assert result.blockers == (
        "coverage_confidence_target_unselected",
        "sample_budget_unset",
        "sample_count_unset",
        "sampling_design_unassessed",
        "tolerance_preregistration_not_frozen",
    )


@pytest.mark.parametrize(
    ("coverage", "confidence", "expected"),
    [
        ("0.5", "0.5", 1),
        ("0.9", "0.9", 22),
        ("0.95", "0.95", 59),
        ("0.99", "0.95", 299),
        ("0.99", "0.99", 459),
    ],
)
def test_minimum_sample_count_matches_exact_one_sided_maximum(coverage, confidence, expected):
    n = minimum_positive_control_samples(coverage, confidence)
    assert n == expected
    p = Fraction(coverage)
    gamma = Fraction(confidence)
    assert p**n <= 1 - gamma
    if n > 1:
        assert p ** (n - 1) > 1 - gamma


@pytest.mark.parametrize(
    "invalid",
    [0.95, True, "0", "1", "0.000000", "1.0", ".95", "0.1234567", "0.5foo", "nan", None],
)
def test_noncanonical_or_out_of_range_targets_rejected(invalid):
    with pytest.raises(ValueError, match="exact decimal|string|strictly"):
        minimum_positive_control_samples(invalid, "0.95")


def test_resource_bound_fails_closed_without_large_allocation():
    with pytest.raises(ValueError, match="exceed bounded implementation cap"):
        minimum_positive_control_samples("0.999999", "0.999999")


@pytest.mark.parametrize(
    "parent", ["effect_contract", "receiver_custody", "negative_observation", "calibration_receiver"]
)
def test_exact_parent_bindings_fail_closed(parent):
    contract = load()
    contract["parent_digests"][parent] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="wrong exact parent digest"):
        validate_tolerance_preregistration(contract)


def test_unselected_target_cannot_smuggle_a_value():
    contract = load()
    contract["target"]["coverage_p"] = "0.95"
    with pytest.raises(ValueError, match="unselected targets"):
        validate_tolerance_preregistration(contract)


def test_calibration_outcomes_cannot_select_targets():
    contract = load()
    contract["method"]["outcomes_used_to_select_targets"] = True
    with pytest.raises(ValueError, match="outcome firewall"):
        validate_tolerance_preregistration(contract)


def test_integer_zero_cannot_impersonate_false_for_outcome_firewall():
    contract = load()
    contract["method"]["outcomes_used_to_select_targets"] = 0
    with pytest.raises(ValueError, match="outcome firewall"):
        validate_tolerance_preregistration(contract)


def test_unassessed_sampling_design_cannot_have_identity():
    contract = load()
    contract["sampling_assumptions"]["sampling_design_id"] = "unexpected"
    with pytest.raises(ValueError, match="unassessed sampling design"):
        validate_tolerance_preregistration(contract)


def test_frozen_target_requires_sampling_design():
    contract = mock_frozen()
    contract["sampling_assumptions"]["status"] = "UNASSESSED"
    contract["sampling_assumptions"]["sampling_design_id"] = None
    with pytest.raises(ValueError, match="documented sampling design"):
        validate_tolerance_preregistration(contract)


def test_one_fewer_than_exact_required_sample_count_is_rejected():
    contract = mock_frozen()
    contract["sample_plan"].update({"samples_per_system": 58, "maximum_allowed_samples": 58})
    with pytest.raises(ValueError, match="below exact tolerance requirement"):
        validate_tolerance_preregistration(contract)


def test_sample_budget_must_cover_full_preregistered_count():
    contract = mock_frozen()
    contract["sample_plan"]["maximum_allowed_samples"] = 58
    with pytest.raises(ValueError, match="budget below"):
        validate_tolerance_preregistration(contract)


def test_equal_counts_and_preregistration_cannot_be_disabled():
    for key in ("equal_counts_across_systems", "preregister_before_positive_controls"):
        contract = load()
        contract["sample_plan"][key] = False
        with pytest.raises(ValueError):
            validate_tolerance_preregistration(contract)


def test_no_empirical_or_authorization_ceiling_can_be_weakened():
    for key in load()["separation"]:
        contract = load()
        contract["separation"][key] = False
        with pytest.raises(ValueError, match="separation cannot be weakened"):
            validate_tolerance_preregistration(contract)


def test_structural_ready_is_not_authorization_or_empirical_evidence():
    contract = mock_frozen()
    result = evaluate_tolerance_preregistration(contract)
    assert result.ready
    assert contract["separation"]["structural_ready_not_run_authorization"] is True
    assert contract["separation"]["no_empirical_samples_collected"] is True
    assert contract["sampling_assumptions"]["status"] == "DOCUMENTED_UNVERIFIED"


def test_candidate_digest_is_deterministic_without_selection():
    digest = tolerance_preregistration_digest(load())
    assert len(digest) == 71
    assert digest == tolerance_preregistration_digest(load())
