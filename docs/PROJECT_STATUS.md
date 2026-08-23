# DGAF/PDMAL Project Status

**Status date:** 2026-08-23
**Repository:** `ndrorchestration/DGAF-Framework`
**Current main:** resolve from GitHub `main` at verification time
**Pilot status:** PRE-FREEZE; authorization not granted
**Empirical N:** 0

## Executive state

The repository is in structured pre-freeze closure. `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is the historical superseded implementation freeze. The corrected pilot apparatus and governance controls are present on mainline, but no corrected apparatus has been independently freeze-verified. No new freeze exists and no empirical pilot has been authorized or executed.

P7 primary scientific adjudication is now adopted. The protocol has been reconciled so that the experiment is explicitly described as controlled runtime characterization containing a pre-specified comparative DGAF-versus-null analysis, without converting the characterization into a production-efficacy claim. P8 remains open until the executable analysis implementation/configuration is bound to the exact candidate apparatus.

The remaining work is evidence production, implementation/configuration binding, independent verification, freeze, and authorization—not permission to infer evidence from implementation or documentation.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Corrected runner | CANDIDATE | Exact-SHA gate, task adapter, artifact validation, and security controls present; fresh candidate verification pending |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Historical characterization; non-empirical pilot evidence |
| Environment | VERIFY | Candidate environment identity must be captured and reconciled at execution time |
| Execution contract | PARTIAL | Contract tests exist; fresh exact-candidate CI execution pending |
| Artifact contract | PARTIAL | Schema/sidecar validation present; candidate artifact execution and retained evidence pending |
| Security / blinding | PARTIAL | Fail-closed controls and synthetic operational procedure present; fresh operational verification pending |
| Topology provenance | PARTIAL | Fingerprint machinery present; exact candidate recomputation pending |
| Provenance / reproducibility | PARTIAL | Candidate provenance chain defined; execution artifact packet pending |
| Durable retention | OPEN | Archive destination and direct custody/retrieval proof not established |
| Primary contrast | ADOPTED | P7: full `dgaf` vs `null`, FFCR primary endpoint, seed-paired primary analysis |
| Analysis lock | OPEN / P8 | Exact executable implementation/configuration identity and candidate binding required |
| Independent verification | NOT EXECUTED | Separate candidate/evidence audit required |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Historical evidence boundary

Historical P2/P6a evidence remains scoped to the exact application source, deployment, workflow run, and artifact that produced it. The retained P6a result for `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` is historical evidence and does not certify the current mainline candidate.

Similarly, historical documentation may preserve former terminology such as the 340% coordination-gain claim or the former FLAG-02 meaning. Such references are provenance records, not current claims.

## Documentation reconciliation rule

Living/current documents must use current terminology and current gate status. Historical records must not be mechanically rewritten merely to make them look current; instead, their temporal scope must remain explicit. `FLAG-02` is a historical identifier; current evaluation-mode terminology is **qualitative**. The former 340% coordination-gain statement is not a current verified result.

## Required closure sequence

1. Execute the full repository audit on an immutable candidate and retain its coverage manifest.
2. Run fresh engineering/unit/contract tests on that exact candidate.
3. Run candidate-scoped artifact, negative-path, determinism, and topology-invariant tests.
4. Execute current-candidate P2 runtime verification.
5. Execute current-candidate P6a CORS verification.
6. Complete synthetic operational blinding verification.
7. Establish durable evidence custody and direct retrieval/hash verification.
8. Reconcile topology fingerprints and environment identity on the exact candidate.
9. **P7 primary scientific target specification — ADOPTED.**
10. **P8 analysis lock — NEXT GATE.** Bind the executable analysis implementation/configuration to the exact candidate and protocol identity.
11. Derive P1–P8 from candidate-scoped evidence.
12. Perform P9 independent verification.
13. Create a new immutable freeze and independently verify that exact freeze.
14. Obtain explicit pilot authorization.
15. Only then execute the authorized 50-seed blinded pilot.

**Empirical validity is NOT ESTABLISHED. Pilot authorization is NOT GRANTED. N = 0.**
