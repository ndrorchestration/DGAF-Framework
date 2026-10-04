#!/usr/bin/env python3
"""Read-only query view over existing DGAF ecosystem-state artifacts.

This module summarizes existing state. It does not establish live currentness,
promote claims, authorize effects, or create a new source of truth.
"""

from __future__ import annotations

import argparse
import json
import runpy
from pathlib import Path

POINTER_PATH = Path("registry/ecosystem_state_pointer.current.json")
COMPONENT_REGISTRY_PATH = Path("docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json")
RECEIPT_SCHEMA_PATH = Path("schemas/execution_receipt.schema.json")
TEKTITE_LEDGER_PATH = Path("docs/tektite-v0.1/evidence-ledger.seed.json")
TEKTITE_SEMANTIC_SOURCE_PATH = Path("registry/tektite_public_status_semantic_source_v1.json")
ACP_RECONCILIATION_SCHEMA_VERSION = "ACP_LIVE_RECONCILIATION_V0_CANDIDATE"
POINTER_VALIDATOR_PATH = Path("scripts/validate_ecosystem_state_pointer.py")
RECONCILIATION_SCHEMA_VERSION = "ECOSYSTEM_LIVE_RECONCILIATION_V1"


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def _pointer_module() -> dict:
    code_root = Path(__file__).resolve().parents[1]
    return runpy.run_path(str(code_root / POINTER_VALIDATOR_PATH))


def _validate_reconciliation_evidence(pointer: dict, evidence: dict) -> None:
    required = {
        "schema_version",
        "observed_at",
        "pointer_source_observation_commit",
        "live_repository_commit",
        "container_commit",
        "evidence_url",
    }
    if set(evidence) != required:
        missing = sorted(required - set(evidence))
        extra = sorted(set(evidence) - required)
        raise ValueError("reconciliation evidence fields mismatch: " f"missing={missing} extra={extra}")
    if evidence["schema_version"] != RECONCILIATION_SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {RECONCILIATION_SCHEMA_VERSION}")
    for key in ("observed_at", "evidence_url"):
        if not isinstance(evidence[key], str) or not evidence[key]:
            raise ValueError(f"{key} must be a non-empty string")

    pointer_module = _pointer_module()
    sha1_re = pointer_module["SHA1_RE"]
    for key in (
        "pointer_source_observation_commit",
        "live_repository_commit",
        "container_commit",
    ):
        if not isinstance(evidence[key], str) or not sha1_re.fullmatch(evidence[key]):
            raise ValueError(f"{key} must be a lowercase 40-character Git SHA")

    source = pointer["snapshot_provenance"]["source_observation_commit"]
    if evidence["pointer_source_observation_commit"] != source:
        raise ValueError("pointer_source_observation_commit must match the embedded pointer")
    if evidence["container_commit"] == source:
        raise ValueError("container_commit must not be treated as the source observation commit")


def _reconciliation_result(pointer: dict, evidence: dict | None) -> dict:
    if evidence is None:
        return {
            "scope": "DGAF_REPOSITORY_TIP_ONLY",
            "state": "NOT_SUPPLIED",
            "observed_at": None,
            "evidence_url": None,
            "live_repository_commit": None,
            "errors": [],
        }

    _validate_reconciliation_evidence(pointer, evidence)
    pointer_module = _pointer_module()
    errors = pointer_module["validate_live_reconciliation"](
        pointer,
        evidence["live_repository_commit"],
        evidence["container_commit"],
    )
    state = "REPOSITORY_TIP_MATCH" if not errors else "STALE_SOURCE_ADVANCED"
    return {
        "scope": "DGAF_REPOSITORY_TIP_ONLY",
        "state": state,
        "observed_at": evidence["observed_at"],
        "evidence_url": evidence["evidence_url"],
        "live_repository_commit": evidence["live_repository_commit"],
        "errors": errors,
    }


def _control_test_reference_scan(root: Path, registry: dict) -> dict:
    tests_dir = root / "tests"
    test_sources = {
        path: path.read_text(encoding="utf-8-sig", errors="ignore")
        for path in sorted(tests_dir.glob("test_*.py"))
        if path.name != "test_query_ecosystem_state.py"
    }
    rows = []
    for component in registry["core_components"]:
        for artifact in component["primary_artifacts"]:
            needle = Path(artifact).stem
            mentions = [
                path.relative_to(root).as_posix()
                for path, source in test_sources.items()
                if artifact in source or needle in source
            ]
            rows.append(
                {
                    "component_id": component["id"],
                    "artifact": artifact,
                    "direct_test_mentions": mentions,
                }
            )
    return {
        "scope": "DIRECT_TEST_REFERENCE_HEURISTIC_ONLY",
        "coverage": "NOT_ESTABLISHED",
        "rows": rows,
        "artifacts_without_direct_mentions": [row["artifact"] for row in rows if not row["direct_test_mentions"]],
    }


def _validate_acp_reconciliation_observation(manifest: dict, observation: dict) -> None:
    required = {
        "schema_version",
        "observed_at",
        "tektite_embedded_acp_commit",
        "live_acp_repository_commit",
        "evidence_url",
    }
    if set(observation) != required:
        missing = sorted(required - set(observation))
        extra = sorted(set(observation) - required)
        raise ValueError(f"ACP reconciliation fields mismatch: missing={missing} extra={extra}")
    if observation["schema_version"] != ACP_RECONCILIATION_SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {ACP_RECONCILIATION_SCHEMA_VERSION}")
    for key in ("observed_at", "evidence_url"):
        if not isinstance(observation[key], str) or not observation[key]:
            raise ValueError(f"{key} must be a non-empty string")

    pointer_module = _pointer_module()
    sha1_re = pointer_module["SHA1_RE"]
    for key in ("tektite_embedded_acp_commit", "live_acp_repository_commit"):
        if not isinstance(observation[key], str) or not sha1_re.fullmatch(observation[key]):
            raise ValueError(f"{key} must be a lowercase 40-character Git SHA")

    authorities = manifest.get("external_authorities")
    if not isinstance(authorities, list):
        raise ValueError("Tektite semantic manifest external_authorities must be an array")
    matches = [item for item in authorities if item.get("authority_id") == "ACP_SOURCE"]
    if len(matches) != 1:
        raise ValueError("Tektite semantic manifest must declare exactly one ACP_SOURCE")
    embedded = matches[0].get("object_identity")
    if observation["tektite_embedded_acp_commit"] != embedded:
        raise ValueError("tektite_embedded_acp_commit must match Tektite semantic manifest ACP_SOURCE")


def _acp_reconciliation_result(manifest: dict, observation: dict | None) -> dict:
    base = {
        "scope": "ACP_REPOSITORY_TIP_ONLY",
        "semantic_reconciliation": "NOT_ESTABLISHED",
        "authority_effect": "NONE",
        "cross_surface_reconciliation": "NOT_ESTABLISHED",
    }
    if observation is None:
        return {
            **base,
            "state": "NOT_SUPPLIED",
            "observed_at": None,
            "evidence_url": None,
            "live_acp_repository_commit": None,
        }

    _validate_acp_reconciliation_observation(manifest, observation)
    state = (
        "ACP_REPOSITORY_TIP_MATCH"
        if observation["tektite_embedded_acp_commit"] == observation["live_acp_repository_commit"]
        else "ACP_SOURCE_ADVANCED"
    )
    return {
        **base,
        "state": state,
        "observed_at": observation["observed_at"],
        "evidence_url": observation["evidence_url"],
        "live_acp_repository_commit": observation["live_acp_repository_commit"],
    }


def build_report(
    root: Path,
    required_consumers: list[str],
    reconciliation_evidence: dict | None = None,
    acp_reconciliation_observation: dict | None = None,
) -> dict:
    root = Path(root)
    pointer = _load_json(root / POINTER_PATH)
    pointer_module = _pointer_module()
    errors = pointer_module["validate"](pointer)
    if errors:
        raise ValueError("invalid ecosystem state pointer: " + "; ".join(errors))

    registry = _load_json(root / COMPONENT_REGISTRY_PATH)
    receipt_schema = _load_json(root / RECEIPT_SCHEMA_PATH)
    tektite_ledger = _load_json(root / TEKTITE_LEDGER_PATH)
    tektite_manifest = _load_json(root / TEKTITE_SEMANTIC_SOURCE_PATH)
    if tektite_ledger.get("schema") != "TEKTITE_V0_1_EVIDENCE_LEDGER_SEED":
        raise ValueError("unexpected Tektite evidence ledger schema")
    ledger_entries = tektite_ledger.get("entries")
    if not isinstance(ledger_entries, list):
        raise ValueError("Tektite evidence ledger entries must be an array")

    consumers = {
        item["consumer_id"]: {
            "manifest_path": item["manifest_path"],
            "freshness_state": item["freshness_state"],
            "invalidation_reason": item["invalidation_reason"],
            "authority_ids": item["authority_ids"],
            "semantic_material_digest_sha256": item["semantic_material_digest_sha256"],
        }
        for item in pointer["consumer_bindings"]
    }
    missing = sorted(set(required_consumers) - set(consumers))

    snapshot = pointer["snapshot_provenance"]
    live = snapshot["live_reconciliation"]
    embedded_states = {item["freshness_state"] for item in pointer["authorities"] + pointer["consumer_bindings"]}
    embedded_scope = "HISTORICAL_SNAPSHOT" if embedded_states == {"HISTORICAL_SNAPSHOT"} else "MIXED_OR_NON_HISTORICAL"

    reconciliation = _reconciliation_result(pointer, reconciliation_evidence)
    if reconciliation["state"] == "REPOSITORY_TIP_MATCH":
        live_currentness = "DGAF_REPOSITORY_TIP_MATCH_EXTERNAL"
    elif reconciliation["state"] == "STALE_SOURCE_ADVANCED":
        live_currentness = "STALE_SOURCE_ADVANCED"
    else:
        live_currentness = (
            "UNVERIFIED_NO_EXTERNAL_RECONCILIATION"
            if live["status"] == "NOT_EMBEDDED"
            else "EXTERNAL_RECONCILIATION_PRESENT"
        )

    acp_reconciliation = _acp_reconciliation_result(tektite_manifest, acp_reconciliation_observation)

    properties = receipt_schema["properties"]
    report = {
        "schema_version": "ECOSYSTEM_QUERY_REPORT_V1",
        "non_authorizing": True,
        "pointer": {
            "observed_at": pointer["observed_at"],
            "source_observation_commit": snapshot["source_observation_commit"],
            "embedded_scope": embedded_scope,
            "live_currentness": live_currentness,
            "live_reconciliation_required": live["required_for_repository_tip_currentness"],
        },
        "reconciliation": reconciliation,
        "acp_reconciliation": acp_reconciliation,
        "claim_ceiling": pointer["claim_ceiling"],
        "consumers": consumers,
        "receipt_authority": {
            "authority_effect": properties["authority_effect"]["const"],
            "follow_on_authority": properties["follow_on_authority"]["const"],
        },
        "public_claim_evidence": {
            "scope": "TEKTITE_V0_1_EVIDENCE_LEDGER_SEED_ONLY",
            "completeness": "NOT_ESTABLISHED",
            "entries": ledger_entries,
            "missing_public_link_artifacts": sorted(
                entry.get("artifact", "<unnamed>") for entry in ledger_entries if not entry.get("public_link")
            ),
        },
        "control_test_reference_scan": _control_test_reference_scan(root, registry),
        "component_registry": {
            "status": registry["status"],
            "core_component_ids": [item["id"] for item in registry["core_components"]],
            "assurance_component_ids": [item["id"] for item in registry["assurance_components"]],
            "governed_profile_ids": [item["id"] for item in registry["governed_profiles"]],
        },
        "gaps": {
            "missing_required_consumers": missing,
            "requires_dgaf_repository_reconciliation": live_currentness != "DGAF_REPOSITORY_TIP_MATCH_EXTERNAL",
            "cross_surface_reconciliation_not_established": True,
            "requires_acp_repository_reconciliation": acp_reconciliation["state"] != "ACP_REPOSITORY_TIP_MATCH",
            "requires_reconciliation": True,
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-consumer", action="append", default=[])
    parser.add_argument("--reconciliation-evidence", type=Path)
    parser.add_argument("--acp-reconciliation-observation", type=Path)
    args = parser.parse_args()

    try:
        reconciliation_evidence = _load_json(args.reconciliation_evidence) if args.reconciliation_evidence else None
        acp_reconciliation_observation = (
            _load_json(args.acp_reconciliation_observation) if args.acp_reconciliation_observation else None
        )
        report = build_report(
            args.root,
            args.require_consumer,
            reconciliation_evidence=reconciliation_evidence,
            acp_reconciliation_observation=acp_reconciliation_observation,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if report["gaps"]["requires_reconciliation"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
