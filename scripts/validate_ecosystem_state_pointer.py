#!/usr/bin/env python3
"""Validate and compare ecosystem freshness pointers and semantic manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "ECOSYSTEM_STATE_POINTER_V1"
MANIFEST_VERSION = "SEMANTIC_SOURCE_MANIFEST_V1"
FRESHNESS = {"CURRENT", "STALE_SOURCE_ADVANCED", "UNVERIFIED", "HISTORICAL_SNAPSHOT"}
REASONS = {
    "NONE",
    "SEMANTIC_SOURCE_CHANGED",
    "NON_SEMANTIC_REPOSITORY_ADVANCE",
    "DEPENDENCY_ADVANCED",
    "MISSING_BINDING",
    "UNVERIFIED",
}
SURFACES = {"GITHUB", "NOTION", "GOOGLE_DRIVE", "RDC_LOCAL", "TEKTITE_PUBLIC", "OTHER"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def validate(pointer: dict) -> list[str]:
    errors: list[str] = []
    if pointer.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be ECOSYSTEM_STATE_POINTER_V1")
    if not isinstance(pointer.get("observed_at"), str) or not pointer["observed_at"]:
        errors.append("observed_at must be a non-empty string")

    authorities = pointer.get("authorities")
    if not isinstance(authorities, list) or not authorities:
        errors.append("authorities must be a non-empty array")
        authorities = []

    authority_ids: set[str] = set()
    for i, item in enumerate(authorities):
        prefix = f"authorities[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        aid = item.get("authority_id")
        if not isinstance(aid, str) or not aid:
            errors.append(f"{prefix}.authority_id must be non-empty")
        elif aid in authority_ids:
            errors.append(f"{prefix}.authority_id is duplicated: {aid}")
        else:
            authority_ids.add(aid)
        if item.get("surface") not in SURFACES:
            errors.append(f"{prefix}.surface is invalid")
        if item.get("freshness_state") not in FRESHNESS:
            errors.append(f"{prefix}.freshness_state is invalid")
        if item.get("invalidation_reason") not in REASONS:
            errors.append(f"{prefix}.invalidation_reason is invalid")
        if not isinstance(item.get("object_identity"), str) or not item["object_identity"]:
            errors.append(f"{prefix}.object_identity must be non-empty")

    bindings = pointer.get("consumer_bindings")
    if not isinstance(bindings, list) or not bindings:
        errors.append("consumer_bindings must be a non-empty array")
        bindings = []

    consumer_ids: set[str] = set()
    for i, item in enumerate(bindings):
        prefix = f"consumer_bindings[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        cid = item.get("consumer_id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"{prefix}.consumer_id must be non-empty")
        elif cid in consumer_ids:
            errors.append(f"{prefix}.consumer_id is duplicated: {cid}")
        else:
            consumer_ids.add(cid)

        refs = item.get("authority_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{prefix}.authority_ids must be non-empty")
        else:
            missing = sorted({ref for ref in refs if ref not in authority_ids})
            if missing:
                errors.append(f"{prefix}.authority_ids reference missing authorities: {missing}")

        digest = item.get("manifest_digest_sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}.manifest_digest_sha256 must be lowercase SHA-256")
        if item.get("freshness_state") not in FRESHNESS:
            errors.append(f"{prefix}.freshness_state is invalid")
        if item.get("invalidation_reason") not in REASONS:
            errors.append(f"{prefix}.invalidation_reason is invalid")
        if not isinstance(item.get("manifest_path"), str) or not item["manifest_path"]:
            errors.append(f"{prefix}.manifest_path must be non-empty")

    required_ceiling = {
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
        "live_repository_mutation": "NOT_AUTHORIZED",
        "production_executor": "NOT_ESTABLISHED",
    }
    if pointer.get("claim_ceiling") != required_ceiling:
        errors.append("claim_ceiling must preserve the fixed v1 non-promotion boundary")

    policy = pointer.get("freshness_policy", {})
    for key in (
        "whole_repository_identity_is_provenance",
        "semantic_manifest_controls_material_change",
        "consumer_specific_bindings_required",
        "unknown_change_fails_closed",
    ):
        if policy.get(key) is not True:
            errors.append(f"freshness_policy.{key} must be true")
    return errors


def canonical_manifest_digest(manifest: dict) -> str:
    material = dict(manifest)
    material.pop("manifest_digest_sha256", None)
    encoded = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != MANIFEST_VERSION:
        errors.append("manifest schema_version must be SEMANTIC_SOURCE_MANIFEST_V1")
    if not isinstance(manifest.get("manifest_id"), str) or not manifest["manifest_id"]:
        errors.append("manifest_id must be non-empty")
    if not isinstance(manifest.get("consumer"), str) or not manifest["consumer"]:
        errors.append("consumer must be non-empty")
    commit = manifest.get("repository_commit")
    if not isinstance(commit, str) or not SHA1_RE.fullmatch(commit):
        errors.append("repository_commit must be a lowercase 40-character Git SHA")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty array")
        artifacts = []
    paths: set[str] = set()
    for i, item in enumerate(artifacts):
        prefix = f"artifacts[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        path = item.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{prefix}.path must be non-empty")
        elif path in paths:
            errors.append(f"{prefix}.path is duplicated: {path}")
        else:
            paths.add(path)
        blob = item.get("git_blob_sha1")
        if not isinstance(blob, str) or not SHA1_RE.fullmatch(blob):
            errors.append(f"{prefix}.git_blob_sha1 must be a lowercase 40-character Git SHA")
        if not isinstance(item.get("role"), str) or not item["role"]:
            errors.append(f"{prefix}.role must be non-empty")

    expected = manifest.get("manifest_digest_sha256")
    actual = canonical_manifest_digest(manifest)
    if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
        errors.append("manifest_digest_sha256 must be lowercase SHA-256")
    elif expected != actual:
        errors.append(f"manifest_digest_sha256 mismatch: expected {expected}, recomputed {actual}")
    return errors


def classify(previous: dict, current: dict) -> dict:
    old_authorities = {x["authority_id"]: x for x in previous["authorities"]}
    new_authorities = {x["authority_id"]: x for x in current["authorities"]}
    changed_authorities = {
        aid
        for aid in set(old_authorities) | set(new_authorities)
        if old_authorities.get(aid, {}).get("object_identity") != new_authorities.get(aid, {}).get("object_identity")
    }

    old_bindings = {x["consumer_id"]: x for x in previous["consumer_bindings"]}
    new_bindings = {x["consumer_id"]: x for x in current["consumer_bindings"]}
    consumer_results: list[dict] = []
    for cid in sorted(set(old_bindings) | set(new_bindings)):
        before = old_bindings.get(cid)
        after = new_bindings.get(cid)
        if before is None or after is None:
            classification = "DEPENDENCY_ADVANCED"
        else:
            old_digest = before.get("manifest_digest_sha256")
            new_digest = after.get("manifest_digest_sha256")
            if not old_digest or not new_digest:
                classification = "UNVERIFIED"
            elif old_digest != new_digest:
                classification = "SEMANTIC_SOURCE_CHANGED"
            elif changed_authorities.intersection(after.get("authority_ids", [])):
                classification = "NON_SEMANTIC_REPOSITORY_ADVANCE"
            else:
                classification = "NONE"
        consumer_results.append({"consumer_id": cid, "classification": classification})

    return {
        "changed_authorities": sorted(changed_authorities),
        "consumer_bindings": consumer_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pointer", type=Path)
    parser.add_argument("--compare", type=Path, help="previous pointer to compare against")
    parser.add_argument("--manifest", action="append", type=Path, default=[])
    args = parser.parse_args()

    current = load(args.pointer)
    errors = validate(current)
    for manifest_path in args.manifest:
        errors.extend(f"{manifest_path}: {error}" for error in validate_manifest(load(manifest_path)))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("ECOSYSTEM_STATE_POINTER_V1: PASS")
    for manifest_path in args.manifest:
        print(f"SEMANTIC_SOURCE_MANIFEST_V1: PASS {manifest_path}")

    if args.compare:
        previous = load(args.compare)
        old_errors = validate(previous)
        if old_errors:
            for error in old_errors:
                print(f"ERROR previous: {error}", file=sys.stderr)
            return 1
        print(json.dumps(classify(previous, current), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
