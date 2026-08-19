"""Machine-readable evidence modes for DGAF truth-layer enforcement.

Modes are intentionally ordered by evidentiary strength. A stronger mode may
consume artifacts produced by a weaker mode, but CI must prevent weaker-mode
artifacts from being represented as stronger evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Literal, TypeVar, cast

EvidenceMode = Literal["synthetic", "integration", "empirical", "production"]

_MODE_ORDER: dict[EvidenceMode, int] = {
    "synthetic": 1,
    "integration": 2,
    "empirical": 3,
    "production": 4,
}

F = TypeVar("F", bound=Callable[..., Any])


@dataclass(frozen=True)
class EvidenceMetadata:
    mode: EvidenceMode
    claim_id: str | None = None
    run_id_required: bool = False
    dataset_required: bool = False


def evidence_mode(
    mode: EvidenceMode,
    *,
    claim_id: str | None = None,
    run_id_required: bool | None = None,
    dataset_required: bool | None = None,
) -> Callable[[F], F]:
    """Annotate a callable with an explicit evidence tier.

    The decorator is metadata-only by design. Runtime/CI validators are
    responsible for enforcing whether an artifact is allowed to satisfy a
    stronger evidence claim.
    """
    if mode not in _MODE_ORDER:
        raise ValueError(f"Unsupported evidence mode: {mode}")

    metadata = EvidenceMetadata(
        mode=mode,
        claim_id=claim_id,
        run_id_required=(mode in {"empirical", "production"})
        if run_id_required is None
        else run_id_required,
        dataset_required=(mode == "empirical")
        if dataset_required is None
        else dataset_required,
    )

    def decorate(fn: F) -> F:
        setattr(fn, "__evidence_metadata__", metadata)
        return cast(F, fn)

    return decorate


def evidence_rank(mode: EvidenceMode) -> int:
    return _MODE_ORDER[mode]


def can_satisfy(observed: EvidenceMode, required: EvidenceMode) -> bool:
    """Return whether an observed evidence tier may satisfy a requirement."""
    return evidence_rank(observed) >= evidence_rank(required)


__all__ = ["EvidenceMode", "EvidenceMetadata", "evidence_mode", "evidence_rank", "can_satisfy"]
