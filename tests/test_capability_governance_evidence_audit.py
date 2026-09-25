from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from scripts.dgaf_capability_evidence import (
    EvidenceStrength,
    evidence_authority_monotonic,
    verification_implies_authorization,
)
from scripts.dgaf_capability_policy import Authority

ROOT = Path(__file__).resolve().parents[1]


def authority(capabilities, resources, budget=None):
    return Authority(
        capabilities=frozenset(capabilities),
        resources=frozenset(resources),
        max_budget=budget,
    )


def test_g5_verification_does_not_manufacture_authorization():
    assert (
        verification_implies_authorization(
            verified=True,
            authorization_status="PENDING",
        )
        is False
    )


def test_g5_verification_plus_active_authorization_is_admissible_input():
    assert (
        verification_implies_authorization(
            verified=True,
            authorization_status="ACTIVE",
        )
        is True
    )


def test_g16_weaker_evidence_cannot_expand_capabilities():
    prior = authority({"repo.read"}, {"repo:a"}, 10)
    expanded = authority({"repo.read", "repo.write"}, {"repo:a"}, 10)
    assert (
        evidence_authority_monotonic(
            prior_strength=EvidenceStrength.VERIFIED,
            prior_authority=prior,
            new_strength=EvidenceStrength.ASSERTED,
            new_authority=expanded,
        )
        is False
    )


def test_g16_weaker_evidence_cannot_expand_resource_scope():
    prior = authority({"repo.read"}, {"repo:a"}, 10)
    expanded = authority({"repo.read"}, {"repo:a", "repo:b"}, 10)
    assert (
        evidence_authority_monotonic(
            prior_strength=EvidenceStrength.VERIFIED,
            prior_authority=prior,
            new_strength=EvidenceStrength.CORROBORATED,
            new_authority=expanded,
        )
        is False
    )


def test_g16_weaker_evidence_can_reduce_authority():
    prior = authority({"repo.read", "repo.write"}, {"repo:a", "repo:b"}, 10)
    reduced = authority({"repo.read"}, {"repo:a"}, 5)
    assert (
        evidence_authority_monotonic(
            prior_strength=EvidenceStrength.VERIFIED,
            prior_authority=prior,
            new_strength=EvidenceStrength.ASSERTED,
            new_authority=reduced,
        )
        is True
    )


def test_capability_audit_schema_accepts_failure_record_with_provenance():
    schema = json.loads((ROOT / "schemas" / "capability_audit_event.schema.json").read_text(encoding="utf-8"))
    event = {
        "schema_version": "0.1-draft",
        "event_id": "audit:1",
        "event_type": "EXECUTION",
        "timestamp": "2026-09-25T13:15:00Z",
        "initiating_principal": "user:alice",
        "executing_principal": "gateway:local",
        "workflow_id": "workflow:1",
        "invocation_id": "invoke:1",
        "capability_id": "dgaf.local.materialize",
        "capability_version": "0.1.0",
        "policy": {"id": "policy:local-materialization", "version": "0.1.0"},
        "authorization_id": "auth:1",
        "delegation_chain_id": "delegation:1",
        "action_digest": "sha256:" + "a" * 64,
        "decision": "ALLOW",
        "decision_reasons": ["authorization_active", "commit_guards_passed"],
        "evidence_ids": ["evidence:input-verification"],
        "verifier_ids": ["verifier:1"],
        "adapter_identity": "dgaf-local-mcp-adapter",
        "runtime_identity": "runtime:local",
        "provider_receipt_id": None,
        "execution_state": "FAILED",
        "postcondition_state": "NOT_CHECKED",
        "recovery_state": "PENDING",
        "secret_material_present": False,
    }
    jsonschema.validate(event, schema)


def test_capability_audit_schema_forbids_secret_material_marker_true():
    schema = json.loads((ROOT / "schemas" / "capability_audit_event.schema.json").read_text(encoding="utf-8"))
    event = {
        "schema_version": "0.1-draft",
        "event_id": "audit:2",
        "event_type": "DECISION",
        "timestamp": "2026-09-25T13:15:00Z",
        "initiating_principal": "user:alice",
        "executing_principal": "gateway:local",
        "workflow_id": "workflow:1",
        "capability_id": "dgaf.local.materialize",
        "policy": {"id": "policy:local-materialization", "version": "0.1.0"},
        "authorization_id": "auth:1",
        "action_digest": "sha256:" + "a" * 64,
        "decision": "DENY",
        "execution_state": "NOT_STARTED",
        "postcondition_state": "NOT_CHECKED",
        "recovery_state": "NONE",
        "secret_material_present": True,
    }
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(event))
    assert errors
