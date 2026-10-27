"""Research-only JUnit classification: never convert failed canonical CI to green.

Analyze the WHOLE Python 3.10 test run. Fail closed unless every failure is
one of exactly two unpromoted canonical lock-identity contract checks. The
caller must still exit with the original nonzero pytest status.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED = {
    "test_source_and_canonical_lock_identities_are_bound": (
        "5ea1c6fe5576eecc308a9adace47b7dc9b66735e9ed2bb4c8c9b729949d2825c",
        "be5239699db277731960d7336a8fbdb9c72bb31a39a97252e50e553bb83b161a",
    ),
    "test_every_direct_ci_pin_is_exactly_represented_in_every_lock": ("26.5.1", "26.10.1"),
}


def main() -> None:
    xml = Path("py310-isolated-repository-pytest.junit.xml")
    text = Path("py310-isolated-repository-pytest.log")
    status = Path("py310-isolated-repository-pytest.status")
    assert xml.is_file() and text.is_file() and status.is_file()
    assert status.read_text(encoding="utf-8").strip() == "pytest_exit_code=1", (
        "full repository pytest must remain red until canonical lock admission"
    )

    root = ET.parse(xml).getroot()
    assert root.tag in ("testsuite", "testsuites"), "unexpected JUnit structure"
    tests = list(root.iter("testcase"))
    assert len(tests) >= 2000, "suite too small for whole repository classification"
    failures = {}
    errors = []
    skipped = 0
    for case in tests:
        classname, name = case.get("classname", ""), case.get("name", "")
        failure = case.find("failure")
        error = case.find("error")
        if case.find("skipped") is not None:
            skipped += 1
        if error is not None:
            errors.append((classname, name, (error.text or "")[:500]))
        if failure is not None:
            identifier = (classname, name)
            assert identifier not in failures, "duplicate failure identity"
            failures[identifier] = (failure.get("message") or "") + "\n" + (failure.text or "")
    assert not errors, ("unexpected test errors", errors[:5])
    actual = {name for (cls, name) in failures if cls.endswith("test_ci_lock_contract")}
    assert actual == set(EXPECTED), ("wrong lock-contract failures", actual)
    assert len(failures) == len(EXPECTED), (
        "non-lock functional regression observed", list(failures)
    )
    for (classname, name), report in failures.items():
        assert classname.endswith("test_ci_lock_contract")
        assert all(fragment in report for fragment in EXPECTED[name]), (
            "canonical lock rejection changed meaning", name
        )
    out = {
        "schema": "DGAF_PY310_RESEARCH_LOCK_CONTRACT_FAILURE_CLASSIFIER_V1",
        "authority": "NOT_GRANTED",
        "scientific_n_increment": 0,
        "overall_test_status": "FAILED",
        "reason": "CANONICAL_SECURITY_LOCK_CONTRACTS_NOT_PROMOTED",
        "nonlock_functional_regression_failures": 0,
        "required_expected_lock_contract_failures": sorted(EXPECTED),
        "testcase_records": len(tests),
        "skipped_testcase_records": skipped,
        "junit_sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
        "pytest_log_sha256": hashlib.sha256(text.read_bytes()).hexdigest(),
        "exact_test_results": "NOT_ACCEPTED_FOR_RELEASE",
    }
    destination = Path("py310-isolated-regression-classification.json")
    destination.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("PY310_ALL_OTHER_TESTCASES_PASSED_BUT_CANONICAL_LOCK_CHECKS_REMAIN_RED")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
