#!/usr/bin/env python3
"""Read-only public-claim evidence linkage receipt.

This adapter consumes a caller-supplied observation of one public surface and
its claim-to-evidence mappings. It verifies structural bindings only. It does
not inspect live public copy, reverify project-local evidence, establish truth,
or alter any authority state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

OBSERVATION_SCHEMA = "PUBLIC_CLAIM_LINKAGE_OBSERVATION_V0"
RECEIPT_SCHEMA = "public-claim.evidence-linkage.v0-candidate"

SUPPORT_STATES = {
    "DIRECT_EVIDENCE_LINKED",
    "INDIRECT_OR_SUMMARY_ONLY",
    "NO_DIRECT_EVIDENCE_LINK",
    "NOT_INSPECTABLE",
    "UNKNOWN",
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _sha40(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(ch in "0123456789abcdef" for ch in value)


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _validate_surface_binding(binding: dict) -> None:
    required = {
        "manifest_schema_version",
        "surface_id",
        "source_repository",
        "source_commit",
        "source_blob_sha",
        "copy_state",
        "release_gate",
        "observed_at",
    }
    if not isinstance(binding, dict) or set(binding) != required:
        raise ValueError("surface_binding fields must match the closed candidate contract")
    if binding["manifest_schema_version"] != "NDR_PUBLIC_SURFACE_MANIFEST_V1":
        raise ValueError("unexpected public-surface manifest schema")
    for key in ("surface_id", "source_repository", "copy_state", "release_gate", "observed_at"):
        if not _nonempty(binding[key]):
            raise ValueError(f"surface_binding.{key} must be non-empty")
    if not _sha40(binding["source_commit"]):
        raise ValueError("surface_binding.source_commit must be a lowercase 40-character Git SHA")
    if not _sha40(binding["source_blob_sha"]):
        raise ValueError("surface_binding.source_blob_sha must be a lowercase 40-character Git blob SHA")


def _validate_authorities(authorities: dict) -> None:
    if not isinstance(authorities, dict) or not authorities:
        raise ValueError("canonical_authorities must be a non-empty object")
    for dependency, binding in authorities.items():
        if not _nonempty(dependency):
            raise ValueError("canonical authority dependency keys must be non-empty")
        if not isinstance(binding, dict) or set(binding) != {"repository", "repository_commit"}:
            raise ValueError(f"canonical authority {dependency} must contain repository and repository_commit")
        if not _nonempty(binding["repository"]):
            raise ValueError(f"canonical authority {dependency} repository must be non-empty")
        if not _sha40(binding["repository_commit"]):
            raise ValueError(f"canonical authority {dependency} repository_commit must be a lowercase Git SHA")


def _validate_evidence_ref(ref: dict, authority: dict) -> None:
    if not isinstance(ref, dict) or set(ref) != {"repository", "repository_commit", "path"}:
        raise ValueError("evidence reference fields must be repository, repository_commit, path")
    if ref["repository"] != authority["repository"]:
        raise ValueError("evidence repository does not match canonical authority")
    if ref["repository_commit"] != authority["repository_commit"]:
        raise ValueError("evidence reference does not match canonical authority commit")
    if not _nonempty(ref["path"]):
        raise ValueError("evidence reference path must be non-empty")


def link_claims(observation: dict) -> dict:
    """Produce a bounded, non-authorizing claim-linkage receipt."""

    required = {
        "schema_version",
        "surface_binding",
        "canonical_authorities",
        "claims",
    }
    if not isinstance(observation, dict) or set(observation) != required:
        raise ValueError("observation fields must match the closed candidate contract")
    if observation["schema_version"] != OBSERVATION_SCHEMA:
        raise ValueError(f"schema_version must be {OBSERVATION_SCHEMA}")

    _validate_surface_binding(observation["surface_binding"])
    _validate_authorities(observation["canonical_authorities"])

    claims = observation["claims"]
    if not isinstance(claims, list):
        raise ValueError("claims must be an array")

    seen_ids: set[str] = set()
    rows: list[dict] = []

    for claim in claims:
        claim_required = {
            "claim_id",
            "claim_text",
            "canonical_dependency",
            "support_state",
            "evidence_refs",
            "claim_not_supported",
            "basis",
        }
        if not isinstance(claim, dict) or set(claim) != claim_required:
            raise ValueError("claim fields must match the closed candidate contract")

        claim_id = claim["claim_id"]
        if not _nonempty(claim_id):
            raise ValueError("claim_id must be non-empty")
        if claim_id in seen_ids:
            raise ValueError(f"duplicate claim_id: {claim_id}")
        seen_ids.add(claim_id)

        for key in ("claim_text", "claim_not_supported", "basis"):
            if not _nonempty(claim[key]):
                raise ValueError(f"{key} must be non-empty")

        dependency = claim["canonical_dependency"]
        authorities = observation["canonical_authorities"]
        if dependency not in authorities:
            raise ValueError(f"canonical_dependency is not declared: {dependency}")
        authority = authorities[dependency]

        support_state = claim["support_state"]
        if support_state not in SUPPORT_STATES:
            raise ValueError(f"unsupported support_state: {support_state}")

        refs = claim["evidence_refs"]
        if not isinstance(refs, list):
            raise ValueError("evidence_refs must be an array")
        if support_state == "DIRECT_EVIDENCE_LINKED" and not refs:
            raise ValueError("DIRECT_EVIDENCE_LINKED requires at least one evidence reference")
        if support_state == "NO_DIRECT_EVIDENCE_LINK" and refs:
            raise ValueError("NO_DIRECT_EVIDENCE_LINK must not carry direct evidence references")

        for ref in refs:
            _validate_evidence_ref(ref, authority)

        rows.append(
            {
                **claim,
                "authority_binding_state": "MATCH" if refs else "NOT_APPLICABLE",
                "evidence_authority": authority,
            }
        )

    without_direct = sorted(row["claim_id"] for row in rows if row["support_state"] == "NO_DIRECT_EVIDENCE_LINK")
    summary_only = sorted(row["claim_id"] for row in rows if row["support_state"] == "INDIRECT_OR_SUMMARY_ONLY")
    not_inspectable = sorted(row["claim_id"] for row in rows if row["support_state"] == "NOT_INSPECTABLE")
    unknown = sorted(row["claim_id"] for row in rows if row["support_state"] == "UNKNOWN")

    direct_linkage_complete = bool(rows) and all(row["support_state"] == "DIRECT_EVIDENCE_LINKED" for row in rows)
    linkage_state = (
        "DIRECT_LINKAGE_COMPLETE_FOR_OBSERVED_CLAIMS" if direct_linkage_complete else "OBSERVED_WITH_LINKAGE_GAPS"
    )

    surface = observation["surface_binding"]
    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "observation_authority": "CALLER_SUPPLIED_NOT_REVERIFIED",
        "surface_binding": surface,
        "surface_release_gate": surface["release_gate"],
        "surface_release_gate_effect": "NONE",
        "claim_count": len(rows),
        "direct_linkage_count": sum(row["support_state"] == "DIRECT_EVIDENCE_LINKED" for row in rows),
        "claims": rows,
        "claims_without_direct_evidence": without_direct,
        "claims_indirect_or_summary_only": summary_only,
        "claims_not_inspectable": not_inspectable,
        "claims_unknown": unknown,
        "direct_linkage_complete": direct_linkage_complete,
        "linkage_state": linkage_state,
        "truth_effect": "NONE",
        "authorization_effect": "NONE",
        "scientific_state_effect": "NONE",
        "evidence_authority_effect": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", type=Path)
    args = parser.parse_args()

    try:
        receipt = link_claims(_load_object(args.observation))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["direct_linkage_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
