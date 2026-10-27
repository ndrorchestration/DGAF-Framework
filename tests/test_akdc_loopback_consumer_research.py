"""Gate 16: actual localhost TCP/HTTP fixture-MAC and downstream dedup tests."""

from __future__ import annotations

import http.client
import os
import select
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

from experiments.akdc.idempotent_consumer_research import SQLiteIdempotentConsumerResearch
from experiments.akdc.loopback_consumer_research import (
    PATH,
    canonical_body,
    deliver_over_loopback,
    mac,
    post_fixture,
)
from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch

KEY = b"AKDC-TEST-OUTBOX-KEY-NOT-SECRET-00000001"
NONCE = "a" * 32
DIGEST = "b" * 64


class LoopbackReceiverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.receiver_file = str(Path(self.tmp.name) / "receiver.sqlite")
        self.sender_file = str(Path(self.tmp.name) / "sender.sqlite")
        self.receiver = SQLiteIdempotentConsumerResearch(self.receiver_file)
        self.sender = SQLiteOutboxResearch(self.sender_file, KEY)
        self.process: subprocess.Popen[str] | None = None
        self.port = 0
        self.start_server()

    def tearDown(self):
        self.stop_server()
        self.tmp.cleanup()

    def start_server(self):
        p = subprocess.Popen(
            [sys.executable, "-m", "experiments.akdc.loopback_consumer_research",
             "--receiver-db", self.receiver_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=dict(os.environ), bufsize=1,
        )
        self.process = p
        stream = p.stdout
        if stream is None:
            raise AssertionError("no test server stdout")
        ready, _, _ = select.select([stream], [], [], 8)
        if not ready:
            self.stop_server()
            raise AssertionError("fixture localhost server did not start")
        info = json.loads(stream.readline())
        self.assertTrue(info["fixture_only"])
        self.port = info["port"]

    def stop_server(self):
        p = self.process
        if p is None:
            return
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=4)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait(timeout=4)
        if p.stdout is not None:
            p.stdout.close()
        if p.stderr is not None:
            p.stderr.close()
        self.process = None

    def enqueue(self, sender=None):
        return (sender or self.sender).submit(
            nonce=NONCE, principal="asserted-only",
            action="akdc-confirm-fixture", operation_digest=DIGEST,
        )

    def identifiers(self):
        with closing(self.sender._connect()) as conn:
            row = conn.execute("SELECT tag, payload FROM outbox ORDER BY rowid LIMIT 1").fetchone()
        self.assertIsNotNone(row)
        return row

    def request(self, key, payload, **kw):
        return post_fixture(self.port, key, payload, **kw)

    def test_real_tcp_loopback_first_and_duplicate(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload), (200, {
            "status": "FIRST_RECEIVER_MARKER", "authority": "NOT_GRANTED"
        }))
        self.assertEqual(self.request(key, payload)[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_lost_http_ack_after_receiver_commit_then_sender_redrive(self):
        self.enqueue()
        self.assertEqual(
            deliver_over_loopback(self.sender, self.port, drop_reply=True), "ACK_UNKNOWN_PENDING"
        )
        self.assertEqual(self.receiver.counts(), (1, 1))
        self.assertEqual(self.sender.counts(), (1, 1, 0))
        self.assertEqual(
            deliver_over_loopback(self.sender, self.port, epoch="fixture-epoch-b"),
            "DUPLICATE_RECEIVER_MARKER"
        )
        self.assertEqual(self.sender.counts(), (1, 0, 1))
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_receiver_restart_still_deduplicates(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload)[1]["status"], "FIRST_RECEIVER_MARKER")
        self.stop_server()
        self.start_server()
        self.assertEqual(self.request(key, payload)[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_eight_parallel_http_requests_one_first(self):
        self.enqueue()
        key, payload = self.identifiers()
        with ThreadPoolExecutor(max_workers=8) as pool:
            replies = list(pool.map(lambda _: self.request(key, payload), range(8)))
        self.assertEqual([x[0] for x in replies], [200] * 8)
        statuses = [x[1]["status"] for x in replies]
        self.assertEqual(statuses.count("FIRST_RECEIVER_MARKER"), 1)
        self.assertEqual(statuses.count("DUPLICATE_RECEIVER_MARKER"), 7)
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_fixture_signing_key_epoch_changes_without_changing_idempotency_tag(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload, epoch="fixture-epoch-a")[0], 200)
        self.assertEqual(
            self.request(key, payload, epoch="fixture-epoch-b")[1]["status"], "DUPLICATE_RECEIVER_MARKER"
        )
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_unknown_fixture_epoch_refused(self):
        self.enqueue()
        key, payload = self.identifiers()
        status, reply = self.request(key, payload, epoch="revoked-epoch", secret=b"not-trusted")
        self.assertEqual((status, reply["status"]), (401, "FIXTURE_AUTH_REFUSED"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_wrong_signature_refused(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload, secret=b"different-test-key")[0], 401)
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_signed_body_tamper_refused(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload, tamper_after_sign=True)[0], 401)
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_unsigned_http_request_refused(self):
        self.enqueue()
        key, payload = self.identifiers()
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=6)
        try:
            connection.request(
                "POST", PATH, canonical_body(key, payload),
                headers={"Content-Type": "application/json"}
            )
            result = connection.getresponse()
            self.assertEqual(result.status, 401)
            result.read()
        finally:
            connection.close()
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_conflicting_payload_same_authenticated_key_refused(self):
        self.enqueue()
        key, payload = self.identifiers()
        self.assertEqual(self.request(key, payload)[0], 200)
        status, reply = self.request(key, "d" * 64)
        self.assertEqual((status, reply["status"]), (400, "INVALID_FIXTURE"))
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_malformed_idempotency_key_refused_even_with_valid_fixture_mac(self):
        self.enqueue()
        _, payload = self.identifiers()
        status, reply = self.request("bad-id", payload)
        self.assertEqual((status, reply["status"]), (400, "INVALID_FIXTURE"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_loopback_get_not_accepted_as_commit(self):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=6)
        try:
            connection.request("GET", PATH)
            response = connection.getresponse()
            self.assertEqual(response.status, 405)
            response.read()
        finally:
            connection.close()
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_two_sender_db_same_stable_tag_deduplicates(self):
        self.enqueue()
        self.assertEqual(deliver_over_loopback(self.sender, self.port), "FIRST_RECEIVER_MARKER")
        second = SQLiteOutboxResearch(str(Path(self.tmp.name) / "other_sender.sqlite"), KEY)
        self.enqueue(second)
        self.assertEqual(deliver_over_loopback(second, self.port), "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_rotated_sender_receipt_key_can_duplicate_receiver_effect(self):
        self.enqueue()
        self.assertEqual(deliver_over_loopback(self.sender, self.port), "FIRST_RECEIVER_MARKER")
        rotated = SQLiteOutboxResearch(self.sender_file, b"DIFFERENT-KEY-WITH-NO-PRODUCTION-CUSTODY-01")
        self.enqueue(rotated)
        self.assertEqual(deliver_over_loopback(rotated, self.port), "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (2, 2))  # bounded negative control

    def test_different_uri_is_not_ingress(self):
        self.enqueue()
        key, payload = self.identifiers()
        data = canonical_body(key, payload)
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=6)
        try:
            connection.request(
                "POST", "/unrecognized", data,
                headers={
                    "Content-Type": "application/json",
                    "X-AKDC-Fixture-Epoch": "fixture-epoch-a",
                    "X-AKDC-Fixture-MAC": mac(data, b"PUBLIC-FIXTURE-KEY-A-NOT-A-REAL-SECRET-2026")
                }
            )
            response = connection.getresponse()
            self.assertEqual(response.status, 404)
            response.read()
        finally:
            connection.close()
        self.assertEqual(self.receiver.counts(), (0, 0))


if __name__ == "__main__":
    unittest.main()
