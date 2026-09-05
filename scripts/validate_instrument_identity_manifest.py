#!/usr/bin/env python3
"""Validate DGAF numerical/control instrument identity without resolving authority.

The validator intentionally treats unresolved contradictions as blocked. It may
confirm that a contradiction is represented correctly, but it never selects a
normalization, threshold, alias, dependency, or canonical formula on the
project's behalf.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST = Path("docs/governance/instrument_identity_manifest_2026-09-04.json")
EXPECTED_BOUNDARY = "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0"
REQUIRED_FIELDS = {
    "instrument_id",
    "instrument_version",
    "instrument_type",
    "canonical_source",
    "formula_or_algorithm",
    "parameter_set",
    "score_range",
    "thresholds_or_predicates",
    "scope",
    "authority",
    "binding_strength",
    "implementation_ref",
    "source_commit",
    "execution_run",
    "execution_timestamp",
    "upstream_dependencies",
    "epistemic_status",
}


def _fail(message: str) -> None:
    raise ValueError(message)


def _by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    instruments = data.get("instruments")
    if not isinstance(instruments, list) or not instruments:
        _fail("instruments must be a non-empty list")
    result: dict[str, dict[str, Any]] = {}
    for instrument in instruments:
        if not isinstance(instrument, dict):
            _fail("instrument rows must be objects")
        missing = REQUIRED_FIELDS - instrument.keys()
        if missing:
            _fail(f"{instrument.get('instrument_id', '<unknown>')}: missing fields {sorted(missing)}")
        instrument_id = instrument["instrument_id"]
        if not isinstance(instrument_id, str) or not instrument_id:
            _fail("instrument_id must be a non-empty string")
        if instrument_id in result:
            _fail(f"duplicate instrument_id: {instrument_id}")
        result[instrument_id] = instrument
    return result


def validate_manifest(data: dict[str, Any]) -> None:
    if data.get("status") != "NON-AUTHORITATIVE_PRE-CANONICALIZATION":
        _fail("manifest must remain non-authoritative before explicit canonicalization")
    if data.get("scientific_boundary") != EXPECTED_BOUNDARY:
        _fail("scientific boundary changed")

    prohibited = set(data.get("prohibitions", []))
    required_prohibitions = {
        "silent weight normalization",
        "silent threshold selection",
        "alias collapse",
        "historical-score promotion",
    }
    if not required_prohibitions.issubset(prohibited):
        _fail("required anti-promotion prohibitions are missing")

    instruments = _by_id(data)

    for instrument_id, instrument in instruments.items():
        deps = instrument["upstream_dependencies"]
        if not isinstance(deps, list):
            _fail(f"{instrument_id}: upstream_dependencies must be a list")
        for dep in deps:
            if dep not in instruments:
                _fail(f"{instrument_id}: missing upstream dependency {dep}")
        if instrument.get("audit_status") == "CONTRADICTION":
            if not str(instrument["binding_strength"]).startswith("BLOCKED"):
                _fail(f"{instrument_id}: contradiction must remain blocked")
            if "UNRESOLVED" not in instrument["epistemic_status"]:
                _fail(f"{instrument_id}: contradiction must remain epistemically unresolved")

    qa11q = instruments["QA-11Q-ARTIFACT-v1"]
    params = qa11q["parameter_set"]
    weight_sum = float(params["declared_default_weight_sum"])
    divisor = float(params["normalization_divisor"])
    derived_max = weight_sum / divisor
    recorded_max = float(params["derived_theoretical_max"])
    if not math.isclose(weight_sum, 1.5, rel_tol=0.0, abs_tol=1e-12):
        _fail("QA-11Q audit must preserve declared weight sum 1.50 until authority resolves it")
    if not math.isclose(divisor, 11.0, rel_tol=0.0, abs_tol=1e-12):
        _fail("QA-11Q audit must preserve declared divisor 11 until authority resolves it")
    if not math.isclose(derived_max, recorded_max, rel_tol=0.0, abs_tol=1e-12):
        _fail("QA-11Q derived theoretical maximum is inconsistent")
    threshold = float(qa11q["thresholds_or_predicates"]["P-11_artifact_quality"])
    reachable = derived_max >= threshold
    if reachable:
        _fail("QA-11Q P-11 threshold unexpectedly became reachable without an authority decision")
    if qa11q.get("diagnostics", {}).get("threshold_reachable_under_declared_formula") is not False:
        _fail("QA-11Q contradiction diagnostic must record threshold as unreachable")

    gate11q = instruments["GATE-11Q-v2"]
    if gate11q["instrument_id"] == qa11q["instrument_id"]:
        _fail("GATE-11Q and QA-11Q scoring must remain distinct instrument identities")
    if gate11q["upstream_dependencies"]:
        _fail("GATE-11Q must not gain an inferred QA-11Q dependency without authority evidence")
    if "distinct" not in gate11q.get("diagnostics", {}).get("lineage", ""):
        _fail("GATE-11Q audit must explicitly preserve distinct lineage")

    axis = instruments["AXIS-v1.2"]
    apogee_axis = instruments["APOGEE-AXIS-RUBRIC-v1"]
    if axis["score_range"] == apogee_axis["score_range"] and axis["formula_or_algorithm"] == apogee_axis["formula_or_algorithm"]:
        _fail("AXIS contradiction was silently collapsed")
    if "AXIS-v1.2" not in apogee_axis["upstream_dependencies"]:
        _fail("Apogee AXIS derivative must preserve explicit AXIS lineage")
    if not str(apogee_axis["binding_strength"]).startswith("BLOCKED"):
        _fail("Apogee AXIS derivative remains blocked while lineage/formula differs")

    reson = instruments["RESON-HARMONIC-v1"]
    observed = reson["thresholds_or_predicates"]["observed_thresholds"]
    if sorted(float(x) for x in observed) != [0.75, 0.85]:
        _fail("Reson threshold contradiction must preserve both observed thresholds")

    ahg_analysis = instruments["AHG-ANALYSIS-v1"]
    ahg_params = ahg_analysis["parameter_set"]
    if not math.isclose(float(ahg_params["declared_weight_sum"]), 1.7, rel_tol=0.0, abs_tol=1e-12):
        _fail("AHG divergence audit must preserve observed weight sum 1.70")
    if ahg_params["explicit_normalization"] is not False:
        _fail("AHG divergence normalization must remain unresolved, not silently normalized")

    for instrument_id in ("P42-RECOVERY-v1", "KAPPA-EVAL-v3.6"):
        instrument = instruments[instrument_id]
        if instrument["audit_status"] != "CONFIRMED_IMPLEMENTATION":
            _fail(f"{instrument_id}: implemented bounded identity unexpectedly downgraded")
        if not instrument["implementation_ref"]:
            _fail(f"{instrument_id}: confirmed implementation requires implementation_ref")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    validate_manifest(data)
    print(f"PASS: {args.manifest} preserves fail-closed instrument lineage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
