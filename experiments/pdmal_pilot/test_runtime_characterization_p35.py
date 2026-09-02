"""Non-empirical P-35 boundary tests for runtime characterization."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

import runtime_characterization as rc


def allow_premises(_text, _invariant) -> bool:
    return True


def test_default_characterization_matrix_excludes_dgaf() -> None:
    assert "dgaf" not in rc.DEFAULT_CONDITIONS


def test_dgaf_characterization_requires_explicit_checker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.delenv("PDMAL_PREMISE_CHECKER", raising=False)
    with pytest.raises(SystemExit, match="PDMAL_PREMISE_CHECKER"):
        rc.run_characterization(
            output_dir=tmp_path,
            seeds=(20260817,),
            conditions=("dgaf",),
            topologies=("ring",),
            failure_counts=(0,),
        )


def test_dgaf_characterization_passes_explicit_checker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "test_runtime_characterization_p35:allow_premises")

    captured: list[dict] = []

    class FakeTask:
        def __init__(self, **kwargs):
            captured.append(kwargs)

        def run_detailed(self, *, seed, attempt):
            return SimpleNamespace(
                attempt_status=rc.AttemptStatus.SUCCESS,
                iterations_completed=1,
                final_std=0.0,
                consensus_success=True,
                trial_key=f"trial-{seed}",
                topology_fingerprint="topology-test",
                failure_nodes=(),
                deviation=None,
            )

    monkeypatch.setattr(rc, "ConsensusTask", FakeTask)
    monkeypatch.setattr(rc, "SEED_RUNTIME_CEILING_SECONDS", 60.0)

    artifact = rc.run_characterization(
        output_dir=tmp_path,
        seeds=(20260817,),
        conditions=("dgaf",),
        topologies=("ring",),
        failure_counts=(0,),
    )

    assert artifact["p35_checker_configured"] is True
    assert len(captured) == 1
    assert captured[0]["condition"] == "dgaf"
    assert captured[0]["premise_check_fn"] is allow_premises
