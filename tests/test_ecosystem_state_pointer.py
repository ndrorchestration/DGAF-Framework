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
validate_manifest = module["validate_manifest"]
classify = module["classify"]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pointer():
    return read_json(CURRENT)


def test_current_pointer_validates():
    assert validate(pointer()) == []


def test_semantic_manifests_recompute_to_declared_digests():
    assert validate_manifest(read_json(AOSS_MANIFEST)) == []
    assert validate_manifest(read_json(TEKTITE_MANIFEST)) == []


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
    binding["manifest_digest_sha256"] = "f" * 64

    result = classify(before, after)
    classes = {x["consumer_id"]: x["classification"] for x in result["consumer_bindings"]}
    assert classes["AOSS_STAGE_A_READINESS"] == "SEMANTIC_SOURCE_CHANGED"
    assert classes["TEKTITE_PUBLIC_STATUS"] == "NONE"


def test_manifest_digest_tampering_is_rejected():
    manifest = read_json(AOSS_MANIFEST)
    manifest["artifacts"][0]["role"] = "tampered"
    errors = validate_manifest(manifest)
    assert any("mismatch" in error for error in errors)


def test_claim_ceiling_cannot_be_promoted():
    value = pointer()
    value["claim_ceiling"]["independent_validation"] = "ESTABLISHED"
    errors = validate(value)
    assert any("claim_ceiling" in error for error in errors)
