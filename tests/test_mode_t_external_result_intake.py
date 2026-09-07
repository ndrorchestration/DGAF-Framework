import copy
import json
import subprocess
import unittest
from pathlib import Path

from scripts.validate_mode_t_external_result_intake import (
    validate_intake_structure,
    validate_repository_binding,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO_ROOT / "docs/governance/mode_t_external_result_intake_template.json"

REQUIRED_OUTPUT_320 = (
    "independently attributable review with exact reviewed blobs, findings, severities, evidence, and disposition"
)
REQUIRED_OUTPUT_310 = (
    "real authenticated Confidential Space PRE/POST admission evidence plus independent retrieval and reverification"
)


def make_submission(template: dict) -> dict:
    candidate = copy.deepcopy(template)
    candidate["record_state"] = "EXTERNAL_SUBMISSION_UNVERIFIED"
    candidate["track"] = {
        "issue": 320,
        "track": "independent_oidc_security_review",
        "required_output": REQUIRED_OUTPUT_320,
    }
    candidate["producer"] = {
        "name": "External Reviewer",
        "organization": "Example Review Organization",
        "external_identifier": "reviewer:example-001",
        "independence_claimed": True,
        "independence_basis": (
            "Reviewer states organizational and operational independence from the " "producing repository principal."
        ),
        "attribution_evidence_refs": ["reviewer-attribution"],
    }
    candidate["submission"] = {
        "submitted_at_utc": "2026-09-07T04:00:00Z",
        "external_record_uri": "urn:example:external-review-record",
        "external_record_sha256": "a" * 64,
    }
    candidate["external_result"] = {
        "execution_state": "EXECUTED",
        "execution_phase": "TRACK_SPECIFIC",
        "external_disposition": "PASS",
        "claims": [
            {
                "claim_id": "oidc-review-001",
                "result": "PASS",
                "evidence_refs": ["review-report"],
                "notes": "External result preserved as reported; not locally adjudicated.",
            }
        ],
        "evidence_artifacts": [
            {
                "artifact_id": "reviewer-attribution",
                "uri": "urn:example:reviewer-attribution",
                "sha256": "c" * 64,
                "media_type": "application/json",
                "description": "Externally supplied reviewer attribution/provenance record.",
            },
            {
                "artifact_id": "review-report",
                "uri": "urn:example:review-report",
                "sha256": "b" * 64,
                "media_type": "application/pdf",
                "description": "Externally produced review report.",
            },
        ],
    }
    return candidate


def handoff_history_available(template: dict) -> bool:
    handoff_sha = template["source_handoff"]["handoff_merge_sha"]
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{handoff_sha}^{{commit}}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


class ModeTExternalResultIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))

    def require_handoff_history(self) -> None:
        if not handoff_history_available(self.template):
            self.skipTest(
                "immutable #343 handoff commit unavailable in shallow checkout; "
                "repository binding is exercised by the full-history intake workflow"
            )

    def test_pristine_template_is_valid(self) -> None:
        self.assertEqual(validate_intake_structure(self.template), [])

    def test_unverified_external_submission_is_valid(self) -> None:
        submission = make_submission(self.template)
        self.assertEqual(validate_intake_structure(submission), [])

    def test_unverified_external_submission_is_repository_bound(self) -> None:
        self.require_handoff_history()
        submission = make_submission(self.template)
        self.assertEqual(validate_repository_binding(submission, REPO_ROOT), [])

    def test_external_pass_does_not_verify_independence(self) -> None:
        submission = make_submission(self.template)
        submission["ingestion_state"]["attribution_verified"] = True
        errors = validate_intake_structure(submission)
        self.assertTrue(any("attribution_verified" in error for error in errors))

    def test_external_pass_does_not_retrieve_artifacts(self) -> None:
        submission = make_submission(self.template)
        submission["ingestion_state"]["artifacts_retrieved"] = True
        errors = validate_intake_structure(submission)
        self.assertTrue(any("artifacts_retrieved" in error for error in errors))

    def test_external_pass_does_not_adjudicate_governance(self) -> None:
        submission = make_submission(self.template)
        submission["ingestion_state"]["governance_adjudication_status"] = "PASS"
        errors = validate_intake_structure(submission)
        self.assertTrue(any("governance_adjudication_status" in error for error in errors))

    def test_external_pass_cannot_close_p4(self) -> None:
        submission = make_submission(self.template)
        submission["scientific_state"]["p4_status"] = "CLOSED"
        errors = validate_intake_structure(submission)
        self.assertTrue(any("p4_status" in error for error in errors))

    def test_external_pass_cannot_grant_authorization(self) -> None:
        submission = make_submission(self.template)
        submission["non_promotion"]["envelope_grants_authorization"] = True
        errors = validate_intake_structure(submission)
        self.assertTrue(any("envelope_grants_authorization" in error for error in errors))

    def test_submission_track_name_must_match_issue(self) -> None:
        submission = make_submission(self.template)
        submission["track"]["track"] = "protected_continuity_acceptance"
        errors = validate_intake_structure(submission)
        self.assertTrue(any("track name" in error for error in errors))

    def test_submission_requires_handoff_required_output(self) -> None:
        submission = make_submission(self.template)
        submission["track"]["required_output"] = None
        errors = validate_intake_structure(submission)
        self.assertTrue(any("required_output is required" in error for error in errors))

    def test_required_output_must_match_handoff_manifest(self) -> None:
        self.require_handoff_history()
        submission = make_submission(self.template)
        submission["track"]["required_output"] = "different obligation"
        self.assertEqual(validate_intake_structure(submission), [])
        errors = validate_repository_binding(submission, REPO_ROOT)
        self.assertTrue(any("required_output does not match" in error for error in errors))

    def test_submission_requires_external_record_digest(self) -> None:
        submission = make_submission(self.template)
        submission["submission"]["external_record_sha256"] = "not-a-digest"
        errors = validate_intake_structure(submission)
        self.assertTrue(any("external_record_sha256" in error for error in errors))

    def test_submission_requires_evidence(self) -> None:
        submission = make_submission(self.template)
        submission["external_result"]["evidence_artifacts"] = []
        errors = validate_intake_structure(submission)
        self.assertTrue(any("at least one evidence artifact" in error for error in errors))

    def test_claim_cannot_reference_unknown_artifact(self) -> None:
        submission = make_submission(self.template)
        submission["external_result"]["claims"][0]["evidence_refs"] = ["missing"]
        errors = validate_intake_structure(submission)
        self.assertTrue(any("unknown artifacts" in error for error in errors))

    def test_independence_claim_requires_basis(self) -> None:
        submission = make_submission(self.template)
        submission["producer"]["independence_basis"] = None
        errors = validate_intake_structure(submission)
        self.assertTrue(any("independence_basis" in error for error in errors))

    def test_submission_requires_attribution_evidence(self) -> None:
        submission = make_submission(self.template)
        submission["producer"]["attribution_evidence_refs"] = []
        errors = validate_intake_structure(submission)
        self.assertTrue(any("attribution evidence" in error for error in errors))

    def test_attribution_cannot_reference_unknown_artifact(self) -> None:
        submission = make_submission(self.template)
        submission["producer"]["attribution_evidence_refs"] = ["missing"]
        errors = validate_intake_structure(submission)
        self.assertTrue(any("attribution_evidence_refs" in error for error in errors))

    def test_issue_310_must_distinguish_stage_a_or_b(self) -> None:
        submission = make_submission(self.template)
        submission["track"] = {
            "issue": 310,
            "track": "real_confidential_space_admission",
            "required_output": REQUIRED_OUTPUT_310,
        }
        submission["external_result"]["execution_phase"] = "TRACK_SPECIFIC"
        errors = validate_intake_structure(submission)
        self.assertTrue(any("Stage A" in error for error in errors))

    def test_issue_310_stage_a_submission_is_valid(self) -> None:
        self.require_handoff_history()
        submission = make_submission(self.template)
        submission["track"] = {
            "issue": 310,
            "track": "real_confidential_space_admission",
            "required_output": REQUIRED_OUTPUT_310,
        }
        submission["external_result"]["execution_phase"] = "STAGE_A_APPARATUS_QUALIFICATION"
        self.assertEqual(validate_intake_structure(submission), [])
        self.assertEqual(validate_repository_binding(submission, REPO_ROOT), [])

    def test_schema_extension_fails_closed(self) -> None:
        submission = make_submission(self.template)
        submission["unexpected"] = True
        errors = validate_intake_structure(submission)
        self.assertTrue(any("top-level keys" in error for error in errors))

    def test_template_cannot_claim_execution(self) -> None:
        candidate = copy.deepcopy(self.template)
        candidate["external_result"]["execution_state"] = "EXECUTED"
        errors = validate_intake_structure(candidate)
        self.assertTrue(any("template execution_state" in error for error in errors))

    def test_template_cannot_claim_execution_phase(self) -> None:
        candidate = copy.deepcopy(self.template)
        candidate["external_result"]["execution_phase"] = "TRACK_SPECIFIC"
        errors = validate_intake_structure(candidate)
        self.assertTrue(any("template execution_phase" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
