import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "app" / "components" / "tektite-cep-observability.tsx"
PAGE = ROOT / "app" / "(command-center)" / "demo" / "page.tsx"
FIXTURE = ROOT / "public" / "evidence" / "tektite-cep-observability-v0.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_cep_projection_is_static_and_non_executing() -> None:
    text = COMPONENT.read_text(encoding="utf-8")
    assert "READ ONLY · AUTOMATIC TOOL GATING NOT ENABLED" in text
    assert "does not gate tools" in text
    assert "does not gate tools, suppress context, invoke ACP" in text
    assert "const CEP_URL = '/evidence/tektite-cep-observability-v0.json'" in text
    assert "http://" not in text
    assert "https://" not in text
    assert "/api/" not in text


def test_cep_fixture_separates_observed_and_unmeasured_claims() -> None:
    data = load_fixture()
    observed = data["observed_catalog_measurement"]
    missing = data["unobserved_or_not_established"]
    boundary = data["comparison_boundary"]

    assert data["live_model_experiment"] is False
    assert data["automatic_tool_gating_enabled"] is False
    assert data["live_context_routing_enabled"] is False
    assert observed["control_descriptor_count"] == 89
    assert observed["treatment_descriptor_count"] == 1
    assert observed["control_tokens"] == 32471
    assert observed["treatment_tokens"] == 268
    assert observed["required_tool_preserved"] is True
    assert missing["live_model_input_token_reduction"] == "NOT_MEASURED"
    assert missing["latency_effect"] == "NOT_MEASURED"
    assert missing["monetary_cost_effect"] == "NOT_MEASURED"
    assert missing["task_correctness_effect"] == "NOT_MEASURED"
    assert missing["task_efficacy"] == "NOT_ESTABLISHED"
    assert boundary["evaluation_scope"] == "BOUNDED_CONTEXT_COST_PRESERVATION_ONLY"
    assert boundary["authority_effect"] == "NONE"
    assert boundary["scientific_n_increment"] == 0
    assert boundary["independent_validation_effect"] == "NONE"
    assert boundary["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert boundary["high_assurance"] == "NOT_AUTHORIZED"


def test_cep_fixture_is_bound_to_accepted_acp_source() -> None:
    data = load_fixture()
    assert data["sources"]["acp_repository"] == "ndrorchestration/agent-control-plane"
    assert data["sources"]["acp_cep_merge_commit"] == ("cb264a123cb67ada7616ece4b30172f7d5d59a2f")
    assert data["sources"]["catalog_snapshot_sha256"] == (
        "f9d463a1c8519061087cba30bd648b68357949f20ce932c61c3f99821663b82e"
    )
    assert data["task"]["required_tool"] == "mcp__GitHub__fetch_commit_workflow_runs"


def test_demo_page_includes_cep_projection_without_replacing_existing_surfaces() -> None:
    text = PAGE.read_text(encoding="utf-8")
    assert "<TektiteDemoView />" in text
    assert "<TektiteGovernedReplayTrace />" in text
    assert "<TektiteCepObservability />" in text
