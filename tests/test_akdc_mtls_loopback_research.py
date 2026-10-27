"""Gate 17: real TLS 1.3 mutual certificate exchange, synthetic localhost only.

Leaf private keys are generated in temp files at test execution, never saved
in the repository or CI artifacts. Trusting an ephemeral fixture CA does not
authenticate a production identity or grant operation-specific authorization.
"""

from __future__ import annotations

import json
import os
import select
import ssl
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

from experiments.akdc.idempotent_consumer_research import (
    SQLiteIdempotentConsumerResearch,
)
from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch
from experiments.akdc.mtls_loopback_research import deliver_mtls, post_mtls

KEY = b"AKDC-TEST-OUTBOX-KEY-NOT-SECRET-00000001"
NONCE = "a" * 32
DIGEST = "b" * 64


class MutualTLSReceiverTests(unittest.TestCase):
    cert_tmp: tempfile.TemporaryDirectory
    certs: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.cert_tmp = tempfile.TemporaryDirectory(prefix="akdc-ephemeral-certs-")
        cls.certs = Path(cls.cert_tmp.name)

        def run(*args: str) -> None:
            subprocess.run(["openssl", *args], capture_output=True, check=True, timeout=12)

        def make_ca(name: str) -> None:
            run(
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-sha256",
                "-days",
                "2",
                "-subj",
                "/CN=AKDC-TEST-ONLY-" + name,
                "-keyout",
                str(cls.certs / (name + ".key")),
                "-out",
                str(cls.certs / (name + ".pem")),
                "-addext",
                "basicConstraints=critical,CA:TRUE",
                "-addext",
                "keyUsage=critical,keyCertSign,cRLSign",
            )

        def make_leaf(name: str, ca_name: str, eku: str, san: str = "") -> None:
            run(
                "req",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-sha256",
                "-subj",
                "/CN=AKDC-TEST-ONLY-" + name,
                "-keyout",
                str(cls.certs / (name + ".key")),
                "-out",
                str(cls.certs / (name + ".csr")),
            )
            ext = cls.certs / (name + ".ext")
            ext.write_text(
                "basicConstraints=critical,CA:FALSE\n"
                "keyUsage=digitalSignature,keyEncipherment\n"
                "extendedKeyUsage=" + eku + "\n" + san,
                encoding="ascii",
            )
            run(
                "x509",
                "-req",
                "-in",
                str(cls.certs / (name + ".csr")),
                "-CA",
                str(cls.certs / (ca_name + ".pem")),
                "-CAkey",
                str(cls.certs / (ca_name + ".key")),
                "-CAcreateserial",
                "-out",
                str(cls.certs / (name + ".pem")),
                "-days",
                "2",
                "-sha256",
                "-extfile",
                str(ext),
            )

        make_ca("trusted-ca")
        make_ca("rogue-ca")
        make_leaf("server", "trusted-ca", "serverAuth", "subjectAltName=IP:127.0.0.1\n")
        make_leaf("client-a", "trusted-ca", "clientAuth")
        make_leaf("client-b", "trusted-ca", "clientAuth")
        make_leaf("rogue-client", "rogue-ca", "clientAuth")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cert_tmp.cleanup()

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.sender_file = str(Path(self.tmp.name) / "sender.sqlite")
        self.receiver_file = str(Path(self.tmp.name) / "receiver.sqlite")
        self.sender = SQLiteOutboxResearch(self.sender_file, KEY)
        self.receiver = SQLiteIdempotentConsumerResearch(self.receiver_file)
        self.proc: subprocess.Popen[str] | None = None
        self.port = 0
        self.start_server()

    def tearDown(self) -> None:
        self.stop_server()
        self.tmp.cleanup()

    def cert(self, name: str, extension: str = ".pem") -> str:
        return str(self.certs / (name + extension))

    def start_server(self) -> None:
        self.proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "experiments.akdc.mtls_loopback_research",
                "--receiver-db",
                self.receiver_file,
                "--ca",
                self.cert("trusted-ca"),
                "--cert",
                self.cert("server"),
                "--key",
                self.cert("server", ".key"),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=dict(os.environ),
            bufsize=1,
        )
        stdout = self.proc.stdout
        if stdout is None:
            raise AssertionError("no TLS fixture stdout")
        readable, _, _ = select.select([stdout], [], [], 10)
        if not readable:
            self.stop_server()
            raise AssertionError("TLS fixture failed to become ready")
        info = json.loads(stdout.readline())
        self.assertEqual(info["tls"], "TLSv1.3")
        self.assertEqual(info["client_cert"], "REQUIRED")
        self.port = int(info["port"])

    def stop_server(self) -> None:
        proc = self.proc
        if proc is None:
            return
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=4)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=4)
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        self.proc = None

    def enqueue(self, sender: SQLiteOutboxResearch | None = None) -> None:
        result = (sender or self.sender).submit(
            nonce=NONCE, principal="asserted-only", action="akdc-confirm-fixture", operation_digest=DIGEST
        )
        self.assertEqual(result, "ENQUEUED")

    def identifiers(self) -> tuple[str, str]:
        with closing(self.sender._connect()) as conn:
            row = conn.execute("SELECT tag, payload FROM outbox ORDER BY rowid LIMIT 1").fetchone()
        self.assertIsNotNone(row)
        return row

    def request(self, key: str, payload: str, client: str = "client-a", **options):
        return post_mtls(
            self.port,
            key,
            payload,
            ca=self.cert("trusted-ca"),
            cert=self.cert(client),
            private_key=self.cert(client, ".key"),
            **options,
        )

    def deliver(self, sender: SQLiteOutboxResearch | None = None, client: str = "client-a", **opts):
        return deliver_mtls(
            sender or self.sender,
            self.port,
            ca=self.cert("trusted-ca"),
            cert=self.cert(client),
            private_key=self.cert(client, ".key"),
            **opts,
        )

    def test_real_mtls_first_and_duplicate_receiver_marker(self):
        self.enqueue()
        tag, payload = self.identifiers()
        self.assertEqual(self.request(tag, payload)[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.request(tag, payload)[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_dropped_tls_reply_after_commit_retries_and_acks(self):
        self.enqueue()
        self.assertEqual(self.deliver(drop_reply=True), "ACK_UNKNOWN_PENDING")
        self.assertEqual(self.sender.counts(), (1, 1, 0))
        self.assertEqual(self.receiver.counts(), (1, 1))
        self.assertEqual(self.deliver(epoch="fixture-epoch-b", client="client-b"), "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.sender.counts(), (1, 0, 1))
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_receiver_restart_preserves_marker(self):
        self.enqueue()
        tag, payload = self.identifiers()
        self.assertEqual(self.request(tag, payload)[1]["status"], "FIRST_RECEIVER_MARKER")
        self.stop_server()
        self.start_server()
        self.assertEqual(self.request(tag, payload)[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_eight_parallel_mtls_calls_one_first(self):
        self.enqueue()
        tag, payload = self.identifiers()
        with ThreadPoolExecutor(max_workers=8) as executor:
            outcomes = list(executor.map(lambda _: self.request(tag, payload), range(8)))
        self.assertTrue(all(x[0] == 200 for x in outcomes))
        values = [x[1]["status"] for x in outcomes]
        self.assertEqual(values.count("FIRST_RECEIVER_MARKER"), 1)
        self.assertEqual(values.count("DUPLICATE_RECEIVER_MARKER"), 7)
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_missing_client_certificate_denied_at_tls(self):
        self.enqueue()
        tag, payload = self.identifiers()
        with self.assertRaises((ssl.SSLError, OSError)):
            post_mtls(self.port, tag, payload, ca=self.cert("trusted-ca"), cert=None, private_key=None)
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_rogue_client_ca_denied_at_tls(self):
        self.enqueue()
        tag, payload = self.identifiers()
        with self.assertRaises((ssl.SSLError, OSError)):
            self.request(tag, payload, client="rogue-client")
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_wrong_server_trust_anchor_denied(self):
        self.enqueue()
        tag, payload = self.identifiers()
        with self.assertRaises((ssl.SSLError, OSError)):
            post_mtls(
                self.port,
                tag,
                payload,
                ca=self.cert("rogue-ca"),
                cert=self.cert("client-a"),
                private_key=self.cert("client-a", ".key"),
            )
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_server_hostname_mismatch_denied(self):
        self.enqueue()
        tag, payload = self.identifiers()
        with self.assertRaises((ssl.SSLError, OSError)):
            self.request(tag, payload, hostname="localhost")
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_valid_tls_cert_but_invalid_message_mac_denied(self):
        self.enqueue()
        tag, payload = self.identifiers()
        result = self.request(tag, payload, invalid_mac=True)
        self.assertEqual(result[0], 401)
        self.assertEqual(result[1]["status"], "FIXTURE_AUTH_REFUSED")
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_two_trusted_client_certs_same_claim_negative_control(self):
        self.enqueue()
        tag, payload = self.identifiers()
        self.assertEqual(self.request(tag, payload, client="client-a")[0], 200)
        self.assertEqual(self.request(tag, payload, client="client-b")[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        # Both unrelated test identities are admitted: no per-cert authorization.
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_sender_tag_key_rotation_not_fixed_by_mutual_tls(self):
        self.enqueue()
        self.assertEqual(self.deliver(), "FIRST_RECEIVER_MARKER")
        rotated = SQLiteOutboxResearch(self.sender_file, b"DIFFERENT-KEY-WITH-NO-PRODUCTION-CUSTODY-01")
        self.enqueue(rotated)
        self.assertEqual(self.deliver(sender=rotated, client="client-b"), "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (2, 2))


if __name__ == "__main__":
    unittest.main()
