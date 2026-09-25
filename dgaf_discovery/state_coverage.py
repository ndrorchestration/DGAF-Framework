from dataclasses import dataclass


@dataclass(frozen=True)
class TransitionCoverage:
    specified_states: int
    reached_states: int
    legal_transitions: int
    exercised_legal_transitions: int
    forbidden_transitions: int
    rejected_forbidden_transitions: int

    @property
    def state_coverage(self):
        return self.reached_states / self.specified_states if self.specified_states else 1.0

    @property
    def legal_transition_coverage(self):
        return self.exercised_legal_transitions / self.legal_transitions if self.legal_transitions else 1.0

    @property
    def forbidden_rejection_coverage(self):
        return self.rejected_forbidden_transitions / self.forbidden_transitions if self.forbidden_transitions else 1.0


@dataclass(frozen=True)
class PositivePathLivenessResult:
    declared_legal_transitions: int
    exercised_legal_transitions: int
    unreachable_legal_transitions: tuple[tuple[str, str], ...]
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0

    @property
    def liveness_established_for_declared_scope(self):
        return not self.unreachable_legal_transitions


def compute_transition_coverage(states, legal, reached, exercised, forbidden, rejected):
    return TransitionCoverage(
        len(states),
        len(states & reached),
        len(legal),
        len(legal & exercised),
        len(forbidden),
        len(forbidden & rejected),
    )


def validate_positive_path_liveness(legal_transitions, exercised_transitions):
    """Validate that every declared legal transition has a positive-path exercise.

    This is an engineering liveness gate. It proves only reachability for the
    explicitly supplied legal-transition scope. It never authorizes a governance
    transition, increments scientific N, or establishes independent validation.
    """
    missing = tuple(sorted(set(legal_transitions) - set(exercised_transitions)))
    result = PositivePathLivenessResult(
        declared_legal_transitions=len(set(legal_transitions)),
        exercised_legal_transitions=len(set(legal_transitions) & set(exercised_transitions)),
        unreachable_legal_transitions=missing,
    )
    if result.authoritative_effect != "NONE":
        raise ValueError("positive-path liveness cannot have authoritative effect")
    if result.scientific_state_effect != "NONE" or result.scientific_n_increment != 0:
        raise ValueError("positive-path liveness cannot alter scientific state")
    if missing:
        formatted = ", ".join(f"{src}->{dst}" for src, dst in missing)
        raise ValueError(f"unreachable declared legal transitions: {formatted}")
    return result
