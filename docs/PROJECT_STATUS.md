# DGAF/PDMAL Project Status

**Status date:** 2026-08-26  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** resolve from GitHub `main` at verification time  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in structured pre-freeze closure. `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is the historical superseded implementation freeze. The current corrected verification candidate is `e6beeb66335e1b50a239697badab22dab50eb5ba`; it has a READY production deployment, but no corrected apparatus has been independently freeze-verified. No new freeze exists and no empirical pilot has been authorized or executed.

P7 is **technically adjudicated but formally OPEN pending authority adoption and exact binding**. The P7 record now resolves the scientific decisions against the current candidate; formal closure still requires authority adoption and cryptographic binding to the exact protocol/apparatus identity. The protocol has been reconciled so that the experiment is explicitly described as controlled runtime characterization containing a pre-specified comparative DGAF-versus-null analysis, without converting the characterization into a production-efficacy claim. P8 remains open until executable analysis implementation/configuration, candidate-scoped runtime predicates, custody, and provenance are fully evidenced.

The remaining work is evidence production, implementation/configuration binding, authenticated runtime verification, independent verification, freeze, and authorization—not permission to infer evidence from implementation or documentation.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Corrected executable candidate | `e6beeb...` | Candidate-scoped governance/repository checks passed; READY Vercel deployment exists; formal P2/P6a execution and downstream verification remain pending |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Historical characterization; non-empirical pilot evidence |
| Environment | VERIFY | Candidate environment identity must be captured and reconciled at execution time |
| Execution contract | PARTIAL | Contract tests and governance CI exist; authenticated exact-candidate P2 runtime evidence pending |
| Artifact contract | PARTIAL | Schema/identity/balance controls strengthened; candidate artifact execution and retained evidence pending |
| Security / blinding | PARTIAL | Fail-closed controls and synthetic procedures present; fresh operational custody verification pending |
| Topology provenance | PARTIAL | Fingerprint machinery present; exact candidate recomputation pending |
| Provenance / reproducibility | PARTIAL | Candidate provenance chain defined; final execution artifact packet pending |
| Durable retention | OPEN | Archive/retrieval/hash proof not yet established for the current candidate |
| Primary contrast | SELECTED / P7 TECHNICALLY ADJUDICATED | Full `dgaf` vs `null`, FFCR primary endpoint, seed-paired primary analysis; formal P7 adoption/binding pending |
| P7 scientific specification | OPEN / PENDING AUTHORITY ADOPTION | Scientific decisions resolved; formal adoption and exact cryptographic binding remain open |
| Analysis lock | OPEN / P8 | Exact executable analysis implementation/configuration identity and candidate binding required |
| Independent verification | NOT EXECUTED | Separate candidate/evidence audit required |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Current deployment boundary

- Candidate SHA: `e6beeb66335e1b50a239697badab22dab50eb5ba`
- Vercel deployment ID: `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`
- Deployment target: production
- Deployment state: READY
- `/api/health`: HTTP 200; `psi_cubic=true`; version `1.8.0`

The READY deployment is deployment evidence only. Formal P2 and P6a workflows still require authenticated execution against this exact deployment identity.

## Historical evidence boundary

Historical P2/P6a evidence remains scoped to the exact application source, deployment, workflow run, and artifact that produced it. The retained P6a result for `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` is historical evidence and does not certify the current mainline candidate.

Similarly, historical documentation may preserve former terminology such as the 340% coordination-gain claim or the former FLAG-02 meaning. Such references are provenance records, not current claims.

## Documentation reconciliation rule

Living/current documents must use current terminology and current gate status. Historical records must not be mechanically rewritten merely to make them look current; instead, their temporal scope must remain explicit. `FLAG-02` is a historical identifier; current evaluation-mode terminology is **qualitative**. The former 340% coordination-gain statement is not a current verified result.

## Required closure sequence

1. Complete authenticated P2 runtime verification against `e6beeb66335e1b50a239697badab22dab50eb5ba` and deployment `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`.
2. Complete authenticated P6a CORS verification against the same deployment identity.
3. Execute candidate-scoped artifact, negative-path, determinism, and topology-invariant tests and retain evidence.
4. Complete synthetic and operational blinding verification as applicable.
5. Establish durable evidence custody and direct retrieval/hash verification.
6. Reconcile topology fingerprints and environment identity on the exact candidate.
7. Complete formal P7 authority adoption and cryptographic binding to protocol/runner/analysis/freeze identities.
8. Bind the executable analysis implementation/configuration to the exact candidate and protocol identity.
9. Freeze canonical protocol, artifact schema, endpoints, statistical analysis plan, baselines, and negative controls.
10. Derive P1–P8 from candidate-scoped evidence.
11. Perform P9 independent verification.
12. Create a new immutable freeze and independently verify that exact freeze.
13. Obtain explicit pilot authorization.
14. Only then execute the authorized 50-seed blinded pilot.

**Empirical validity is NOT ESTABLISHED. Pilot authorization is NOT GRANTED. N = 0.**
