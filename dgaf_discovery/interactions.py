from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class ControlContract:
    control_id: str
    reads: frozenset[str] = frozenset()
    writes: frozenset[str] = frozenset()
    requires: frozenset[str] = frozenset()
    forbids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ControlInteraction:
    left: str
    right: str
    codes: tuple[str, ...]


def analyze_pairwise(controls):
    findings = []
    for left, right in combinations(controls, 2):
        codes = set()
        if left.writes & right.writes:
            codes.add("W")
        if (left.writes & right.reads) or (right.writes & left.reads):
            codes.add("R")
        if (left.requires & right.forbids) or (right.requires & left.forbids):
            codes.add("F")
        if codes:
            findings.append(
                ControlInteraction(
                    left.control_id,
                    right.control_id,
                    tuple(sorted(codes)),
                )
            )
    return tuple(findings)
