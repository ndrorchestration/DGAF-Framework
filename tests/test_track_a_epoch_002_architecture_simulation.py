"""Synthetic Track A Epoch 002 architecture exercise.

Runs the REAL authorization validator against synthetic experiment receipts.
Never collects/unblinds/analyses real observations or writes canonical records.
"""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEST_HELPERS = ROOT / "tests/test_track_a_epoch_002_primary_analysis_authorization.py"


def fixture_module():
    spec = importlib.util.spec_from_file_location("track_a_fixture_helpers", TEST_HELPERS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_synthetic_experiment_proves_authority_bound_then_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trace materialization -> authorization -> source event without executing analysis."""
    helpers = fixture_module()
    validator = helpers.load_validator()
    receipt = helpers.materialization_receipt_fixture()
    authorization = helpers.valid_authorization(validator)

    # Baseline contract: an exact synthetic receipt is cryptographically bound
    # to its predecessor and parent. This is validation, not real authorization.
    helpers.validate_fixture(validator, authorization)
    assert authorization["predecessor_record_ids"] == [receipt["record_id"]]
    assert authorization["scientific_state_effect"]["empirical_n_increment"] == 0
    assert "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION" in authorization["non_effects"]

    # Adversarial changes isolate four independent parts of the chain.
    corruptions = (
        ("predecessor_record_ids", ["E002-FORGED-RECEIPT"]),
        ("evidence_scope", "PRIMARY_AND_EXPLORATORY_ANALYSIS"),
        ("authorization_effect", "EXECUTE_AND_PUBLISH"),
        ("status", "PASS_WITH_WARNINGS"),
    )
    for field, bad_value in corruptions:
        changed = copy.deepcopy(authorization)
        changed[field] = bad_value
        with pytest.raises(SystemExit):
            helpers.validate_fixture(validator, changed)

    # Separate source-event gate: source-bound receipt and first-only history.
    head, parent, _event, state = helpers.install_valid_event_fixture(
        monkeypatch, validator
    )
    assert helpers.validate_event_fixture(validator, head, parent) == parent
    state["receipt_history"].append("8" * 40)
    with pytest.raises(SystemExit):
        helpers.validate_event_fixture(validator, head, parent)


def test_synthetic_experiment_never_promotes_research_or_executes_analysis() -> None:
    helpers = fixture_module()
    validator = helpers.load_validator()
    authorization = helpers.valid_authorization(validator)
    effects = authorization["scientific_state_effect"]
    assert effects == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    for required in (
        "DOES_NOT_AUTHORIZE_COLLECTION",
        "DOES_NOT_AUTHORIZE_UNBLINDING",
        "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
        "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
    ):
        assert required in authorization["non_effects"]
