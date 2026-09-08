from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "preflight_track_a_epoch_001_custody_key.py"


class TrackACustodyKeyPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCRIPT.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.text)

    def test_script_is_syntax_valid(self) -> None:
        self.assertIsInstance(self.tree, ast.Module)

    def test_exact_protected_and_certificate_digests_are_bound(self) -> None:
        self.assertIn(
            "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f",
            self.text,
        )
        self.assertIn(
            "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707",
            self.text,
        )

    def test_preflight_compares_public_keys_only(self) -> None:
        self.assertIn('"pkey", "-in", str(private_key), "-pubout"', self.text)
        self.assertIn('"x509", "-in", str(cert), "-pubkey", "-noout"', self.text)
        self.assertIn("private_public_der == cert_public_der", self.text)

    def test_preflight_does_not_decrypt_cms_payload(self) -> None:
        self.assertNotIn('"cms", "-decrypt"', self.text)
        self.assertNotIn("track_a_epoch_001_protected.cms", self.text)

    def test_private_key_is_not_printed_or_persisted(self) -> None:
        self.assertNotIn("read_bytes()", self.text)
        self.assertNotIn("write_text(private", self.text)
        self.assertNotIn("write_bytes(private", self.text)
        self.assertIn('print("PRIVATE_KEY_PUBLISHED=FALSE")', self.text)

    def test_boundary_remains_nonanalytical(self) -> None:
        self.assertIn('print("PROTECTED_MAPPING_DECRYPTED=FALSE")', self.text)
        self.assertIn('print("UNBLINDED_ANALYSIS_INPUT_MATERIALIZED=FALSE")', self.text)
        self.assertIn('print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")', self.text)


if __name__ == "__main__":
    unittest.main()
