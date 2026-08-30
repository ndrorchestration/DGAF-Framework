# Minimal DGAF Construct Specification (PDMAL Experiment)

**Status:** DRAFT — defines the constitutive treatment for the PDMAL empirical
characterization. Read-only; does not modify the apparatus, freeze, or
authorization state.

**Date:** 2026-08-30
**Authoritative apparatus:** `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
(treed `dd662325149c42843d5ca99178ca4399fde6f440`)
**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

---

## 1. Purpose

Resolve the Issue #152 A/B/C classification per the research-design rule:

> A historical DGAF component is constitutive of the PDMAL treatment **only if**
> removing it changes the defined treatment in a way that alters the primary
> hypothesis being tested.

This document establishes what "DGAF" *means* in the PDMAL experiment, then maps
every historical gate against that definition. The outcome is the gate-class
map that Issue #152 required, grounded in the frozen apparatus rather than
abstract governance intent.

---

## 2. The frozen treatment definition (code-grounded)

The PDMAL experiment tests a single primary contrast (`analysis.py:5-10`,
`DGAF_QA_ASSERTION_REPORT.md:77-81`):

```text
  T (dgaf)  = full DGAF governance stack
  R (null)  = no-DGAF baseline
  estimand  = mean seed-level paired difference  d_i = FFCR_i(T) − FFCR_i(R)
  inference = prespecified paired-bootstrap CI
  endpoint  = FFCR = (trials completing without failure) / (total trials)
```

The apparatus that *constitutes* T is, verbatim from the merged code:

| Behavior | Code location | Role in treatment |
|---|---|---|
| Domain premise check | `pptl/corpus/inv03_credit_signals.py:48` `premise_check_fn_credit` | P-35 — auto-wired (`orchestrator.py:144-153`); constitutive gate of the DGAF condition |
| Fail-closed control plane | `experiments/pdmal_pilot/dgaf_tgl_adapter.py:141-184` (`_has_unwired_required_gate` → `FAIL_CLOSED` at `:184`) | Prevents the DGAF condition from silently collapsing to the `null`/`simple` baseline (F1 remediation) |
| Bounded decision operator | `dgaf_tgl_adapter.py:172-191` (`alpha=0.2` CONSERVATIVE_MIX else `0.5`) | The numeric treatment effect |

**Constitutive TGL hooks actually wired:** `premise_check_fn` only. All other
TGL hook slots (`scpe_fn`, `kappa_fn`, `sentinel_fn`, `phi_closure_fn`,
`apogee_fn`) are `None` and therefore declared `REQUIRED_STEPS` and SKIP →
FAIL_CLOSED (`:141-184`).

**Conclusion:** the minimal DGAF treatment = P-35 premise check + fail-closed
control plane + bounded decision operator. That is the entire constitutive
construct. Everything else in DGAF's broader governance ecosystem is **not**
part of T as defined.

---

## 3. Historical gate classification (A / B / C)

Test applied to each historical gate: *If removed entirely, does the PDMAL
treatment definition (FFCR contrast, T vs R) change in a way that alters the
primary hypothesis?*

| Gate | Historical substrate | Constitutive of T? | Evidence | Class | Action |
|---|---|---|---|---|---|
| **P-35 premise_check_fn** | corpus credit signals | **YES** | wired in `orchestrator.py:144-153`; sole T gate | **A** | Already bound; part of frozen apparatus |
| **P-31 SCPE** | ContextToken / tier / TIF | No | fails `R` test — not on T execution path; named only as transparency metric | **C** | DO NOT implement; FAIL-CLOSED, documented as out-of-construct |
| **P-27 KAPPA** | eval confidence `0.28/0.25` vs docs `0.22/0.18` | No | contradictory; not on T path | **C** | DO NOT implement; FAIL-CLOSED |
| **P-29 Sentinel** | record/routing audit-only | No | doc HALT vs code audit-only conflict; not on T path | **C** | DO NOT implement; FAIL-CLOSED |
| **P-32 Phi** | weight-graph ratio, missing `KILL_REC` | No | conjugate phi consistent; `KILL_REC` absent; not on T path | **C** | DO NOT implement; FAIL-CLOSED |
| **P-30 Apogee** | attestation stub | No | partial recovery only; not on T path | **C** | DO NOT implement; FAIL-CLOSED |
| **P-33 Convergence** | `‖W_t−W_{t-1}‖_F` (weight graph) | No | substrate absent from `ConsensusState`; listed as *secondary transparency metric* (`DGAF_QA_ASSERTION_REPORT.md:78`), NOT primary endpoint | **C→B pending** | DO NOT implement; `current_final_std` is a transparency metric, not a proxy for P-33 (operator invariant: Missing(X)≠Proxy(Y)) |
| **DemiJoule** | six semantic axes | No | substrate absent; not on T path | **C→B pending** | DO NOT implement; FAIL-CLOSED |

**Classification rule result:** Only **P-35** is **A (constitutive)**. The
remaining seven historical gates are **C (unresolved / not constitutive)** under
the primary contrast. Per the research-design rule, C = *do not implement;
resolve definition first* — and the definition is already resolved: they are
explicitly outside the treatment. They therefore remain **FAIL-CLOSED** and do
not contribute behavior to the characterization.

P-33 and DemiJoule are additionally named in the protocol as *secondary
transparency metrics* (`final_std`, phi-convergence traces),
`DGAF_QA_ASSERTION_REPORT.md:78,81` — explicitly "NOT for hypothesis testing."
Their FAIL-CLOSED execution status does not affect the primary FFCR contrast.

---

## 4. Scientific statement this enables

> The N=1 characterization tests the explicitly defined minimal DGAF treatment
> implemented in the frozen PDMAL apparatus (`05fa286…`, tree `dd662325…`):
> the P-35 premise-check gate plus the fail-closed control plane plus the
> bounded decision operator, contrasted against the no-DGAF `null` baseline on
> the FFCR endpoint (paired seed-level, paired-bootstrap CI).
>
> Historical DGAF governance mechanisms (P-31, P-27, P-29, P-32, P-30, P-33,
> DemiJoule) whose executable semantics are not established on the PDMAL
> `ConsensusState` substrate are **outside the tested construct** and remain
> FAIL-CLOSED. They do not contribute behavior to the characterization and are
> not claimed as part of the treatment. Their recovery/translation is deferred
> (Issue #152 R1–R4 complete; R5–R7 not started) and is a post-N=1 research
> activity, not a pre-N=1 blocker.

---

## 5. Why this is NOT the two failure modes

- **Not "mark them out-of-scope to run":** the out-of-scope status is established
  by the frozen treatment definition (`analysis.py`, `DGAF_QA_ASSERTION_REPORT.md`),
  not asserted for convenience. The A/B/C test was applied to each gate.
- **Not "reconstruct all historical gates":** that would recreate the
  infinite-project trap. Only A-class gates (P-35) are pre-N=1 engineering, and
  P-35 is already bound.

---

## 6. Next transition (ORBIT-N1)

With the minimal construct defined and only P-35 constitutive:

- The 7 historical gates are **not** pre-N=1 blockers (Class C, documented).
- The next valid transition is **fresh candidate-scoped P2 + P6a** pinned to
  `05fa286…` + exact Vercel deployment, then P3–P8, then independent P9, then
  freeze, then authorization, then N=1.
- No R5–R7 work is required for N=1.

---

*This document is the Construct-Spec deliverable requested by the Issue #152
A/B/C decision. It authorizes no gate, no merge, no freeze, no pilot.*
