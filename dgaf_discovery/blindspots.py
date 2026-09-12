from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionRecord:
    finding_id: str
    discovered_by: frozenset[str]
    missed_by: frozenset[str] = frozenset()


def method_overlap(records: tuple[DetectionRecord, ...], left: str, right: str) -> float:
    left_findings = {record.finding_id for record in records if left in record.discovered_by}
    right_findings = {record.finding_id for record in records if right in record.discovered_by}
    union = left_findings | right_findings
    if not union:
        return 0.0
    return len(left_findings & right_findings) / len(union)


def unique_discovery_rate(records: tuple[DetectionRecord, ...], method: str) -> float:
    found = [record for record in records if method in record.discovered_by]
    if not found:
        return 0.0
    unique = sum(1 for record in found if record.discovered_by == frozenset({method}))
    return unique / len(found)


def unexplained_shared_misses(
    records: tuple[DetectionRecord, ...],
) -> dict[frozenset[str], tuple[str, ...]]:
    groups: dict[frozenset[str], list[str]] = {}
    for record in records:
        if len(record.missed_by) < 2:
            continue
        groups.setdefault(record.missed_by, []).append(record.finding_id)
    return {methods: tuple(ids) for methods, ids in groups.items()}
