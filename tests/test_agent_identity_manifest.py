import copy
import json
from pathlib import Path

import pytest

from scripts.validate_agent_identity_manifest import validate_manifest

MANIFEST = Path("registry/agent_identity_manifest.v1.json")
ADJUDICATION = Path("registry/agent_ontology_adjudication.v1.json")


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_adjudication():
    return json.loads(ADJUDICATION.read_text(encoding="utf-8"))


def test_current_manifest_validates():
    validate_manifest(load_manifest())


def test_current_adjudication_is_separate_authority_layer():
    data = load_adjudication()
    assert data["status"] == "accepted-ontology-adjudication"
    assert data["canonical_seats"]["agent.ionia"] == "A-13"
    assert data["distinct_objects"]["ionia"]["state.ionia-0hz"]["canonical_seat"] is None


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


def test_conflict_observation_cannot_be_silently_erased():
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


def test_legacy_ionia_observation_may_remain_conflicted_without_overriding_adjudication():
    data = load_manifest()
    ionia = next(x for x in data["identities"] if x["identity_id"] == "agent.ionia")
    assert ionia["seat_status"] == "conflicted"
    adjudication = load_adjudication()
    assert adjudication["canonical_seats"]["agent.ionia"] == "A-13"
    validate_manifest(data)


def test_a20_plus_cannot_be_promoted_by_presence_alone():
    data = load_manifest()
    oracle = next(x for x in data["identities"] if x["identity_id"] == "agent.oracle")
    oracle["seat_status"] = "canonical"
    with pytest.raises(ValueError, match="cannot be silently promoted"):
        validate_manifest(data)


def test_identity_control_cannot_claim_scientific_state_effect():
    data = load_manifest()
    data["scientific_state_effect"] = "authorize"
    with pytest.raises(ValueError, match="no scientific-state effect"):
        validate_manifest(data)


def test_identity_control_cannot_embed_moving_scientific_boundary():
    data = load_manifest()
    data["scientific_boundary"] = "TRACK A COLLECTION COMPLETE"
    with pytest.raises(ValueError, match="must not embed moving scientific state"):
        validate_manifest(data)


def test_scientific_state_authority_pointer_is_fixed():
    data = load_manifest()
    data["scientific_state_authority"] = "registry/agent_identity_manifest.v1.json"
    with pytest.raises(ValueError, match="scientific-state authority pointer changed"):
        validate_manifest(data)
