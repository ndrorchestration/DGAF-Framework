from pathlib import Path

import pytest

from scripts.aoss_stage_a import source_driver


def _manifest():
    return {
        "schema": "agent-control-plane.provenance.v1",
        "run_id": "run-1",
        "event_count": 2,
        "events": [
            {
                "event": "task.started",
                "task_id": "task-1",
                "run_id": "run-1",
                "timestamp": "2026-09-18T10:00:00+00:00",
            },
            {
                "event": "task.completed",
                "task_id": "task-1",
                "run_id": "run-1",
                "timestamp": "2026-09-18T10:00:01+00:00",
            },
        ],
    }


def test_driver_is_bound_to_frozen_acp_identity():
    assert source_driver.SOURCE_COMMIT == "dbab7c1afafec524ce7c18157de2089cafe79c87"
    assert source_driver.SOURCE_MODULE == "src/agent_control_plane/core.py"
    assert source_driver.SOURCE_MODULE_BLOB == "1341df7296a426b336b76ac6b1e4df67611ec931"
    assert len(source_driver.RECIPE_CLASSES) == 16


@pytest.mark.parametrize(
    ("recipe_class", "terminal"),
    [
        ("missing_event", "task.started"),
        ("reordered_exported_events", "task.started"),
        ("duplicate_replayed_event", "task.completed"),
        ("malformed_manifest", "task.started"),
        ("mismatched_run_id", "task.started"),
    ],
)
def test_post_export_controls_preserve_original_manifest(recipe_class, terminal):
    raw = _manifest()
    before = source_driver._canonical_bytes(raw)
    transformed, label = source_driver._transform(recipe_class, raw)

    assert source_driver._canonical_bytes(raw) == before
    assert label == f"POST_EXPORT_{recipe_class.upper()}"
    assert transformed is not raw
    assert transformed["event_count"] == len(transformed["events"])
    assert transformed["events"][-1]["event"] == terminal


def test_missing_authority_evidence_is_label_only_post_export_control():
    raw = _manifest()
    transformed, label = source_driver._transform("missing_authority_evidence", raw)

    assert transformed == raw
    assert transformed is not raw
    assert label == "POST_EXPORT_MISSING_AUTHORITY_EVIDENCE"


def test_source_order_ambiguity_changes_export_not_raw_source():
    raw = _manifest()
    transformed, _ = source_driver._transform("source_order_ambiguity", raw)

    assert raw["events"][0]["timestamp"] != raw["events"][1]["timestamp"]
    assert transformed["events"][0]["timestamp"] == transformed["events"][1]["timestamp"]


def test_exclusive_result_write_refuses_overwrite(tmp_path):
    destination = tmp_path / "result.json"
    result = {
        "record_type": "AOSS_V0_6_STAGE_A_SOURCE_DRIVER_RESULT",
        "collection_authorized": False,
        "scientific_n_increment": 0,
    }

    first = source_driver.write_result_exclusive(result, destination)
    assert len(first) == 64
    assert destination.is_file()

    with pytest.raises(source_driver.SourceDriverError, match="SOURCE_DRIVER_DESTINATION_EXISTS"):
        source_driver.write_result_exclusive(result, destination)


def test_unknown_recipe_fails_before_any_acp_load(monkeypatch):
    called = False

    def forbidden(_root: Path):
        nonlocal called
        called = True
        raise AssertionError("ACP must not load for unknown recipe")

    monkeypatch.setattr(source_driver, "_load_frozen_acp", forbidden)

    with pytest.raises(source_driver.SourceDriverError, match="SOURCE_DRIVER_RECIPE_NOT_FROZEN"):
        source_driver.execute_recipe(Path("/not-used"), "not-frozen", run_id="run-1")

    assert called is False


@pytest.mark.parametrize(
    ("git_results", "error"),
    [
        (
            {
                ("rev-parse", "--is-shallow-repository"): "true",
            },
            "SOURCE_DRIVER_ACP_SHALLOW_REPOSITORY",
        ),
        (
            {
                ("rev-parse", "--is-shallow-repository"): "false",
                ("status", "--porcelain=v1", "--untracked-files=all"): "dirty",
            },
            "SOURCE_DRIVER_ACP_WORKTREE_DIRTY",
        ),
        (
            {
                ("rev-parse", "--is-shallow-repository"): "false",
                ("status", "--porcelain=v1", "--untracked-files=all"): "",
                ("rev-parse", "HEAD"): "0" * 40,
            },
            "SOURCE_DRIVER_ACP_COMMIT_MISMATCH",
        ),
    ],
)
def test_frozen_checkout_verification_fails_closed(tmp_path, monkeypatch, git_results, error):
    def fake_git(_root: Path, *args: str) -> str:
        return git_results.get(tuple(args), "")

    monkeypatch.setattr(source_driver, "_git", fake_git)

    with pytest.raises(source_driver.SourceDriverError, match=error):
        source_driver.verify_frozen_acp_checkout(tmp_path)
