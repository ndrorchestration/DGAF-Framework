# Claim / Evidence Index

**Current reconciliation:** 2026-08-31  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main control-plane lineage:** resolve `main` directly in GitHub; the literal tip SHA is intentionally not embedded here.  
**Current apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` (PR #174 merge; seven-gate restoration + complete seven-gate provenance binding).

> **Reconciliation notice:** Historical claim/evidence rows below preserve their original evidence scope. They must not be read as a current-candidate status ledger. The current apparatus source is `2a54a67d…` after PR #174 completed provenance binding for all restored gate-state substrates. Fresh runtime and experimental evidence is required for the post-#174 candidate cycle.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. Engineering restoration and provenance integrity are complete; candidate-scoped runtime and scientific verification remain outstanding. Historical P2/P6a/P3–P9 evidence remains source-bound and is not transferred.

**Last substantive evidence reconciliation:** 2026-08-31  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`

This index maps high-impact claims to the evidence class actually supported by retained evidence. It is intentionally conservative and claim-specific. Historical rows below preserve their original evidence scope; current-state assertions should be taken from `docs/CURRENT_STATE.md` and exact current GitHub/Vercel evidence.

The repository runs a deterministic claim-language audit (`.github/workflows/claim-hygiene.yml`). Textual presence alone is not treated as proof of overclaiming; contextual review is required. Residual contextual candidates remain historical audit material unless separately reconciled.

The evidence-gate toolchain and quality rows below preserve historical scope. Current-candidate status is controlled by exact apparatus/deployment binding and fresh verification.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Historical Governance CI and TLC artifact. | Bounded state graph only; not an unbounded mathematical proof; not current live-production efficacy evidence. | TLC failure/counterexample, changed specification/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` — historical scope | Historical Python CI/staging evidence stage. | Repository-local deterministic harness only; not automatically transferred to the current apparatus. | Harness assertion failure, altered semantics, or contradictory independent observation. |
| DGAF Python test suite passes under the historically executed Python matrix. | `VERIFIED` — historical matrix | Historical Python 3.10/3.11/3.12 runs. | Historical toolchain; does not itself establish current-candidate runtime behavior. | Current-candidate failure or supported-runtime policy change. |
| DGAF security scan completes successfully. | `VERIFIED` — historical configured scan | Historical Python CI security stage. | Historical configured scope and dependency state. | New findings, dependency changes, scan-scope changes, or materially different tool interpretation. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` — historical tested behavior | Historical Governance CI P-42 stage. | Unit/regression behavior only; not a current-candidate efficacy claim. | Test regression, altered scoring/control logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` evidence class | Historical evaluator artifact. | Fixture predictions are repository-authored evaluator inputs; not DGAF/model performance. | Fixture corruption, scorer mismatch, generated outputs differing from labels, or independent failure. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No current retained end-to-end transaction trace establishing this claim. | Contracts/deployment configuration are insufficient. | Dated end-to-end request/event trace bound to exact source/deployment. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Historical local harness only in the retained index. | Local harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is retained. | Synthetic tests and engineering validation do not establish efficacy. | Reproducible real-workload evaluation under the defined protocol. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Historical quality logs. | Functional tests do not establish global formatting/type cleanliness. | Current configured formatting/type gates fail or pass. |
| Evidence-gate toolchain is pinned and fully verified across the supported Python matrix. | `IMPLEMENTED / PENDING CURRENT-CANDIDATE VERIFICATION` | `requirements-ci.txt` and historical runs. | Historical verification does not by itself establish current-candidate runtime support. | Current-candidate full matrix success or policy revision. |
| DGAF is deployed to Vercel and has current live runtime verification. | `CURRENT DEPLOYMENT PENDING / RUNTIME VERIFICATION PENDING` | Pre-correction deployment is historical only; new deployment must be source-matched to `2a54a67d…`. | Deployment readiness is not P2/P6a runtime verification. | Fresh candidate-bound P2/P6a/runtime evidence. |
| Repository-local epistemic evidence standard is canonical. | `VERIFIED` — standard scope | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`. | Repository-local governance standard, not external scientific authority. | Reconciliation required if evidence classes/closure rules change. |
| Canonical claim/evidence index is current in lineage metadata. | `RECONCILED 2026-08-31; substantive evidence rows remain historical` | This document. | Historical rows preserve exact original evidence scope. | Any material source/evidence change requires reconciliation. |

## Current apparatus additions requiring candidate-scoped evidence

- **P-31:** restored and provenance-bound; engineering completion, not experimental verification.
- **P-33:** restored and provenance-bound; engineering completion, not experimental verification.
- **P-27:** restored and parity-tested against recovered v3.5 behavior; candidate-scoped verification remains required.
- **P-29:** restored under the authorized Sentinel risk/halt designation; substrate path and provenance binding are tested; candidate-scoped verification remains required.
- **P-30:** restored under the authorized acceptance-schema/gold-star designation; candidate-scoped verification remains required.
- **P-32:** restored under historical PHI_STAR/KILL_REC behavior with direct parity coverage; candidate-scoped verification remains required.
- **DemiJoule:** restored as the authorized six-axis semantic-safety gate. The historical heuristic's WARN/reprompt reachability limitation remains documented and is not silently altered.

## Current candidate runtime binding

- Apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Production deployment: **NOT YET ESTABLISHED FOR THIS APPARATUS**
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`
- The pre-correction deployment `dpl_76UU8mCm…` and all evidence derived from it are historical/non-closing.
- Fresh P2/P6a inputs must be generated only after a deployment is verified READY and source-matched to `2a54a67d…`.

## Open repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#51** — supported-runtime policy and Python matrix alignment.
- **#53** — repository-wide semantic audit for overclaiming verification language; residual contextual review remains historical unless re-opened by current evidence.
- **#54** — evidence-gate toolchain pinning is implemented; current-candidate verification remains.
- **#59** — semantic triage of residual high-impact claim-language findings.

## Current evidence hierarchy

1. Current main-branch execution evidence outranks historical runs for present-state claims.
2. Machine-readable retained artifacts outrank narrative status text.
3. Exact-claim evidence outranks adjacent or proxy evidence.
4. Independent evidence outranks self-authored assertions when validating efficacy.
5. Contradictory evidence remains visible and must trigger reconciliation or claim downgrade.

## Status vocabulary

Use the canonical ladder in [`EPISTEMIC_EVIDENCE_STANDARD.md`](EPISTEMIC_EVIDENCE_STANDARD.md):

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`

The status is claim-specific. A repository is never globally `VERIFIED` merely because one subsystem or workflow passes.
