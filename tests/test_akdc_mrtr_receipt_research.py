"""Gate 13 SQLite MRTR receipt tests: no production permission or effects."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from experiments.akdc.mrtr_receipt_ledger_research import MRTRReceiptRefusal, SQLiteMRTRReceiptResearch

KEY = b"AKDC-TEST-RECEIPT-KEY-NOT-SECRET-0000001"
NONCE = "a" * 32
DIGEST = "b" * 64


class MRTRResearchReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "mrtr-fixture.sqlite")
        self.store = SQLiteMRTRReceiptResearch(self.db, KEY)

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, store=None, **kw):
        options = dict(
            nonce=NONCE, principal_claim="asserted-fixture-only", action="akdc-confirm-fixture", operation_digest=DIGEST
        )
        options.update(kw)
        return (store or self.store).record(**options)

    def cli(self, *, crash="", nonce=NONCE, key=KEY):
        cmd = [
            sys.executable,
            "-m",
            "experiments.akdc.mrtr_receipt_ledger_research",
            "--db",
            self.db,
            "--nonce",
            nonce,
            "--principal",
            "asserted-fixture-only",
            "--action",
            "akdc-confirm-fixture",
            "--operation-digest",
            DIGEST,
        ]
        if crash:
            cmd.extend(["--crash", crash])
        env = dict(os.environ, AKDC_RESEARCH_RECEIPT_KEY_HEX=key.hex())
        return subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)

    def test_first_and_duplicate_record_no_authority(self):
        self.assertEqual(self.record(), "FIRST_RECORDED")
        self.assertEqual(self.record(), "DUPLICATE_RECORDED")
        self.assertEqual(self.store.count(), 1)

    def test_concurrent_threads_one_first(self):
        with ThreadPoolExecutor(max_workers=16) as pool:
            outcomes = list(pool.map(lambda _: self.record(), range(32)))
        self.assertEqual(outcomes.count("FIRST_RECORDED"), 1)
        self.assertEqual(outcomes.count("DUPLICATE_RECORDED"), 31)
        self.assertEqual(self.store.count(), 1)

    def test_concurrent_independent_processes_one_first(self):
        cmd = [
            sys.executable,
            "-m",
            "experiments.akdc.mrtr_receipt_ledger_research",
            "--db",
            self.db,
            "--nonce",
            NONCE,
            "--principal",
            "asserted-fixture-only",
            "--action",
            "akdc-confirm-fixture",
            "--operation-digest",
            DIGEST,
        ]
        env = dict(os.environ, AKDC_RESEARCH_RECEIPT_KEY_HEX=KEY.hex())
        runners = [
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env) for _ in range(8)
        ]
        outputs = [p.communicate(timeout=25) for p in runners]
        self.assertTrue(all(p.returncode == 0 for p in runners), outputs)
        self.assertEqual(sum('"receipt": "FIRST_RECORDED"' in out[0] for out in outputs), 1)
        self.assertEqual(sum('"receipt": "DUPLICATE_RECORDED"' in out[0] for out in outputs), 7)
        self.assertEqual(self.store.count(), 1)

    def test_reopen_after_commit_is_duplicate(self):
        self.record()
        reopened = SQLiteMRTRReceiptResearch(self.db, KEY)
        self.assertEqual(self.record(reopened), "DUPLICATE_RECORDED")
        self.assertEqual(reopened.count(), 1)

    def test_crash_before_commit_rolls_back(self):
        self.assertEqual(self.cli(crash="before_commit").returncode, 35)
        reopened = SQLiteMRTRReceiptResearch(self.db, KEY)
        self.assertEqual(reopened.count(), 0)
        self.assertEqual(self.record(reopened), "FIRST_RECORDED")

    def test_crash_after_commit_persists_receipt(self):
        self.assertEqual(self.cli(crash="after_commit").returncode, 36)
        reopened = SQLiteMRTRReceiptResearch(self.db, KEY)
        self.assertEqual(reopened.count(), 1)
        self.assertEqual(self.record(reopened), "DUPLICATE_RECORDED")

    def test_principal_rebinding_refused(self):
        self.record()
        with self.assertRaisesRegex(MRTRReceiptRefusal, "binding collision"):
            self.record(principal_claim="different-claim")
        self.assertEqual(self.store.count(), 1)

    def test_operation_digest_rebinding_refused(self):
        self.record()
        with self.assertRaisesRegex(MRTRReceiptRefusal, "binding collision"):
            self.record(operation_digest="c" * 64)

    def test_key_rotation_does_not_preserve_replay_identity(self):
        self.record()
        rotated = SQLiteMRTRReceiptResearch(self.db, b"ANOTHER-TEST-KEY-ALSO-NOT-SECRET-00000")
        self.assertEqual(self.record(rotated), "FIRST_RECORDED")
        self.assertEqual(self.store.count(), 2)  # negative control: no automatic key-epoch dedup

    def test_wrong_claim_shape_fails_before_any_write(self):
        for kw in (
            dict(nonce="unsealed"),
            dict(principal_claim="claim with spaces"),
            dict(action="execute-payment"),
            dict(operation_digest="bad"),
            dict(crash="unknown"),
        ):
            with self.subTest(kw=kw), self.assertRaises(MRTRReceiptRefusal):
                self.record(**kw)
        self.assertEqual(self.store.count(), 0)

    def test_unversioned_partial_schema_refused_without_repair(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("DROP TABLE mrtr_receipt")
            conn.execute("PRAGMA user_version=0")
            conn.execute("CREATE TABLE mrtr_receipt (token_tag TEXT)")
        with self.assertRaisesRegex(MRTRReceiptRefusal, "unversioned"):
            SQLiteMRTRReceiptResearch(self.db, KEY)

    def test_weakened_constraints_refused(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("DROP TABLE mrtr_receipt")
            conn.execute(
                "CREATE TABLE mrtr_receipt (token_tag TEXT NOT NULL, bound_claim TEXT NOT NULL, "
                "status TEXT NOT NULL, outcome TEXT NOT NULL)"
            )
        with self.assertRaisesRegex(MRTRReceiptRefusal, "weakened"):
            SQLiteMRTRReceiptResearch(self.db, KEY)

    def test_plaintext_binding_and_nonce_not_stored(self):
        self.record()
        with sqlite3.connect(self.db) as conn:
            row = conn.execute("SELECT * FROM mrtr_receipt").fetchone()
        data = repr(row)
        self.assertNotIn(NONCE, data)
        self.assertNotIn("asserted-fixture-only", data)
        self.assertNotIn(KEY.decode("ascii"), data)
        self.assertEqual(row[2:], ("RECORD_ONLY", "SYNTHETIC_COMPLETE"))

    def test_empty_or_short_key_refused(self):
        for key in (b"", b"123", "nonbytes"):
            with self.subTest(key=key), self.assertRaisesRegex(MRTRReceiptRefusal, "key"):
                SQLiteMRTRReceiptResearch(self.db, key)


if __name__ == "__main__":
    unittest.main()
