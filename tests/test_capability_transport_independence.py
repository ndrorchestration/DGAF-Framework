from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import jsonschema
import pytest

from scripts.dgaf_mock_http_adapter import (
    MockHttpAdapterRefusal,
    dispatch_http,
)

ROOT = Path(__file__).resolve().parents[1]
MCP_MANIFESTS = ROOT / "docs" / "experiment" / "DGAF_LOCAL_MCP_CAPABILITY_MANIFESTS.draft.json"
HTTP_MANIFESTS = ROOT / "docs" / "experiment" / "DGAF_MOCK_HTTP_CAPABILITY_MANIFESTS.draft.json"


def load_bridge():
    scripts = ROOT / "scripts"
    path = scripts / "dgaf_local_operator_bridge.py"
    spec = importlib.util.spec_from_file_location("dgaf_local_operator_bridge_http_test", path)
    assert spec is not None and spec.loader is not None
    original = list(sys.path)
    try:
        sys.path.insert(0, str(scripts))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original
    return module


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def governed_fields(manifest):
    return {key: value for key, value in manifest.items() if key not in {"adapter", "signing", "lifecycle"}}


def test_mock_http_manifest_validates_against_same_capability_schema():
    schema = load_json(ROOT / "schemas" / "capability_manifest.schema.json")
    manifest = load_json(HTTP_MANIFESTS)["capabilities"][0]
    jsonschema.validate(manifest, schema)


def test_same_capability_identity_survives_transport_substitution():
    mcp = load_json(MCP_MANIFESTS)["capabilities"][0]
    http = load_json(HTTP_MANIFESTS)["capabilities"][0]

    assert mcp["id"] == http["id"] == "dgaf.local.status"
    assert mcp["version"] == http["version"]
    assert mcp["provider"] == http["provider"]
    assert mcp["adapter"]["kind"] == "mcp"
    assert http["adapter"]["kind"] == "rest"
    assert governed_fields(mcp) == governed_fields(http)


def test_mock_http_status_reaches_same_bridge_status_without_network_listener():
    bridge = load_bridge()
    response = dispatch_http(
        {"method": "GET", "path": "/v1/status"},
        bridge_dispatch=bridge.dispatch,
    )

    provider = response["provider_response"]
    assert response["network_listener"] is False
    assert response["capability_id"] == "dgaf.local.status"
    assert provider["bridge"] == "DGAF_LOCAL_OPERATOR_BRIDGE"
    assert provider["scientific_n_increment"] == 0
    assert provider["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"


def test_mock_http_adapter_rejects_unadmitted_route():
    bridge = load_bridge()
    with pytest.raises(MockHttpAdapterRefusal, match="route is not admitted"):
        dispatch_http(
            {"method": "POST", "path": "/v1/materialize"},
            bridge_dispatch=bridge.dispatch,
        )


def test_mock_http_adapter_rejects_extra_request_fields():
    bridge = load_bridge()
    with pytest.raises(MockHttpAdapterRefusal, match="exactly method and path"):
        dispatch_http(
            {"method": "GET", "path": "/v1/status", "body": {}},
            bridge_dispatch=bridge.dispatch,
        )
