from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PreservationRelation:
    relation_id: str
    protected_paths: tuple[str, ...]


@dataclass(frozen=True)
class RelationResult:
    passed: bool
    violations: tuple[str, ...]


def _read_path(record: dict[str, Any], path: str) -> Any:
    current: Any = record
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def evaluate_preservation(
    relation: PreservationRelation,
    before: dict[str, Any],
    after: dict[str, Any],
) -> RelationResult:
    violations = tuple(path for path in relation.protected_paths if _read_path(before, path) != _read_path(after, path))
    return RelationResult(passed=not violations, violations=violations)


def provenance_removal_requires_nonpass(
    before: dict[str, Any],
    after: dict[str, Any],
    provenance_path: str = "evidence.predecessor_sha",
    decision_path: str = "decision",
) -> RelationResult:
    before_provenance = _read_path(before, provenance_path)
    after_provenance = _read_path(after, provenance_path)
    after_decision = _read_path(after, decision_path)
    violation = before_provenance is not None and after_provenance is None and after_decision == "PASS"
    return RelationResult(
        passed=not violation,
        violations=(decision_path,) if violation else (),
    )
