"""Deterministic bridge from numeric consensus state to the verified DGAF/TGL runtime.

This module is pre-freeze infrastructure only. It never authorizes pilot execution,
unblinding, or statistical analysis. The TGL runtime is consumed directly through
the verified ``pptl.triadic_governance_loop.TriadicGovernanceLoop.run_turn`` API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Mapping, Sequence

from pptl.triadic_governance_loop import (
    GateResult,
    TGLHooks,
    TriadicGovernanceLoop,
    TurnAuditRecord,
    TurnStatus,
)
from task_engine import AttemptStatus

from pdmaltgl_gate_binding import (
    ApogeeAttestationState,
    ConvergenceState,
    DemiJouleState,
    KappaState,
    PhiClosureState,
    SCPEState,
    SentinelRiskState,
    build_apogee_hook,
    build_demijoule_hook,
    build_kappa_hook,
    build_pdmal_hook,
    build_phi_hook,
    build_scpe_hook,
    build_sentinel_hook,
)

ADAPTER_VERSION = "0.7.2"
PROVENANCE_STATE_VERSION = "1"
DECISIONS = (
    "NO_CHANGE",
    "CONSERVATIVE_MIX",
    "ISOLATE_FAILED_NEIGHBORS",
    "FAIL_CLOSED",
)


@dataclass(frozen=True)
class ConsensusState:
    seed_id: int
    iteration: int
    agent_values: tuple[float, ...]
    alive: tuple[bool, ...]
    original_neighbors: tuple[tuple[int, ...], ...]
    active_neighbors: tuple[tuple[int, ...], ...]
    failure_history: tuple[tuple[int, ...], ...]
    failure_count_current: int
    failure_count_total: int
    current_final_std: float
    current_mean: float
    runtime_budget_remaining_ms: int
    protocol_id: str
    adapter_version: str = ADAPTER_VERSION
    scpe_state: SCPEState = field(default_factory=SCPEState)
    convergence_state: ConvergenceState = field(default_factory=ConvergenceState)
    sentinel_state: SentinelRiskState = field(default_factory=SentinelRiskState)
    apogee_state: ApogeeAttestationState = field(default_factory=ApogeeAttestationState)
    demijoule_state: DemiJouleState = field(default_factory=DemiJouleState)
    kappa_state: KappaState = field(default_factory=KappaState)
    phi_state: PhiClosureState = field(default_factory=PhiClosureState)

    def validate(self) -> None:
        n = len(self.agent_values)
        if n == 0:
            raise ValueError("agent_values must not be empty")
        if len(self.alive) != n:
            raise ValueError("alive length must equal agent_values length")
        if len(self.original_neighbors) != n or len(self.active_neighbors) != n:
            raise ValueError("neighbor arrays must match agent count")
        if self.runtime_budget_remaining_ms < 0:
            raise ValueError("runtime budget cannot be negative")
        if not self.protocol_id:
            raise ValueError("protocol_id must be non-empty")
        expected_nodes = set(range(n))
        for neighbors in (*self.original_neighbors, *self.active_neighbors):
            if tuple(sorted(set(neighbors))) != tuple(neighbors):
                raise ValueError("neighbor lists must be sorted and duplicate-free")
            if not set(neighbors).issubset(expected_nodes):
                raise ValueError("neighbor index out of range")
        if self.scpe_state.threshold <= 0:
            raise ValueError("SCPE threshold must be positive")
        if self.scpe_state.trust_edge_boost != 0.15:
            raise ValueError("SCPE trust_edge_boost must remain the historical 0.15")
        if self.scpe_state.last_k_anchor != 3:
            raise ValueError("SCPE last_k_anchor must remain the historical 3")
        if self.convergence_state.alert_thresh < 0 or self.convergence_state.conv_thresh < 0:
            raise ValueError("P-33 thresholds cannot be negative")
        if self.convergence_state.n_consec < 1:
            raise ValueError("P-33 n_consec must be positive")


def _float_repr(value: float) -> str:
    return format(float(value), ".17g")


def _canonical_scpe_state(state: SCPEState) -> str:
    token_lines = []
    for token in sorted(state.tokens, key=lambda item: str(item["token_id"])):
        token_lines.append(":".join((
            str(token["token_id"]),
            str(token.get("tier", "")),
            str(token.get("content", "")),
            _float_repr(float(token.get("inserted_at", 0.0))),
            "1" if bool(token.get("has_trust_edge", False)) else "0",
        )))
    return "\n".join((
        f"threshold={_float_repr(state.threshold)}",
        f"trust_edge_boost={_float_repr(state.trust_edge_boost)}",
        f"last_k_anchor={state.last_k_anchor}",
        "tokens=" + ";".join(token_lines),
    ))


def _canonical_convergence_state(state: ConvergenceState) -> str:
    def _weights(values: dict[tuple[str, str], float]) -> str:
        return ";".join(
            f"{src}->{dst}={_float_repr(weight)}"
            for (src, dst), weight in sorted(values.items())
        )
    return "\n".join((
        f"alert_thresh={_float_repr(state.alert_thresh)}",
        f"conv_thresh={_float_repr(state.conv_thresh)}",
        f"n_consec={state.n_consec}",
        f"consec_divergent={state._consec_divergent}",
        f"consec_stable={state._consec_stable}",
        f"turn={state._turn}",
        "weights=" + _weights(state.weights),
        "prev_weights=" + _weights(state.prev_weights),
    ))


def _canonical_sentinel_state(state: SentinelRiskState) -> str:
    return "|".join((
        f"record_category={state.record_category}",
        f"routing_policy={state.routing_policy}",
        f"routing_confidence={_float_repr(state.routing_confidence)}",
        f"hook_point={state.hook_point}",
        f"deontic={state.deontic}",
    ))


def _canonical_apogee_state(state: ApogeeAttestationState) -> str:
    return "|".join((
        f"confidence={_float_repr(state.confidence)}",
        f"artifact_description={state.artifact_description}",
        f"grade={state.grade}",
        f"gold_star={'1' if state.gold_star else '0'}",
    ))


def _canonical_demijoule_state(state: DemiJouleState) -> str:
    axes = ";".join(
        f"{k}={_float_repr(v)}" for k, v in sorted(state.axis_scores.items())
    )
    return "|".join((
        f"axes={axes}",
        f"decision={state.decision}",
        f"mean_score={_float_repr(state.mean_score)}",
    ))


def _canonical_kappa_state(state: KappaState) -> str:
    return "|".join((
        f"detected_category={state.detected_category}",
        f"pattern_score={_float_repr(state.pattern_score)}",
        f"continuous_score={_float_repr(state.continuous_score)}",
        f"length_boost={_float_repr(state.length_boost)}",
        f"confidence={_float_repr(state.confidence)}",
        f"routing_decision={state.routing_decision}",
    ))


def _canonical_phi_state(state: PhiClosureState) -> str:
    return "|".join((
        f"stable_count={state.stable_count}",
        f"total_count={state.total_count}",
        f"consec_fails={state.consec_fails}",
        f"last_decision={state.last_decision}",
    ))


def canonicalize_state(state: ConsensusState) -> str:
    """Return the canonical byte-stable TGL representation including restored P31/P33 state."""
    state.validate()
    lines = [
        "PDMAL_DGAF_ADAPTER_V1",
        f"provenance_state_version={PROVENANCE_STATE_VERSION}",
        f"protocol={state.protocol_id}",
        f"adapter={state.adapter_version}",
        f"seed={state.seed_id}",
        f"iteration={state.iteration}",
        "values=" + ",".join(_float_repr(v) for v in state.agent_values),
        "alive=" + "".join("1" if value else "0" for value in state.alive),
        "neighbors=" + ";".join(":".join(str(node) for node in neighbors) for neighbors in state.original_neighbors),
        "active_neighbors=" + ";".join(":".join(str(node) for node in neighbors) for neighbors in state.active_neighbors),
        "failure_history=" + ";".join(",".join(str(node) for node in event) for event in state.failure_history),
        f"failure_count_current={state.failure_count_current}",
        f"failure_count_total={state.failure_count_total}",
        "metrics=" + ",".join((
            f"final_std={_float_repr(state.current_final_std)}",
            f"mean={_float_repr(state.current_mean)}",
        )),
        f"budget_ms={state.runtime_budget_remaining_ms}",
        "scpe=" + _canonical_scpe_state(state.scpe_state).replace("\n", "|"),
        "convergence=" + _canonical_convergence_state(state.convergence_state).replace("\n", "|"),
        "sentinel=" + _canonical_sentinel_state(state.sentinel_state).replace("\n", "|"),
        "apogee=" + _canonical_apogee_state(state.apogee_state).replace("\n", "|"),
        "demijoule=" + _canonical_demijoule_state(state.demijoule_state).replace("\n", "|"),
        "kappa=" + _canonical_kappa_state(state.kappa_state).replace("\n", "|"),
        "phi=" + _canonical_phi_state(state.phi_state).replace("\n", "|"),
    ]
    return "\n".join(lines) + "\n"


def _context_for_state(state: ConsensusState) -> dict[str, Any]:
    state.validate()
    return {
        "pdmaltgl": {
            "schema_version": "1",
            "state": {
                "seed_id": state.seed_id,
                "iteration": state.iteration,
                "agent_values": list(state.agent_values),
                "alive": list(state.alive),
                "original_neighbors": [list(x) for x in state.original_neighbors],
                "active_neighbors": [list(x) for x in state.active_neighbors],
            },
            "failure_history": [list(x) for x in state.failure_history],
            "metrics": {
                "final_std": state.current_final_std,
                "mean": state.current_mean,
                "runtime_budget_remaining_ms": state.runtime_budget_remaining_ms,
            },
            "decision_policy_id": "PDMAL-TGL-V1",
        }
    }


def _pdmall_failure_event_requires_isolation(audit: TurnAuditRecord) -> bool:
    for gate in audit.gate_records:
        if gate.pattern == "P-33" and gate.gate_name == "PDMAL_ConvergenceMonitor":
            return gate.result in {GateResult.WARN, GateResult.KILL}
    return False


def _has_unwired_required_gate(audit: TurnAuditRecord) -> bool:
    required = TriadicGovernanceLoop.REQUIRED_STEPS
    return any(gate.step in required and gate.result is GateResult.SKIP for gate in audit.gate_records)


def decision_from_audit(audit: TurnAuditRecord) -> str:
    if _has_unwired_required_gate(audit):
        return "FAIL_CLOSED"
    status = audit.final_status
    if status in {TurnStatus.KILL, TurnStatus.KILL_REC}:
        return "FAIL_CLOSED"
    if status in {TurnStatus.WARN, TurnStatus.ESCALATE}:
        return "CONSERVATIVE_MIX"
    if status == TurnStatus.PASS and _pdmall_failure_event_requires_isolation(audit):
        return "ISOLATE_FAILED_NEIGHBORS"
    if status == TurnStatus.PASS:
        return "NO_CHANGE"
    raise ValueError(f"unsupported TGL turn status: {status!r}")


def _active_average(values: Sequence[float], active_nodes: Sequence[int]) -> float:
    if not active_nodes:
        return 0.0
    return sum(values[node] for node in active_nodes) / len(active_nodes)


def apply_decision(decision: str, values: Sequence[float], active_neighbors: Sequence[Sequence[int]]) -> tuple[float, ...]:
    if decision not in DECISIONS:
        raise ValueError(f"invalid decision: {decision!r}")
    if len(values) != len(active_neighbors):
        raise ValueError("values and active_neighbors must have identical length")
    if decision == "FAIL_CLOSED":
        raise RuntimeError("DGAF/TGL governance decision is FAIL_CLOSED")
    alpha = 0.2 if decision == "CONSERVATIVE_MIX" else 0.5
    return tuple((1.0 - alpha) * values[index] + alpha * _active_average(values, neighbors)
                 for index, neighbors in enumerate(active_neighbors))


@dataclass(frozen=True)
class AdapterResult:
    input_text: str
    input_hash: str
    decision: str
    next_values: tuple[float, ...] | None
    attempt_status: AttemptStatus
    audit: TurnAuditRecord

    @property
    def audit_seal_hash(self) -> str:
        return self.audit.seal_hash


class DGAF_TGLAdapter:
    def __init__(self, session_id: str, premise_check_fn: Callable[[str, Any], bool], agent_id: str = "pdmAL-agent") -> None:
        if not callable(premise_check_fn):
            raise TypeError("premise_check_fn must be an explicit callable; omission is fail-closed")
        self.session_id = session_id
        self.agent_id = agent_id
        self.premise_check_fn = premise_check_fn

    def run_turn(self, state: ConsensusState) -> AdapterResult:
        input_text = canonicalize_state(state)
        context = _context_for_state(state)
        input_hash = sha256(input_text.encode("utf-8")).hexdigest()
        hooks = TGLHooks(
            premise_check_fn=self.premise_check_fn,
            scpe_fn=build_scpe_hook(state.scpe_state),
            pdmal_fn=build_pdmal_hook(state.convergence_state),
            sentinel_fn=build_sentinel_hook(state.sentinel_state),
            apogee_fn=build_apogee_hook(state.apogee_state),
            demijoul_fn=build_demijoule_hook(state.demijoule_state),
            kappa_fn=build_kappa_hook(state.kappa_state),
            phi_closure_fn=build_phi_hook(state.phi_state),
        )
        tgl = TriadicGovernanceLoop(
            session_id=self.session_id,
            agent_id=self.agent_id,
            hooks=hooks,
            turn_counter=state.iteration,
        )
        audit = tgl.run_turn(input_text, context=context)
        decision = decision_from_audit(audit)
        try:
            next_values = apply_decision(decision, state.agent_values, state.active_neighbors)
            status = AttemptStatus.SUCCESS
        except RuntimeError:
            next_values = None
            status = AttemptStatus.FAILURE
        return AdapterResult(
            input_text=input_text,
            input_hash=input_hash,
            decision=decision,
            next_values=next_values,
            attempt_status=status,
            audit=audit,
        )
