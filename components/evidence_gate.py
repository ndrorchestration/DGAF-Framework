"""Framework-neutral, non-authorizing evidence admission core.

Evidence Gate verifies evidence bytes, exact target/provenance bindings, and
claim-scope constraints. It never authorizes downstream execution or state
transitions.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

EVIDENCE_GATE_SCHEMA_VERSION = "dgaf.evidence-gate.v0-candidate"
AUTHORIZATION_EFFECT_NONE = "NONE"

Check = Callable[["EvidenceObject", "EvidenceTarget", "ProvenanceBinding", "ClaimScope"], bool]
HistoricalTransferCheck = Callable[
    ["EvidenceTarget", "EvidenceTarget", "EvidenceObject", "ProvenanceBinding", "ClaimScope"],
    bool,
]


def _required(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be blank")
    return value.strip()


class EvidenceAdmissionReason(str, Enum):
    EVIDENCE_MISSING_OR_INVALID = "EVIDENCE_MISSING_OR_INVALID"
    DIGEST_MISMATCH = "DIGEST_MISMATCH"
    TARGET_IDENTITY_MISMATCH = "TARGET_IDENTITY_MISMATCH"
    SOURCE_IDENTITY_MISMATCH = "SOURCE_IDENTITY_MISMATCH"
    ENVIRONMENT_IDENTITY_MISMATCH = "ENVIRONMENT_IDENTITY_MISMATCH"
    PROVENANCE_CLASS_MISMATCH = "PROVENANCE_CLASS_MISMATCH"
    RECEIPT_MISMATCH = "RECEIPT_MISMATCH"
    MANIFEST_MISMATCH = "MANIFEST_MISMATCH"
    CONTENT_SET_MISMATCH = "CONTENT_SET_MISMATCH"
    CUSTODY_REQUIREMENT_UNSATISFIED = "CUSTODY_REQUIREMENT_UNSATISFIED"
    CLAIM_SCOPE_MISSING = "CLAIM_SCOPE_MISSING"
    CLAIM_SCOPE_EXCEEDS_EVIDENCE = "CLAIM_SCOPE_EXCEEDS_EVIDENCE"
    HISTORICAL_TRANSFER_NOT_ESTABLISHED = "HISTORICAL_TRANSFER_NOT_ESTABLISHED"
    REQUIRED_CHECK_UNAVAILABLE = "REQUIRED_CHECK_UNAVAILABLE"
    ADMITTED = "ADMITTED"


@dataclass(frozen=True)
class EvidenceObject:
    evidence_id: str
    evidence_type: str
    digest_algorithm: str
    content_digest: str
    source_class: str
    produced_at: Optional[str] = None
    observed_at: Optional[str] = None
    retained_reference: Optional[str] = None

    def __post_init__(self) -> None:
        for field_name in (
            "evidence_id",
            "evidence_type",
            "digest_algorithm",
            "content_digest",
            "source_class",
        ):
            object.__setattr__(self, field_name, _required(getattr(self, field_name), field_name))
        algorithm = self.digest_algorithm.lower()
        object.__setattr__(self, "digest_algorithm", algorithm)
        if algorithm != "sha256":
            raise ValueError("Evidence Gate v0 supports sha256 only")
        if len(self.content_digest) != 64:
            raise ValueError("content_digest must be a 64-character sha256 hex digest")
        try:
            int(self.content_digest, 16)
        except ValueError as exc:
            raise ValueError("content_digest must be hexadecimal") from exc
        for field_name in ("produced_at", "observed_at", "retained_reference"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _required(value, field_name))


@dataclass(frozen=True)
class EvidenceTarget:
    target_type: str
    target_id: str
    scope_id: str
    source_revision: Optional[str] = None
    tree_identity: Optional[str] = None
    build_identity: Optional[str] = None
    environment_identity: Optional[str] = None
    config_identity: Optional[str] = None

    def __post_init__(self) -> None:
        for field_name in ("target_type", "target_id", "scope_id"):
            object.__setattr__(self, field_name, _required(getattr(self, field_name), field_name))
        for field_name in (
            "source_revision",
            "tree_identity",
            "build_identity",
            "environment_identity",
            "config_identity",
        ):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _required(value, field_name))


@dataclass(frozen=True)
class ProvenanceBinding:
    producer_class: str
    custody_class: str
    source_identity: Optional[str] = None
    runtime_identity: Optional[str] = None
    environment_identity: Optional[str] = None
    receipt_identity: Optional[str] = None
    manifest_identity: Optional[str] = None
    provider_identity: Optional[str] = None
    workflow_identity: Optional[str] = None
    artifact_identity: Optional[str] = None

    def __post_init__(self) -> None:
        for field_name in ("producer_class", "custody_class"):
            object.__setattr__(self, field_name, _required(getattr(self, field_name), field_name))
        for field_name in (
            "source_identity",
            "runtime_identity",
            "environment_identity",
            "receipt_identity",
            "manifest_identity",
            "provider_identity",
            "workflow_identity",
            "artifact_identity",
        ):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _required(value, field_name))


@dataclass(frozen=True)
class ClaimScope:
    claim_id: str
    claim_class: str
    scope_id: str
    evidence_class: str
    limitations: tuple[str, ...] = ()
    non_transfer: bool = True
    excluded_claims: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("claim_id", "claim_class", "scope_id", "evidence_class"):
            object.__setattr__(self, field_name, _required(getattr(self, field_name), field_name))
        object.__setattr__(
            self,
            "limitations",
            tuple(_required(item, "limitations item") for item in self.limitations),
        )
        object.__setattr__(
            self,
            "excluded_claims",
            tuple(_required(item, "excluded_claims item") for item in self.excluded_claims),
        )


@dataclass(frozen=True)
class EvidenceAdmissionReceipt:
    admitted: bool
    reason_code: EvidenceAdmissionReason
    evidence_id: str
    target_type: str
    target_id: str
    scope_id: str
    verified_digest: Optional[str]
    provenance_class: str
    claim_id: str
    claim_class: str
    evidence_class: str
    claim_ceiling: tuple[str, ...]
    digest_checked: bool = False
    target_checked: bool = False
    source_checked: bool = False
    environment_checked: bool = False
    provenance_checked: bool = False
    receipt_checked: bool = False
    manifest_checked: bool = False
    content_set_checked: bool = False
    custody_checked: bool = False
    claim_scope_checked: bool = False
    historical_transfer_checked: bool = False
    authorization_effect: str = AUTHORIZATION_EFFECT_NONE
    schema_version: str = EVIDENCE_GATE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.authorization_effect != AUTHORIZATION_EFFECT_NONE:
            raise ValueError("Evidence Gate never grants authorization")
        if not isinstance(self.reason_code, EvidenceAdmissionReason):
            raise ValueError("reason_code must be EvidenceAdmissionReason")


def _receipt(
    evidence: EvidenceObject,
    target: EvidenceTarget,
    provenance: ProvenanceBinding,
    claim_scope: ClaimScope,
    *,
    admitted: bool,
    reason_code: EvidenceAdmissionReason,
    verified_digest: Optional[str] = None,
    digest_checked: bool = False,
    target_checked: bool = False,
    source_checked: bool = False,
    environment_checked: bool = False,
    provenance_checked: bool = False,
    receipt_checked: bool = False,
    manifest_checked: bool = False,
    content_set_checked: bool = False,
    custody_checked: bool = False,
    claim_scope_checked: bool = False,
    historical_transfer_checked: bool = False,
) -> EvidenceAdmissionReceipt:
    return EvidenceAdmissionReceipt(
        admitted=admitted,
        reason_code=reason_code,
        evidence_id=evidence.evidence_id,
        target_type=target.target_type,
        target_id=target.target_id,
        scope_id=target.scope_id,
        verified_digest=verified_digest,
        provenance_class=provenance.producer_class,
        claim_id=claim_scope.claim_id,
        claim_class=claim_scope.claim_class,
        evidence_class=claim_scope.evidence_class,
        claim_ceiling=tuple(claim_scope.excluded_claims),
        digest_checked=digest_checked,
        target_checked=target_checked,
        source_checked=source_checked,
        environment_checked=environment_checked,
        provenance_checked=provenance_checked,
        receipt_checked=receipt_checked,
        manifest_checked=manifest_checked,
        content_set_checked=content_set_checked,
        custody_checked=custody_checked,
        claim_scope_checked=claim_scope_checked,
        historical_transfer_checked=historical_transfer_checked,
    )


def _run_required_check(
    checker: Optional[Check],
    evidence: EvidenceObject,
    target: EvidenceTarget,
    provenance: ProvenanceBinding,
    claim_scope: ClaimScope,
) -> Optional[bool]:
    if checker is None:
        return None
    try:
        return checker(evidence, target, provenance, claim_scope) is True
    except Exception:
        return False


def admit_evidence(
    evidence: EvidenceObject,
    target: EvidenceTarget,
    provenance: ProvenanceBinding,
    claim_scope: ClaimScope,
    *,
    evidence_bytes: Optional[bytes],
    expected_target: EvidenceTarget,
    required_producer_class: Optional[str] = None,
    receipt_checker: Optional[Check] = None,
    manifest_checker: Optional[Check] = None,
    content_set_checker: Optional[Check] = None,
    custody_checker: Optional[Check] = None,
    claim_scope_checker: Optional[Check] = None,
    historical_transfer_checker: Optional[HistoricalTransferCheck] = None,
) -> EvidenceAdmissionReceipt:
    """Admit evidence for one exact target/scope without granting authority."""

    if not isinstance(evidence, EvidenceObject):
        raise TypeError("evidence must be EvidenceObject")
    if not isinstance(target, EvidenceTarget):
        raise TypeError("target must be EvidenceTarget")
    if not isinstance(expected_target, EvidenceTarget):
        raise TypeError("expected_target must be EvidenceTarget")
    if not isinstance(provenance, ProvenanceBinding):
        raise TypeError("provenance must be ProvenanceBinding")
    if not isinstance(claim_scope, ClaimScope):
        raise TypeError("claim_scope must be ClaimScope")

    if evidence_bytes is None or not isinstance(evidence_bytes, (bytes, bytearray)):
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.EVIDENCE_MISSING_OR_INVALID,
        )

    digest = hashlib.sha256(bytes(evidence_bytes)).hexdigest()
    if digest != evidence.content_digest:
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.DIGEST_MISMATCH,
            verified_digest=digest,
            digest_checked=True,
        )

    common = dict(verified_digest=digest, digest_checked=True)

    target_checked = True
    if target.target_type != expected_target.target_type or target.scope_id != expected_target.scope_id:
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.TARGET_IDENTITY_MISMATCH,
            target_checked=target_checked,
            **common,
        )

    historical_transfer_checked = False
    if target.target_id != expected_target.target_id:
        historical_transfer_checked = True
        if historical_transfer_checker is None:
            return _receipt(
                evidence,
                target,
                provenance,
                claim_scope,
                admitted=False,
                reason_code=EvidenceAdmissionReason.HISTORICAL_TRANSFER_NOT_ESTABLISHED,
                target_checked=target_checked,
                historical_transfer_checked=True,
                **common,
            )
        try:
            transfer_ok = historical_transfer_checker(
                target,
                expected_target,
                evidence,
                provenance,
                claim_scope,
            )
        except Exception:
            transfer_ok = False
        if transfer_ok is not True:
            return _receipt(
                evidence,
                target,
                provenance,
                claim_scope,
                admitted=False,
                reason_code=EvidenceAdmissionReason.HISTORICAL_TRANSFER_NOT_ESTABLISHED,
                target_checked=target_checked,
                historical_transfer_checked=True,
                **common,
            )

    source_checked = any(
        value is not None
        for value in (
            expected_target.source_revision,
            expected_target.tree_identity,
            expected_target.build_identity,
            expected_target.config_identity,
        )
    )
    for field_name in ("source_revision", "tree_identity", "build_identity", "config_identity"):
        expected = getattr(expected_target, field_name)
        if expected is not None and getattr(target, field_name) != expected:
            return _receipt(
                evidence,
                target,
                provenance,
                claim_scope,
                admitted=False,
                reason_code=EvidenceAdmissionReason.SOURCE_IDENTITY_MISMATCH,
                target_checked=target_checked,
                source_checked=source_checked,
                historical_transfer_checked=historical_transfer_checked,
                **common,
            )

    environment_checked = expected_target.environment_identity is not None
    if (
        expected_target.environment_identity is not None
        and target.environment_identity != expected_target.environment_identity
    ):
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.ENVIRONMENT_IDENTITY_MISMATCH,
            target_checked=target_checked,
            source_checked=source_checked,
            environment_checked=environment_checked,
            historical_transfer_checked=historical_transfer_checked,
            **common,
        )

    provenance_checked = required_producer_class is not None
    if required_producer_class is not None and provenance.producer_class != required_producer_class:
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.PROVENANCE_CLASS_MISMATCH,
            target_checked=target_checked,
            source_checked=source_checked,
            environment_checked=environment_checked,
            provenance_checked=True,
            historical_transfer_checked=historical_transfer_checked,
            **common,
        )

    checker_specs = (
        ("receipt_checked", receipt_checker, EvidenceAdmissionReason.RECEIPT_MISMATCH),
        ("manifest_checked", manifest_checker, EvidenceAdmissionReason.MANIFEST_MISMATCH),
        ("content_set_checked", content_set_checker, EvidenceAdmissionReason.CONTENT_SET_MISMATCH),
        (
            "custody_checked",
            custody_checker,
            EvidenceAdmissionReason.CUSTODY_REQUIREMENT_UNSATISFIED,
        ),
    )
    flags = {
        "receipt_checked": False,
        "manifest_checked": False,
        "content_set_checked": False,
        "custody_checked": False,
    }
    for flag_name, checker, failure_reason in checker_specs:
        if checker is None:
            continue
        flags[flag_name] = True
        result = _run_required_check(checker, evidence, target, provenance, claim_scope)
        if result is not True:
            return _receipt(
                evidence,
                target,
                provenance,
                claim_scope,
                admitted=False,
                reason_code=failure_reason,
                target_checked=target_checked,
                source_checked=source_checked,
                environment_checked=environment_checked,
                provenance_checked=provenance_checked,
                historical_transfer_checked=historical_transfer_checked,
                **flags,
                **common,
            )

    if not claim_scope.claim_id or not claim_scope.scope_id:
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.CLAIM_SCOPE_MISSING,
            target_checked=target_checked,
            source_checked=source_checked,
            environment_checked=environment_checked,
            provenance_checked=provenance_checked,
            historical_transfer_checked=historical_transfer_checked,
            **flags,
            **common,
        )

    claim_scope_checked = True
    if claim_scope.scope_id != expected_target.scope_id:
        return _receipt(
            evidence,
            target,
            provenance,
            claim_scope,
            admitted=False,
            reason_code=EvidenceAdmissionReason.CLAIM_SCOPE_EXCEEDS_EVIDENCE,
            target_checked=target_checked,
            source_checked=source_checked,
            environment_checked=environment_checked,
            provenance_checked=provenance_checked,
            claim_scope_checked=True,
            historical_transfer_checked=historical_transfer_checked,
            **flags,
            **common,
        )
    if claim_scope_checker is not None:
        result = _run_required_check(
            claim_scope_checker,
            evidence,
            target,
            provenance,
            claim_scope,
        )
        if result is not True:
            return _receipt(
                evidence,
                target,
                provenance,
                claim_scope,
                admitted=False,
                reason_code=EvidenceAdmissionReason.CLAIM_SCOPE_EXCEEDS_EVIDENCE,
                target_checked=target_checked,
                source_checked=source_checked,
                environment_checked=environment_checked,
                provenance_checked=provenance_checked,
                claim_scope_checked=True,
                historical_transfer_checked=historical_transfer_checked,
                **flags,
                **common,
            )

    return _receipt(
        evidence,
        target,
        provenance,
        claim_scope,
        admitted=True,
        reason_code=EvidenceAdmissionReason.ADMITTED,
        target_checked=target_checked,
        source_checked=source_checked,
        environment_checked=environment_checked,
        provenance_checked=provenance_checked,
        claim_scope_checked=claim_scope_checked,
        historical_transfer_checked=historical_transfer_checked,
        **flags,
        **common,
    )
