from dataclasses import asdict, dataclass
from typing import Any


EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"


@dataclass(frozen=True)
class HistoricalReplayResult:
    case_id: str
    historical_defect: str
    detector: str
    expected_disposition: str
    observed_disposition: str
    observed_code: str | None
    detected_now: bool
    historical_prevention_claimed: bool = False
    evidence_class: str = EVIDENCE_CLASS
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0
    independent_validation_established: bool = False
    canonical_dgaf_efficacy: str = "NOT_ESTABLISHED"
    high_assurance: str = "NOT_AUTHORIZED"

    @property
    def replay_pass(self) -> bool:
        return self.detected_now and self.observed_disposition == self.expected_disposition

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_historical_replay_result(result: HistoricalReplayResult) -> None:
    """Validate the epistemic boundary of a retained historical-defect replay.

    A replay may record either detection or escape. Validation protects the claim
    ceiling; it deliberately does not convert a current detector result into a
    counterfactual claim about what would have happened historically.
    """

    errors = []
    if not result.case_id:
        errors.append("case_id is required")
    if not result.historical_defect:
        errors.append("historical_defect is required")
    if not result.detector:
        errors.append("detector is required")
    if result.historical_prevention_claimed:
        errors.append("historical prevention counterfactual is prohibited")
    if result.evidence_class != EVIDENCE_CLASS:
        errors.append(f"evidence_class must be {EVIDENCE_CLASS}")
    if result.authoritative_effect != "NONE":
        errors.append("authoritative_effect must be NONE")
    if result.scientific_state_effect != "NONE":
        errors.append("scientific_state_effect must be NONE")
    if result.scientific_n_increment != 0:
        errors.append("scientific_n_increment must be 0")
    if result.independent_validation_established:
        errors.append("historical replay cannot establish independent validation")
    if result.canonical_dgaf_efficacy != "NOT_ESTABLISHED":
        errors.append("historical replay cannot establish canonical DGAF efficacy")
    if result.high_assurance != "NOT_AUTHORIZED":
        errors.append("historical replay cannot authorize High-Assurance")

    if errors:
        raise ValueError("; ".join(errors))
