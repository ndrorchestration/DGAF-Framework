"""Negative controls for disposable fixture-key message admission, not real agents."""

import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier

from scripts import triadic_message_boundary as auth


class SignedMessageBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.keys = {"gen": b"g" * 32, "critic": b"c" * 32, "gov": b"v" * 32}
        self.roles = {"gen": "Generator", "critic": "Critic", "gov": "Governor"}
        self.candidate_digest = auth.digest_text("2+2=5")
        self.evidence_digest = auth.digest_text("fixture evidence v1")
        self.policy_digest = auth.digest_text("fixture policy v1")
        self.boundary = self.new_boundary()

    def new_boundary(self):
        return auth.SyntheticMessageBoundary(
            "run-001", self.roles, self.keys, self.candidate_digest, self.evidence_digest, self.policy_digest
        )

    def message(self, sender="gen", kind="CANDIDATE", **changes):
        msg = auth.SignedMessage(
            auth.VERSION, "run-001", "m1", sender, self.roles.get(sender, "Generator"),
            "controller", kind, 0, 0, 10, self.candidate_digest, self.evidence_digest,
            self.policy_digest, "fixture-message", auth.digest_text("fixture-message"),
        )
        return auth.sign_fixture(replace(msg, **changes), self.keys.get(sender, b"unknown-" * 4))

    def test_valid_generator_message(self):
        receipt = self.boundary.admit(self.message(), 1)
        self.assertEqual(receipt.outcome, "ADMITTED_SYNTHETIC")
        self.assertEqual(self.boundary.snapshot(), (0, 1, ("m1",)))

    def test_critic_and_governor_allowed_kinds(self):
        for sender, kind in (("critic", "ASSESSMENT"), ("critic", "OBJECTION"), ("gov", "RESOLUTION")):
            with self.subTest(sender=sender, kind=kind):
                boundary = self.new_boundary()
                self.assertEqual(boundary.admit(self.message(sender, kind), 1).outcome, "ADMITTED_SYNTHETIC")

    def test_role_cannot_request_disallowed_kind(self):
        self.assertEqual(self.boundary.admit(self.message("critic", "CANDIDATE"), 1).reason, "UNAUTHORIZED_KIND")
        self.assertEqual(self.boundary.snapshot()[1], 0)

    def test_role_spoof_even_with_sender_key(self):
        forged = self.message(sender="gen", sender_role="Critic", kind="ASSESSMENT")
        self.assertEqual(self.boundary.admit(forged, 1).reason, "ROLE_SPOOF")

    def test_wrong_mac_is_rejected_and_does_not_reserve_id(self):
        forged = replace(self.message(), mac="0" * 64)
        self.assertEqual(self.boundary.admit(forged, 1).reason, "INVALID_MAC")
        self.assertEqual(self.boundary.admit(self.message(), 1).outcome, "ADMITTED_SYNTHETIC")

    def test_content_tamper_after_signing_is_rejected(self):
        message = replace(self.message(), content="modified")
        self.assertEqual(self.boundary.admit(message, 1).reason, "INVALID_MAC")

    def test_signed_but_false_content_digest_is_rejected(self):
        message = self.message(content="modified")
        self.assertEqual(self.boundary.admit(message, 1).reason, "CONTENT_DIGEST_MISMATCH")

    def test_signed_wrong_run_does_not_reserve_current_run_id(self):
        self.assertEqual(self.boundary.admit(self.message(run_id="other"), 1).reason, "WRONG_RUN_OR_VERSION")
        self.assertEqual(self.boundary.admit(self.message(), 1).outcome, "ADMITTED_SYNTHETIC")

    def test_ledger_capacity_fails_closed_without_erasing_prior_receipts(self):
        boundary = auth.SyntheticMessageBoundary(
            "run-001", self.roles, self.keys,
            self.candidate_digest, self.evidence_digest, self.policy_digest,
            max_messages=1,
        )
        first = self.message(message_id="first")
        receipt = boundary.admit(first, 1)
        self.assertEqual(receipt.outcome, "ADMITTED_SYNTHETIC")
        self.assertEqual(boundary.admit(self.message(message_id="second"), 1).reason, "LEDGER_FULL")
        self.assertEqual(boundary.admit(first, 30), receipt)
        self.assertEqual(boundary.snapshot()[1], 1)

    def test_oversized_and_non_utf8_content_are_rejected(self):
        oversized_content = "X" * 4097
        oversized = self.message(content=oversized_content, content_digest=auth.digest_text(oversized_content))
        self.assertEqual(self.boundary.admit(oversized, 1).reason, "OVERSIZED_CONTENT")
        malformed = self.message(content="\\ud800")
        self.assertEqual(self.boundary.admit(malformed, 1).reason, "MALFORMED")

    def test_unknown_identity_cannot_reserve_message_id(self):
        forged = self.message(sender="intruder")
        self.assertEqual(self.boundary.admit(forged, 1).reason, "UNKNOWN_IDENTITY")
        self.assertEqual(self.boundary.admit(self.message(), 1).outcome, "ADMITTED_SYNTHETIC")

    def test_duplicate_replay_after_revocation_and_epoch_change(self):
        message = self.message()
        receipt = self.boundary.admit(message, 1)
        self.boundary.revoke_identity("gen")
        self.boundary.invalidate_epoch()
        self.assertEqual(self.boundary.admit(message, 20), receipt)
        self.assertEqual(self.boundary.snapshot(), (1, 1, ("m1",)))

    def test_signed_changed_payload_conflicts_with_existing_id(self):
        self.boundary.admit(self.message(), 1)
        other = self.message(content="different", content_digest=auth.digest_text("different"))
        self.assertEqual(self.boundary.admit(other, 2).reason, "ID_CONFLICT")
        self.assertEqual(self.boundary.snapshot()[1], 1)

    def test_revocation_blocks_new_signed_message(self):
        self.boundary.revoke_identity("gen")
        self.assertEqual(self.boundary.admit(self.message(message_id="m2"), 1).reason, "REVOKED")
        self.assertEqual(self.boundary.snapshot()[1], 0)

    def test_stale_epoch_is_rejected(self):
        self.boundary.invalidate_epoch()
        self.assertEqual(self.boundary.admit(self.message(), 1).reason, "STALE_EPOCH")

    def test_expiry_is_rejected_at_deadline(self):
        self.assertEqual(self.boundary.admit(self.message(), 10).reason, "EXPIRED")

    def test_wrong_run_or_contract_version_is_rejected(self):
        for change in ({"run_id": "other"}, {"version": "future"}):
            with self.subTest(change=change):
                self.assertEqual(self.new_boundary().admit(self.message(**change), 1).reason, "WRONG_RUN_OR_VERSION")

    def test_changed_candidate_evidence_or_policy_digest_is_rejected(self):
        for field in ("candidate_digest", "evidence_digest", "policy_digest"):
            with self.subTest(field=field):
                self.assertEqual(
                    self.new_boundary().admit(self.message(**{field: auth.digest_text("wrong")}), 1).reason,
                    "IDENTITY_MISMATCH",
                )

    def test_no_peer_edge_in_independent_mode(self):
        self.assertEqual(self.boundary.admit(self.message(recipient_id="critic"), 1).reason, "UNAUTHORIZED_EDGE")

    def test_switch_requests_are_not_implicitly_authorized(self):
        self.assertEqual(self.boundary.admit(self.message(sender="gov", kind="SWITCH_REQUEST"), 1).reason,
                         "UNAUTHORIZED_KIND")

    def test_malformed_fields_fail_closed(self):
        for change in ({"epoch": True}, {"predecessor": -1}, {"deadline": "tomorrow"}, {"mac": None}):
            with self.subTest(change=change):
                original = replace(self.message(), **change)
                self.assertEqual(self.new_boundary().admit(original, 1).reason, "MALFORMED")
        self.assertEqual(self.boundary.admit(None, 1).reason, "MALFORMED")
        self.assertEqual(self.boundary.admit(self.message(), True).reason, "MALFORMED")

    def test_denied_authenticated_message_id_cannot_be_overwritten(self):
        bad = self.message(kind="SWITCH_REQUEST")
        self.assertEqual(self.boundary.admit(bad, 1).reason, "UNAUTHORIZED_KIND")
        self.assertEqual(self.boundary.admit(self.message(), 1).reason, "ID_CONFLICT")

    def test_concurrent_same_message_has_one_receipt_and_one_admission(self):
        message = self.message()
        barrier = Barrier(2)

        def attempt(_):
            barrier.wait()
            return self.boundary.admit(message, 1)

        with ThreadPoolExecutor(max_workers=2) as executor:
            receipts = list(executor.map(attempt, range(2)))
        self.assertEqual(receipts[0], receipts[1])
        self.assertEqual(self.boundary.snapshot()[1], 1)

    def test_invalid_manifest_cannot_create_authentication_boundary(self):
        with self.assertRaisesRegex(ValueError, "BAD_MANIFEST"):
            auth.SyntheticMessageBoundary(
                "run-001", {"gen": "Generator"}, {"gen": b"g" * 32},
                self.candidate_digest, self.evidence_digest, self.policy_digest,
            )
        with self.assertRaisesRegex(ValueError, "BAD_MANIFEST"):
            auth.SyntheticMessageBoundary(
                "run-001", self.roles, {"gen": b"too-short", "critic": b"c" * 32, "gov": b"v" * 32},
                self.candidate_digest, self.evidence_digest, self.policy_digest,
            )


if __name__ == "__main__":
    unittest.main()
