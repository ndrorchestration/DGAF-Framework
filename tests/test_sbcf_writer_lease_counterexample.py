"""Known writer-lease limitation: server wall-clock rollback can revive expiry."""

import pytest

from experiments.sbcf.offhost_witness import RemoteCheckpoint, WriterLease


@pytest.mark.xfail(
    strict=True,
    reason="Lease expiry trusts the witness host wall clock; rollback-resistant trusted time is not established",
)
def test_wall_clock_rollback_cannot_revive_expired_writer_lease():
    lease = WriterLease(
        token="writer",
        source="broker",
        run="r",
        policy="p",
        min_sequence=1,
        max_sequence=2,
        expires_at=150.0,
    )
    record = RemoteCheckpoint(
        source="broker",
        run="r",
        policy="p",
        sequence=1,
        checkpoint_id="cp-1",
    )
    assert not lease.allows(record, now=150.0)
    # Counterexample: ordinary wall time can move backward and make the lease valid again.
    assert not lease.allows(record, now=100.0)
