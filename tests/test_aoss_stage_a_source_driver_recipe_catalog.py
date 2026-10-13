import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
GROUND_TRUTH = ROOT / "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json"
FIXTURES = ROOT / "tests/resources/aoss_v0_6_acp_fixture_bundle.json"

TERMINALS = {
    "task.completed",
    "task.denied",
    "task.rejected",
    "task.failed",
    "task.cancelled",
    "task.budget_exhausted",
}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_terminal(case):
    terminals = [event["event"] for event in case["events"] if event.get("event") in TERMINALS]
    return terminals[-1] if terminals else None


def test_recipe_catalog_matches_frozen_ground_truth_and_fixture_terminals():
    catalog = _load(CATALOG)
    ground_truth = _load(GROUND_TRUTH)
    fixtures = _load(FIXTURES)

    recipes = {item["class"]: item["synthetic_terminal_event"] for item in catalog["recipes"]}
    labels = ground_truth["labels"]
    cases = fixtures["cases"]

    assert set(recipes) == set(labels) == set(cases)
    assert fixtures["source_identity"]["commit"] == catalog["recipe_boundary"]["source_commit"]

    for name, expected in recipes.items():
        assert expected == labels[name]["terminal_event"], name
        assert expected == _fixture_terminal(cases[name]), name


def test_recipe_catalog_remains_non_collecting_and_non_authorizing():
    catalog = _load(CATALOG)
    assert catalog["status"] == "PROPOSED_NON_COLLECTING_SYNTHETIC_ONLY"
    assert catalog["execution_status"] == "NO_SOURCE_DRIVER_IMPLEMENTED"
    assert catalog["recipe_boundary"]["driver_import_allowed"] is False
    assert catalog["recipe_boundary"]["acp_execution_allowed"] is False
    assert catalog["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert catalog["scientific_n_increment"] == 0
