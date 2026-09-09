import copy
import json
from pathlib import Path

import pytest

from scripts.validate_p30_authority_reconciliation import RECORD, validate_record


def _record() -> dict:
    return json.loads(Path(RECORD).read_text(encoding="utf-8"))


def test_reconciliation_record_passes() -> None:
    validate_record(_record())


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("canonical_p30", "authority"), "LEGACY_RUNTIME_SCALAR"),
        (("legacy_runtime_scalar_gate", "equivalent_to_canonical_p30"), True),
        (("bridge", "p11_11q_to_runtime_confidence"), "IMPLICIT_IDENTITY"),
        (("bridge", "agent_values_proxy_allowed"), True),
        (("bridge", "outcome_derived_proxy_allowed"), True),
        (("bridge", "default_constant_as_calibrated_confidence_allowed"), True),
        (("bridge", "phi_constant_as_calibrated_confidence_allowed"), True),
        (("bridge", "synthetic_fixture_as_calibrated_confidence_allowed"), True),
        (("empirical_gate", "fresh_empirical_authorization_granted"), True),
        (("empirical_gate", "new_canonical_dgaf_empirical_epoch"), "AUTHORIZED"),
        (("empirical_gate", "high_assurance_authorization_changed"), True),
    ],
)
def test_reconciliation_fails_closed_on_semantic_drift(path, value) -> None:
    data = copy.deepcopy(_record())
    section, key = path
    data[section][key] = value
    with pytest.raises(AssertionError):
        validate_record(data)
