# DGAF/PDMAL Project Status

**Status date:** 2026-09-01  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Controlled completion candidate:** `566273c6c2906bdf71827381493a26ee7697034c`  
**Candidate branch:** `completion/2026-09-01-exact-candidate`  
**PR:** #187 (draft; unmerged)  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository remains **PRE-FREEZE / FAIL-CLOSED**. PR #187 is the current controlled candidate for the completion-control, provenance-reconciliation, and P9 independent-verification machinery. It is not merged to `main` and does not authorize a freeze, pilot, unblinding, or empirical execution.

The candidate-bound cycle has already demonstrated that the substantive verification machinery can pass deterministic structural tests, artifact generation/custody checks, and registry generation. The latest PDMAL workflow nevertheless ends with a CI-only defect in its final one-seed structural dry-run shell command: the embedded Python invocation is malformed by missing command quoting. This is the immediate engineering blocker. It does not constitute experimental failure and must be repaired by a new candidate commit; evidence from the preceding candidate is not transferred.

P9 was implemented as an independent verification path using a second canonicalization/hash implementation (`jq -S -c` plus `sha256sum`) and exact-candidate authority-identity regression. The completion controller was corrected to accept structured predicate evidence without weakening candidate identity checks. These are implementation capabilities, not closure of P9 or any downstream governance gate until fresh exact-candidate runs complete successfully.

## Gate board

| Gate / control | Current status | Boundary / next proof |
|---|---|---|
| E2b | CLOSED / VERIFIED — historical scope | Retain exact historical execution boundary; do not generalize to current candidate |
| M6 | CLOSED / VERIFIED — historical candidate scope | Retain exact candidate/run boundary; no automatic inheritance |
| P2 | OPEN | Fresh authenticated five-case runtime matrix on exact current candidate/deployment |
| P3 | OPEN | Fresh candidate-bound artifact contract evidence |
| P4 | OPEN | Fresh custody, bijection, access-separation, and operational blinding evidence |
| P5 | OPEN | Fresh candidate-bound reproducibility execution and retained packet |
| P6 | OPEN | Independent archive → retrieval → hash verification for current evidence |
| P6a | OPEN | Fresh authenticated four-case CORS matrix on exact current candidate/deployment |
| P7 | OPEN / EXTERNAL DECISION | Scientific decision must be explicitly bound to final candidate/protocol/analysis/freeze identity |
| P8 | OPEN / FAIL-CLOSED | Current-candidate prerequisites and analysis binding remain incomplete |
| P9 | OPEN | Current-candidate independent verification must execute and bind run/artifact evidence |
| Freeze | NOT CREATED | No immutable freeze identity exists |
| Pilot authorization | NOT GRANTED | Separate explicit governance transition |
| Empirical data | ZERO | No authorized empirical execution has occurred |

## Current verification architecture

1. **Candidate identity:** every current verification begins from an exact Git SHA and must reject mismatched `HEAD`/`GITHUB_SHA`.
2. **PDMAL structural dry run:** verifies deterministic topology/instrumentation behavior without launching the planned 9,000-observation experiment.
3. **P5 contract checks:** verify RNG-stream separation, deterministic repeated cases, and digest equality.
4. **P9 independent verification:** reproduces canonicalization/hash independently and runs authority-identity regression.
5. **Evidence custody:** artifacts are uploaded, retrieved, and checksum-verified; controller additionally binds workflow/artifact metadata.
6. **Completion reconciliation:** the controller can reconcile asynchronous PDMAL/P9 completion and synthesize a fail-closed baseline when evidence is missing.
7. **Governance boundary:** the controller evaluates evidence predicates but cannot manufacture P7, freeze, authorization, or empirical results.

## Provenance rule

Evidence is bound to the tuple appropriate to the claim: source SHA, workflow run, deployment identity, artifact ID, and artifact digest. A successful run on a superseded candidate is historical evidence only. In particular, the earlier exact-candidate PDMAL/P9 cycle on `cea9e49deb6738f29deefa95b1357b8c1663b6b3` is superseded by `566273c6c2906bdf71827381493a26ee7697034c` and does not certify the current candidate.

## Current engineering issue

**Immediate blocker:** repair the malformed final one-seed PDMAL structural dry-run command on the controlled branch. Prefer a heredoc or otherwise unambiguous shell quoting. The repair must create a new candidate identity and trigger the complete candidate-bound verification chain.

Do not resolve this by copying prior artifacts, editing evidence records to imply success, manually promoting predicates, merging PR #187, exposing blinding material, or starting empirical execution.

## Mathematical notation

`φ` is the Golden Ratio, `(1+√5)/2 ≈ 1.618033989`.

`ρ` is the mathematical plastic number, `≈1.3247179572447454`, the unique real root of `x³ - x - 1 = 0`.

`pP` / **Platinum Mean** is DGAF-specific notation for the regular-hendecagon unit-side circumradius, `1/(2 sin(π/11)) ≈ 1.774732842`; it is not the plastic number and must not replace `ρ`.

## Required closure sequence

1. Repair the current CI defect and create a new candidate.
2. Re-run candidate-bound PDMAL instrumentation and P9 verification.
3. Reconcile P3–P6/P9 evidence without cross-candidate transfer.
4. Investigate and execute authenticated P2/P6a against the exact candidate/deployment.
5. Complete P4/P5/P6 current-cycle evidence.
6. Resolve P7 as an external scientific decision and bind it exactly.
7. Close P8 only from current-candidate evidence.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the authorized blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
