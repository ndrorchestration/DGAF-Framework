# DGAF Live Demo Walkthrough

This page is the shortest path for evaluating the public DGAF proof-of-operation without first reading the full research and governance history.

## Open the demo

**Public demo:** [Open the DGAF proof-of-operation demo](https://project-7ybao.vercel.app/demo)

The page is intentionally usable without authentication.

## What to do first

Run the two guided cases at the top of the page.

### 1. Allowed action

The demonstration constructs a bounded action with:

- an exact action class and target;
- an explicit policy binding;
- live delegated scope;
- a passing verifier state;
- an action digest bound to the submitted parameters.

Expected path:

`REQUEST → AUTHORITY → ADMISSION → EFFECT → RECEIPT → FRESH ADJUDICATION`

The accepted production demonstration executes the bounded ephemeral audit-counter effect and emits an `AAR_EXECUTION_RECEIPT_V1` with `postcondition=VERIFIED`, `authority_effect=NONE`, and `follow_on_authority=FRESH_ADJUDICATION_REQUIRED`.

The receipt is execution evidence, not continuing authority. A subsequent consequential action requires a fresh admission/adjudication path and new authority; the successful prior receipt cannot silently authorize the next effect.

### 2. Revoked authority

Run the blocked-action case.

The action class remains recognizable, but the authorization is explicitly revoked.

Expected result:

`DENY · AUTHORIZATION_REVOKED`

No execution receipt should be emitted.

This distinction is the core behavior to inspect: **capability and a well-formed request do not substitute for current authority**.

## What DGAF is doing around the action

1. **REQUEST** — identify the exact action, target, parameters, and policy.
2. **AUTHORITY** — inspect the authorization, delegated scope, expiry, and revocation state.
3. **ADMISSION** — evaluate the declared predicates and either admit or deny the action.
4. **EFFECT** — execute only after admission.
5. **RECEIPT** — retain evidence of what executed and whether the bounded postcondition was verified; the receipt has `authority_effect=NONE`.
6. **FRESH ADJUDICATION** — require a new decision and new authorization before any consequential follow-on action; the prior receipt cannot be reused as authority.
7. **CLAIM BOUNDARY** — prevent the resulting evidence from silently becoming a stronger scientific or assurance claim.

A compact description is:

> DGAF is not the button. DGAF is the control chain around the button: what the system wants to do, whether it is authorized, whether it executes, what evidence comes back, why that evidence does not authorize the next action, and what that evidence is allowed to mean.

## Deeper failure cases

The same demo also exposes:

- missing delegated scope → `REQUIRED_SCOPE_MISSING`;
- tampered action parameters → `ACTION_DIGEST_MISMATCH`;
- replay of the same admitted record → first execution succeeds, second request is denied as `AAR_REPLAY`.

## Accepted proof identity

The currently accepted public proof is bound to:

- DGAF source SHA: `ae0d254158fa831162274077872c3f752a891431`;
- Vercel production deployment: `dpl_6W1uTG3sJ6dyU7KJsAzHpXpFXvvU`;
- GitHub Actions workflow run: `36476664359`;
- proof artifact: `tektite-proof-ae0d254158fa831162274077872c3f752a891431`;
- artifact ID: `10993339146`;
- artifact SHA-256: `35a39d19a11d65b7c6af36fe1a6d7e8672636137a66003482d3306505fbe2862`;
- verifier result: `TEKTITE_PROOF_OF_OPERATION_V1 = PASS`.

A separate fresh unauthenticated browser acceptance confirmed that the public alias loads without login, the allowed action visibly executes and emits a receipt, the revoked-authority action is denied without a receipt, and the six-stage walkthrough remains coherent.

## Claim ceiling

The accepted demonstration is bounded engineering evidence only.

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

The demo does **not** establish a general production AAR issuer, durable cross-instance replay protection, independent validation, canonical efficacy, certification, or High-Assurance authorization.
