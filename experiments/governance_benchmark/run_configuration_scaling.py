"""Neutral configuration-scaling falsification model.

Both conventional policy-as-code and DGAF are granted reusable shared semantic
modules plus per-scope bindings. This avoids manufacturing a DGAF advantage by
forcing the comparator to duplicate rules.

Synthetic engineering evidence only.
"""

from __future__ import annotations

import json
from typing import Any

SCOPE_COUNTS = (1, 8, 64, 512)
SEMANTIC_CONTROLS = (
    "ACTION_AUTHORIZED",
    "TOOL_ALLOWED",
    "TARGET_ALLOWED",
    "DELEGATED_REQUESTER_AUTHORIZED",
    "NO_TOKEN_REPLAY",
    "INTENT_BOUND",
    "WORKLOAD_ATTESTED",
    "CHILD_SCOPE_SUBSET",
    "CLAIM_EVIDENCE_PRESENT_AND_FRESH",
    "INDEPENDENT_STATUS_REQUIRES_INDEPENDENT_VERIFICATION",
    "FLOW_PROVENANCE_KNOWN",
    "PROTECTED_EGRESS_REQUIRES_COMPOSITION_AUTHORIZATION",
)


def _architecture(kind: str, scope_count: int) -> dict[str, Any]:
    if kind not in {"C3_POLICY", "DGAF"}:
        raise ValueError(f"unsupported architecture: {kind}")

    module_key = "policy_modules" if kind == "C3_POLICY" else "guard_modules"
    binding_key = "policy_binding" if kind == "C3_POLICY" else "governance_contract"

    return {
        "architecture": kind,
        "semantic_version": "V1",
        module_key: [{"id": control, "version": 1} for control in SEMANTIC_CONTROLS],
        "scopes": [
            {
                "scope_id": f"SCOPE-{index:04d}",
                binding_key: "V1",
            }
            for index in range(scope_count)
        ],
    }


def canonical_bytes(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _update_semantics(payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    updated = json.loads(json.dumps(payload))
    updated["semantic_version"] = "V2"

    module_key = "policy_modules" if updated["architecture"] == "C3_POLICY" else "guard_modules"
    for module in updated[module_key]:
        if module["id"] == "INDEPENDENT_STATUS_REQUIRES_INDEPENDENT_VERIFICATION":
            module["version"] = 2
            break
    else:
        raise AssertionError("target semantic control missing")

    return updated, 1


def run() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for scope_count in SCOPE_COUNTS:
        policy = _architecture("C3_POLICY", scope_count)
        dgaf = _architecture("DGAF", scope_count)
        policy_updated, policy_edits = _update_semantics(policy)
        dgaf_updated, dgaf_edits = _update_semantics(dgaf)

        rows.append(
            {
                "scope_count": scope_count,
                "c3": {
                    "shared_semantic_modules": len(SEMANTIC_CONTROLS),
                    "scope_bindings": scope_count,
                    "semantic_update_artifacts_touched": policy_edits,
                    "canonical_config_bytes": canonical_bytes(policy),
                    "updated_canonical_config_bytes": canonical_bytes(policy_updated),
                },
                "dgaf": {
                    "shared_semantic_modules": len(SEMANTIC_CONTROLS),
                    "scope_bindings": scope_count,
                    "semantic_update_artifacts_touched": dgaf_edits,
                    "canonical_config_bytes": canonical_bytes(dgaf),
                    "updated_canonical_config_bytes": canonical_bytes(dgaf_updated),
                },
            }
        )

    structural_parity = all(
        row["c3"]["shared_semantic_modules"] == row["dgaf"]["shared_semantic_modules"]
        and row["c3"]["scope_bindings"] == row["dgaf"]["scope_bindings"]
        and row["c3"]["semantic_update_artifacts_touched"]
        == row["dgaf"]["semantic_update_artifacts_touched"]
        for row in rows
    )

    return {
        "version": "DGAF_CONFIGURATION_SCALING_PARITY_V1",
        "evidence_class": "SYNTHETIC_STRUCTURAL_FALSIFICATION_EVIDENCE",
        "scope_counts": list(SCOPE_COUNTS),
        "semantic_control_count": len(SEMANTIC_CONTROLS),
        "fairness_constraints": [
            "Both architectures receive reusable shared semantic modules.",
            "Both architectures receive one binding per governed scope.",
            "No comparator-specific rule duplication is imposed.",
            "A semantic change may be implemented once in the shared module layer.",
            "Canonical byte size is reported descriptively, not as a superiority metric.",
        ],
        "rows": rows,
        "summary": {
            "structural_scaling_parity": structural_parity,
            "c3_update_artifacts_touched": sorted(
                {row["c3"]["semantic_update_artifacts_touched"] for row in rows}
            ),
            "dgaf_update_artifacts_touched": sorted(
                {row["dgaf"]["semantic_update_artifacts_touched"] for row in rows}
            ),
            "scope_binding_growth": "LINEAR_FOR_BOTH",
            "semantic_update_growth": "CONSTANT_FOR_BOTH",
        },
        "falsification_outcome": (
            "NO_UNIQUE_CONFIGURATION_SCALING_ADVANTAGE_IN_NEUTRAL_REUSE_MODEL"
            if structural_parity
            else "STRUCTURAL_DIFFERENCE_OBSERVED"
        ),
        "interpretation_boundary": [
            "This model tests representation structure, not real operator time or production maintenance cost.",
            "Parity weakens claims of an inherent DGAF configuration-scaling advantage under reusable abstractions.",
            "Real integrations may differ because tooling, schemas, provenance, recovery, and lifecycle requirements differ.",
            "Canonical byte counts are descriptive and must not be treated as burden scores.",
        ],
        "claim_ceiling": [
            "SCIENTIFIC_N_INCREMENT_0",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
            "HIGH_ASSURANCE_NOT_AUTHORIZED",
        ],
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
