from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.validate_agent_ontology_adjudication import validate_record

RECORD = Path("registry/agent_ontology_adjudication.v1.json")


def load_record() -> dict[str, object]:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_current_record_passes() -> None:
    validate_record(load_record())


def test_canonical_seat_drift_fails() -> None:
    record = copy.deepcopy(load_record())
    canonical = record["canonical_seats"]
    assert isinstance(canonical, dict)
    canonical["agent.reson"] = "A-09"
    with pytest.raises(ValueError, match="canonical seat adjudication drifted"):
        validate_record(record)


def test_sentinel_phi_cannot_consume_echolette_seat() -> None:
    record = copy.deepcopy(load_record())
    distinct = record["distinct_objects"]
    assert isinstance(distinct, dict)
    lineage = distinct["sentinel_lineage"]
    assert isinstance(lineage, dict)
    sentinel_phi = lineage["agent.sentinel-phi"]
    assert isinstance(sentinel_phi, dict)
    sentinel_phi["canonical_seat"] = "A-12"
    with pytest.raises(ValueError, match="cannot consume"):
        validate_record(record)


def test_ionia_state_cannot_consume_agent_seat() -> None:
    record = copy.deepcopy(load_record())
    distinct = record["distinct_objects"]
    assert isinstance(distinct, dict)
    ionia = distinct["ionia"]
    assert isinstance(ionia, dict)
    state = ionia["state.ionia-0hz"]
    assert isinstance(state, dict)
    state["canonical_seat"] = "A-13"
    with pytest.raises(ValueError, match="cannot consume a seat"):
        validate_record(record)


def test_archetype_cannot_grant_sentinel_identity() -> None:
    record = copy.deepcopy(load_record())
    distinct = record["distinct_objects"]
    assert isinstance(distinct, dict)
    archetype = distinct["demijoule_sentinel_archetype"]
    assert isinstance(archetype, dict)
    archetype["grants_sentinel_identity"] = True
    with pytest.raises(ValueError, match="cannot grant Sentinel identity"):
        validate_record(record)


def test_scientific_state_effect_cannot_change() -> None:
    record = copy.deepcopy(load_record())
    record["scientific_state_effect"] = "AUTHORIZE"
    with pytest.raises(ValueError, match="cannot change scientific state"):
        validate_record(record)
