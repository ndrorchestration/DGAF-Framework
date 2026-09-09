import copy
import json
import unittest
from pathlib import Path

from scripts.validate_mode_t_external_acceptance_manifest import (
    validate_manifest_structure,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "docs/governance/mode_t_external_acceptance_manifest.json"


class ModeTExternalAcceptanceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_current_manifest_is_structurally_conservative(self) -> None:
        self.assertEqual(validate_manifest_structure(self.manifest), [])

    def test_external_track_cannot_be_promoted(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["external_tracks"][0]["status"] = "PASS"
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("NOT_EXECUTED" in error for error in errors))

    def test_final_candidate_cannot_be_designated_by_handoff(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["scientific_state"]["final_candidate_status"] = "DESIGNATED"
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("final_candidate_status" in error for error in errors))

    def test_authorization_cannot_be_promoted(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["non_promotion"]["packet_is_authorization"] = True
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("packet_is_authorization" in error for error in errors))

    def test_reviewed_blob_must_be_exact_git_object_id(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["reviewed_sources"][0]["git_blob"] = "not-a-blob"
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("git_blob" in error for error in errors))

    def test_external_issue_set_is_closed(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["external_tracks"][0]["issue"] = 999
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("issue set" in error for error in errors))

    def test_schema_extension_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["unexpected"] = True
        errors = validate_manifest_structure(candidate)
        self.assertTrue(any("top-level keys" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
