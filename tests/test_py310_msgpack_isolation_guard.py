"""Synthetic negative controls for the non-admitting MessagePack split-auditor proof."""

from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts import proof_py310_audit_isolation as proof
from scripts import proof_py310_msgpack_regression_classifier as classifier


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_workspace(tmp_path, monkeypatch, *, msgpack: str = "1.2.3"):
    source = tmp_path / "requirements-ci.txt"
    workload = tmp_path / "py310-isolated-workload-requirements.txt"
    lines = [
        "# Synthetic conditional-source test fixture; NOT canonical",
        "pytest==9.1.1",
        "pytest-cov==7.1.0",
        "pytest-asyncio==1.4.0",
        "pytest-timeout==2.4.0",
        "numpy==2.2.6",
        "mypy==2.3.1",
        "flake8==7.3.0",
        "black==26.10.1",
        "isort==8.0.1",
        "pydantic==2.13.4",
        "jsonschema==4.26.0",
        "setuptools==84.2.1",
        "bandit==1.9.4",
        'pip-audit==2.10.1 ; python_version >= "3.11"',
        "requests==2.34.2",
        f"msgpack=={msgpack}",
        "pip==26.2.1",
        "certifi==2026.10.23",
    ]
    source.write_text("\n".join(lines) + "\n", encoding="utf-8")
    monkeypatch.setattr(proof, "SOURCE", source)
    monkeypatch.setattr(proof, "WORKLOAD_SOURCE", workload)
    return source, workload


def test_patched_marker_source_is_mirrored_without_rewriting_pins(tmp_path, monkeypatch) -> None:
    source, workload = _source_workspace(tmp_path, monkeypatch)
    proof.make_source()
    src, candidate = source.read_text(encoding="utf-8"), workload.read_text(encoding="utf-8")
    assert src in candidate
    assert 'pip-audit==2.10.1 ; python_version >= "3.11"' in candidate
    assert "\npip-audit==2.10.1\n" not in candidate
    assert "requests==2.34.2" in candidate
    assert "msgpack==1.2.3" in candidate
    assert "black==26.10.1" in candidate


def test_unpatched_messagepack_is_rejected_before_resolver(tmp_path, monkeypatch) -> None:
    _source_workspace(tmp_path, monkeypatch, msgpack="1.2.2")
    with pytest.raises(AssertionError, match="patched MessagePack"):
        proof.make_source()


def test_duplicate_scanner_pin_is_rejected_before_resolver(tmp_path, monkeypatch) -> None:
    source, _ = _source_workspace(tmp_path, monkeypatch)
    source.write_text(source.read_text() + "pip-audit==2.10.1\n")
    with pytest.raises(AssertionError, match="conditional scanner pin required"):
        proof.make_source()


def _audit_workspace(tmp_path, monkeypatch) -> None:
    source, workload = _source_workspace(tmp_path, monkeypatch)
    proof.make_source()
    lock = tmp_path / "py310-isolated-workload-hash.lock"
    rows = (("msgpack", "1.2.3"), ("pip", "26.2.1"), ("setuptools", "84.2.1"))
    lock.write_text(
        "# TEST-ONLY LOCK — NEVER ADMITTED\n"
        + "".join(f"{name}=={version} \\\n    --hash=sha256:{'a' * 64}\n" for name, version in rows),
        encoding="utf-8",
    )
    manifest = tmp_path / "py310-isolated-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "source_sha256": _sha(source),
                "workload_source_sha256": _sha(workload),
                "workload_lock_sha256": _sha(lock),
                "resolved_package_count": len(rows),
                "security_audit_status": "NOT_YET_VERIFIED",
            }
        ),
        encoding="utf-8",
    )
    audit = tmp_path / "py310-isolated-audit.json"
    audit.write_text(
        json.dumps(
            {
                "dependencies": [
                    {"name": name, "version": version, "vulns": []}
                    for name, version in rows
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(proof, "LOCK", lock)
    monkeypatch.setattr(proof, "MANIFEST", manifest)
    monkeypatch.setattr(proof, "AUDIT", audit)


def test_complete_hash_bound_audit_updates_only_proof_receipt(tmp_path, monkeypatch) -> None:
    _audit_workspace(tmp_path, monkeypatch)
    proof.verify_audit()
    receipt = json.loads(proof.MANIFEST.read_text(encoding="utf-8"))
    assert receipt["audited_package_count"] == 3
    assert receipt["security_audit_status"] == "PASSED_COMPLETE_INDEPENDENT_HASHED_REQUIREMENTS_SCAN"
    assert receipt["audit_json_sha256"] == _sha(proof.AUDIT)


@pytest.mark.parametrize("failure", ["missing", "extra", "wrong_version", "vulnerable", "duplicate"])
def test_audit_fail_closed_for_incomplete_or_modified_inventory(tmp_path, monkeypatch, failure: str) -> None:
    _audit_workspace(tmp_path, monkeypatch)
    audit = json.loads(proof.AUDIT.read_text(encoding="utf-8"))
    deps = audit["dependencies"]
    if failure == "missing":
        deps.pop()
    elif failure == "extra":
        deps.append({"name": "unverified-package", "version": "1.0", "vulns": []})
    elif failure == "wrong_version":
        deps[0]["version"] = "1.2.2"
    elif failure == "vulnerable":
        deps[0]["vulns"] = [{"id": "synthetic-advisory"}]
    elif failure == "duplicate":
        deps.append(dict(deps[0]))
    proof.AUDIT.write_text(json.dumps(audit), encoding="utf-8")

    with pytest.raises(AssertionError):
        proof.verify_audit()
    assert json.loads(proof.MANIFEST.read_text())["security_audit_status"] == "NOT_YET_VERIFIED"


@pytest.mark.parametrize("target", ["source", "workload", "lock"])
def test_source_and_lock_tampering_is_rejected(tmp_path, monkeypatch, target: str) -> None:
    _audit_workspace(tmp_path, monkeypatch)
    path = {"source": proof.SOURCE, "workload": proof.WORKLOAD_SOURCE, "lock": proof.LOCK}[target]
    path.write_text(path.read_text() + "# unauthorized test change\n", encoding="utf-8")
    with pytest.raises(AssertionError):
        proof.verify_audit()


def _classifier_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path, Path, Path, Path]:
    source = tmp_path / "requirements-ci.txt"
    source.write_text("synthetic source for classifier only\n", encoding="utf-8")
    monkeypatch.setattr(classifier, "SOURCE_SHA256", _sha(source))
    xml = tmp_path / "full-pytest.xml"
    root = ET.Element("testsuite")
    for i in range(2000):
        ET.SubElement(root, "testcase", classname="tests.synthetic", name=f"test_pass_{i}")
    for name, fragments in classifier.EXPECTED.items():
        item = ET.SubElement(root, "testcase", classname="tests.test_ci_lock_contract", name=name)
        ET.SubElement(item, "failure", message="expected: " + " ".join(fragments))
    ET.ElementTree(root).write(xml, encoding="utf-8")
    log = tmp_path / "pytest.log"
    log.write_text("synthetic classification unit fixture", encoding="utf-8")
    status = tmp_path / "pytest.status"
    status.write_text("pytest_exit_code=1", encoding="utf-8")
    return xml, log, status, source, tmp_path / "classification.json"


@pytest.mark.parametrize(
    "mutation",
    ["valid", "unexpected_failure", "missing_expected", "changed_meaning", "error", "status_zero", "source_drift"],
)
def test_classifier_is_strict_and_never_converts_failure_to_release(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    xml, log, status, source, destination = _classifier_workspace(tmp_path, monkeypatch)
    if mutation in {"unexpected_failure", "missing_expected", "changed_meaning", "error"}:
        root = ET.parse(xml).getroot()
        if mutation == "unexpected_failure":
            item = ET.SubElement(root, "testcase", classname="tests.functional", name="test_unexpected")
            ET.SubElement(item, "failure", message="synthetic functional regression")
        elif mutation == "missing_expected":
            cases = [item for item in root if item.get("name") == "test_every_direct_ci_pin_is_exactly_represented_in_every_lock"]
            assert len(cases) == 1
            root.remove(cases[0])
        elif mutation == "changed_meaning":
            first = next(item for item in root if item.get("name") == "test_source_and_canonical_lock_identities_are_bound")
            failure = first.find("failure")
            assert failure is not None
            failure.set("message", "unrelated source error")
        elif mutation == "error":
            item = ET.SubElement(root, "testcase", classname="tests.functional", name="test_collection_error")
            ET.SubElement(item, "error", message="collection failed")
        ET.ElementTree(root).write(xml, encoding="utf-8")
    elif mutation == "status_zero":
        status.write_text("pytest_exit_code=0", encoding="utf-8")
    elif mutation == "source_drift":
        source.write_text(source.read_text(encoding="utf-8") + "drift", encoding="utf-8")
    if mutation == "valid":
        result = classifier.classify(xml, log, status, source, destination)
        assert result["unexpected_functional_regression_failures"] == 0
        assert result["overall_pytest_status"] == "FAILED"
        assert result["release_authorization"] == "NOT_AUTHORIZED"
        assert destination.is_file()
    else:
        with pytest.raises(AssertionError):
            classifier.classify(xml, log, status, source, destination)
        assert not destination.exists()
