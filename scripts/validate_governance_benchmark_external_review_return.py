"""Validate a returned external governance-benchmark reproduction record."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

FROZEN_COMMIT = "b5057bf836f67136c6030a81a604e5fd0d269076"
EXPECTED_BUNDLE_SHA256 = "1a55c88c7e8536be67ea13e2ba0718fc8318cc938f0b3bf4e275be4961c4de48"
SCHEMA_VERSION = "DGAF_GOVERNANCE_BENCHMARK_EXTERNAL_REVIEW_RETURN_V1"
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(record.get("schema_version") == SCHEMA_VERSION, "schema_version mismatch", errors)

    reviewer = record.get("reviewer") or {}
    for field in ("durable_identity", "affiliation", "role"):
        require(bool(reviewer.get(field)), f"reviewer.{field} required", errors)

    disclosure = record.get("independence_disclosure") or {}
    for field in (
        "relationship_to_project",
        "prior_artifact_authorship_or_modification",
        "prior_outcome_access",
        "commercial_relationship",
        "reviewer_stated_independence",
        "limitations",
    ):
        require(field in disclosure, f"independence_disclosure.{field} required", errors)

    environment = record.get("environment") or {}
    for field in ("os", "python", "git", "notes"):
        require(field in environment, f"environment.{field} required", errors)

    target = record.get("frozen_target") or {}
    require(target.get("commit") == FROZEN_COMMIT, "frozen_target.commit mismatch", errors)
    require(
        target.get("expected_bundle_sha256") == EXPECTED_BUNDLE_SHA256,
        "frozen_target.expected_bundle_sha256 mismatch",
        errors,
    )

    execution = record.get("execution") or {}
    require(execution.get("first_attempt_preserved") is True, "first attempt must be preserved", errors)
    require(execution.get("contract_tests") in {"PASS", "FAIL", "BLOCKED"}, "invalid contract_tests", errors)
    bundle_sha = execution.get("regenerated_bundle_sha256", "")
    require(bool(SHA256.fullmatch(bundle_sha)), "invalid regenerated_bundle_sha256", errors)

    digests = execution.get("canonical_layer_digests") or {}
    for field in ("fixed", "mutations", "same_domain_interactions", "cross_domain_interactions"):
        require(bool(SHA256.fullmatch(digests.get(field, ""))), f"invalid canonical digest: {field}", errors)

    evidence = record.get("returned_evidence") or {}
    require(bool(evidence.get("independently_retained_location")), "independently retained location required", errors)
    require(bool(SHA256.fullmatch(evidence.get("sha256", ""))), "returned evidence sha256 invalid", errors)
    require(
        evidence.get("retained_before_project_owner_adjudication") is True,
        "returned evidence must be retained before project-owner adjudication",
        errors,
    )

    disposition = record.get("disposition")
    require(disposition in {"REPRODUCED", "MISMATCH", "BLOCKED"}, "invalid disposition", errors)
    if disposition == "REPRODUCED":
        require(execution.get("contract_tests") == "PASS", "REPRODUCED requires PASS contract tests", errors)
        require(bundle_sha == EXPECTED_BUNDLE_SHA256, "REPRODUCED requires matching bundle digest", errors)

    boundary = record.get("claim_boundary") or {}
    require(boundary.get("scientific_n_increment") == 0, "scientific_n_increment must remain 0", errors)
    require(
        boundary.get("canonical_dgaf_efficacy") == "NOT_ESTABLISHED",
        "canonical DGAF efficacy cannot self-promote",
        errors,
    )
    require(boundary.get("state_of_the_art") == "NOT_ESTABLISHED", "SOTA cannot self-promote", errors)
    require(boundary.get("high_assurance") == "NOT_AUTHORIZED", "High-Assurance cannot self-promote", errors)
    require(
        boundary.get("independent_validation_self_promoted") is False,
        "independent validation cannot self-promote",
        errors,
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
