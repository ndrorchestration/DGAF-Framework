"""Explicit identity wrapper for the historical scalar Apogee runtime reviewer.

This module does not redefine canonical P-30. Canonical P-30 remains the S035
P-11/11Q Apogee attestation gate. The scalar S/A/B/C/D reviewer restored in the
PDMAL apparatus is preserved as historical runtime behavior under a distinct,
non-canonical identity.
"""

try:  # Package import path used by repository-wide tests and tooling.
    from .pdmaltgl_gate_binding import ApogeeAttestationState, build_apogee_hook
except ImportError:  # Flat pilot PYTHONPATH used by historical experiment workflows.
    from pdmaltgl_gate_binding import ApogeeAttestationState, build_apogee_hook

LEGACY_APOGEE_RUNTIME_GATE_ID = "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
CANONICAL_P30_AUTHORITY = "S035_P11_11Q_ATTESTATION"
CANONICAL_TREATMENT_STATUS = "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE = "NOT_ESTABLISHED"

# Compatibility aliases deliberately preserve the historical implementation
# without claiming that its symbols define canonical P-30.
LegacyApogeeRuntimeConfidenceState = ApogeeAttestationState
build_legacy_apogee_runtime_hook = build_apogee_hook


def assert_noncanonical_runtime_identity() -> None:
    """Fail closed if the legacy runtime mechanism is conflated with P-30."""

    assert LEGACY_APOGEE_RUNTIME_GATE_ID != "P-30"
    assert not LEGACY_APOGEE_RUNTIME_GATE_ID.startswith("P-")
    assert CANONICAL_P30_AUTHORITY == "S035_P11_11Q_ATTESTATION"
    assert CANONICAL_TREATMENT_STATUS == "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
    assert NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE == "NOT_ESTABLISHED"
