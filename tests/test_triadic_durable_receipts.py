"""Disposable POSIX disk-state recovery tests; no real authority or effects."""

import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from hmac import new
from pathlib import Path
from threading import Barrier
from typing import cast

from scripts.triadic_commit_model import Proposal, SyntheticController
from scripts.triadic_durable_receipts import (
    DurableSyntheticController,
    JournalCorrupt,
    SimulatedCrash,
)


class DurableReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "journal.json"
        self.key = b"fixture-key-must-be-32-bytes-long!"
        self.proposal = Proposal("op1", "candidate", "evidence-v1", "policy-v1", 0, 0, True, False, 10)
        self.writer = self.create()

    def create(self, **kwargs):
        return DurableSyntheticController(
            self.path, "research-run", "evidence-v1", "policy-v1", self.key, create=True, **kwargs
        )

    def recover(self, **kwargs):
        manifest = {
            "path": self.path,
            "run_id": "research-run",
            "evidence": "evidence-v1",
            "policy": "policy-v1",
            "key": self.key,
        }
        manifest.update(kwargs)
        return DurableSyntheticController(**manifest)

    def signed_edit(self, change):
        """Malicious fixture authority can re-sign; test structural validation only."""
        data = json.loads(self.path.read_text())
        change(data["state"])
        canonical = json.dumps(data["state"], sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
        data["mac"] = new(self.key, canonical, "sha256").hexdigest()
        self.path.write_text(json.dumps(data))

    def test_committed_receipt_survives_restart_with_no_second_transition(self):
        receipt = self.writer.commit(self.proposal, 1)
        self.assertEqual(receipt.outcome, "COMMITTED_SYNTHETIC")
        recovered = self.recover()
        self.assertEqual(recovered.snapshot(), (1, 0, "candidate", True))
        self.assertEqual(recovered.commit(self.proposal, 20), receipt)
        self.assertEqual(recovered.snapshot(), (1, 0, "candidate", True))

    def test_recovered_reader_cannot_mint_new_admission_or_permission(self):
        self.writer.commit(self.proposal, 1)
        recovered = self.recover()
        attempt = replace(self.proposal, operation="op2", predecessor=1)
        self.assertEqual(recovered.commit(attempt, 2).reason, "RECOVERY_ONLY")
        with self.assertRaises(PermissionError):
            recovered.revoke()
        with self.assertRaises(PermissionError):
            recovered.invalidate_epoch()

    def test_before_replace_crash_does_not_persist_transition(self):
        with self.assertRaisesRegex(SimulatedCrash, "BEFORE_REPLACE"):
            self.writer.commit(self.proposal, 1, fault="BEFORE_REPLACE")
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))
        self.assertEqual(self.writer.commit(self.proposal, 2).reason, "WRITER_POISONED")
        self.assertEqual(self.recover().commit(self.proposal, 2).reason, "RECOVERY_ONLY")

    def test_after_durable_before_ack_replay_is_exactly_once(self):
        with self.assertRaisesRegex(SimulatedCrash, "AFTER_DURABLE_BEFORE_ACK"):
            self.writer.commit(self.proposal, 1, fault="AFTER_DURABLE_BEFORE_ACK")
        recovered = self.recover()
        self.assertEqual(recovered.snapshot(), (1, 0, "candidate", True))
        self.assertEqual(recovered.commit(self.proposal, 50).outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(recovered.snapshot(), (1, 0, "candidate", True))

    def test_conflicting_replay_preserves_historical_receipt(self):
        expected = self.writer.commit(self.proposal, 1)
        recovered = self.recover()
        self.assertEqual(recovered.commit(replace(self.proposal, candidate="other"), 2).reason, "ID_CONFLICT")
        self.assertEqual(recovered.commit(self.proposal, 2), expected)

    def test_durable_denial_cannot_be_replaced_by_changed_operation(self):
        rejected = replace(self.proposal, objection=True)
        self.assertEqual(self.writer.commit(rejected, 1).reason, "INCOMPLETE_OR_OBJECTED")
        recovered = self.recover()
        self.assertEqual(recovered.commit(rejected, 3).reason, "INCOMPLETE_OR_OBJECTED")
        self.assertEqual(recovered.commit(self.proposal, 3).reason, "ID_CONFLICT")
        self.assertEqual(recovered.snapshot()[0], 0)

    def test_persisted_revocation_survives_reopen_and_cannot_reauthorize(self):
        self.writer.revoke()
        self.assertEqual(self.writer.commit(self.proposal, 1).reason, "REVOKED")
        recovered = self.recover()
        self.assertFalse(recovered.snapshot()[3])
        self.assertEqual(recovered.commit(self.proposal, 5).reason, "REVOKED")
        self.assertEqual(recovered.commit(replace(self.proposal, operation="op2"), 5).reason, "RECOVERY_ONLY")

    def test_epoch_fault_injection_is_persisted(self):
        self.writer.invalidate_epoch()
        self.assertEqual(self.writer.commit(self.proposal, 1).reason, "STALE_EPOCH")
        self.assertEqual(self.recover().snapshot(), (0, 1, None, True))

    def test_malformed_proposals_and_clock_do_not_create_entries(self):
        self.assertEqual(self.writer.commit(cast(Proposal, None), 1).reason, "MALFORMED")
        self.assertEqual(self.writer.commit(replace(self.proposal, epoch=True), 1).reason, "MALFORMED")
        self.assertEqual(self.writer.commit(self.proposal, True).reason, "MALFORMED")
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))

    def test_controller_parity_for_frozen_bounded_sequence(self):
        controller = SyntheticController("evidence-v1", "policy-v1")
        attempts = (
            (replace(self.proposal, operation="deny", objection=True), 1),
            (self.proposal, 1),
            (replace(self.proposal, operation="op2", predecessor=0), 2),
            (replace(self.proposal, operation="op3", predecessor=1, candidate="new"), 3),
        )
        for proposal, now in attempts:
            self.assertEqual(self.writer.commit(proposal, now), controller.commit(proposal, now))
        self.assertEqual(self.writer.snapshot()[:3], controller.snapshot())
        self.assertEqual(self.recover().snapshot()[:3], controller.snapshot())

    def test_two_concurrent_proposals_have_one_winner(self):
        barrier = Barrier(2)

        def attempt(operation):
            barrier.wait()
            return self.writer.commit(replace(self.proposal, operation=operation), 1)

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(attempt, ("first", "second")))
        self.assertEqual(sorted(result.reason for result in results), ["ELIGIBLE", "STALE_PREDECESSOR"])
        self.assertEqual(self.recover().snapshot()[0], 1)

    def test_existing_path_cannot_be_recreated_to_reset_authority(self):
        self.writer.revoke()
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertFalse(self.recover().snapshot()[3])

    def test_wrong_manifest_and_wrong_key_reject_recovery(self):
        with self.assertRaises(JournalCorrupt):
            self.recover(policy="wrong")
        with self.assertRaises(JournalCorrupt):
            self.recover(key=b"x" * 32)

    def test_single_byte_tampering_is_detected(self):
        raw = self.path.read_bytes()
        self.path.write_bytes(raw.replace(b"research-run", b"research-fun"))
        with self.assertRaises(JournalCorrupt):
            self.recover()

    def test_truncated_and_trailing_unparsed_bytes_fail_closed(self):
        raw = self.path.read_bytes()
        self.path.write_bytes(raw[:13])
        with self.assertRaises(JournalCorrupt):
            self.recover()
        self.path.write_bytes(raw + b"BROKEN")
        with self.assertRaises(JournalCorrupt):
            self.recover()

    def test_wrong_key_length_and_insecure_manifest_rejected(self):
        with self.assertRaisesRegex(ValueError, "BAD_FIXTURE_MANIFEST"):
            DurableSyntheticController(self.path, "research-run", "evidence-v1", "policy-v1", b"weak")

    def test_missing_journal_never_creates_authority_on_recovery(self):
        self.path.unlink()
        with self.assertRaises(JournalCorrupt):
            self.recover()

    def test_mac_valid_but_inconsistent_commit_count_rejected(self):
        self.writer.commit(self.proposal, 1)
        self.signed_edit(lambda state: state.update(version=2))
        with self.assertRaisesRegex(JournalCorrupt, "BAD_COMMIT_COUNT"):
            self.recover()

    def test_mac_valid_but_duplicated_operation_rejected(self):
        self.writer.commit(self.proposal, 1)
        self.signed_edit(lambda state: state["entries"].append(state["entries"][0]))
        with self.assertRaisesRegex(JournalCorrupt, "BAD_ENTRY"):
            self.recover()

    def test_valid_older_snapshot_rollback_is_not_detected(self):
        """Known negative: MAC alone does not provide anti-rollback custody."""
        self.writer.commit(self.proposal, 1)
        old_authenticated_snapshot = self.path.read_bytes()
        later = replace(self.proposal, operation="op2", candidate="new", predecessor=1)
        self.writer.commit(later, 2)
        self.assertEqual(self.recover().snapshot()[0], 2)
        self.path.write_bytes(old_authenticated_snapshot)
        recovered = self.recover()
        self.assertEqual(recovered.snapshot(), (1, 0, "candidate", True))
        self.assertEqual(recovered.commit(later, 3).reason, "RECOVERY_ONLY")

    def test_wrong_run_cannot_recover_a_journal(self):
        with self.assertRaisesRegex(JournalCorrupt, "MANIFEST_MISMATCH"):
            DurableSyntheticController(self.path, "other-run", "evidence-v1", "policy-v1", self.key)

    def test_recovery_does_not_claim_semantic_correctness(self):
        wrong = replace(self.proposal, candidate="2+2=5")
        self.assertEqual(self.writer.commit(wrong, 1).outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(self.recover().snapshot()[2], "2+2=5")
        self.assertNotEqual(self.recover().snapshot()[2], "2+2=4")


if __name__ == "__main__":
    unittest.main()
