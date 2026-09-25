from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.dgaf_capability_canonicalize import (
    CanonicalizationError,
    canonical_json_bytes,
    sha256_digest,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name: str) -> jsonschema.Draft202012Validator:
    schema = load_json(SCHEMAS / name)
    return jsonschema.Draft202012Validator(schema)
def test_local_mcp_capability_manifests_validate():
    schema = load_json(SCHEMAS / "capability_manifest.schema.json")
    manifest_set = load_json(
        ROOT / "docs" / "experiment" / "DGAF_LOCAL_MCP_CAPABILITY_MANIFESTS.draft.json"
    )
    for manifest in manifest_set["capabilities"]:
        jsonschema.validate(manifest, schema)


@pytest.mark.parametrize(
    "schema_name",
    [
        "authorization_object.schema.json",
        "delegation_chain.schema.json",
        "workflow_authorization.schema.json",
        "execution_receipt.schema.json",
        "reconciliation_record.schema.json",
    ],
)
def test_core_schemas_are_valid_json_schema(schema_name):
    jsonschema.Draft202012Validator.check_schema(load_json(SCHEMAS / schema_name))


def test_canonical_digest_vector_is_stable():
    vectors = load_json(FIXTURES / "capability_action_digest_vectors.json")
    vector = vectors["vectors"][0]
    assert canonical_json_bytes(vector["action"]).decode("utf-8") == vector["canonical_json"]
    assert sha256_digest(vector["action"]) == vector["sha256"]


def test_material_change_changes_action_digest():
    vectors = load_json(FIXTURES / "capability_action_digest_vectors.json")
    original = vectors["vectors"][0]["action"]
    changed = copy.deepcopy(original)
    changed["parameters"]["to"] = ["outside@example.org"]
    assert sha256_digest(changed) != sha256_digest(original)


def test_key_order_does_not_change_action_digest():
    vectors = load_json(FIXTURES / "capability_action_digest_vectors.json")
    original = vectors["vectors"][0]["action"]
    reordered = dict(reversed(list(original.items())))
    assert sha256_digest(reordered) == sha256_digest(original)


def test_nonfinite_values_fail_canonicalization():
    with pytest.raises(CanonicalizationError):
        canonical_json_bytes({"amount": float("nan")})


def test_authorization_rejects_invalid_digest():
    auth = {
        "schema_version": "0.1-draft",
        "authorization_id": "auth:1",
        "subject": "agent:assistant-7",
        "initiating_principal": "user:alice",
        "capability": {"id": "gmail.message.send", "version": "1.0.0"},
        "resource_scope": {"mailbox": "me"},
        "action_digest": "sha256:not-a-real-digest",
        "policy": {"id": "policy:outbound-mail", "version": "3.2.1"},
        "validity": {
            "not_before": "2026-09-25T12:00:00Z",
            "expires_at": "2026-09-25T13:00:00Z",
        },
        "status": "ACTIVE",
    }
    errors = list(validator("authorization_object.schema.json").iter_errors(auth))
    assert errors


def test_execution_receipt_preserves_unknown_outcome():
    receipt = {
        "schema_version": "0.1-draft",
        "invocation_id": "invoke:1",
        "workflow_id": "workflow:1",
        "authorization_id": "auth:1",
        "capability_id": "gmail.message.send",
        "action_digest": "sha256:" + "a" * 64,
        "idempotency_key": "idem:1",
        "attempt": 1,
        "execution_state": "EXECUTION_OUTCOME_UNKNOWN",
        "executor_identity": "gateway:local",
        "adapter_identity": "adapter:mcp",
        "provider_receipt": None,
        "timestamp": "2026-09-25T12:30:00Z",
        "postcondition_state": "INCONCLUSIVE",
        "recovery_state": "PENDING",
    }
    errors = list(validator("execution_receipt.schema.json").iter_errors(receipt))
    assert errors == []
