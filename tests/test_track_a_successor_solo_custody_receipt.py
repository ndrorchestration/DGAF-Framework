from __future__ import annotations

import copy

import pytest

from scripts.validate_track_a_successor_solo_custody_receipt import validate_receipt


def valid_receipt() -> dict[str, object]:
    return {
        "record_type": "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "schema_version": 1,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "keypair_created_before_collection": True,
        "private_key_in_repository": False,
        "private_key_in_notion": False,
        "private_key_in_chat": False,
        "encrypted_private_key_sha256": "1" * 64,
        "certificate_sha256": "2" * 64,
        "certificate_public_key_der_sha256": "3" * 64,
        "recovered_public_key_der_sha256": "3" * 64,
        "recovery_drill": "PASS",
        "backup_refs": [
            {
                "class": "ENCRYPTED_LOCAL_ARCHIVE",
                "nonsecret_id": "recovery-copy-a",
                "encrypted": True,
                "user_controlled": True,
            },
            {
                "class": "ENCRYPTED_OFFSITE_ARCHIVE",
                "nonsecret_id": "recovery-copy-b",
                "encrypted": True,
                "user_controlled": True,
            },
        ],
        "empirical_collection_authorized": False,
        "scientific_state_effect": "NONE",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_valid_receipt_passes() -> None:
    validate_receipt(valid_receipt())


def test_requires_two_recovery_copies() -> None:
    receipt = valid_receipt()
    receipt["backup_refs"] = receipt["backup_refs"][:1]  # type: ignore[index]
    with pytest.raises(ValueError, match="at least two"):
        validate_receipt(receipt)


def test_recovered_key_must_match_certificate() -> None:
    receipt = valid_receipt()
    receipt["recovered_public_key_der_sha256"] = "4" * 64
    with pytest.raises(ValueError, match="does not match"):
        validate_receipt(receipt)


def test_cannot_self_claim_independent_custody() -> None:
    receipt = valid_receipt()
    receipt["independent_custody"] = True
    with pytest.raises(ValueError, match="must not claim independence"):
        validate_receipt(receipt)


def test_receipt_cannot_authorize_collection() -> None:
    receipt = valid_receipt()
    receipt["empirical_collection_authorized"] = True
    with pytest.raises(ValueError, match="must not authorize"):
        validate_receipt(receipt)


def test_rejects_extra_secret_bearing_field() -> None:
    receipt = copy.deepcopy(valid_receipt())
    receipt["passphrase"] = "must-never-be-here"
    with pytest.raises(ValueError, match="schema exactly"):
        validate_receipt(receipt)


def test_backup_identifiers_must_be_distinct() -> None:
    receipt = valid_receipt()
    backups = receipt["backup_refs"]
    assert isinstance(backups, list)
    assert isinstance(backups[1], dict)
    backups[1]["nonsecret_id"] = "recovery-copy-a"
    with pytest.raises(ValueError, match="must be distinct"):
        validate_receipt(receipt)


def valid_v2_receipt() -> dict:
    receipt = valid_receipt()
    receipt["schema_version"] = 2
    receipt["recovery_verified_at"] = "2026-09-10T03:00:00+00:00"
    for backup in receipt["backup_refs"]:
        backup.update(
            {
                "encrypted_private_key_sha256": receipt["encrypted_private_key_sha256"],
                "recovered_public_key_der_sha256": receipt["certificate_public_key_der_sha256"],
                "recovery_drill": "PASS",
            }
        )
    return receipt


def test_v2_requires_both_backup_recovery_records() -> None:
    receipt = valid_v2_receipt()
    validate_receipt(receipt)
    receipt["backup_refs"][1].pop("recovery_drill")
    with pytest.raises(ValueError, match="keys invalid"):
        validate_receipt(receipt)


@pytest.mark.parametrize(
    "field,value",
    [
        ("recovery_drill", "FAIL"),
        ("encrypted_private_key_sha256", "0" * 64),
        ("recovered_public_key_der_sha256", "0" * 64),
        ("class", "ENCRYPTED_LOCAL_ARCHIVE"),
    ],
)
def test_v2_rejects_bad_second_backup(field: str, value: str) -> None:
    receipt = valid_v2_receipt()
    receipt["backup_refs"][1][field] = value
    with pytest.raises(ValueError):
        validate_receipt(receipt)


def test_v2_rejects_timezone_free_timestamp() -> None:
    receipt = valid_v2_receipt()
    receipt["recovery_verified_at"] = "2026-09-10T03:00:00"
    with pytest.raises(ValueError, match="timezone"):
        validate_receipt(receipt)
