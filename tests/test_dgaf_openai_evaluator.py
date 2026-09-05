import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "tools" / "dgaf_openai_evaluator.py"
spec = importlib.util.spec_from_file_location("dgaf_openai_evaluator", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_deterministic_checks_accept_non_empirical_artifact():
    artifact = {
        "seed": 20260817,
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "empirical_n": 0,
        "provenance": {"source_sha": "abc123"},
    }
    assert module.deterministic_checks(artifact) == []


def test_deterministic_checks_rejects_inconsistent_empirical_declaration():
    artifact = {
        "seed": 20260817,
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "empirical_n": 1,
    }
    checks = module.deterministic_checks(artifact)
    assert "non-empirical artifact cannot report empirical_n > 0" in checks


def test_deterministic_failure_overrides_model_pass(monkeypatch):
    artifact = {
        "seed": 20260817,
        "protocol_status": "INVALID",
        "empirical_data_collection": False,
        "empirical_n": 0,
    }

    monkeypatch.setattr(
        module,
        "call_openai",
        lambda prompt, api_key, model: {
            "decision": "PASS",
            "semantic_score": 1.0,
            "claim_type": "implementation",
            "strengths": ["coherent"],
            "concerns": [],
            "recommended_actions": [],
            "epistemic_boundary": "not efficacy evidence",
        },
    )

    result = module.evaluate(artifact, "test-key", "test-model")
    assert result["evaluation"]["decision"] == "FAIL"
    assert result["deterministic_checks"]
