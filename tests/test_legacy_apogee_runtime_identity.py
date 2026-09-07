import copy
import json

import pytest

from experiments.pdmal_pilot.legacy_apogee_runtime_gate import (
    CANONICAL_P30_AUTHORITY,
    CANONICAL_TREATMENT_STATUS,
    LEGACY_APOGEE_RUNTIME_GATE_ID,
    LegacyApogeeRuntimeConfidenceState,
    assert_noncanonical_runtime_identity,
    build_legacy_apogee_runtime_hook,
)
from scripts.validate_legacy_apogee_runtime_identity import (
    MIGRATION,
    RECONCILIATION,
    validate,
)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_legacy_apogee_identity_migration_passes() -> None:
    validate(_load(MIGRATION), _load(RECONCILIATION))


def test_compatibility_wrapper_is_explicitly_noncanonical() -> None:
    assert_noncanonical_runtime_identity()
    assert LEGACY_APOGEE_RUNTIME_GATE_ID == "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
    assert CANONICAL_P30_AUTHORITY == "S035_P11_11Q_ATTESTATION"
    assert CANONICAL_TREATMENT_STATUS == "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"


def test_compatibility_wrapper_preserves_historical_scalar_behavior() -> None:
    passing = LegacyApogeeRuntimeConfidenceState(confidence=0.45)
    assert build_legacy_apogee_runtime_hook(passing)("", {}).value == "PASS"
    assert passing.grade == "C"

    failing = LegacyApogeeRuntimeConfidenceState(confidence=0.44)
    assert build_legacy_apogee_runtime_hook(failing)("", {}).value == "KILL"
    assert failing.grade == "D"


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("canonical_p30", "inside_per_turn_pdmal_consensus_dynamics", True),
        ("canonical_p30", "authority", "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"),
        ("legacy_runtime_gate", "id", "P-30"),
        ("legacy_runtime_gate", "canonical_pattern_id", "P-30"),
        ("legacy_runtime_gate", "canonical_treatment_status", "CANONICAL"),
        ("bridge", "p11_11q_to_runtime_confidence", "IDENTITY"),
        ("bridge", "implicit_numeric_bridge_allowed", True),
        ("bridge", "agent_values_proxy_allowed", True),
        ("bridge", "outcome_derived_proxy_allowed", True),
        ("next_gate", "new_canonical_empirical_epoch", "AUTHORIZED"),
        ("next_gate", "high_assurance_authorization_changed", True),
    ],
)
def test_migration_fails_closed_on_conflation(section, key, value) -> None:
    data = copy.deepcopy(_load(MIGRATION))
    data[section][key] = value
    with pytest.raises(AssertionError):
        validate(data, _load(RECONCILIATION))
