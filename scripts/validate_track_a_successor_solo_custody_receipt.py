#!/usr/bin/env python3
"""Validate the non-secret recovery receipt for a Track A successor custody key.

This validator never reads private-key bytes or passphrases. It validates only
public fingerprints and a non-secret record proving that a local recovery drill
was completed before empirical collection is authorized.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_KEYS = {
    "record_type",
    "schema_version",
    "custody_class",
    "independent_custody",
    "keypair_created_before_collection",
    "private_key_in_repository",
    "private_key_in_notion",
    "private_key_in_chat",
    "encrypted_private_key_sha256",
    "certificate_sha256",
    "certificate_public_key_der_sha256",
    "recovered_public_key_der_sha256",
    "recovery_drill",
    "backup_refs",
    "empirical_collection_authorized",
    "scientific_state_effect",
    "canonical_dgaf_efficacy",
}

FORBIDDEN_KEY_FRAGMENTS = (
    "private_key_pem",
    "private_key_bytes",
    "passphrase",
    "password",
    "secret_value",
    "recovery_phrase",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def validate_receipt(payload: dict[str, Any]) -> None:
    version = payload.get("schema_version")
    _require(type(version) is int and version in (1, 2), "unsupported schema_version")
    expected_keys = EXPECTED_KEYS | ({"recovery_verified_at"} if version == 2 else set())
    _require(set(payload) == expected_keys, "receipt keys must match schema exactly")
    if version == 2:
        timestamp = payload["recovery_verified_at"]
        _require(isinstance(timestamp, str), "recovery timestamp required")
        _require(datetime.fromisoformat(timestamp).utcoffset() is not None, "recovery timestamp must include timezone")

    lowered_keys = {key.lower() for key in payload}
    for fragment in FORBIDDEN_KEY_FRAGMENTS:
        _require(fragment not in lowered_keys, f"secret-bearing field prohibited: {fragment}")

    _require(
        payload["record_type"] == "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "wrong record_type",
    )
    _require(payload["custody_class"] == "SAME_SYSTEM_NONINDEPENDENT", "wrong custody_class")
    _require(payload["independent_custody"] is False, "solo custody must not claim independence")
    _require(payload["keypair_created_before_collection"] is True, "keypair must predate collection")
    _require(payload["private_key_in_repository"] is False, "private key must remain outside repository")
    _require(payload["private_key_in_notion"] is False, "private key must remain outside Notion")
    _require(payload["private_key_in_chat"] is False, "private key must remain outside chat")

    for field in (
        "encrypted_private_key_sha256",
        "certificate_sha256",
        "certificate_public_key_der_sha256",
        "recovered_public_key_der_sha256",
    ):
        _require(_is_sha256(payload[field]), f"{field} must be lowercase SHA-256")

    _require(payload["recovery_drill"] == "PASS", "recovery drill must PASS")
    _require(
        payload["certificate_public_key_der_sha256"] == payload["recovered_public_key_der_sha256"],
        "recovered private key does not match collection certificate",
    )

    backups = payload["backup_refs"]
    _require(isinstance(backups, list) and len(backups) >= 2, "at least two encrypted recovery copies required")
    seen_ids: set[str] = set()
    seen_classes: set[str] = set()
    for index, backup in enumerate(backups):
        _require(isinstance(backup, dict), f"backup_refs[{index}] must be an object")
        _require(
            set(backup)
            == {"class", "nonsecret_id", "encrypted", "user_controlled"}
            | (
                {"encrypted_private_key_sha256", "recovered_public_key_der_sha256", "recovery_drill"}
                if version == 2
                else set()
            ),
            f"backup_refs[{index}] keys invalid",
        )
        _require(isinstance(backup["class"], str) and backup["class"], "backup class required")
        _require(
            isinstance(backup["nonsecret_id"], str) and backup["nonsecret_id"],
            "non-secret backup identifier required",
        )
        _require(backup["nonsecret_id"] not in seen_ids, "backup identifiers must be distinct")
        seen_ids.add(backup["nonsecret_id"])
        _require(backup["encrypted"] is True, "each recovery copy must be encrypted")
        _require(backup["user_controlled"] is True, "each recovery copy must be user controlled")
        if version == 2:
            _require(
                backup["class"]
                in {"ENCRYPTED_LOCAL_ARCHIVE", "ENCRYPTED_REMOVABLE_ARCHIVE", "ENCRYPTED_OFFSITE_ARCHIVE"},
                "unsupported backup storage class",
            )
            _require(backup["class"] not in seen_classes, "backup storage classes must be distinct")
            seen_classes.add(backup["class"])
            _require(backup["recovery_drill"] == "PASS", "each backup recovery must PASS")
            _require(
                backup["encrypted_private_key_sha256"] == payload["encrypted_private_key_sha256"],
                "backup encrypted bytes do not match",
            )
            _require(
                backup["recovered_public_key_der_sha256"] == payload["certificate_public_key_der_sha256"],
                "backup recovered public key does not match certificate",
            )

    _require(
        payload["empirical_collection_authorized"] is False,
        "custody receipt must not authorize empirical collection",
    )
    _require(payload["scientific_state_effect"] == "NONE", "custody receipt has no scientific-state authority")
    _require(payload["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED", "efficacy must remain not established")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.receipt.read_text(encoding="utf-8"))
    _require(isinstance(payload, dict), "receipt must be a JSON object")
    validate_receipt(payload)
    print("TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECEIPT=PASS")
    print("RECEIPT_VALIDATION=STRUCTURAL_SELF_ATTESTED_ONLY")
    print(f"BOTH_BACKUPS_RECORDED={payload['schema_version'] == 2}")
    print("INDEPENDENT_CUSTODY=FALSE")
    print("EMPIRICAL_COLLECTION_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
