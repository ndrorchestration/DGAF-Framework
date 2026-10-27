"""Input-custody and interpretation gates for optional, non-admitted DDE receipts."""

import copy
import math

import pytest

from tools.pdmal.early_window_oracle import initial_window_trajectory
from tools.pdmal.early_window_receipt_audit import audit_receipts
from tools.pdmal.jitcdde_reference_probe import EXPECTED_FIXTURE_SHA256, INITIAL


def _fixtures():
    """Artificial traces validate parsing only; never numerical-scientific data."""
    oracle = initial_window_trajectory(0.000625)
    base = [list(INITIAL)] + [list(oracle[32]), list(oracle[64])]
    base.extend([list(oracle[64])] * 38)
    variants = []
    for step in (0.001, 0.0005, 0.00025):
        trace = copy.deepcopy(base)
        trace[1][0] += 0.2 * step
        trace[2][0] += 0.2 * step
        variants.append({"bootstrap_step_s": step, "complete_trajectory": trace})
    nominal = {
        "fixture_sha256": EXPECTED_FIXTURE_SHA256,
        "dde_trajectory_unwrapped_rad": copy.deepcopy(variants[0]["complete_trajectory"]),
        "scientific_n_increment": 0,
        "pilot_authorization": "NOT_GRANTED",
        "independent_validation": "NOT_ESTABLISHED",
    }
    sensitivity = {
        "nominal_fixture_sha256": EXPECTED_FIXTURE_SHA256,
        "variants": variants,
        "scientific_n_increment": 0,
        "pilot_authorization": "NOT_GRANTED",
        "independent_validation": "NOT_ESTABLISHED",
    }
    return nominal, sensitivity


def test_first_window_residual_report_discloses_disagreement_not_acceptance():
    nominal, sensitivity = _fixtures()
    audit = audit_receipts(nominal, sensitivity)
    assert audit["status"] == "EXECUTION_RECEIPT_AUDITED_NUMERICAL_ACCURACY_NOT_CERTIFIED"
    assert audit["independent_validation"] == "NOT_ESTABLISHED"
    assert audit["scientific_n_increment"] == 0
    assert len(audit["first_window_residuals"]) == 3
    assert audit["t_0p02_residual_halving_ratios"] == pytest.approx([2.0, 2.0])
    assert audit["t_0p04_residual_halving_ratios"] == pytest.approx([2.0, 2.0])


@pytest.mark.parametrize(
    "field,bad",
    [
        ("fixture_sha256", "changed"),
        ("pilot_authorization", "GRANTED"),
        ("independent_validation", "ESTABLISHED"),
        ("scientific_n_increment", 1),
    ],
)
def test_nominal_receipt_custody_fails_closed(field, bad):
    nominal, sensitivity = _fixtures()
    nominal[field] = bad
    with pytest.raises(ValueError):
        audit_receipts(nominal, sensitivity)


@pytest.mark.parametrize(
    "field,bad",
    [
        ("nominal_fixture_sha256", "changed"),
        ("pilot_authorization", "GRANTED"),
        ("independent_validation", "ESTABLISHED"),
        ("scientific_n_increment", 2),
    ],
)
def test_variant_receipt_custody_fails_closed(field, bad):
    nominal, sensitivity = _fixtures()
    sensitivity[field] = bad
    with pytest.raises(ValueError):
        audit_receipts(nominal, sensitivity)


def test_truncated_variant_trajectory_rejected():
    nominal, sensitivity = _fixtures()
    sensitivity["variants"][2]["complete_trajectory"].pop()
    with pytest.raises(ValueError, match="41 sampled states"):
        audit_receipts(nominal, sensitivity)


def test_nonfinite_variant_trajectory_rejected():
    nominal, sensitivity = _fixtures()
    sensitivity["variants"][1]["complete_trajectory"][2][2] = math.nan
    with pytest.raises(ValueError, match="invalid numerical value"):
        audit_receipts(nominal, sensitivity)


def test_modified_initial_state_rejected():
    nominal, sensitivity = _fixtures()
    sensitivity["variants"][2]["complete_trajectory"][0][0] += 0.1
    with pytest.raises(ValueError, match="prescribed initial state"):
        audit_receipts(nominal, sensitivity)


def test_misordered_bootstrap_variants_rejected():
    nominal, sensitivity = _fixtures()
    sensitivity["variants"].reverse()
    with pytest.raises(ValueError, match="bootstrap sequence"):
        audit_receipts(nominal, sensitivity)


def test_nominal_and_sensitivity_disagreement_rejected():
    nominal, sensitivity = _fixtures()
    nominal["dde_trajectory_unwrapped_rad"][10][0] += 0.01
    with pytest.raises(ValueError, match="trajectories disagree"):
        audit_receipts(nominal, sensitivity)


def test_invalid_trace_type_rejected():
    nominal, sensitivity = _fixtures()
    nominal["dde_trajectory_unwrapped_rad"] = "redacted"
    with pytest.raises(ValueError, match="41 sampled states"):
        audit_receipts(nominal, sensitivity)

def test_zero_error_variants_have_undefined_ratios_not_infinite_values():
    nominal, sensitivity = _fixtures()
    early = initial_window_trajectory(0.000625)
    for variant in sensitivity["variants"]:
        variant["complete_trajectory"][1] = list(early[32])
        variant["complete_trajectory"][2] = list(early[64])
    nominal["dde_trajectory_unwrapped_rad"] = copy.deepcopy(sensitivity["variants"][0]["complete_trajectory"])
    audited = audit_receipts(nominal, sensitivity)
    assert audited["t_0p02_residual_halving_ratios"] == [None, None]
    assert audited["t_0p04_residual_halving_ratios"] == [None, None]
    assert audited["independent_validation"] == "NOT_ESTABLISHED"

