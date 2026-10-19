"""Separate generation-floor contract tests.

These tests establish bounded failure-domain separation only. They do not
establish independent custody or rollback-resistant storage.
"""

import json
import shutil
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from experiments.sbcf.generation_anchor import (
    GenerationAnchorHTTPServer,
    GenerationAnchorStore,
)
from experiments.sbcf.offhost_witness import (
    RemoteCheckpoint,
    WitnessHTTPServer,
    WitnessStore,
    WriterLease,
)


def checkpoint(sequence=1, **changes):
    data = dict(
        source="broker",
        run="r",
        policy="p",
        sequence=sequence,
        checkpoint_id=f"cp-{sequence}",
    )
    data.update(changes)
    return RemoteCheckpoint(**data)


def lease(*, token="writer", generation=1, min_sequence=1, max_sequence=3):
    return WriterLease(
        token=token,
        source="broker",
        run="r",
        policy="p",
        min_sequence=min_sequence,
        max_sequence=max_sequence,
        generation=generation,
        expires_at=200.0,
    )


def post_checkpoint(server, record, *, token="writer"):
    request = Request(
        f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
        data=json.dumps(record.__dict__).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=2) as response:
            return response.status
    except HTTPError as exc:
        return exc.code


def test_generation_anchor_store_is_monotonic_and_persistent(tmp_path):
    path = tmp_path / "anchor.db"
    store = GenerationAnchorStore(path)

    assert store.read("broker", "r", "p") == 0
    assert store.advance("broker", "r", "p", 2)
    assert store.read("broker", "r", "p") == 2
    assert not store.advance("broker", "r", "p", 2)
    assert not store.advance("broker", "r", "p", 1)
    assert not store.advance("broker", "r", "p", True)
    assert not store.advance("", "r", "p", 3)

    reopened = GenerationAnchorStore(path)
    assert reopened.read("broker", "r", "p") == 2
    assert reopened.advance("broker", "r", "p", 3)
    assert reopened.read("broker", "r", "p") == 3


def test_generation_anchor_requires_distinct_read_admin_credentials(tmp_path):
    store = GenerationAnchorStore(tmp_path / "anchor.db")
    with pytest.raises(ValueError):
        GenerationAnchorHTTPServer(
            ("127.0.0.1", 0),
            store,
            read_token="same",
            admin_token="same",
        )


def test_generation_anchor_http_separates_read_and_admin_roles(tmp_path):
    store = GenerationAnchorStore(tmp_path / "anchor.db")
    server = GenerationAnchorHTTPServer(
        ("127.0.0.1", 0),
        store,
        read_token="reader",
        admin_token="admin",
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        body = json.dumps({"source": "broker", "run": "r", "policy": "p", "generation": 2}).encode("utf-8")

        reader_write = Request(
            f"http://127.0.0.1:{server.server_port}/v1/generation",
            data=body,
            method="POST",
            headers={"Authorization": "Bearer reader", "Content-Type": "application/json"},
        )
        with pytest.raises(HTTPError) as exc:
            urlopen(reader_write, timeout=2)
        assert exc.value.code == 401

        admin_write = Request(
            f"http://127.0.0.1:{server.server_port}/v1/generation",
            data=body,
            method="POST",
            headers={"Authorization": "Bearer admin", "Content-Type": "application/json"},
        )
        with urlopen(admin_write, timeout=2) as response:
            assert response.status == 201

        admin_read = Request(
            f"http://127.0.0.1:{server.server_port}/v1/generation?source=broker&run=r&policy=p",
            headers={"Authorization": "Bearer admin"},
        )
        with pytest.raises(HTTPError) as exc:
            urlopen(admin_read, timeout=2)
        assert exc.value.code == 401

        reader_read = Request(
            f"http://127.0.0.1:{server.server_port}/v1/generation?source=broker&run=r&policy=p",
            headers={"Authorization": "Bearer reader"},
        )
        with urlopen(reader_read, timeout=2) as response:
            payload = json.loads(response.read())
        assert payload == {"generation": 2, "status": "ok"}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.mark.parametrize("floor", [None, -1, True, "2"])
def test_witness_fails_closed_when_generation_floor_is_unavailable(tmp_path, floor):
    server = WitnessHTTPServer(
        ("127.0.0.1", 0),
        WitnessStore(tmp_path / "witness.db"),
        read_token="reader",
        writer_leases=(lease(),),
        now_fn=lambda: 100.0,
        generation_floor_fn=lambda source, run, policy: floor,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        assert post_checkpoint(server, checkpoint(1)) == 503
        assert server.store.read("broker", "r") is None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_external_floor_rejects_writer_below_generation(tmp_path):
    anchor = GenerationAnchorStore(tmp_path / "anchor.db")
    assert anchor.advance("broker", "r", "p", 2)

    server = WitnessHTTPServer(
        ("127.0.0.1", 0),
        WitnessStore(tmp_path / "witness.db"),
        read_token="reader",
        writer_leases=(lease(generation=1),),
        now_fn=lambda: 100.0,
        generation_floor_fn=anchor.read,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        assert post_checkpoint(server, checkpoint(1)) == 409
        assert server.store.read("broker", "r") is None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_external_floor_survives_witness_database_rollback(tmp_path):
    witness_path = tmp_path / "witness.db"
    witness_backup = tmp_path / "witness-before-revocation.db"
    anchor = GenerationAnchorStore(tmp_path / "anchor.db")

    initial_store = WitnessStore(witness_path)
    assert initial_store.advance(checkpoint(1), writer_generation=1)
    shutil.copy2(witness_path, witness_backup)

    assert anchor.advance("broker", "r", "p", 2)

    # Roll back only the witness database. The separate generation floor stays at 2.
    shutil.copy2(witness_backup, witness_path)
    rolled_back_store = WitnessStore(witness_path)
    assert rolled_back_store.required_writer_generation("broker", "r", "p") == 0

    server = WitnessHTTPServer(
        ("127.0.0.1", 0),
        rolled_back_store,
        read_token="reader",
        writer_leases=(lease(generation=1, min_sequence=2, max_sequence=2),),
        now_fn=lambda: 100.0,
        generation_floor_fn=anchor.read,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        assert post_checkpoint(server, checkpoint(2)) == 409
        assert server.store.read("broker", "r") == checkpoint(1)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
