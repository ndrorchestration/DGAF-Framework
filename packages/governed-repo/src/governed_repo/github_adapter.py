"""Thin GitHub observation adapter for Governed Repo v0.

This module translates caller-supplied GitHub REST-shaped observations into
the pure Governed Repo records. It performs no network I/O and has no merge,
push, branch-protection mutation, release, deployment, or authorization
capability.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from .core import (
    ChangeIdentity,
    GateReceipt,
    PromotionPolicy,
    PromotionReceipt,
    UpstreamDecision,
    assess_promotion,
)


class GitHubAdapterInputError(ValueError):
    """Raised when a GitHub observation cannot be mapped without guessing."""


def _required_string(mapping: Mapping[str, Any], key: str, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise GitHubAdapterInputError(f"{context}.{key} must be a non-empty string")
    return value


def _required_mapping(mapping: Mapping[str, Any], key: str, context: str) -> Mapping[str, Any]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise GitHubAdapterInputError(f"{context}.{key} must be an object")
    return value


def _pull_number(pull_request: Mapping[str, Any]) -> int:
    value = pull_request.get("number")
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise GitHubAdapterInputError("pull_request.number must be a positive integer")
    return value


def _optional_merge_sha(pull_request: Mapping[str, Any]) -> Optional[str]:
    value = pull_request.get("merge_commit_sha")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise GitHubAdapterInputError("pull_request.merge_commit_sha must be null or a non-empty string")
    return value


def _check_source_identity(check_run: Mapping[str, Any]) -> Optional[str]:
    app = check_run.get("app")
    if app is None:
        return None
    if not isinstance(app, Mapping):
        raise GitHubAdapterInputError("check_run.app must be null or an object")

    slug = app.get("slug")
    app_id = app.get("id")

    if isinstance(slug, str) and slug.strip():
        if isinstance(app_id, int) and not isinstance(app_id, bool):
            return f"github-app:{slug}:{app_id}"
        return f"github-app:{slug}"

    if isinstance(app_id, int) and not isinstance(app_id, bool):
        return f"github-app-id:{app_id}"

    return None


def change_identity_from_pull_request(
    repository: str,
    pull_request: Mapping[str, Any],
    *,
    expected_base_sha: str,
    expected_head_sha: str,
    observed_at: str,
) -> ChangeIdentity:
    """Map one GitHub pull-request observation into an exact change identity."""

    if not isinstance(repository, str) or not repository.strip():
        raise GitHubAdapterInputError("repository must be a non-empty string")
    if not isinstance(expected_base_sha, str) or not expected_base_sha.strip():
        raise GitHubAdapterInputError("expected_base_sha must be a non-empty string")
    if not isinstance(expected_head_sha, str) or not expected_head_sha.strip():
        raise GitHubAdapterInputError("expected_head_sha must be a non-empty string")
    if not isinstance(observed_at, str) or not observed_at.strip():
        raise GitHubAdapterInputError("observed_at must be a non-empty string")

    base = _required_mapping(pull_request, "base", "pull_request")
    head = _required_mapping(pull_request, "head", "pull_request")

    return ChangeIdentity(
        repository=repository,
        change_id=f"pull/{_pull_number(pull_request)}",
        base_sha=expected_base_sha,
        head_sha=expected_head_sha,
        observed_base_sha=_required_string(base, "sha", "pull_request.base"),
        observed_head_sha=_required_string(head, "sha", "pull_request.head"),
        observed_at=observed_at,
        merge_ref_sha=_optional_merge_sha(pull_request),
    )


def gate_receipt_from_check_run(
    check_run: Mapping[str, Any],
    *,
    observed_at: Optional[str] = None,
) -> GateReceipt:
    """Map one GitHub check-run observation into a head-bound gate receipt.

    GitHub check-run payloads are treated as head-bound observations only.
    They do not, by themselves, establish base binding. Therefore base_sha is
    deliberately left unset. A policy that requires per-gate base binding
    will fail closed unless a different adapter supplies such evidence.
    """

    name = _required_string(check_run, "name", "check_run")
    status = _required_string(check_run, "status", "check_run")
    head_sha = _required_string(check_run, "head_sha", "check_run")

    conclusion = check_run.get("conclusion")
    if conclusion is not None and (not isinstance(conclusion, str) or not conclusion.strip()):
        raise GitHubAdapterInputError("check_run.conclusion must be null or a non-empty string")

    effective_observed_at = observed_at
    if effective_observed_at is None:
        for key in ("completed_at", "started_at"):
            value = check_run.get(key)
            if isinstance(value, str) and value.strip():
                effective_observed_at = value
                break
    if not isinstance(effective_observed_at, str) or not effective_observed_at.strip():
        raise GitHubAdapterInputError("check_run requires observed_at, completed_at, or started_at")

    return GateReceipt(
        gate_id=name,
        status=status,
        conclusion=conclusion,
        observed_at=effective_observed_at,
        source_identity=_check_source_identity(check_run),
        head_sha=head_sha,
        base_sha=None,
    )


def assess_github_promotion(
    repository: str,
    pull_request: Mapping[str, Any],
    check_runs: Sequence[Mapping[str, Any]],
    *,
    expected_base_sha: str,
    expected_head_sha: str,
    observed_at: str,
    policy: PromotionPolicy,
    evidence: Optional[UpstreamDecision] = None,
    claim_scope: Optional[UpstreamDecision] = None,
    mutation_policy: Optional[UpstreamDecision] = None,
    authority: Optional[UpstreamDecision] = None,
) -> PromotionReceipt:
    """Translate supplied GitHub observations, then invoke the pure evaluator."""

    identity = change_identity_from_pull_request(
        repository,
        pull_request,
        expected_base_sha=expected_base_sha,
        expected_head_sha=expected_head_sha,
        observed_at=observed_at,
    )
    receipts = tuple(gate_receipt_from_check_run(check) for check in check_runs)

    return assess_promotion(
        identity,
        policy,
        receipts,
        evidence=evidence,
        claim_scope=claim_scope,
        mutation_policy=mutation_policy,
        authority=authority,
    )
