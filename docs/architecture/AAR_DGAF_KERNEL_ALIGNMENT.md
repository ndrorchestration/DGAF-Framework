# AAR to DGAF Kernel Alignment

**Status:** PROPOSED / ARCHITECTURE ALIGNMENT / NON-AUTHORIZING

## Finding

DGAF does not currently contain two equivalent general-purpose authorization engines.

`AAR_V1` is a **bounded action-admission implementation/profile** for exactly:
- action class: `AUDIT_COUNTER_UPDATE_V1`;
- target: `/api/audit`;
- policy: `AAR_AUDIT_POLICY_V1`;
- decision effect: non-scientific ephemeral audit-counter update only.

Its own coverage report explicitly remains incomplete and identifies:
- process-local replay only;
- record-local revocation only;
- server-HMAC trust anchor;
- no production issuer;
- no durable action ledger;
- no other action-class coverage.

The Python capability-governance implementation is broader and provider-neutral. It models action canonicalization, effective authority, non-widening delegation, state guards, policy enforcement, idempotency/outcome ambiguity, execution receipts, postconditions, reconciliation, and evidence/authority separation.

## Canonical placement

Treat `AAR_V1` as a **bounded K1–K5 profile/adapter**:

- K1 — its canonical action digest is action identity;
- K2 — parent/delegated scopes and expiry/revocation are bounded authority inputs;
- K3 — `validateAuditAdmission` is its admission/enforcement point;
- K5 — `usedRecordIds` is a bounded process-local replay mechanism and record-local revocation is a limited trust safeguard.

It also emits/participates in K6-style evidence through its coverage and audit pathway, but it is not the canonical implementation of K6.

## Convergence target

Future expansion of Action Admission should reuse the generic DGAF kernel contracts rather than grow a second general authority stack inside `app/lib/action-admission.ts`.

Specifically:

1. New action classes should use the generic canonical action/effect identity model.
2. Delegation and effective authority should use the same non-widening semantics.
3. Commit-time guards and revocation should use the generic authority vocabulary where semantics match.
4. Durable replay should bind to effect identity rather than record ID.
5. Execution evidence should use the common receipt/reconciliation shapes where applicable.
6. A future `AAR_V2` may remain a domain record, but its authority semantics should be mapped explicitly to K1–K8 instead of becoming an independent kernel.

## Preserve bounded behavior

Do not rewrite `AAR_V1` merely for architectural uniformity. Its exact current bounded behavior is evidence-bearing and tested.

Any migration should be:
- additive or versioned;
- test-first;
- claim-preserving;
- backward-compatible where required;
- explicit about changed replay/revocation/trust semantics.

## Non-effect

This alignment record does not expand AAR coverage, admit a durable provider, establish authoritative revocation, establish an issuer/trust-anchor lifecycle, authorize new action classes, or change scientific/High-Assurance state.
