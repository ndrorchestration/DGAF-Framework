import copy
import json

import pytest

from experiments.pdmal_pilot.legacy_apogee_runtime_gate import (
    CANONICAL_P30_AUTHORITY,
    CANONICAL_TREATMENT_STATUS,
    HISTORICAL_DESIGNATION_ISSUE,
    HISTORICAL_HOOK_SYMBOL,
    HISTORICAL_IMPLEMENTATION_MODULE,
    HISTORICAL_STATE_SYMBOL,
    HISTORICAL_TERMINAL_RULE,
    HISTORICAL_THRESHOLD_MAP,
    LEGACY_APOGEE_RUNTIME_GATE_ID,
    assert_noncanonical_runtime_identity,
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


def test_identity_map_is_explicitly_noncanonical() -> None:
    assert_noncanonical_runtime_identity()
    assert LEGACY_APOGEE_RUNTIME_GATE_ID == "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
    assert CANONICAL_P30_AUTHORITY == "S035_P11_11Q_ATTESTATION"
    assert CANONICAL_TREATMENT_STATUS == "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"


def test_identity_map_points_to_preserved_historical_semantics() -> None:
    assert HISTORICAL_IMPLEMENTATION_MODULE == "experiments/pdmal_pilot/pdmaltgl_gate_binding.py"
    assert HISTORICAL_STATE_SYMBOL == "ApogeeAttestationState"
    assert HISTORICAL_HOOK_SYMBOL == "build_apogee_hook"
    assert HISTORICAL_DESIGNATION_ISSUE == 165
    assert HISTORICAL_THRESHOLD_MAP == {"S": 0.90, "A": 0.75, "B": 0.60, "C": 0.45}
    assert HISTORICAL_TERMINAL_RULE == "D_TO_KILL"


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
