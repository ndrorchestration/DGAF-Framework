import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.aoss_stage_a.execution_identity_review import (
    ExecutionIdentityReviewPacketError,
    prepare_execution_identity_review_packet,
    record_sha256,
    validate_execution_identity_review_packet,
)

ROOT = Path(__file__).resolve().parents[1]


def _records():
    source = json.loads((ROOT / "registry/aoss_v0_6_stage_a_source_driver_binding_v1.json").read_text())
    identities = json.loads((ROOT / "registry/aoss_v0_6_stage_a_executable_destination_binding_v1.json").read_text())
    return source, identities


def _packet():
    source, identities = _records()
    packet = prepare_execution_identity_review_packet(
        source_driver_binding=source,
        executable_destination_binding=identities,
        source_driver_ref="registry://aoss/source-driver-binding-v1",
        executable_destination_ref="registry://aoss/executable-destination-binding-v1",
    )
    return source, identities, packet


def test_review_packet_binds_proposals_and_remains_blocked():
    source, identities, packet = _packet()
    report = validate_execution_identity_review_packet(
        packet,
        source_driver_binding=source,
        executable_destination_binding=identities,
    )

    assert packet["source_driver"]["record_sha256"] == record_sha256(source)
    assert packet["executable_destination"]["record_sha256"] == record_sha256(identities)
    assert report["packet_validation"] == "PASS_BLOCKED_REVIEW_PACKET"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["external_adjudication"] == "NOT_EXECUTED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        (
            "executable_identity_class",
            "REAL_EXECUTABLE",
            "EXECUTABLE_IDENTITY_CLASS_OVERCLAIM",
        ),
        (
            "destination_identity_class",
            "REAL_DESTINATION",
            "DESTINATION_IDENTITY_CLASS_OVERCLAIM",
        ),
        (
            "attempt_identity_class",
            "REAL_ATTEMPT",
            "ATTEMPT_IDENTITY_CLASS_OVERCLAIM",
        ),
        ("executable_acceptance", "ACCEPTED", "EXECUTABLE_ACCEPTANCE_PREMATURE"),
        ("destination_acceptance", "ACCEPTED", "DESTINATION_ACCEPTANCE_PREMATURE"),
    ],
)
def test_review_packet_rejects_identity_or_acceptance_overclaim(field, value, error):
    source, identities, packet = _packet()
    packet["executable_destination"][field] = value

    with pytest.raises(ExecutionIdentityReviewPacketError, match=error):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=identities,
        )


def test_review_packet_rejects_source_record_drift():
    source, identities, packet = _packet()
    packet["source_driver"]["record_sha256"] = "0" * 64

    with pytest.raises(
        ExecutionIdentityReviewPacketError,
        match="SOURCE_DRIVER_REVIEW_DIGEST_MISMATCH",
    ):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=identities,
        )


def test_review_packet_rejects_identity_record_drift():
    source, identities, packet = _packet()
    packet["executable_destination"]["record_sha256"] = "0" * 64

    with pytest.raises(
        ExecutionIdentityReviewPacketError,
        match="EXECUTABLE_DESTINATION_REVIEW_DIGEST_MISMATCH",
    ):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=identities,
        )


def test_review_packet_rejects_adjudication_prepopulation():
    source, identities, packet = _packet()
    packet["adjudication"]["reviewer_identity"] = "self"

    with pytest.raises(
        ExecutionIdentityReviewPacketError,
        match="EXECUTION_IDENTITY_ADJUDICATION_PREMATURE",
    ):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=identities,
        )


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("execution_allowed", True, "EXECUTION_PREMATURE"),
        (
            "collection_execution_readiness",
            "ESTABLISHED",
            "COLLECTION_READINESS_PREMATURE",
        ),
        ("outcomes_generated", True, "OUTCOME_GENERATION_PREMATURE"),
        ("scientific_n_increment", 1, "SCIENTIFIC_N_INCREMENT_INVALID"),
    ],
)
def test_review_packet_cannot_promote_execution_state(field, value, error):
    source, identities, packet = _packet()
    packet[field] = value

    with pytest.raises(ExecutionIdentityReviewPacketError, match=error):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=identities,
        )


def test_review_packet_detects_underlying_record_mutation():
    source, identities, packet = _packet()
    mutated = deepcopy(identities)
    mutated["source_commit"] = "0" * 40

    with pytest.raises(Exception):
        validate_execution_identity_review_packet(
            packet,
            source_driver_binding=source,
            executable_destination_binding=mutated,
        )
