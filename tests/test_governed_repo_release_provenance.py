import importlib.util
import json
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_governed_repo_release_provenance.py"
SPEC = importlib.util.spec_from_file_location("release_provenance", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def _args(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "ndrorchestration_governed_repo-0.0.0.dev0-py3-none-any.whl").write_bytes(b"wheel")
    (dist / "ndrorchestration_governed_repo-0.0.0.dev0.tar.gz").write_bytes(b"sdist")
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "ndrorchestration-governed-repo"\nversion = "0.0.0.dev0"\n',
        encoding="utf-8",
    )
    return Namespace(
        dist_dir=str(dist),
        pyproject=str(pyproject),
        output=str(tmp_path / "manifest.json"),
        repository="ndrorchestration/DGAF-Framework",
        source_sha="a" * 40,
        action_sha="a" * 40,
        workflow_run_id="123",
        workflow_run_attempt="1",
    )


def test_manifest_binds_artifacts_source_and_non_effects(tmp_path):
    args = _args(tmp_path)
    manifest = MODULE.build_manifest(args)
    dist = Path(args.dist_dir)

    assert manifest["source"]["commit_sha"] == "a" * 40
    assert manifest["package"]["wheel"]["sha256"] == MODULE.sha256(
        dist / "ndrorchestration_governed_repo-0.0.0.dev0-py3-none-any.whl"
    )
    assert manifest["package"]["sdist"]["sha256"] == MODULE.sha256(
        dist / "ndrorchestration_governed_repo-0.0.0.dev0.tar.gz"
    )
    assert manifest["verification"]["python_versions"] == [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    ]
    assert manifest["non_effects"] == {
        "merge_executed": False,
        "mutation_executed": False,
        "authorization_effect": "NONE",
    }


def test_generator_fails_closed_on_ambiguous_artifact_set(tmp_path):
    args = _args(tmp_path)
    dist = Path(args.dist_dir)
    (dist / "second.whl").write_bytes(b"other")

    try:
        MODULE.build_manifest(args)
    except ValueError as exc:
        assert "exactly one wheel" in str(exc)
    else:
        raise AssertionError("ambiguous wheel set must fail closed")


def test_validator_rejects_authorization_effect(tmp_path):
    manifest = MODULE.build_manifest(_args(tmp_path))
    manifest["non_effects"]["authorization_effect"] = "GRANTED"

    try:
        MODULE.validate_manifest(manifest)
    except ValueError as exc:
        assert "non-effect" in str(exc)
    else:
        raise AssertionError("authorization effect must fail closed")


def test_manifest_is_json_serializable(tmp_path):
    manifest = MODULE.build_manifest(_args(tmp_path))
    encoded = json.dumps(manifest, sort_keys=True)
    assert "governed_repo_release_provenance.v1" in encoded
