from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/gate0-release-sbom-proof.yml"
SCRIPT = ROOT / "scripts/build_release_sbom_manifest.py"


def test_sbom_workflow_is_read_only_exact_source_and_pinned() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "permissions:\n  contents: read" in text
    assert "secrets." not in text
    assert "persist-credentials: false" in text
    assert "github.event.pull_request.head.sha || github.sha" in text
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in text
    assert "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405" in text
    assert "actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020" in text
    assert "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02" in text


def test_sbom_workflow_preserves_security_failure_separation() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pip_audit_exit_code" in text
    assert "security-scan waiver" not in text.lower()
    assert "release_admission" in text
    assert 'assert data["release_admission"] is False' in text
    assert 'assert data["independent_validation"] is False' in text
    assert "if: always()" not in text


def test_sbom_artifact_is_bounded_and_retained() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "python-ci-py312.cdx.json" in text
    assert "npm-lock.cdx.json" in text
    assert "manifest.json" in text
    assert "retention-days: 30" in text
    assert "if-no-files-found: error" in text


def test_manifest_builder_encodes_non_claims() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert '"claim_scope": "G6_SBOM_PROOF_ONLY"' in text
    assert '"release_admission": False' in text
    assert '"independent_validation": False' in text
    assert '"security_scan_pass": args.pip_audit_exit_code == 0' in text
    assert "SBOM generation is not a security-scan waiver or release admission." in text


def test_manifest_builder_accepts_utf8_bom(tmp_path) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("sbom_manifest", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    path = tmp_path / "bom.json"
    path.write_bytes(b"\xef\xbb\xbf" + b'{"bomFormat":"CycloneDX","components":[]}')
    data = module.load_cyclonedx(path)
    assert data["bomFormat"] == "CycloneDX"
