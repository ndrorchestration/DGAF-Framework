import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "tektite-v0.1" / "status.seed.json"
LEDGER = ROOT / "docs" / "tektite-v0.1" / "evidence-ledger.seed.json"
PUBLIC = ROOT / "docs" / "tektite-v0.1" / "public" / "index.html"
MANIFEST = ROOT / "registry" / "tektite_public_status_semantic_source_v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_current_tektite_seed_projects_bounded_executor_without_wider_authority() -> None:
    status = load(STATUS)

    assert status["date"] == "2026-10-04"
    assert status["current_status"]["BOUNDED_LOCAL_TEST_EXECUTOR"] == ("ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE")
    assert status["current_status"]["LIVE_REPOSITORY_MUTATION"] == "NOT_AUTHORIZED"
    assert status["current_status"]["ROLLBACK_EXECUTION"] == "NOT_AUTHORIZED"
    assert status["current_status"]["PRODUCTION_EXECUTOR"] == "NOT_ESTABLISHED"
    assert status["current_status"]["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"


def test_117_118_are_retained_risks_not_active_blockers() -> None:
    status = load(STATUS)

    assert status["active_blockers"] == []
    retained = {item["id"]: item for item in status["retained_risks"]}
    assert set(retained) == {"#117", "#118"}
    for issue_id in ("#117", "#118"):
        assert retained[issue_id]["status"] == "CLOSED_BY_RETAINED_RISK_DECISION"
        assert retained[issue_id]["bounded_profile"] == "BOUNDED_LOCAL_TEST"
        assert retained[issue_id]["stronger_guarantee"] == "NOT_ESTABLISHED"


def test_static_public_shell_matches_current_seed_boundary() -> None:
    text = PUBLIC.read_text(encoding="utf-8")

    assert "Bounded Local-Test Executor" in text
    assert "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE" in text
    assert "ACP retained risks #117 and #118" in text
    assert "ACP blockers #117 and #118" not in text
    assert "LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED" in text
    assert "ROLLBACK_EXECUTION=NOT_AUTHORIZED" in text
    assert "PRODUCTION_EXECUTOR=NOT_ESTABLISHED" in text


def test_evidence_ledger_contains_current_bounded_executor_row() -> None:
    ledger = load(LEDGER)
    rows = {item["artifact"]: item for item in ledger["entries"]}
    row = rows["ACP bounded local-test executor + retained-risk reconciliation"]

    assert "tested BOUNDED_LOCAL_TEST profile" in row["claim_supported"]
    assert "No real-project mutation" in row["claim_not_supported"]
    assert row["authorization_effect"].startswith("NONE;")


def test_semantic_manifest_binds_current_acp_authority_without_claim_promotion() -> None:
    manifest = load(MANIFEST)

    assert manifest["external_authorities"] == [
        {
            "authority_id": "ACP_SOURCE",
            "object_identity": "e7135323663ebbe025b18b74a13f2d99c14e2b57",
            "role": "ACP status dependency",
        }
    ]
    assert manifest["non_effects"]["scientific_n_increment"] == 0
    assert manifest["non_effects"]["independent_validation"] == "NOT_ESTABLISHED"
    assert manifest["non_effects"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert manifest["non_effects"]["high_assurance"] == "NOT_AUTHORIZED"


def test_durable_lineage_is_visible_with_disposable_scope_and_no_continuing_authority() -> None:
    status = load(STATUS)
    assert status["current_status"]["DURABLE_LOCAL_MUTATION_LINEAGE"] == "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE"
    html = PUBLIC.read_text(encoding="utf-8")
    assert "Durable Local Mutation Lineage" in html
    assert "distributed/global lineage" in html
    assert "fresh adjudication" in html


def test_historical_case_and_current_milestones_are_separately_reviewable() -> None:
    html = PUBLIC.read_text(encoding="utf-8")
    assert "Historical PR #145 disposition" in html
    case = ROOT / "docs/tektite-v0.1/case-studies/ACP_BOUNDED_LOCAL_TEST_EXECUTOR.md"
    assert case.is_file()
    assert "Historical scope" in (case.parent / "ACP_PR_145.md").read_text(encoding="utf-8")
    text = case.read_text(encoding="utf-8")
    for number in (156, 159):
        link = f"https://github.com/ndrorchestration/agent-control-plane/pull/{number}"
        assert link in text
        assert link in html
    assert "authority_effect=NONE" in text
    assert "FRESH_ADJUDICATION_REQUIRED" in text
    assert "../case-studies/ACP_BOUNDED_LOCAL_TEST_EXECUTOR.md" in html
    assert str(case.relative_to(ROOT)) in {row["path"] for row in load(MANIFEST)["artifacts"]}
