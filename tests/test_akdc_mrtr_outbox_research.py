"""Gate 14 synthetic outbox, crash boundaries, replay and nonauthority."""

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

from experiments.akdc.mrtr_outbox_research import (
    OutboxRefusal,
    SQLiteOutboxResearch,
)

KEY = b"AKDC-TEST-OUTBOX-KEY-NOT-SECRET-00000001"
NONCE = "a" * 32
DIGEST = "b" * 64


class OutboxResearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / "outbox.sqlite")
        self.sink = Path(self.tmp.name) / "synthetic-effects.log"
        self.store = SQLiteOutboxResearch(self.path, KEY)

    def tearDown(self):
        self.tmp.cleanup()

    def submit(self, store=None, **kw):
        d = dict(nonce=NONCE, principal="asserted-only", action="akdc-confirm-fixture", operation_digest=DIGEST)
        d.update(kw)
        return (store or self.store).submit(**d)

    def cli(self, mode, crash="", *, sink=False, nonce=NONCE):
        command = [
            sys.executable,
            "-m",
            "experiments.akdc.mrtr_outbox_research",
            "--db",
            self.path,
            "--mode",
            mode,
            "--nonce",
            nonce,
            "--principal",
            "asserted-only",
            "--operation-digest",
            DIGEST,
        ]
        if crash:
            command.extend(("--crash", crash))
        if sink:
            command.extend(("--sink", str(self.sink)))
        env = dict(os.environ, AKDC_RESEARCH_OUTBOX_KEY_HEX=KEY.hex())
        return subprocess.run(command, capture_output=True, text=True, env=env, check=False)

    def test_submit_one_and_duplicate_pending(self):
        self.assertEqual(self.submit(), "ENQUEUED")
        self.assertEqual(self.submit(), "EXISTING_PENDING")
        self.assertEqual(self.store.counts(), (1, 1, 0))

    def test_dispatch_local_marker_atomically_and_repeat_is_noop(self):
        self.submit()
        self.assertEqual(self.store.dispatch_one(), "LOCAL_MARKER_COMMITTED")
        self.assertEqual(self.store.dispatch_one(), "NO_PENDING")
        self.assertEqual(self.submit(), "EXISTING_APPLIED")
        self.assertEqual(self.store.counts(), (1, 0, 1))

    def test_32_threads_submit_one(self):
        with ThreadPoolExecutor(max_workers=16) as p:
            results = list(p.map(lambda _: self.submit(), range(32)))
        self.assertEqual(results.count("ENQUEUED"), 1)
        self.assertEqual(results.count("EXISTING_PENDING"), 31)
        self.assertEqual(self.store.counts(), (1, 1, 0))

    def test_eight_independent_processes_submit_one(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: self.cli("submit"), range(8)))
        self.assertTrue(all(r.returncode == 0 for r in results), [r.stderr for r in results])
        self.assertEqual(sum('"ENQUEUED"' in r.stdout for r in results), 1)
        self.assertEqual(sum('"EXISTING_PENDING"' in r.stdout for r in results), 7)
        self.assertEqual(self.store.counts(), (1, 1, 0))

    def test_crash_before_enqueue_commit_rolls_back_both_tables(self):
        self.assertEqual(self.cli("submit", "before_commit").returncode, 51)
        self.assertEqual(SQLiteOutboxResearch(self.path, KEY).counts(), (0, 0, 0))
        self.assertEqual(self.submit(), "ENQUEUED")

    def test_crash_after_enqueue_commit_recovers_pending(self):
        self.assertEqual(self.cli("submit", "after_commit").returncode, 52)
        self.assertEqual(SQLiteOutboxResearch(self.path, KEY).counts(), (1, 1, 0))
        self.assertEqual(self.store.dispatch_one(), "LOCAL_MARKER_COMMITTED")

    def test_crash_before_local_effect_commit_rolls_back(self):
        self.submit()
        self.assertEqual(self.cli("dispatch", "before_local_commit").returncode, 53)
        self.assertEqual(SQLiteOutboxResearch(self.path, KEY).counts(), (1, 1, 0))
        self.assertEqual(self.store.dispatch_one(), "LOCAL_MARKER_COMMITTED")
        self.assertEqual(self.store.counts(), (1, 0, 1))

    def test_crash_after_local_effect_commit_persists(self):
        self.submit()
        self.assertEqual(self.cli("dispatch", "after_local_commit").returncode, 54)
        self.assertEqual(SQLiteOutboxResearch(self.path, KEY).counts(), (1, 0, 1))
        self.assertEqual(self.store.dispatch_one(), "NO_PENDING")

    def test_external_sink_failure_demonstrates_duplicate_effect(self):
        self.submit()
        self.assertEqual(self.cli("dispatch", "after_sink_before_commit", sink=True).returncode, 53)
        self.assertEqual(self.store.counts(), (1, 1, 0))
        self.assertEqual(self.sink.read_text().count("SYNTHETIC_NONAUTHORIZING_EFFECT"), 1)
        self.assertEqual(self.store.dispatch_one(sink=self.sink), "LOCAL_MARKER_COMMITTED")
        self.assertEqual(self.store.counts(), (1, 0, 1))
        self.assertEqual(self.sink.read_text().count("SYNTHETIC_NONAUTHORIZING_EFFECT"), 2)

    def test_concurrent_dispatchers_one_local_effect(self):
        self.submit()
        with ThreadPoolExecutor(max_workers=12) as p:
            out = list(p.map(lambda _: self.store.dispatch_one(), range(12)))
        self.assertEqual(out.count("LOCAL_MARKER_COMMITTED"), 1)
        self.assertEqual(out.count("NO_PENDING"), 11)
        self.assertEqual(self.store.counts(), (1, 0, 1))

    def test_binding_collision_denies_reassociation(self):
        self.submit()
        with self.assertRaisesRegex(OutboxRefusal, "rebinding"):
            self.submit(principal="other-assertion")
        with self.assertRaisesRegex(OutboxRefusal, "rebinding"):
            self.submit(operation_digest="c" * 64)
        self.assertEqual(self.store.counts(), (1, 1, 0))

    def test_key_rotation_can_create_second_receipt_negative_control(self):
        self.submit()
        rotated = SQLiteOutboxResearch(self.path, b"DIFFERENT-KEY-WITH-NO-PRODUCTION-CUSTODY-01")
        self.assertEqual(self.submit(rotated), "ENQUEUED")
        self.assertEqual(self.store.counts(), (2, 2, 0))

    def test_plaintext_nonce_and_claim_not_persisted(self):
        self.submit()
        with closing(sqlite3.connect(self.path)) as conn, conn:
            d = repr(conn.execute("SELECT * FROM receipt").fetchall())
        self.assertNotIn(NONCE, d)
        self.assertNotIn("asserted-only", d)
        self.assertNotIn(KEY.decode(), d)

    def test_invalid_inputs_fail_closed(self):
        bads = [
            dict(nonce="bad"),
            dict(principal="with spaces"),
            dict(operation_digest="wrong"),
            dict(action="some-payment"),
            dict(crash="invalid"),
        ]
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(OutboxRefusal):
                self.submit(**bad)
        self.assertEqual(self.store.counts(), (0, 0, 0))

    def test_unversioned_partial_schema_refused(self):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute("DROP TABLE local_effect")
            conn.execute("DROP TABLE outbox")
            conn.execute("DROP TABLE receipt")
            conn.execute("PRAGMA user_version=0")
            conn.execute("CREATE TABLE receipt (tag TEXT)")
        with self.assertRaises(OutboxRefusal):
            SQLiteOutboxResearch(self.path, KEY)

    def test_weakened_primary_key_refused(self):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute("DROP TABLE local_effect")
            conn.execute("DROP TABLE outbox")
            conn.execute("DROP TABLE receipt")
            conn.execute("CREATE TABLE receipt (tag TEXT NOT NULL, binding TEXT NOT NULL, status TEXT NOT NULL)")
        with self.assertRaises(OutboxRefusal):
            SQLiteOutboxResearch(self.path, KEY)

    def test_foreign_key_is_enforced(self):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute("PRAGMA foreign_keys=ON")
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO outbox VALUES ('orphan', 'x', 'PENDING')")

    def test_no_pending_dispatch_is_noop(self):
        self.assertEqual(self.store.dispatch_one(), "NO_PENDING")
        self.assertEqual(self.store.counts(), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
