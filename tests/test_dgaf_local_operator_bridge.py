from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "scripts/dgaf_local_operator_bridge.py"


def load_bridge():
    spec = importlib.util.spec_from_file_location("dgaf_local_operator_bridge", BRIDGE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_status_is_non_authorizing_and_local_only():
    bridge = load_bridge()
    status = bridge.dispatch({"action": "status"})

    assert status["network_listener"] is False
    assert status["execution_class"] == "LOCAL_OPERATOR_ONLY"
    assert status["scientific_n_increment"] == 0
    assert status["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_request_schema_is_exact():
    bridge = load_bridge()

    with pytest.raises(bridge.BridgeRefusal, match="only the action field"):
        bridge.dispatch({"action": "status", "extra": "nope"})


def test_unknown_action_fails_closed():
    bridge = load_bridge()

    with pytest.raises(bridge.BridgeRefusal, match="unsupported action"):
        bridge.dispatch({"action": "shell"})


def test_retention_id_rejects_secret_bearing_tokens(monkeypatch):
    bridge = load_bridge()
    monkeypatch.setenv(bridge.ENV_RETENTION, "contains-private_key-material")

    with pytest.raises(bridge.BridgeRefusal, match="prohibited secret-bearing text"):
        bridge.configured_retention_id()


def test_paths_inside_repository_are_rejected(tmp_path, monkeypatch):
    bridge = load_bridge()
    inside = ROOT / "tests" / "fake-secret.pem"
    monkeypatch.setattr(bridge, "ROOT", ROOT)

    assert bridge.outside_repository(inside) is False


def test_get_evidence_rejects_authorized_analysis(tmp_path, monkeypatch):
    bridge = load_bridge()
    output = tmp_path / "bundle"
    output.mkdir()
    evidence = {
        "primary_analysis_authorized": True,
        "primary_analysis_run": False,
        "scientific_n_increment": 0,
    }
    (output / bridge.EVIDENCE_NAME).write_text(json.dumps(evidence), encoding="utf-8")
    monkeypatch.setenv(bridge.ENV_OUTPUT, str(output))

    with pytest.raises(
        bridge.BridgeRefusal,
        match="does not preserve primary-analysis non-authorization",
    ):
        bridge.get_evidence_response()


def test_get_evidence_returns_only_nonsecret_record(tmp_path, monkeypatch):
    bridge = load_bridge()
    output = tmp_path / "bundle"
    output.mkdir()
    evidence = {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "scientific_n_increment": 0,
    }
    (output / bridge.EVIDENCE_NAME).write_text(
        json.dumps(evidence, sort_keys=True),
        encoding="utf-8",
    )
    monkeypatch.setenv(bridge.ENV_OUTPUT, str(output))

    response = bridge.get_evidence_response()

    assert response["status"] == "PASS"
    assert response["evidence"] == evidence
    assert response["secret_material_returned"] is False
    assert "path" not in response
