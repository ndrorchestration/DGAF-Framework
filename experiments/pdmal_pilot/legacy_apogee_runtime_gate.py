"""Pure identity map for the historical scalar Apogee runtime reviewer.

This module does not import or execute the historical pilot stack. Canonical
P-30 remains the S035 P-11/11Q Apogee attestation gate. The scalar S/A/B/C/D
reviewer restored in the PDMAL apparatus is preserved by symbolic reference
under a distinct, non-canonical identity.
"""

LEGACY_APOGEE_RUNTIME_GATE_ID = "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
CANONICAL_P30_AUTHORITY = "S035_P11_11Q_ATTESTATION"
CANONICAL_TREATMENT_STATUS = "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE = "NOT_ESTABLISHED"

HISTORICAL_IMPLEMENTATION_MODULE = "experiments/pdmal_pilot/pdmaltgl_gate_binding.py"
HISTORICAL_STATE_SYMBOL = "ApogeeAttestationState"
HISTORICAL_HOOK_SYMBOL = "build_apogee_hook"
HISTORICAL_DESIGNATION_ISSUE = 165
HISTORICAL_THRESHOLD_MAP = {
    "S": 0.90,
    "A": 0.75,
    "B": 0.60,
    "C": 0.45,
}
HISTORICAL_TERMINAL_RULE = "D_TO_KILL"
HISTORICAL_GOLD_STAR_RULE = "GRADE_S_AND_NONTRIVIAL_DESCRIPTION"


def assert_noncanonical_runtime_identity() -> None:
    """Fail closed if the legacy runtime mechanism is conflated with P-30."""

    assert LEGACY_APOGEE_RUNTIME_GATE_ID != "P-30"
    assert not LEGACY_APOGEE_RUNTIME_GATE_ID.startswith("P-")
    assert CANONICAL_P30_AUTHORITY == "S035_P11_11Q_ATTESTATION"
    assert CANONICAL_TREATMENT_STATUS == "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
    assert NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE == "NOT_ESTABLISHED"
    assert HISTORICAL_DESIGNATION_ISSUE == 165
    assert HISTORICAL_THRESHOLD_MAP == {
        "S": 0.90,
        "A": 0.75,
        "B": 0.60,
        "C": 0.45,
    }
    assert HISTORICAL_TERMINAL_RULE == "D_TO_KILL"
