from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import mode_t_sigstore_verifier as verifier_module
from mode_t_retention_contract import (
    EXPECTED_GITHUB_WORKFLOW_REF,
    EXPECTED_GITHUB_WORKFLOW_REPOSITORY,
    EXPECTED_OIDC_ISSUER,
    TransparencyExpectation,
)
from mode_t_sigstore_verifier import (
    EXPECTED_COSIGN_LINUX_AMD64_SHA256,
    EXPECTED_COSIGN_VERSION,
    SigstoreVerifierError,
    retention_safe_evidence,
    verify_retention_record_with_sigstore,
)

IDENTITY = "https://github.com/ndrorchestration/DGAF-Framework/.github/workflows/p4-mode-t-transparency.yml@refs/heads/main"
WORKFLOW_SHA = "a" * 40


def bundle_fixture(*, entries: int = 1, inclusion: bool = True,
                   media_type: str = "application/vnd.dev.sigstore.bundle.v0.3+json",
                   log_index: int | str = "310",
                   integrated_time: int | str = "1800000000") -> dict:
    item = {"logIndex": log_index, "integratedTime": integrated_time,
            "logId": {"keyId": "synthetic-log-key-id"}}
    if inclusion:
        item["inclusionProof"] = {"checkpoint": "synthetic"}
    return {"mediaType": media_type,
            "verificationMaterial": {"tlogEntries": [dict(item) for _ in range(entries)]}}


class ModeTSigstoreVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.cosign = root / "cosign"
        self.artifact = root / "record.json"
        self.bundle = root / "bundle.json"
        self.trusted_root = root / "trusted-root.json"
        self.cosign.write_bytes(b"not-the-reviewed-cosign-binary")
        self.artifact.write_bytes(b'{"record":"synthetic"}\n')
        self.bundle.write_text(json.dumps(bundle_fixture()), encoding="utf-8")
        self.trusted_root.write_text(
            json.dumps({"mediaType": "synthetic-trusted-root-fixture", "roots": []}),
            encoding="utf-8",
        )
        self.trusted_root_sha = hashlib.sha256(self.trusted_root.read_bytes()).hexdigest()
        self.expectation = TransparencyExpectation(
            record_type="PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION",
            record_sha256=hashlib.sha256(self.artifact.read_bytes()).hexdigest(),
            certificate_identity=IDENTITY,
            github_workflow_sha=WORKFLOW_SHA,
            trusted_root_sha256=self.trusted_root_sha,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _verify(self):
        return verify_retention_record_with_sigstore(
            expectation=self.expectation, cosign=self.cosign,
            artifact=self.artifact, bundle=self.bundle,
            trusted_root=self.trusted_root,
        )

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_verified_bundle_flows_into_retention_contract_without_promotion(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        verified = self._verify()
        result = verified.retention_result
        self.assertEqual(result["retention_contract"], "PASS_NORMALIZED_INCLUSION_ONLY")
        self.assertEqual(result["log_id_key_id"], "synthetic-log-key-id")
        self.assertEqual(result["github_workflow_sha"], WORKFLOW_SHA)
        self.assertEqual(result["trusted_root_sha256"], self.trusted_root_sha)
        self.assertTrue(result["trusted_root_explicit_and_digest_bound"])
        self.assertFalse(result["trusted_root_independently_approved"])
        self.assertFalse(result["real_external_retention_established"])
        self.assertFalse(result["temporal_order_verified"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)
        self.assertEqual(verified.cosign_version, EXPECTED_COSIGN_VERSION)
        self.assertEqual(verified.cosign_sha256, EXPECTED_COSIGN_LINUX_AMD64_SHA256)
        self.assertEqual(verified.trusted_root_sha256, self.trusted_root_sha)
        args = run.call_args.args[0]
        self.assertEqual(args[1], "verify-blob")
        self.assertIn("--trusted-root", args)
        self.assertIn(str(self.trusted_root), args)
        self.assertIn("--certificate-identity", args)
        self.assertIn(IDENTITY, args)
        self.assertIn("--certificate-oidc-issuer", args)
        self.assertIn(EXPECTED_OIDC_ISSUER, args)
        self.assertIn("--certificate-github-workflow-sha", args)
        self.assertIn(WORKFLOW_SHA, args)
        self.assertNotIn("sign-blob", args)

    def test_public_api_has_no_normalize_without_crypto_entry(self) -> None:
        self.assertFalse(hasattr(verifier_module, "normalize_verified_bundle"))
        signature = inspect.signature(verify_retention_record_with_sigstore)
        self.assertIn("trusted_root", signature.parameters)
        self.assertNotIn("expected_cosign_sha256", signature.parameters)
        self.assertNotIn("oidc_issuer", signature.parameters)
        self.assertNotIn("github_workflow_sha", signature.parameters)
        self.assertEqual(tuple(inspect.signature(retention_safe_evidence).parameters), ("verified",))

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_cosign_failure(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 1, stdout="", stderr="reject")
        with self.assertRaisesRegex(SigstoreVerifierError, "rejected artifact/bundle"):
            self._verify()

    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_wrong_cosign_identity_before_execution(self, run) -> None:
        with self.assertRaisesRegex(SigstoreVerifierError, "pinned v3.1.3"):
            self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_trusted_root_tamper_before_execution(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        self.trusted_root.write_text('{"tampered":true}', encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "TrustedRoot SHA-256"):
            self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_missing_trusted_root_before_execution(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        self.trusted_root.unlink()
        with self.assertRaisesRegex(SigstoreVerifierError, "Sigstore TrustedRoot missing"):
            self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_invalid_json_trusted_root_before_execution(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        self.trusted_root.write_text("not-json", encoding="utf-8")
        bad_sha = hashlib.sha256(self.trusted_root.read_bytes()).hexdigest()
        self.expectation = TransparencyExpectation(
            record_type=self.expectation.record_type,
            record_sha256=self.expectation.record_sha256,
            certificate_identity=IDENTITY,
            github_workflow_sha=WORKFLOW_SHA,
            trusted_root_sha256=bad_sha,
        )
        with self.assertRaisesRegex(SigstoreVerifierError, "not valid UTF-8 JSON"):
            self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_unexpected_oidc_issuer_expectation_before_execution(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        self.expectation = TransparencyExpectation(
            record_type=self.expectation.record_type,
            record_sha256=self.expectation.record_sha256,
            certificate_identity=IDENTITY,
            github_workflow_sha=WORKFLOW_SHA,
            trusted_root_sha256=self.trusted_root_sha,
            oidc_issuer="https://example.invalid",
        )
        with self.assertRaisesRegex(SigstoreVerifierError, "unexpected certificate OIDC issuer"):
            self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_unexpected_workflow_repository_or_ref_before_execution(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        for repository, ref, expected in (("example/other", EXPECTED_GITHUB_WORKFLOW_REF, "repository"),
                                          (EXPECTED_GITHUB_WORKFLOW_REPOSITORY, "refs/heads/other", "ref")):
            with self.subTest(repository=repository, ref=ref):
                self.expectation = TransparencyExpectation(
                    record_type=self.expectation.record_type,
                    record_sha256=self.expectation.record_sha256,
                    certificate_identity=IDENTITY,
                    github_workflow_sha=WORKFLOW_SHA,
                    trusted_root_sha256=self.trusted_root_sha,
                    github_workflow_repository=repository,
                    github_workflow_ref=ref,
                )
                with self.assertRaisesRegex(SigstoreVerifierError, expected):
                    self._verify()
        run.assert_not_called()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_multiple_tlog_entries(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        self.bundle.write_text(json.dumps(bundle_fixture(entries=2)), encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "exactly one transparency-log entry"):
            self._verify()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_promise_only_or_missing_inclusion_proof(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        fixture = bundle_fixture(inclusion=False)
        fixture["verificationMaterial"]["tlogEntries"][0]["inclusionPromise"] = {"signedEntryTimestamp": "synthetic"}
        self.bundle.write_text(json.dumps(fixture), encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "requires a transparency-log inclusion proof"):
            self._verify()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_legacy_or_old_standardized_bundle_media_types(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        for media_type in ("application/vnd.dev.cosign.simplesigning.v1+json",
                           "application/vnd.dev.sigstore.bundle+json;version=0.1",
                           "application/vnd.dev.sigstore.bundle+json;version=0.2", ""):
            with self.subTest(media_type=media_type):
                self.bundle.write_text(json.dumps(bundle_fixture(media_type=media_type)), encoding="utf-8")
                with self.assertRaisesRegex(SigstoreVerifierError, "standardized v0.3"):
                    self._verify()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_accepts_protobuf_json_uint64_strings_and_integer_form(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        for log_index, integrated_time in (("310", "1800000000"), (310, 1_800_000_000)):
            self.bundle.write_text(json.dumps(bundle_fixture(log_index=log_index, integrated_time=integrated_time)), encoding="utf-8")
            verified = self._verify()
            self.assertEqual(verified.transparency.log_index, 310)
            self.assertEqual(verified.transparency.integrated_time_unix, 1_800_000_000)

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_noncanonical_uint64_encodings(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        for invalid in (True, -1, "-1", "+1", "01", " 1", "1 ", "1.0", None):
            self.bundle.write_text(json.dumps(bundle_fixture(log_index=invalid)), encoding="utf-8")
            with self.assertRaisesRegex(SigstoreVerifierError, "canonical non-negative integer"):
                self._verify()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_rejects_missing_transparency_log_key_identity(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        fixture = bundle_fixture()
        fixture["verificationMaterial"]["tlogEntries"][0]["logId"] = {}
        self.bundle.write_text(json.dumps(fixture), encoding="utf-8")
        with self.assertRaisesRegex(SigstoreVerifierError, "log key identity"):
            self._verify()

    @patch("mode_t_sigstore_verifier._verify_cosign_binary")
    @patch("mode_t_sigstore_verifier.subprocess.run")
    def test_retention_safe_evidence_cannot_promote_state(self, run, verify_binary) -> None:
        verify_binary.return_value = EXPECTED_COSIGN_LINUX_AMD64_SHA256
        run.return_value = subprocess.CompletedProcess([], 0, stdout="Verified OK", stderr="")
        evidence = retention_safe_evidence(self._verify())
        self.assertTrue(evidence["sigstore_crypto_verified"])
        self.assertEqual(evidence["trusted_root_sha256"], self.trusted_root_sha)
        self.assertTrue(evidence["trusted_root_explicit_and_digest_bound"])
        self.assertFalse(evidence["trusted_root_independently_approved"])
        self.assertFalse(evidence["external_write_performed_by_verifier"])
        self.assertFalse(evidence["real_external_retention_established"])
        self.assertFalse(evidence["temporal_order_verified"])
        self.assertFalse(evidence["freeze_established"])
        self.assertFalse(evidence["pilot_authorized"])
        self.assertEqual(evidence["empirical_n"], 0)


if __name__ == "__main__":
    unittest.main()
