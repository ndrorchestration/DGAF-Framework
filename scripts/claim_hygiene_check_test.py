#!/usr/bin/env python3
"""Focused regression tests for claim-hygiene non-assertive context handling."""
from __future__ import annotations

import re

from claim_hygiene_check import line_is_non_assertive

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


def test_policy_list_fragment_is_non_assertive() -> None:
    line = "- is empirically superior;"
    assert PATTERNS[2].search(line)
    assert line_is_non_assertive(line)


def test_positive_efficacy_claim_is_not_non_assertive() -> None:
    line = "DGAF is empirically superior to the null condition."
    assert PATTERNS[2].search(line)
    assert not line_is_non_assertive(line)


def test_positive_bulleted_efficacy_claim_is_not_non_assertive() -> None:
    line = "- DGAF is empirically superior to the null condition."
    assert PATTERNS[2].search(line)
    assert not line_is_non_assertive(line)


if __name__ == "__main__":
    test_explicit_prohibition_is_non_assertive()
    test_negative_efficacy_statement_is_non_assertive()
    test_policy_list_fragment_is_non_assertive()
    test_positive_efficacy_claim_is_not_non_assertive()
    test_positive_bulleted_efficacy_claim_is_not_non_assertive()
    print("claim-hygiene regression tests passed")
