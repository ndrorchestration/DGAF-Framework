import hashlib
import json
from pathlib import Path

import pytest

import mode_t_publication_timing as publication


@pytest.fixture
def context(monkeypatch):
    for key, value in {
        "EVIDENCE_SHA": "a" * 40,
        "GITHUB_REPOSITORY": "owner/repo",
        "GITHUB_RUN_ID": "123",
        "GITHUB_RUN_ATTEMPT": "1",
        "GITHUB_WORKFLOW_REF": "owner/repo/.github/workflows/timing.yml@refs/heads/test",
    }.items():
        monkeypatch.setenv(key, value)
    return publication.identity()


def test_metadata_rejects_wrong_run_head_digest_and_deleted_artifact(context):
    state = {**context, "artifact_name": "fixture"}
    metadata = {
        "id": 456,
        "name": "fixture",
        "digest": "sha256:" + "b" * 64,
        "expired": False,
        "workflow_run": {"id": 123, "head_sha": "a" * 40},
    }
    publication.validate_metadata(state, metadata, 456, "b" * 64)
    for field, value in [
        ("id", 789),
        ("name", "wrong"),
        ("digest", "sha256:" + "c" * 64),
        ("expired", True),
        ("workflow_run", {"id": 999, "head_sha": "a" * 40}),
        ("workflow_run", {"id": 123, "head_sha": "d" * 40}),
    ]:
        with pytest.raises(ValueError):
            publication.validate_metadata(
                state, {**metadata, field: value}, 456, "b" * 64
            )


def write_evidence(path: Path, document: dict):
    raw = json.dumps(document).encode()
    path.write_bytes(raw)
    path.with_suffix(".json.sha256").write_text(
        hashlib.sha256(raw).hexdigest() + "  " + path.name
    )


def test_failed_measurement_removes_fixture_without_emitting_pass(
    context, tmp_path, monkeypatch
):
    fixture = tmp_path / "fixture.bin"
    fixture.write_bytes(b"synthetic")
    monkeypatch.setattr(publication, "FIXTURE", fixture)
    monkeypatch.setattr(publication, "STATE", tmp_path / "missing.json")
    monkeypatch.setattr(publication, "OUTPUT", tmp_path / "output.json")
    with pytest.raises(FileNotFoundError):
        publication.finish()
    assert not fixture.exists()
    assert not publication.OUTPUT.exists()


def test_loader_rejects_identity_tampering_and_scientific_promotion(context, tmp_path):
    document = {
        **context,
        "evidence_class": publication.CLASS,
        "status": "PASS",
        "api_metadata_verified": True,
        "artifact_id": 456,
        "artifact_digest": "sha256:" + "b" * 64,
        "duration_ms": 1.0,
        "start_monotonic_ns": 1,
        "end_monotonic_ns": 1000001,
        "proposed_w_seconds": None,
    }
    false_fields = [
        "durable_custody",
        "external_transparency_verified",
        "coverage_complete",
        "w_proposal_eligible",
        "numeric_w_selected",
        "protocol_frozen",
        "pilot_authorized",
        "empirical_data_collection",
    ]
    document.update({key: False for key in false_fields})
    path = tmp_path / "publication.json"
    write_evidence(path, document)
    assert publication.load_stage(path)["durable_custody"] is False
    for field, value in [(key, True) for key in false_fields] + [
        ("control_plane_sha", "c" * 40),
        ("run_attempt", 2),
        ("api_metadata_verified", False),
        ("duration_ms", float("nan")),
        ("duration_ms", 2.0),
        ("artifact_id", 0),
        ("artifact_digest", "bad"),
        ("proposed_w_seconds", 60),
    ]:
        write_evidence(path, {**document, field: value})
        with pytest.raises(ValueError):
            publication.load_stage(path)
    write_evidence(path, document)
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="sidecar"):
        publication.load_stage(path)
