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
POINTER_VALIDATOR_PATH = Path("scripts/validate_ecosystem_state_pointer.py")


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def _pointer_validator():
    code_root = Path(__file__).resolve().parents[1]
    module = runpy.run_path(str(code_root / POINTER_VALIDATOR_PATH))
    return module["validate"]


def build_report(root: Path, required_consumers: list[str]) -> dict:
    root = Path(root)
    pointer = _load_json(root / POINTER_PATH)
    errors = _pointer_validator()(pointer)
    if errors:
        raise ValueError("invalid ecosystem state pointer: " + "; ".join(errors))

    registry = _load_json(root / COMPONENT_REGISTRY_PATH)
    receipt_schema = _load_json(root / RECEIPT_SCHEMA_PATH)

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
    live_currentness = (
        "UNVERIFIED_NO_EXTERNAL_RECONCILIATION"
        if live["status"] == "NOT_EMBEDDED"
        else "EXTERNAL_RECONCILIATION_PRESENT"
    )

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
        "claim_ceiling": pointer["claim_ceiling"],
        "consumers": consumers,
        "receipt_authority": {
            "authority_effect": properties["authority_effect"]["const"],
            "follow_on_authority": properties["follow_on_authority"]["const"],
        },
        "component_registry": {
            "status": registry["status"],
            "core_component_ids": [item["id"] for item in registry["core_components"]],
            "assurance_component_ids": [item["id"] for item in registry["assurance_components"]],
            "governed_profile_ids": [item["id"] for item in registry["governed_profiles"]],
        },
        "gaps": {
            "missing_required_consumers": missing,
            "requires_reconciliation": bool(missing) or live_currentness.startswith("UNVERIFIED"),
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-consumer", action="append", default=[])
    args = parser.parse_args()

    try:
        report = build_report(args.root, args.require_consumer)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if report["gaps"]["missing_required_consumers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
