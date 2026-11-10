"""Bounded control tests; no scientific samples or real authority."""

import importlib.util
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier

SPEC = importlib.util.spec_from_file_location(
    "triadic_commit_model", Path(__file__).resolve().parents[1] / "scripts/triadic_commit_model.py"
)
MODEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODEL
SPEC.loader.exec_module(MODEL)


class CommitBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.controller = MODEL.SyntheticController("evidence-v1", "policy-v1")
        self.proposal = MODEL.Proposal("op1", "candidate", "evidence-v1", "policy-v1", 0, 0, True, False, 10)

    def test_valid_commit_and_ack_loss_replay(self):
        first = self.controller.commit(self.proposal, 1)
        self.assertEqual(first.outcome, "COMMITTED_SYNTHETIC")
        self.controller.revoke()
        self.assertEqual(self.controller.commit(self.proposal, 20), first)
        self.assertEqual(self.controller.snapshot(), (1, 0, "candidate"))

    def test_changed_payload_cannot_reuse_identifier(self):
        self.controller.commit(self.proposal, 1)
        result = self.controller.commit(replace(self.proposal, candidate="other"), 2)
        self.assertEqual(result.reason, "ID_CONFLICT")
        self.assertEqual(self.controller.snapshot(), (1, 0, "candidate"))

    def test_revocation_between_review_and_commit(self):
        self.controller.revoke()
        self.assertEqual(self.controller.commit(self.proposal, 1).reason, "REVOKED")
        self.assertEqual(self.controller.snapshot(), (0, 0, None))

    def test_stale_epoch_cannot_commit(self):
        self.controller.invalidate_epoch()
        self.assertEqual(self.controller.commit(self.proposal, 1).reason, "STALE_EPOCH")
        self.assertEqual(self.controller.snapshot(), (0, 1, None))

    def test_concurrent_candidates_have_one_winner(self):
        barrier = Barrier(2)
        def attempt(operation):
            barrier.wait()
            return self.controller.commit(replace(self.proposal, operation=operation), 1)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, ["first", "second"]))
        self.assertEqual(sorted(r.reason for r in results), ["ELIGIBLE", "STALE_PREDECESSOR"])
        self.assertEqual(self.controller.snapshot()[0], 1)

    def test_required_checks_objections_and_timeout(self):
        for change in ({"checks_pass": False}, {"objection": True}, {"deadline": 1}):
            with self.subTest(change=change):
                controller = MODEL.SyntheticController("evidence-v1", "policy-v1")
                self.assertEqual(controller.commit(replace(self.proposal, **change), 1).outcome, "HOLD")
                self.assertEqual(controller.snapshot(), (0, 0, None))

    def test_malformed_or_wrong_identity_is_rejected(self):
        for change in ({"evidence": "wrong"}, {"policy": "wrong"}, {"candidate": ""},
                       {"epoch": True}, {"checks_pass": 1}, {"deadline": float("nan")}):
            with self.subTest(change=change):
                controller = MODEL.SyntheticController("evidence-v1", "policy-v1")
                self.assertEqual(controller.commit(replace(self.proposal, **change), 1).outcome, "HOLD")
                self.assertEqual(controller.snapshot(), (0, 0, None))
        self.assertEqual(self.controller.commit(None, 1).reason, "MALFORMED")

    def test_denial_is_retained_for_operation_id(self):
        denied = self.controller.commit(replace(self.proposal, objection=True), 1)
        self.assertEqual(denied.outcome, "HOLD")
        self.assertEqual(self.controller.commit(self.proposal, 2).reason, "ID_CONFLICT")

    def test_policy_eligibility_does_not_establish_truth(self):
        # Deliberately wrong oracle answer: the model has no semantic verifier.
        proposal = replace(self.proposal, candidate="2+2=5")
        self.assertEqual(self.controller.commit(proposal, 1).outcome, "COMMITTED_SYNTHETIC")
        self.assertNotEqual(self.controller.snapshot()[2], "2+2=4")


if __name__ == "__main__":
    unittest.main()
