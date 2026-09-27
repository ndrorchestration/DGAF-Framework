"""Regression contract for Governance CI dependency admission (#1056)."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GovernanceBootstrapContract(unittest.TestCase):
    def test_main_environment_requires_hashes_and_binary_artifacts(self):
        workflow = (ROOT / ".github/workflows/governance-ci.yml").read_text()
        bootstrap = workflow.split("      - name: Emit E2b/M6 evidence", 1)[0]
        commands = re.findall(r"python -m pip install[^\n]*(?:\n        [^\n]+)*", bootstrap)
        self.assertTrue(commands, "main environment must explicitly install its locked dependencies")
        for command in commands:
            self.assertIn("--require-hashes", command)
            self.assertIn("--only-binary=:all:", command)
            self.assertNotIn("--upgrade", command)
        self.assertIn("bash scripts/bootstrap_ci_pip.sh", bootstrap)
        self.assertIn("runs-on: ubuntu-24.04", bootstrap)
        self.assertIn("requirements-ci-control-plane-py312-ubuntu2404-x64.lock", bootstrap)
        self.assertIn("requirements-ci-governance-networkx.lock", bootstrap)

    def test_networkx_overlay_retains_accepted_hash_identity(self):
        overlay = ROOT / "requirements-ci-governance-networkx.lock"
        self.assertTrue(overlay.is_file(), "NetworkX must not fall back to an unpinned inline install")
        content = overlay.read_text()
        self.assertIn("networkx==3.6.1", content)
        hashes = set(re.findall(r"--hash=sha256:([0-9a-f]{64})", content))
        self.assertEqual(
            hashes,
            {
                "26b7c357accc0c8cde558ad486283728b65b6a95d85ee1cd66bafab4c8168509",
                "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
            },
        )


if __name__ == "__main__":
    unittest.main()
