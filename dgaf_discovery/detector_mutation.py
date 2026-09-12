from dataclasses import dataclass
from typing import Any, Callable

Detector = Callable[[dict[str, Any]], bool]


@dataclass(frozen=True)
class PropertyCase:
    case_id: str
    specimen: dict[str, Any]
    expected_valid: bool


@dataclass(frozen=True)
class DetectorMutation:
    mutation_id: str
    family: str
    description: str
    detector: Detector


@dataclass(frozen=True)
class DetectorMutationResult:
    mutation_id: str
    family: str
    killed: bool
    distinguishing_cases: tuple[str, ...]


@dataclass(frozen=True)
class FamilyMutationSummary:
    attempted: int
    killed: int
    survived: int

    @property
    def score(self) -> float:
        return self.killed / self.attempted if self.attempted else 0.0


@dataclass(frozen=True)
class MutationCampaignResult:
    results: tuple[DetectorMutationResult, ...]
    by_family: dict[str, FamilyMutationSummary]
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0
    mutation_scope: str = "EPHEMERAL_COPY_ONLY"

    @property
    def attempted(self) -> int:
        return len(self.results)

    @property
    def killed(self) -> int:
        return sum(result.killed for result in self.results)

    @property
    def survived(self) -> int:
        return self.attempted - self.killed

    @property
    def score(self) -> float:
        return self.killed / self.attempted if self.attempted else 0.0


def run_mutation_campaign(
    canonical_detector: Detector,
    mutations: tuple[DetectorMutation, ...],
    cases: tuple[PropertyCase, ...],
) -> MutationCampaignResult:
    if not cases:
        raise ValueError("detector mutation campaign requires property cases")
    if not mutations:
        raise ValueError("detector mutation campaign requires detector mutations")

    for case in cases:
        observed = canonical_detector(case.specimen)
        if observed != case.expected_valid:
            raise ValueError(
                f"canonical detector disagrees with property oracle for {case.case_id}"
            )

    results = []
    family_counts: dict[str, list[int]] = {}
    for mutation in mutations:
        distinguishing_cases = tuple(
            case.case_id
            for case in cases
            if mutation.detector(case.specimen) != case.expected_valid
        )
        killed = bool(distinguishing_cases)
        results.append(
            DetectorMutationResult(
                mutation_id=mutation.mutation_id,
                family=mutation.family,
                killed=killed,
                distinguishing_cases=distinguishing_cases,
            )
        )
        counts = family_counts.setdefault(mutation.family, [0, 0])
        counts[0] += 1
        counts[1] += int(killed)

    by_family = {
        family: FamilyMutationSummary(
            attempted=counts[0],
            killed=counts[1],
            survived=counts[0] - counts[1],
        )
        for family, counts in family_counts.items()
    }
    return MutationCampaignResult(tuple(results), by_family)
