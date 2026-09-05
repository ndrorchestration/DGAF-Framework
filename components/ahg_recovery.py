"""AHG Tribunal recovery scoring (P-42 v1.5).

The recovery score is an empirical control signal. It is not a stability proof.
"""

from __future__ import annotations

from .ahg_conductor import StateVector

R1: float = 0.50
R2: float = 0.30
R3: float = 0.20
R_THRESHOLD: float = 0.05
PHI_EXIT_THRESHOLD: float = 1.70
RECOVERY_CONSECUTIVE_TURNS: int = 2


def compute_recovery_score(
    sv_prev: StateVector,
    sv_curr: StateVector,
    phi_history: list[float],
) -> float:
    """Compute P-42 recovery score from consecutive state vectors.

    Positive values indicate improvement: lower D_e, higher K, and decreasing
    phase velocity each contribute positively. The signal is an empirical
    recovery metric, not a proof of system stability.
    """
    delta_d_e = sv_prev.D_e - sv_curr.D_e
    delta_k = sv_curr.K - sv_prev.K
    if len(phi_history) >= 3:
        v_prev = phi_history[-2] - phi_history[-3]
        v_curr = phi_history[-1] - phi_history[-2]
        delta_v_phi = v_prev - v_curr
    else:
        delta_v_phi = 0.0
    return R1 * delta_d_e + R2 * delta_k + R3 * delta_v_phi


def recovery_exit_met(
    recovery_score: float,
    phi: float,
    consecutive_turns: int,
    *,
    threshold: float = R_THRESHOLD,
    phi_threshold: float = PHI_EXIT_THRESHOLD,
    required_turns: int = RECOVERY_CONSECUTIVE_TURNS,
) -> bool:
    """Return whether the Tribunal recovery exit condition is satisfied."""
    return recovery_score > threshold and phi < phi_threshold and consecutive_turns >= required_turns
