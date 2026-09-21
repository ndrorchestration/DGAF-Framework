import os
from concurrent.futures import ThreadPoolExecutor

import pytest


def test_canonical_bytes_are_exact():
    from scripts.aoss_stage_a.custody import canonical_bytes

    assert canonical_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n'


def test_nonfinite_payload_rejected():
    from scripts.aoss_stage_a.custody import canonical_bytes

    with pytest.raises(ValueError):
        canonical_bytes({"value": float("nan")})


def test_attempt_cannot_be_reused(tmp_path):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt

    path = reserve_synthetic_attempt(tmp_path, "case-1")
    assert (path / "SYNTHETIC_TEST_ONLY").is_file()
    with pytest.raises(FileExistsError):
        reserve_synthetic_attempt(tmp_path, "case-1")


@pytest.mark.parametrize(
    "attempt_id",
    ["", "../escape", "a/b", "a\\b", "-leading", "x" * 65],
)
def test_disallowed_attempt_ids_fail_closed(tmp_path, attempt_id):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt

    with pytest.raises(ValueError):
        reserve_synthetic_attempt(tmp_path, attempt_id)


def test_symlink_parent_is_rejected(tmp_path):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt

    real = tmp_path / "real"
    real.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(real, target_is_directory=True)

    with pytest.raises(ValueError, match="symlink path component rejected"):
        reserve_synthetic_attempt(alias, "case")


def test_concurrent_reservation_allows_exactly_one_creator(tmp_path):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt

    def reserve():
        try:
            reserve_synthetic_attempt(tmp_path, "race")
            return "CREATED"
        except FileExistsError:
            return "EXISTS"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = sorted(pool.map(lambda _: reserve(), range(2)))

    assert results == ["CREATED", "EXISTS"]


def test_incomplete_reservation_is_preserved_and_not_reused(tmp_path, monkeypatch):
    import scripts.aoss_stage_a.custody as custody

    original = custody._exclusive_write_at

    def fail_started(dir_fd, name, data):
        if name == "STARTED.json":
            raise OSError("simulated crash")
        return original(dir_fd, name, data)

    monkeypatch.setattr(custody, "_exclusive_write_at", fail_started)

    with pytest.raises(OSError, match="simulated crash"):
        custody.reserve_synthetic_attempt(tmp_path, "crash")

    attempt = tmp_path / "crash"
    assert attempt.is_dir()
    assert (attempt / "SYNTHETIC_TEST_ONLY").is_file()
    with pytest.raises(FileExistsError):
        custody.reserve_synthetic_attempt(tmp_path, "crash")


def test_write_object_is_content_addressed_and_deduplicated(tmp_path):
    from scripts.aoss_stage_a.custody import (
        canonical_bytes,
        digest_bytes,
        reserve_synthetic_attempt,
        write_object,
    )

    attempt = reserve_synthetic_attempt(tmp_path, "case")
    payload = {"b": 2, "a": 1}
    expected = digest_bytes(canonical_bytes(payload))

    first = write_object(attempt, payload)
    second = write_object(attempt, payload)

    assert first == expected
    assert second == expected
    assert (attempt / "objects" / f"{expected}.json").read_bytes() == canonical_bytes(payload)


def test_corrupt_existing_content_address_fails_closed(tmp_path):
    from scripts.aoss_stage_a.custody import (
        canonical_bytes,
        digest_bytes,
        reserve_synthetic_attempt,
        write_object,
    )

    attempt = reserve_synthetic_attempt(tmp_path, "case")
    payload = {"a": 1}
    digest = digest_bytes(canonical_bytes(payload))
    target = attempt / "objects" / f"{digest}.json"
    target.write_bytes(b"corrupt\n")

    with pytest.raises(FileExistsError):
        write_object(attempt, payload)


def test_missing_synthetic_marker_blocks_object_write(tmp_path):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt, write_object

    attempt = reserve_synthetic_attempt(tmp_path, "case")
    (attempt / "SYNTHETIC_TEST_ONLY").unlink()

    with pytest.raises(ValueError, match="marker"):
        write_object(attempt, {"a": 1})


def test_symlink_object_directory_is_rejected(tmp_path):
    from scripts.aoss_stage_a.custody import reserve_synthetic_attempt, write_object

    attempt = reserve_synthetic_attempt(tmp_path, "case")
    objects = attempt / "objects"
    objects.rmdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    objects.symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError, match="object directory"):
        write_object(attempt, {"a": 1})


def test_reservation_and_object_writes_fsync_directories(tmp_path, monkeypatch):
    import scripts.aoss_stage_a.custody as custody

    calls = []
    original = custody._fsync_fd

    def recording_fsync(fd):
        calls.append(os.fstat(fd).st_ino)
        return original(fd)

    monkeypatch.setattr(custody, "_fsync_fd", recording_fsync)

    attempt = custody.reserve_synthetic_attempt(tmp_path, "durable")
    custody.write_object(attempt, {"a": 1})

    assert len(calls) >= 8


def test_parent_swap_cannot_redirect_attempt_creation(tmp_path, monkeypatch):
    import scripts.aoss_stage_a.custody as custody

    parent = tmp_path / "parent"
    parent.mkdir()
    moved = tmp_path / "moved-parent"
    outside = tmp_path / "outside"
    outside.mkdir()
    original_mkdir = custody.os.mkdir
    swapped = False

    def swapping_mkdir(path, mode=0o777, *, dir_fd=None):
        nonlocal swapped
        if not swapped:
            swapped = True
            parent.rename(moved)
            parent.symlink_to(outside, target_is_directory=True)
        if dir_fd is None:
            return original_mkdir(path, mode)
        return original_mkdir(path, mode, dir_fd=dir_fd)

    monkeypatch.setattr(custody.os, "mkdir", swapping_mkdir)

    with pytest.raises(ValueError, match="parent directory changed during reservation"):
        custody.reserve_synthetic_attempt(parent, "case")

    assert not (outside / "case").exists()
