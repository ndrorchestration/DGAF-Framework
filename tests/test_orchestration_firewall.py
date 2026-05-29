"""test_orchestration_firewall.py

Pytest suite for the DGAF-Framework orchestration firewall.
Covers all 5 invariants, happy path, attack paths, authority chain,
and provenance completeness.

Steward: COLLEEN
Orchestrator: Amethyst
Anchor: S043
"""

import pytest
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Callable
from enum import Enum, auto


# ---------------------------------------------------------------------------
# Domain model (inline for test self-containment)
# ---------------------------------------------------------------------------

class ArtifactStatus(Enum):
    DRAFT = auto()
    APPROVED = auto()
    TESTED_PASS = auto()
    TESTED_FAIL = auto()
    DEPLOYED = auto()


class EventType(Enum):
    REQUEST = auto()
    CODEGEN = auto()
    EDIT = auto()
    REVIEW_APPROVE = auto()
    REVIEW_REJECT = auto()
    TEST_PASS = auto()
    TEST_FAIL = auto()
    SECURITY_PASS = auto()
    SECURITY_FAIL = auto()
    DEPLOY_ATTEMPT = auto()
    DEPLOY_SUCCESS = auto()
    DEPLOY_FAILURE = auto()


@dataclass
class Event:
    id: str
    type: EventType
    artifact_id: str
    actor_id: str
    timestamp: datetime
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Agent:
    id: str
    role: str
    permissions: Set[str]
    fn: Optional[Callable] = None


@dataclass
class AuthorityEdge:
    grantor: str
    grantee: str
    scope: str
    constraints: Dict[str, str] = field(default_factory=dict)


@dataclass
class Artifact:
    id: str
    branch: str
    current_version: int = 0
    status: ArtifactStatus = ArtifactStatus.DRAFT


@dataclass
class State:
    artifacts: Dict[str, Artifact] = field(default_factory=dict)
    events: List[Event] = field(default_factory=list)
    agents: Dict[str, Agent] = field(default_factory=dict)
    authority_graph: List[AuthorityEdge] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

def authorized_reviewer(agent_id: str, artifact_id: str, state: State) -> bool:
    return agent_id in state.agents and "review" in state.agents[agent_id].permissions


def authority_chain_valid(agent_id: str, permission: str, state: State) -> bool:
    visited: Set[str] = set()
    frontier = {agent_id}
    while frontier:
        current = frontier.pop()
        if current in visited:
            continue
        visited.add(current)
        ag = state.agents.get(current)
        if ag and permission in ag.permissions:
            return True
        for edge in state.authority_graph:
            if edge.grantee == current and edge.scope == permission:
                frontier.add(edge.grantor)
    return False


def invariant_no_unreviewed_deploy(state: State) -> bool:
    for e in state.events:
        if e.type == EventType.DEPLOY_SUCCESS:
            if not any(
                r.artifact_id == e.artifact_id
                and r.type == EventType.REVIEW_APPROVE
                and r.timestamp < e.timestamp
                and authorized_reviewer(r.actor_id, e.artifact_id, state)
                for r in state.events
            ):
                return False
    return True


def invariant_tests_before_deploy(state: State) -> bool:
    for e in state.events:
        if e.type == EventType.DEPLOY_SUCCESS:
            last_change = max(
                (c.timestamp for c in state.events
                 if c.artifact_id == e.artifact_id
                 and c.type in {EventType.CODEGEN, EventType.EDIT}),
                default=None
            )
            if last_change is None:
                return False
            if not any(
                t.artifact_id == e.artifact_id
                and t.type == EventType.TEST_PASS
                and last_change < t.timestamp < e.timestamp
                for t in state.events
            ):
                return False
    return True


def invariant_single_active_deploy_attempt(state: State) -> bool:
    attempts: Dict = {}
    for e in state.events:
        if e.type == EventType.DEPLOY_ATTEMPT:
            k = (e.artifact_id, e.metadata.get("environment", "unknown"))
            attempts.setdefault(k, []).append(e)
    for (aid, env), arr in attempts.items():
        active = 0
        for a in arr:
            if not any(
                f.artifact_id == aid
                and f.metadata.get("environment") == env
                and f.type in {EventType.DEPLOY_SUCCESS, EventType.DEPLOY_FAILURE}
                and f.timestamp > a.timestamp
                for f in state.events
            ):
                active += 1
        if active > 1:
            return False
    return True


def invariant_provenance_complete(state: State) -> bool:
    for e in state.events:
        if e.type == EventType.DEPLOY_SUCCESS:
            aid = e.artifact_id
            if not any(c.artifact_id == aid and c.type == EventType.CODEGEN for c in state.events):
                return False
            if not any(r.artifact_id == aid and r.type == EventType.REVIEW_APPROVE for r in state.events):
                return False
            if not any(t.artifact_id == aid and t.type == EventType.TEST_PASS for t in state.events):
                return False
    return True


def invariant_authority_bounded_deployment(state: State) -> bool:
    for e in state.events:
        if e.type == EventType.DEPLOY_SUCCESS:
            perm = f"deploy:{e.metadata.get('environment', 'unknown')}"
            if not authority_chain_valid(e.actor_id, perm, state):
                return False
    return True


def all_invariants_hold(state: State) -> bool:
    return all([
        invariant_no_unreviewed_deploy(state),
        invariant_tests_before_deploy(state),
        invariant_single_active_deploy_attempt(state),
        invariant_provenance_complete(state),
        invariant_authority_bounded_deployment(state),
    ])


# ---------------------------------------------------------------------------
# Firewall
# ---------------------------------------------------------------------------

def now_ts() -> datetime:
    return datetime.now(timezone.utc)


def new_event(event_type: EventType, artifact_id: str, actor_id: str,
              metadata: Optional[Dict] = None) -> Event:
    return Event(str(uuid.uuid4()), event_type, artifact_id, actor_id, now_ts(), metadata or {})


def apply_event(state: State, event: Event) -> bool:
    state.events.append(event)
    art = state.artifacts.setdefault(
        event.artifact_id,
        Artifact(id=event.artifact_id, branch=event.metadata.get("branch", "main"))
    )
    if event.type in {EventType.CODEGEN, EventType.EDIT}:
        art.current_version += 1
        art.status = ArtifactStatus.DRAFT
    elif event.type == EventType.REVIEW_APPROVE:
        art.status = ArtifactStatus.APPROVED
    elif event.type == EventType.TEST_PASS:
        art.status = ArtifactStatus.TESTED_PASS
    elif event.type == EventType.DEPLOY_SUCCESS:
        art.status = ArtifactStatus.DEPLOYED

    ok = all_invariants_hold(state)
    if not ok:
        state.events.pop()
    return ok


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def base_agents() -> Dict[str, Agent]:
    return {
        "code_agent": Agent("code_agent", "code", set()),
        "review_agent": Agent("review_agent", "review", {"review"}),
        "test_agent": Agent("test_agent", "test", set()),
        "deploy_agent": Agent("deploy_agent", "deploy", {"deploy:prod"}),
        "human_owner": Agent("human_owner", "owner", {"deploy:prod"}),
    }


@pytest.fixture
def base_authority() -> List[AuthorityEdge]:
    return [AuthorityEdge("human_owner", "deploy_agent", "deploy:prod")]


@pytest.fixture
def clean_state(base_agents, base_authority) -> State:
    return State(agents=base_agents, authority_graph=base_authority)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHappyPath:
    """Complete CODEGEN → REVIEW → TEST → ATTEMPT → DEPLOY sequence must succeed."""

    def test_all_events_committed(self, clean_state):
        aid, env = "A1", "prod"
        results = [
            apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent")),
            apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent")),
            apply_event(clean_state, new_event(EventType.TEST_PASS, aid, "test_agent")),
            apply_event(clean_state, new_event(EventType.DEPLOY_ATTEMPT, aid, "deploy_agent", {"environment": env})),
            apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": env})),
        ]
        assert all(results), "Happy path: all events must be committed"

    def test_artifact_status_deployed(self, clean_state):
        aid, env = "A2", "prod"
        for et, actor, meta in [
            (EventType.CODEGEN, "code_agent", {}),
            (EventType.REVIEW_APPROVE, "review_agent", {}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
            (EventType.DEPLOY_SUCCESS, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(et, aid, actor, meta))
        assert clean_state.artifacts[aid].status == ArtifactStatus.DEPLOYED

    def test_invariants_hold_after_happy_path(self, clean_state):
        aid, env = "A3", "prod"
        for et, actor, meta in [
            (EventType.CODEGEN, "code_agent", {}),
            (EventType.REVIEW_APPROVE, "review_agent", {}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
            (EventType.DEPLOY_SUCCESS, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(et, aid, actor, meta))
        assert all_invariants_hold(clean_state)


class TestAttackPaths:
    """All attack paths must be blocked and rolled back."""

    def test_direct_deploy_no_review_blocked(self, clean_state):
        """CODEGEN → DEPLOY_SUCCESS (no review) must be rejected."""
        aid = "B1"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        result = apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}
        ))
        assert result is False, "Direct deploy without review must be blocked"
        assert len(clean_state.events) == 1, "Only CODEGEN should be committed"

    def test_deploy_without_tests_blocked(self, clean_state):
        """CODEGEN → REVIEW → DEPLOY (no tests) must be rejected."""
        aid = "B2"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        result = apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}
        ))
        assert result is False, "Deploy without tests must be blocked"

    def test_unauthorized_deploy_blocked(self, clean_state):
        """Deploy by actor with no deploy permission must be rejected."""
        aid = "B3"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        apply_event(clean_state, new_event(EventType.TEST_PASS, aid, "test_agent"))
        apply_event(clean_state, new_event(
            EventType.DEPLOY_ATTEMPT, aid, "code_agent", {"environment": "prod"}
        ))
        result = apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "code_agent", {"environment": "prod"}
        ))
        assert result is False, "Unauthorized deploy must be blocked"

    def test_invariants_hold_after_attack(self, clean_state):
        """After blocked attack, invariants must still hold on committed state."""
        aid = "B4"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}
        ))  # should be blocked
        assert all_invariants_hold(clean_state)


class TestAuthorityChain:
    """Authority chain validation tests."""

    def test_direct_permission_grants_access(self, base_agents, base_authority):
        state = State(agents=base_agents, authority_graph=base_authority)
        assert authority_chain_valid("deploy_agent", "deploy:prod", state)

    def test_transitive_authority_valid(self, base_agents, base_authority):
        state = State(agents=base_agents, authority_graph=base_authority)
        assert authority_chain_valid("human_owner", "deploy:prod", state)

    def test_no_permission_agent_blocked(self, base_agents, base_authority):
        state = State(agents=base_agents, authority_graph=base_authority)
        assert not authority_chain_valid("code_agent", "deploy:prod", state)

    def test_test_agent_cannot_deploy(self, base_agents, base_authority):
        state = State(agents=base_agents, authority_graph=base_authority)
        assert not authority_chain_valid("test_agent", "deploy:prod", state)


class TestProvenanceCompleteness:
    """Provenance chain must include codegen, review, and test before deploy."""

    def test_missing_codegen_in_provenance(self, clean_state):
        """Deploy without codegen in history must fail provenance check."""
        aid = "C1"
        # Manually inject review and test without codegen
        clean_state.events.append(new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        clean_state.events.append(new_event(EventType.TEST_PASS, aid, "test_agent"))
        # Attempt deploy
        result = apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}
        ))
        assert result is False

    def test_full_provenance_accepted(self, clean_state):
        """Full provenance chain must be accepted."""
        aid, env = "C2", "prod"
        for et, actor, meta in [
            (EventType.CODEGEN, "code_agent", {}),
            (EventType.REVIEW_APPROVE, "review_agent", {}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(et, aid, actor, meta))
        result = apply_event(clean_state, new_event(
            EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": env}
        ))
        assert result is True
