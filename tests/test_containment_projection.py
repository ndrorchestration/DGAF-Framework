import copy
import json
import unittest
from pathlib import Path

from scripts.dgaf_containment_assessment import AssessmentInputError
from scripts.generate_tektite_containment import build_projection, render_html

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/containment"


class ProjectionTests(unittest.TestCase):
    def test_priority_cases_and_actual_assessment_receipt_refusal(self):
        result = build_projection(FIXTURES)
        cases = {case["case_id"]: case for case in result["cases"]}
        self.assertEqual(set(cases), {"SC-01", "SC-05", "SC-13", "SC-16", "SC-28"})
        self.assertEqual(cases["SC-01"]["assessment"]["disposition"], "ESTABLISHED_IN_SCOPE")
        for case_id in ("SC-05", "SC-13", "SC-16"):
            self.assertEqual(cases[case_id]["assessment"]["disposition"], "NOT_ESTABLISHED")
        self.assertEqual(cases["SC-28"]["observed"], "REFUSED")
        self.assertEqual(cases["SC-28"]["dispatcher_calls"], 0)
        self.assertEqual(cases["SC-28"]["prior_assessment_digest"], cases["SC-01"]["assessment_digest"])
        self.assertEqual(result["evaluation_mode"], "FIXED_TIME_SNAPSHOT_REPLAY")
        self.assertEqual(result["claim_boundary"]["live_containment"], "NOT_ESTABLISHED")

    def test_deterministic_projection(self):
        self.assertEqual(build_projection(FIXTURES), build_projection(FIXTURES))

    def test_manifest_pin_is_required(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            fixtures = Path(directory) / "fixtures"
            shutil.copytree(FIXTURES, fixtures)
            manifest = json.loads((fixtures / "manifest.json").read_text())
            manifest["observations"]["SC-01"] = "sha256:" + "a" * 64
            (fixtures / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaises(AssessmentInputError):
                build_projection(fixtures)

    def test_html_escapes_embedded_record_and_labels_historical_scope(self):
        result = copy.deepcopy(build_projection(FIXTURES))
        result["cases"][0]["assessment"]["evidence_ids"] = ["</script><script>alert(1)</script>"]
        html = render_html(result)
        self.assertNotIn("</script><script>alert", html)
        self.assertIn("Fixed-time synthetic snapshot replay", html)
        self.assertIn("Live containment: NOT_ESTABLISHED", html)

    def test_retained_projection_matches_recomputed_output(self):
        saved = json.loads((ROOT / "public/evidence/tektite-containment-v0.json").read_text())
        self.assertEqual(saved, build_projection(FIXTURES))
