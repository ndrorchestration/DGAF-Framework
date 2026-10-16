"""Bind synthetic JSON bytes to a caller-supplied pin; do not authenticate sources."""

import hashlib
import hmac
import json
import re
from collections.abc import Mapping
from datetime import datetime

from scripts.dgaf_containment_assessment import AssessmentInputError, assess

MAX_OBSERVATION_BYTES = 65536


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssessmentInputError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value):
    raise AssessmentInputError("non-finite JSON constant")


def assess_bound_snapshot(
    contract: Mapping[str, object],
    observation_bytes: bytes,
    *,
    expected_observation_digest: str | None,
    now: datetime,
) -> dict[str, object]:
    """Check exact-byte integrity relative to an external pin, then assess.

    The caller must obtain the expected digest outside the submitted record.
    This function does not establish how that pin or producer was trusted.
    """
    if not isinstance(observation_bytes, bytes) or not 0 < len(observation_bytes) <= MAX_OBSERVATION_BYTES:
        raise AssessmentInputError("observation requires 1–65536 raw bytes")
    if (
        not isinstance(expected_observation_digest, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", expected_observation_digest) is None
    ):
        raise AssessmentInputError("separately supplied expected observation digest is required")
    actual = "sha256:" + hashlib.sha256(observation_bytes).hexdigest()
    if not hmac.compare_digest(actual, expected_observation_digest):
        raise AssessmentInputError("observation integrity binding mismatch")
    try:
        observation = json.loads(
            observation_bytes.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise AssessmentInputError("observation is not supported UTF-8 JSON") from exc
    result = assess(contract, observation, now=now)
    return {
        **result,
        "observation_digest": actual,
        "integrity_binding": "EXPECTED_DIGEST_MATCH",
        "source_authenticity": "NOT_ESTABLISHED",
    }
