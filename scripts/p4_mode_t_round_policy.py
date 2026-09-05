#!/usr/bin/env python3
"""Pure deterministic helpers for the draft P4 Mode T drand round policy.

This module performs no network access, secret generation, encryption, empirical
execution, freeze mutation, or authorization. It exists only to make the
non-secret timing/round arithmetic in Issue #287 machine-testable.
"""

from __future__ import annotations

import math

QUICKNET_CHAIN_HASH = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
QUICKNET_GENESIS_TIME_UNIX = 1692803367
QUICKNET_PERIOD_SECONDS = 3


def round_time_unix(round_number: int) -> int:
    """Return the deterministic nominal Unix time for quicknet round >= 1."""
    if not isinstance(round_number, int) or isinstance(round_number, bool) or round_number < 1:
        raise ValueError("round_number must be an integer >= 1")
    return QUICKNET_GENESIS_TIME_UNIX + (round_number - 1) * QUICKNET_PERIOD_SECONDS


def first_round_at_or_after(timestamp_unix: int) -> int:
    """Return the first quicknet round whose nominal time is >= timestamp."""
    if not isinstance(timestamp_unix, int) or isinstance(timestamp_unix, bool):
        raise ValueError("timestamp_unix must be an integer")
    if timestamp_unix <= QUICKNET_GENESIS_TIME_UNIX:
        return 1
    delta = timestamp_unix - QUICKNET_GENESIS_TIME_UNIX
    return math.ceil(delta / QUICKNET_PERIOD_SECONDS) + 1


def select_release_round(consumption_time_unix: int, analysis_lock_window_seconds: int) -> int:
    """Derive the release round from pre-secret C time plus frozen window W."""
    if not isinstance(consumption_time_unix, int) or isinstance(consumption_time_unix, bool):
        raise ValueError("consumption_time_unix must be an integer")
    if (
        not isinstance(analysis_lock_window_seconds, int)
        or isinstance(analysis_lock_window_seconds, bool)
        or analysis_lock_window_seconds <= 0
    ):
        raise ValueError("analysis_lock_window_seconds must be a positive integer")
    target = consumption_time_unix + analysis_lock_window_seconds
    return first_round_at_or_after(target)


def analysis_lock_precedes_release(analysis_lock_time_unix: int, release_round: int) -> bool:
    """Require strict pre-release ordering for the externally integrated L time."""
    if not isinstance(analysis_lock_time_unix, int) or isinstance(analysis_lock_time_unix, bool):
        raise ValueError("analysis_lock_time_unix must be an integer")
    return analysis_lock_time_unix < round_time_unix(release_round)
