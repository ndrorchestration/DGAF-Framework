# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment that produced it.

## Current project state — 2026-09-02

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No pilot authorization has been granted and empirical **N = 0**.

`main` remains the documentation/control-plane lineage. The active completion/remediation candidate is PR #199, branch `remediation/p35-minimal-mainline-2026-09-02`, head `fb485e9e0fd253be03e6937a448f4818eb8d54a1`, based directly on current `main`. This candidate supersedes the earlier remediation/completion branches for the active completion path; historical evidence from prior candidates is not transferred.

## Active P-35 remediation boundary

PR #199 carries the minimal current-mainline P-35 remediation: the DGAF pilot runner requires an explicit callable `PDMAL_PREMISE_CHECKER`, `ConsensusTask(condition="dgaf")` rejects omission, and the checker is propagated through `DGAF_TGLAdapter` into `TGLHooks`. Regression coverage exercises missing/malformed/non-callable configuration, explicit injection, premise KILL, and the real runner/task/adapter/TGL path.

No PDMAL-specific constitutional policy is invented by this change. A real pilot remains fail-closed until an approved checker is supplied by the experimental-control design. PR #199 is not frozen and does not authorize empirical execution.

## Historical candidate boundaries

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Previous mainline runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`, tree `73cf3ad…`; P2/P6a evidence remains bound to its exact deployment.
- Previous controlled completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`; PDMAL/P9 evidence remains bound to its exact tree.
- Previous P-35 remediation PR #188 and its heads are historical engineering evidence only.

These identities remain useful provenance records but none is the active candidate for closure of the remediated apparatus.

## Experimental gate state

| Boundary | Status |
|---|---|
| Corrected apparatus source | `2a54a67d…` |
| Active completion/remediation candidate | `fb485e9e…` / PR #199 |
| P-35 implementation | `IMPLEMENTED / EXACT-HEAD VALIDATION PENDING` |
| P2 | `HISTORICAL VERIFIED / RE-RUN REQUIRED` |
| P3 | `HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED` |
| P4 | `OPEN` |
| P5 | `OPEN` |
| P6 | `OPEN / FAIL-CLOSED` |
| P6a | `HISTORICAL VERIFIED / RE-RUN REQUIRED` |
| P7 | `ADOPTED / FINAL BINDING OPEN` |
| P8 | `OPEN / FAIL-CLOSED` |
| P9 | `HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED` |
| New immutable freeze | `NOT CREATED` |
| Pilot authorization | `NOT GRANTED` |
| Empirical N | `0` |

## Existing evidence retained by scope

Prior PDMAL instrumentation run `33572123862`, artifact `9825740072`, and prior independent P9 run `33572123857`, artifact `9825660346`, remain valid historical evidence for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`. They are not promoted to PR #199 because the P-35 boundary materially changed.

Prior P2 run `33509348174` / artifact `9800942933` and P6a run `33509416955` / artifact `9800972819` remain bound to runtime candidate `92ff830b…` and deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. They must be rerun against the final selected candidate/deployment.

## Current TGL contract boundary

- required unwired gates are `SKIP` and reduce the turn to `ESCALATE`;
- `WARN` propagates to `TurnStatus.WARN` unless a stronger failure applies;
- HPG is conditional on Phi-Closure and cannot run after terminal failure;
- terminal failures stop downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid gate outcomes do not silently become PASS;
- P-35 premise checking is explicitly injected for DGAF treatment execution and is fail-closed when absent.

## Canonical agent-role boundary

- Sentinel-Phi — canonical governance/security identity.
- Professor Prodigy — formalization/proof; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis; no independent normative authorization.
- Reciprocity — fairness and affected-party review.
- Herald — evidence/public-surface publication; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity/archive/provenance/routing integrity.
- Apogee — independent evidence/integrity review.

Generic execution roles do not create or elevate agent authority.

## Remaining critical path

1. Exact-head pre-freeze validation of PR #199.
2. P-35 adjudication from exact-head evidence.
3. Select the resulting exact experimental candidate.
4. Fresh P3–P6 and affected P2/P6a verification against that exact candidate/deployment.
5. Final P7 scientific/protocol binding.
6. P8 closure.
7. Independent P9 verification against the final candidate.
8. New immutable freeze and independent verification.
9. Separate explicit pilot authorization.
10. Only then execute the blinded pilot and allow empirical N to advance from 0.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
