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

def compute_transition_coverage(states, legal, reached, exercised, forbidden, rejected):
    return TransitionCoverage(
        len(states), len(states & reached), len(legal), len(legal & exercised),
        len(forbidden), len(forbidden & rejected)
    )
