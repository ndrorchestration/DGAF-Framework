"""Non-admitting classifier of the whole Python 3.10 source-locked test result.

Only the two expected *unmodified* inherited research-branch source/hash-lock contract failures
may appear. This classification NEVER changes the original failing pytest
exit status. All evidence remains research-only.
"""

from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE_SHA256 = "71c54083bbfe492fc720a1d10269227926d1cd4ec7cfc5c0f46ce98ea53cd31b"
KNOWN_CONTRACT_SHA256 = "be5239699db277731960d7336a8fbdb9c72bb31a39a97252e50e553bb83b161a"
EXPECTED = {
    "test_source_and_canonical_lock_identities_are_bound": ("71c54083bbfe", "be5239699db2"),
    "test_every_direct_ci_pin_is_exactly_represented_in_every_lock": ('pip-audit==2.10.1', 'python_version'),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(xml: Path, log: Path, status: Path, source: Path, destination: Path) -> dict[str, object]:
    assert all(path.is_file() for path in (xml, log, status, source))
    assert _digest(source) == SOURCE_SHA256, "research source identity changed"
    assert SOURCE_SHA256 != KNOWN_CONTRACT_SHA256, "no longer a known stale-source condition"
    assert status.read_text(encoding="utf-8").strip() == "pytest_exit_code=1", (
        "canonical failure must be retained, never converted to pass"
    )

    root = ET.parse(xml).getroot()
    assert root.tag in {"testsuite", "testsuites"}
    cases = list(root.iter("testcase"))
    assert len(cases) >= 2000, "insufficient test suite coverage"

    failures: dict[tuple[str, str], str] = {}
    errors: list[tuple[str, str]] = []
    skipped = 0
    for case in cases:
        classname, name = case.get("classname", ""), case.get("name", "")
        identifier = (classname, name)
        failure, error = case.find("failure"), case.find("error")
        if case.find("skipped") is not None:
            skipped += 1
        if error is not None:
            errors.append(identifier)
        if failure is not None:
            assert identifier not in failures, "duplicate failed testcase"
            failures[identifier] = (failure.get("message") or "") + "\n" + (failure.text or "")

    assert not errors, ("unexpected test errors", errors[:5])
    assert len(failures) == len(EXPECTED), (
        "unexpected functional regressions or missing canonical failures",
        list(failures),
    )
    names = {name for (classname, name) in failures if classname.endswith("test_ci_lock_contract")}
    assert names == set(EXPECTED), ("only exact canonical lock contracts may be red", names)
    for (classname, name), report in failures.items():
        assert classname.endswith("test_ci_lock_contract"), ("unexpected failure location", classname, name)
        assert all(fragment in report for fragment in EXPECTED[name]), (
            "known lock failure changed meaning",
            name,
        )
    outcome: dict[str, object] = {
        "schema": "DGAF_MARKER_PY310_EXACT_SOURCE_REGRESSION_CLASSIFICATION_V1",
        "authority": "NOT_GRANTED",
        "scientific_n_increment": 0,
        "source_sha256": SOURCE_SHA256,
        "canonical_source_sha256": KNOWN_CONTRACT_SHA256,
        "overall_pytest_status": "FAILED",
        "canonical_lock_contract_status": "BLOCKED",
        "required_known_failed_tests": sorted(EXPECTED),
        "unexpected_functional_regression_failures": 0,
        "testcase_records": len(cases),
        "skipped_testcase_records": skipped,
        "junit_sha256": _digest(xml),
        "pytest_log_sha256": _digest(log),
        "release_authorization": "NOT_AUTHORIZED",
        "scientific_validity": "NOT_ESTABLISHED",
    }
    destination.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return outcome


def main() -> None:
    output = classify(
        Path("py310-isolated-repository-pytest.junit.xml"),
        Path("py310-isolated-repository-pytest.log"),
        Path("py310-isolated-repository-pytest.status"),
        Path("requirements-ci.txt"),
        Path("py310-isolated-regression-classification.json"),
    )
    print("ALL_NONLOCK_TESTS_PASSED__CANONICAL_SECURITY_LOCK_CONTRACTS_STILL_RED")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
