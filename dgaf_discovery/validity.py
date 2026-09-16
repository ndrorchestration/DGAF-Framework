from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum


class ValidityState(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


class DependencyRelation(str, Enum):
    REQUIRES_VALIDITY = "REQUIRES_VALIDITY"
    DERIVED_FROM = "DERIVED_FROM"
    SUPPORTS_REQUIRED = "SUPPORTS_REQUIRED"
    SUPPORTS_CONTRIBUTORY = "SUPPORTS_CONTRIBUTORY"
    ASSUMES = "ASSUMES"
    DEFEATS = "DEFEATS"
    MITIGATES = "MITIGATES"
    SUPERSEDES = "SUPERSEDES"
    PRESENTS = "PRESENTS"
    REFERENCES = "REFERENCES"
    LINEAGE = "LINEAGE"
    AUTHORIZES = "AUTHORIZES"


class ImpactDisposition(str, Enum):
    NO_EFFECT = "NO_EFFECT"
    STALE_PROJECTION = "STALE_PROJECTION"
    REVERIFY = "REVERIFY"
    SUSPEND = "SUSPEND"
    SUPERSEDE = "SUPERSEDE"
    INVALIDATE = "INVALIDATE"


@dataclass(frozen=True)
class ValidityEvent:
    event_id: str
    subject_ref: str
    prior_state: ValidityState
    new_state: ValidityState
    cause_code: str
    evidence_refs: tuple[str, ...]
    authority_scope: str
    decision_ref: str
    classification: str = "ENGINEERING_DISCOVERY_ONLY"
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0


@dataclass(frozen=True)
class DependencyEdge:
    source_ref: str
    target_ref: str
    relation: DependencyRelation
    source_evidence_ref: str


@dataclass(frozen=True)
class ImpactFinding:
    ref: str
    disposition: ImpactDisposition
    reason: str
    via: tuple[str, ...]


@dataclass(frozen=True)
class ImpactAssessment:
    subject_ref: str
    findings: tuple[ImpactFinding, ...]
    unresolved_paths: tuple[str, ...]
    classification: str = "ENGINEERING_DISCOVERY_ONLY"
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0

    def disposition_for(self, ref: str):
        for finding in self.findings:
            if finding.ref == ref:
                return finding.disposition
        return None


def validate_validity_event(event: ValidityEvent) -> None:
    if not isinstance(event.prior_state, ValidityState):
        raise ValueError("prior_state must use ValidityState")
    if not isinstance(event.new_state, ValidityState):
        raise ValueError("new_state must use ValidityState")
    if event.prior_state is event.new_state:
        raise ValueError("validity state transition must change state")
    if not event.event_id:
        raise ValueError("event_id is required")
    if not event.subject_ref:
        raise ValueError("subject_ref is required")
    if not event.cause_code:
        raise ValueError("cause_code is required")
    if not event.evidence_refs or any(not ref for ref in event.evidence_refs):
        raise ValueError("evidence_refs must contain at least one non-empty reference")
    if not event.authority_scope:
        raise ValueError("authority_scope is required")
    if not event.decision_ref:
        raise ValueError("decision_ref is required")
    if event.classification != "ENGINEERING_DISCOVERY_ONLY":
        raise ValueError("validity events in the discovery harness are engineering-discovery only")
    if event.authoritative_effect != "NONE":
        raise ValueError("validity events in the discovery harness cannot have authoritative effect")
    if event.scientific_state_effect != "NONE" or event.scientific_n_increment != 0:
        raise ValueError("validity events in the discovery harness cannot alter scientific state")


def validate_dependency_edge(edge: DependencyEdge) -> None:
    if not edge.source_ref or not edge.target_ref:
        raise ValueError("dependency edges require source_ref and target_ref")
    if not isinstance(edge.relation, DependencyRelation):
        raise ValueError("relation must use DependencyRelation")
    if not edge.source_evidence_ref:
        raise ValueError("dependency edges require source_evidence_ref")


_PROPAGATION = {
    DependencyRelation.REQUIRES_VALIDITY: ImpactDisposition.REVERIFY,
    DependencyRelation.DERIVED_FROM: ImpactDisposition.REVERIFY,
    DependencyRelation.SUPPORTS_REQUIRED: ImpactDisposition.SUSPEND,
    DependencyRelation.SUPPORTS_CONTRIBUTORY: ImpactDisposition.REVERIFY,
    DependencyRelation.ASSUMES: ImpactDisposition.REVERIFY,
    DependencyRelation.MITIGATES: ImpactDisposition.REVERIFY,
    DependencyRelation.PRESENTS: ImpactDisposition.STALE_PROJECTION,
    DependencyRelation.REFERENCES: ImpactDisposition.NO_EFFECT,
    DependencyRelation.LINEAGE: ImpactDisposition.NO_EFFECT,
    DependencyRelation.AUTHORIZES: ImpactDisposition.SUSPEND,
}

_AMBIGUOUS = {
    DependencyRelation.DEFEATS,
    DependencyRelation.SUPERSEDES,
}

_RANK = {
    ImpactDisposition.NO_EFFECT: 0,
    ImpactDisposition.STALE_PROJECTION: 1,
    ImpactDisposition.REVERIFY: 2,
    ImpactDisposition.SUSPEND: 3,
    ImpactDisposition.SUPERSEDE: 4,
    ImpactDisposition.INVALIDATE: 5,
}

_STOP_PROPAGATION = {
    ImpactDisposition.NO_EFFECT,
    ImpactDisposition.STALE_PROJECTION,
}


def _reason(edge: DependencyEdge, disposition: ImpactDisposition) -> str:
    return (
        f"{edge.relation.value} from {edge.source_ref} requires {disposition.value}; "
        f"rule source: {edge.source_evidence_ref}"
    )


def _stronger(current: ImpactFinding | None, candidate: ImpactFinding) -> bool:
    if current is None:
        return True
    return _RANK[candidate.disposition] > _RANK[current.disposition]


def compute_validity_impact(
    event: ValidityEvent,
    edges: tuple[DependencyEdge, ...],
) -> ImpactAssessment:
    validate_validity_event(event)
    if event.new_state not in {ValidityState.INVALIDATED, ValidityState.SUPERSEDED}:
        raise ValueError("impact traversal requires a new state of INVALIDATED or SUPERSEDED")

    adjacency = defaultdict(list)
    for edge in edges:
        validate_dependency_edge(edge)
        adjacency[edge.source_ref].append(edge)

    findings: dict[str, ImpactFinding] = {}
    unresolved = set()
    queue = deque([(event.subject_ref, (event.subject_ref,))])
    traversed = set()

    while queue:
        current_ref, path = queue.popleft()
        for edge in adjacency.get(current_ref, ()):
            edge_key = (edge.source_ref, edge.target_ref, edge.relation)
            if edge_key in traversed:
                continue
            traversed.add(edge_key)

            if edge.relation in _AMBIGUOUS:
                unresolved.add(
                    f"{edge.source_ref} -[{edge.relation.value}]-> {edge.target_ref} "
                    f"requires owner adjudication; source: {edge.source_evidence_ref}"
                )
                continue

            disposition = _PROPAGATION[edge.relation]
            candidate = ImpactFinding(
                ref=edge.target_ref,
                disposition=disposition,
                reason=_reason(edge, disposition),
                via=path + (edge.target_ref,),
            )
            if not _stronger(findings.get(edge.target_ref), candidate):
                continue

            findings[edge.target_ref] = candidate
            if disposition not in _STOP_PROPAGATION:
                queue.append((edge.target_ref, candidate.via))

    return ImpactAssessment(
        subject_ref=event.subject_ref,
        findings=tuple(findings[ref] for ref in sorted(findings)),
        unresolved_paths=tuple(sorted(unresolved)),
    )
