"""Tests for governance-benchmark external review return validation."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts/validate_governance_benchmark_external_review_return.py"

spec = importlib.util.spec_from_file_location("return_validator", MODULE_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def valid_record() -> dict:
    digest = "a" * 64
    return {
        "schema_version": validator.SCHEMA_VERSION,
        "reviewer": {
            "durable_identity": "reviewer@example.org",
            "affiliation": "Independent Lab",
            "role": "Reviewer",
        },
        "independence_disclosure": {
            "relationship_to_project": "none",
            "prior_artifact_authorship_or_modification": False,
            "prior_outcome_access": False,
            "commercial_relationship": "none",
            "reviewer_stated_independence": True,
            "limitations": "none stated",
        },
        "environment": {
            "os": "Example OS",
            "python": "3.12.x",
            "git": "2.x",
            "notes": "clean clone",
        },
        "frozen_target": {
            "repository": "https://github.com/ndrorchestration/DGAF-Framework",
            "commit": validator.FROZEN_COMMIT,
            "expected_bundle_sha256": validator.EXPECTED_BUNDLE_SHA256,
        },
        "execution": {
            "first_attempt_preserved": True,
            "contract_tests": "PASS",
            "regenerated_bundle_sha256": validator.EXPECTED_BUNDLE_SHA256,
            "canonical_layer_digests": {
                "fixed": digest,
                "mutations": digest,
                "same_domain_interactions": digest,
                "cross_domain_interactions": digest,
            },
            "notes": "",
        },
        "returned_evidence": {
            "independently_retained_location": "content-addressed://example",
            "sha256": digest,
            "retained_before_project_owner_adjudication": True,
        },
        "disposition": "REPRODUCED",
        "claim_boundary": {
            "scientific_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "state_of_the_art": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
            "independent_validation_self_promoted": False,
        },
    }


def test_valid_reproduced_record_is_admissible() -> None:
    assert validator.validate(valid_record()) == []


def test_reproduced_requires_matching_frozen_bundle_digest() -> None:
    record = valid_record()
    record["execution"]["regenerated_bundle_sha256"] = "b" * 64
    errors = validator.validate(record)
    assert "REPRODUCED requires matching bundle digest" in errors


def test_first_attempt_must_be_preserved() -> None:
    record = valid_record()
    record["execution"]["first_attempt_preserved"] = False
    errors = validator.validate(record)
    assert "first attempt must be preserved" in errors


def test_returned_evidence_must_precede_owner_adjudication() -> None:
    record = valid_record()
    record["returned_evidence"]["retained_before_project_owner_adjudication"] = False
    errors = validator.validate(record)
    assert "returned evidence must be retained before project-owner adjudication" in errors


def test_claim_boundary_cannot_self_promote() -> None:
    record = valid_record()
    record["claim_boundary"]["independent_validation_self_promoted"] = True
    record["claim_boundary"]["state_of_the_art"] = "ESTABLISHED"
    errors = validator.validate(record)
    assert "independent validation cannot self-promote" in errors
    assert "SOTA cannot self-promote" in errors


def test_mismatch_is_valid_negative_outcome() -> None:
    record = valid_record()
    record["disposition"] = "MISMATCH"
    record["execution"]["contract_tests"] = "FAIL"
    record["execution"]["regenerated_bundle_sha256"] = "b" * 64
    assert validator.validate(record) == []
