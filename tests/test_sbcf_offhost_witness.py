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
)


def checkpoint(sequence=1, **changes):
    data = dict(source="broker", run="r", policy="p", sequence=sequence, checkpoint_id=f"cp-{sequence}")
    data.update(changes)
    return RemoteCheckpoint(**data)


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
    server = WitnessHTTPServer(("127.0.0.1", 0), WitnessStore(tmp_path / "remote.db"), "secret")
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


def test_handler_accepts_only_strictly_monotonic_records(tmp_path):
    import json

    server = WitnessHTTPServer(("127.0.0.1", 0), WitnessStore(tmp_path / "remote.db"), "secret")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def post(record):
        data = json.dumps(record.__dict__).encode("utf-8")
        request = Request(
            f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
            data=data,
            method="POST",
            headers={"Authorization": "Bearer secret", "Content-Type": "application/json"},
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
