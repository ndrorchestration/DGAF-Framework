"""SciPy probe contract tests without requiring SciPy in the CI environment.

NON-ADMITTED: this checks input and evidence integrity, not topology efficacy,
full DDE solver correctness or an independent scientific replication.
"""

import math

import pytest

from tools.pdmal.scipy_reference_probe import (
    _max_phase_difference,
    validate_reference_grid,
)


@pytest.mark.parametrize("segment, expected", [(0.02, 40), (0.01, 80), (0.005, 160), (0.0025, 320)])
def test_valid_reference_grid_has_exact_requested_horizon(segment, expected):
    assert validate_reference_grid(segment, 1e-11, 1e-13) == expected


@pytest.mark.parametrize("bad_segment", [0, -0.02, True, 0.03, 0.016, 0.04, 0.5, math.nan, math.inf])
def test_bad_or_discontinuity_misaligned_grids_fail_closed(bad_segment):
    with pytest.raises(ValueError):
        validate_reference_grid(bad_segment, 1e-11, 1e-13)


@pytest.mark.parametrize("bad_tolerance", [0, -1e-5, True, math.nan, math.inf, "1e-11"])
def test_invalid_reference_tolerances_fail_closed(bad_tolerance):
    with pytest.raises(ValueError):
        validate_reference_grid(0.02, bad_tolerance, 1e-13)
    with pytest.raises(ValueError):
        validate_reference_grid(0.02, 1e-11, bad_tolerance)


def test_phase_difference_rejects_mismatched_and_nonfinite_vectors():
    for a, b in (((), ()), ((0.0, 1.0), (0.0,)), ((math.nan,), (0.0,)), ((0.0,), (math.inf,))):
        with pytest.raises(ValueError):
            _max_phase_difference(a, b)
    assert _max_phase_difference((0.1, 0.5), (0.1, 0.4)) == pytest.approx(0.1)
