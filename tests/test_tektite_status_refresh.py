import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/tektite-v0.1/status.seed.json"
LEDGER = ROOT / "docs/tektite-v0.1/evidence-ledger.seed.json"
PUBLIC = ROOT / "docs/tektite-v0.1/public/index.html"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_status_seed_projects_bounded_executor_without_stronger_authority():
    status = load(STATUS)
    current = status["current_status"]

    assert current["BOUNDED_LOCAL_TEST_EXECUTOR"] == "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE"
    assert current["LIVE_REPOSITORY_MUTATION"] == "NOT_AUTHORIZED"
    assert current["ROLLBACK_EXECUTION"] == "NOT_AUTHORIZED"
    assert current["PRODUCTION_EXECUTOR"] == "NOT_ESTABLISHED"
    assert current["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"
    assert current["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"
    assert current["CANONICAL_DGAF_EFFICACY"] == "NOT_ESTABLISHED"


def test_closed_retained_risk_issues_are_not_active_blockers():
    status = load(STATUS)
    active_ids = {item["id"] for item in status["active_blockers"]}
    assert "#117" not in active_ids
    assert "#118" not in active_ids


def test_latest_milestone_is_bounded_executor_and_preserves_non_claims():
    milestone = load(STATUS)["latest_milestone"]
    assert milestone["title"] == "ACP PR #156 merged"
    assert milestone["merge_commit"] == "b975aeb178b07551869ea6e80421e473ecb48593"
    assert "Bounded local-test executor" in milestone["supports"]
    assert "Real-project repository mutation" in milestone["does_not_support"]
    assert "Rollback execution" in milestone["does_not_support"]
    assert "High-Assurance status" in milestone["does_not_support"]


def test_evidence_ledger_retains_pr145_and_adds_pr156():
    entries = load(LEDGER)["entries"]
    by_artifact = {item["artifact"]: item for item in entries}
    assert "ACP PR #145" in by_artifact
    assert "ACP PR #156" in by_artifact
    assert "tested disposable-repository scope" in by_artifact["ACP PR #156"]["claim_supported"]
    assert "real-project mutation" in by_artifact["ACP PR #156"]["claim_not_supported"].lower()
    assert by_artifact["ACP PR #156"]["authorization_effect"] == "NONE; FRESH_ADJUDICATION_REQUIRED"


def test_public_shell_drops_current_blocker_claim_and_shows_bounded_executor():
    html = PUBLIC.read_text(encoding="utf-8")
    assert "ACP blockers #117 and #118" not in html
    assert "Held executor PRs remain held" not in html
    assert "Bounded Local-Test Executor" in html
    assert "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE" in html
    assert "ACP PR #156" in html
    assert "Real-project mutation remains unauthorized" in html
