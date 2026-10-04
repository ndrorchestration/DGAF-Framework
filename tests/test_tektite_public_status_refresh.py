import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/tektite-v0.1/status.seed.json"
LEDGER = ROOT / "docs/tektite-v0.1/evidence-ledger.seed.json"
PUBLIC_INDEX = ROOT / "docs/tektite-v0.1/public/index.html"
CURRENT_CASE = ROOT / "docs/tektite-v0.1/case-studies/ACP_BOUNDED_EXECUTOR_2026_10_04.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_tektite_status_seed_preserves_bounded_executor_and_negative_ceilings():
    status = read_json(STATUS)
    current = status["current_status"]

    assert status["date"] == "2026-10-04"
    assert current["ACP_BOUNDED_LOCAL_TEST_EXECUTOR"] == "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE"
    assert current["ACP_DURABLE_LOCAL_MUTATION_LINEAGE"] == "ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE"
    assert current["LIVE_REPOSITORY_MUTATION"] == "NOT_AUTHORIZED"
    assert current["ROLLBACK_EXECUTION"] == "NOT_AUTHORIZED"
    assert current["PRODUCTION_EXECUTOR"] == "NOT_ESTABLISHED"
    assert current["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"
    assert current["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"
    assert current["CANONICAL_DGAF_EFFICACY"] == "NOT_ESTABLISHED"


def test_tektite_status_seed_moves_117_118_to_retained_risk_not_active_blocker():
    status = read_json(STATUS)

    assert status["active_blockers"] == []
    risks = {item["id"]: item for item in status["retained_risks"]}
    assert set(risks) == {"#117", "#118"}
    assert risks["#117"]["disposition"] == "CLOSED_BY_RETAINED_RISK_DECISION"
    assert risks["#118"]["disposition"] == "CLOSED_BY_RETAINED_RISK_DECISION"
    assert risks["#117"]["status"] == "RETAINED_GAP"
    assert risks["#118"]["status"] == "RETAINED_GAP"


def test_tektite_evidence_ledger_distinguishes_historical_and_current_acp_rows():
    ledger = read_json(LEDGER)
    rows = {entry["artifact"]: entry for entry in ledger["entries"]}

    assert "ACP PR #145 (historical)" in rows
    assert "ACP PR #156" in rows
    assert "ACP PR #159" in rows
    assert "later bounded executor" in rows["ACP PR #145 (historical)"]["claim_not_supported"]
    assert "tested disposable-repository scope" in rows["ACP PR #156"]["claim_supported"]
    assert "Durable local mutation lineage" in rows["ACP PR #159"]["claim_supported"]


def test_tektite_public_index_shows_bounded_capabilities_and_retained_risks():
    html = PUBLIC_INDEX.read_text(encoding="utf-8")

    assert "ACP Bounded Local-Test Executor" in html
    assert "ACP Durable Local Mutation Lineage" in html
    assert "ESTABLISHED FOR TESTED DISPOSABLE SCOPE" in html
    assert "ACP retained risks #117 and #118" in html
    assert "ACP blockers #117 and #118" not in html
    assert "LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED" in html
    assert "ROLLBACK_EXECUTION=NOT_AUTHORIZED" in html
    assert "PRODUCTION_EXECUTOR=NOT_ESTABLISHED" in html


def test_current_acp_case_study_preserves_non_promotion_boundary():
    text = CURRENT_CASE.read_text(encoding="utf-8")

    assert "BOUNDED_LOCAL_TEST_EXECUTOR=ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE" in text
    assert "DURABLE_LOCAL_MUTATION_LINEAGE=ESTABLISHED_FOR_TESTED_DISPOSABLE_SCOPE" in text
    assert "FINAL_PATH_TO_SYSCALL_TOCTOU=NOT_ELIMINATED" in text
    assert "LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED" in text
    assert "ROLLBACK_EXECUTION=NOT_AUTHORIZED" in text
    assert "PRODUCTION_EXECUTOR=NOT_ESTABLISHED" in text
    assert "HIGH_ASSURANCE=NOT_AUTHORIZED" in text



def test_tektite_manifest_advances_without_rewriting_historical_ecosystem_pointer():
    manifest = read_json(ROOT / "registry/tektite_public_status_semantic_source_v1.json")
    pointer = read_json(ROOT / "registry/ecosystem_state_pointer.current.json")

    binding = next(
        item
        for item in pointer["consumer_bindings"]
        if item["consumer_id"] == "TEKTITE_PUBLIC_STATUS"
    )
    acp = next(
        item
        for item in manifest["external_authorities"]
        if item["authority_id"] == "ACP_SOURCE"
    )

    assert acp["object_identity"] == "e7135323663ebbe025b18b74a13f2d99c14e2b57"
    assert manifest["semantic_material_digest_sha256"] != binding["semantic_material_digest_sha256"]
    assert binding["freshness_state"] == "HISTORICAL_SNAPSHOT"
    assert binding["invalidation_reason"] == "SEMANTIC_SOURCE_CHANGED"
    assert pointer["snapshot_provenance"]["live_reconciliation"]["status"] == "NOT_EMBEDDED"


def test_tektite_manifest_binds_current_bounded_case_study():
    manifest = read_json(ROOT / "registry/tektite_public_status_semantic_source_v1.json")
    paths = {item["path"] for item in manifest["artifacts"]}

    assert "docs/tektite-v0.1/case-studies/ACP_BOUNDED_EXECUTOR_2026_10_04.md" in paths
