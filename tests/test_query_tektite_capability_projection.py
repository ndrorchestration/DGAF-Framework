import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/query_tektite_capability_projection.py"
STATUS_PATH = ROOT / "docs/tektite-v0.1/status.seed.json"


def load_module():
    spec = importlib.util.spec_from_file_location("query_tektite_capability_projection", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def status_seed():
    return json.loads(STATUS_PATH.read_text(encoding="utf-8"))


def observation(
    repository_commit="cb264a123cb67ada7616ece4b30172f7d5d59a2f",
    source_artifact="docs/CURRENT_FRONTIER.md",
):
    return {
        "schema_version": "TEKTITE_CAPABILITY_AUTHORITY_OBSERVATION_V0",
        "authority_id": "ACP_SOURCE",
        "repository": "ndrorchestration/agent-control-plane",
        "repository_commit": repository_commit,
        "source_artifact": source_artifact,
        "observed_at": "2026-10-04T15:32:00Z",
        "capability_states": {
            "BOUNDED_LOCAL_TEST_EXECUTOR": "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE",
            "LIVE_REPOSITORY_MUTATION": "NOT_AUTHORIZED",
            "ROLLBACK_EXECUTION": "NOT_AUTHORIZED",
            "PRODUCTION_EXECUTOR": "NOT_ESTABLISHED",
            "HIGH_ASSURANCE": "NOT_AUTHORIZED",
            "TRUSTED_PROCESS_IDENTITY": "NOT_ESTABLISHED",
            "PEER_PROCESS_TAMPER_RESISTANCE": "NOT_ESTABLISHED",
            "HIGH_ASSURANCE_PROCESS_BOUNDARY": "NOT_ESTABLISHED",
        },
        "lifecycle_states": {
            "#117": "CLOSED_RETAINED_RISK",
            "#118": "CLOSED_RETAINED_RISK",
        },
    }


def test_matching_capability_ceilings_are_current_answer_eligible():
    module = load_module()
    receipt = module.reconcile(status_seed(), observation())

    by_key = {row["projection_key"]: row for row in receipt["projection_rows"]}
    for key in [
        "LIVE_REPOSITORY_MUTATION",
        "ROLLBACK_EXECUTION",
        "PRODUCTION_EXECUTOR",
        "HIGH_ASSURANCE",
    ]:
        assert by_key[key]["relation"] == "MATCH"
        assert by_key[key]["current_answer_eligible"] is True


def test_stale_active_blockers_are_detected_without_capability_promotion():
    module = load_module()
    receipt = module.reconcile(status_seed(), observation())

    by_id = {row["blocker_id"]: row for row in receipt["lifecycle_rows"]}
    assert by_id["#117"]["relation"] == "STALE_LIFECYCLE_LABEL"
    assert by_id["#118"]["relation"] == "STALE_LIFECYCLE_LABEL"
    assert by_id["#117"]["current_answer_eligible"] is False

    by_key = {row["projection_key"]: row for row in receipt["projection_rows"]}
    assert by_key["LIVE_REPOSITORY_MUTATION"]["observed_authority_value"] == "NOT_AUTHORIZED"


def test_unprojected_authority_capabilities_are_exposed():
    module = load_module()
    receipt = module.reconcile(status_seed(), observation())

    gaps = {row["capability_key"]: row for row in receipt["unprojected_authority_states"]}
    assert gaps["BOUNDED_LOCAL_TEST_EXECUTOR"]["observed_authority_value"] == (
        "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE"
    )
    assert gaps["TRUSTED_PROCESS_IDENTITY"]["observed_authority_value"] == "NOT_ESTABLISHED"


def test_missing_external_observation_fails_closed():
    module = load_module()
    receipt = module.reconcile(status_seed(), None)

    assert receipt["reconciliation_state"] == "NOT_SUPPLIED"
    assert receipt["currentness"] == "NOT_ESTABLISHED"
    assert receipt["projection_rows"] == []


def test_unexpected_authority_identity_is_rejected():
    module = load_module()
    bad = observation()
    bad["authority_id"] = "NOT_ACP"

    with pytest.raises(ValueError, match="authority_id"):
        module.reconcile(status_seed(), bad)


def test_commit_and_source_are_preserved_in_receipt():
    module = load_module()
    receipt = module.reconcile(status_seed(), observation())

    assert receipt["authority_binding"]["repository_commit"] == ("cb264a123cb67ada7616ece4b30172f7d5d59a2f")
    assert receipt["authority_binding"]["source_artifact"] == "docs/CURRENT_FRONTIER.md"
    assert receipt["observation_authority"] == "CALLER_SUPPLIED_NOT_REVERIFIED"


def test_mismatched_projected_state_requires_review():
    module = load_module()
    obs = observation()
    obs["capability_states"]["LIVE_REPOSITORY_MUTATION"] = "AUTHORIZED"
    receipt = module.reconcile(status_seed(), obs)

    by_key = {row["projection_key"]: row for row in receipt["projection_rows"]}
    row = by_key["LIVE_REPOSITORY_MUTATION"]
    assert row["relation"] == "MISMATCH_REQUIRES_REVIEW"
    assert row["current_answer_eligible"] is False


def test_receipt_has_no_authority_effects():
    module = load_module()
    receipt = module.reconcile(status_seed(), observation())

    assert receipt["truth_effect"] == "NONE"
    assert receipt["authorization_effect"] == "NONE"
    assert receipt["scientific_state_effect"] == "NONE"


def test_cli_missing_observation_exits_two():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(STATUS_PATH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2, result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["reconciliation_state"] == "NOT_SUPPLIED"


def semantic_manifest():
    return json.loads((ROOT / "registry/tektite_public_status_semantic_source_v1.json").read_text(encoding="utf-8"))


def test_stale_semantic_authority_pointer_is_detected():
    module = load_module()
    receipt = module.reconcile(
        status_seed(),
        observation(),
        semantic_manifest=semantic_manifest(),
    )

    binding = receipt["semantic_authority_binding"]
    assert binding["manifest_id"] == "TEKTITE_PUBLIC_STATUS_SEMANTIC_SOURCE_V1"
    assert binding["consumer"] == "TEKTITE_PUBLIC_STATUS"
    assert binding["authority_id"] == "ACP_SOURCE"
    assert binding["manifest_object_identity"] == ("4d3cdd21a445b765753cb5d36360f643210fe0b5")
    assert binding["observed_repository_commit"] == ("cb264a123cb67ada7616ece4b30172f7d5d59a2f")
    assert binding["relation"] == "STALE_AUTHORITY_POINTER"


def test_matching_semantic_authority_pointer_passes():
    module = load_module()
    manifest = semantic_manifest()
    manifest["external_authorities"][0]["object_identity"] = "cb264a123cb67ada7616ece4b30172f7d5d59a2f"
    receipt = module.reconcile(
        status_seed(),
        observation(),
        semantic_manifest=manifest,
    )

    assert receipt["semantic_authority_binding"]["relation"] == "MATCH"


def test_wrong_semantic_authority_id_is_rejected():
    module = load_module()
    manifest = semantic_manifest()
    manifest["external_authorities"][0]["authority_id"] = "OTHER"

    with pytest.raises(ValueError, match="ACP_SOURCE"):
        module.reconcile(
            status_seed(),
            observation(),
            semantic_manifest=manifest,
        )
