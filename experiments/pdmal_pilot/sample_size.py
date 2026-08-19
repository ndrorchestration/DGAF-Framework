"""Paired-difference sample-size planning for FFCR.

This is a planning utility, not an analysis of observed pilot data. It expects
an externally supplied pilot SD and never reads or modifies experiment data.
"""
from __future__ import annotations

import math
from statistics import NormalDist


def required_n(
    sigma_diff: float,
    *,
    alpha: float = 0.05,
    power: float = 0.80,
    mdd: float = 0.15,
) -> int:
    if sigma_diff <= 0:
        raise ValueError("sigma_diff must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    if not 0 < power < 1:
        raise ValueError("power must be in (0,1)")
    if mdd <= 0:
        raise ValueError("mdd must be positive")
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    return math.ceil(((z_alpha + z_power) ** 2 * sigma_diff**2) / (mdd**2))


def planning_record(sigma_diff: float, **kwargs: float) -> dict[str, float | int | str]:
    n = required_n(sigma_diff, **kwargs)
    return {
        "method": "paired_difference_normal_approximation",
        "sigma_diff": sigma_diff,
        "alpha": kwargs.get("alpha", 0.05),
        "power": kwargs.get("power", 0.80),
        "mdd": kwargs.get("mdd", 0.15),
        "required_n": n,
        "rounding": "math.ceil",
    }
