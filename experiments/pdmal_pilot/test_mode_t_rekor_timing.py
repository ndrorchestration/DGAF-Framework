from __future__ import annotations

import unittest

from experiments.pdmal_pilot.mode_t_rekor_timing import (
    EVIDENCE_CLASS,
    RekorTimingError,
    build_synthetic_blob,
    extract_tlog_evidence,
)


class RekorTimingTests(unittest.TestCase):
    def test_build_blob_is_non_authorizing(self) -> None:
        blob = build_synthetic_blob(
            evidence_sha="a" * 40,
            run_id="123",
            run_attempt="1",
            workflow_ref="ndrorchestration/DGAF-Framework/.github/workflows/p4-mode-t-rekor-timing.yml@refs/heads/design/test",
        ).decode("utf-8")
        self.assertIn(EVIDENCE_CLASS, blob)
        self.assertIn('"empirical_data_collection":false', blob)
        self.assertIn('"pilot_authorized":false', blob)
        self.assertIn('"authorization_consumed":false', blob)
        self.assertIn('"numeric_w_selected":false', blob)
        self.assertIn('"empirical_n":0', blob)

    def test_rejects_retried_workflow_attempt(self) -> None:
        with self.assertRaises(RekorTimingError):
            build_synthetic_blob(
                evidence_sha="a" * 40,
                run_id="123",
                run_attempt="2",
                workflow_ref="ndrorchestration/DGAF-Framework/.github/workflows/p4-mode-t-rekor-timing.yml@refs/heads/design/test",
            )

    def test_extracts_transparency_evidence(self) -> None:
        bundle = {
            "verificationMaterial": {
                "tlogEntries": [
                    {
                        "integratedTime": "1788650000",
                        "logIndex": "42",
                        "logId": {"keyId": "abcd"},
                        "inclusionProof": {"checkpoint": {"envelope": "example"}},
                    }
                ]
            }
        }
        result = extract_tlog_evidence(bundle)
        self.assertEqual(result["integrated_time"], 1788650000)
        self.assertEqual(result["log_index"], 42)
        self.assertEqual(result["log_id"], "abcd")
        self.assertTrue(result["has_inclusion_proof"])

    def test_rejects_bundle_without_tlog_entry(self) -> None:
        with self.assertRaises(RekorTimingError):
            extract_tlog_evidence({"verificationMaterial": {"tlogEntries": []}})

    def test_rejects_entry_without_inclusion_material(self) -> None:
        bundle = {
            "verificationMaterial": {
                "tlogEntries": [
                    {"integratedTime": 1788650000, "logIndex": 42, "logId": {"keyId": "abcd"}}
                ]
            }
        }
        with self.assertRaises(RekorTimingError):
            extract_tlog_evidence(bundle)


if __name__ == "__main__":
    unittest.main()
