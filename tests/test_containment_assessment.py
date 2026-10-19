import copy
import unittest
from datetime import datetime, timezone

from scripts.dgaf_containment_assessment import (
    AssessmentInputError,
    assess,
    contract_digest,
)


def contract_fixture():
    return {
        "schema_version": "SYNTHETIC_CONTAINMENT_CONTRACT_V1",
        "contract_id": "synthetic-containment-v1",
        "definition_version": "1",
        "subject_id": "synthetic-agent",
        "session_id": "synthetic-session",
        "environment_id": "synthetic-environment",
        "required_predicates": [
            "capabilities_restricted",
            "workers_covered",
            "pending_actions_contained",
            "egress_covered",
            "persistence_contained",
        ],
        "max_age_seconds": 30,
    }


class ContractTests(unittest.TestCase):
    def test_digest_is_bound_and_key_order_independent(self):
        value = contract_fixture()
        digest = contract_digest(value)
        self.assertIsInstance(digest, str)
        self.assertRegex(digest, r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(digest, contract_digest(dict(reversed(list(value.items())))))

    def test_changed_definition_changes_digest(self):
        value = contract_fixture()
        changed = {**value, "definition_version": "2"}
        self.assertNotEqual(contract_digest(value), contract_digest(changed))

    def test_rejects_bad_contracts(self):
        mutations = [
            ("missing", lambda c: c.pop("subject_id")),
            ("extra", lambda c: c.update(extra=True)),
            ("duplicate", lambda c: c.update(required_predicates=["a", "a"])),
            ("empty-name", lambda c: c.update(required_predicates=[""])),
            ("empty-predicates", lambda c: c.update(required_predicates=[])),
            ("bad-id", lambda c: c.update(contract_id=" ")),
            ("integer-version", lambda c: c.update(definition_version=1)),
            ("wrong-schema", lambda c: c.update(schema_version="OTHER")),
        ]
        for label, mutate in mutations:
            with self.subTest(label=label):
                value = copy.deepcopy(contract_fixture())
                mutate(value)
                with self.assertRaises(AssessmentInputError):
                    contract_digest(value)

    def test_rejects_invalid_age_limits(self):
        for value in (True, False, float("nan"), float("inf"), -float("inf"), 0, -1, "30", None):
            with self.subTest(value=repr(value)):
                with self.assertRaises(AssessmentInputError):
                    contract_digest({**contract_fixture(), "max_age_seconds": value})


NOW = datetime(2026, 10, 11, 8, tzinfo=timezone.utc)


def observation_fixture(contract=None):
    contract = contract or contract_fixture()
    return {
        "schema_version": "SYNTHETIC_CONTAINMENT_OBSERVATION_V1",
        "evidence_class": "SYNTHETIC",
        "subject_id": contract["subject_id"],
        "session_id": contract["session_id"],
        "environment_id": contract["environment_id"],
        "contract_digest": contract_digest(contract),
        "observed_at": "2026-10-11T07:59:50Z",
        "time_basis": "SNAPSHOT",
        "predicate_results": {p: "ESTABLISHED" for p in contract["required_predicates"]},
        "evidence_ids": ["synthetic:evidence-1"],
        "blocking_defeaters": [],
    }


class AssessmentTests(unittest.TestCase):
    def evaluate(self, observation=None, contract=None):
        contract = contract or contract_fixture()
        observation = observation if observation is not None else observation_fixture(contract)
        result = assess(contract, observation, now=NOW)
        self.assertIsInstance(result, dict, "assessment must return a linked record")
        return result

    def test_SC01_valid_bounded_snapshot(self):
        result = self.evaluate()
        self.assertEqual(result["disposition"], "ESTABLISHED_IN_SCOPE")
        self.assertEqual(result["evidence_class"], "SYNTHETIC")
        self.assertEqual(result["reasons"], [])
        self.assertEqual(result["time_basis"], "SNAPSHOT")
        self.assertEqual(result["assessed_at"], "2026-10-11T08:00:00Z")
        self.assertEqual(result["contract_digest"], contract_digest(contract_fixture()))

    def test_SC05_unknown_worker_coverage(self):
        observation = observation_fixture()
        observation["predicate_results"]["workers_covered"] = "UNKNOWN"
        result = self.evaluate(observation)
        self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
        self.assertIn("UNKNOWN:workers_covered", result["reasons"])
        self.assertEqual(result["predicate_results"], observation["predicate_results"])

    def test_SC13_stale_snapshot(self):
        observation = {**observation_fixture(), "observed_at": "2026-10-11T07:59:00Z"}
        result = self.evaluate(observation)
        self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
        self.assertIn("STALE", result["reasons"])

    def test_SC16_changed_definition(self):
        old_contract = contract_fixture()
        observation = observation_fixture(old_contract)
        result = self.evaluate(observation, {**old_contract, "definition_version": "2"})
        self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
        self.assertIn("CONTRACT_BINDING_MISMATCH", result["reasons"])

    def test_scope_mismatch_does_not_import_foreign_contradiction(self):
        for field in ("subject_id", "session_id", "environment_id"):
            with self.subTest(field=field):
                observation = observation_fixture()
                observation[field] = "different"
                observation["predicate_results"]["workers_covered"] = "CONTRADICTED"
                result = self.evaluate(observation)
                self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
                self.assertIn("SCOPE_MISMATCH:" + field, result["reasons"])

    def test_age_limit_is_inclusive(self):
        for stamp, expected in [
            ("2026-10-11T07:59:30Z", "ESTABLISHED_IN_SCOPE"),
            ("2026-10-11T07:59:29.999999Z", "NOT_ESTABLISHED"),
        ]:
            with self.subTest(stamp=stamp):
                result = self.evaluate({**observation_fixture(), "observed_at": stamp})
                self.assertEqual(result["disposition"], expected)

    def test_future_snapshot_not_established(self):
        result = self.evaluate({**observation_fixture(), "observed_at": "2026-10-11T08:00:01Z"})
        self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
        self.assertIn("FUTURE_SNAPSHOT", result["reasons"])

    def test_timestamp_offsets_normalized(self):
        result = self.evaluate({**observation_fixture(), "observed_at": "2026-10-11T03:59:50-04:00"})
        self.assertEqual(result["observed_at"], "2026-10-11T07:59:50Z")
        self.assertEqual(result["disposition"], "ESTABLISHED_IN_SCOPE")

    def test_rejects_bad_timestamps_and_clocks(self):
        for stamp in ("2026-10-11T07:59:50", "not-a-date", None, True):
            with self.subTest(stamp=stamp):
                with self.assertRaises(AssessmentInputError):
                    assess(contract_fixture(), {**observation_fixture(), "observed_at": stamp}, now=NOW)
        for clock in (datetime(2026, 10, 11, 8), None, "now"):
            with self.subTest(clock=repr(clock)):
                with self.assertRaises(AssessmentInputError):
                    assess(contract_fixture(), observation_fixture(), now=clock)

    def test_rejects_interval_and_wrong_evidence_class(self):
        for field, value in [("time_basis", "INTERVAL"), ("evidence_class", "LIVE"), ("schema_version", "OTHER")]:
            with self.subTest(field=field):
                with self.assertRaises(AssessmentInputError):
                    assess(contract_fixture(), {**observation_fixture(), field: value}, now=NOW)

    def test_rejects_missing_extra_and_invalid_predicates(self):
        observations = []
        value = observation_fixture()
        value["predicate_results"].pop("workers_covered")
        observations.append(value)
        value = observation_fixture()
        value["predicate_results"]["extra"] = "ESTABLISHED"
        observations.append(value)
        for state in (True, 1, None, "verified", ["UNKNOWN"]):
            value = observation_fixture()
            value["predicate_results"]["workers_covered"] = state
            observations.append(value)
        value = observation_fixture()
        value["predicate_results"] = []
        observations.append(value)
        for index, value in enumerate(observations):
            with self.subTest(index=index):
                with self.assertRaises(AssessmentInputError):
                    assess(contract_fixture(), value, now=NOW)

    def test_empty_evidence_blocks_establishment(self):
        result = self.evaluate({**observation_fixture(), "evidence_ids": []})
        self.assertEqual(result["disposition"], "NOT_ESTABLISHED")
        self.assertIn("NO_EVIDENCE", result["reasons"])

    def test_rejects_bad_lists_and_top_level_fields(self):
        for field in ("evidence_ids", "blocking_defeaters"):
            for value in (None, "one", [" "], ["same", "same"], [1]):
                with self.subTest(field=field, value=repr(value)):
                    with self.assertRaises(AssessmentInputError):
                        assess(contract_fixture(), {**observation_fixture(), field: value}, now=NOW)
        value = observation_fixture()
        value.pop("subject_id")
        with self.assertRaises(AssessmentInputError):
            assess(contract_fixture(), value, now=NOW)
        with self.assertRaises(AssessmentInputError):
            assess(contract_fixture(), {**observation_fixture(), "execution_permitted": True}, now=NOW)

    def test_rejects_malformed_contract_digest(self):
        for digest in ("", "v1", "sha256:" + "x" * 64, True):
            with self.subTest(digest=digest):
                with self.assertRaises(AssessmentInputError):
                    assess(contract_fixture(), {**observation_fixture(), "contract_digest": digest}, now=NOW)

    def test_contradiction_preserves_stale_and_unknown_reasons(self):
        value = observation_fixture()
        value["observed_at"] = "2026-10-11T07:59:00Z"
        value["predicate_results"]["egress_covered"] = "CONTRADICTED"
        value["predicate_results"]["workers_covered"] = "UNKNOWN"
        result = self.evaluate(value)
        self.assertEqual(result["disposition"], "CONTRADICTED_IN_SCOPE")
        for reason in ("CONTRADICTED:egress_covered", "UNKNOWN:workers_covered", "STALE"):
            self.assertIn(reason, result["reasons"])

    def test_blocking_defeater_is_retained(self):
        result = self.evaluate({**observation_fixture(), "blocking_defeaters": ["policy-revoked"]})
        self.assertEqual(result["disposition"], "CONTRADICTED_IN_SCOPE")
        self.assertIn("DEFEATER:policy-revoked", result["reasons"])

    def test_output_does_not_alias_input(self):
        value = observation_fixture()
        before = copy.deepcopy(value)
        result = self.evaluate(value)
        self.assertEqual(value, before)
        result["predicate_results"]["workers_covered"] = "UNKNOWN"
        result["evidence_ids"].append("synthetic:new")
        self.assertEqual(value, before)


class ReviewRegressionTests(unittest.TestCase):
    def test_rejects_ambiguous_timestamp_grammar_and_precision(self):
        for stamp in (
            "2026-10-11T08:59:50+00:60",
            "2026-10-11T08:00:00.0000001Z",
            "2026-10-11T07:59:50+24:00",
            "2026-10-11 07:59:50Z",
            "2026-10-11T07:59:50+00:00:00",
            "2026-02-30T07:59:50Z",
        ):
            with self.subTest(stamp=stamp), self.assertRaises(AssessmentInputError):
                assess(contract_fixture(), {**observation_fixture(), "observed_at": stamp}, now=NOW)

    def test_rejects_non_utf8_text_at_input_boundary(self):
        with self.assertRaises(AssessmentInputError):
            contract_digest({**contract_fixture(), "contract_id": "\ud800"})
        with self.assertRaises(AssessmentInputError):
            assess(contract_fixture(), {**observation_fixture(), "evidence_ids": ["\ud800"]}, now=NOW)
