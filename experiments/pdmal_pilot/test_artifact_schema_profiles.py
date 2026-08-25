"""Tests preventing ambiguity between pre-freeze and authorized-pilot contracts."""
from __future__ import annotations

import hashlib

from artifact_schema import ARTIFACT_PROFILE as PRE_FREEZE_PROFILE
from artifact_schema import canonical_json_bytes as pre_freeze_canonical_json_bytes
from pilot_artifact_schema import ARTIFACT_PROFILE as PILOT_PROFILE
from pilot_artifact_schema import canonical_json_bytes as pilot_canonical_json_bytes


def test_schema_profiles_are_explicitly_distinct() -> None:
    assert PRE_FREEZE_PROFILE == "PDMAL_PRE_FREEZE_V1"
    assert PILOT_PROFILE == "PDMAL_AUTHORIZED_PILOT_V1"
    assert PRE_FREEZE_PROFILE != PILOT_PROFILE


def test_canonical_serialization_is_byte_identical() -> None:
    payload = {
        "z": 1,
        "nested": {"b": True, "a": [3, 2, 1]},
        "text": "profile-check",
    }
    pre = pre_freeze_canonical_json_bytes(payload)
    pilot = pilot_canonical_json_bytes(payload)
    assert pre == pilot
    assert hashlib.sha256(pre).hexdigest() == hashlib.sha256(pilot).hexdigest()


def test_profile_identity_cannot_be_inferred_from_schema_version_alone() -> None:
    # Both lifecycle contracts intentionally retain schema_version=1.0 for
    # compatibility; profile identity is therefore mandatory metadata.
    from artifact_schema import ARTIFACT_SCHEMA_VERSION as pre_version
    from pilot_artifact_schema import ARTIFACT_SCHEMA_VERSION as pilot_version

    assert pre_version == pilot_version == "1.0"
    assert PRE_FREEZE_PROFILE != PILOT_PROFILE
