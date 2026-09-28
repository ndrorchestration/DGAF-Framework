# DGAF Interactive Proof of Operation

## Purpose

This page is the shortest evaluator path into Dynamic Governance Agentic Formation (DGAF).

The public demonstration is available at:

**https://project-7ybao.vercel.app/demo**

It is intended to make one DGAF idea concrete before a reviewer reads the full architecture or research history:

> capability, authority, execution, evidence, and permission to make a claim are separate states.

## What to do first

Run these two guided cases.

### 1. Allowed bounded action

Expected path:

`REQUEST → AUTHORITY → ADMISSION → EFFECT → RECEIPT → CLAIM BOUNDARY`

Expected result:

- the request carries live delegated scope;
- admission succeeds;
- the bounded ephemeral audit-counter effect executes;
- an `AAR_EXECUTION_RECEIPT_V1` is returned;
- receipt postcondition is `VERIFIED`;
- the claim boundary remains unchanged.

### 2. Revoked authority

Expected path:

`REQUEST → AUTHORITY → DENY`

Expected result:

- the authorization record is correctly formed but marked revoked;
- admission returns `AUTHORIZATION_REVOKED`;
- the bounded effect does not execute;
- no execution receipt is produced.

## What the demonstration is actually using

The demo uses the repository's bounded `AAR_V1` action-admission path and the real `/api/audit` effect endpoint.

The public shell issues only the five hard-coded demonstration scenarios:

- authorized;
- revoked authority;
- missing delegated scope;
- tampered action;
- replay of the same admission record.

The production demo uses an isolated server-only trust channel. It does not establish the general production `DGAF_AAR_HMAC_KEY` issuer.

## Accepted production evidence

Current accepted production lineage at publication:

- protected-main source: `ae0d254158fa831162274077872c3f752a891431`;
- Vercel deployment: `dpl_6W1uTG3sJ6dyU7KJsAzHpXpFXvvU`;
- deployment target: production;
- exact-source deployment verification: PASS;
- live 30-turn regression: PASS;
- `TEKTITE_PROOF_OF_OPERATION_V1`: PASS;
- public unauthenticated browser walkthrough: PASS.

The five production proof scenarios established:

| Scenario | Expected bounded result |
| --- | --- |
| Authorized | executes; verified receipt emitted |
| Revoked | `AUTHORIZATION_REVOKED`; no receipt |
| Missing scope | `REQUIRED_SCOPE_MISSING` |
| Tampered action | `ACTION_DIGEST_MISMATCH` |
| Replay | first execution succeeds; second attempt `AAR_REPLAY` |

## Claim boundary

A successful demonstration does not promote the research or assurance state.

The machine-readable and public-browser evidence both preserve:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

The demo effect is explicitly:

`NON_SCIENTIFIC_EPHEMERAL_AUDIT_COUNTER_UPDATE_ONLY`

## How to interpret a successful run

A successful allowed action supports this bounded engineering statement:

> For the exact deployed path tested, a correctly formed action with the declared scoped authority was admitted, executed, checked against its bounded postcondition, and represented by an execution receipt.

It does not support these stronger statements:

- DGAF is independently validated;
- DGAF has established canonical empirical efficacy;
- the demonstration establishes production security for arbitrary actions;
- High-Assurance operation is authorized;
- a receipt creates future authorization.

## One-sentence explanation

**DGAF is not the button. DGAF is the control chain around the button: what the system wants to do, whether it is authorized, whether it actually executes, what evidence comes back, and what that evidence is allowed to mean.**

## Where to go next

After the 60-second demo:

1. read [`docs/CURRENT_STATE.md`](../CURRENT_STATE.md) for the current evidence and authorization state;
2. read [`README.technical.md`](../../README.technical.md) for implementation detail;
3. read [`README.governance.md`](../../README.governance.md) for the governance model;
4. use [`docs/qa/DGAF_OPERATOR_SELFTEST.md`](../qa/DGAF_OPERATOR_SELFTEST.md) for a bounded local engineering check.

Tektite is the human-facing shell used by the current demonstration. It is not a second governance authority and is not treated here as the primary public name of the framework.
