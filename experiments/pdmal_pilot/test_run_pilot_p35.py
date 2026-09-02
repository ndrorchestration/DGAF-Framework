"""Tests for the explicit pilot-time P-35 checker boundary.

These tests validate configuration failure modes only. They do not authorize or
execute the empirical pilot.
"""
from __future__ import annotations

import os

import pytest

from run_pilot import require_pilot_premise_checker


def test_missing_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PDMAL_PREMISE_CHECKER", raising=False)
    with pytest.raises(SystemExit, match="PDMAL_PREMISE_CHECKER"):
        require_pilot_premise_checker()


def test_malformed_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "not-module-attribute")
    with pytest.raises(SystemExit, match="module:attribute"):
        require_pilot_premise_checker()


def test_unknown_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "module_that_does_not_exist:checker")
    with pytest.raises(SystemExit, match="unable to load P-35 checker"):
        require_pilot_premise_checker()


def test_non_callable_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "os:path")
    with pytest.raises(SystemExit, match="not callable"):
        require_pilot_premise_checker()


def test_explicit_premise_checker_is_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "test_run_pilot_p35:allow_premises")
    checker = require_pilot_premise_checker()
    assert checker("input", object()) is True


def allow_premises(_text, _invariant) -> bool:
    return True
