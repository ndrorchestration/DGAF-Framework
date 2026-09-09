#!/usr/bin/env python3
"""Non-empirical matrix diagnostic for the qualified canonical PDMAL profile.

This module does not execute an efficacy experiment. It verifies that the candidate
canonical treatment can traverse the required TGL gates when step 8 verifies the
already-frozen, source-bound P-30/P-11 11Q qualification artifact. Scientific N
increment is always zero.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from canonical_p30_qualification import build_qualification_verifier_hook, verify_qualification_artifact
from dgaf_tgl_adapter import (
    AdapterResult,
    ConsensusState,
    _context_for_state,
    apply_decision,
    canonicalize_state,
    decision_from_audit,
)
from harness_contract import TOPOLOGY_SPECS
from pdmaltgl_gate_binding import (
    build_demijoule_hook,
    build_kappa_hook,
    build_pdmal_hook,
    build_phi_hook,
    build_scpe_hook,
    build_sentinel_hook,
)
from pptl.triadic_governance_loop import TGLHooks, TriadicGovernanceLoop
from task_engine import (
    AttemptStatus,
    PILOT_FAILURE_COUNTS,
    SEED_RUNTIME_CEILING_SECONDS,
    ConsensusTask,
    ConsensusTrialResult,
)

DIAGNOSTIC_RECORD_TYPE = "DGAF_CANONICAL_PROFILE_TGL_NONEMPIRICAL_DIAGNOSTIC"
DIAGNOSTIC_ID = "DGAF-CANONICAL-PROFILE-TGL-DIAGNOSTIC-V1"
PROFILE_ID = "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"
PROFILE_SOURCE_SHA = "c8a07306d212e23cc5a4c1e0d98b7e8f47f45e21"
QUALIFICATION_PATH = Path(
    "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.json"
)
QUALIFICATION_SHA256 = "4d0346f6a05046f03ce5a399d1dd4de2d31b69f683988fe9af20802d2c062d78"
DIAGNOSTIC_SEEDS = (20260819, 20260820)
PROTOCOL_ID = "PDMAL-CANONICAL-PROFILE-DIAGNOSTIC-V1"


def load_and_validate_qualification(root: Path = Path(".")) -> bytes:
    raw = (root / QUALIFICATION_PATH).read_bytes()
    if hashlib.sha256(raw).hexdigest() != QUALIFICATION_SHA256:
        raise RuntimeError("qualification digest mismatch")
    if not verify_qualification_artifact(
        raw,
        expected_sha256=QUALIFICATION_SHA256,
        expected_profile_id=PROFILE_ID,
        expected_profile_source_sha=PROFILE_SOURCE_SHA,
    ):
        raise RuntimeError("qualification fails canonical step-8 verifier")
    return raw


def _qualified_input_text(state: ConsensusState) -> str:
    """Canonicalize state without serializing the retired scalar Apogee substrate."""
    historical = canonicalize_state(state)
    lines = [line for line in historical.splitlines() if not line.startswith("apogee=")]
    lines.append(
        "p30_qualification="
        f"profile_id={PROFILE_ID}|profile_source_sha={PROFILE_SOURCE_SHA}|"
        f"qualification_sha256={QUALIFICATION_SHA256}|mode=VERIFY_EXTERNAL_11Q"
    )
    return "\n".join(lines) + "\n"


class CanonicalQualifiedTGLAdapter:
    """Diagnostic-only TGL adapter with external qualification verification at step 8."""

    def __init__(self, *, session_id: str, qualification_bytes: bytes) -> None:
        self.session_id = session_id
        self.qualification_bytes = qualification_bytes

    def run_turn(self, state: ConsensusState) -> AdapterResult:
        state.validate()
        input_text = _qualified_input_text(state)
        input_hash = hashlib.sha256(input_text.encode("utf-8")).hexdigest()
        context = _context_for_state(state)
        hooks = TGLHooks(
            scpe_fn=build_scpe_hook(state.scpe_state),
            pdmal_fn=build_pdmal_hook(state.convergence_state),
            sentinel_fn=build_sentinel_hook(state.sentinel_state),
            apogee_fn=build_qualification_verifier_hook(
                self.qualification_bytes,
                expected_sha256=QUALIFICATION_SHA256,
                expected_profile_id=PROFILE_ID,
                expected_profile_source_sha=PROFILE_SOURCE_SHA,
            ),
            demijoul_fn=build_demijoule_hook(state.demijoule_state),
            kappa_fn=build_kappa_hook(state.kappa_state),
            phi_closure_fn=build_phi_hook(state.phi_state),
        )
        tgl = TriadicGovernanceLoop(
            session_id=self.session_id,
            agent_id="pdmAL-canonical-profile-diagnostic",
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


class CanonicalProfileDiagnosticTask(ConsensusTask):
    """DGAF-only task for the non-empirical qualified-profile diagnostic."""

    def __init__(self, *, topology: str, failure_count: int, qualification_bytes: bytes) -> None:
        super().__init__(topology=topology, failure_count=failure_count, condition="dgaf")
        self.qualification_bytes = qualification_bytes

    def _dgaf_update(
        self,
        *,
        seed: int,
        iteration: int,
        values: np.ndarray,
        graph,
        alive: tuple[bool, ...],
        active_neighbors: tuple[tuple[int, ...], ...],
        failure_history: tuple[tuple[int, ...], ...],
        failure_count_current: int,
        failure_count_total: int,
    ):
        adapter = CanonicalQualifiedTGLAdapter(
            session_id=f"canonical-profile-diagnostic-{self.trial_key(seed, self.topology, self.condition, self.failure_count)}",
            qualification_bytes=self.qualification_bytes,
        )
        state = ConsensusState(
            seed_id=seed,
            iteration=iteration,
            agent_values=tuple(float(x) for x in values),
            alive=alive,
            original_neighbors=tuple(tuple(sorted(graph.neighbors(i))) for i in range(20)),
            active_neighbors=active_neighbors,
            failure_history=failure_history,
            failure_count_current=failure_count_current,
            failure_count_total=failure_count_total,
            current_final_std=float(np.std(values)),
            current_mean=float(np.mean(values)),
            runtime_budget_remaining_ms=int(SEED_RUNTIME_CEILING_SECONDS * 1000),
            protocol_id=PROTOCOL_ID,
        )
        try:
            result = adapter.run_turn(state)
        except Exception as exc:
            return values, AttemptStatus.FAILURE, f"canonical-adapter-error:{type(exc).__name__}: {exc}", None
        trace = result.audit.to_dict()
        trace["decision"] = result.decision
        trace["outcome"] = result.attempt_status.value
        if result.decision == "FAIL_CLOSED" or result.next_values is None:
            return values, AttemptStatus.FAILURE, "canonical-profile-fail-closed", trace
        return np.asarray(result.next_values, dtype=float), AttemptStatus.SUCCESS, None, trace


def _audit_summary(result: ConsensusTrialResult) -> dict[str, Any]:
    required_bad: dict[str, int] = {}
    step8_passes = 0
    malformed_turns = 0
    for turn in result.governance_trace:
        gates = turn.get("gates")
        if not isinstance(gates, list):
            malformed_turns += 1
            continue
        step8 = [g for g in gates if g.get("step") == 8]
        if len(step8) == 1 and step8[0].get("pattern") == "P-30" and step8[0].get("result") == "PASS":
            step8_passes += 1
        else:
            key = "STEP8_MISSING_OR_NONPASS"
            required_bad[key] = required_bad.get(key, 0) + 1
        for gate in gates:
            if gate.get("step") in TriadicGovernanceLoop.REQUIRED_STEPS and gate.get("result") in {"KILL", "SKIP"}:
                key = f"step{gate.get('step')}:{gate.get('gate', 'UNKNOWN')}:{gate.get('result')}"
                required_bad[key] = required_bad.get(key, 0) + 1
    return {
        "governance_turn_count": len(result.governance_trace),
        "step8_pass_count": step8_passes,
        "malformed_turn_count": malformed_turns,
        "required_gate_failures": dict(sorted(required_bad.items())),
    }


def run_diagnostic(output: Path) -> dict[str, Any]:
    qualification = load_and_validate_qualification()
    records: list[dict[str, Any]] = []
    attempt_success_count = 0
    attempt_failure_count = 0
    total_governance_turns = 0
    total_step8_passes = 0
    aggregate_required_failures: dict[str, int] = {}

    for seed in DIAGNOSTIC_SEEDS:
        for topology in TOPOLOGY_SPECS:
            for failure_count in PILOT_FAILURE_COUNTS:
                task = CanonicalProfileDiagnosticTask(
                    topology=topology,
                    failure_count=failure_count,
                    qualification_bytes=qualification,
                )
                result = task.run_detailed(seed=seed, attempt=1)
                summary = _audit_summary(result)
                success = result.attempt_status is AttemptStatus.SUCCESS
                attempt_success_count += int(success)
                attempt_failure_count += int(not success)
                total_governance_turns += summary["governance_turn_count"]
                total_step8_passes += summary["step8_pass_count"]
                for key, count in summary["required_gate_failures"].items():
                    aggregate_required_failures[key] = aggregate_required_failures.get(key, 0) + count
                records.append(
                    {
                        "seed": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "attempt_status": result.attempt_status.value,
                        "iterations_completed": result.iterations_completed,
                        **summary,
                    }
                )

    document = {
        "record_type": DIAGNOSTIC_RECORD_TYPE,
        "classification": "NON_EMPIRICAL_ENGINEERING_DIAGNOSTIC",
        "diagnostic_id": DIAGNOSTIC_ID,
        "profile_id": PROFILE_ID,
        "profile_source_sha": PROFILE_SOURCE_SHA,
        "qualification_sha256": QUALIFICATION_SHA256,
        "qualification_verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        "independent_verification": False,
        "scientific_n_increment": 0,
        "empirical_authorization": False,
        "seeds": list(DIAGNOSTIC_SEEDS),
        "topologies": list(TOPOLOGY_SPECS),
        "failure_counts": list(PILOT_FAILURE_COUNTS),
        "total_diagnostic_trials": len(records),
        "attempt_success_count": attempt_success_count,
        "attempt_failure_count": attempt_failure_count,
        "total_governance_turns": total_governance_turns,
        "total_step8_passes": total_step8_passes,
        "aggregate_required_gate_failures": dict(sorted(aggregate_required_failures.items())),
        "efficacy_metrics_emitted": False,
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def adjudicate(document: dict[str, Any]) -> None:
    if document["total_diagnostic_trials"] != 90:
        raise RuntimeError("diagnostic matrix must contain exactly 90 trials")
    if document["attempt_success_count"] != 90 or document["attempt_failure_count"] != 0:
        raise RuntimeError("all 90 diagnostic trials must execute successfully")
    if document["aggregate_required_gate_failures"]:
        raise RuntimeError(f"required gate failure observed: {document['aggregate_required_gate_failures']}")
    if document["total_governance_turns"] != 9000:
        raise RuntimeError("all 90 trials must complete all 100 governance turns")
    if document["total_step8_passes"] != document["total_governance_turns"]:
        raise RuntimeError("step 8 must PASS exactly once on every governance turn")
    if any(record["malformed_turn_count"] for record in document["records"]):
        raise RuntimeError("malformed governance trace observed")


def main() -> int:
    output = Path("test-artifacts/canonical_profile_tgl_diagnostic.json")
    document = run_diagnostic(output)
    adjudicate(document)
    print(
        "CANONICAL_PROFILE_TGL_DIAGNOSTIC_PASS: "
        f"trials={document['total_diagnostic_trials']} "
        f"turns={document['total_governance_turns']} "
        f"step8_passes={document['total_step8_passes']}"
    )
    print("SCIENTIFIC_N_INCREMENT=0")
    print("EMPIRICAL_AUTHORIZATION=false")
    print(f"artifact={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
