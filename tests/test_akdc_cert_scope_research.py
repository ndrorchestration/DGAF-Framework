"""Gate 18: mTLS certificate-policy and operation-id invariants (test CA only)."""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import select
import ssl
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from experiments.akdc.cert_bound_receiver_research import (
    ACTION,
    certificate_fingerprint,
    post_bound_fixture,
    read_fixture_policy,
    stable_operation_key,
)
from experiments.akdc.idempotent_consumer_research import SQLiteIdempotentConsumerResearch
from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch

OP = "a" * 32
DIGEST = "b" * 64
SENDER_KEY_1 = b"AKDC-TEST-OUTBOX-KEY-NOT-SECRET-00000001"
SENDER_KEY_2 = b"DIFFERENT-KEY-WITH-NO-PRODUCTION-CUSTODY-01"


class BoundCertificateReceiverTests(unittest.TestCase):
    cert_tmp: tempfile.TemporaryDirectory
    certs: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.cert_tmp = tempfile.TemporaryDirectory(prefix="akdc-g18-ephemeral-certs-")
        cls.certs = Path(cls.cert_tmp.name)

        def openssl(*args: str) -> None:
            subprocess.run(["openssl", *args], timeout=12, capture_output=True, check=True)

        def ca(name: str) -> None:
            openssl(
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-days",
                "2",
                "-sha256",
                "-subj",
                "/CN=AKDC-SYNTHETIC-CA-" + name,
                "-keyout",
                str(cls.certs / (name + ".key")),
                "-out",
                str(cls.certs / (name + ".pem")),
                "-addext",
                "basicConstraints=critical,CA:TRUE",
                "-addext",
                "keyUsage=critical,keyCertSign,cRLSign",
            )

        def leaf(name: str, issuer: str, usage: str, san: str = "") -> None:
            openssl(
                "req",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-sha256",
                "-subj",
                "/CN=AKDC-SYNTHETIC-LEAF-" + name,
                "-keyout",
                str(cls.certs / (name + ".key")),
                "-out",
                str(cls.certs / (name + ".csr")),
            )
            ext = cls.certs / (name + ".ext")
            ext.write_text(
                "basicConstraints=critical,CA:FALSE\n"
                "keyUsage=digitalSignature,keyEncipherment\n"
                "extendedKeyUsage=" + usage + "\n" + san,
                encoding="ascii",
            )
            openssl(
                "x509",
                "-req",
                "-in",
                str(cls.certs / (name + ".csr")),
                "-CA",
                str(cls.certs / (issuer + ".pem")),
                "-CAkey",
                str(cls.certs / (issuer + ".key")),
                "-CAcreateserial",
                "-out",
                str(cls.certs / (name + ".pem")),
                "-days",
                "2",
                "-sha256",
                "-extfile",
                str(ext),
            )

        ca("trusted")
        ca("rogue")
        leaf("server", "trusted", "serverAuth", "subjectAltName=IP:127.0.0.1\n")
        for name in ("alpha", "alpha-rotated", "beta", "unlisted"):
            leaf(name, "trusted", "clientAuth")
        leaf("rogue-client", "rogue", "clientAuth")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cert_tmp.cleanup()

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.receiver_db = str(base / "receiver.sqlite")
        self.receiver = SQLiteIdempotentConsumerResearch(self.receiver_db)
        self.policy = base / "cert-policy.json"
        self.write_policy()
        self.process: subprocess.Popen[str] | None = None
        self.port = 0
        self.start()

    def tearDown(self) -> None:
        self.stop()
        self.tmp.cleanup()

    def cert(self, name: str, extension: str = ".pem") -> str:
        return str(self.certs / (name + extension))

    def write_policy(self, *, allow_alpha: bool = True) -> None:
        data = {
            certificate_fingerprint(self.cert("alpha-rotated")): {"principal": "fixture-alpha", "actions": [ACTION]},
            certificate_fingerprint(self.cert("beta")): {
                "principal": "fixture-beta",
                "actions": ["akdc-observe-fixture"],
            },
        }
        if allow_alpha:
            data[certificate_fingerprint(self.cert("alpha"))] = {"principal": "fixture-alpha", "actions": [ACTION]}
        self.policy.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")

    def start(self) -> None:
        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "experiments.akdc.cert_bound_receiver_research",
                "--receiver-db",
                self.receiver_db,
                "--policy",
                str(self.policy),
                "--ca",
                self.cert("trusted"),
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
        if self.process.stdout is None:
            raise AssertionError("no fixture subprocess pipe")
        readable, _, _ = select.select([self.process.stdout], [], [], 12)
        if not readable:
            self.stop()
            raise AssertionError("fixture policy process not ready")
        info = json.loads(self.process.stdout.readline())
        self.assertTrue(info["test_only"])
        self.port = int(info["port"])

    def stop(self) -> None:
        process = self.process
        if process is None:
            return
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=4)
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        self.process = None

    def request(
        self,
        client: str = "alpha",
        *,
        principal: str = "fixture-alpha",
        operation_id: str = OP,
        payload_tag: str = DIGEST,
        action: str = ACTION,
        drop_reply: bool = False,
    ) -> tuple[int, dict]:
        return post_bound_fixture(
            self.port,
            self.cert("trusted"),
            self.cert(client),
            self.cert(client, ".key"),
            principal=principal,
            action=action,
            operation_id=operation_id,
            payload_tag=payload_tag,
            drop_reply=drop_reply,
        )

    def test_bound_alpha_first_and_duplicate(self):
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.request()[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_rotated_certificate_stable_operation_identity(self):
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.request("alpha-rotated")[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_sender_hmac_rotation_does_not_change_explicit_operation_key(self):
        db = str(Path(self.tmp.name) / "sender.sqlite")
        left = SQLiteOutboxResearch(db, SENDER_KEY_1)
        right = SQLiteOutboxResearch(db, SENDER_KEY_2)
        assert left.submit(nonce=OP, principal="asserted-only", action=ACTION, operation_digest=DIGEST) == "ENQUEUED"
        assert right.submit(nonce=OP, principal="asserted-only", action=ACTION, operation_digest=DIGEST) == "ENQUEUED"
        self.assertEqual(left.counts(), (2, 2, 0))
        explicit = stable_operation_key("fixture-alpha", ACTION, OP)
        self.assertEqual(explicit, stable_operation_key("fixture-alpha", ACTION, OP))
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.request("alpha-rotated")[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))
        # This is only a receiver endpoint experiment; sender's separate receipts remain doubled.

    def test_other_ca_trusted_client_cannot_claim_alpha(self):
        code, result = self.request("beta")
        self.assertEqual((code, result["status"]), (403, "OPERATION_SCOPE_REFUSED"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_alpha_cannot_claim_beta(self):
        code, result = self.request("alpha", principal="fixture-beta")
        self.assertEqual((code, result["status"]), (403, "OPERATION_SCOPE_REFUSED"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_beta_client_lacks_allowed_method(self):
        code, result = self.request("beta", principal="fixture-beta")
        self.assertEqual((code, result["status"]), (403, "OPERATION_SCOPE_REFUSED"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_trusted_ca_but_unlisted_client_fails_policy(self):
        code, result = self.request("unlisted")
        self.assertEqual((code, result["status"]), (403, "CLIENT_IDENTITY_REFUSED"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_rogue_ca_client_is_rejected_at_tls_handshake(self):
        with self.assertRaises((ssl.SSLError, OSError)):
            self.request("rogue-client")
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_missing_client_cert_fails_tls(self):
        with self.assertRaises((ssl.SSLError, OSError)):
            post_bound_fixture(
                self.port,
                self.cert("trusted"),
                None,
                None,
                principal="fixture-alpha",
                operation_id=OP,
                payload_tag=DIGEST,
            )
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_payload_rebinding_same_scoped_id_refused(self):
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        code, result = self.request(payload_tag="c" * 64)
        self.assertEqual((code, result["status"]), (400, "INVALID_SYNTHETIC_OPERATION"))
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_eight_parallel_mtls_scoped_requests_one_first(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda _: self.request(), range(8)))
        self.assertEqual([x[0] for x in results], [200] * 8)
        statuses = [x[1]["status"] for x in results]
        self.assertEqual(statuses.count("FIRST_RECEIVER_MARKER"), 1)
        self.assertEqual(statuses.count("DUPLICATE_RECEIVER_MARKER"), 7)
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_drop_reply_then_rotated_cert_retry_is_duplicate(self):
        with self.assertRaises((http.client.HTTPException, OSError)):
            self.request(drop_reply=True)
        self.assertEqual(self.receiver.counts(), (1, 1))
        self.assertEqual(self.request("alpha-rotated")[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_static_policy_revocation_requires_server_reload(self):
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        self.stop()
        self.write_policy(allow_alpha=False)
        self.start()
        code, result = self.request()
        self.assertEqual((code, result["status"]), (403, "CLIENT_IDENTITY_REFUSED"))
        self.assertEqual(self.request("alpha-rotated")[1]["status"], "DUPLICATE_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (1, 1))

    def test_different_operation_id_is_new_scoped_marker(self):
        self.assertEqual(self.request()[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.request(operation_id="c" * 32)[1]["status"], "FIRST_RECEIVER_MARKER")
        self.assertEqual(self.receiver.counts(), (2, 2))

    def test_invalid_operation_id_fails_without_insert(self):
        code, result = self.request(operation_id="malformed")
        self.assertEqual((code, result["status"]), (400, "INVALID_SYNTHETIC_OPERATION"))
        self.assertEqual(self.receiver.counts(), (0, 0))

    def test_invalid_or_unversioned_policy_refused_before_start(self):
        self.assertTrue(read_fixture_policy(str(self.policy)))
        self.policy.write_text(json.dumps({"bad": {"principal": "fixture-alpha", "actions": [ACTION]}}))
        with self.assertRaises(ValueError):
            read_fixture_policy(str(self.policy))

    def test_certificate_fingerprints_are_distinct(self):
        self.assertNotEqual(
            certificate_fingerprint(self.cert("alpha")),
            certificate_fingerprint(self.cert("alpha-rotated")),
        )
        self.assertNotEqual(
            hashlib.sha256(b"fake").hexdigest(),
            certificate_fingerprint(self.cert("alpha")),
        )


if __name__ == "__main__":
    unittest.main()
