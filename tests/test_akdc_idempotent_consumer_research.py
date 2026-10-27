"""Gate 15 synthetic two-database idempotent consumer crash / replay controls."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

from experiments.akdc.idempotent_consumer_research import (
    ConsumerRefusal,
    SQLiteIdempotentConsumerResearch,
    deliver_one,
)
from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch

KEY = b"AKDC-TEST-OUTBOX-KEY-NOT-SECRET-00000001"
NONCE = "a" * 32
DIGEST = "b" * 64
OTHER = "c" * 64


class Gate15SyntheticConsumerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.producer_path = str(Path(self.tmp.name) / "sender.sqlite")
        self.consumer_path = str(Path(self.tmp.name) / "receiver.sqlite")
        self.producer = SQLiteOutboxResearch(self.producer_path, KEY)
        self.consumer = SQLiteIdempotentConsumerResearch(self.consumer_path)

    def tearDown(self):
        self.tmp.cleanup()

    def submit(self, sender=None, nonce=NONCE):
        return (sender or self.producer).submit(
            nonce=nonce,
            principal="asserted-only",
            action="akdc-confirm-fixture",
            operation_digest=DIGEST,
        )

    def die(self, crash):
        command = [
            sys.executable,
            "-m",
            "experiments.akdc.idempotent_consumer_research",
            "--producer",
            self.producer_path,
            "--consumer",
            self.consumer_path,
            "--crash",
            crash,
        ]
        env = dict(os.environ, AKDC_RESEARCH_OUTBOX_KEY_HEX=KEY.hex())
        return subprocess.run(command, env=env, capture_output=True, text=True, check=False)

    def sample_key(self):
        with closing(sqlite3.connect(self.producer_path)) as conn:
            return conn.execute("SELECT tag, payload FROM outbox LIMIT 1").fetchone()

    def test_first_delivery_and_noop_replay(self):
        self.submit()
        self.assertEqual(deliver_one(self.producer, self.consumer), "FIRST_RECEIVER_MARKER")
        self.assertEqual(deliver_one(self.producer, self.consumer), "NO_PENDING")
        self.assertEqual(self.consumer.counts(), (1, 1))
        self.assertEqual(self.producer.counts(), (1, 0, 1))

    def test_receiver_commit_then_sender_crash_replays_once(self):
        self.submit()
        self.assertEqual(self.die("after_receiver_before_ack").returncode, 73)
        self.assertEqual(self.consumer.counts(), (1, 1))
        self.assertEqual(self.producer.counts(), (1, 1, 0))
        self.assertEqual(deliver_one(self.producer, self.consumer), "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.producer.counts(), (1, 0, 1))
        self.assertEqual(self.consumer.counts(), (1, 1))

    def test_sender_ack_then_crash_does_not_redeliver(self):
        self.submit()
        self.assertEqual(self.die("after_sender_ack").returncode, 74)
        self.assertEqual(self.consumer.counts(), (1, 1))
        self.assertEqual(self.producer.counts(), (1, 0, 1))
        self.assertEqual(deliver_one(self.producer, self.consumer), "NO_PENDING")

    def test_32_threads_deliver_a_single_marker(self):
        self.submit()
        with ThreadPoolExecutor(max_workers=16) as executor:
            results = list(executor.map(lambda _: deliver_one(self.producer, self.consumer), range(32)))
        self.assertEqual(results.count("FIRST_RECEIVER_MARKER"), 1)
        self.assertEqual(results.count("NO_PENDING"), 31)
        self.assertEqual(self.consumer.counts(), (1, 1))

    def test_eight_processes_deliver_a_single_marker(self):
        self.submit()
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.die(""), range(8)))
        self.assertTrue(all(x.returncode == 0 for x in results), [x.stderr for x in results])
        self.assertEqual(sum("FIRST_RECEIVER_MARKER" in x.stdout for x in results), 1)
        self.assertEqual(sum("NO_PENDING" in x.stdout for x in results), 7)
        self.assertEqual(self.consumer.counts(), (1, 1))

    def test_reused_key_different_payload_is_refused(self):
        self.submit()
        tag, payload = self.sample_key()
        self.assertEqual(self.consumer.accept(key=tag, payload=payload), "FIRST_RECEIVER_MARKER")
        with self.assertRaisesRegex(ConsumerRefusal, "different bound payload"):
            self.consumer.accept(key=tag, payload=OTHER)
        self.assertEqual(self.consumer.counts(), (1, 1))

    def test_receiver_crash_before_commit_leaves_no_marker(self):
        self.submit()
        tag, payload = self.sample_key()
        code = (
            "from experiments.akdc.idempotent_consumer_research import SQLiteIdempotentConsumerResearch as S;"
            "import sys;S(sys.argv[1]).accept(key=sys.argv[2],payload=sys.argv[3],crash='before_commit')"
        )
        result = subprocess.run(
            [sys.executable, "-c", code, self.consumer_path, tag, payload],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 71)
        self.assertEqual(self.consumer.counts(), (0, 0))
        self.assertEqual(deliver_one(self.producer, self.consumer), "FIRST_RECEIVER_MARKER")

    def test_receiver_crash_after_commit_replay_is_duplicate(self):
        self.submit()
        tag, payload = self.sample_key()
        code = (
            "from experiments.akdc.idempotent_consumer_research import SQLiteIdempotentConsumerResearch as S;"
            "import sys;S(sys.argv[1]).accept(key=sys.argv[2],payload=sys.argv[3],crash='after_commit')"
        )
        result = subprocess.run(
            [sys.executable, "-c", code, self.consumer_path, tag, payload],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 72)
        self.assertEqual(self.consumer.counts(), (1, 1))
        self.assertEqual(deliver_one(self.producer, self.consumer), "DUPLICATE_RECEIVER_MARKER")

    def test_consumer_survives_reopen_without_double_marker(self):
        self.submit()
        self.assertEqual(deliver_one(self.producer, self.consumer), "FIRST_RECEIVER_MARKER")
        reopened = SQLiteIdempotentConsumerResearch(self.consumer_path)
        tag, payload = self.sample_key()
        self.assertEqual(reopened.accept(key=tag, payload=payload), "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(reopened.counts(), (1, 1))

    def test_sender_key_epoch_rotation_creates_second_consumer_identity(self):
        self.submit()
        self.assertEqual(deliver_one(self.producer, self.consumer), "FIRST_RECEIVER_MARKER")
        rotated_sender = SQLiteOutboxResearch(self.producer_path, b"DIFFERENT-KEY-WITH-NO-PRODUCTION-CUSTODY-01")
        self.assertEqual(self.submit(rotated_sender), "ENQUEUED")
        self.assertEqual(deliver_one(rotated_sender, self.consumer), "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.consumer.counts(), (2, 2))  # negative control

    def test_schema_weakening_refused(self):
        with closing(sqlite3.connect(self.consumer_path)) as conn, conn:
            conn.execute("DROP TABLE receiver_effect")
            conn.execute("DROP TABLE inbox")
            conn.execute("CREATE TABLE inbox (idempotency_key TEXT, payload_tag TEXT)")
        with self.assertRaises(ConsumerRefusal):
            SQLiteIdempotentConsumerResearch(self.consumer_path)

    def test_unversioned_partial_schema_refused(self):
        with closing(sqlite3.connect(self.consumer_path)) as conn, conn:
            conn.execute("PRAGMA user_version=0")
        with self.assertRaisesRegex(ConsumerRefusal, "unversioned"):
            SQLiteIdempotentConsumerResearch(self.consumer_path)

    def test_reject_bad_key_payload_and_in_memory(self):
        with self.assertRaises(ConsumerRefusal):
            SQLiteIdempotentConsumerResearch(":memory:")
        with self.assertRaises(ConsumerRefusal):
            self.consumer.accept(key="wrong", payload=DIGEST)
        with self.assertRaises(ConsumerRefusal):
            self.consumer.accept(key=NONCE + NONCE, payload="wrong")

    def test_two_sender_dbs_with_same_identity_dedup_at_consumer(self):
        self.submit()
        self.assertEqual(deliver_one(self.producer, self.consumer), "FIRST_RECEIVER_MARKER")
        second_path = str(Path(self.tmp.name) / "sender2.sqlite")
        second = SQLiteOutboxResearch(second_path, KEY)
        self.submit(second)
        self.assertEqual(deliver_one(second, self.consumer), "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.consumer.counts(), (1, 1))
        self.assertEqual(second.counts(), (1, 0, 1))


if __name__ == "__main__":
    unittest.main()
