"""Fail-closed validator for the replay-only Tektite DGAF -> ACP trace.

This validates a static public projection of already accepted bounded semantics.
It does not execute ACP, authorize mutation, or establish cross-system runtime
integration.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "TEKTITE_DGAF_ACP_REPLAY_TRACE_V0"
EVIDENCE_CLASS = "STATIC_REPLAY_OF_ACCEPTED_BOUNDED_SEMANTICS"

DGAF_AUTHORITY_COMMIT = "afa078fade63c280208ffae6abafa7a110b9860d"
DGAF_TEKTITE_COMMIT = "45dcf701c63812e9484d98e2cf3e8e8368aeab78"
ACP_EXECUTION_COMMIT = "cad2ef94f1a690deee741b81ea8bfab8c248cd7d"

EXPECTED_BOUNDARY = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
    "production_execution": "NOT_ESTABLISHED",
    "generalized_usability": "NOT_ESTABLISHED",
}


class ReplayTraceValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayTraceValidationError(message)


def _object(trace: dict[str, Any], key: str) -> dict[str, Any]:
    value = trace.get(key)
    if not isinstance(value, dict):
        raise ReplayTraceValidationError(f"{key} must be an object")
    return value


def validate_trace(trace: dict[str, Any]) -> None:
    _require(trace.get("schema_version") == SCHEMA_VERSION, "schema_version mismatch")
    _require(trace.get("evidence_class") == EVIDENCE_CLASS, "evidence_class mismatch")
    _require(trace.get("live_execution") is False, "trace must not claim live execution")
    _require(
        trace.get("cross_system_live_integration") is False,
        "trace must not claim live DGAF/ACP integration",
    )

    sources = _object(trace, "sources")
    _require(
        sources.get("dgaf_repository") == "ndrorchestration/DGAF-Framework",
        "DGAF repository identity mismatch",
    )
    _require(
        sources.get("dgaf_authority_semantics_commit") == DGAF_AUTHORITY_COMMIT,
        "DGAF authority source identity mismatch",
    )
    _require(
        sources.get("dgaf_tektite_projection_commit") == DGAF_TEKTITE_COMMIT,
        "DGAF Tektite source identity mismatch",
    )
    _require(
        sources.get("acp_repository") == "ndrorchestration/agent-control-plane",
        "ACP repository identity mismatch",
    )
    _require(
        sources.get("acp_execution_semantics_commit") == ACP_EXECUTION_COMMIT,
        "ACP execution source identity mismatch",
    )

    intent = _object(trace, "intent")
    _require(
        intent.get("target_class") == "DISPOSABLE_TEST_REPOSITORY_ONLY",
        "trace must remain disposable-test only",
    )

    admission = _object(trace, "dgaf_admission")
    _require(admission.get("authority_effect") == "NONE", "admission cannot grant replay authority")

    authorization = _object(trace, "authorization")
    _require(
        authorization.get("scope") == "BOUNDED_LOCAL_TEST",
        "authorization scope widened beyond bounded local test",
    )
    _require(
        authorization.get("next_authorization_state") == "NOT_ISSUED",
        "trace cannot pre-issue follow-on authority",
    )

    execution = _object(trace, "acp_execution_contract")
    _require(
        execution.get("execution_profile") == "BOUNDED_LOCAL_TEST",
        "execution profile widened",
    )
    _require(
        execution.get("state") == "REPLAYED_TERMINAL_EXAMPLE",
        "trace must remain a replayed terminal example",
    )
    _require(
        execution.get("real_project_mutation_authorized") is False,
        "real-project mutation cannot be authorized",
    )
    _require(
        execution.get("rollback_execution_authorized") is False,
        "rollback execution cannot be authorized",
    )

    receipt = _object(trace, "receipt")
    _require(receipt.get("authority_effect") == "NONE", "receipt cannot carry authority")
    _require(
        receipt.get("follow_on_authority") == "FRESH_ADJUDICATION_REQUIRED",
        "receipt must require fresh adjudication",
    )

    lineage = _object(trace, "durable_lineage")
    _require(
        lineage.get("scope") == "LOCAL_DISPOSABLE_REPOSITORY_ONLY",
        "durable lineage scope widened",
    )
    _require(
        lineage.get("distributed_global_lineage") is False,
        "local lineage cannot be presented as distributed/global",
    )

    follow_on = _object(trace, "follow_on")
    _require(
        follow_on.get("fresh_dgaf_adjudication") == "REQUIRED",
        "fresh DGAF adjudication must remain required",
    )
    _require(
        follow_on.get("next_authorization_state") == "NOT_ISSUED",
        "next authorization cannot be inherited",
    )
    _require(
        follow_on.get("next_effect_state") == "BLOCKED_PENDING_FRESH_ADJUDICATION",
        "next effect must remain blocked pending fresh adjudication",
    )

    _require(trace.get("claim_boundary") == EXPECTED_BOUNDARY, "claim boundary mismatch")


def load_trace(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReplayTraceValidationError("trace root must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trace",
        default="public/evidence/tektite-dgaf-acp-replay-trace-v0.json",
    )
    args = parser.parse_args()
    trace = load_trace(Path(args.trace))
    validate_trace(trace)
    print("TEKTITE_DGAF_ACP_REPLAY_TRACE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
