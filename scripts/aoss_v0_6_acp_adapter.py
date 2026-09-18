"""Deterministic, non-authorizing ACP -> AOSS Stage A telemetry adapter."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

ADAPTER_VERSION = "AOSS_V0_6_ACP_ADAPTER_V1"
EXPECTED_SCHEMA = "agent-control-plane.provenance.v1"
SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"

KNOWN_EVENTS = {
    "task.started",
    "task.completed",
    "task.failed",
    "task.cancelled",
    "task.budget_exhausted",
    "task.denied",
    "task.rejected",
}


class AdapterError(ValueError):
    """Raised when the frozen ACP manifest contract is not satisfied."""


@dataclass(frozen=True)
class NormalizedEvent:
    trace_id: str
    observer_event_id: str
    source_event_id: None
    parent_event_id: None
    source_order_index: int
    component: str
    event_kind: str
    task_id: str
    capability: str | None
    state: str | None
    detail: str | None
    wall_time: str
    trust_domain: str
    source_repository: str
    source_commit: str
    adapter_version: str
    source_event_id_derivation: str
    parent_event_id_derivation: str
    source_order_derivation: str
    trust_domain_derivation: str
    validation_state: str
    authorization_state: str
    durable_attestation: str


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _observer_event_id(event: dict[str, Any], index: int) -> str:
    payload = {"source_order_index": index, "event": event}
    return "sha256:" + hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _parse_timestamp(value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise AdapterError("ACP timestamp missing or invalid")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AdapterError("ACP timestamp missing or invalid") from exc
    if parsed.tzinfo is None:
        raise AdapterError("ACP timestamp must be timezone-aware")


def normalize_manifest(manifest: dict[str, Any]) -> list[NormalizedEvent]:
    if not isinstance(manifest, dict):
        raise AdapterError("ACP manifest must be an object")
    if manifest.get("schema") != EXPECTED_SCHEMA:
        raise AdapterError("ACP provenance schema mismatch")

    run_id = manifest.get("run_id")
    events = manifest.get("events")
    event_count = manifest.get("event_count")

    if not isinstance(run_id, str) or not run_id.strip():
        raise AdapterError("ACP run_id missing or invalid")
    if not isinstance(events, list):
        raise AdapterError("ACP events must be a list")
    if event_count != len(events):
        raise AdapterError("ACP event_count mismatch")

    normalized: list[NormalizedEvent] = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise AdapterError(f"ACP event {index} is not an object")
        if event.get("run_id") != run_id:
            raise AdapterError(f"ACP event {index} run_id mismatch")

        event_kind = event.get("event")
        if event_kind not in KNOWN_EVENTS:
            raise AdapterError(f"ACP event {index} has unknown event kind")

        task_id = event.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise AdapterError(f"ACP event {index} task_id missing or invalid")

        _parse_timestamp(event.get("timestamp"))

        normalized.append(
            NormalizedEvent(
                trace_id=run_id,
                observer_event_id=_observer_event_id(event, index),
                source_event_id=None,
                parent_event_id=None,
                source_order_index=index,
                component="agent-control-plane",
                event_kind=event_kind,
                task_id=task_id,
                capability=event.get("capability"),
                state=event.get("state"),
                detail=event.get("detail"),
                wall_time=event["timestamp"],
                trust_domain="SYSTEM",
                source_repository=SOURCE_REPOSITORY,
                source_commit=SOURCE_COMMIT,
                adapter_version=ADAPTER_VERSION,
                source_event_id_derivation="UNMEASURED",
                parent_event_id_derivation="UNMEASURED",
                source_order_derivation="ADAPTER_DERIVED",
                trust_domain_derivation="ADAPTER_DERIVED",
                validation_state="UNMEASURED",
                authorization_state="UNMEASURED",
                durable_attestation="NOT_ESTABLISHED",
            )
        )

    return normalized


def normalized_digest(events: list[NormalizedEvent]) -> str:
    payload = [asdict(event) for event in events]
    return "sha256:" + hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def classify_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    events = normalize_manifest(manifest)
    kinds = [event.event_kind for event in events]

    terminal = None
    for candidate in (
        "task.completed",
        "task.failed",
        "task.cancelled",
        "task.budget_exhausted",
        "task.denied",
        "task.rejected",
    ):
        if candidate in kinds:
            terminal = candidate

    return {
        "adapter_version": ADAPTER_VERSION,
        "normalized_digest": normalized_digest(events),
        "event_count": len(events),
        "terminal_event": terminal,
        "has_unmeasured_authority": all(
            event.authorization_state == "UNMEASURED" for event in events
        ),
        "has_unmeasured_validation": all(
            event.validation_state == "UNMEASURED" for event in events
        ),
        "parent_lineage_measured": False,
        "source_native_event_ids_present": False,
        "durable_attestation_established": False,
        "events": [asdict(event) for event in events],
    }
