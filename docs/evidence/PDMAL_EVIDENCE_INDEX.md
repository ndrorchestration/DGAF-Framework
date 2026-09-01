---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-01
applies_to_sha: a43219b4ed91fff8615f6c655ab3d17ca871fc29
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically. The latest completion
  candidate is the current P9 execution target; the mainline runtime candidate
  remains separately identified. No freeze or authorization is implied.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current documentation lineage | CURRENT | `main` | Active control/documentation lineage |
| Current mainline runtime candidate | CURRENT / NOT FROZEN | `92ff830b…` / tree `73cf3ad…` | Current production/runtime evidence target on mainline |
| Latest completion candidate | CONTROLLED / NOT FROZEN | `a43219b…` | Exact candidate for current scoped verification on completion branch |
| Prior completion candidate | SUPERSEDED / HISTORICAL | `562753b…` | P9 run `33567199896` scoped only to this superseded candidate |
| Candidate deployment provenance | VERIFIED FOR MAINLINE RUNTIME | `92ff830b…` → `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` | P2/P6a current runtime evidence; re-run if pilot candidate changes |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | Seven-gate restoration/provenance lineage |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…` | Prior candidate cycle; evidence does not transfer |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267…` | Historical provenance only |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b868…` | Historical apparatus only |
| Corrected pilot runner | IMPLEMENTED / EVIDENCE GATED | runner/schema controls | Selected candidate still requires complete current-cycle evidence |
| TGL contract | CURRENT ENGINEERING CONTROL / VERIFIED | current remediation lineage | Engineering control evidence; not experimental authorization |
| Environment lock | VERIFY | CI dependency/runtime configuration | Final selected candidate must bind exact environment fingerprint |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not efficacy evidence |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic/control evidence only |
| Artifact contract | IMPLEMENTED / CANDIDATE-BOUND | `pilot_artifact_schema.py` + run `33572123862` | Current completion-candidate artifact evidence retained |
| Security controls | VERIFIED FOR ENGINEERING SCOPE | current Governance/PDMAL security CI | Does not substitute for P4 operational custody |
| Topology provenance | VERIFY | `PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` | Recompute/bind against exact selected candidate |
| Durable retention | OPEN | policy | Operational archive + independent retrieval/hash proof required |
| Primary contrast | ADJUDICATED / BINDING PENDING | `dgaf` vs `null`; FFCR; paired seed | Exact final candidate/freeze binding remains required |
| Analysis lock | OPEN / FAIL-CLOSED | P8 control plan | Exact final candidate/configuration binding required |
| P2 runtime | VERIFIED — MAINLINE CANDIDATE | Run `33509348174`; artifact `9800942933`; candidate `92ff830b…` | Five-case authenticated runtime predicate evidence |
| P6a CORS runtime | VERIFIED — MAINLINE CANDIDATE | Run `33509416955`; artifact `9800972819`; candidate `92ff830b…` | Four-case authenticated CORS predicate evidence |
| P3 artifact contract | VERIFIED — COMPLETION CANDIDATE | Run `33572123862`; artifact `9825367738`; candidate `a43219b…` | Exact-candidate instrumentation artifact passed required dry-run contract checks |
| P4 blinding/security | VERIFIED — WORKFLOW-LEVEL COMPLETION EVIDENCE | Run `33572123862`; artifact `9825367738`; candidate `a43219b…` | Secret presence was checked without disclosure and masked dry-run output was produced; full operational custody closure remains separate |
| P5 provenance/reproducibility | VERIFIED — COMPLETION CANDIDATE | Run `33572123862`; artifact `9825367738`; candidate `a43219b…` | Exact candidate/artifact binding, RNG stream separation, deterministic digest, and environment fingerprint were recorded |
| P6 durable evidence custody | VERIFIED — WORKFLOW-LEVEL COMPLETION EVIDENCE | Run `33572123862`; artifact `9825367738`; candidate `a43219b…` | Same-run artifact download and inner-CSV checksum re-verification passed; durable external archive closure remains open |
| P9 independent verification | SCOPED PASS — CURRENT COMPLETION CANDIDATE | Run `33572123857`; artifact `9825316781`; candidate `a43219b…` | Exact identity, alternate canonicalization/hash path, and authority identity regression passed; broader P9 closure remains open |
| P9 prior scoped verification | PASS — SUPERSEDED CANDIDATE | Run `33567199896`; artifact `9823570326`; candidate `562753b…` | Historical scoped identity/hash/authority verification only |

## Candidate identity boundary

- `2a54a67d…` is the corrected apparatus provenance anchor.
- `92ff830b…` / `73cf3ad…` is the current mainline runtime candidate/tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` is the deployment bound to current P2/P6a evidence.
- `a43219b…` is the latest controlled completion candidate and current exact-candidate verification target.
- `562753b…` is the superseded completion candidate whose P9 run remains historical evidence.
- `main` is the documentation/evidence lineage and is not itself the apparatus identity.

## Evidence inheritance rule

Historical P2/P6a evidence does not automatically qualify a different candidate. P9 evidence for `562753b…` does not qualify `a43219b…`, `92ff830b…`, or `main`. A candidate change requires explicit re-binding and fresh affected-predicate evidence.

A later documentation/control commit does not redefine the apparatus candidate unless executable apparatus behavior changes; a controlled completion branch nevertheless uses the exact branch tip as its verification identity.

## Current exact-candidate PDMAL dry-run evidence

Run `33572123862` completed successfully on 2026-09-01 for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Verified in that run:

- exact checkout identity (`HEAD == GITHUB_SHA`);
- `PDMAL_BLINDING_KEY` was present and its value was withheld;
- deterministic smoke reproduced identically;
- P5 RNG stream separation and deterministic digest checks passed;
- structural/artifact test suite returned `19 passed`;
- masked one-seed dry-run CSV was generated and schema validation passed;
- CSV SHA-256 sidecar matched the recomputed checksum;
- uploaded artifact was successfully downloaded in a separate step and its inner CSV checksum re-matched;
- completion-controller evaluation marked P3/P4/P5/P6 promotable while P2/P7/P8/P9 remained blocking.

Artifact ID: `9825367738`.  
Artifact ZIP digest: `sha256:51b89e5321674ff19eecc53a4445237677025649fe36ed5ddc762835a24c2c6c`.  
Inner CSV SHA-256: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.

The workflow's evidence registry marks P3, P4, P5, and P6 `VERIFIED` for this exact candidate. P4 and P6 are explicitly workflow-level/synthetic custody evidence and must not be conflated with full operational blinding/custody closure.

## Current P9 scoped evidence

Fresh run `33572123857` completed successfully on 2026-09-01 for exact candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

Verified:

- exact checkout identity (`HEAD == GITHUB_SHA`);
- independent `jq -S -c` canonicalization plus `sha256sum` hash path matched the DGAF/Python deterministic-case digest;
- authority identity regression, 4 tests passed;
- authorization was represented as external and empirical execution was explicitly false;
- independent P9 evidence JSON and SHA-256 sidecar were uploaded successfully.

Independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.  
P9 artifact ID: `9825316781`.  
P9 artifact ZIP digest: `sha256:15e5ba72dd524f90b0bb3499c9b0b3f7de602f0e1905b0734183e830c22af671`.

This is a **current-candidate scoped P9 pass**. It does not by itself establish broader P9 closure, P2/P6a for `a43219b…`, P7 exact freeze binding, P8 analysis lock, durable external archive, experimental authorization, empirical execution, or efficacy.

## Prior P9 scoped evidence history

Run `33567199896` is a successful independent-verification execution against `562753b3053b3566b0fcad1b0b1df151d7de119a`.

Artifact ID: `9823570326`.  
Artifact ZIP digest: `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This remains scoped historical evidence for `562753b…` and is not closure for `a43219b…`.

## Current selected-candidate execution boundary

Before pilot execution, one exact candidate must be explicitly selected and rebound across:

1. apparatus/source identity;
2. deployment identity;
3. P3 artifact contract;
4. P4 blinding/security;
5. P5 reproducibility;
6. P6 durable custody;
7. P7 scientific decision;
8. P8 analysis lock;
9. P9 complete evidence-chain verification;
10. immutable freeze and separate authorization.

## Historical-priority boundary

The historical review is a separate evidence domain. Current adjudication establishes substantial prior art for the individual mechanisms, while leaving only a narrower cross-domain architectural integration as a conditional historical hypothesis. See `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

## Remaining gate sequence

1. Bind/finalize P2 and P6a for the intended completion candidate if that candidate remains the pilot target; existing runtime evidence is only for `92ff830b…`.
2. Finalize P7 exact scientific/protocol/apparatus binding for the selected candidate.
3. Close P8 against the same candidate.
4. Complete broader P9 evidence-chain closure against the same candidate after all prerequisites are current.
5. Create and independently verify the immutable freeze.
6. Obtain explicit pilot authorization.
7. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
