"""Deterministic malformed-input corpus; operator-authored, not scientific N."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "experiments/governance_benchmark/fixtures_v1.json"
VALUES: list[Any] = [
    None,
    False,
    True,
    0,
    1,
    -1,
    1.2,
    "",
    "__ABSENT__",
    "INDEPENDENT_VALIDATION_ESTABLISHED",
    "CONFIDENTIAL",
    "EXTERNAL",
    [],
    {},
    ["EXTERNAL"],
]
FIELDS = [
    "action.authorized",
    "action.tool_allowed",
    "action.target_allowed",
    "authority_context.delegated_requester_authorized",
    "authority_context.token_replay_detected",
    "authority_context.request_bound_to_authorized_intent",
    "authority_context.workload_attested",
    "authority_context.child_scope_subset",
    "claim.evidence_present",
    "claim.evidence_fresh",
    "claim.requested_status",
    "claim.verification_class",
    "flow.provenance_known",
    "flow.source_classification",
    "flow.destination_class",
    "flow.composition_authorized",
]


def cases() -> list[dict[str, Any]]:
    """Reproduce the issue #1394 operator matrix (370 exact generated cases)."""
    baseline = json.loads(FIXTURES.read_text(encoding="utf-8"))["cases"][0]
    rows = [copy.deepcopy(baseline)]
    for top in ("action", "authority_context", "claim", "flow"):
        for value in VALUES:
            entry = copy.deepcopy(baseline)
            entry[top] = value
            rows.append(entry)
    for path in FIELDS:
        outer, key = path.split(".")
        for value in VALUES:
            entry = copy.deepcopy(baseline)
            if not isinstance(entry.get(outer), dict):
                entry[outer] = {}
            entry[outer][key] = value
            rows.append(entry)
    for present in (None, True, False):
        for fresh in (None, True, False):
            entry = copy.deepcopy(baseline)
            entry["claim"] = {}
            if present is not None:
                entry["claim"]["evidence_present"] = present
            if fresh is not None:
                entry["claim"]["evidence_fresh"] = fresh
            rows.append(entry)
    for source in ("CONFIDENTIAL", "RESTRICTED", "PUBLIC", 1, None):
        for target in ("EXTERNAL", "INTERNAL", True, None):
            for authority in (True, False, None):
                entry = copy.deepcopy(baseline)
                entry["flow"] = {"source_classification": source, "destination_class": target}
                if authority is not None:
                    entry["flow"]["composition_authorized"] = authority
                rows.append(entry)
    assert len(rows) == 370
    return rows
