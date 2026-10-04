#!/usr/bin/env python3
"""Read-only Tektite capability-projection reconciliation.

The adapter compares the existing Tektite status seed with a caller-supplied
external authority observation. It does not verify the external source itself,
rewrite Tektite state, or grant any authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

OBSERVATION_SCHEMA = "TEKTITE_CAPABILITY_AUTHORITY_OBSERVATION_V0"
RECEIPT_SCHEMA = "tektite.capability-projection-reconciliation.v0-candidate"
EXPECTED_AUTHORITY_ID = "ACP_SOURCE"
EXPECTED_REPOSITORY = "ndrorchestration/agent-control-plane"

CORE_PROJECTED_CAPABILITIES = {
    "LIVE_REPOSITORY_MUTATION",
    "ROLLBACK_EXECUTION",
    "PRODUCTION_EXECUTOR",
    "HIGH_ASSURANCE",
}


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_status_seed(seed: dict) -> None:
    if seed.get("schema") != "TEKTITE_V0_1_STATUS_SEED":
        raise ValueError("unexpected Tektite status seed schema")
    if not isinstance(seed.get("current_status"), dict):
        raise ValueError("Tektite current_status must be an object")
    if not isinstance(seed.get("active_blockers"), list):
        raise ValueError("Tektite active_blockers must be an array")


def _validate_observation(observation: dict) -> None:
    required = {
        "schema_version",
        "authority_id",
        "repository",
        "repository_commit",
        "source_artifact",
        "observed_at",
        "capability_states",
        "lifecycle_states",
    }
    if set(observation) != required:
        missing = sorted(required - set(observation))
        extra = sorted(set(observation) - required)
        raise ValueError(f"authority observation fields mismatch: missing={missing} extra={extra}")

    if observation["schema_version"] != OBSERVATION_SCHEMA:
        raise ValueError(f"schema_version must be {OBSERVATION_SCHEMA}")
    if observation["authority_id"] != EXPECTED_AUTHORITY_ID:
        raise ValueError(f"authority_id must be {EXPECTED_AUTHORITY_ID}")
    if observation["repository"] != EXPECTED_REPOSITORY:
        raise ValueError(f"repository must be {EXPECTED_REPOSITORY}")

    commit = observation["repository_commit"]
    if not (isinstance(commit, str) and len(commit) == 40 and all(ch in "0123456789abcdef" for ch in commit)):
        raise ValueError("repository_commit must be a lowercase 40-character Git SHA")

    for key in ("source_artifact", "observed_at"):
        if not _nonempty_string(observation[key]):
            raise ValueError(f"{key} must be a non-empty string")

    for key in ("capability_states", "lifecycle_states"):
        value = observation[key]
        if not isinstance(value, dict):
            raise ValueError(f"{key} must be an object")
        for state_key, state_value in value.items():
            if not _nonempty_string(state_key) or not _nonempty_string(state_value):
                raise ValueError(f"{key} keys and values must be non-empty strings")


def _semantic_authority_binding(semantic_manifest: dict | None, observation: dict) -> dict | None:
    if semantic_manifest is None:
        return None
    if semantic_manifest.get("manifest_id") != "TEKTITE_PUBLIC_STATUS_SEMANTIC_SOURCE_V1":
        raise ValueError("unexpected Tektite semantic-source manifest")
    authorities = semantic_manifest.get("external_authorities")
    if not isinstance(authorities, list):
        raise ValueError("semantic-source external_authorities must be an array")
    matches = [
        item for item in authorities if isinstance(item, dict) and item.get("authority_id") == EXPECTED_AUTHORITY_ID
    ]
    if len(matches) != 1:
        raise ValueError("semantic-source manifest must contain exactly one ACP_SOURCE authority")
    item = matches[0]
    identity = item.get("object_identity")
    if not (isinstance(identity, str) and len(identity) == 40 and all(ch in "0123456789abcdef" for ch in identity)):
        raise ValueError("semantic-source ACP_SOURCE object_identity must be a lowercase 40-character Git SHA")
    observed = observation["repository_commit"]
    return {
        "manifest_id": semantic_manifest["manifest_id"],
        "consumer": semantic_manifest.get("consumer"),
        "authority_id": EXPECTED_AUTHORITY_ID,
        "manifest_object_identity": identity,
        "observed_repository_commit": observed,
        "relation": "MATCH" if identity == observed else "STALE_AUTHORITY_POINTER",
        "current_answer_eligible": identity == observed,
    }


def reconcile(seed: dict, observation: dict | None, semantic_manifest: dict | None = None) -> dict:
    """Return a non-authorizing projection reconciliation receipt."""

    _validate_status_seed(seed)

    base = {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "observation_authority": "CALLER_SUPPLIED_NOT_REVERIFIED",
        "truth_effect": "NONE",
        "authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
    }

    if observation is None:
        return {
            **base,
            "reconciliation_state": "NOT_SUPPLIED",
            "currentness": "NOT_ESTABLISHED",
            "authority_binding": None,
            "semantic_authority_binding": None,
            "projection_rows": [],
            "lifecycle_rows": [],
            "unprojected_authority_states": [],
        }

    _validate_observation(observation)
    semantic_binding = _semantic_authority_binding(semantic_manifest, observation)

    current_status = seed["current_status"]
    capability_states = observation["capability_states"]
    lifecycle_states = observation["lifecycle_states"]

    projection_rows = []
    for key in sorted(CORE_PROJECTED_CAPABILITIES):
        projected = current_status.get(key)
        observed = capability_states.get(key)

        if projected is None:
            relation = "PROJECTION_MISSING"
            eligible = False
        elif observed is None:
            relation = "UNKNOWN"
            eligible = False
        elif projected == observed:
            relation = "MATCH"
            eligible = True
        else:
            relation = "MISMATCH_REQUIRES_REVIEW"
            eligible = False

        projection_rows.append(
            {
                "projection_key": key,
                "projected_value": projected,
                "observed_authority_value": observed,
                "relation": relation,
                "current_answer_eligible": eligible,
                "basis": (
                    "Exact string comparison against caller-supplied ACP authority observation; "
                    "no relative-strength inference is performed."
                ),
            }
        )

    lifecycle_rows = []
    for blocker in seed["active_blockers"]:
        blocker_id = blocker.get("id")
        projected_status = blocker.get("status")
        observed_status = lifecycle_states.get(blocker_id)

        if observed_status is None:
            relation = "UNKNOWN"
            eligible = False
        elif projected_status == observed_status:
            relation = "MATCH"
            eligible = True
        elif projected_status == "ACTIVE_BLOCKER" and observed_status.startswith("CLOSED_"):
            relation = "STALE_LIFECYCLE_LABEL"
            eligible = False
        else:
            relation = "MISMATCH_REQUIRES_REVIEW"
            eligible = False

        lifecycle_rows.append(
            {
                "blocker_id": blocker_id,
                "projected_status": projected_status,
                "observed_authority_status": observed_status,
                "relation": relation,
                "current_answer_eligible": eligible,
                "basis": (
                    "Lifecycle comparison only. Closure does not establish any capability "
                    "formerly associated with the blocker."
                ),
            }
        )

    represented_capability_keys = set(current_status)
    unprojected = [
        {
            "capability_key": key,
            "observed_authority_value": value,
            "relation": "UNPROJECTED_AUTHORITY_STATE",
            "current_answer_eligible": False,
        }
        for key, value in sorted(capability_states.items())
        if key not in represented_capability_keys
    ]

    all_projection_match = all(
        row["relation"] == "MATCH" for row in projection_rows if row["projected_value"] is not None
    )
    any_stale_lifecycle = any(row["relation"] == "STALE_LIFECYCLE_LABEL" for row in lifecycle_rows)
    reconciliation_state = (
        "OBSERVED_WITH_STALE_LIFECYCLE_LABELS"
        if any_stale_lifecycle and all_projection_match
        else "OBSERVED_REQUIRES_REVIEW"
    )

    return {
        **base,
        "reconciliation_state": reconciliation_state,
        "currentness": "PARTIAL_EXTERNAL_OBSERVATION",
        "semantic_authority_binding": semantic_binding,
        "authority_binding": {
            "authority_id": observation["authority_id"],
            "repository": observation["repository"],
            "repository_commit": observation["repository_commit"],
            "source_artifact": observation["source_artifact"],
            "observed_at": observation["observed_at"],
        },
        "projection_rows": projection_rows,
        "lifecycle_rows": lifecycle_rows,
        "unprojected_authority_states": unprojected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("status_seed", type=Path)
    parser.add_argument("--authority-observation", type=Path)
    parser.add_argument("--semantic-manifest", type=Path)
    args = parser.parse_args()

    try:
        seed = _load_object(args.status_seed)
        observation = _load_object(args.authority_observation) if args.authority_observation else None
        semantic_manifest = _load_object(args.semantic_manifest) if args.semantic_manifest else None
        receipt = reconcile(seed, observation, semantic_manifest=semantic_manifest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 2 if receipt["currentness"] != "PARTIAL_EXTERNAL_OBSERVATION" else 0


if __name__ == "__main__":
    raise SystemExit(main())
