"""Bounded Mode-T external-retention evidence contract.

This module deliberately separates transparency-log inclusion / anti-deletion evidence
from temporal-order evidence. A Rekor/Sigstore verification result can support that a
specific public record is signed and included under an expected identity, but Rekor v1
``integratedTime`` is not treated as an independently verifiable wall-clock proof.

The module consumes already-verified, non-secret external evidence metadata; it is not
itself a Sigstore cryptographic verifier or time authority. Therefore a PASS here does
not establish real P6 retention, L-before-release ordering, P4, freeze, authorization,
or empirical execution.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_RECORD_TYPES = frozenset(
    {
        "PDMAL_MODE_T_RUN_RESERVATION",
        "PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION",
        "PDMAL_P4_T_EXECUTION",
        "PDMAL_P4_T_ANALYSIS_LOCK",
    }
)
EXPECTED_OIDC_ISSUER = "https://token.actions.githubusercontent.com"


class RetentionContractError(ValueError):
    """Raised when normalized external-retention evidence fails closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RetentionContractError(message)


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} must be non-empty")
    return value


@dataclass(frozen=True)
class TransparencyExpectation:
    """Exact public record and identity values fixed before evidence acceptance."""

    record_type: str
    record_sha256: str
    certificate_identity: str
    oidc_issuer: str = EXPECTED_OIDC_ISSUER


@dataclass(frozen=True)
class VerifiedTransparencyContext:
    """Normalized result from a separate Sigstore-capable cryptographic verifier.

    ``integrated_time_unix`` is retained as log metadata only. It is never accepted
    as independent temporal proof by this contract.
    """

    signature_verified: bool
    certificate_chain_verified: bool
    certificate_identity_verified: bool
    transparency_inclusion_verified: bool
    signed_entry_timestamp_verified: bool
    bundle_sha256: str
    log_entry_uuid: str
    log_index: int
    integrated_time_unix: int | None
    verified_record_sha256: str
    certificate_identity: str
    oidc_issuer: str


def verify_transparency_inclusion(
    expectation: TransparencyExpectation,
    context: VerifiedTransparencyContext,
) -> dict[str, Any]:
    """Verify exact normalized inclusion evidence without promoting log time."""
    _require(expectation.record_type in _ALLOWED_RECORD_TYPES, "unsupported Mode-T record type")
    expected_record = _sha(expectation.record_sha256, "expected record SHA-256")
    expected_identity = _string(expectation.certificate_identity, "expected certificate identity")
    _require(
        expectation.oidc_issuer == EXPECTED_OIDC_ISSUER,
        "unexpected transparency signing OIDC issuer expectation",
    )

    _require(context.signature_verified is True, "artifact signature is not verified")
    _require(context.certificate_chain_verified is True, "Sigstore certificate chain is not verified")
    _require(context.certificate_identity_verified is True, "certificate identity is not verified")
    _require(context.transparency_inclusion_verified is True, "transparency-log inclusion is not verified")
    _require(context.signed_entry_timestamp_verified is True, "signed entry timestamp is not verified")
    bundle_sha = _sha(context.bundle_sha256, "bundle SHA-256")
    verified_record = _sha(context.verified_record_sha256, "verified record SHA-256")
    _require(verified_record == expected_record, "verified record digest mismatch")
    _require(context.certificate_identity == expected_identity, "certificate identity mismatch")
    _require(context.oidc_issuer == expectation.oidc_issuer, "certificate OIDC issuer mismatch")
    _require(isinstance(context.log_entry_uuid, str) and bool(context.log_entry_uuid), "log entry UUID missing")
    _require(
        isinstance(context.log_index, int)
        and not isinstance(context.log_index, bool)
        and context.log_index >= 0,
        "log index must be a non-negative integer",
    )
    if context.integrated_time_unix is not None:
        _require(
            isinstance(context.integrated_time_unix, int)
            and not isinstance(context.integrated_time_unix, bool)
            and context.integrated_time_unix >= 0,
            "integratedTime must be a non-negative integer when retained",
        )

    return {
        "retention_contract": "PASS_NORMALIZED_INCLUSION_ONLY",
        "record_type": expectation.record_type,
        "record_sha256": expected_record,
        "bundle_sha256": bundle_sha,
        "log_entry_uuid": context.log_entry_uuid,
        "log_index": context.log_index,
        "certificate_identity": expected_identity,
        "oidc_issuer": expectation.oidc_issuer,
        "signature_verified": True,
        "certificate_chain_verified": True,
        "transparency_inclusion_verified": True,
        "signed_entry_timestamp_verified": True,
        "integrated_time_unix_metadata_only": context.integrated_time_unix,
        "anti_deletion_inclusion_evidence": "VERIFIED_NORMALIZED",
        "temporal_order_verified": False,
        "temporal_order_reason": "REKOR_INTEGRATED_TIME_NOT_ACCEPTED_AS_INDEPENDENT_TIME_AUTHORITY",
        "external_sigstore_crypto_performed_by_this_module": False,
        "real_external_retention_established": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }


def verify_analysis_lock_temporal_order(
    inclusion_evidence: Mapping[str, Any],
    *,
    independent_time_order_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Fail closed unless a separately defined independent time mechanism exists.

    No independent time-order mechanism is approved in this implementation tranche,
    so callers cannot turn Rekor metadata into L-before-release PASS by supplying a
    timestamp-like dictionary.
    """
    _require(
        isinstance(inclusion_evidence, Mapping)
        and inclusion_evidence.get("retention_contract") == "PASS_NORMALIZED_INCLUSION_ONLY",
        "analysis-lock inclusion evidence is not accepted",
    )
    _require(
        inclusion_evidence.get("record_type") == "PDMAL_P4_T_ANALYSIS_LOCK",
        "temporal-order check requires an analysis-lock record",
    )
    if independent_time_order_evidence is not None:
        raise RetentionContractError(
            "no independent temporal-order authority is approved in this contract version"
        )
    return {
        "analysis_lock_inclusion_verified": True,
        "temporal_order_verified": False,
        "temporal_order_status": "OPEN",
        "reason": "SEPARATE_INDEPENDENT_TIME_OR_ORDER_MECHANISM_REQUIRED",
        "rekor_integrated_time_promoted": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
