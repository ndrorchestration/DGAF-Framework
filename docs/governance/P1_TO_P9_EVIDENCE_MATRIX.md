# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED
**Current executable candidate:** `e6beeb66335e1b50a239697badab22dab50eb5ba`
**Current `main`:** `bc325486a2986256532e58dccf39a155ed75a72a`
**Current candidate deployment:** `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`
**Empirical N:** `0`
**Pilot authorization:** `NOT GRANTED`
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does **not** constitute executed evidence. Detailed dependency, freshness, invalidation, and parallel-lane rules are governed by `docs/governance/DYNAMIC_FREEZE_ADMISSIBILITY_CONTROL_2026-08-26.md`.

## State precedence

`current live main > current executable candidate > historical candidate/freeze`.

The historical candidates `2a80f819...`, `83e1678...`, `94fb6fd...`, `b681c87...`, and historical PR heads remain provenance only. They must not be substituted for `e6beeb...` in current verification or freeze decisions.

The 18 commits from `e6beeb...` to current `main` are documentation/governance synchronization successors as presently audited. A substantive executable/schema/workflow/dependency/protocol/analysis change would invalidate the candidate binding and require a new candidate plus affected-predicate re-verification.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact candidate/tree identity and provenance | **READY → OPEN** | exact candidate retained and independently reconciled; no substantive drift |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **BLOCKED** | P2 matrix passes with exact candidate/deployment identity and retained artifacts |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **READY → OPEN** | candidate-scoped execution and retained integrity evidence |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | operational blinding evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | candidate-scoped reproducibility evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED/OPEN** | end-to-end custody evidence retained and verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **BLOCKED** | four-case matrix passes on same deployment as P2 |
| P7 Scientific Target | explicit authority adoption + exact binding | **FORMALLY OPEN** | authority/date/decision identity recorded and cryptographically bound |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture of assumptions/toolchain |

## Additional freeze-admissibility predicates

| Predicate | Requirement | State |
|---|---|---|
| E2b | immutable verifier-toolchain runtime/dependency/workflow/environment fingerprint | **OPEN — #105** |
| M6 | machine-retained proof of N=0/no authorization/no pilot/no unblinding | **OPEN — #106** |

These are required for freeze admissibility but are not additional scientific hypotheses.

## Current candidate-scoped evidence

The candidate has fresh evidence for:

- Governance Sweep: run `32977423225` — **SUCCESS**
- Full Repository Coverage Audit: run `32977423223` — **SUCCESS**
- IP & Claim Hygiene: run `32977423310` — **SUCCESS**
- Vercel production deployment: **READY**
- Candidate deployment ID: `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`
- Candidate `/api/health`: HTTP 200, `psi_cubic=true`, version `1.8.0`

These establish engineering/deployment evidence only. They do not constitute P2/P6a closure or efficacy evidence.

## Remaining critical path

1. Configure `VERCEL_AUTOMATION_BYPASS_SECRET` out-of-band.
2. Execute P2 five-case runtime matrix.
3. Execute P6a four-case CORS matrix.
4. Produce E2b verifier-toolchain fingerprint evidence.
5. Produce M6 negative-state evidence.
6. Complete P4 operational blinding/custody verification.
7. Complete P5 environment/topology/reproducibility evidence.
8. Complete P6 durable custody and independent retrieval/hash verification.
9. Complete P7 authority adoption and cryptographic binding.
10. Close P8 only after exact-candidate evidence inspection.
11. Execute P9 independent verification.
12. Create and independently verify an immutable freeze.
13. Obtain explicit pilot authorization.
14. Only then execute the authorized blinded pilot.

## Dynamic invalidation rule

Any substantive change to executable code, workflow behavior, dependencies, schemas, protocol semantics, analysis semantics, blinding semantics, failure/recovery semantics, deployment behavior, or verification-toolchain provenance invalidates the affected candidate/predicate bindings.

Documentation-only successors may update live governance records without advancing the executable candidate, provided the audit confirms no substantive apparatus change.

## Historical boundary

Older matrix contents and candidate identities are preserved in Git history as provenance. They are not current state. The current matrix intentionally supersedes stale candidate references so agents and reviewers do not mistake historical planning records for live freeze authority.

**No predicate is currently CLOSED. No freeze exists. No pilot is authorized. N=0.**
