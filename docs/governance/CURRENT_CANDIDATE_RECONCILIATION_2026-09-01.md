# Current Candidate Evidence Reconciliation — 2026-09-01

## Scope

This record reconciles current candidate/deployment evidence with older candidate-bound governance records. It is a control-plane/evidence record only. It does **not** create a freeze, grant authorization, or contribute empirical observations.

## Current runtime candidate

- Candidate/source commit: `92ff830b1c67413df745e37087e6447c9c251b9a`
- Candidate tree: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- Production deployment: `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`
- Deployment target: `production`
- Deployment state: `READY`
- Source SHA binding: exact match to candidate commit

## Verified current-cycle runtime evidence

### P2

- Workflow run: `33509348174`
- Artifact: `9800942933`
- Evidence class: `P2_RUNTIME_EXECUTION`
- Result: **PASS / VERIFIED**
- Matrix: five required cases passed
- Artifact SHA-256 recorded by the evidence workflow: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`

The downloaded artifact is a GitHub Actions artifact package containing `p2-runtime-verification.json`. The local byte hash of that JSON file is not expected to equal the GitHub artifact-package digest; those are different integrity domains.

### P6a

- Workflow run: `33509416955`
- Artifact: `9800972819`
- Evidence class: `P6A_CORS_RUNTIME_EXECUTION`
- Result: **PASS / VERIFIED**
- Matrix: four required CORS cases passed
- Artifact SHA-256 recorded by the evidence workflow: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`

The downloaded artifact is a GitHub Actions artifact package containing `p6a-cors-verification.json`; the workflow-recorded digest is the artifact-package integrity value and is distinct from a local extracted-file hash.

## Current P3 assessment

The current pilot artifact validator is `experiments/pdmal_pilot/pilot_artifact_schema.py`.

It currently enforces:

- complete required pilot-record fields;
- full 40-character frozen commit SHA;
- optional exact identity matching for commit, seed, protocol, experiment, and environment;
- canonical per-record SHA-256 recomputation;
- blinded condition IDs;
- canonical topology set;
- canonical failure-count set;
- boolean FFCR outcome;
- exactly `180` records per seed;
- unique matrix cells;
- unique trial IDs covering exactly `0..179`;
- exactly four blinded conditions with `45` cells each;
- sidecar verification through `verify_sidecar()`.

The current `run_pilot.py` imports and invokes `validate_artifact()` and `verify_sidecar()` in `_write_and_validate_artifact()` before retaining each pilot artifact. Therefore the older claim that the current runner does not perform inline pilot-artifact validation is **historical/stale** and must not be used as a current-state defect without re-verification against this commit.

P3 is nevertheless not promoted to CLOSED here because no authorized pilot artifact exists at this candidate and empirical N remains zero.

## P4–P6 status

Existing records named below are candidate-bound to historical candidate `c6157158bf0ee4840e99a381a4b99bd2febe2302` and are retained as historical provenance:

- `P4_Security_Blinding_Attestation.md`
- `docs/experiment/P5_REPRODUCIBILITY_RECORD.md`
- `docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION.md`
- `docs/GOVERNANCE/P7_BINDING_RECORD_2026-08-30.md`

Their CLOSED labels must not be interpreted as current-cycle closure for `92ff830b...`.

## P7/P8 status

The scientific decision remains the adopted primary contrast `dgaf` versus `null`, with FFCR as the primary endpoint, seed-level paired analysis, and the recorded paired-bootstrap configuration. However, the existing P7 binding record is historically bound to `c6157158...`, while `P8_ANALYSIS_LOCK.md` contains older verification-boundary identifiers. Current-cycle P7/P8 evidence must therefore be rebound to the exact candidate that is ultimately proposed for freeze.

## Experimental boundary

- Freeze: **NOT ESTABLISHED**
- Pilot authorization: **NOT GRANTED**
- Empirical N: **0**
- P9: **NOT EXECUTED**

## Identity rule

`main` control-plane tip, apparatus source boundary, candidate identity, deployment identity, and scientific binding identity are separate provenance objects. Evidence may be promoted only when its exact binding is satisfied.

## Next admissible work

1. Create and verify current-candidate P3/P4/P5/P6 evidence records without empirical collection.
2. Rebind P7/P8 scientific/control records to the eventual freeze candidate.
3. Perform independent P9 verification.
4. Construct freeze packet only after all required predicates are satisfied.
5. Grant authorization separately and explicitly; only then may empirical execution change N.
