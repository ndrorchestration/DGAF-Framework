"""Build a stable evidence manifest for the bounded DGAF governance benchmark.

Raw benchmark reports may contain informational runtime timing. The canonical
digests produced here exclude unstable timing fields and retain decision-relevant
content only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load_module(name: str, filename: str):
    path = ROOT / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


benchmark = load_module("benchmark", "run_benchmark.py")
mutations = load_module("mutations", "run_mutations.py")
interactions = load_module("interactions", "run_interactions.py")
cross_domain = load_module("cross_domain", "run_cross_domain.py")


def canonicalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonicalize(item) for key, item in sorted(value.items()) if key != "elapsed_ns_informational"}
    if isinstance(value, list):
        return [canonicalize(item) for item in value]
    return value


def digest(value: Any) -> str:
    encoded = json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_manifest() -> dict[str, Any]:
    reports = {
        "fixed": benchmark.run(),
        "mutations": mutations.run_mutations(),
        "same_domain_interactions": interactions.run_interactions(),
        "cross_domain_interactions": cross_domain.run_cross_domain_interactions(),
    }

    entries: dict[str, Any] = {}
    for name, report in reports.items():
        entries[name] = {
            "canonical_sha256": digest(report),
            "evidence_class": report["evidence_class"],
            "claim_ceiling": report["claim_ceiling"],
        }
        if "summary" in report:
            entries[name]["summary"] = report["summary"]
        if "mutation_count" in report:
            entries[name]["case_count"] = report["mutation_count"]
            entries[name]["all_pass"] = report["all_pass"]
        if "interaction_count" in report:
            entries[name]["case_count"] = report["interaction_count"]
            entries[name]["all_pass"] = report["all_pass"]

    return {
        "version": "DGAF_GOVERNANCE_BENCHMARK_EVIDENCE_MANIFEST_V1",
        "digest_scope": "DECISION_RELEVANT_CONTENT_EXCLUDING_INFORMATIONAL_TIMING",
        "non_effects": [
            "NO_SCIENTIFIC_N_INCREMENT",
            "NO_INDEPENDENT_VALIDATION",
            "NO_CANONICAL_EFFICACY",
            "NO_STATE_OF_THE_ART_CLAIM",
        ],
        "entries": entries,
    }


def main() -> int:
    print(json.dumps(build_manifest(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
