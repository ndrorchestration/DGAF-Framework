# DGAF Custody, Freeze, and Recovery Boundary

**Status:** PROPOSED / ARCHITECTURE BOUNDARY / NON-AUTHORIZING

## Custody is cross-cutting assurance

Custody belongs primarily to **A2 — Provenance & Custody Assurance**.

It provides reusable primitives for:
- exact source/artifact identity;
- controlled access and separation;
- retention and retrieval;
- cryptographic binding;
- protected-lane handling;
- custody receipts and evidence;
- independently enforceable blinding/separation where required.

Custody may gate K2/K3/K4 decisions when a policy requires it, but custody itself is not a universal execution step for every DGAF-governed action.

## Freeze is profile policy

An immutable freeze is **not** a universal K1–K8 kernel state.

Freeze semantics belong to profiles that require prospective immutability, such as:
- controlled experiments;
- blinded analysis;
- external-review handoffs;
- exact-candidate validation;
- specific high-assurance or release profiles.

The Track A freeze apparatus is an example of a profile using A2 custody/provenance primitives plus K4 transition controls and K8 evidence/claim ceilings.

### Canonical rule

`CUSTODY_PRIMITIVE != FREEZE_REQUIREMENT`

A profile may require freeze. The kernel must support exact identity, evidence, state guards, and authority checks needed to enforce that policy, but it must not impose dataset/analysis freeze on unrelated governed actions.

## Recovery and reconciliation are kernel behavior

Recovery/reconciliation belongs primarily to **K7 — Postcondition, Ambiguity, Recovery & Reconciliation**.

Reusable kernel semantics include:
- outcome-known vs outcome-unknown;
- postcondition verified / failed / inconclusive;
- reconcile-before-retry;
- rollback / compensate / contain / escalate selection;
- no silent success promotion after ambiguous effect;
- audit-before-closure.

Profiles may add stronger recovery procedures, custody, human approval, or rollback-material requirements.

## Novelty boundary

The paired recovery-composition benchmark retained on protected main reports:
- 11 paired synthetic cases;
- parity: 11/11;
- differences: 0;
- no unique composition/recovery advantage under matched semantics.

Therefore:

**DGAF must not present K7's current bounded recovery/idempotency mechanisms as inherently unique merely because they are implemented inside DGAF.**

The architecture contribution, if supported, must instead be evaluated at the level of:
- how governance components are composed;
- evidence/provenance attachment;
- fail-closed claim-state discipline;
- inspectability/reproducibility;
- cross-component authority boundaries;
- empirical effects under controlled comparison.

## Architectural mapping

| Mechanism | Primary owner | Secondary dependencies |
|---|---|---|
| Source/artifact hashes, custody receipts | A2 | K6, K8 |
| Blinding/key separation | A2 / profile | K2, K3, K4 |
| Immutable experimental freeze | Profile | A2, K4, K8 |
| Candidate-source drift checks | A2 | K1, K4, K6 |
| Unknown execution outcome | K7 | K5, K6 |
| Rollback/compensation decision | K7 | K4, K6 |
| Recovery material custody | A2 + K7 | K6 |
| Independent review package freeze | Profile | A2, K8 |

## Non-effect

This boundary classification changes no custody requirement, freeze state, recovery authorization, experimental lifecycle, scientific N, efficacy, or High-Assurance status.
