# DGAF/PDMAL Project Status

**Status date:** 2026-08-26  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** resolve from GitHub `main` at verification time  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in structured pre-freeze closure. `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is the historical superseded implementation freeze. The corrected pilot apparatus and governance controls are present on mainline, but no corrected apparatus has been independently freeze-verified. No new freeze exists and no empirical pilot has been authorized or executed.

P7 is **technically adjudicated but formally OPEN pending authority adoption**. The panel-ready P7 record presents the 11 scientific decisions that must be explicitly adopted and bound to the exact protocol/candidate identity before P7 can be represented as closed. The protocol has been reconciled so that the experiment is explicitly described as controlled runtime characterization containing a pre-specified comparative DGAF-versus-null analysis, without converting the characterization into a production-efficacy claim. P8 remains open until the executable analysis implementation/configuration is bound to the exact candidate apparatus and candidate-scoped evidence is retained.

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
| Primary contrast | SELECTED / P7 TECHNICALLY ADJUDICATED | Full `dgaf` vs `null`, FFCR primary endpoint, seed-paired primary analysis; formal P7 adoption pending |
| P7 scientific specification | OPEN / PENDING AUTHORITY ADOPTION | All 11 decisions in the panel-ready adjudication record remain open until explicit authority adoption and binding |
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

1. Establish a new immutable candidate identity from the corrected post-merge apparatus; do not reuse the superseded `2a80f819...` candidate for corrected-CI closure.
2. Execute the full repository audit on that immutable candidate and retain its coverage manifest.
3. Run fresh engineering/unit/contract tests on that exact candidate.
4. Run candidate-scoped artifact, negative-path, determinism, and topology-invariant tests.
5. Execute current-candidate P2 runtime verification.
6. Execute current-candidate P6a CORS verification.
7. Complete synthetic and operational blinding verification as applicable.
8. Establish durable evidence custody and direct retrieval/hash verification.
9. Reconcile topology fingerprints and environment identity on the exact candidate.
10. **P7 scientific target specification — TECHNICALLY ADJUDICATED / FORMALLY OPEN until authority adoption.**
11. **P8 analysis lock — NEXT GATE.** Bind the executable analysis implementation/configuration to the exact candidate and protocol identity.
12. Derive P1–P8 from candidate-scoped evidence.
13. Perform P9 independent verification.
14. Create a new immutable freeze and independently verify that exact freeze.
15. Obtain explicit pilot authorization.
16. Only then execute the authorized 50-seed blinded pilot.

**Empirical validity is NOT ESTABLISHED. Pilot authorization is NOT GRANTED. N = 0.**
