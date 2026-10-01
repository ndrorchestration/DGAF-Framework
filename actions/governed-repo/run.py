"""Entrypoint for the bounded Governed Repo composite Action.

All caller-controlled values arrive through environment variables and are
parsed as data. They are never interpolated into shell commands.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Optional

PACKAGE_SRC = Path(__file__).resolve().parents[2] / "packages" / "governed-repo" / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from governed_repo import (  # noqa: E402
    GateRequirement,
    GitHubAdapterInputError,
    PromotionPolicy,
    UpstreamDecision,
    assess_github_promotion,
)


class ActionInputError(ValueError):
    """Raised when the Action input contract is malformed or unsupported."""


def _env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise ActionInputError(f"{name} must be a non-empty string")
    return value


def _json_env(name: str) -> Any:
    raw = _env(name)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ActionInputError(f"{name} must contain valid JSON") from exc


def _bool(mapping: Mapping[str, Any], key: str, default: bool) -> bool:
    value = mapping.get(key, default)
    if type(value) is not bool:
        raise ActionInputError(f"policy.{key} must be boolean")
    return value


def _gate(raw: Any, index: int) -> GateRequirement:
    if not isinstance(raw, Mapping):
        raise ActionInputError(f"policy.required_gates[{index}] must be an object")

    allowed = {
        "gate_id",
        "gate_class",
        "required",
        "accepted_conclusions",
        "require_head_binding",
        "require_base_binding",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ActionInputError(f"policy.required_gates[{index}] contains unsupported keys: {sorted(unknown)}")

    gate_id = raw.get("gate_id")
    gate_class = raw.get("gate_class")
    if not isinstance(gate_id, str) or not gate_id.strip():
        raise ActionInputError(f"policy.required_gates[{index}].gate_id is required")
    if not isinstance(gate_class, str) or not gate_class.strip():
        raise ActionInputError(f"policy.required_gates[{index}].gate_class is required")

    conclusions = raw.get("accepted_conclusions", ["success"])
    if (
        not isinstance(conclusions, list)
        or not conclusions
        or any(not isinstance(item, str) or not item.strip() for item in conclusions)
    ):
        raise ActionInputError(
            f"policy.required_gates[{index}].accepted_conclusions " "must be a non-empty string array"
        )

    required = raw.get("required", True)
    head_binding = raw.get("require_head_binding", True)
    base_binding = raw.get("require_base_binding", False)
    for name, value in (
        ("required", required),
        ("require_head_binding", head_binding),
        ("require_base_binding", base_binding),
    ):
        if type(value) is not bool:
            raise ActionInputError(f"policy.required_gates[{index}].{name} must be boolean")

    return GateRequirement(
        gate_id=gate_id,
        gate_class=gate_class,
        required=required,
        accepted_conclusions=tuple(conclusions),
        require_head_binding=head_binding,
        require_base_binding=base_binding,
    )


def _policy(raw: Any) -> PromotionPolicy:
    if not isinstance(raw, Mapping):
        raise ActionInputError("policy must be an object")

    allowed = {
        "required_gates",
        "hold",
        "lifecycle_blocked",
        "require_evidence_acceptance",
        "require_claim_scope_acceptance",
        "require_mutation_policy_acceptance",
        "require_authority_resolution",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ActionInputError(f"policy contains unsupported keys: {sorted(unknown)}")

    raw_gates = raw.get("required_gates", [])
    if not isinstance(raw_gates, list):
        raise ActionInputError("policy.required_gates must be an array")

    return PromotionPolicy(
        required_gates=tuple(_gate(item, index) for index, item in enumerate(raw_gates)),
        hold=_bool(raw, "hold", False),
        lifecycle_blocked=_bool(raw, "lifecycle_blocked", False),
        require_evidence_acceptance=_bool(raw, "require_evidence_acceptance", False),
        require_claim_scope_acceptance=_bool(raw, "require_claim_scope_acceptance", False),
        require_mutation_policy_acceptance=_bool(raw, "require_mutation_policy_acceptance", False),
        require_authority_resolution=_bool(raw, "require_authority_resolution", False),
    )


def _decision(raw: Any, key: str) -> Optional[UpstreamDecision]:
    if raw is None:
        return None
    if not isinstance(raw, Mapping):
        raise ActionInputError(f"upstream_decisions.{key} must be null or an object")

    allowed = {"decision_class", "accepted", "reason_code", "receipt_id"}
    unknown = set(raw) - allowed
    if unknown:
        raise ActionInputError(f"upstream_decisions.{key} contains unsupported keys: {sorted(unknown)}")

    decision_class = raw.get("decision_class")
    accepted = raw.get("accepted")
    reason_code = raw.get("reason_code")
    receipt_id = raw.get("receipt_id")

    if not isinstance(decision_class, str) or not decision_class.strip():
        raise ActionInputError(f"upstream_decisions.{key}.decision_class must be a non-empty string")
    if type(accepted) is not bool:
        raise ActionInputError(f"upstream_decisions.{key}.accepted must be boolean")
    if not isinstance(reason_code, str) or not reason_code.strip():
        raise ActionInputError(f"upstream_decisions.{key}.reason_code must be a non-empty string")
    if receipt_id is not None and (not isinstance(receipt_id, str) or not receipt_id.strip()):
        raise ActionInputError(f"upstream_decisions.{key}.receipt_id must be null or a non-empty string")

    return UpstreamDecision(
        decision_class=decision_class,
        accepted=accepted,
        reason_code=reason_code,
        receipt_id=receipt_id,
    )


def _upstream(raw: Any) -> dict[str, Optional[UpstreamDecision]]:
    if not isinstance(raw, Mapping):
        raise ActionInputError("upstream_decisions must be an object")

    allowed = {"evidence", "claim_scope", "mutation_policy", "authority"}
    unknown = set(raw) - allowed
    if unknown:
        raise ActionInputError(f"upstream_decisions contains unsupported keys: {sorted(unknown)}")

    return {key: _decision(raw.get(key), key) for key in allowed}


def _write_output(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        raise ActionInputError("GITHUB_OUTPUT is not available")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def main() -> None:
    pull_request = _json_env("GOVERNED_REPO_PULL_REQUEST_JSON")
    check_runs = _json_env("GOVERNED_REPO_CHECK_RUNS_JSON")
    policy = _policy(_json_env("GOVERNED_REPO_POLICY_JSON"))
    upstream = _upstream(_json_env("GOVERNED_REPO_UPSTREAM_DECISIONS_JSON"))

    if not isinstance(pull_request, Mapping):
        raise ActionInputError("pull-request-json must decode to an object")
    if not isinstance(check_runs, list) or any(not isinstance(item, Mapping) for item in check_runs):
        raise ActionInputError("check-runs-json must decode to an array of objects")

    receipt = assess_github_promotion(
        _env("GOVERNED_REPO_REPOSITORY"),
        pull_request,
        check_runs,
        expected_base_sha=_env("GOVERNED_REPO_EXPECTED_BASE_SHA"),
        expected_head_sha=_env("GOVERNED_REPO_EXPECTED_HEAD_SHA"),
        observed_at=_env("GOVERNED_REPO_OBSERVED_AT"),
        policy=policy,
        evidence=upstream["evidence"],
        claim_scope=upstream["claim_scope"],
        mutation_policy=upstream["mutation_policy"],
        authority=upstream["authority"],
    )

    payload = receipt.to_dict()
    _write_output("eligible", "true" if receipt.eligible else "false")
    _write_output("reason_code", receipt.reason_code.value)
    _write_output(
        "promotion_receipt",
        json.dumps(payload, sort_keys=True, separators=(",", ":")),
    )
    _write_output("merge_executed", "false")
    _write_output("mutation_executed", "false")
    _write_output("authorization_effect", "NONE")


if __name__ == "__main__":
    try:
        main()
    except (ActionInputError, GitHubAdapterInputError) as exc:
        print(f"Governed Repo Action input error: {exc}", file=sys.stderr)
        raise SystemExit(2)
