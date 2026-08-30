# Minimal DGAF Construct Spec — SUPERSEDED

**Superseded by:** `docs/experiment/MINIMAL_DGAF_CONSTRUCT_DECISION_2026-08-30.md`
(commit `ee529878486cae7e4fe213173ea7daa16642abbe` on `main`, 2026-08-30).

This earlier draft resolved the A/B/C gate classification as **B/C** (only P-35
constitutive; the seven historical gates not constitutive of the tested
treatment). The operator has since affirmed the authoritative decision in
`ee529878`, which resolves it as:

- **A (constitutive / required):** P-31, P-33, DemiJoule, P-27, P-29, P-32, P-30.
  These are `REQUIRED_STEPS` in the canonical TGL contract that the `dgaf`
  condition invokes on every consensus iteration. They are therefore constitutive
  of the *defined* treatment even when currently unwired. Unwired ⇒ SKIP ⇒
  FAIL_CLOSED ⇒ the implemented treatment is invalid/incomplete — **not**
  out-of-scope. The earlier "removal test" used the wrong axis (it measured
  current behavioral contribution rather than membership in the defined treatment).
- **B (out of scope):** HPG (step 7, conditional), Herald (step 9, evidence/fan-out),
  and other non-required historical governance capabilities.

This draft's B/C conclusion is **retracted**. The seven gates are pre-N=1 blocking:
N=1 may proceed only after they are faithfully restored or adapted (Issue #152
R5–R7). Where a faithful semantic translation cannot be established, the gate
remains FAIL-CLOSED and N=1 of the full `dgaf` treatment is blocked (operator
invariant: Missing(X) ≠ Proxy(Y); Correlation(X,Y) ≠ Restoration(G_X, Y)).

The corrected anti-trap rule (operator, 2026-08-30):

> A component is pre-N=1 blocking when removing it would change the **defined
> treatment being executed** — not merely when it produces a nonzero behavioral
> contribution in its current broken state.

No apparatus, freeze, or authorization change. This file is retained only as a
record of the superseded reasoning.
