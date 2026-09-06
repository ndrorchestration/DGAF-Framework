from __future__ import annotations

import copy
import unittest

from main_push_provenance_audit import (
    ProvenanceAuditError,
    classify_associated_pulls,
)


HEAD = "a" * 40
OTHER = "b" * 40


def merged_pull(
    *,
    number: int = 339,
    merge_commit_sha: str = HEAD,
    base_ref: str = "main",
) -> dict:
    return {
        "number": number,
        "state": "closed",
        "merged_at": "2026-09-06T18:00:00Z",
        "merge_commit_sha": merge_commit_sha,
        "html_url": f"https://github.com/ndrorchestration/DGAF-Framework/pull/{number}",
        "base": {"ref": base_ref},
    }


class MainPushProvenanceAuditTests(unittest.TestCase):
    def test_accepts_exactly_one_merged_pr_to_main(self) -> None:
        result = classify_associated_pulls(HEAD, [merged_pull()])
        self.assertEqual(result["main_push_provenance_audit"], "PASS_MERGED_PR_ASSOCIATION")
        self.assertEqual(result["head_sha"], HEAD)
        self.assertEqual(result["pull_request_number"], 339)
        self.assertFalse(result["preventive_enforcement_established"])
        self.assertTrue(result["detective_control_only"])

    def test_rejects_no_associated_pr(self) -> None:
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [])

    def test_rejects_open_pr_even_when_head_matches(self) -> None:
        pull = merged_pull()
        pull["state"] = "open"
        pull["merged_at"] = None
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [pull])

    def test_rejects_closed_unmerged_pr(self) -> None:
        pull = merged_pull()
        pull["merged_at"] = None
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [pull])

    def test_rejects_pr_merged_to_other_base(self) -> None:
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [merged_pull(base_ref="release")])

    def test_rejects_associated_pr_when_merge_commit_differs(self) -> None:
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [merged_pull(merge_commit_sha=OTHER)])

    def test_rejects_multiple_exact_merge_associations(self) -> None:
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(
                HEAD,
                [merged_pull(number=339), merged_pull(number=340)],
            )

    def test_ignores_unrelated_association_when_one_exact_merge_exists(self) -> None:
        unrelated = merged_pull(number=1, merge_commit_sha=OTHER)
        result = classify_associated_pulls(HEAD, [unrelated, merged_pull()])
        self.assertEqual(result["pull_request_number"], 339)

    def test_does_not_mutate_provider_payload(self) -> None:
        pulls = [merged_pull()]
        original = copy.deepcopy(pulls)
        classify_associated_pulls(HEAD, pulls)
        self.assertEqual(pulls, original)

    def test_rejects_malformed_head_sha(self) -> None:
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls("not-a-sha", [merged_pull()])

    def test_rejects_boolean_pr_number(self) -> None:
        pull = merged_pull()
        pull["number"] = True
        with self.assertRaises(ProvenanceAuditError):
            classify_associated_pulls(HEAD, [pull])


if __name__ == "__main__":
    unittest.main()
