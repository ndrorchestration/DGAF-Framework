import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governance-ci.yml"

TLA_URL = "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"
TLA_SIZE = "2274532"
TLA_SHA1 = "bee4a54f3ee3d4afc347c3240ec2d9e93b075104"
TLA_SHA256 = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"


class TestGovernanceTlaplusPinContract(unittest.TestCase):
    def test_governance_ci_uses_exact_byte_identity_without_release_api_dependency(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("api.github.com/repos/tlaplus/tlaplus/releases", workflow)
        self.assertIn(TLA_URL, workflow)
        self.assertIn(TLA_SIZE, workflow)
        self.assertIn(TLA_SHA1, workflow)
        self.assertIn(TLA_SHA256, workflow)
        self.assertIn("stat -c '%s' tla2tools.jar", workflow)
        self.assertIn("sha1sum --check --strict", workflow)
        self.assertIn("sha256sum --check --strict", workflow)
        self.assertIn("--retry-all-errors", workflow)
        self.assertIn("runtime does not depend on release API availability", workflow)

    def test_tlc_model_check_remains_mandatory(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "java -cp tla2tools.jar tlc2.TLC -config specs/DGAFContainment.cfg specs/DGAFContainment.tla",
            workflow,
        )
        self.assertIn("Model checking completed. No error has been found.", workflow)
        self.assertIn("artifacts/tlc_model_check.txt", workflow)
        self.assertIn("artifacts/tlc_evidence.json", workflow)


if __name__ == "__main__":
    unittest.main()
