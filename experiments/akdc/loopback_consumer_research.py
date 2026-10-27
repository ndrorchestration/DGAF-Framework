"""AKDC Gate 16: real loopback TCP/HTTP receiver with fixture-only HMAC.

Two separate SQLite files and separate OS processes; receiver-local atomic
synthetic marker only. The published demo keys below are NOT credentials,
real identity authentication, TLS, or protection against local attackers.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import http.client
import json
import re
import socket
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from experiments.akdc.idempotent_consumer_research import ConsumerRefusal, SQLiteIdempotentConsumerResearch
from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch

PATH = "/v1/research/idempotent-receipt"
DOMAIN = b"AKDC-GATE16-FIXTURE-POST-V1\n"
FIXTURE_KEYS = {
    "fixture-epoch-a": b"PUBLIC-FIXTURE-KEY-A-NOT-A-REAL-SECRET-2026",
    "fixture-epoch-b": b"PUBLIC-FIXTURE-KEY-B-NOT-A-REAL-SECRET-2026",
}
MAX_BODY = 2048


def canonical_body(key: str, payload: str, *, drop_reply: bool = False) -> bytes:
    obj = {"idempotency_key": key, "payload_tag": payload, "drop_reply": drop_reply}
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("ascii")


def mac(data: bytes, secret: bytes) -> str:
    return hmac.new(secret, DOMAIN + b"POST\n" + PATH.encode("ascii") + b"\n" + data, hashlib.sha256).hexdigest()


def post_fixture(
    port: int, key: str, payload: str, *, epoch: str = "fixture-epoch-a",
    secret: bytes | None = None, drop_reply: bool = False,
    tamper_after_sign: bool = False,
) -> tuple[int, dict[str, Any]]:
    if type(port) is not int or not 0 < port < 65536:
        raise ValueError("local server port required")
    body = canonical_body(key, payload, drop_reply=drop_reply)
    sign_key = FIXTURE_KEYS[epoch] if secret is None else secret
    digest = mac(body, sign_key)
    if tamper_after_sign:
        body = body.replace(payload.encode("ascii"), ("f" * 64).encode("ascii"))
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=6)
    try:
        conn.request(
            "POST", PATH, body=body,
            headers={
                "Content-Type": "application/json",
                "X-AKDC-Fixture-Epoch": epoch,
                "X-AKDC-Fixture-MAC": digest,
            },
        )
        response = conn.getresponse()
        text = response.read()
        return response.status, json.loads(text)
    finally:
        conn.close()


class FixtureHTTPHandler(BaseHTTPRequestHandler):
    """Only configured 127.0.0.1 network listener; no production authz."""

    server: ThreadingHTTPServer

    def log_message(self, format: str, *args: Any) -> None:
        # Do not write input, HMAC headers or body into server logs.
        return

    def _respond(self, status: int, result: str) -> None:
        body = json.dumps(
            {"status": result, "authority": "NOT_GRANTED"}, separators=(",", ":")
        ).encode("ascii")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self._respond(405, "METHOD_NOT_ALLOWED")

    def do_POST(self) -> None:
        if self.path != PATH:
            self._respond(404, "UNKNOWN_PATH")
            return
        if self.headers.get("Transfer-Encoding") is not None:
            self._respond(400, "CHUNKED_NOT_SUPPORTED")
            return
        length = self.headers.get("Content-Length", "")
        if not re.fullmatch(r"[0-9]{1,5}", length):
            self._respond(411, "CONTENT_LENGTH_REQUIRED")
            return
        count = int(length)
        if count > MAX_BODY:
            self._respond(413, "BODY_TOO_LARGE")
            return
        if self.headers.get("Content-Type") != "application/json":
            self._respond(415, "UNSUPPORTED_MEDIA_TYPE")
            return
        body = self.rfile.read(count)
        epoch = self.headers.get("X-AKDC-Fixture-Epoch", "")
        secret = FIXTURE_KEYS.get(epoch)
        supplied = self.headers.get("X-AKDC-Fixture-MAC", "")
        if secret is None or not re.fullmatch(r"[0-9a-f]{64}", supplied):
            self._respond(401, "FIXTURE_AUTH_REFUSED")
            return
        if not hmac.compare_digest(supplied, mac(body, secret)):
            self._respond(401, "FIXTURE_AUTH_REFUSED")
            return
        try:
            obj = json.loads(body)
            if type(obj) is not dict or set(obj) != {"idempotency_key", "payload_tag", "drop_reply"}:
                raise ValueError("invalid fixture shape")
            if type(obj["drop_reply"]) is not bool:
                raise ValueError("drop_reply must be bool")
            receiver: SQLiteIdempotentConsumerResearch = self.server.receiver  # type: ignore[attr-defined]
            outcome = receiver.accept(key=obj["idempotency_key"], payload=obj["payload_tag"])
        except (ValueError, TypeError, ConsumerRefusal, UnicodeDecodeError):
            self._respond(400, "INVALID_FIXTURE")
            return
        if obj["drop_reply"]:
            # Deliberately simulate a lost ACK AFTER receiver COMMIT.
            self.close_connection = True
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return
        self._respond(200, outcome)


def run_server(db: str) -> None:
    receiver = SQLiteIdempotentConsumerResearch(db)
    with ThreadingHTTPServer(("127.0.0.1", 0), FixtureHTTPHandler) as server:
        server.receiver = receiver  # type: ignore[attr-defined]
        print(json.dumps({"port": server.server_port, "fixture_only": True}), flush=True)
        server.serve_forever(poll_interval=0.05)


def deliver_over_loopback(
    sender: SQLiteOutboxResearch, port: int, *, epoch: str = "fixture-epoch-a",
    drop_reply: bool = False,
) -> str:
    """Sender ACK intentionally separate from receiver COMMIT, for crash testing."""
    with closing(sender._connect()) as conn:
        try:
            conn.execute("BEGIN IMMEDIATE")
            sender._check_schema(conn)
            row = conn.execute(
                "SELECT tag, payload FROM outbox WHERE status='PENDING' ORDER BY rowid LIMIT 1"
            ).fetchone()
            if row is None:
                conn.execute("COMMIT")
                return "NO_PENDING"
            tag, payload = row
            try:
                status, response = post_fixture(port, tag, payload, epoch=epoch, drop_reply=drop_reply)
            except (OSError, http.client.HTTPException):
                conn.execute("ROLLBACK")
                return "ACK_UNKNOWN_PENDING"
            if status != 200 or response.get("authority") != "NOT_GRANTED":
                raise ConsumerRefusal("fixture response refused or invalid")
            if response.get("status") not in ("FIRST_RECEIVER_MARKER", "DUPLICATE_RECEIVER_MARKER"):
                raise ConsumerRefusal("unrecognized receiver state")
            conn.execute("INSERT INTO local_effect VALUES (?, 'SYNTHETIC_DB_MARKER')", (tag,))
            conn.execute("UPDATE receipt SET status='APPLIED' WHERE tag=?", (tag,))
            conn.execute("UPDATE outbox SET status='APPLIED' WHERE tag=?", (tag,))
            conn.execute("COMMIT")
            return response["status"]
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 16 loopback-only synthetic receiver")
    parser.add_argument("--receiver-db", required=True)
    args = parser.parse_args()
    run_server(args.receiver_db)


if __name__ == "__main__":
    main()
