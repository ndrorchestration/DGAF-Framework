from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_governed_repo_release_provenance.py"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("governed_repo_release_provenance", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_dist(tmp_path: Path) -> Path:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "ndrorchestration_governed_repo-0.0.0.dev0-py3-none-any.whl").write_bytes(b"wheel-bytes")
    (dist / "ndrorchestration_governed_repo-0.0.0.dev0.tar.gz").write_bytes(b"sdist-bytes")
    return dist


def test_build_manifest_binds_artifacts_source_and_non_effects(tmp_path: Path):
    module = load_module()
    manifest = module.build_manifest(
        dist_dir=make_dist(tmp_path),
        source_sha="a" * 40,
        workflow_run_id="123456",
        python_versions=["3.10", "3.11", "3.12", "3.13", "3.14"],
        release_notes_ref="issue://1214",
    )

    assert module.validate_manifest(manifest) == []
    assert manifest["source"]["sha"] == "a" * 40
    assert manifest["action"]["source_sha"] == "a" * 40
    assert len(manifest["package"]["wheel"]["sha256"]) == 64
    assert len(manifest["package"]["sdist"]["sha256"]) == 64
    assert manifest["non_effects"] == {
        "merge_executed": False,
        "mutation_executed": False,
        "authorization_effect": "NONE",
        "publication_effect": "NONE",
    }
    assert manifest["claim_ceiling"]["publication_readiness"] == "NOT_ESTABLISHED"


def test_validation_rejects_source_identity_drift(tmp_path: Path):
    module = load_module()
    manifest = module.build_manifest(
        dist_dir=make_dist(tmp_path),
        source_sha="b" * 40,
        workflow_run_id="789",
        python_versions=["3.12"],
        release_notes_ref="issue://1214",
    )
    manifest["action"]["source_sha"] = "c" * 40

    errors = module.validate_manifest(manifest)

    assert any("action.source_sha must equal source.sha" in error for error in errors)


def test_validation_rejects_authorization_or_publication_effect(tmp_path: Path):
    module = load_module()
    manifest = module.build_manifest(
        dist_dir=make_dist(tmp_path),
        source_sha="d" * 40,
        workflow_run_id="987",
        python_versions=["3.12"],
        release_notes_ref="issue://1214",
    )
    manifest["non_effects"]["authorization_effect"] = "GRANTED"

    errors = module.validate_manifest(manifest)

    assert any("non_effects" in error for error in errors)


def test_cli_emits_deterministic_json_for_same_inputs(tmp_path: Path, monkeypatch):
    module = load_module()
    dist = make_dist(tmp_path)
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    argv = [
        "build_governed_repo_release_provenance.py",
        "--dist-dir",
        str(dist),
        "--source-sha",
        "e" * 40,
        "--workflow-run-id",
        "555",
        "--python-version",
        "3.10",
        "--python-version",
        "3.14",
        "--output",
        str(first),
    ]
    monkeypatch.setattr("sys.argv", argv)
    assert module.main() == 0

    argv[-1] = str(second)
    monkeypatch.setattr("sys.argv", argv)
    assert module.main() == 0

    assert first.read_bytes() == second.read_bytes()
    assert json.loads(first.read_text(encoding="utf-8"))["workflow"]["run_id"] == "555"
