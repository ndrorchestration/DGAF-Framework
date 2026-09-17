"""Provider-neutral, non-authoritative external runtime ingress validation.

Admission here means only that an external submission is acceptable as a DGAF
input record. It never grants execution authority, verification, empirical
support, or any scientific-state transition.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1"
RESULT_VERSION = "DGAF_EXTERNAL_RUNTIME_ADMISSION_V1"
TRUST_CLASS = "EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED"
AUTHORITY_STATUS = "PRESENTED_NOT_GRANTED"
DGAF_VERIFICATION_CLASS = "UNVERIFIED_EXTERNAL_ASSERTION"
FRESHNESS_SECONDS = 3600

TOP_LEVEL_FIELDS = (
    "schema_version",
    "provider",
    "identity",
    "evidence",
    "provenance",
    "request",
    "assertions",
    "risk",
)
PROVIDER_FIELDS = ("provider_id", "runtime_id", "adapter_id", "adapter_version")
IDENTITY_FIELDS = ("event_id", "effect_id", "source_id")
EVIDENCE_FIELDS = ("evidence_class", "observed_at", "content_digest", "payload")
PROVENANCE_FIELDS = ("producer_id", "producer_run_id", "source_bindings")
REQUEST_FIELDS = ("action_class", "requested_transition")
ASSERTION_FIELDS = ("verification_class", "authority")
RISK_FIELDS = ("consequence_class", "reversibility")

ALLOWED_ACTION_TRANSITIONS = {
    "NON_CONSEQUENTIAL_RECORD_INGRESS": {"RECORD_ONLY"},
    "CONSEQUENTIAL_ACTION_REQUEST": {"REQUEST_ACTION_ADMISSION"},
}
RESERVED_PROVIDER_PREFIXES = ("dgaf-", "dgaf_")
OPAQUE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_bytes(value)).hexdigest()


def canonical_envelope_digest(envelope: dict[str, Any]) -> str:
    """Return the deterministic content identity for one envelope."""

    return _sha256(envelope)


def _reject(code: str, stage: str, effect_id: str | None = None) -> dict[str, Any]:
    return {
        "admitted": False,
        "result_version": RESULT_VERSION,
        "record_id": None,
        "effect_id": effect_id,
        "trust_class": TRUST_CLASS,
        "dgaf_evidence_class": "UNCLASSIFIED_EXTERNAL_INPUT",
        "dgaf_verification_class": DGAF_VERIFICATION_CLASS,
        "authority_status": AUTHORITY_STATUS,
        "reason_codes": [code],
        "failed_stage": stage,
    }


def _missing_fields(data: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if field not in data]


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_opaque_id(value: Any) -> bool:
    return _is_nonempty_string(value) and bool(OPAQUE_ID.fullmatch(value))


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate_external_runtime_envelope(
    envelope: dict[str, Any],
    *,
    seen_effect_ids: set[str] | None = None,
    seen_events: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate and normalize one external runtime submission fail-closed."""

    if not isinstance(envelope, dict):
        return _reject("DGAF_EXT_TYPE_INVALID", "SCHEMA_AND_REQUIRED_FIELDS")

    effect_id = None
    identity_obj = envelope.get("identity")
    if isinstance(identity_obj, dict):
        candidate_effect = identity_obj.get("effect_id")
        if isinstance(candidate_effect, str):
            effect_id = candidate_effect

    if envelope.get("schema_version") != SCHEMA_VERSION:
        return _reject("DGAF_EXT_SCHEMA_UNSUPPORTED", "SCHEMA_AND_REQUIRED_FIELDS", effect_id)
    if _missing_fields(envelope, TOP_LEVEL_FIELDS):
        return _reject("DGAF_EXT_REQUIRED_FIELD_MISSING", "SCHEMA_AND_REQUIRED_FIELDS", effect_id)

    object_fields = ("provider", "identity", "evidence", "provenance", "request", "assertions", "risk")
    if any(not isinstance(envelope[field], dict) for field in object_fields):
        return _reject("DGAF_EXT_TYPE_INVALID", "STRUCTURAL_TYPES", effect_id)

    provider = envelope["provider"]
    identity = envelope["identity"]
    evidence = envelope["evidence"]
    provenance = envelope["provenance"]
    request = envelope["request"]
    assertions = envelope["assertions"]
    risk = envelope["risk"]

    nested_requirements = (
        (provider, PROVIDER_FIELDS),
        (identity, IDENTITY_FIELDS),
        (evidence, EVIDENCE_FIELDS),
        (provenance, PROVENANCE_FIELDS),
        (request, REQUEST_FIELDS),
        (assertions, ASSERTION_FIELDS),
        (risk, RISK_FIELDS),
    )
    if any(_missing_fields(obj, fields) for obj, fields in nested_requirements):
        return _reject("DGAF_EXT_REQUIRED_FIELD_MISSING", "SCHEMA_AND_REQUIRED_FIELDS", effect_id)

    if any(not _valid_opaque_id(provider[field]) for field in PROVIDER_FIELDS):
        return _reject("DGAF_EXT_IDENTITY_MALFORMED", "PROVIDER_RUNTIME_ADAPTER_IDENTITY", effect_id)
    provider_id = provider["provider_id"]
    if provider_id.lower().startswith(RESERVED_PROVIDER_PREFIXES):
        return _reject("DGAF_EXT_PROVIDER_SUBSTITUTION", "PROVIDER_RUNTIME_ADAPTER_IDENTITY", effect_id)

    if not _valid_opaque_id(identity["event_id"]) or not _valid_opaque_id(identity["effect_id"]):
        return _reject("DGAF_EXT_IDENTITY_MALFORMED", "EVENT_EFFECT_SOURCE_IDENTITY", effect_id)
    if not _valid_opaque_id(identity["source_id"]):
        return _reject("DGAF_EXT_SOURCE_IDENTITY_INVALID", "EVENT_EFFECT_SOURCE_IDENTITY", effect_id)

    event_id = identity["event_id"]
    effect_id = identity["effect_id"]
    if seen_events is not None and event_id in seen_events:
        if seen_events[event_id] != canonical_envelope_digest(envelope):
            return _reject("DGAF_EXT_EVENT_IDENTITY_COLLISION", "EVENT_EFFECT_SOURCE_IDENTITY", effect_id)

    if not _is_nonempty_string(evidence["evidence_class"]):
        return _reject("DGAF_EXT_TYPE_INVALID", "EVIDENCE_DIGEST_AND_PROVENANCE", effect_id)
    digest = evidence["content_digest"]
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        return _reject("DGAF_EXT_EVIDENCE_DIGEST_MISMATCH", "EVIDENCE_DIGEST_AND_PROVENANCE", effect_id)
    if digest != _sha256(evidence["payload"]):
        return _reject("DGAF_EXT_EVIDENCE_DIGEST_MISMATCH", "EVIDENCE_DIGEST_AND_PROVENANCE", effect_id)

    source_bindings = provenance["source_bindings"]
    if (
        not _valid_opaque_id(provenance["producer_id"])
        or not _valid_opaque_id(provenance["producer_run_id"])
        or not isinstance(source_bindings, list)
        or identity["source_id"] not in source_bindings
        or any(not _valid_opaque_id(item) for item in source_bindings)
    ):
        return _reject("DGAF_EXT_PROVENANCE_INVALID", "EVIDENCE_DIGEST_AND_PROVENANCE", effect_id)

    observed_at = _parse_timestamp(evidence["observed_at"])
    if observed_at is None:
        return _reject("DGAF_EXT_TYPE_INVALID", "FRESHNESS", effect_id)
    current_time = now or datetime.now(timezone.utc)
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    current_time = current_time.astimezone(timezone.utc)
    age_seconds = (current_time - observed_at).total_seconds()
    if age_seconds < 0 or age_seconds > FRESHNESS_SECONDS:
        return _reject("DGAF_EXT_EVIDENCE_STALE", "FRESHNESS", effect_id)

    action_class = request["action_class"]
    transition = request["requested_transition"]
    if action_class not in ALLOWED_ACTION_TRANSITIONS:
        return _reject("DGAF_EXT_ACTION_CLASS_UNSUPPORTED", "ACTION_AND_TRANSITION_SUPPORT", effect_id)
    if transition not in ALLOWED_ACTION_TRANSITIONS[action_class]:
        return _reject("DGAF_EXT_TRANSITION_UNSUPPORTED", "ACTION_AND_TRANSITION_SUPPORT", effect_id)

    authority = assertions["authority"]
    if not isinstance(authority, dict):
        return _reject("DGAF_EXT_TYPE_INVALID", "AUTHORITY_COMPATIBILITY", effect_id)
    authority_status = authority.get("status")
    if isinstance(authority_status, str) and authority_status.startswith("DGAF_"):
        return _reject("DGAF_EXT_AUTHORITY_MISMATCH", "AUTHORITY_COMPATIBILITY", effect_id)

    if action_class == "CONSEQUENTIAL_ACTION_REQUEST":
        if risk["consequence_class"] in ("UNKNOWN", "NOT_APPLICABLE", "") or risk["reversibility"] in (
            "UNKNOWN",
            "NOT_APPLICABLE",
            "",
        ):
            return _reject("DGAF_EXT_RISK_METADATA_REQUIRED", "CONSEQUENCE_AND_REVERSIBILITY", effect_id)

    if seen_effect_ids is not None and effect_id in seen_effect_ids:
        return _reject("DGAF_EXT_DUPLICATE_EFFECT", "REPLAY_AND_DUPLICATE_EFFECT", effect_id)

    normalized = deepcopy(envelope)
    record_id = canonical_envelope_digest(normalized)
    return {
        "admitted": True,
        "result_version": RESULT_VERSION,
        "record_id": record_id,
        "effect_id": effect_id,
        "trust_class": TRUST_CLASS,
        "dgaf_evidence_class": evidence["evidence_class"],
        "dgaf_verification_class": DGAF_VERIFICATION_CLASS,
        "authority_status": AUTHORITY_STATUS,
        "requested_action_class": action_class,
        "requested_transition": transition,
        "external_assertions": deepcopy(assertions),
        "normalized_envelope": normalized,
        "reason_codes": [],
    }
