"""Synthetic-only attempt-integrity contract for AOSS Stage A."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class AttemptIntegrityError(ValueError):
    """Raised when attempt-integrity evidence is malformed."""


@dataclass(frozen=True)
class AttemptIntegrityReport:
    status: str
    source_identity_match: bool
    contract_digest_match: bool
    artifact_digest_match: bool
    required_classes_complete: bool
    outcome_inspected: bool
    retry_allowed: bool
    scientific_n_increment: int = 0
    collection_execution_readiness: str = "NOT_ESTABLISHED"


def _require_digest_map(value: Mapping[str, str], label: str) -> dict[str, str]:
    normalized = dict(value)
    if not normalized:
        raise AttemptIntegrityError(f"{label} must not be empty")
    for key, digest in normalized.items():
        if not isinstance(key, str) or not key:
            raise AttemptIntegrityError(f"{label} contains invalid role")
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
        ):
            raise AttemptIntegrityError(f"{label} contains invalid SHA-256")
    return normalized


def assess_attempt_integrity(
    *,
    expected_source_identity: str,
    actual_source_identity: str,
    expected_contract_digests: Mapping[str, str],
    actual_contract_digests: Mapping[str, str],
    expected_artifact_digests: Mapping[str, str],
    actual_artifact_digests: Mapping[str, str],
    required_classes: Sequence[str],
    observed_classes: Sequence[str],
    outcome_inspected: bool,
) -> AttemptIntegrityReport:
    """Fail closed on identity/hash/class drift and freeze retries after inspection."""

    if not expected_source_identity or not actual_source_identity:
        raise AttemptIntegrityError("source identity must be explicit")
    if type(outcome_inspected) is not bool:
        raise AttemptIntegrityError("outcome_inspected must be boolean")

    expected_contracts = _require_digest_map(
        expected_contract_digests, "expected_contract_digests"
    )
    actual_contracts = _require_digest_map(
        actual_contract_digests, "actual_contract_digests"
    )
    expected_artifacts = _require_digest_map(
        expected_artifact_digests, "expected_artifact_digests"
    )
    actual_artifacts = _require_digest_map(
        actual_artifact_digests, "actual_artifact_digests"
    )

    required = tuple(required_classes)
    observed = tuple(observed_classes)
    if not required or any(
        not isinstance(item, str) or not item for item in required
    ):
        raise AttemptIntegrityError("required_classes must contain explicit names")
    if len(set(required)) != len(required):
        raise AttemptIntegrityError("required_classes must be unique")
    if any(not isinstance(item, str) or not item for item in observed):
        raise AttemptIntegrityError("observed_classes must contain explicit names")
    if len(set(observed)) != len(observed):
        raise AttemptIntegrityError("observed_classes must be unique")

    source_identity_match = actual_source_identity == expected_source_identity
    contract_digest_match = actual_contracts == expected_contracts
    artifact_digest_match = actual_artifacts == expected_artifacts
    required_classes_complete = set(observed) == set(required)

    valid = (
        source_identity_match
        and contract_digest_match
        and artifact_digest_match
        and required_classes_complete
    )
    status = "VALID_SYNTHETIC_ATTEMPT" if valid else "INVALID_SYNTHETIC_ATTEMPT"

    # The frozen contract prohibits retry once outcomes have been inspected.
    # Invalidity never overrides that prohibition.
    retry_allowed = not outcome_inspected

    return AttemptIntegrityReport(
        status=status,
        source_identity_match=source_identity_match,
        contract_digest_match=contract_digest_match,
        artifact_digest_match=artifact_digest_match,
        required_classes_complete=required_classes_complete,
        outcome_inspected=outcome_inspected,
        retry_allowed=retry_allowed,
    )


def require_retry_allowed(report: AttemptIntegrityReport) -> None:
    """Fail closed when a caller tries to retry after outcome inspection."""

    if report.outcome_inspected or not report.retry_allowed:
        raise AttemptIntegrityError("retry after outcome inspection is prohibited")
