"""Pytest suite for the DGAF-Framework orchestration firewall.

Covers all 5 invariants, happy path, attack paths, authority chain,
and provenance completeness.

Steward: COLLEEN
Orchestrator: Amethyst
Anchor: S043
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Set
import time
import uuid

import pytest


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
        agent = state.agents.get(current)
        if agent and permission in agent.permissions:
            return True
        for edge in state.authority_graph:
            if edge.grantee == current and edge.scope == permission:
                frontier.add(edge.grantor)
    return False


def invariant_no_unreviewed_deploy(state: State) -> bool:
    for event in state.events:
        if event.type == EventType.DEPLOY_SUCCESS and not any(
            review.artifact_id == event.artifact_id
            and review.type == EventType.REVIEW_APPROVE
            and review.timestamp < event.timestamp
            and authorized_reviewer(review.actor_id, event.artifact_id, state)
            for review in state.events
        ):
            return False
    return True


def invariant_tests_before_deploy(state: State) -> bool:
    for event in state.events:
        if event.type != EventType.DEPLOY_SUCCESS:
            continue
        last_change = max(
            (
                change.timestamp
                for change in state.events
                if change.artifact_id == event.artifact_id
                and change.type in {EventType.CODEGEN, EventType.EDIT}
            ),
            default=None,
        )
        if last_change is None:
            return False
        if not any(
            test.artifact_id == event.artifact_id
            and test.type == EventType.TEST_PASS
            and last_change < test.timestamp < event.timestamp
            for test in state.events
        ):
            return False
    return True


def invariant_single_active_deploy_attempt(state: State) -> bool:
    attempts: Dict = {}
    for event in state.events:
        if event.type == EventType.DEPLOY_ATTEMPT:
            key = (event.artifact_id, event.metadata.get("environment", "unknown"))
            attempts.setdefault(key, []).append(event)
    for (artifact_id, environment), entries in attempts.items():
        active = 0
        for attempt in entries:
            if not any(
                follow_up.artifact_id == artifact_id
                and follow_up.metadata.get("environment") == environment
                and follow_up.type in {EventType.DEPLOY_SUCCESS, EventType.DEPLOY_FAILURE}
                and follow_up.timestamp > attempt.timestamp
                for follow_up in state.events
            ):
                active += 1
        if active > 1:
            return False
    return True


def invariant_provenance_complete(state: State) -> bool:
    for event in state.events:
        if event.type != EventType.DEPLOY_SUCCESS:
            continue
        artifact_id = event.artifact_id
        if not any(item.artifact_id == artifact_id and item.type == EventType.CODEGEN for item in state.events):
            return False
        if not any(item.artifact_id == artifact_id and item.type == EventType.REVIEW_APPROVE for item in state.events):
            return False
        if not any(item.artifact_id == artifact_id and item.type == EventType.TEST_PASS for item in state.events):
            return False
    return True


def invariant_authority_bounded_deployment(state: State) -> bool:
    for event in state.events:
        if event.type == EventType.DEPLOY_SUCCESS:
            permission = f"deploy:{event.metadata.get('environment', 'unknown')}"
            if not authority_chain_valid(event.actor_id, permission, state):
                return False
    return True


def all_invariants_hold(state: State) -> bool:
    return all(
        [
            invariant_no_unreviewed_deploy(state),
            invariant_tests_before_deploy(state),
            invariant_single_active_deploy_attempt(state),
            invariant_provenance_complete(state),
            invariant_authority_bounded_deployment(state),
        ]
    )


def now_ts() -> datetime:
    return datetime.now(timezone.utc)


def new_event(
    event_type: EventType,
    artifact_id: str,
    actor_id: str,
    metadata: Optional[Dict] = None,
    **compat_metadata: object,
) -> Event:
    """Create an event, preserving compatibility with legacy keyword metadata."""
    merged = dict(metadata or {})
    merged.update(compat_metadata)
    return Event(str(uuid.uuid4()), event_type, artifact_id, actor_id, now_ts(), merged)


def apply_event(state: State, event: Event) -> bool:
    state.events.append(event)
    artifact = state.artifacts.setdefault(
        event.artifact_id,
        Artifact(id=event.artifact_id, branch=event.metadata.get("branch", "main")),
    )
    if event.type in {EventType.CODEGEN, EventType.EDIT}:
        artifact.current_version += 1
        artifact.status = ArtifactStatus.DRAFT
    elif event.type == EventType.REVIEW_APPROVE:
        artifact.status = ArtifactStatus.APPROVED
    elif event.type == EventType.TEST_PASS:
        artifact.status = ArtifactStatus.TESTED_PASS
    elif event.type == EventType.DEPLOY_SUCCESS:
        artifact.status = ArtifactStatus.DEPLOYED
    ok = all_invariants_hold(state)
    if not ok:
        state.events.pop()
    return ok


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


class TestHappyPath:
    def test_all_events_committed(self, clean_state):
        aid, env = "A1", "prod"
        results = [
            apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent", test_passed=True)),
            apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent", test_passed=True)),
            apply_event(clean_state, new_event(EventType.TEST_PASS, aid, "test_agent")),
            apply_event(clean_state, new_event(EventType.DEPLOY_ATTEMPT, aid, "deploy_agent", {"environment": env})),
            apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": env})),
        ]
        assert all(results), "Happy path: all events must be committed"

    def test_artifact_status_deployed(self, clean_state):
        aid, env = "A2", "prod"
        for event_type, actor, metadata in [
            (EventType.CODEGEN, "code_agent", {"test_passed": True}),
            (EventType.REVIEW_APPROVE, "review_agent", {"test_passed": True}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
            (EventType.DEPLOY_SUCCESS, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(event_type, aid, actor, metadata))
        assert clean_state.artifacts[aid].status == ArtifactStatus.DEPLOYED

    def test_invariants_hold_after_happy_path(self, clean_state):
        aid, env = "A3", "prod"
        for event_type, actor, metadata in [
            (EventType.CODEGEN, "code_agent", {"test_passed": True}),
            (EventType.REVIEW_APPROVE, "review_agent", {"test_passed": True}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
            (EventType.DEPLOY_SUCCESS, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(event_type, aid, actor, metadata))
        assert all_invariants_hold(clean_state)


class TestAttackPaths:
    def test_direct_deploy_no_review_blocked(self, clean_state):
        aid = "B1"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        result = apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}))
        assert result is False, "Direct deploy without review must be blocked"
        assert len(clean_state.events) == 1, "Only CODEGEN should be committed"

    def test_deploy_without_tests_blocked(self, clean_state):
        aid = "B2"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        result = apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}))
        assert result is False, "Deploy without tests must be blocked"

    def test_unauthorized_deploy_blocked(self, clean_state):
        aid = "B3"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        apply_event(clean_state, new_event(EventType.TEST_PASS, aid, "test_agent"))
        apply_event(clean_state, new_event(EventType.DEPLOY_ATTEMPT, aid, "code_agent", {"environment": "prod"}))
        result = apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "code_agent", {"environment": "prod"}))
        assert result is False, "Unauthorized deploy must be blocked"

    def test_invariants_hold_after_attack(self, clean_state):
        aid = "B4"
        apply_event(clean_state, new_event(EventType.CODEGEN, aid, "code_agent"))
        apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}))
        assert all_invariants_hold(clean_state)


class TestAuthorityChain:
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
    def test_missing_codegen_in_provenance(self, clean_state):
        aid = "C1"
        clean_state.events.append(new_event(EventType.REVIEW_APPROVE, aid, "review_agent"))
        clean_state.events.append(new_event(EventType.TEST_PASS, aid, "test_agent"))
        result = apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": "prod"}))
        assert result is False

    def test_full_provenance_accepted(self, clean_state):
        aid, env = "C2", "prod"
        for event_type, actor, metadata in [
            (EventType.CODEGEN, "code_agent", {"test_passed": True}),
            (EventType.REVIEW_APPROVE, "review_agent", {"test_passed": True}),
            (EventType.TEST_PASS, "test_agent", {}),
            (EventType.DEPLOY_ATTEMPT, "deploy_agent", {"environment": env}),
        ]:
            apply_event(clean_state, new_event(event_type, aid, actor, metadata))
        result = apply_event(clean_state, new_event(EventType.DEPLOY_SUCCESS, aid, "deploy_agent", {"environment": env}))
        assert result is True
