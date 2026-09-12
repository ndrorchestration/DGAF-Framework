from dataclasses import dataclass


@dataclass(frozen=True)
class BlindSpotRecord:
    finding_id: str
    discovered_by: frozenset[str]
    missed_by: frozenset[str]
    reproduction_evidence: tuple[str, ...]
    generated_detector: str | None = None
    review_status: str = "CANDIDATE"
    authoritative_effect: str = "NONE"


def validate_blindspot_record(record: BlindSpotRecord) -> None:
    errors: list[str] = []
    if not record.finding_id.strip():
        errors.append("finding_id is required")
    if not record.discovered_by:
        errors.append("discovered_by cannot be empty")
    if record.discovered_by & record.missed_by:
        errors.append("a detector cannot both discover and miss the same finding")
    if not record.reproduction_evidence:
        errors.append("reproduction_evidence cannot be empty")
    if record.review_status not in {"CANDIDATE", "REVIEWED", "REJECTED"}:
        errors.append("review_status is invalid")
    if record.authoritative_effect != "NONE":
        errors.append("blind-spot records cannot have authoritative effect")
    if errors:
        raise ValueError("; ".join(errors))
