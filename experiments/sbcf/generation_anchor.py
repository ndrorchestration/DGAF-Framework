"""Separate HTTPS generation-floor service for SBCF research.

This service can separate writer-revocation generation state from the witness
database. It does not establish independent custody, production authorization,
or rollback-resistant storage.
"""

from __future__ import annotations

import hmac
import http.client
import json
import sqlite3
import ssl
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast
from urllib.parse import parse_qs, urlencode, urlparse

MAX_BODY_BYTES = 4096


class GenerationAnchorStore:
    """Monotonic generation floor intended to live outside the witness host."""

    def __init__(self, path: str | Path):
        self.path = str(Path(path).resolve())
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS generation_floor ("
                "source TEXT NOT NULL, run TEXT NOT NULL, policy TEXT NOT NULL, "
                "generation INTEGER NOT NULL, "
                "PRIMARY KEY(source, run, policy))"
            )

    def read(self, source: str, run: str, policy: str) -> int | None:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return None
        with closing(sqlite3.connect(self.path, timeout=3)) as db:
            row = db.execute(
                "SELECT generation FROM generation_floor WHERE source=? AND run=? AND policy=?",
                (source, run, policy),
            ).fetchone()
        return 0 if row is None else int(row[0])

    def advance(self, source: str, run: str, policy: str, generation: int) -> bool:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return False
        if type(generation) is not int or generation <= 0:
            return False
        try:
            with closing(sqlite3.connect(self.path, timeout=10, isolation_level=None)) as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute(
                    "SELECT generation FROM generation_floor WHERE source=? AND run=? AND policy=?",
                    (source, run, policy),
                ).fetchone()
                current = 0 if row is None else int(row[0])
                if generation <= current:
                    db.rollback()
                    return False
                db.execute(
                    "INSERT INTO generation_floor(source,run,policy,generation) VALUES (?,?,?,?) "
                    "ON CONFLICT(source,run,policy) DO UPDATE SET generation=excluded.generation",
                    (source, run, policy, generation),
                )
                db.commit()
            return True
        except sqlite3.IntegrityError:
            return False


class GenerationAnchorHTTPServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        store: GenerationAnchorStore,
        *,
        read_token: str,
        admin_token: str,
    ):
        if not read_token or not admin_token or read_token == admin_token:
            raise ValueError("distinct generation-anchor read/admin tokens are required")
        super().__init__(server_address, GenerationAnchorRequestHandler)
        self.store = store
        self.read_token = read_token
        self.admin_token = admin_token


class GenerationAnchorRequestHandler(BaseHTTPRequestHandler):
    server_version = "SBCF-Generation-Anchor-Research/0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def _server(self) -> GenerationAnchorHTTPServer:
        return cast(GenerationAnchorHTTPServer, self.server)

    def _authorized(self, token: str) -> bool:
        supplied = self.headers.get("Authorization", "")
        return hmac.compare_digest(supplied, f"Bearer {token}")

    def _reply(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if not self._authorized(self._server().read_token):
            self._reply(401, {"status": "blocked"})
            return
        parsed = urlparse(self.path)
        if parsed.path != "/v1/generation":
            self._reply(404, {"status": "not_found"})
            return
        query = parse_qs(parsed.query, strict_parsing=False)
        source = query.get("source", [""])[0]
        run = query.get("run", [""])[0]
        policy = query.get("policy", [""])[0]
        generation = self._server().store.read(source, run, policy)
        if generation is None:
            self._reply(400, {"status": "invalid"})
            return
        self._reply(200, {"status": "ok", "generation": generation})

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized(self._server().admin_token):
            self._reply(401, {"status": "blocked"})
            return
        if self.path != "/v1/generation":
            self._reply(404, {"status": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._reply(400, {"status": "invalid"})
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            self._reply(413, {"status": "invalid"})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict) or set(payload) != {"source", "run", "policy", "generation"}:
                raise ValueError("invalid fields")
            source = payload["source"]
            run = payload["run"]
            policy = payload["policy"]
            generation = payload["generation"]
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
            self._reply(400, {"status": "invalid"})
            return
        if not self._server().store.advance(source, run, policy, generation):
            self._reply(409, {"status": "rejected"})
            return
        self._reply(201, {"status": "accepted", "generation": generation})


def make_generation_anchor_https_server(
    host: str,
    port: int,
    *,
    store_path: str | Path,
    read_token: str,
    admin_token: str,
    certfile: str | Path,
    keyfile: str | Path,
) -> GenerationAnchorHTTPServer:
    server = GenerationAnchorHTTPServer(
        (host, port),
        GenerationAnchorStore(store_path),
        read_token=read_token,
        admin_token=admin_token,
    )
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=str(certfile), keyfile=str(keyfile))
    server.socket = context.wrap_socket(server.socket, server_side=True)
    return server


class RemoteGenerationAnchorClient:
    """Fail-closed HTTPS client for a generation-floor service."""

    def __init__(self, base_url: str, *, token: str, cafile: str | Path, timeout: float = 3.0):
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or not parsed.hostname or not token:
            raise ValueError("verified https generation anchor and token required")
        if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
            raise ValueError("generation-anchor base URL must not contain path, query, or fragment")
        self.host = parsed.hostname
        self.port = parsed.port or 443
        self.token = token
        self.timeout = timeout
        self.context = ssl.create_default_context(cafile=str(cafile))
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2

    def _connection(self) -> http.client.HTTPSConnection:
        return http.client.HTTPSConnection(
            self.host,
            self.port,
            timeout=self.timeout,
            context=self.context,
        )

    def required_generation(self, source: str, run: str, policy: str) -> int | None:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return None
        path = "/v1/generation?" + urlencode({"source": source, "run": run, "policy": policy})
        try:
            connection = self._connection()
            connection.request("GET", path, headers={"Authorization": f"Bearer {self.token}"})
            response = connection.getresponse()
            body = response.read(MAX_BODY_BYTES + 1)
            connection.close()
            if response.status != 200 or len(body) > MAX_BODY_BYTES:
                return None
            payload = json.loads(body)
            if not isinstance(payload, dict) or payload.get("status") != "ok":
                return None
            generation = payload.get("generation")
            if type(generation) is not int or generation < 0:
                return None
            return generation
        except (OSError, ssl.SSLError, http.client.HTTPException, json.JSONDecodeError):
            return None

    def advance_generation(self, source: str, run: str, policy: str, generation: int) -> bool:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return False
        if type(generation) is not int or generation <= 0:
            return False
        payload = json.dumps(
            {"source": source, "run": run, "policy": policy, "generation": generation},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            connection = self._connection()
            connection.request(
                "POST",
                "/v1/generation",
                body=payload,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                    "Content-Length": str(len(payload)),
                },
            )
            response = connection.getresponse()
            response.read(MAX_BODY_BYTES + 1)
            connection.close()
            return response.status == 201
        except (OSError, ssl.SSLError, http.client.HTTPException):
            return False
