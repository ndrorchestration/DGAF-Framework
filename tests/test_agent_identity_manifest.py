import copy
import json
from pathlib import Path

import pytest

from scripts.validate_agent_identity_manifest import validate_manifest

MANIFEST = Path("registry/agent_identity_manifest.v1.json")


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_current_manifest_validates():
    validate_manifest(load_manifest())


def test_duplicate_stable_identity_fails_closed():
    data = load_manifest()
    data["identities"].append(copy.deepcopy(data["identities"][0]))
    with pytest.raises(ValueError, match="duplicate stable identity_id"):
        validate_manifest(data)


def test_duplicate_source_designation_fails_closed():
    data = load_manifest()
    duplicate = copy.deepcopy(data["identities"][0]["observed_designations"][0])
    data["identities"][1]["observed_designations"].append(duplicate)
    with pytest.raises(ValueError, match="source designation maps to multiple identities"):
        validate_manifest(data)


def test_conflict_cannot_be_silently_erased():
    data = load_manifest()
    reson = next(x for x in data["identities"] if x["identity_id"] == "agent.reson")
    reson["conflicts"] = []
    with pytest.raises(ValueError, match="conflicted identity must explain conflict"):
        validate_manifest(data)


def test_sentinel_phi_must_remain_variant_of_sentinel():
    data = load_manifest()
    sentinel_phi = next(x for x in data["identities"] if x["identity_id"] == "agent.sentinel-phi")
    sentinel_phi["variant_of"] = None
    with pytest.raises(ValueError, match="Sentinel-Phi variant lineage"):
        validate_manifest(data)


def test_ionia_state_agent_collision_cannot_be_silently_resolved():
    data = load_manifest()
    ionia = next(x for x in data["identities"] if x["identity_id"] == "agent.ionia")
    ionia["seat_status"] = "canonical"
    with pytest.raises(ValueError, match="Ionia agent/state conflict"):
        validate_manifest(data)


def test_a20_plus_cannot_be_promoted_by_presence_alone():
    data = load_manifest()
    oracle = next(x for x in data["identities"] if x["identity_id"] == "agent.oracle")
    oracle["seat_status"] = "canonical"
    with pytest.raises(ValueError, match="cannot be silently promoted"):
        validate_manifest(data)


def test_scientific_boundary_is_immutable_for_identity_control():
    data = load_manifest()
    data["scientific_boundary"] = "AUTHORIZED"
    with pytest.raises(ValueError, match="scientific boundary changed"):
        validate_manifest(data)
