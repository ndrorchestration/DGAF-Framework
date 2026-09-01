---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-01
applies_to_ref: completion/2026-09-01-exact-candidate
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

## Current controlled boundary

The active completion candidate is `566273c6c2906bdf71827381493a26ee7697034c` on draft PR #187, branch `completion/2026-09-01-exact-candidate`. It is not merged to `main`. This candidate is the current control-plane/provenance verification target; it does not constitute a freeze or authorization boundary.

The previous exact-candidate cycle at `cea9e49deb6738f29deefa95b1357b8c1663b6b3` is superseded. Its PDMAL/P9 artifacts and run results remain historical evidence and are not transferred to `566273c6…`.

## Current engineering state

The candidate includes:

- exact candidate identity checks (`HEAD == GITHUB_SHA`);
- deterministic PDMAL structural/instrumentation verification;
- P5 RNG-stream separation and deterministic digest checks;
- P9 independent `jq -S -c` canonicalization/hash verification;
- exact-candidate authority-identity regression;
- candidate/run/artifact/digest reconciliation in the completion controller;
- fail-closed baseline synthesis when exact evidence is absent;
- structured predicate-evidence deserialization in `scripts/completion_controller.py`.

The latest PDMAL candidate-bound run passed the substantive deterministic structural tests, artifact generation/custody checks, and registry generation, but the workflow's final one-seed structural dry-run step failed because its embedded Python shell command has malformed quoting. This is a CI implementation defect, not empirical failure. The correct response is a new narrowly scoped candidate repair followed by a fresh complete verification cycle.

## Authoritative state table

| Boundary | Status | Meaning |
|---|---|---|
| `main` | CONTROL-PLANE LINEAGE | Documentation/evidence lineage; not automatically the experimental candidate |
| PR #187 candidate | CURRENT / DRAFT / UNMERGED | `566273c6…`; exact current control-plane verification target |
| Previous candidate | SUPERSEDED | `cea9e49…`; no evidence inheritance |
| P2 | OPEN | Fresh authenticated exact-candidate runtime evidence required |
| P3 | OPEN | Fresh exact-candidate artifact-contract evidence required |
| P4 | OPEN | Fresh security/blinding/custody operational evidence required |
| P5 | OPEN | Fresh exact-candidate reproducibility execution required |
| P6 | OPEN | Fresh archive/retrieval/hash custody proof required |
| P6a | OPEN | Fresh authenticated exact-candidate CORS evidence required |
| P7 | OPEN / EXTERNAL SCIENTIFIC DECISION | Must be explicitly bound to final candidate/protocol/analysis/freeze |
| P8 | OPEN / FAIL-CLOSED | Current-candidate prerequisites and analysis binding incomplete |
| P9 | OPEN | Current-candidate independent verification required |
| Freeze | NOT CREATED | No immutable freeze identity exists |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No empirical execution |

## Evidence and authority boundary

Engineering CI success, deterministic tests, deployment readiness, artifact custody, synthetic fixtures, documentation, and independent structural verification are not PDMAL efficacy evidence and do not authorize experimentation. The completion controller can reconcile evidence predicates but cannot manufacture P7, freeze, authorization, or empirical results.

## Recursive verification principle

The control plane is being used to reduce mechanical verification bottlenecks through automation and independent re-checks, not to bypass governance. Parallel PDMAL/P9 execution, exact SHA/run/artifact binding, deterministic retries, custody checks, and completion reconciliation shorten candidate → diagnosis → repair → re-verification cycles while preserving fail-closed transitions.

## Closure sequence

1. Repair the malformed PDMAL structural dry-run command and create a new candidate.
2. Re-run PDMAL instrumentation and P9 against that exact SHA.
3. Reconcile current-candidate P3–P6/P9 evidence.
4. Execute authenticated P2/P6a for the exact candidate/deployment.
5. Complete P4/P5/P6.
6. Resolve and bind P7 as the external scientific decision.
7. Close P8 only from current-candidate evidence.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the authorized blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
