# P-35 / TGL / PDMAL interoperability boundary — engineering reconciliation

**Date:** 2026-10-26  
**Classification:** non-empirical design and same-system source inspection, not an admission or scientific validation  
**Release:** HOLD · **SCIENTIFIC_N_INCREMENT:** 0 · **HIGH_ASSURANCE:** NOT_AUTHORIZED

## Exact source lineage

- Protected `main` observed at `1a95b94332dffb404c5a3ce026d70781a8c10b90`.
- Signed, unmerged canonical completeness candidate: [PR #1388](https://github.com/ndrorchestration/DGAF-Framework/pull/1388), exact head `92ecb234d18e981723e5a5be9c5906255df1643e`.
- Unsigned, unmerged P-35 fail-closed candidate: [PR #1519](https://github.com/ndrorchestration/DGAF-Framework/pull/1519), exact head MUST be read live.
- Unsigned, unmerged combined rehearsal: [PR #1522](https://github.com/ndrorchestration/DGAF-Framework/pull/1522), exact head MUST be read live.
- Related boundaries: [#1509](https://github.com/ndrorchestration/DGAF-Framework/issues/1509), [#1343](https://github.com/ndrorchestration/DGAF-Framework/issues/1343), [#1367](https://github.com/ndrorchestration/DGAF-Framework/issues/1367), [#1387](https://github.com/ndrorchestration/DGAF-Framework/pull/1387).

This document is a compatibility and verification proposal. All recorded source hashes are Git object identity, not raw checkout-byte or authenticated-runner evidence.

## Current consumers and exact protected-main blobs

| Consumer | Protected-main Git blob | P-35 predicate wired? | Consequence of proposed P-35 semantics |
|---|---|---|---|
| `experiments/pdmal_pilot/dgaf_tgl_adapter.py` | `9e86883591d62b289d360fb3f5e6093e0d8a81cb` | No | Gate 0 SKIP, downstream 1–8 SKIP, ESCALATE, `decision_from_audit` FAIL_CLOSED, no `apply_decision` value update |
| `experiments/pdmal_pilot/canonical_profile_tgl_diagnostic.py` | `715fd54f2200e8b204448cc2dd1fb11a57350640` | No | Same blocked path; cannot claim prior profile-diagnostic parity as fresh new-head behavior |
| `experiments/pdmal_pilot/canonical_epoch_004_adapter.py` | `95dc2f05196fe1df054fa9677bdfcd5d4d188081` | No | Same blocked path; frozen treatment qualification is not equivalent to prospective P-35 approval |

Static inspection confirms each constructs `TGLHooks` and uses `decision_from_audit` without `premise_check_fn`. These are **prospective control-flow predictions**, not new execution evidence for all three full adapters.

## Contract reconciliation

1. **Absence is not a violation and is not PASS.** An absent P-35 predicate produces `GateResult.SKIP` with an explicit `UNVERIFIED` note, a sealed `TurnStatus.ESCALATE`, and no downstream hook execution. The Herald audit may be published but cannot promote the decision.
2. A predicate returning a strict `False` creates an explicit constitutional violation and terminal `KILL` with the existing `PremiseViolationEvent`; invalid types or exceptions fail closed but **must not be mislabeled as proven constitutional violations**.
3. A configured predicate returning `True` proves only that the function returned `True` for the evaluated input and invariant. It does **not** establish authenticated policy origin, correct current policy version, independent approval or scientific efficacy. A self-sealed audit is not a trusted attestation.
4. #1388's control plane must reject incomplete/substituted/reordered gate manifests, gate 0 SKIP, altered status, seal mismatch and input-hash mismatch before `MERGE_READY`. Gate 0 KILL is permitted only as a *terminal denial prefix*, not authorization.
5. Combine both independent TGL status reductions: P-35 SKIP always ESCALATE; Phi PASS with conditional HPG SKIP also ESCALATE; legitimate Phi WARN may leave HPG SKIP without incorrectly being escalated on that basis.
6. Preserve `TriadicGovernanceLoop.REQUIRED_STEPS = frozenset({1, 2, 3, 4, 5, 6, 8})` exactly. Canonical Epoch 004 preflight binds this historical value; introducing 0 into this constant breaks the frozen protocol identity even if the runtime decision is safer. Implement P-35 admission logic separately.

## Migration policy — requires human protocol decision

**Historic reproducibility lane:** Reproduce an accepted historical experiment only from its exact pinned runtime, lockfiles, protocol and input/evidence hashes under the already authorized historical contract. Such replay does **not** establish the new P-35 guarantee. Do not silently substitute a modern runtime while calling the result equivalent.

**Prospective governance lane:** Any use of the new P-35 fail-closed semantics in a PDMAL numerical experiment requires a new explicitly versioned adapter and protocol profile, approved policy predicate implementation, predicate authenticity/currentness/invariant-to-input binding, seeded negative cases and fresh preregistration/authorization. Do not implement an unconditional `lambda True` compatibility shim. Until authorized, stop with `FAIL_CLOSED`; do not publish new treatment results.

## Proposed admission checks

- Unit: missing, noncallable, non-boolean and exception-raising predicates; explicit False; explicit True plus provenance ceiling; Herald PASS cannot override SKIP/KILL.
- Cross-component: trace prefix and unique canonical gates; Phi/HPG conditional; current-input SHA-256 binding; seal tamper; origin/replay claims explicitly outside #1519/#1388 scope.
- PDMAL: each of the three adapters on a synthetic single-step state records P-35 SKIP, final ESCALATE, decision FAIL_CLOSED, `AttemptStatus.FAILURE` and no numerical update **without mutating frozen source**; preserve complete negative fixture and independent reviewer verdict.
- Workflow: exact-head hosted PPTL/quality/security, governance, pre-freeze, canonical treatment preflight, signed history and independent non-author review.
- Security: fix dependency CVE via separately admitted signed maintenance; do not bypass `pip-audit`, rewrite dependency locks here or claim overall green CI from passing subset.
- Release gate: signed reviewed integration successor reconciles #1388, #1387 and #1367; separately accepted authority, not same-system green tests, controls main admission.

## #1387 event redaction and #1367 authenticated provenance boundary

The same integration rehearsal includes signed-source [PR #1387](https://github.com/ndrorchestration/DGAF-Framework/pull/1387)'s narrow TGL runner-error event redaction: `TGL_RUNNER_FAILURE.reason` is the constant `"TGL runner exception"`, not `str(exc)`. Its two signed-source adversarial tests check multiline synthetic secret injection and an exception whose `__str__` raises. The #1388 verifier's independent structural checks remain in force. **The #1387 commit itself is signed, but its reauthored copy on this integration branch is unsigned**. The original exception remains chained as Python `__cause__`, so downstream exception/traceback consumers require their own confidentiality review; redacted audit events alone do not provide end-to-end secrecy.

[Issue #1367](https://github.com/ndrorchestration/DGAF-Framework/issues/1367) is **not remedied** by this rehearsal. A complete audit record bound to `SHA256(input_text)` can be self-sealed by an untrusted runner, reused for the same input under different authority contexts, and lack any independent verification of policy freshness. A prospective control-plane evidence contract therefore needs all of:

- A control-plane-owned attempt identifier or nonce, task/session/agent identity, policy/invariant-set version, authorization context digest and canonical input digest.
- A trusted-runner boundary and an externally verifiable attestation/signature or an explicitly limited internal trust decision; do not treat an unkeyed, runner-generated hash as a signature.
- Replay-specific binding and atomic attempt consumption with negative controls for stale, cross-context and cross-task records.
- A separate versioned protocol, key/lifecycle/revocation policy, reviewer approval and integration test authorization before any accepted security-assurance claim.

No new cryptographic origin primitive or context-binding authority is supplied here. A configured `True` predicate still reports only a local callback outcome, **not proven current/authorized constitutional verification**.

## Non-effects

No frozen experimental input, protocol, statistical analysis, custody material, interpretation, locked result or claim state is changed by this engineering note. No PDMAL empirical execution or external authorization is requested. **RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.**
