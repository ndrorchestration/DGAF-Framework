import unittest
from datetime import timedelta

from test_containment_assessment import NOW, contract_fixture, observation_fixture

from scripts.dgaf_capability_pep import (
    ApprovalState,
    EnforcementContext,
    EnforcementRefusal,
    VerificationState,
    governed_dispatch,
)
from scripts.dgaf_capability_policy import Authority
from scripts.dgaf_containment_assessment import AssessmentInputError, assess


class FollowOnTests(unittest.TestCase):
    def test_all_dispositions_are_non_authorizing(self):
        for state in ("ESTABLISHED", "UNKNOWN", "CONTRADICTED"):
            with self.subTest(state=state):
                observation = observation_fixture()
                observation["predicate_results"]["workers_covered"] = state
                result = assess(contract_fixture(), observation, now=NOW)
                for field in (
                    "authority_effect",
                    "follow_on_authority",
                    "execution_permitted",
                    "scientific_n_increment",
                ):
                    self.assertIn(field, result)
                self.assertEqual(result["authority_effect"], "NONE")
                self.assertEqual(result["follow_on_authority"], "FRESH_ADJUDICATION_REQUIRED")
                self.assertIs(result["execution_permitted"], False)
                self.assertEqual(result["scientific_n_increment"], 0)

    def test_SC28_supplied_receipt_cannot_authorize_follow_on_dispatch(self):
        authority = Authority(frozenset({"synthetic.restrict"}), frozenset({"synthetic-session"}))
        context = EnforcementContext(
            capability="synthetic.restrict",
            resource="synthetic-session",
            protected_side_effect=True,
            requester_authority=authority,
            delegation_authority=authority,
            executor_authority=authority,
            policy_authority=authority,
            authorization_status="ACTIVE",
            authorization_not_before=NOW - timedelta(seconds=1),
            authorization_expires_at=NOW + timedelta(seconds=60),
            commit_digest="synthetic-digest",
            approval=ApprovalState("requester", "approver", "synthetic-digest"),
            verification=VerificationState(required=True, passed=True),
            required_state_guards={},
            observed_state_guards={},
            now=NOW,
            prior_execution_receipt={"follow_on_authority": "FRESH_ADJUDICATION_REQUIRED"},
            fresh_adjudication_complete=False,
        )
        dispatched = []
        with self.assertRaisesRegex(EnforcementRefusal, "fresh adjudication"):
            governed_dispatch({}, context, dispatcher=lambda req: dispatched.append(req) or {})
        self.assertEqual(dispatched, [])

    def test_observation_cannot_assert_permission(self):
        with self.assertRaises(AssessmentInputError):
            assess(contract_fixture(), {**observation_fixture(), "execution_permitted": True}, now=NOW)
