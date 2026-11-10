"""Cross-process POSIX fixture witness tests, not external custody validation."""

import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from hashlib import sha256
from pathlib import Path

from scripts.triadic_commit_model import Proposal
from scripts.triadic_durable_receipts import SimulatedCrash
from scripts.triadic_monotonic_custody import CustodyMismatch, WitnessedSyntheticController
from scripts.triadic_posix_witness import PosixFileWitness


class FileWitnessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "journal").mkdir()
        (root / "witness").mkdir()
        self.journal = root / "journal" / "journal.json"
        self.anchor = root / "witness" / "witness.jsonl"
        self.run_id = "run-file-witness"
        self.key = b"journal-fixture-key-32-bytes-long!"
        self.witness_key = b"independent-fixture-witness-key-32!"
        self.witness = self.open_witness()
        self.controller = WitnessedSyntheticController.create(
            self.journal, self.run_id, "evidence-v1", "policy-v1", self.key, self.witness
        )
        self.proposal = Proposal("op1", "candidate", "evidence-v1", "policy-v1", 0, 0, True, False, 10)

    def open_witness(self, **changes):
        arguments = {"path": self.anchor, "stream_id": self.run_id, "key": self.witness_key}
        arguments.update(changes)
        return PosixFileWitness(**arguments)

    def recover(self, witness=None):
        return WitnessedSyntheticController.recover(
            self.journal, self.run_id, "evidence-v1", "policy-v1", self.key,
            witness if witness is not None else self.open_witness(),
        )

    def anchored(self):
        state = self.open_witness().snapshot()
        assert state is not None
        return state

    def test_genesis_is_durable_across_object_reopen(self):
        self.assertEqual(self.anchored().sequence, 0)
        self.assertEqual(self.anchored().journal_digest, sha256(self.journal.read_bytes()).hexdigest())
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))

    def test_committed_receipt_and_sequence_survive_reopening(self):
        original = self.controller.commit(self.proposal, 1)
        self.assertEqual(self.anchored().sequence, 1)
        reader = self.recover()
        self.assertEqual(reader.commit(self.proposal, 20), original)
        self.assertEqual(reader.snapshot(), (1, 0, "candidate", True))

    def test_reopened_reader_cannot_mint_more_authority(self):
        self.controller.commit(self.proposal, 1)
        attempt = replace(self.proposal, operation="new", predecessor=1)
        self.assertEqual(self.recover().commit(attempt, 2).reason, "RECOVERY_ONLY")
        self.assertEqual(self.anchored().sequence, 1)

    def test_denied_receipt_is_also_witnessed(self):
        denied = replace(self.proposal, objection=True)
        self.assertEqual(self.controller.commit(denied, 1).outcome, "HOLD")
        self.assertEqual(self.anchored().sequence, 1)
        self.assertEqual(self.recover().commit(denied, 2).reason, "INCOMPLETE_OR_OBJECTED")

    def test_replay_and_changed_id_do_not_advance_witness(self):
        self.controller.commit(self.proposal, 1)
        old = self.anchored()
        self.assertEqual(self.controller.commit(self.proposal, 2).outcome, "COMMITTED_SYNTHETIC")
        changed = replace(self.proposal, candidate="other")
        self.assertEqual(self.controller.commit(changed, 2).reason, "ID_CONFLICT")
        self.assertEqual(self.anchored(), old)

    def test_surviving_witness_detects_signed_journal_rollback(self):
        self.controller.commit(self.proposal, 1)
        older = self.journal.read_bytes()
        second = replace(self.proposal, operation="op2", candidate="new", predecessor=1)
        self.controller.commit(second, 2)
        self.journal.write_bytes(older)
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()

    def test_roll_back_both_files_is_a_known_undetected_attack(self):
        self.controller.commit(self.proposal, 1)
        old_journal = self.journal.read_bytes()
        old_witness = self.anchor.read_bytes()
        second = replace(self.proposal, operation="op2", candidate="new", predecessor=1)
        self.controller.commit(second, 2)
        self.assertEqual(self.anchored().sequence, 2)
        self.journal.write_bytes(old_journal)
        self.anchor.write_bytes(old_witness)
        self.assertEqual(self.recover().snapshot(), (1, 0, "candidate", True))
        self.assertEqual(self.anchored().sequence, 1)

    def test_crash_before_journal_replace_recovers_old_state(self):
        with self.assertRaisesRegex(SimulatedCrash, "BEFORE_REPLACE"):
            self.controller.commit(self.proposal, 1, fault="BEFORE_REPLACE")
        self.assertEqual(self.recover().snapshot(), (0, 0, None, True))
        self.assertEqual(self.anchored().sequence, 0)

    def test_crash_after_journal_before_witness_blocks_restart(self):
        with self.assertRaisesRegex(SimulatedCrash, "AFTER_DURABLE_BEFORE_ACK"):
            self.controller.commit(self.proposal, 1, fault="AFTER_JOURNAL_BEFORE_WITNESS")
        with self.assertRaisesRegex(CustodyMismatch, "JOURNAL_WITNESS_DIVERGENCE"):
            self.recover()

    def test_crash_after_witness_before_ack_recovers_original_receipt(self):
        with self.assertRaisesRegex(SimulatedCrash, "AFTER_WITNESS_BEFORE_ACK"):
            self.controller.commit(self.proposal, 1, fault="AFTER_WITNESS_BEFORE_ACK")
        reader = self.recover()
        self.assertEqual(reader.snapshot(), (1, 0, "candidate", True))
        self.assertEqual(reader.commit(self.proposal, 20).outcome, "COMMITTED_SYNTHETIC")
        self.assertEqual(self.anchored().sequence, 1)

    def test_partial_append_blocks_recovery_not_silently_truncated(self):
        with self.anchor.open("ab") as handle:
            handle.write(b'{"body":')
        with self.assertRaisesRegex(CustodyMismatch, "INCOMPLETE_WITNESS"):
            self.recover()

    def test_tampered_hmac_chain_blocks_recovery(self):
        self.controller.commit(self.proposal, 1)
        self.anchor.write_bytes(self.anchor.read_bytes().replace(b'"sequence":1', b'"sequence":9'))
        with self.assertRaises(CustodyMismatch):
            self.recover()

    def test_wrong_witness_key_fails_closed(self):
        with self.assertRaisesRegex(CustodyMismatch, "INVALID_WITNESS_MAC"):
            self.recover(witness=self.open_witness(key=b"other-independent-witness-key-32!"))

    def test_wrong_witness_stream_fails_closed(self):
        with self.assertRaisesRegex(CustodyMismatch, "INVALID_WITNESS_CHAIN"):
            self.recover(witness=self.open_witness(stream_id="wrong"))

    def test_deleted_witness_does_not_bootstrap_on_recovery(self):
        self.anchor.unlink()
        with self.assertRaisesRegex(CustodyMismatch, "MISSING_WITNESS"):
            self.recover()

    def test_duplicate_initialize_is_blocked(self):
        with self.assertRaisesRegex(CustodyMismatch, "ALREADY_INITIALIZED"):
            self.open_witness().initialize("0" * 64)

    def test_stale_cas_does_not_append(self):
        old = self.anchored()
        self.controller.commit(self.proposal, 1)
        current = self.anchored()
        with self.assertRaisesRegex(CustodyMismatch, "STALE_WITNESS"):
            self.open_witness().advance(old, "a" * 64)
        self.assertEqual(self.anchored(), current)

    def test_nonadvancing_cas_is_rejected(self):
        old = self.anchored()
        with self.assertRaisesRegex(CustodyMismatch, "NON_ADVANCING_WITNESS"):
            self.open_witness().advance(old, old.journal_digest)

    def test_symlink_witness_is_rejected(self):
        raw = self.anchor.read_bytes()
        other = self.anchor.with_name("other.jsonl")
        other.write_bytes(raw)
        self.anchor.unlink()
        self.anchor.symlink_to(other)
        with self.assertRaisesRegex(CustodyMismatch, "SYMLINK_WITNESS"):
            self.recover()

    def test_symlink_lock_is_rejected(self):
        lock_path = self.anchor.with_name(self.anchor.name + ".lock")
        lock_path.unlink()
        lock_path.symlink_to(self.anchor)
        with self.assertRaisesRegex(CustodyMismatch, "WITNESS_LOCK_UNAVAILABLE"):
            self.recover()

    def test_two_competing_processes_cannot_both_advance_one_sequence(self):
        current = self.anchored()
        code = (
            "import sys\n"
            "from scripts.triadic_monotonic_custody import WitnessState, CustodyMismatch\n"
            "from scripts.triadic_posix_witness import PosixFileWitness\n"
            "from pathlib import Path\n"
            "w=PosixFileWitness(Path(sys.argv[1]),sys.argv[2],bytes.fromhex(sys.argv[3]))\n"
            "expected=WitnessState(sys.argv[2],int(sys.argv[4]),sys.argv[5])\n"
            "try:\n"
            "    w.advance(expected,sys.argv[6]); print('ADVANCED')\n"
            "except CustodyMismatch as exc:\n"
            "    print(str(exc))\n"
        )
        argv = [
            sys.executable, "-c", code, str(self.anchor),
            self.run_id, self.witness_key.hex(),
            str(current.sequence), current.journal_digest,
        ]
        root = Path(__file__).resolve().parents[1]
        first = subprocess.Popen(argv + ["a" * 64], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        second = subprocess.Popen(argv + ["b" * 64], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        first_out, first_err = first.communicate(timeout=15)
        second_out, second_err = second.communicate(timeout=15)
        self.assertEqual((first.returncode, second.returncode), (0, 0), (first_err, second_err))
        self.assertEqual(
            sorted((first_out.decode().strip(), second_out.decode().strip())),
            ["ADVANCED", "STALE_WITNESS"],
        )
        self.assertEqual(self.anchored().sequence, current.sequence + 1)

    def test_invalid_manifest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "BAD_FILE_WITNESS_MANIFEST"):
            self.open_witness(key=b"short")
        with self.assertRaisesRegex(ValueError, "BAD_FILE_WITNESS_MANIFEST"):
            self.open_witness(stream_id="")


if __name__ == "__main__":
    unittest.main()
