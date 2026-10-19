"""Known limitation: rolling back the witness DB can revive a revoked writer generation."""

import shutil

import pytest

from experiments.sbcf.offhost_witness import RemoteCheckpoint, WitnessStore


@pytest.mark.xfail(
    strict=True,
    reason="Writer-generation revocation lives in the witness DB; durable anti-rollback storage is not established",
)
def test_witness_db_rollback_cannot_revive_revoked_writer_generation(tmp_path):
    path = tmp_path / "remote.db"
    snapshot = tmp_path / "before-revocation.db"

    store = WitnessStore(path)
    shutil.copyfile(path, snapshot)

    assert store.advance_writer_generation("broker", "r", "p", 2)
    record = RemoteCheckpoint(
        source="broker",
        run="r",
        policy="p",
        sequence=1,
        checkpoint_id="cp-1",
    )
    assert not store.advance(record, writer_generation=1)

    # Counterexample: restoring the pre-revocation DB also restores generation 0.
    shutil.copyfile(snapshot, path)
    restored = WitnessStore(path)
    assert not restored.advance(record, writer_generation=1)
