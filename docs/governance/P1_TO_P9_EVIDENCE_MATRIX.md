# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED
**Current `main`:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
**Current-tree verification boundary:** `ac8ea26…`
**E2b exact-tree closure:** `d299dd152fb82d48a066d66a64bf0917e20d6167` / run `33047380487`
**Empirical N:** `0`
**Pilot authorization:** `NOT GRANTED`
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does not constitute executed evidence. Historical evidence remains scoped to the exact SHA/run/artifact that produced it.

## State precedence

`current live main > current executable verification boundary > historical candidate/freeze`.

The historical candidate `e6beeb66335e1b50a239697badab22dab50eb5ba` and historical verifier merge-ref `2516f32…` remain provenance only for current freeze decisions. The prior M6 evidence targeting that historical candidate is non-closing for `ac8ea26…`.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact current-tree identity and provenance | **OPEN** | current candidate retained and independently reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **BLOCKED / OPEN** | matrix passes with exact candidate/deployment identity |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **OPEN** | current candidate-scoped evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current candidate evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | end-to-end current evidence verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **BLOCKED / OPEN** | matrix passes on same deployment as P2 |
| P7 Scientific Target | explicit authority adoption + exact binding | **FORMALLY OPEN** | authority/date/decision identity recorded and cryptographically bound |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture |

## Additional freeze-admissibility predicates

| Predicate | Requirement | State |
|---|---|---|
| E2b | immutable verifier-toolchain runtime/dependency/workflow/environment fingerprint | **CLOSED / VERIFIED @ `d299dd1…`** |
| M6 | machine-retained proof of N=0/no authorization/no pilot/no unblinding | **OPEN / CURRENT-TREE VERIFICATION REQUIRED @ `ac8ea26…`** |

E2b closure is retained historical exact-tree evidence. Because the Governance CI workflow subsequently changed at `ac8ea26…`, current-tree applicability requires execution of the corrected binding before it is used as current freeze evidence. This does not retroactively invalidate the `d299dd1…` result.

## Verified E2b evidence

- Run: `33047380487` — **SUCCESS**
- Exact tree: `d299dd152fb82d48a066d66a64bf0917e20d6167`
- Artifact: `9636185725`
- Artifact digest: `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`
- Exact checkout/target assertion: **PASS**
- Hash-pinned installation: **PASS**
- Exact-tree provenance emission: **PASS**

## Current-tree verification boundary

At `ac8ea26…`, Governance CI binds `PDMAL_TARGET_CANDIDATE_SHA` to `${{ github.sha }}`. This removes the previous hard-coded historical-candidate rebinding path. A successful current-tree execution and independent inspection remain required.

## Remaining critical path

1. Execute current-tree E2b/M6 verification on `ac8ea26…`.
2. Inspect and retain the resulting artifact.
3. Independently verify integrity, scope, and negative-state claims.
4. Complete authenticated P2/P6a runtime verification against the exact deployment identity.
5. Complete P4 blinding/custody, P5 reproducibility, and P6 durable custody.
6. Complete formal P7 authority adoption/binding.
7. Close P8 only after exact-candidate evidence inspection.
8. Execute P9 independent verification.
9. Create and independently verify a new immutable freeze.
10. Obtain explicit pilot authorization.
11. Only then execute the authorized blinded pilot.

**No freeze exists. No pilot is authorized. Empirical N = 0.**
