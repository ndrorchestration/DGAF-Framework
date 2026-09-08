"""Canonical Epoch 004 TGL adapter with external P-30/11Q verification.

This module is treatment runtime code, not the historical non-empirical diagnostic
identity. It deliberately reuses the already-qualified input contract and step-8
verification semantics while emitting an Epoch 004-specific agent identity.
"""
from __future__ import annotations

import hashlib

from canonical_p30_qualification import build_qualification_verifier_hook
from canonical_profile_tgl_diagnostic import (
    PROFILE_ID,
    PROFILE_SOURCE_SHA,
    QUALIFICATION_SHA256,
    _qualified_input_text,
)
from dgaf_tgl_adapter import (
    AdapterResult,
    ConsensusState,
    _context_for_state,
    apply_decision,
    decision_from_audit,
)
from pdmaltgl_gate_binding import (
    build_demijoule_hook,
    build_kappa_hook,
    build_pdmal_hook,
    build_phi_hook,
    build_scpe_hook,
    build_sentinel_hook,
)
from pptl.triadic_governance_loop import TGLHooks, TriadicGovernanceLoop
from task_engine import AttemptStatus


class CanonicalEpoch004TGLAdapter:
    """Canonical treatment adapter for `PDMAL-SOLO-CANONICAL-EPOCH-004`."""

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
            agent_id="pdmal-canonical-epoch-004",
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
