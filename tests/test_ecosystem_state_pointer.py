import copy
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_ecosystem_state_pointer.py"
CURRENT = ROOT / "registry" / "ecosystem_state_pointer.current.json"
AOSS_MANIFEST = ROOT / "registry" / "aoss_stage_a_readiness_semantic_source_v1.json"
TEKTITE_MANIFEST = ROOT / "registry" / "tektite_public_status_semantic_source_v1.json"

module = runpy.run_path(str(SCRIPT))
validate = module["validate"]
validate_live_reconciliation = module["validate_live_reconciliation"]
validate_manifest = module["validate_manifest"]
semantic_material_digest = module["semantic_material_digest"]
classify = module["classify"]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pointer():
    return read_json(CURRENT)


def test_current_pointer_validates_as_embedded_snapshot():
    value = pointer()
    assert validate(value) == []
    assert value["snapshot_provenance"]["container_commit"] is None
    assert value["snapshot_provenance"]["live_reconciliation"]["status"] == "NOT_EMBEDDED"


def test_embedded_pointer_records_historical_snapshot_state():
    value = pointer()
    assert all(x["freshness_state"] == "HISTORICAL_SNAPSHOT" for x in value["authorities"])
    assert all(x["freshness_state"] == "HISTORICAL_SNAPSHOT" for x in value["consumer_bindings"])


def test_semantic_manifests_recompute_to_declared_digests():
    assert validate_manifest(read_json(AOSS_MANIFEST)) == []
    assert validate_manifest(read_json(TEKTITE_MANIFEST)) == []


def test_provenance_refresh_does_not_change_semantic_digest():
    before = read_json(AOSS_MANIFEST)
    after = copy.deepcopy(before)
    after["observed_at"] = "2099-01-01T00:00:00Z"
    after["repository_commit"] = "f" * 40
    assert semantic_material_digest(before) == semantic_material_digest(after)


def test_self_reference_is_not_encoded_in_pointer():
    value = pointer()
    value["snapshot_provenance"]["container_commit"] = value["snapshot_provenance"]["source_observation_commit"]
    errors = validate(value)
    assert any("container_commit must be null" in error for error in errors)


def test_live_tip_currentness_requires_external_reconciliation():
    value = pointer()
    source = value["snapshot_provenance"]["source_observation_commit"]
    assert validate_live_reconciliation(value, source, "e" * 40) == []


def test_live_tip_advance_fails_closed():
    value = pointer()
    errors = validate_live_reconciliation(value, "f" * 40, "e" * 40)
    assert any("not repository-tip current" in error for error in errors)


def test_container_commit_cannot_masquerade_as_source_observation():
    value = pointer()
    source = value["snapshot_provenance"]["source_observation_commit"]
    errors = validate_live_reconciliation(value, source, source)
    assert any("container_commit must not be treated" in error for error in errors)


def test_same_binding_after_authority_advance_is_non_semantic():
    before = pointer()
    after = copy.deepcopy(before)
    dgaf = next(x for x in after["authorities"] if x["authority_id"] == "DGAF_SOURCE")
    dgaf["object_identity"] = "f" * 40

    result = classify(before, after)
    classes = {x["consumer_id"]: x["classification"] for x in result["consumer_bindings"]}
    assert classes["AOSS_STAGE_A_READINESS"] == "NON_SEMANTIC_REPOSITORY_ADVANCE"
    assert classes["TEKTITE_PUBLIC_STATUS"] == "NON_SEMANTIC_REPOSITORY_ADVANCE"


def test_changed_consumer_digest_is_semantic_source_change():
    before = pointer()
    after = copy.deepcopy(before)
    binding = next(x for x in after["consumer_bindings"] if x["consumer_id"] == "AOSS_STAGE_A_READINESS")
    binding["semantic_material_digest_sha256"] = "f" * 64

    result = classify(before, after)
    classes = {x["consumer_id"]: x["classification"] for x in result["consumer_bindings"]}
    assert classes["AOSS_STAGE_A_READINESS"] == "SEMANTIC_SOURCE_CHANGED"
    assert classes["TEKTITE_PUBLIC_STATUS"] == "NONE"


def test_semantic_material_tampering_is_rejected():
    manifest = read_json(AOSS_MANIFEST)
    manifest["artifacts"][0]["role"] = "tampered"
    errors = validate_manifest(manifest)
    assert any("mismatch" in error for error in errors)


def test_claim_ceiling_cannot_be_promoted():
    value = pointer()
    value["claim_ceiling"]["independent_validation"] = "ESTABLISHED"
    errors = validate(value)
    assert any("claim_ceiling" in error for error in errors)


def test_aoss_readiness_manifest_covers_transitive_semantic_closure():
    manifest = read_json(AOSS_MANIFEST)
    paths = {item["path"] for item in manifest["artifacts"]}
    required = {
        "scripts/validate_aoss_v0_6_stage_a_predata_readiness.py",
        "registry/aoss_v0_6_stage_a_predata_readiness_v1.json",
        "registry/aoss_v0_6_acp_measurement_manifest_v1.json",
        "registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json",
        "registry/aoss_v0_6_stage_a_artifact_replay_receipt_contract_v1.json",
        "schemas/aoss_v0_6_stage_a_replay_receipt.schema.json",
        "registry/aoss_v0_6_stage_a_freshness_calibration_v1.json",
        "registry/aoss_v0_6_stage_a_episode_eligibility_repetition_v1.json",
        "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json",
        "registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json",
        "registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json",
        "registry/aoss_v0_6_stage_a_comparator_input_derivation_gap_v1.json",
        "registry/aoss_v0_6_stage_a_primary_comparator_amendment_v1.json",
        "scripts/aoss_v0_6_stage_a_acp_direct_baseline.py",
        "registry/aoss_v0_6_stage_a_decision_policy_v1.json",
        "scripts/aoss_v0_6_stage_a_decision_policy.py",
        "scripts/aoss_v0_6_acp_adapter.py",
        "registry/aoss_v0_6_stage_a_collection_authorization_v1.json",
        "registry/aoss_v0_6_stage_a_environment_manifest_v1.json",
        "registry/aoss_v0_6_stage_a_executable_destination_binding_v1.json",
    }
    assert required <= paths
