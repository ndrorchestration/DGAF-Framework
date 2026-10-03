from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.validate_tektite_dgaf_acp_replay_trace import (
    ReplayTraceValidationError,
    validate_trace,
)

ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "public" / "evidence" / "tektite-dgaf-acp-replay-trace-v0.json"


def trace() -> dict:
    return json.loads(TRACE_PATH.read_text(encoding="utf-8"))


def test_canonical_replay_trace_passes() -> None:
    validate_trace(trace())


@pytest.mark.parametrize(
    "mutation, message",
    [
        (lambda value: value.update(live_execution=True), "live execution"),
        (
            lambda value: value.update(cross_system_live_integration=True),
            "live DGAF/ACP integration",
        ),
        (
            lambda value: value["sources"].update(dgaf_authority_semantics_commit="0" * 40),
            "DGAF authority source identity",
        ),
        (
            lambda value: value["sources"].update(acp_execution_semantics_commit="0" * 40),
            "ACP execution source identity",
        ),
        (
            lambda value: value["intent"].update(target_class="REAL_PROJECT"),
            "disposable-test only",
        ),
        (
            lambda value: value["authorization"].update(scope="PRODUCTION"),
            "scope widened",
        ),
        (
            lambda value: value["receipt"].update(authority_effect="GRANTED"),
            "receipt cannot carry authority",
        ),
        (
            lambda value: value["receipt"].update(follow_on_authority="INHERITED"),
            "fresh adjudication",
        ),
        (
            lambda value: value["durable_lineage"].update(distributed_global_lineage=True),
            "distributed/global",
        ),
        (
            lambda value: value["follow_on"].update(next_authorization_state="ISSUED"),
            "cannot be inherited",
        ),
        (
            lambda value: value["follow_on"].update(next_effect_state="AUTHORIZED"),
            "blocked pending fresh adjudication",
        ),
        (
            lambda value: value["claim_boundary"].update(scientific_n_increment=1),
            "claim boundary",
        ),
        (
            lambda value: value["claim_boundary"].update(independent_validation="ESTABLISHED"),
            "claim boundary",
        ),
        (
            lambda value: value["claim_boundary"].update(high_assurance="AUTHORIZED"),
            "claim boundary",
        ),
    ],
)
def test_replay_trace_fails_closed_on_claim_or_authority_widening(mutation, message) -> None:
    candidate = deepcopy(trace())
    mutation(candidate)
    with pytest.raises(ReplayTraceValidationError, match=message):
        validate_trace(candidate)
