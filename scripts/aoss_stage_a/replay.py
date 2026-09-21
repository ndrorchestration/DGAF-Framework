"""Synthetic-only five-bundle replay verification for AOSS Stage A."""

from __future__ import annotations

import hashlib
from typing import Mapping, Sequence

REQUIRED_ARTIFACT_ROLES = (
    "study_manifest_sha256",
    "source_episode_bundle_sha256",
    "normalized_bundle_sha256",
    "decision_bundle_sha256",
    "analysis_bundle_sha256",
)
REPLAY_VERIFICATION_FIELDS = (
    "source_identity_match",
    "contract_digest_match",
    "study_manifest_hash_match",
    "source_episode_bundle_hash_match",
    "normalized_replay_digest_match",
    "decision_replay_digest_match",
    "analysis_replay_digest_match",
)
EXPECTED_REPLAY_PASSES = 5

_ROLE_TO_VERIFICATION = {
    "study_manifest_sha256": "study_manifest_hash_match",
    "source_episode_bundle_sha256": "source_episode_bundle_hash_match",
    "normalized_bundle_sha256": "normalized_replay_digest_match",
    "decision_bundle_sha256": "decision_replay_digest_match",
    "analysis_bundle_sha256": "analysis_replay_digest_match",
}


class ReplayVerificationError(ValueError):
    """Raised when synthetic replay inputs violate the frozen contract."""


def _digest(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise ReplayVerificationError("replay artifacts must be exact bytes")
    return hashlib.sha256(data).hexdigest()


def artifact_digests(bundle_bytes: Mapping[str, bytes]) -> dict[str, str]:
    if set(bundle_bytes) != set(REQUIRED_ARTIFACT_ROLES):
        raise ReplayVerificationError("five-bundle artifact role set mismatch")
    return {role: _digest(bundle_bytes[role]) for role in REQUIRED_ARTIFACT_ROLES}


def verify_replay_pass(
    expected: Mapping[str, bytes],
    replayed: Mapping[str, bytes],
    *,
    source_identity_match: bool,
    contract_digest_match: bool,
) -> dict[str, object]:
    """Compute every frozen replay boolean from actual byte comparisons."""

    expected_digests = artifact_digests(expected)
    replay_digests = artifact_digests(replayed)

    verification: dict[str, bool] = {
        "source_identity_match": bool(source_identity_match),
        "contract_digest_match": bool(contract_digest_match),
    }
    for role, field in _ROLE_TO_VERIFICATION.items():
        verification[field] = replay_digests[role] == expected_digests[role]

    status = "PASS" if all(verification[field] for field in REPLAY_VERIFICATION_FIELDS) else "FAIL"
    return {
        "status": status,
        **verification,
    }


def verify_five_exact_byte_replays(
    expected: Mapping[str, bytes],
    replay_passes: Sequence[Mapping[str, bytes]],
    *,
    source_identity_match: bool,
    contract_digest_match: bool,
) -> dict[str, object]:
    """Verify exactly five read-only synthetic replay passes."""

    if len(replay_passes) != EXPECTED_REPLAY_PASSES:
        raise ReplayVerificationError("exactly five replay passes are required")

    expected_digests = artifact_digests(expected)
    passes = [
        verify_replay_pass(
            expected,
            replayed,
            source_identity_match=source_identity_match,
            contract_digest_match=contract_digest_match,
        )
        for replayed in replay_passes
    ]
    return {
        "record_type": "AOSS_STAGE_A_SYNTHETIC_REPLAY_REPORT",
        "status": ("PASS" if all(item["status"] == "PASS" for item in passes) else "FAIL"),
        "artifact_digests": expected_digests,
        "replay_pass_count": EXPECTED_REPLAY_PASSES,
        "passes": passes,
        "replay_passes_count_as_independent_observations": False,
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "collection_execution_readiness": "NOT_ESTABLISHED",
    }
