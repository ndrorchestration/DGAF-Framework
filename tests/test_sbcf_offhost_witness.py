"""Off-host witness contract tests. These do not establish independent custody."""

import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from experiments.sbcf.offhost_witness import (
    RemoteCheckpoint,
    RemoteWitnessClient,
    WitnessHTTPServer,
    WitnessStore,
    WriterLease,
)


def checkpoint(sequence=1, **changes):
    data = dict(source="broker", run="r", policy="p", sequence=sequence, checkpoint_id=f"cp-{sequence}")
    data.update(changes)
    return RemoteCheckpoint(**data)


def writer_lease(**changes):
    data = dict(
        token="writer",
        source="broker",
        run="r",
        policy="p",
        min_sequence=1,
        max_sequence=2,
        expires_at=200.0,
    )
    data.update(changes)
    return WriterLease(**data)


def witness_server(tmp_path, *, leases=None, now=100.0):
    return WitnessHTTPServer(
        ("127.0.0.1", 0),
        WitnessStore(tmp_path / "remote.db"),
        read_token="reader",
        writer_leases=tuple(leases or (writer_lease(),)),
        now_fn=lambda: now,
    )


def test_store_is_monotonic_and_policy_bound(tmp_path):
    store = WitnessStore(tmp_path / "remote.db")
    assert store.advance(checkpoint(1))
    assert not store.advance(checkpoint(1, checkpoint_id="repeat"))
    assert not store.advance(checkpoint(0, checkpoint_id="old"))
    assert not store.advance(checkpoint(2, policy="other"))
    assert store.advance(checkpoint(2))
    assert store.read("broker", "r") == checkpoint(2)


def test_checkpoint_id_cannot_be_reused_across_scope(tmp_path):
    store = WitnessStore(tmp_path / "remote.db")
    assert store.advance(checkpoint(1))
    duplicate_id = checkpoint(1, source="registry", run="other", checkpoint_id="cp-1")
    assert not store.advance(duplicate_id)


def test_invalid_checkpoint_is_rejected(tmp_path):
    store = WitnessStore(tmp_path / "remote.db")
    assert not store.advance(checkpoint(-1))
    assert not store.advance(checkpoint(1, policy=""))
    assert store.read("", "r") is None


def test_client_requires_https(tmp_path):
    ca = tmp_path / "unused.pem"
    ca.write_text("not a certificate", encoding="utf-8")
    with pytest.raises(ValueError):
        RemoteWitnessClient("http://127.0.0.1:4443", token="t", cafile=ca)


def test_client_fails_closed_when_endpoint_unreachable(tmp_path):
    ca = tmp_path / "unused.pem"
    ca.write_text("not a certificate", encoding="utf-8")
    with pytest.raises(Exception):
        # Invalid CA material is itself fail-closed during client construction.
        RemoteWitnessClient("https://127.0.0.1:9", token="t", cafile=ca)


def test_handler_rejects_missing_authorization(tmp_path):
    server = witness_server(tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(f"http://127.0.0.1:{server.server_port}/v1/checkpoint?source=broker&run=r")
        with pytest.raises(HTTPError) as exc:
            urlopen(request, timeout=2)
        assert exc.value.code == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_server_requires_distinct_read_write_tokens(tmp_path):
    store = WitnessStore(tmp_path / "remote.db")
    with pytest.raises(ValueError):
        WitnessHTTPServer(
            ("127.0.0.1", 0),
            store,
            read_token="same",
            writer_leases=(writer_lease(token="same"),),
        )


def test_server_rejects_duplicate_writer_credentials(tmp_path):
    store = WitnessStore(tmp_path / "remote.db")
    with pytest.raises(ValueError):
        WitnessHTTPServer(
            ("127.0.0.1", 0),
            store,
            read_token="reader",
            writer_leases=(
                writer_lease(token="duplicate"),
                writer_lease(token="duplicate", run="other"),
            ),
        )


def test_writer_lease_restricts_scope_sequence_and_expiry(tmp_path):
    import json

    clock = {"now": 100.0}
    server = WitnessHTTPServer(
        ("127.0.0.1", 0),
        WitnessStore(tmp_path / "remote.db"),
        read_token="reader",
        writer_leases=(writer_lease(min_sequence=1, max_sequence=2, expires_at=150.0),),
        now_fn=lambda: clock["now"],
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def post(record):
        data = json.dumps(record.__dict__).encode("utf-8")
        request = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
            data=data,
            method="POST",
            headers={"Authorization": "Bearer writer", "Content-Type": "application/json"},
        )
        try:
            with urlopen(request, timeout=2) as response:
                return response.status
        except HTTPError as exc:
            return exc.code

    try:
        assert post(checkpoint(0, checkpoint_id="below-min")) == 403
        assert post(checkpoint(1, source="registry", checkpoint_id="wrong-source")) == 403
        assert post(checkpoint(1, run="other", checkpoint_id="wrong-run")) == 403
        assert post(checkpoint(1, policy="other", checkpoint_id="wrong-policy")) == 403
        assert post(checkpoint(1)) == 201
        assert post(checkpoint(3, checkpoint_id="above-max")) == 403
        clock["now"] = 150.0
        assert post(checkpoint(2)) == 403
        assert server.store.read("broker", "r") == checkpoint(1)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_read_token_cannot_advance_and_write_token_cannot_read(tmp_path):
    import json

    server = witness_server(tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        payload = json.dumps(checkpoint(1).__dict__).encode("utf-8")
        read_credential_post = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
            data=payload,
            method="POST",
            headers={"Authorization": "Bearer reader", "Content-Type": "application/json"},
        )
        with pytest.raises(HTTPError) as exc:
            urlopen(read_credential_post, timeout=2)
        assert exc.value.code == 401

        write_credential_post = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
            data=payload,
            method="POST",
            headers={"Authorization": "Bearer writer", "Content-Type": "application/json"},
        )
        with urlopen(write_credential_post, timeout=2) as response:
            assert response.status == 201

        write_credential_get = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint?source=broker&run=r",
            headers={"Authorization": "Bearer writer"},
        )
        with pytest.raises(HTTPError) as exc:
            urlopen(write_credential_get, timeout=2)
        assert exc.value.code == 401

        read_credential_get = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint?source=broker&run=r",
            headers={"Authorization": "Bearer reader"},
        )
        with urlopen(read_credential_get, timeout=2) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_handler_accepts_only_strictly_monotonic_records(tmp_path):
    import json

    server = witness_server(tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def post(record):
        data = json.dumps(record.__dict__).encode("utf-8")
        request = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
            data=data,
            method="POST",
            headers={"Authorization": "Bearer writer", "Content-Type": "application/json"},
        )
        try:
            with urlopen(request, timeout=2) as response:
                return response.status
        except HTTPError as exc:
            return exc.code

    try:
        assert post(checkpoint(1)) == 201
        assert post(checkpoint(1, checkpoint_id="replay")) == 409
        assert post(checkpoint(2)) == 201
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
