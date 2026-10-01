import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT_PATH = REPO_ROOT / "registry" / "workflow_mutation_policy_supplement_epoch001_successor.v1.json"
PRIMARY_POLICY_PATH = REPO_ROOT / "registry" / "workflow_mutation_policy.v1.json"

REQUIRED_BOUNDARY = {
    "SCIENTIFIC_N_INCREMENT=0",
    "INDEPENDENT_VALIDATION=NOT_ESTABLISHED",
    "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED",
    "HIGH_ASSURANCE=NOT_AUTHORIZED",
}

EXPECTED_BLOCKED_PATHS = {
    ".github/workflows/track-a-epoch-001-unblinding-materialization.yml",
    ".github/workflows/track-a-epoch-001-primary-analysis-authorization.yml",
    ".github/workflows/track-a-successor-solo-custody.yml",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _policies_by_path() -> dict[str, dict]:
    supplement = _load(SUPPLEMENT_PATH)
    return {entry["path"]: entry for entry in supplement["policies"]}


def test_supplement_declares_bounded_projection_scope():
    supplement = _load(SUPPLEMENT_PATH)

    assert supplement["version"] == "WORKFLOW_MUTATION_POLICY_SUPPLEMENT_EPOCH001_SUCCESSOR_V1"
    assert supplement["supplements"] == "registry/workflow_mutation_policy.v1.json"
    assert PRIMARY_POLICY_PATH.exists()
    assert "does not authorize scientific" in supplement["scope"]
    assert "High-Assurance" in supplement["scope"]


def test_all_supplemented_paths_exist_and_are_blocked():
    policies = _policies_by_path()

    assert set(policies) == EXPECTED_BLOCKED_PATHS
    for path, entry in policies.items():
        assert (REPO_ROOT / path).exists()
        assert entry["tektite_lane_status"] == "BLOCKED"
        assert entry["routine_hardening_allowed"] is False
        assert entry["workflow_lifecycle"]
        assert entry["allowed_next_action"]
        assert entry["minimum_verification_before_mutation"]
        assert entry["triggering_evidence"]


def test_supplement_preserves_claim_boundaries():
    for entry in _policies_by_path().values():
        assert set(entry["claim_boundary"]) == REQUIRED_BOUNDARY


def test_unblinding_materialization_policy_records_no_unblinding_boundary():
    entry = _policies_by_path()[".github/workflows/track-a-epoch-001-unblinding-materialization.yml"]

    assert entry["policy_id"] == "MUTATION_BLOCKED_UNBLINDING_MATERIALIZATION_STATE_RECONCILIATION_REQUIRED"
    assert (
        any("no-unblinding" in item for item in entry["allowed_next_action"].split())
        or "no-unblinding" in entry["allowed_next_action"]
    )
    assert any("unblinding" in item for item in entry["minimum_verification_before_mutation"])
    assert any("track_a_epoch_001_unblinded_analysis_input.json" in item for item in entry["triggering_evidence"])


def test_primary_analysis_authorization_policy_records_exact_scope_boundary():
    entry = _policies_by_path()[".github/workflows/track-a-epoch-001-primary-analysis-authorization.yml"]

    assert entry["policy_id"] == "MUTATION_BLOCKED_PRIMARY_AUTHORIZATION_EXACT_SCOPE_RECONCILIATION_REQUIRED"
    assert any("three-file" in item for item in entry["minimum_verification_before_mutation"])
    assert any("primary-result" in item for item in entry["triggering_evidence"])


def test_successor_custody_policy_records_side_effect_boundary():
    entry = _policies_by_path()[".github/workflows/track-a-successor-solo-custody.yml"]

    assert entry["policy_id"] == "MUTATION_BLOCKED_SUCCESSOR_CUSTODY_SIDE_EFFECT_RECONCILIATION_REQUIRED"
    assert entry["workflow_classification_kind"] == "SUCCESSOR_CUSTODY_TOOLING_CONTRACT"
    assert any("no-secret-generation" in item for item in entry["minimum_verification_before_mutation"])
    assert any("TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json" in item for item in entry["triggering_evidence"])
