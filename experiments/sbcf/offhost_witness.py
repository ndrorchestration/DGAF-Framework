"""Off-host monotonic witness research prototype.

The service separates checkpoint state from the SBCF client process and requires
HTTPS plus a bearer token. It does not establish independent custody, production
authorization, or protection against compromise of the witness host.
"""

from __future__ import annotations

import hmac
import http.client
import json
import sqlite3
import ssl
import time
from contextlib import closing
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, cast
from urllib.parse import parse_qs, urlencode, urlparse

MAX_BODY_BYTES = 8192


@dataclass(frozen=True)
class RemoteCheckpoint:
    source: str
    run: str
    policy: str
    sequence: int
    checkpoint_id: str


@dataclass(frozen=True)
class WriterLease:
    """Server-side bounded authority for one off-host witness writer."""

    token: str
    source: str
    run: str
    policy: str
    min_sequence: int
    max_sequence: int
    generation: int
    expires_at: float

    def allows(self, record: RemoteCheckpoint, *, now: float) -> bool:
        return (
            now < self.expires_at
            and record.source == self.source
            and record.run == self.run
            and record.policy == self.policy
            and self.min_sequence <= record.sequence <= self.max_sequence
        )


def _valid_writer_lease(lease: WriterLease) -> bool:
    return (
        all(isinstance(value, str) and value for value in (lease.token, lease.source, lease.run, lease.policy))
        and type(lease.min_sequence) is int
        and type(lease.max_sequence) is int
        and lease.min_sequence >= 0
        and lease.max_sequence >= lease.min_sequence
        and type(lease.generation) is int
        and lease.generation >= 0
        and isinstance(lease.expires_at, (int, float))
        and not isinstance(lease.expires_at, bool)
        and lease.expires_at > 0
    )


def _valid_checkpoint(record: RemoteCheckpoint) -> bool:
    return (
        all(
            isinstance(value, str) and value
            for value in (record.source, record.run, record.policy, record.checkpoint_id)
        )
        and type(record.sequence) is int
        and record.sequence >= 0
    )


class WitnessStore:
    """Monotonic SQLite checkpoint store intended to live on another host."""

    def __init__(self, path: str | Path):
        self.path = str(Path(path).resolve())
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS checkpoint ("
                "source TEXT NOT NULL, run TEXT NOT NULL, policy TEXT NOT NULL, "
                "sequence INTEGER NOT NULL, checkpoint_id TEXT NOT NULL, "
                "PRIMARY KEY(source, run), UNIQUE(checkpoint_id))"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS writer_generation ("
                "source TEXT NOT NULL, run TEXT NOT NULL, policy TEXT NOT NULL, "
                "generation INTEGER NOT NULL, "
                "PRIMARY KEY(source, run, policy))"
            )

    def advance(self, record: RemoteCheckpoint, *, writer_generation: int | None = None) -> bool:
        if not _valid_checkpoint(record):
            return False
        if writer_generation is not None and (type(writer_generation) is not int or writer_generation < 0):
            return False
        try:
            with closing(sqlite3.connect(self.path, timeout=10, isolation_level=None)) as db:
                db.execute("BEGIN IMMEDIATE")
                if writer_generation is not None:
                    required_row = db.execute(
                        "SELECT generation FROM writer_generation WHERE source=? AND run=? AND policy=?",
                        (record.source, record.run, record.policy),
                    ).fetchone()
                    required_generation = 0 if required_row is None else int(required_row[0])
                    if writer_generation < required_generation:
                        db.rollback()
                        return False
                current = db.execute(
                    "SELECT policy, sequence FROM checkpoint WHERE source=? AND run=?",
                    (record.source, record.run),
                ).fetchone()
                if current is not None:
                    if current[0] != record.policy or record.sequence <= current[1]:
                        db.rollback()
                        return False
                    db.execute(
                        "UPDATE checkpoint SET sequence=?, checkpoint_id=? WHERE source=? AND run=?",
                        (record.sequence, record.checkpoint_id, record.source, record.run),
                    )
                else:
                    db.execute(
                        "INSERT INTO checkpoint(source,run,policy,sequence,checkpoint_id) VALUES (?,?,?,?,?)",
                        (
                            record.source,
                            record.run,
                            record.policy,
                            record.sequence,
                            record.checkpoint_id,
                        ),
                    )
                db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def required_writer_generation(self, source: str, run: str, policy: str) -> int | None:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return None
        with closing(sqlite3.connect(self.path, timeout=3)) as db:
            row = db.execute(
                "SELECT generation FROM writer_generation WHERE source=? AND run=? AND policy=?",
                (source, run, policy),
            ).fetchone()
        return 0 if row is None else int(row[0])

    def advance_writer_generation(self, source: str, run: str, policy: str, generation: int) -> bool:
        if not all(isinstance(value, str) and value for value in (source, run, policy)):
            return False
        if type(generation) is not int or generation <= 0:
            return False
        try:
            with closing(sqlite3.connect(self.path, timeout=10, isolation_level=None)) as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute(
                    "SELECT generation FROM writer_generation WHERE source=? AND run=? AND policy=?",
                    (source, run, policy),
                ).fetchone()
                current_generation = 0 if row is None else int(row[0])
                if generation <= current_generation:
                    db.rollback()
                    return False
                db.execute(
                    "INSERT INTO writer_generation(source,run,policy,generation) VALUES (?,?,?,?) "
                    "ON CONFLICT(source,run,policy) DO UPDATE SET generation=excluded.generation",
                    (source, run, policy, generation),
                )
                db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def read(self, source: str, run: str) -> RemoteCheckpoint | None:
        if not source or not run:
            return None
        with closing(sqlite3.connect(self.path, timeout=3)) as db:
            row = db.execute(
                "SELECT source,run,policy,sequence,checkpoint_id FROM checkpoint WHERE source=? AND run=?",
                (source, run),
            ).fetchone()
        return None if row is None else RemoteCheckpoint(*row)


class WitnessHTTPServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        store: WitnessStore,
        *,
        read_token: str,
        writer_leases: tuple[WriterLease, ...],
        now_fn: Callable[[], float] = time.time,
        generation_floor_fn: Callable[[str, str, str], int | None] | None = None,
    ):
        if not read_token or not writer_leases:
            raise ValueError("witness read token and writer lease are required")
        if any(not _valid_writer_lease(lease) for lease in writer_leases):
            raise ValueError("invalid writer lease")
        writer_tokens = [lease.token for lease in writer_leases]
        if read_token in writer_tokens or len(set(writer_tokens)) != len(writer_tokens):
            raise ValueError("witness read/write credentials must be distinct")
        super().__init__(server_address, WitnessRequestHandler)
        self.store = store
        self.read_token = read_token
        self.writer_leases = writer_leases
        self.now_fn = now_fn
        self.generation_floor_fn = generation_floor_fn


class WitnessRequestHandler(BaseHTTPRequestHandler):
    server_version = "SBCF-Witness-Research/0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def _server(self) -> WitnessHTTPServer:
        return cast(WitnessHTTPServer, self.server)

    def _authorized(self, token: str) -> bool:
        supplied = self.headers.get("Authorization", "")
        expected = f"Bearer {token}"
        return hmac.compare_digest(supplied, expected)

    def _writer_lease(self) -> WriterLease | None:
        supplied = self.headers.get("Authorization", "")
        for lease in self._server().writer_leases:
            if hmac.compare_digest(supplied, f"Bearer {lease.token}"):
                return lease
        return None

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
        if parsed.path != "/v1/checkpoint":
            self._reply(404, {"status": "not_found"})
            return
        query = parse_qs(parsed.query, strict_parsing=False)
        source = query.get("source", [""])[0]
        run = query.get("run", [""])[0]
        record = self._server().store.read(source, run)
        if record is None:
            self._reply(404, {"status": "not_found"})
            return
        self._reply(200, {"status": "ok", "checkpoint": asdict(record)})

    def do_POST(self) -> None:  # noqa: N802
        lease = self._writer_lease()
        if lease is None:
            self._reply(401, {"status": "blocked"})
            return
        if self.path != "/v1/checkpoint":
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
            if not isinstance(payload, dict) or set(payload) != {
                "source",
                "run",
                "policy",
                "sequence",
                "checkpoint_id",
            }:
                raise ValueError("invalid fields")
            record = RemoteCheckpoint(**payload)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
            self._reply(400, {"status": "invalid"})
            return
        if not lease.allows(record, now=self._server().now_fn()):
            self._reply(403, {"status": "out_of_scope"})
            return
        floor_fn = self._server().generation_floor_fn
        if floor_fn is not None:
            floor = floor_fn(record.source, record.run, record.policy)
            if type(floor) is not int or floor < 0:
                self._reply(503, {"status": "generation_floor_unavailable"})
                return
            if lease.generation < floor:
                self._reply(409, {"status": "rejected"})
                return
        if not self._server().store.advance(record, writer_generation=lease.generation):
            self._reply(409, {"status": "rejected"})
            return
        self._reply(201, {"status": "accepted", "checkpoint": asdict(record)})


def make_https_server(
    host: str,
    port: int,
    *,
    store_path: str | Path,
    read_token: str,
    writer_leases: tuple[WriterLease, ...],
    certfile: str | Path,
    keyfile: str | Path,
    now_fn: Callable[[], float] = time.time,
    generation_floor_fn: Callable[[str, str, str], int | None] | None = None,
) -> WitnessHTTPServer:
    server = WitnessHTTPServer(
        (host, port),
        WitnessStore(store_path),
        read_token=read_token,
        writer_leases=writer_leases,
        now_fn=now_fn,
        generation_floor_fn=generation_floor_fn,
    )
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=str(certfile), keyfile=str(keyfile))
    server.socket = context.wrap_socket(server.socket, server_side=True)
    return server


class RemoteWitnessClient:
    """Fail-closed HTTPS client for an off-host checkpoint service."""

    def __init__(self, base_url: str, *, token: str, cafile: str | Path, timeout: float = 3.0):
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or not parsed.hostname or not token:
            raise ValueError("verified https witness endpoint and token required")
        if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
            raise ValueError("witness base URL must not contain path, query, or fragment")
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

    def advance(self, record: RemoteCheckpoint) -> bool:
        if not _valid_checkpoint(record):
            return False
        data = json.dumps(asdict(record), sort_keys=True, separators=(",", ":")).encode("utf-8")
        connection = self._connection()
        try:
            connection.request(
                "POST",
                "/v1/checkpoint",
                body=data,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            response.read()
            return response.status == 201
        except (http.client.HTTPException, TimeoutError, ssl.SSLError, OSError):
            return False
        finally:
            connection.close()

    def read(self, source: str, run: str) -> RemoteCheckpoint | None:
        if not source or not run:
            return None
        query = urlencode({"source": source, "run": run})
        connection = self._connection()
        try:
            connection.request(
                "GET",
                f"/v1/checkpoint?{query}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response = connection.getresponse()
            body = response.read()
            if response.status != 200:
                return None
            payload = json.loads(body)
            if not isinstance(payload, dict) or payload.get("status") != "ok":
                return None
            checkpoint = payload.get("checkpoint")
            if not isinstance(checkpoint, dict):
                return None
            record = RemoteCheckpoint(**checkpoint)
            return record if _valid_checkpoint(record) else None
        except (
            http.client.HTTPException,
            TimeoutError,
            ssl.SSLError,
            OSError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            return None
        finally:
            connection.close()
