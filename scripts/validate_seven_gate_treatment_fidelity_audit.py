#!/usr/bin/env python3
"""Validate the source-bound seven-gate treatment fidelity audit."""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "docs/experiment/SEVEN_GATE_TREATMENT_FIDELITY_AUDIT_2026-09-08.json"
RUNNER = ROOT / "experiments/pdmal_pilot/run_canonical_epoch_004.py"
ADAPTER = ROOT / "experiments/pdmal_pilot/canonical_epoch_004_adapter.py"
BINDING = ROOT / "experiments/pdmal_pilot/pdmaltgl_gate_binding.py"
BASE_ADAPTER = ROOT / "experiments/pdmal_pilot/dgaf_tgl_adapter.py"

EXPECTED_BLOBS = {
    RUNNER: "eaedb40862684c33b3bff08d294338c74f7c9d92",
    ADAPTER: "95dc2f05196fe1df054fa9677bdfcd5d4d188081",
    BINDING: "11677608141e53de0a963eb62d6c5fbfa70f211b",
}
GATE_STATE_KEYWORDS = {
    "scpe_state",
    "convergence_state",
    "sentinel_state",
    "kappa_state",
    "demijoule_state",
    "phi_state",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def function_node(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"function not found: {name}")


def epoch004_consensus_state_keywords() -> set[str]:
    tree = ast.parse(RUNNER.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "CanonicalEpoch004Task":
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == "_dgaf_update":
                    for call in ast.walk(child):
                        if (
                            isinstance(call, ast.Call)
                            and isinstance(call.func, ast.Name)
                            and call.func.id == "ConsensusState"
                        ):
                            return {kw.arg for kw in call.keywords if kw.arg is not None}
    raise AssertionError("CanonicalEpoch004Task ConsensusState call not found")


def context_string_constants() -> set[str]:
    tree = ast.parse(BASE_ADAPTER.read_text(encoding="utf-8"))
    fn = function_node(tree, "_context_for_state")
    return {
        node.value
        for node in ast.walk(fn)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }


def main() -> int:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert audit["record_type"] == "DGAF_SEVEN_GATE_TREATMENT_FIDELITY_AUDIT"
    assert audit["classification"] == "POST_EMPIRICAL_SOURCE_AUDIT_NONEMPIRICAL"
    assert audit["scientific_n_increment"] == 0
    assert audit["epoch_004_primary_result_preserved"] is True
    assert audit["canonical_seven_gate_treatment_fidelity"] == "NOT_ESTABLISHED"
    assert audit["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert audit["fresh_canonical_empirical_epoch_authorized"] is False

    expected_gates = {
        "P-31_SCPE",
        "P-33_CONVERGENCE",
        "DEMIJOULE",
        "P-27_KAPPA",
        "P-29_SENTINEL",
        "P-32_PHI_CLOSURE",
        "P-30_APOGEE",
    }
    assert set(audit["gates"]) == expected_gates
    assert (
        audit["gates"]["P-30_APOGEE"]["fidelity"]
        == "ESTABLISHED_DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    )
    for name in expected_gates - {"P-30_APOGEE"}:
        assert audit["gates"][name]["fidelity"].startswith("NOT_ESTABLISHED")

    for path, expected in EXPECTED_BLOBS.items():
        actual = git_blob(path)
        assert actual == expected, f"source blob drift: {path}: {actual} != {expected}"

    supplied = epoch004_consensus_state_keywords()
    assert GATE_STATE_KEYWORDS.isdisjoint(supplied), (
        "Epoch 004 now explicitly supplies gate state; audit requires re-adjudication: "
        + ",".join(sorted(GATE_STATE_KEYWORDS & supplied))
    )

    context_keys = context_string_constants()
    for absent_semantic_input in {
        "payload",
        "is_stable",
        "sentinel_decision",
        "risk_decision",
    }:
        assert absent_semantic_input not in context_keys, (
            f"PDMAL context now supplies {absent_semantic_input}; "
            "audit requires re-adjudication"
        )

    adapter_source = ADAPTER.read_text(encoding="utf-8")
    assert "build_qualification_verifier_hook" in adapter_source
    assert "expected_sha256=QUALIFICATION_SHA256" in adapter_source
    assert "expected_profile_id=PROFILE_ID" in adapter_source
    assert "expected_profile_source_sha=PROFILE_SOURCE_SHA" in adapter_source

    binding_source = BINDING.read_text(encoding="utf-8")
    required_markers = (
        "across turns",
        'context.get("is_stable", True)',
        'context.get("sentinel_decision", context.get("risk_decision", "risk_ok"))',
        "pattern_score: float = 0.0",
        "continuous_score: float = 0.0",
        "length_boost: float = 0.0",
    )
    for marker in required_markers:
        assert marker in binding_source, f"binding source marker drifted: {marker}"

    print("SEVEN_GATE_TREATMENT_FIDELITY_AUDIT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
