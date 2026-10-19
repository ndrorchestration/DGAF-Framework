"""Known counterexample for the separate generation floor."""

import json
import shutil
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from experiments.sbcf.generation_anchor import GenerationAnchorStore
from experiments.sbcf.offhost_witness import (
    RemoteCheckpoint,
    WitnessHTTPServer,
    WitnessStore,
    WriterLease,
)


def checkpoint(sequence):
    return RemoteCheckpoint(
        source="broker",
        run="r",
        policy="p",
        sequence=sequence,
        checkpoint_id=f"cp-{sequence}",
    )


def post_checkpoint(server, record):
    request = Request(
        f"http://127.0.0.1:{server.server_port}/v1/checkpoint",
        data=json.dumps(record.__dict__).encode("utf-8"),
        method="POST",
        headers={"Authorization": "Bearer writer", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=2) as response:
            return response.status
    except HTTPError as exc:
        return exc.code


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The generation anchor is a separate SQLite failure domain, not durable "
        "anti-rollback storage; coordinated rollback can revive an old writer"
    ),
)
def test_coordinated_witness_and_generation_anchor_rollback_cannot_revive_writer(tmp_path):
    witness_path = tmp_path / "witness.db"
    anchor_path = tmp_path / "anchor.db"
    witness_backup = tmp_path / "witness-old.db"
    anchor_backup = tmp_path / "anchor-old.db"

    witness = WitnessStore(witness_path)
    anchor = GenerationAnchorStore(anchor_path)
    assert witness.advance(checkpoint(1), writer_generation=1)

    # Capture a consistent pre-revocation snapshot of both failure domains.
    shutil.copy2(witness_path, witness_backup)
    shutil.copy2(anchor_path, anchor_backup)

    assert anchor.advance("broker", "r", "p", 2)

    # Coordinated rollback defeats the separation.
    shutil.copy2(witness_backup, witness_path)
    shutil.copy2(anchor_backup, anchor_path)
    rolled_back_anchor = GenerationAnchorStore(anchor_path)
    rolled_back_witness = WitnessStore(witness_path)

    server = WitnessHTTPServer(
        ("127.0.0.1", 0),
        rolled_back_witness,
        read_token="reader",
        writer_leases=(
            WriterLease(
                token="writer",
                source="broker",
                run="r",
                policy="p",
                min_sequence=2,
                max_sequence=2,
                generation=1,
                expires_at=200.0,
            ),
        ),
        now_fn=lambda: 100.0,
        generation_floor_fn=rolled_back_anchor.read,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        assert post_checkpoint(server, checkpoint(2)) != 201
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
