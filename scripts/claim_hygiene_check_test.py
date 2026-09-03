#!/usr/bin/env python3
"""Focused regression tests for claim-hygiene non-assertive context handling."""
from __future__ import annotations

import re

from claim_hygiene_check import artifact_is_historical, line_is_non_assertive

PATTERNS = [
    re.compile(r"\bDGAF\s+(?:Certified|Official|Endorsed|Verified|Approved)\b", re.I),
    re.compile(r"\b(?:production[- ]ready|guarantees? convergence|guaranteed convergence)\b", re.I),
    re.compile(r"\b(?:universally safe|universal safety|proven efficacy|empirically superior)\b", re.I),
]


def test_explicit_prohibition_is_non_assertive() -> None:
    line = "future ‘Official DGAF,’ ‘DGAF Certified,’ or endorsement claims require separate governance"
    assert PATTERNS[0].search(line)
    assert line_is_non_assertive(line)


def test_negative_efficacy_statement_is_non_assertive() -> None:
    line = "The procedure does not by itself prove that the system is empirically superior."
    assert PATTERNS[2].search(line)
    assert line_is_non_assertive(line)


def test_positive_claim_is_not_non_assertive() -> None:
    line = "DGAF is empirically superior to the null condition."
    assert PATTERNS[2].search(line)
    assert not line_is_non_assertive(line)


def test_historical_priority_adjudication_is_historical_context() -> None:
    text = """# DGAF Historical-Priority Adjudication — 2026-09-01

## Executive conclusion

The defensible historical thesis is narrower.

- is empirically superior;
"""
    assert artifact_is_historical(text, 7)


if __name__ == "__main__":
    test_explicit_prohibition_is_non_assertive()
    test_negative_efficacy_statement_is_non_assertive()
    test_positive_claim_is_not_non_assertive()
    test_historical_priority_adjudication_is_historical_context()
    print("claim-hygiene regression tests passed")
