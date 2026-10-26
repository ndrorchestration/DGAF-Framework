# AKDC / DGAF non-authoritative ingress research — Gate 3 (2026-10-26)

**State:** RESEARCH CANDIDATE / PRE-FREEZE / NON-AUTHORIZING / NO EMPIRICAL N / NOT RELEASE ADMITTING.

This draft is intentionally *not* a feature integration, production MCP/A2A adapter, provider trust admission, category-theoretic governance proof, or authorization mechanism. It does not change any existing DGAF runtime, protected workflow, registry, policy, scientific state, or custody surface.

## Scope and exact authority boundary

Research-only source: `experiments/akdc/akdc_ingress_bridge.py`.

Contract tests: `tests/test_akdc_ingress_research.py`.

Inputs are synthetic and explicitly versioned observations of A2A **1.0.1** task state or MCP **2026-07-28** raw `tools/call` JSON-RPC responses. Their representations are bounded fixtures, not an official SDK/transport implementation.

Output is only a versioned `DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1` with:

- `request.action_class = NON_CONSEQUENTIAL_RECORD_INGRESS`
- `request.requested_transition = RECORD_ONLY`
- `assertions.authority.status = EXTERNAL_OBSERVED_NOT_GRANTED`
- `assertions.verification_class = EXTERNAL_UNVERIFIED`

The existing `scripts.validate_external_runtime_adapter` performs the *separate*, actual DGAF ingress checks. Its successful result retains `PRESENTED_NOT_GRANTED` and `UNVERIFIED_EXTERNAL_ASSERTION`, and does not authorize execution. A2A task completion, MCP tool success, adapter acceptance, translated consensus, and a source quorum are never permissions in DGAF.

## Evidence and known limitations

At the time of repository readback, the reference baseline was `main` commit `1a95b94332dffb404c5a3ce026d70781a8c10b90`; the actual DGAF validator had Git blob SHA `fab53669c69ea0b26bc9a55bce2ab157ac8f5348`. The validator was copied byte-for-byte into an isolated local test snapshot and the blob SHA was recomputed to confirm exact identity.

Local evidence: **41/41** pre-existing + AKDC synthetic/pinned-source tests passed; **0 skipped**. Separately, **14/14** repository-ready research contract tests passed locally against the pinned DGAF validator. These are local engineering tests: **not a GitHub Actions CI claim**. CI and independent review of this PR remain open.

Source protocol basis:

- [A2A v1.0.1](https://a2a-protocol.org/v1.0.1/specification/) — `TASK_STATE_*` values, non-return to active states after a terminal task.
- [MCP 2026-07-28 schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.json) — `CallToolResult.resultType` required for 2026 wire frames; protocol errors and tool errors are distinct.

The research toy `OrderingGate` is *single-process, volatile and non-transactional*. Its state cannot be used for replay protection, distributed consensus, principal binding, permissions, or durable exactly-once effects. It cannot be attached to the real DGAF local operator bridge without a separate authorized contract.

No production transport, authentication, signed provenance, SDK transcript, revocation, race testing, real agent experiment, field trial, TRL advancement, or safety/efficacy measurement occurred. The underlying user-supplied dossier is not added to this PR; its `ORCON-NOFORN` legend has not been authenticated and redistribution requires provenance review.

## Explicit guards

- Do not add any new MCP tools, HTTP routes, shell/file capabilities, downstream commit operations, or runtime dispatch from this research.
- Do not modify `scripts/validate_external_runtime_adapter.py`, `registry/external_runtime_adapter_contract_v1.json`, or DGAF's existing custody, control-plane, governance or scientific configuration.
- Preserve `SCIENTIFIC_N_INCREMENT=0`, `DGAF_V1_RELEASE=HOLD`, `HIGH_ASSURANCE=NOT_AUTHORIZED`, independent validation not established.
- Synthetic AKDC toy IDs must **not** reuse `SYN-AUTH-01` from independently governed [issue #1508](https://github.com/ndrorchestration/DGAF-Framework/issues/1508). That candidate remains UNFROZEN and NOT PEER-RUN.

## Next gates (separately authorized)

1. Require exact-head CI on this draft PR; retain full test list, SHA, failures and environment.
2. Add a durable, transactionally coupled effect/event replay store behind independent ingress admission; adversarially test duplicate messages and concurrency.
3. Compare official SDK protocol traces and strict schemas; test fragmented streams, capability negotiation, resumption, cancellation, context/task identity and revocation.
4. Predeclare a comparator: protocol-only adapter vs adapter plus explicit invariants vs categorical coherence checker, under identical blinded trace inputs. Report cost as well as all detection and failure outcomes.
5. Independently review candidate semantics and freeze fixtures/oracles before any interop efficacy or scientific claims.

**No merge or release authorization is implied by draft PR creation.**