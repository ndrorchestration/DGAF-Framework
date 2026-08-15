"""P-42 v1.5 recovery-score tests."""

import math

from components.ahg_conductor import StateVector
from components.ahg_recovery import (
    R_THRESHOLD,
    compute_recovery_score,
    recovery_exit_met,
)


def test_recovery_score_sign_convention():
    prev = StateVector(D_e=0.8, K=0.2)
    curr = StateVector(D_e=0.6, K=0.5)
    score = compute_recovery_score(prev, curr, [1.80, 1.75, 1.70])
    # 0.50*.2 + 0.30*.3 + 0.20*.05 = .205
    assert math.isclose(score, 0.205, rel_tol=1e-9)


def test_recovery_score_no_velocity_term_with_short_history():
    prev = StateVector(D_e=0.8, K=0.2)
    curr = StateVector(D_e=0.6, K=0.5)
    assert math.isclose(compute_recovery_score(prev, curr, [1.8, 1.7]), 0.19)


def test_recovery_exit_requires_two_consecutive_turns():
    assert not recovery_exit_met(R_THRESHOLD + 0.01, 1.69, 1)
    assert recovery_exit_met(R_THRESHOLD + 0.01, 1.69, 2)


def test_recovery_exit_requires_phi_below_threshold():
    assert not recovery_exit_met(R_THRESHOLD + 0.01, 1.70, 2)
