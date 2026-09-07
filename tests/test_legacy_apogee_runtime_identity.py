import copy
import json

import pytest

from scripts.validate_legacy_apogee_runtime_identity import (
    MIGRATION,
    RECONCILIATION,
    validate,
)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_legacy_apogee_identity_migration_passes() -> None:
    validate(_load(MIGRATION), _load(RECONCILIATION))


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
