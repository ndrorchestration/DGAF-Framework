from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import prepare_track_a_epoch_002_immutable_freeze as freeze

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))


def test_validate_retained_freeze_does_not_reapply_creation_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    base_sha = "f" * 40
    candidate_sha = "a" * 40
    candidate_tree = "b" * 40
    preflight_blob = "c" * 40
    protected = {"example": "d" * 40}
    record = freeze.expected_record(
        protocol_id=CONTRACT["protocol_id"],
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        protected_source_blobs=protected,
    )
    freeze_path = tmp_path / "freeze.json"
    freeze_path.write_text(json.dumps(record), encoding="utf-8")

    monkeypatch.setattr(freeze, "FREEZE_PATH", freeze_path)
    monkeypatch.setattr(
        freeze,
        "validate_non_authorizing_contract",
        lambda: {"protocol_id": CONTRACT["protocol_id"]},
    )
    monkeypatch.setattr(
        freeze,
        "reject_downstream_gates",
        lambda: pytest.fail("retained freeze validation re-applied the creation-time downstream gate"),
    )
    monkeypatch.setattr(
        freeze,
        "git_path_exists",
        lambda path, revision="HEAD": path == freeze.FREEZE_REL and revision in {"HEAD", base_sha},
    )
    monkeypatch.setattr(
        freeze,
        "require_valid_preflight",
        lambda: ({}, candidate_sha, candidate_tree, preflight_blob),
    )
    monkeypatch.setattr(freeze, "protected_source_blobs_at", lambda candidate: protected)
    monkeypatch.setattr(freeze, "require_sources_unchanged", lambda candidate, expected: None)
    monkeypatch.setattr(freeze, "git_history", lambda path, revision="HEAD": ("e" * 40,))
    monkeypatch.setattr(freeze, "git_blob", lambda path, revision: "9" * 40)

    freeze.validate_freeze(base_sha)
