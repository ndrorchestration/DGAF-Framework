"""Deterministic, non-empirical oracle-score and contamination lineage tests."""

import unittest
from dataclasses import replace

from scripts.triadic_commit_model import Proposal, SyntheticController
from scripts import triadic_oracle_scoring as oracle


class OracleScoringTests(unittest.TestCase):
    def setUp(self):
        self.known = oracle.OracleCase("C02", "2+2=4")
        self.injected = oracle.OracleCase("C10", "2+2=4", frozenset({"bad-arithmetic"}), frozenset({"injected"}))
        self.oracle = oracle.FrozenOracle((self.known, self.injected))
        self.proposal = Proposal("op1", "2+2=4", "evidence-v1", "policy-v1", 0, 0, True, False, 10)

    def observe(self, case_id, proposal=None, trace=(), claimed=None):
        candidate = proposal if proposal is not None else self.proposal
        controller = SyntheticController("evidence-v1", "policy-v1")
        receipt = controller.commit(candidate, 1)
        return oracle.Observation(
            case_id, candidate.candidate, receipt.outcome, controller.snapshot()[2], trace, claimed
        )

    def trace(self):
        return (
            oracle.TraceEvent("injected", "fixture", ("bad-arithmetic",), "ASSERT"),
            oracle.TraceEvent("critic", "Critic", ("bad-arithmetic",), "CHALLENGE", ("injected",)),
            oracle.TraceEvent("relay", "Generator", ("bad-arithmetic",), "ASSERT", ("injected",)),
            oracle.TraceEvent("repeat", "Governor", ("bad-arithmetic",), "ASSERT", ("relay",)),
        )

    def test_correct_committed_answer_is_true_under_external_key(self):
        score = self.oracle.score(self.observe("C02"))
        self.assertTrue(score.committed)
        self.assertTrue(score.oracle_correct)
        self.assertFalse(score.false_promotion)

    def test_oracle_false_but_eligible_is_scored_false_promotion(self):
        false = replace(self.proposal, candidate="2+2=5")
        score = self.oracle.score(self.observe("C02", false, claimed=True))
        self.assertTrue(score.committed)
        self.assertFalse(score.oracle_correct)
        self.assertTrue(score.false_promotion)

    def test_three_roles_agree_on_false_answer_but_oracle_rejects_truth_claim(self):
        trace = (
            oracle.TraceEvent("g", "Generator", ("claim-false",), "ASSERT"),
            oracle.TraceEvent("c", "Critic", ("claim-false",), "ASSERT"),
            oracle.TraceEvent("v", "Governor", ("claim-false",), "ASSERT"),
        )
        proposal = replace(self.proposal, candidate="2+2=5")
        score = self.oracle.score(self.observe("C02", proposal, trace, claimed=True))
        self.assertTrue(score.false_promotion)
        self.assertFalse(score.oracle_correct)
        self.assertEqual(score.propagated_assertion_ids, ())

    def test_agent_claimed_correctness_cannot_change_oracle_score(self):
        obs = self.observe("C02", replace(self.proposal, candidate="2+2=5"), claimed=True)
        self.assertEqual(self.oracle.score(obs), self.oracle.score(replace(obs, agent_claimed_correct=False)))
        self.assertEqual(self.oracle.score(obs), self.oracle.score(replace(obs, agent_claimed_correct=None)))

    def test_false_candidate_on_hold_is_not_a_false_promotion(self):
        proposal = replace(self.proposal, candidate="2+2=5", checks_pass=False)
        score = self.oracle.score(self.observe("C02", proposal))
        self.assertFalse(score.committed)
        self.assertIsNone(score.oracle_correct)
        self.assertFalse(score.false_promotion)

    def test_injection_propagates_over_transitive_lineage(self):
        score = self.oracle.score(self.observe("C10", trace=self.trace()))
        self.assertEqual(score.propagated_assertion_ids, ("relay", "repeat"))
        self.assertEqual(score.challenged_claim_event_ids, ("critic",))
        self.assertEqual(score.unsupported_assertion_ids, ("relay", "repeat"))
        self.assertEqual(score.tainted_lineage_ids, ("injected", "critic", "relay", "repeat"))

    def test_unverified_assertion_without_known_parent_is_not_proven_propagation(self):
        trace = self.trace() + (oracle.TraceEvent("unknown-source", "Governor", ("bad-arithmetic",), "ASSERT"),)
        score = self.oracle.score(self.observe("C10", trace=trace))
        self.assertEqual(score.unattributed_assertion_ids, ("unknown-source",))
        self.assertNotIn("unknown-source", score.propagated_assertion_ids)

    def test_critic_challenge_does_not_count_as_adoption(self):
        score = self.oracle.score(self.observe("C10", trace=self.trace()[:2]))
        self.assertEqual(score.propagated_assertion_ids, ())
        self.assertEqual(score.challenged_claim_event_ids, ("critic",))

    def test_contamination_and_false_promotion_are_distinct_measures(self):
        false = replace(self.proposal, candidate="2+2=5")
        score = self.oracle.score(self.observe("C10", false, self.trace()))
        self.assertTrue(score.false_promotion)
        self.assertEqual(len(score.propagated_assertion_ids), 2)
        correct = self.oracle.score(self.observe("C10", trace=self.trace()))
        self.assertFalse(correct.false_promotion)
        self.assertEqual(len(correct.propagated_assertion_ids), 2)

    def test_unknown_fixture_and_duplicate_fixture_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_CASE"):
            self.oracle.score(self.observe("wrong"))
        with self.assertRaisesRegex(ValueError, "DUPLICATE_CASE"):
            oracle.FrozenOracle((self.known, self.known))
        with self.assertRaisesRegex(ValueError, "EMPTY_ORACLE"):
            oracle.FrozenOracle(())

    def test_missing_injection_and_spoofed_injection_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "MISSING_INJECTION_ROOT"):
            self.oracle.score(self.observe("C10"))
        forged = (oracle.TraceEvent("injected", "Governor", ("bad-arithmetic",), "ASSERT"),)
        with self.assertRaisesRegex(ValueError, "INVALID_INJECTION_ROOT"):
            self.oracle.score(self.observe("C10", trace=forged))

    def test_duplicate_ids_and_forward_parents_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_EVENT"):
            self.oracle.score(self.observe("C10", trace=self.trace() + (self.trace()[2],)))
        bad = (
            oracle.TraceEvent("injected", "fixture", ("bad-arithmetic",), "ASSERT"),
            oracle.TraceEvent("relay", "Governor", ("bad-arithmetic",), "ASSERT", ("future",)),
        )
        with self.assertRaisesRegex(ValueError, "UNKNOWN_OR_FORWARD_PARENT"):
            self.oracle.score(self.observe("C10", trace=bad))

    def test_unknown_stance_and_bad_claim_data_are_rejected(self):
        bad = (
            oracle.TraceEvent("injected", "fixture", ("bad-arithmetic",), "ASSERT"),
            oracle.TraceEvent("relay", "Governor", ("bad-arithmetic",), "ENDORSE", ("injected",)),
        )
        with self.assertRaisesRegex(ValueError, "MALFORMED_TRACE"):
            self.oracle.score(self.observe("C10", trace=bad))
        duplicate_claim = (oracle.TraceEvent("injected", "fixture", ("bad-arithmetic", "bad-arithmetic"), "ASSERT"),)
        with self.assertRaisesRegex(ValueError, "DUPLICATE_TRACE_REFERENCE"):
            self.oracle.score(self.observe("C10", trace=duplicate_claim))

    def test_inconsistent_receipt_and_accepted_snapshot_are_rejected(self):
        obs = self.observe("C02")
        with self.assertRaisesRegex(ValueError, "INCONSISTENT_COMMIT"):
            self.oracle.score(replace(obs, accepted_candidate="2+2=5"))
        with self.assertRaisesRegex(ValueError, "INCONSISTENT_HOLD"):
            self.oracle.score(replace(obs, receipt_outcome="HOLD"))

    def test_malformed_oracle_case_is_not_silently_used(self):
        with self.assertRaisesRegex(ValueError, "MALFORMED_ORACLE"):
            oracle.FrozenOracle((oracle.OracleCase("C10", "2+2=4", frozenset(), frozenset({"injected"})),))
        with self.assertRaisesRegex(ValueError, "MALFORMED_OBSERVATION"):
            self.oracle.score(replace(self.observe("C02"), agent_claimed_correct="yes"))


if __name__ == "__main__":
    unittest.main()
