"""Gate 18: explicitly mapped ephemeral mTLS certificate -> synthetic operation scope.

CA trust alone is insufficient. The receiver rejects valid CA-trusted but
unlisted certificates, cross-principal claims, and out-of-scope actions BEFORE
a receiver-local SQLite write. Stable idempotency tags never depend on either
the TLS signing certificate or the sender's independently rotated HMAC key.

Research fixture only: no external CA custody, real user identity, delegation,
consent, real external effect, revocation service or production authorization.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import re
import socket
import ssl
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from experiments.akdc.idempotent_consumer_research import (
    ConsumerRefusal,
    SQLiteIdempotentConsumerResearch,
)
from experiments.akdc.loopback_consumer_research import FixtureHTTPHandler
from experiments.akdc.mtls_loopback_research import client_context

PATH = "/v1/research/cert-bound-marker"
MAX_BODY = 1024
ACTION = "akdc-confirm-fixture"


def stable_operation_key(principal: str, action: str, operation_id: str) -> str:
    """Hash canonical scoped identity; not a secret and not authorization."""
    if not re.fullmatch(r"fixture-[a-z]{1,24}", principal):
        raise ValueError("bad asserted synthetic principal")
    if action != ACTION or not re.fullmatch(r"[0-9a-f]{32}", operation_id):
        raise ValueError("bad fixture action or operation ID")
    encoded = json.dumps(
        ["AKDC-STABLE-OPERATION-ID-V1", principal, action, operation_id],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def certificate_fingerprint(pem_path: str) -> str:
    pem = Path(pem_path).read_text(encoding="ascii")
    return hashlib.sha256(ssl.PEM_cert_to_DER_cert(pem)).hexdigest()


def read_fixture_policy(path: str) -> dict[str, tuple[str, frozenset[str]]]:
    """Read temporary allowlist at server startup, fail closed on bad configuration."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if type(raw) is not dict or not raw:
        raise ValueError("fixture cert policy must be nonempty object")
    parsed = {}
    for fingerprint, value in raw.items():
        if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            raise ValueError("bad fixture certificate fingerprint")
        if type(value) is not dict or set(value) != {"principal", "actions"}:
            raise ValueError("bad fixture policy binding")
        principal, actions = value["principal"], value["actions"]
        if type(principal) is not str or not re.fullmatch(r"fixture-[a-z]{1,24}", principal):
            raise ValueError("bad fixture principal")
        if type(actions) is not list or not actions or any(type(x) is not str for x in actions):
            raise ValueError("bad fixture actions")
        if len(set(actions)) != len(actions):
            raise ValueError("duplicate fixture action")
        if not set(actions).issubset({ACTION, "akdc-observe-fixture"}):
            raise ValueError("unknown test-only action")
        parsed[fingerprint] = (principal, frozenset(actions))
    return parsed


class BoundCertificateHandler(FixtureHTTPHandler):
    """Only a synthetic receiver marker; certificate policy is not real authz."""

    def do_POST(self) -> None:
        if self.path != PATH:
            self._respond(404, "UNKNOWN_PATH")
            return
        length = self.headers.get("Content-Length", "")
        if not re.fullmatch(r"[0-9]{1,4}", length) or self.headers.get("Transfer-Encoding"):
            self._respond(400, "BAD_FRAMING")
            return
        if int(length) > MAX_BODY or self.headers.get("Content-Type") != "application/json":
            self._respond(400, "BAD_CONTENT_TYPE_OR_SIZE")
            return
        if not isinstance(self.connection, ssl.SSLSocket):
            self._respond(403, "CLIENT_IDENTITY_REFUSED")
            return
        certificate = self.connection.getpeercert(binary_form=True)
        if not certificate:
            self._respond(403, "CLIENT_IDENTITY_REFUSED")
            return
        fingerprint = hashlib.sha256(certificate).hexdigest()
        policy: dict[str, tuple[str, frozenset[str]]] = self.server.cert_policy  # type: ignore[attr-defined]
        allowed = policy.get(fingerprint)
        if allowed is None:
            self._respond(403, "CLIENT_IDENTITY_REFUSED")
            return
        try:
            body = self.rfile.read(int(length))
            data = json.loads(body)
            if type(data) is not dict or set(data) != {
                "principal",
                "action",
                "operation_id",
                "payload_tag",
                "drop_reply",
            }:
                raise ValueError("bad test object")
            if type(data["drop_reply"]) is not bool:
                raise ValueError("bad drop flag")
            principal, actions = allowed
            if data["principal"] != principal or data["action"] not in actions:
                self._respond(403, "OPERATION_SCOPE_REFUSED")
                return
            key = stable_operation_key(principal, data["action"], data["operation_id"])
            payload = data["payload_tag"]
            receiver: SQLiteIdempotentConsumerResearch = self.server.receiver  # type: ignore[attr-defined]
            result = receiver.accept(key=key, payload=payload)
        except (ValueError, TypeError, ConsumerRefusal, UnicodeDecodeError):
            self._respond(400, "INVALID_SYNTHETIC_OPERATION")
            return
        if data["drop_reply"]:
            self.close_connection = True
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return
        self._respond(200, result)


def run_bound_server(receiver_db: str, ca: str, certificate: str, key: str, policy_path: str) -> None:
    policy = read_fixture_policy(policy_path)
    receiver = SQLiteIdempotentConsumerResearch(receiver_db)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_3
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_cert_chain(certfile=certificate, keyfile=key)
    ctx.load_verify_locations(cafile=ca)
    with ThreadingHTTPServer(("127.0.0.1", 0), BoundCertificateHandler) as server:
        server.receiver = receiver  # type: ignore[attr-defined]
        server.cert_policy = policy  # type: ignore[attr-defined]
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        print(json.dumps({"port": server.server_port, "test_only": True}), flush=True)
        server.serve_forever(poll_interval=0.05)


def post_bound_fixture(
    port: int,
    ca: str,
    certificate: str | None,
    key: str | None,
    *,
    principal: str,
    action: str = ACTION,
    operation_id: str,
    payload_tag: str,
    drop_reply: bool = False,
) -> tuple[int, dict[str, Any]]:
    """TLS client sends a synthetic scoped operation; no real dispatch."""
    payload = json.dumps(
        {
            "principal": principal,
            "action": action,
            "operation_id": operation_id,
            "payload_tag": payload_tag,
            "drop_reply": drop_reply,
        },
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    ctx = client_context(ca, certificate, key)
    conn = http.client.HTTPSConnection("127.0.0.1", port, context=ctx, timeout=6)
    try:
        conn.request("POST", PATH, body=payload, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        return response.status, json.loads(response.read())
    finally:
        conn.close()


def main() -> None:
    p = argparse.ArgumentParser(description="ephemeral CA fixture-only certificate-bound receiver")
    p.add_argument("--receiver-db", required=True)
    p.add_argument("--ca", required=True)
    p.add_argument("--cert", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--policy", required=True)
    args = p.parse_args()
    run_bound_server(args.receiver_db, args.ca, args.cert, args.key, args.policy)


if __name__ == "__main__":
    main()
