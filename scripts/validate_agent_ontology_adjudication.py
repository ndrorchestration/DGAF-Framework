#!/usr/bin/env python3
"""Fail-closed validator for the accepted DGAF agent ontology adjudication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_RECORD = Path("registry/agent_ontology_adjudication.v1.json")

EXPECTED_CANONICAL = {
    "agent.colleen": "A-05",
    "agent.librarian": "A-06",
    "agent.zenith": "A-09",
    "agent.reson": "A-10",
    "agent.lyra": "A-11",
    "agent.echolette": "A-12",
    "agent.ionia": "A-13",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_record(data: dict[str, Any]) -> None:
    _require(data.get("schema_version") == "1.0.0", "unexpected schema_version")
    _require(data.get("status") == "accepted-ontology-adjudication", "adjudication not accepted")
    _require(data.get("controller_issue") == 522, "wrong controller issue")
    _require(data.get("scientific_state_effect") == "none", "ontology cannot change scientific state")
    _require(data.get("authority_matrix_effect") == "none", "ontology cannot silently change authority")

    policy = data.get("authority_policy", {})
    _require(
        policy.get("canonical_identity_source") == "docs/agents/AGENT_ROSTER.md",
        "sovereign roster precedence changed",
    )
    _require(
        policy.get("formation_source") == "docs/agents/FORMATION_TOPOLOGY.md",
        "formation source changed",
    )
    _require(
        policy.get("ecosystem_source") == "docs/agents/AGENT_ECOSYSTEM_REGISTRY.md",
        "ecosystem source changed",
    )

    canonical = data.get("canonical_seats")
    _require(canonical == EXPECTED_CANONICAL, "canonical seat adjudication drifted")

    local = data.get("formation_local_designations", {})
    _require(local.get("agent.colleen") == ["A-00-GOV"], "COLLEEN local designation drifted")
    _require(local.get("agent.librarian") == ["A-06-L"], "Librarian local designation drifted")
    _require(local.get("agent.zenith") == ["A-09-Z"], "Zenith local designation drifted")
    _require(local.get("agent.reson") == ["A-09"], "Reson local designation drifted")
    _require(local.get("agent.lyra") == ["A-10"], "Lyra local designation drifted")
    _require(local.get("agent.echolette") == ["A-11"], "Echolette local designation drifted")

    distinct = data.get("distinct_objects", {})
    sentinel = distinct.get("sentinel_lineage", {})
    _require("agent.sentinel" in sentinel and "agent.sentinel-phi" in sentinel, "Sentinel lineage missing")
    _require(sentinel["agent.sentinel"].get("collapsed_into") is None, "Sentinel was silently collapsed")
    _require(
        sentinel["agent.sentinel-phi"].get("variant_of") == "agent.sentinel",
        "Sentinel-Phi lineage changed",
    )
    _require(
        sentinel["agent.sentinel-phi"].get("canonical_seat") is None,
        "Sentinel-Phi cannot consume a sovereign numbered seat",
    )

    ionia = distinct.get("ionia", {})
    _require(ionia.get("agent.ionia", {}).get("canonical_seat") == "A-13", "Agent Ionia seat changed")
    _require(
        ionia.get("state.ionia-0hz", {}).get("kind") == "formation-runtime-state",
        "IONIA_STATE must remain a state",
    )
    _require(ionia.get("state.ionia-0hz", {}).get("canonical_seat") is None, "IONIA_STATE cannot consume a seat")

    archetype = distinct.get("demijoule_sentinel_archetype", {})
    _require(archetype.get("kind") == "archetype-role", "DemiJoule sentinel archetype changed kind")
    _require(archetype.get("grants_sentinel_identity") is False, "archetype cannot grant Sentinel identity")
    _require(archetype.get("grants_sentinel_phi_identity") is False, "archetype cannot grant Sentinel-Phi identity")

    invariants = data.get("invariants", {})
    for key in (
        "local_designation_cannot_override_canonical_seat",
        "sentinel_and_sentinel_phi_remain_distinct",
        "ionia_agent_and_ionia_state_remain_distinct",
        "topology_membership_does_not_create_sovereign_seat",
        "translation_has_no_identity_resolution_authority",
    ):
        _require(invariants.get(key) is True, f"required invariant disabled: {key}")
    _require(invariants.get("scientific_state_effect") == "none", "invariant scientific-state effect changed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", type=Path, default=DEFAULT_RECORD)
    args = parser.parse_args()
    data = json.loads(args.record.read_text(encoding="utf-8"))
    _require(isinstance(data, dict), "adjudication record must be a JSON object")
    validate_record(data)
    print("AGENT_ONTOLOGY_ADJUDICATION=PASS")
    print("SCIENTIFIC_STATE_EFFECT=NONE")
    print("AUTHORITY_MATRIX_EFFECT=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
