import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO_ROOT / "registry" / "workflow_mutation_policy.v1.json"
CLASSIFICATION_PATH = REPO_ROOT / "registry" / "workflow_classification.v1.json"
AUDIT_CATALOG_PATH = REPO_ROOT / "registry" / "audit_catalog.v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _policies_by_path() -> dict[str, dict]:
    policy = _load(POLICY_PATH)
    return {entry["path"]: entry for entry in policy["policies"]}


def test_workflow_mutation_policy_registry_declares_projection_not_reclassification():
    policy = _load(POLICY_PATH)

    assert policy["version"] == "WORKFLOW_MUTATION_POLICY_V1"
    assert "registry/workflow_classification.v1.json" in policy["source_registries"]
    assert "registry/audit_catalog.v1.json" in policy["source_registries"]
    assert "does not reclassify audit families" in policy["scope"]
    assert "does not authorize scientific" in policy["scope"]


def test_policy_paths_are_existing_workflows_or_catalog_mapped_workflows():
    classification = _load(CLASSIFICATION_PATH)
    catalog = _load(AUDIT_CATALOG_PATH)
    classified_paths = {
        entry["path"]
        for entry in classification["classifications"]
        if entry.get("classification") == "CLASSIFIED_NON_AUDIT"
    }
    catalog_paths = {
        path
        for audit in catalog["audits"]
        for path in audit.get("implementation", [])
        if isinstance(path, str) and path.startswith(".github/workflows/")
    }

    for path, entry in _policies_by_path().items():
        assert (REPO_ROOT / path).exists()
        assert path in classified_paths or path in catalog_paths
        assert isinstance(entry["routine_hardening_allowed"], bool)
        assert entry["tektite_lane_status"] in {"BLOCKED", "ADMISSIBLE", "HELD"}


def test_retired_solo_workflow_is_blocked_pending_retirement_contract_cleanup():
    entry = _policies_by_path()[".github/workflows/pdmal-solo-final-experiment.yml"]

    assert entry["policy_id"] == "MUTATION_BLOCKED_PENDING_RETIREMENT_CONTRACT_CLEANUP"
    assert entry["workflow_classification_kind"] == "RETIRED_EXPERIMENT_EXECUTION_GUARD"
    assert entry["workflow_lifecycle"] == "HISTORICAL_EXACT_SCOPE"
    assert entry["routine_hardening_allowed"] is False
    assert "#1138" in entry["related_issues"]
    assert "#369" in entry["related_issues"]
    assert any("historical provenance tokens" in item for item in entry["minimum_verification_before_mutation"])


def test_b3_p33_workflow_is_blocked_pending_source_binding_reconciliation():
    entry = _policies_by_path()[".github/workflows/b3-p33-convergence-profile.yml"]

    assert entry["policy_id"] == "MUTATION_BLOCKED_SOURCE_BOUND_RECONCILIATION_REQUIRED"
    assert entry["workflow_lifecycle"] == "SOURCE_BOUND_EVIDENCE"
    assert entry["routine_hardening_allowed"] is False
    assert "#1127" in entry["related_issues"]
    assert any("source-binds this workflow path" in item for item in entry["minimum_verification_before_mutation"])


def test_mutation_policy_preserves_claim_boundaries():
    for entry in _policies_by_path().values():
        boundary = set(entry["claim_boundary"])
        assert "SCIENTIFIC_N_INCREMENT=0" in boundary
        assert "INDEPENDENT_VALIDATION=NOT_ESTABLISHED" in boundary
        assert "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED" in boundary
        assert "HIGH_ASSURANCE=NOT_AUTHORIZED" in boundary
