from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class DiscoveryEnvelope:
    result_class: str
    mutation_scope: str = "EPHEMERAL_COPY_ONLY"
    mutation_performed_on_repository: bool = False
    authorizes_transition: bool = False
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0
    production_execution: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_discovery_envelope(envelope: DiscoveryEnvelope) -> None:
    errors = []
    if envelope.mutation_scope != "EPHEMERAL_COPY_ONLY":
        errors.append("mutation_scope must be EPHEMERAL_COPY_ONLY")
    if envelope.mutation_performed_on_repository:
        errors.append("repository mutation is forbidden")
    if envelope.authorizes_transition:
        errors.append("discovery output cannot authorize transitions")
    if envelope.scientific_state_effect != "NONE":
        errors.append("scientific_state_effect must be NONE")
    if envelope.scientific_n_increment != 0:
        errors.append("scientific_n_increment must be 0")
    if envelope.production_execution:
        errors.append("production_execution must be false")
    if errors:
        raise ValueError("; ".join(errors))
