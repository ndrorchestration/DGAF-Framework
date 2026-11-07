"""Synthetic negative controls for the non-admitting MessagePack split-auditor proof."""

from __future__ import annotations

import hashlib
import json

import pytest

from scripts import proof_py310_audit_isolation as proof


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_workspace(tmp_path, monkeypatch, *, msgpack: str = "1.2.3"):
    source = tmp_path / "requirements-ci.txt"
    workload = tmp_path / "py310-isolated-workload-requirements.txt"
    source.write_text(
        "# Synthetic source only — never use as canonical.\n"
        "black==26.10.1\n"
        "setuptools==84.2.1\n"
        "certifi==2026.10.23\n"
        f"msgpack=={msgpack}\n"
        "pip-audit==2.10.1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(proof, "SOURCE", source)
    monkeypatch.setattr(proof, "WORKLOAD_SOURCE", workload)
    return source, workload


def test_exact_patched_msgpack_source_removes_only_external_auditor(tmp_path, monkeypatch) -> None:
    _, workload = _source_workspace(tmp_path, monkeypatch)
    proof.make_source()
    pins = workload.read_text(encoding="utf-8")
    assert "msgpack==1.2.3" in pins
    assert "pip-audit==2.10.1" not in pins
    assert "requests==2.34.2" in pins
    assert "black==26.10.1" in pins


def test_unpatched_messagepack_is_rejected_before_resolver(tmp_path, monkeypatch) -> None:
    _source_workspace(tmp_path, monkeypatch, msgpack="1.2.2")
    with pytest.raises(AssertionError, match="patched MessagePack"):
        proof.make_source()


def test_duplicate_scanner_pin_is_rejected_before_resolver(tmp_path, monkeypatch) -> None:
    source, _ = _source_workspace(tmp_path, monkeypatch)
    source.write_text(source.read_text() + "pip-audit==2.10.1\n")
    with pytest.raises(AssertionError, match="exact scanner pin"):
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
