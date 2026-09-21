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
