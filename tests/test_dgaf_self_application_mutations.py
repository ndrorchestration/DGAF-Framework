from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_dgaf_self_application_mutations.py"
REGISTRY = ROOT / "registry" / "dgaf_self_application_mutations_v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("dgaf_self_application_mutations", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_registry_is_bounded_and_complete():
    module = load_module()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cases = module.validate_registry(data)

    assert len(cases) == 8
    assert {case["validator"] for case in cases} == {
        "claim_hygiene",
        "control_state",
        "truth_layer",
        "registry_consistency",
    }
    assert all(case["expected_disposition"] == "BLOCKED" for case in cases)


def test_claim_ceiling_is_nonpromoting():
    module = load_module()

    assert module.EVIDENCE_CLASS == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert module.CLAIM_CEILING == {
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "external_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def test_summary_requires_every_mutation_to_be_detected_and_fail_closed():
    module = load_module()
    passed = [
        {"detected": True, "fail_closed": True},
        {"detected": True, "fail_closed": True},
    ]
    failed = [
        {"detected": True, "fail_closed": True},
        {"detected": False, "fail_closed": False},
    ]

    pass_summary = module.summarize(passed)
    fail_summary = module.summarize(failed)

    assert pass_summary["mutation_detection_rate"] == 1.0
    assert pass_summary["fail_closed_rate"] == 1.0
    assert pass_summary["all_expected_mutations_detected"] is True
    assert pass_summary["all_expected_mutations_fail_closed"] is True

    assert fail_summary["mutation_detection_rate"] == 0.5
    assert fail_summary["fail_closed_rate"] == 0.5
    assert fail_summary["all_expected_mutations_detected"] is False
    assert fail_summary["all_expected_mutations_fail_closed"] is False
