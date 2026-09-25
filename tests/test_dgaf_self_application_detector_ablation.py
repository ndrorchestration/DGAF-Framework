from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_dgaf_self_application_detector_ablation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("dgaf_detector_ablation", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_summary_counts_unique_escapes_without_overclaiming():
    module = load_module()
    records = [
        {
            "baseline_detected": True,
            "ablations": {
                "claim_hygiene": {"escaped": True},
                "control_state": {"escaped": False},
                "truth_layer": {"escaped": False},
                "registry_consistency": {"escaped": False},
            },
        }
    ]
    summary = module.summarize(records)
    assert summary["baseline_detection_rate"] == 1.0
    assert summary["unique_escape_count_by_ablated_detector"]["claim_hygiene"] == 1
    assert "does not imply" in summary["interpretation"]


def test_claim_ceiling_is_inherited_and_nonpromoting():
    module = load_module()
    assert module.EVIDENCE_CLASS == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert module.CLAIM_CEILING["scientific_n_increment"] == 0
    assert module.CLAIM_CEILING["independent_validation"] == "NOT_ESTABLISHED"
    assert module.CLAIM_CEILING["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert module.CLAIM_CEILING["high_assurance"] == "NOT_AUTHORIZED"
