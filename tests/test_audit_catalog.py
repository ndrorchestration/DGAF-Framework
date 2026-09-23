import json
from pathlib import Path

import pytest

from registry.audit_catalog import (\n    collect_catalog_violations,\n    collect_missing_implementation_paths,\n    load_catalog,\n)

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "registry" / "audit_catalog.v1.json"


def _entry(**overrides):
    base = {
        "id": "AUD-TEST-001",
        "name": "Example assurance mechanism",
        "class": "REPOSITORY_CI",
        "target_layers": ["REPOSITORY"],
        "assertion": "Example assertion.",
        "owner": "role.project-maintainer",
        "implementation": [".github/workflows/example.yml"],
        "trigger": ["pull_request"],
        "blocking": True,
        "evidence": ["workflow conclusion"],
        "verdicts": ["PASS", "FAIL"],
        "decision_effect": "Blocks merge when the declared assertion fails.",
        "non_effects": ["Does not establish scientific efficacy."],
        "fail_behavior": "FAIL_CLOSED",
        "independence": "SAME_SYSTEM_NONINDEPENDENT",
        "known_gaps": [],
        "lifecycle": "CURRENT",
    }
    base.update(overrides)
    return base


def test_missing_catalog_is_a_hard_failure():
    with pytest.raises(FileNotFoundError):
        load_catalog(REPO_ROOT / "registry" / "definitely_missing_audit_catalog.json")


def test_catalog_validator_rejects_duplicate_ids_and_unbound_decision_effects():
    duplicate = _entry(decision_effect="")
    catalog = {"version": "AUDIT_CATALOG_V1", "audits": [_entry(), duplicate]}
    codes = {violation["code"] for violation in collect_catalog_violations(catalog)}
    assert "DUPLICATE_AUDIT_ID" in codes
    assert "DECISION_EFFECT_MISSING" in codes


def test_catalog_validator_requires_explicit_non_effects_and_fail_behavior():
    catalog = {
        "version": "AUDIT_CATALOG_V1",
        "audits": [_entry(non_effects=[], fail_behavior="")],
    }
    codes = {violation["code"] for violation in collect_catalog_violations(catalog)}
    assert "NON_EFFECTS_MISSING" in codes
    assert "FAIL_BEHAVIOR_MISSING" in codes


def test_real_catalog_is_valid_and_contains_core_assurance_families():
    catalog = load_catalog(CATALOG_PATH)
    assert collect_catalog_violations(catalog) == []
    ids = {entry["id"] for entry in catalog["audits"]}
    assert {
        "AUD-CI-GOVERNANCE",
        "AUD-CI-PREFREEZE",
        "AUD-CI-TRUTH",
        "AUD-CI-ECOSYSTEM",
        "AUD-RUNTIME-LIVE",
    } <= ids


def test_real_catalog_does_not_claim_complete_repository_coverage():
    catalog = load_catalog(CATALOG_PATH)
    assert catalog["coverage"]["status"] != "COMPLETE_FOR_REPOSITORY"
    assert catalog["coverage"]["known_gaps"]


def test_catalog_json_is_machine_readable_without_loader_side_effects():
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    assert raw["version"] == "AUDIT_CATALOG_V1"


def test_catalog_implementation_bindings_resolve_to_existing_repository_paths():
    catalog = load_catalog(CATALOG_PATH)
    assert collect_missing_implementation_paths(REPO_ROOT, catalog) == []


def test_missing_implementation_path_is_reported_deterministically(tmp_path):
    catalog = {
        "version": "AUDIT_CATALOG_V1",
        "audits": [
            _entry(id="AUD-Z", implementation=["missing/z.yml"]),
            _entry(id="AUD-A", implementation=["missing/a.yml"]),
        ],
    }

    assert collect_missing_implementation_paths(tmp_path, catalog) == [
        {"audit_id": "AUD-A", "path": "missing/a.yml"},
        {"audit_id": "AUD-Z", "path": "missing/z.yml"},
    ]
