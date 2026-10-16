import hashlib
import json
import unittest

from test_containment_assessment import NOW, contract_fixture, observation_fixture

from scripts.dgaf_containment_assessment import AssessmentInputError
from scripts.dgaf_containment_observation import assess_bound_snapshot


def digest(raw):
    return "sha256:" + hashlib.sha256(raw).hexdigest()


class ObservationIntakeTests(unittest.TestCase):
    def evaluate(self, raw, pin=None):
        return assess_bound_snapshot(contract_fixture(), raw, expected_observation_digest=pin, now=NOW)

    def test_valid_bound_snapshot_retains_non_authentication_and_non_authority(self):
        raw = json.dumps(observation_fixture()).encode()
        result = self.evaluate(raw, digest(raw))
        self.assertEqual(result["disposition"], "ESTABLISHED_IN_SCOPE")
        self.assertEqual(result["observation_digest"], digest(raw))
        self.assertEqual(result["integrity_binding"], "EXPECTED_DIGEST_MATCH")
        self.assertEqual(result["source_authenticity"], "NOT_ESTABLISHED")
        self.assertEqual(result["authority_effect"], "NONE")
        self.assertIs(result["execution_permitted"], False)

    def test_missing_malformed_and_wrong_pins_fail_closed(self):
        raw = json.dumps(observation_fixture()).encode()
        for pin in (None, "", True, "sha256:" + "a" * 64, digest(raw + b" ")):
            with self.subTest(pin=pin), self.assertRaises(AssessmentInputError):
                self.evaluate(raw, pin)

    def test_tampered_content_rejected_against_separate_pin(self):
        raw = json.dumps(observation_fixture()).encode()
        changed = raw.replace(b"ESTABLISHED", b"UNKNOWN")
        with self.assertRaises(AssessmentInputError):
            self.evaluate(changed, digest(raw))

    def test_rejects_ambiguous_and_malformed_json_even_with_matching_pin(self):
        for raw in (
            b'{"a":1,"a":2}',
            b'{"a":{"b":1,"b":2}}',
            b'{"a":NaN}',
            b'{"a":Infinity}',
            b"[]",
            b"null",
            b"{} trailing",
            b"\xff",
            b"\xef\xbb\xbf{}",
            b" " * 65537,
        ):
            with self.subTest(raw=raw[:80]), self.assertRaises(AssessmentInputError):
                self.evaluate(raw, digest(raw))

    def test_rejects_non_bytes(self):
        for raw in ("{}", None, {}, bytearray(b"{}")):
            with self.subTest(raw=raw), self.assertRaises(AssessmentInputError):
                self.evaluate(raw, "sha256:" + "a" * 64)

    def test_large_integer_parser_error_uses_assessment_input_boundary(self):
        raw = b'{"a":' + b"9" * 5000 + b"}"
        with self.assertRaises(AssessmentInputError):
            self.evaluate(raw, digest(raw))
