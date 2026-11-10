"""Finite C14-adjacent custody tests. No scientific or deployment samples."""

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from threading import Barrier

from scripts.triadic_commit_model import Proposal
from scripts.triadic_durable_receipts import SimulatedCrash
from scripts.triadic_monotonic_custody import (
    CustodyMismatch,
    FixtureMonotonicWitness,
    WitnessedSyntheticController,
)


class MonotonicCustodyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "journal.json"
        self.key = b"fixture-key-must-be-32-bytes-long!"
        self.run_id = "research-run"
        self.witness = FixtureMonotonicWitness(self.run_id)
        self.writer = WitnessedSyntheticController.create(
            self.path, self.run_id, "evidence-v1", "policy-v1", self.key, self.witness
        )
        self.proposal = Proposal("op1", "candidate", "evidence-v1", "policy-v1", 0, 0, True, False, 10)

    def recover(self, witness=None, run_id=None):
        return WitnessedSyntheticController.recover(
            self.path,
            run_id if run_id is not None else self.run_id,
            "evidence-v1",
            "policy-v1",
            self.key,
            witness if witness is not None else self.witness,
        )

    def anchored(self):
        state = self.witness.snapshot()
        assert state is not None
        return state

    def test_genesis_anchor_matches_journal(self):
        state = self.anchored()
        self.assertIsNotNone(state)
        self.assertEqual(state.sequence, 0)
        self.assertEqual(state.journal_digest, sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))

    def test_rejected_new_operation_is_anchored_too(self):
        denied = replace(self.proposal, objection=True)
        receipt = self.writer.commit(denied, 1)
        self.assertEqual(receipt.reason, "INCOMPLETE_OR_OBJECTED")
        self.assertEqual(self.anchored().sequence, 1)
        self.assertEqual(self.recover().commit(denied, 20), receipt)
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))

    def test_committed_receipt_survives_anchored_recovery(self):
        receipt = self.writer.commit(self.proposal, 1)
        self.assertEqual(receipt.outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(self.anchored().sequence, 1)
        reader = self.recover()
        self.assertEqual(reader.commit(self.proposal, 20), receipt)
        self.assertEqual(reader.snapshot(), (1, 0, "candidate", True))

    def test_recovered_reader_cannot_mint_new_admission(self):
        self.writer.commit(self.proposal, 1)
        future = replace(self.proposal, operation="new", predecessor=1)
        self.assertEqual(self.recover().commit(future, 2).reason, "RECOVERY_ONLY")
        self.assertEqual(self.anchored().sequence, 1)

    def test_identical_replay_does_not_advance_witness(self):
        expected = self.writer.commit(self.proposal, 1)
        before = self.witness.snapshot()
        self.assertEqual(self.writer.commit(self.proposal, 20), expected)
        self.assertEqual(self.witness.snapshot(), before)
        self.assertEqual(self.writer.commit(replace(self.proposal, candidate="different"), 2).reason, "ID_CONFLICT")
        self.assertEqual(self.witness.snapshot(), before)

    def test_before_replace_crash_keeps_genesis_anchor(self):
        initial = self.anchored()
        with self.assertRaisesRegex(SimulatedCrash, "BEFORE_REPLACE"):
            self.writer.commit(self.proposal, 1, fault="BEFORE_REPLACE")
        self.assertEqual(self.witness.snapshot(), initial)
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))
        with self.assertRaisesRegex(CustodyMismatch, "WRITER_QUARANTINED"):
            self.writer.commit(self.proposal, 2)

    def test_after_journal_before_witness_crash_is_detected_not_repaired(self):
        initial = self.anchored()
        with self.assertRaisesRegex(SimulatedCrash, "AFTER_DURABLE_BEFORE_ACK"):
            self.writer.commit(self.proposal, 1, fault="AFTER_JOURNAL_BEFORE_WITNESS")
        self.assertEqual(self.witness.snapshot(), initial)
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()
        with self.assertRaisesRegex(CustodyMismatch, "WRITER_QUARANTINED"):
            self.writer.commit(self.proposal, 2)

    def test_witness_refusal_after_durable_journal_blocks_recovery(self):
        with self.assertRaisesRegex(SimulatedCrash, "WITNESS_REFUSED"):
            self.writer.commit(self.proposal, 1, fault="WITNESS_REFUSED")
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()

    def test_after_witness_before_ack_crash_is_recoverable_exactly_once(self):
        with self.assertRaisesRegex(SimulatedCrash, "AFTER_WITNESS_BEFORE_ACK"):
            self.writer.commit(self.proposal, 1, fault="AFTER_WITNESS_BEFORE_ACK")
        reader = self.recover()
        self.assertEqual(reader.snapshot(), (1, 0, "candidate", True))
        first = reader.commit(self.proposal, 100)
        self.assertEqual(first.outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(reader.commit(self.proposal, 100), first)
        self.assertEqual(self.anchored().sequence, 1)
        with self.assertRaisesRegex(CustodyMismatch, "WRITER_QUARANTINED"):
            self.writer.commit(self.proposal, 2)

    def test_valid_hmac_snapshot_rollback_is_rejected_by_surviving_witness(self):
        self.writer.commit(self.proposal, 1)
        older = self.path.read_bytes()
        second = replace(self.proposal, operation="op2", candidate="new", predecessor=1)
        self.writer.commit(second, 2)
        self.assertEqual(self.anchored().sequence, 2)
        self.path.write_bytes(older)
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.writer.snapshot()

    def test_unchanged_witness_blocks_writer_after_file_rollback(self):
        initial_bytes = self.path.read_bytes()
        self.writer.commit(self.proposal, 1)
        self.path.write_bytes(initial_bytes)
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.writer.commit(replace(self.proposal, operation="op2", predecessor=1), 2)

    def test_replacing_witness_allows_valid_rollback_known_negative(self):
        self.writer.commit(self.proposal, 1)
        older = self.path.read_bytes()
        second = replace(self.proposal, operation="op2", candidate="new", predecessor=1)
        self.writer.commit(second, 2)
        self.path.write_bytes(older)
        attacker_replacement = FixtureMonotonicWitness(self.run_id)
        attacker_replacement.initialize(sha256(older).hexdigest())
        self.assertEqual(self.recover(witness=attacker_replacement).snapshot(), (1, 0, "candidate", True))
        self.assertEqual(self.anchored().sequence, 2)

    def test_missing_witness_never_bootstraps_from_untrusted_existing_file(self):
        empty = FixtureMonotonicWitness(self.run_id)
        with self.assertRaisesRegex(CustodyMismatch, "MISSING_WITNESS"):
            self.recover(witness=empty)

    def test_wrong_witness_stream_fails_closed(self):
        wrong = FixtureMonotonicWitness("other-run")
        wrong.initialize(sha256(self.path.read_bytes()).hexdigest())
        with self.assertRaisesRegex(CustodyMismatch, "WRONG_WITNESS_STREAM"):
            self.recover(witness=wrong)

    def test_cas_rejects_stale_witness_sequence(self):
        old = self.anchored()
        self.witness.advance(old, "1" * 64)
        with self.assertRaisesRegex(CustodyMismatch, "STALE_WITNESS"):
            self.witness.advance(old, "2" * 64)
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()

    def test_witness_cannot_be_reinitialized_or_nonadvancing(self):
        old = self.anchored()
        with self.assertRaisesRegex(CustodyMismatch, "ALREADY_INITIALIZED"):
            self.witness.initialize(old.journal_digest)
        with self.assertRaisesRegex(CustodyMismatch, "NON_ADVANCING_WITNESS"):
            self.witness.advance(old, old.journal_digest)

    def test_valid_manifest_cannot_create_duplicate_journal(self):
        second = FixtureMonotonicWitness(self.run_id)
        with self.assertRaises(FileExistsError):
            WitnessedSyntheticController.create(
                self.path, self.run_id, "evidence-v1", "policy-v1", self.key, second
            )
        self.assertIsNone(second.snapshot())

    def test_unsupported_fault_does_not_change_journal_or_witness(self):
        old_bytes = self.path.read_bytes()
        old = self.anchored()
        with self.assertRaisesRegex(ValueError, "UNKNOWN_FAULT"):
            self.writer.commit(self.proposal, 1, fault="UNKNOWN")
        self.assertEqual(self.witness.snapshot(), old)
        self.assertEqual(self.path.read_bytes(), old_bytes)

    def test_revocation_and_epoch_invalidation_are_witnessed(self):
        self.writer.revoke()
        self.assertEqual(self.anchored().sequence, 1)
        self.writer.invalidate_epoch()
        self.assertEqual(self.anchored().sequence, 2)
        self.assertEqual(self.recover().snapshot(), (0, 1, None, False))
        self.assertEqual(self.writer.commit(self.proposal, 1).reason, "REVOKED")
        self.assertEqual(self.anchored().sequence, 3)

    def test_noop_revocation_does_not_mint_witness_event(self):
        self.writer.revoke()
        old = self.anchored()
        self.writer.revoke()
        self.assertEqual(self.witness.snapshot(), old)

    def test_concurrent_proposals_still_have_single_commit_winner(self):
        barrier = Barrier(2)

        def attempt(operation):
            barrier.wait()
            return self.writer.commit(replace(self.proposal, operation=operation), 1)

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(attempt, ("first", "second")))
        self.assertEqual(sorted(result.reason for result in outcomes), ["ELIGIBLE", "STALE_PREDECESSOR"])
        self.assertEqual(self.recover().snapshot()[0], 1)
        self.assertEqual(self.anchored().sequence, 2)

    def test_invalid_proposal_has_no_persisted_receipt_or_witness_change(self):
        malformed = replace(self.proposal, predecessor=True)
        old = self.anchored()
        self.assertEqual(self.writer.commit(malformed, 1).reason, "MALFORMED")
        self.assertEqual(self.witness.snapshot(), old)
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))

    def test_false_answer_still_commits_but_custody_does_not_certify_truth(self):
        false_answer = replace(self.proposal, candidate="2+2=5")
        self.assertEqual(self.writer.commit(false_answer, 1).outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(self.recover().snapshot()[2], "2+2=5")
        self.assertNotEqual(self.recover().snapshot()[2], "2+2=4")


if __name__ == "__main__":
    unittest.main()
