from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from mode_t_retention_contract import TransparencyExpectation, verify_transparency_inclusion
from mode_t_sigstore_verifier import (
    EXPECTED_OIDC_ISSUER,
    SigstoreVerifierError,
    retention_safe_evidence,
    verify_sigstore_bundle,
)

IDENTITY = "https://github.com/ndrorchestration/DGAF-Framework/.github/workflows/p4-mode-t-transparency.yml@refs/heads/main"


def bundle_fixture(*, entries: int = 1, inclusion: bool = True) -> dict:
    item = {
        "logIndex": 310,
        "integratedTime": 1_800_000_000,
        "logId": {"keyId": "synthetic-log-key-id"},
    }
    if inclusion:
        item["inclusionProof"] = {"checkpoint": "synthetic"}
    return {
        "verificationMaterial": {
            "tlogEntries": [dict(item) for _ in range(entries)]
        }
    }


class ModeTSigstoreVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.cosign = root / "cosign"
        self.artifact = root / "record.json"
        self.bundle = root / "bundle.json"
        self.cosign.write_bytes(b"reviewed-cosign-fixture")
        self.artifact.write_bytes(b'{"record":"synthetic"}\n')
        self.bundle.write_text(json.dumps(bundle_fixture()), encoding="utf-8")
        self.cosign_sha = hashlib.sha256(self.cosign.read_bytes()).hexdigest()

    def tearDown(self) -> None:
        self.temp.cleanup()

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_verified_bundle_flows_into_retention_contract_without_promotion(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        context = verify_sigstore_bundle(
            cosign=self.cosign,
            expected_cosign_sha256=self.cosign_sha,
            artifact=self.artifact,
            bundle=self.bundle,
            certificate_identity=IDENTITY,
        )
        expectation = TransparencyExpectation(
            record_type="PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION",
            record_sha256=hashlib.sha256(self.artifact.read_bytes()).hexdigest(),
            certificate_identity=IDENTITY,
        )
        result = verify_transparency_inclusion(expectation, context)
        self.assertEqual(result["retention_contract"], "PASS_NORMALIZED_INCLUSION_ONLY")
        self.assertFalse(result["real_external_retention_established"])
        self.assertFalse(result["temporal_order_verified"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)
        args = run.call_args.args[0]
        self.assertEqual(args[1], "verify-blob")
        self.assertIn("--certificate-identity", args)
        self.assertIn(IDENTITY, args)
        self.assertIn("--certificate-oidc-issuer", args)
        self.assertIn(EXPECTED_OIDC_ISSUER, args)
        self.assertNotIn("sign-blob", args)

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_cosign_failure(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 1, stdout="", stderr="reject")
        with self.assertRaisesRegex(SigstoreVerifierError, "rejected artifact/bundle"):
            verify_sigstore_bundle(
                cosign=self.cosign,
                expected_cosign_sha256=self.cosign_sha,
                artifact=self.artifact,
                bundle=self.bundle,
                certificate_identity=IDENTITY,
            )

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_wrong_cosign_identity_before_execution(self, run) -> None:
        with self.assertRaisesRegex(SigstoreVerifierError, "SHA-256 does not match"):
            verify_sigstore_bundle(
                cosign=self.cosign,
                expected_cosign_sha256="0" * 64,
                artifact=self.artifact,
                bundle=self.bundle,
                certificate_identity=IDENTITY,
            )
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_unexpected_oidc_issuer_before_execution(self, run) -> None:
        with self.assertRaisesRegex(SigstoreVerifierError, "unexpected certificate OIDC issuer"):
            verify_sigstore_bundle(
                cosign=self.cosign,
                expected_cosign_sha256=self.cosign_sha,
                artifact=self.artifact,
                bundle=self.bundle,
                certificate_identity=IDENTITY,
                oidc_issuer="https://example.invalid",
            )
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_multiple_tlog_entries(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        self.bundle.write_text(json.dumps(bundle_fixture(entries=2)), encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "exactly one transparency-log entry"):
            verify_sigstore_bundle(
                cosign=self.cosign,
                expected_cosign_sha256=self.cosign_sha,
                artifact=self.artifact,
                bundle=self.bundle,
                certificate_identity=IDENTITY,
            )

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_missing_inclusion_material(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        self.bundle.write_text(json.dumps(bundle_fixture(inclusion=False)), encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "neither inclusion proof nor inclusion promise"):
            verify_sigstore_bundle(
                cosign=self.cosign,
                expected_cosign_sha256=self.cosign_sha,
                artifact=self.artifact,
                bundle=self.bundle,
                certificate_identity=IDENTITY,
            )

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_retention_safe_evidence_cannot_promote_state(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        context = verify_sigstore_bundle(
            cosign=self.cosign,
            expected_cosign_sha256=self.cosign_sha,
            artifact=self.artifact,
            bundle=self.bundle,
            certificate_identity=IDENTITY,
        )
        evidence = retention_safe_evidence(context, cosign_sha256=self.cosign_sha)
        self.assertTrue(evidence["sigstore_crypto_verified"])
        self.assertFalse(evidence["external_write_performed_by_verifier"])
        self.assertFalse(evidence["oidc_token_requested_by_verifier"])
        self.assertFalse(evidence["real_external_retention_established"])
        self.assertFalse(evidence["temporal_order_verified"])
        self.assertFalse(evidence["freeze_established"])
        self.assertFalse(evidence["pilot_authorized"])
        self.assertEqual(evidence["empirical_n"], 0)


if __name__ == "__main__":
    unittest.main()
