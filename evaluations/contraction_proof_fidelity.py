"""Deterministic repository-native contraction-fidelity evaluator for Issue #32.

The fixture contains analytic diagonal matrices with independently specified
spectral radii and contraction labels. The evaluator recomputes eigenvalues
numerically and checks both the expected spectral radius and contraction decision.
This is synthetic evaluator evidence, not model or real-workload performance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

TARGET = 0.98
DEFAULT_FIXTURE = Path(__file__).parent / "fixtures" / "contraction_proof_fidelity_v1.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("evaluation") != "contraction_proof_fidelity":
        raise ValueError("fixture evaluation must be contraction_proof_fidelity")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 100:
        raise ValueError("fixture must contain exactly 100 cases")
    return data


def evaluate(path: Path) -> dict[str, Any]:
    fixture = load_fixture(path)
    results = []
    correct = 0
    for case in fixture["cases"]:
        matrix = np.asarray(case["matrix"], dtype=float)
        eigenvalues = np.linalg.eigvals(matrix)
        observed_radius = float(np.max(np.abs(eigenvalues)))
        observed_contraction = observed_radius < 1.0
        radius_ok = abs(observed_radius - case["expected_spectral_radius"]) <= 1e-12
        contraction_ok = observed_contraction == case["expected_contraction"]
        passed = radius_ok and contraction_ok
        correct += int(passed)
        results.append(
            {
                "id": case["id"],
                "expected_spectral_radius": case["expected_spectral_radius"],
                "observed_spectral_radius": observed_radius,
                "expected_contraction": case["expected_contraction"],
                "observed_contraction": observed_contraction,
                "radius_match": radius_ok,
                "classification_match": contraction_ok,
                "correct": passed,
            }
        )
    score = correct / len(results)
    return {
        "schema_version": "1.0",
        "evaluation": "contraction_proof_fidelity",
        "evidence_class": "SYNTHETIC",
        "fixture_sha256": sha256_file(path),
        "sample_count": len(results),
        "correct_count": correct,
        "score": score,
        "target": TARGET,
        "passed": score >= TARGET,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "failure_analysis": [r for r in results if not r["correct"]],
        "limitations": [
            "Synthetic analytic matrix corpus only; not model-generated proof outputs.",
            "The corpus intentionally uses diagonal matrices, so it validates the evaluator/scoring contract rather than general proof-generation ability.",
            "Passing this slice does not establish DGAF efficacy or real-workload contraction guarantees.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output", type=Path, default=Path("artifacts/contraction_proof_fidelity.json"))
    args = parser.parse_args()
    result = evaluate(args.fixture)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
