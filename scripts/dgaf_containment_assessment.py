"""Assess explicit synthetic snapshots. Does not authenticate or enforce effects."""

import math
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from scripts.dgaf_capability_canonicalize import sha256_digest


class AssessmentInputError(ValueError):
    """Malformed synthetic assessment input."""


CONTRACT_KEYS = frozenset(
    {
        "schema_version",
        "contract_id",
        "definition_version",
        "subject_id",
        "session_id",
        "environment_id",
        "required_predicates",
        "max_age_seconds",
    }
)


def _strict_keys(value, keys, label):
    if not isinstance(value, Mapping):
        raise AssessmentInputError(f"{label} must be a mapping")
    if set(value) != keys:
        raise AssessmentInputError(f"{label} fields do not match the schema")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise AssessmentInputError(f"{label} must be nonempty text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise AssessmentInputError(f"{label} must be UTF-8 encodable") from exc


def _names(value, label, *, allow_empty=False):
    if not isinstance(value, list) or (not value and not allow_empty):
        raise AssessmentInputError(f"{label} must be a list")
    for name in value:
        _text(name, label)
    if len(set(value)) != len(value):
        raise AssessmentInputError(f"{label} contains duplicates")


def _validate_contract(contract):
    _strict_keys(contract, CONTRACT_KEYS, "contract")
    if contract["schema_version"] != "SYNTHETIC_CONTAINMENT_CONTRACT_V1":
        raise AssessmentInputError("unsupported contract schema")
    for key in ("contract_id", "definition_version", "subject_id", "session_id", "environment_id"):
        _text(contract[key], key)
    _names(contract["required_predicates"], "required_predicates")
    age = contract["max_age_seconds"]
    if type(age) not in (int, float):
        raise AssessmentInputError("max_age_seconds must be a finite positive number")
    try:
        valid = math.isfinite(age) and age > 0
    except OverflowError:
        valid = False
    if not valid:
        raise AssessmentInputError("max_age_seconds must be a finite positive number")


def contract_digest(contract: Mapping[str, Any]) -> str:
    _validate_contract(contract)
    return sha256_digest(dict(contract))


OBSERVATION_KEYS = frozenset(
    {
        "schema_version",
        "evidence_class",
        "subject_id",
        "session_id",
        "environment_id",
        "contract_digest",
        "observed_at",
        "time_basis",
        "predicate_results",
        "evidence_ids",
        "blocking_defeaters",
    }
)


def _utc(value, label):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise AssessmentInputError(f"{label} must be a timezone-aware datetime")
    try:
        return value.astimezone(timezone.utc)
    except (OverflowError, ValueError) as exc:
        raise AssessmentInputError(f"{label} cannot be normalized") from exc


def _timestamp(value):
    _text(value, "observed_at")
    match = re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
        r"(?:\.[0-9]{1,6})?(?:Z|[+-](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}))",
        value,
    )
    if match is None or (match["hour"] is not None and (int(match["hour"]) > 23 or int(match["minute"]) > 59)):
        raise AssessmentInputError("observed_at requires a valid offset timestamp with at most six fractional digits")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AssessmentInputError("observed_at is not ISO-8601") from exc
    return _utc(parsed, "observed_at")


def _iso(value):
    return value.isoformat().replace("+00:00", "Z")


def assess(contract: Mapping[str, Any], observation: Mapping[str, Any], *, now: datetime) -> dict[str, object]:
    """Check supplied synthetic data; establish no live containment or permission."""
    digest = contract_digest(contract)
    _strict_keys(observation, OBSERVATION_KEYS, "observation")
    if observation["schema_version"] != "SYNTHETIC_CONTAINMENT_OBSERVATION_V1":
        raise AssessmentInputError("unsupported observation schema")
    if observation["evidence_class"] != "SYNTHETIC" or observation["time_basis"] != "SNAPSHOT":
        raise AssessmentInputError("only SYNTHETIC SNAPSHOT evidence is accepted")
    for key in ("subject_id", "session_id", "environment_id"):
        _text(observation[key], key)
    supplied_digest = observation["contract_digest"]
    if not isinstance(supplied_digest, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", supplied_digest) is None:
        raise AssessmentInputError("contract_digest is malformed")
    predicates = observation["predicate_results"]
    _strict_keys(predicates, frozenset(contract["required_predicates"]), "predicate_results")
    for value in predicates.values():
        if not isinstance(value, str) or value not in ("ESTABLISHED", "CONTRADICTED", "UNKNOWN"):
            raise AssessmentInputError("invalid predicate state")
    _names(observation["evidence_ids"], "evidence_ids", allow_empty=True)
    _names(observation["blocking_defeaters"], "blocking_defeaters", allow_empty=True)
    observed_at = _timestamp(observation["observed_at"])
    assessed_at = _utc(now, "now")
    reasons = []
    binding_mismatch = supplied_digest != digest
    if binding_mismatch:
        reasons.append("CONTRACT_BINDING_MISMATCH")
    for key in ("subject_id", "session_id", "environment_id"):
        if observation[key] != contract[key]:
            binding_mismatch = True
            reasons.append("SCOPE_MISMATCH:" + key)
    age = (assessed_at - observed_at).total_seconds()
    if age < 0:
        reasons.append("FUTURE_SNAPSHOT")
    elif age > contract["max_age_seconds"]:
        reasons.append("STALE")
    if not observation["evidence_ids"]:
        reasons.append("NO_EVIDENCE")
    for name in contract["required_predicates"]:
        if predicates[name] != "ESTABLISHED":
            reasons.append(predicates[name] + ":" + name)
    reasons.extend("DEFEATER:" + reason for reason in observation["blocking_defeaters"])
    contradicted = any(value == "CONTRADICTED" for value in predicates.values()) or bool(
        observation["blocking_defeaters"]
    )
    if binding_mismatch:
        disposition = "NOT_ESTABLISHED"
    elif contradicted:
        disposition = "CONTRADICTED_IN_SCOPE"
    elif reasons:
        disposition = "NOT_ESTABLISHED"
    else:
        disposition = "ESTABLISHED_IN_SCOPE"
    return {
        "schema_version": "SYNTHETIC_CONTAINMENT_ASSESSMENT_V1",
        "evidence_class": "SYNTHETIC",
        "contract_digest": digest,
        "subject_id": contract["subject_id"],
        "session_id": contract["session_id"],
        "environment_id": contract["environment_id"],
        "observed_at": _iso(observed_at),
        "assessed_at": _iso(assessed_at),
        "time_basis": "SNAPSHOT",
        "disposition": disposition,
        "reasons": reasons,
        "predicate_results": dict(predicates),
        "evidence_ids": list(observation["evidence_ids"]),
        "blocking_defeaters": list(observation["blocking_defeaters"]),
        "authority_effect": "NONE",
        "follow_on_authority": "FRESH_ADJUDICATION_REQUIRED",
        "execution_permitted": False,
        "scientific_n_increment": 0,
    }
