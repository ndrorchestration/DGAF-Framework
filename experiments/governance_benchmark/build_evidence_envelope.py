"""Build a bounded evidence envelope for the DGAF governance benchmark."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "build_evidence_manifest.py"

spec = importlib.util.spec_from_file_location("benchmark_manifest", MANIFEST_PATH)
assert spec and spec.loader
manifest_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest_module)


def git_head(repo_root: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()


def build_envelope(repo_root: Path) -> dict[str, Any]:
    manifest = manifest_module.build_manifest()
    return {
        "version": "DGAF_GOVERNANCE_BENCHMARK_EVIDENCE_ENVELOPE_V1",
        "repository_commit": git_head(repo_root),
        "verification_class": "SAME_SYSTEM_LOCAL_ENGINEERING_VERIFICATION",
        "evidence_scope": {
            "fixed_cases": 13,
            "one_field_mutations": manifest["entries"]["mutations"]["case_count"],
            "same_domain_interactions": manifest["entries"]["same_domain_interactions"]["case_count"],
            "cross_domain_interactions": manifest["entries"]["cross_domain_interactions"]["case_count"],
        },
        "canonical_layer_digests": {name: entry["canonical_sha256"] for name, entry in manifest["entries"].items()},
        "supported_statements": [
            "The bounded synthetic benchmark executed according to its declared decision logic.",
            "DGAF produced the expected decision for all current fixed synthetic fixtures.",
            "The deterministic mutation and interaction suites matched their declared expectations.",
            "Canonical decision-relevant digests are stable across repeated unchanged executions.",
        ],
        "prohibited_inferences": [
            "DGAF is state of the art.",
            "DGAF is generally safer than alternative governance systems.",
            "DGAF efficacy is established.",
            "DGAF has independent validation.",
            "DGAF is production certified or regulatorily compliant.",
            "Scientific N has increased.",
        ],
        "state_projection": {
            "SCIENTIFIC_N_INCREMENT": 0,
            "INDEPENDENT_VALIDATION": "NOT_ESTABLISHED",
            "CANONICAL_DGAF_EFFICACY": "NOT_ESTABLISHED",
            "STATE_OF_THE_ART": "NOT_ESTABLISHED",
            "HIGH_ASSURANCE": "NOT_AUTHORIZED",
        },
        "manifest": manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo_root = ROOT.parents[1]
    envelope = build_envelope(repo_root)
    encoded = json.dumps(envelope, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
