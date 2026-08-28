"""Deterministic repository-native governance-schema conformance evaluator.

Issue #32, synthetic evidence only. The evaluator does not exercise a model,
production deployment, or real workload. It generates a fixed corpus of valid
and intentionally invalid governance objects, validates them against the
versioned JSON Schema, and scores correct accept/reject classification.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

TARGET = 0.99
SEED = 20260828
DEFAULT_SCHEMA = Path(__file__).parents[1] / "schemas" / "governance.yml.schema.json"
DEFAULT_OUTPUT = Path("artifacts/governance_schema_conformance.json")

BASE = {
    "schema_version": "1.0.0",
    "session_id": "S208-CONFORMANCE",
    "roles": [
        {
            "name": "Amethyst",
            "curvature": 0.5,
            "contraction_rate": 0.8,
            "fallback_chain": ["COLLEEN"],
            "compliance_flags": {"nist_rmf": True, "eu_ai_act_articles": ["Art. 9"], "owasp_controls": ["ASI01"]},
            "thinking_tokens": 0,
            "tools": ["github"],
        }
    ],
    "default_precision": "BF16",
    "eval_suite_version": "schema-conformance-v1",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_variant(rng: random.Random, index: int) -> dict[str, Any]:
    doc = copy.deepcopy(BASE)
    doc["session_id"] = f"S{200 + index:03d}-CONFORMANCE"
    doc["roles"][0]["curvature"] = round(rng.uniform(0.0, 1.0), 6)
    doc["roles"][0]["contraction_rate"] = round(rng.uniform(0.01, 0.99), 6)
    if index % 2:
        doc["default_precision"] = "NVFP4"
    return doc


def invalid_variant(valid: dict[str, Any], mutation: int) -> dict[str, Any]:
    doc = copy.deepcopy(valid)
    role = doc["roles"][0]
    mutations = (
        lambda: doc.update({"unexpected": True}),
        lambda: role.update({"unexpected": True}),
        lambda: role.update({"contraction_rate": 1.0}),
        lambda: role.update({"curvature": -0.001}),
        lambda: doc.update({"session_id": "invalid-session"}),
        lambda: doc.update({"default_precision": "FP8"}),
        lambda: role.pop("name"),
        lambda: doc.pop("roles"),
        lambda: role.update({"fallback_chain": "COLLEEN"}),
        lambda: role.update({"compliance_flags": {"extra": True}}),
    )
    mutations[mutation % len(mutations)]()
    return doc


def build_corpus(n_variants: int = 1000) -> list[dict[str, Any]]:
    rng = random.Random(SEED)
    corpus: list[dict[str, Any]] = []
    half = n_variants // 2
    for i in range(half):
        corpus.append({"id": f"valid-{i:04d}", "expected_valid": True, "document": valid_variant(rng, i)})
    for i in range(n_variants - half):
        base = valid_variant(rng, half + i)
        corpus.append({"id": f"invalid-{i:04d}", "expected_valid": False, "document": invalid_variant(base, i)})
    return corpus


def evaluate(schema_path: Path, n_variants: int = 1000) -> dict[str, Any]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema)
    corpus = build_corpus(n_variants)
    results = []
    correct = 0
    for case in corpus:
        is_valid = not any(validator.iter_errors(case["document"]))
        passed = is_valid == case["expected_valid"]
        correct += int(passed)
        results.append(
            {
                "id": case["id"],
                "expected_valid": case["expected_valid"],
                "observed_valid": is_valid,
                "correct": passed,
            }
        )
    score = correct / len(results)
    return {
        "schema_version": "1.0",
        "evaluation": "governance_schema_conformance",
        "evidence_class": "SYNTHETIC",
        "seed": SEED,
        "schema_sha256": sha256_file(schema_path),
        "sample_count": len(results),
        "correct_count": correct,
        "score": score,
        "target": TARGET,
        "passed": score >= TARGET,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "failure_analysis": [r for r in results if not r["correct"]],
        "limitations": [
            "Synthetic mutation corpus only; not model-generated governance outputs.",
            "Conformance is measured against the versioned JSON Schema, not live Pydantic runtime behavior.",
            "Successful synthetic conformance does not establish DGAF efficacy or production reliability.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--variants", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.variants < 2:
        raise SystemExit("--variants must be >= 2")
    result = evaluate(args.schema, args.variants)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
