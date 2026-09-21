from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from scripts.aoss_stage_a.runtime_binding import (
    CONTRACT_REL,
    LOCK_REL,
    RuntimeBindingError,
    RuntimeFacts,
    load_runtime_contract,
    verify_runtime_binding,
)

ROOT = Path(__file__).resolve().parents[1]


def _lock_digest() -> str:
    return hashlib.sha256((ROOT / LOCK_REL).read_bytes()).hexdigest()


def _facts(**changes: object) -> RuntimeFacts:
    values: dict[str, object] = {
        "implementation": "cpython",
        "version": "3.12.3",
        "platform_system": "Linux",
        "platform_machine": "x86_64",
        "executable": "/isolated/bin/python",
        "prefix": "/isolated",
        "base_prefix": "/isolated",
    }
    values.update(changes)
    return RuntimeFacts(**values)  # type: ignore[arg-type]


def test_runtime_contract_selects_one_exact_interpreter_and_empty_direct_dependency_lock() -> None:
    contract = load_runtime_contract(ROOT)

    assert contract["record_type"] == "AOSS_V0_6_STAGE_A_RUNTIME_BINDING"
    assert contract["status"] == "PROPOSED_NON_COLLECTING_RUNTIME_BINDING"
    assert contract["controller_issue"] == 901
    assert contract["interpreter"] == {
        "implementation": "cpython",
        "version": "3.12.3",
    }
    assert contract["dependency_lock"]["path"] == LOCK_REL
    assert contract["dependency_lock"]["sha256"] == _lock_digest()
    assert contract["dependency_lock"]["direct_third_party_dependencies"] == []
    assert contract["installed_environment_manifest_required_before_collection"] is True
    assert contract["source_driver_binding"] == "NOT_ESTABLISHED"
    assert contract["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert contract["scientific_n_increment"] == 0

    requirement_lines = [
        line
        for line in (ROOT / LOCK_REL).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert requirement_lines == []


def test_exact_runtime_candidate_verifies_without_promoting_collection_readiness() -> None:
    report = verify_runtime_binding(ROOT, _facts())

    assert report["runtime_binding"] == "PASS_PROSPECTIVE_NON_COLLECTING"
    assert report["implementation"] == "cpython"
    assert report["version"] == "3.12.3"
    assert report["dependency_lock_sha256"] == _lock_digest()
    assert report["installed_environment_manifest"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("facts", "code"),
    [
        (_facts(implementation="pypy"), "RUNTIME_IMPLEMENTATION_MISMATCH"),
        (_facts(version="3.12.4"), "RUNTIME_VERSION_MISMATCH"),
        (_facts(version="3.11.9"), "RUNTIME_VERSION_MISMATCH"),
    ],
)
def test_interpreter_drift_fails_closed(facts: RuntimeFacts, code: str) -> None:
    with pytest.raises(RuntimeBindingError, match=code):
        verify_runtime_binding(ROOT, facts)


def test_dependency_lock_byte_drift_fails_closed(tmp_path: Path) -> None:
    contract = load_runtime_contract(ROOT)
    lock = tmp_path / "requirements-aoss-stage-a.lock"
    lock.write_bytes((ROOT / LOCK_REL).read_bytes() + b"unexpected-package==1.0\n")

    with pytest.raises(RuntimeBindingError, match="DEPENDENCY_LOCK_DIGEST_MISMATCH"):
        verify_runtime_binding(ROOT, _facts(), contract=contract, lock_path=lock)


def test_platform_is_observed_but_not_silently_frozen_by_this_tranche() -> None:
    report = verify_runtime_binding(
        ROOT,
        _facts(platform_system="Windows", platform_machine="AMD64"),
    )

    assert report["platform_system"] == "Windows"
    assert report["platform_machine"] == "AMD64"
    assert report["platform_binding"] == "OBSERVED_NOT_ACCEPTED"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"


def test_contract_location_is_stable() -> None:
    assert CONTRACT_REL == "registry/aoss_v0_6_stage_a_runtime_binding_v1.json"
