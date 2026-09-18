#!/usr/bin/env python3
"""Summarize bounded synthetic DGAF/PDMAL assurance evidence.

This helper consumes only synthetic/non-secret artifacts produced by CI. It is
not an empirical analysis and cannot increment scientific N or establish DGAF
efficacy.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from defusedxml import ElementTree as ET

CLASSIFICATION = "SYNTHETIC_ENGINEERING_ASSURANCE_ONLY"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def junit_counts(paths: list[Path]) -> dict[str, int]:
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for path in paths:
        root = ET.parse(path).getroot()
        suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
        if not suites:
            raise ValueError(f"{path} does not contain a JUnit testsuite")
        for suite in suites:
            for key in totals:
                totals[key] += int(suite.attrib.get(key, "0"))
    return totals


def validate_full_timing(data: dict[str, Any]) -> None:
    if data.get("evidence_class") != "P4_MODE_T_SYNTHETIC_FULL_PILOT_TASK_TIMING_V1":
        raise ValueError("unexpected full-task timing evidence class")
    if data.get("total_trials_per_repetition") != 9000:
        raise ValueError("full synthetic task shape must contain 9,000 trials")
    if data.get("synthetic_seed_count_per_repetition") != 50:
        raise ValueError("full synthetic task shape must contain 50 seeds")
    if data.get("trials_per_seed") != 180:
        raise ValueError("full synthetic task shape must contain 180 trials per seed")
    if data.get("empirical_data_collection") is not False:
        raise ValueError("synthetic timing must not collect empirical data")
    if data.get("protected_material_present") is not False:
        raise ValueError("synthetic timing must not use protected material")
    if data.get("pilot_authorized") is not False:
        raise ValueError("synthetic timing must not authorize the pilot")
    if data.get("empirical_n") != 0:
        raise ValueError("synthetic timing must preserve empirical N=0")


def validate_partial_timing(data: dict[str, Any]) -> None:
    if data.get("evidence_class") != "P4_MODE_T_SYNTHETIC_TIMING_PARTIAL_V1":
        raise ValueError("unexpected component timing evidence class")
    if data.get("empirical_data_collection") is not False:
        raise ValueError("component timing must not collect empirical data")
    if data.get("pilot_authorized") is not False:
        raise ValueError("component timing must not authorize the pilot")
    if data.get("numeric_w_selected") is not False:
        raise ValueError("synthetic timing cannot select W")
    if data.get("w_proposal_eligible") is not False:
        raise ValueError("synthetic timing cannot make W proposal eligible")

    stages = data.get("stages")
    if not isinstance(stages, dict):
        raise ValueError("component timing stages are missing")
    for required in ("full_synthetic_matrix_timing", "locked_primary_analysis_timing"):
        stage = stages.get(required)
        if not isinstance(stage, dict) or stage.get("status") != "PASS":
            raise ValueError(f"{required} must PASS")


def validate_weighted_forman(data: dict[str, Any]) -> None:
    classification = data.get("epistemic_classification")
    protocol = data.get("protocol")
    if not isinstance(classification, dict) or not isinstance(protocol, dict):
        raise ValueError("weighted Forman result is malformed")
    if classification.get("track_a_state_effect") != "NONE":
        raise ValueError("weighted Forman study cannot change Track A state")
    if classification.get("canonical_dgaf_efficacy") != "NOT_ESTABLISHED":
        raise ValueError("weighted Forman study cannot establish DGAF efficacy")
    if protocol.get("total_trials") != 480:
        raise ValueError("weighted Forman matrix must contain 480 trials")
    if protocol.get("calibration_trials") != 240 or protocol.get("heldout_trials") != 240:
        raise ValueError("weighted Forman calibration/heldout split drifted")


def build_summary(
    full: dict[str, Any],
    partial: dict[str, Any],
    weighted: dict[str, Any],
    junit: dict[str, int],
) -> dict[str, Any]:
    validate_full_timing(full)
    validate_partial_timing(partial)
    validate_weighted_forman(weighted)

    if junit["failures"] or junit["errors"]:
        raise ValueError("synthetic assurance JUnit evidence contains failures/errors")

    stages = partial["stages"]
    weighted_protocol = weighted["protocol"]
    variance = weighted["variance_restoration"]

    return {
        "schema_version": 1,
        "classification": CLASSIFICATION,
        "source_sha": os.environ.get("SOURCE_SHA") or os.environ.get("GITHUB_SHA", "UNBOUND_LOCAL"),
        "empirical_data_used": False,
        "protected_material_used": False,
        "real_materialization_performed": False,
        "real_primary_analysis_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "measurements": {
            "junit": junit,
            "full_pilot_shape": {
                "synthetic_seed_count": full["synthetic_seed_count_per_repetition"],
                "trials_per_seed": full["trials_per_seed"],
                "total_trials": full["total_trials_per_repetition"],
                "duration_statistics": full["full_task_shape_duration_statistics"],
            },
            "component_matrix_timing": stages["full_synthetic_matrix_timing"],
            "synthetic_locked_analysis_timing": stages["locked_primary_analysis_timing"],
            "weighted_forman_falsification": {
                "total_trials": weighted_protocol["total_trials"],
                "calibration_trials": weighted_protocol["calibration_trials"],
                "heldout_trials": weighted_protocol["heldout_trials"],
                "variance_restoration": variance,
                "detector_summary": weighted["heldout_detector_summary"],
            },
        },
        "known_nonclosures": {
            "real_track_a_materialization": "NOT_ESTABLISHED",
            "materialization_receipt_event": "NOT_ESTABLISHED",
            "real_primary_analysis_authorization": "NOT_ESTABLISHED",
            "real_primary_analysis": "NOT_RUN",
            "external_transparency_timing": stages["external_transparency_retention_timing"]["status"],
            "artifact_publication_retention_timing": stages["artifact_publication_retention_timing"]["status"],
            "synthetic_tlock_encryption_timing": stages["synthetic_timelock_encryption_timing"]["status"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-timing", type=Path, required=True)
    parser.add_argument("--partial-timing", type=Path, required=True)
    parser.add_argument("--weighted-forman", type=Path, required=True)
    parser.add_argument("--junit", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.junit:
        raise ValueError("at least one --junit input is required")

    summary = build_summary(
        load_json(args.full_timing),
        load_json(args.partial_timing),
        load_json(args.weighted_forman),
        junit_counts(args.junit),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
