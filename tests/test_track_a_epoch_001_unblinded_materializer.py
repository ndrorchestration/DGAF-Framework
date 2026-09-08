from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts" / "materialize_track_a_epoch_001_unblinded_input.py"


class TrackAUnblindingMaterializerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = MATERIALIZER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.text)

    def test_script_is_syntax_valid_and_has_no_analysis_import(self) -> None:
        imported = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertNotIn("experiments.pdmal_pilot.track_a_epoch_001_analysis", imported)
        self.assertNotIn("track_a_epoch_001_analysis", imported)

    def test_exact_authorization_and_artifact_digests_are_bound(self) -> None:
        for value in (
            "2e1981870a8455abed36fd72dcb3aaa35e2f9bff",
            "659aaa4dea2dd42624747952f1a47f307e69a014",
            "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231",
            "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f",
            "15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614",
            "ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35",
            "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707",
        ):
            self.assertIn(value, self.text)

    def test_decryption_is_cms_and_requires_separate_private_key(self) -> None:
        self.assertIn('"openssl",', self.text)
        self.assertIn('"cms",', self.text)
        self.assertIn('"-decrypt",', self.text)
        self.assertIn('"-inkey",', self.text)
        self.assertIn("--custody-private-key", self.text)

    def test_output_is_unblinded_input_not_primary_result(self) -> None:
        self.assertIn("TRACK_A_EPOCH_001_UNBLINDED_ANALYSIS_INPUT", self.text)
        self.assertIn('"primary_analysis_authorized": False', self.text)
        self.assertIn('"primary_analysis_run": False', self.text)
        self.assertIn('"outcome_aggregation_performed": False', self.text)
        self.assertNotIn("paired_bootstrap_ci(", self.text)
        self.assertNotIn("primary_estimate(", self.text)

    def test_exact_matrix_shape_is_enforced(self) -> None:
        self.assertIn("EXPECTED_TOTAL = 2250", self.text)
        self.assertIn("len(seed_records) == 45", self.text)
        self.assertIn("len(mapping) == 5", self.text)
        self.assertIn("seen_cells == expected_cells", self.text)

    def test_private_key_material_is_never_written_to_output(self) -> None:
        self.assertNotIn('read_text(encoding="utf-8")\n        output', self.text)
        self.assertNotIn('"private_key"', self.text)
        self.assertNotIn('"custody_private_key"', self.text)


if __name__ == "__main__":
    unittest.main()
