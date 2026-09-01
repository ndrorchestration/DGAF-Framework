# DGAF/PDMAL — Current-Candidate Evidence Readiness — 2026-09-01

## Scope

This record is a non-authorizing control/evidence assessment for the current runtime candidate. It does not create empirical observations, freeze the apparatus, grant authorization, or change empirical N.

## Exact identity chain

- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Corrected apparatus tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- Current runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`
- Current runtime candidate tree: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- Current P2/P6a production deployment: `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`
- Candidate lineage: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 → 92ff830b1c67413df745e37087e6447c9c251b9a`

## Verified runtime evidence

### P2
- Run: `33509348174`
- Artifact: `9800942933`
- Digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`
- State: VERIFIED
- Required matrix: 5/5 passed
- Fail-closed case: `valid_missing_audit` → HTTP 503 / `BLOCKED`

### P6a
- Run: `33509416955`
- Artifact: `9800972819`
- Digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`
- State: VERIFIED
- Required matrix: 4/4 passed
- Allowed-origin preflight: HTTP 204
- Disallowed-origin preflight: HTTP 403

## P3 assessment

Implementation is present on the current runtime candidate. The frozen/pilot artifact contract `experiments/pdmal_pilot/pilot_artifact_schema.py` enforces the current package-level structural predicates identified in the control record, and `run_pilot.py` invokes artifact and sidecar validation before retention.

A successful instrumentation dry run also exists:
- Run: `33516447975`
- Artifact: `9803868540`
- Digest: `sha256:c3a615301222d64d6fe53537eb242af288c311d241035341439a987131683391`

However, that dry run executed on documentation/control-plane commit `da40b085…`, not exact candidate `92ff830b…`. It is therefore supporting evidence and does not close current-candidate P3.

**Disposition: IMPLEMENTATION PRESENT / EVIDENCE OPEN.**

## P4 assessment

Existing P4 closure records are historical and explicitly bound to candidate `c6157158…`. They are not transferable to the current runtime candidate. Current P4 requires fresh operational evidence covering custody, access separation, bijection, and the current blinding procedure.

**Disposition: OPEN.**

## P5 assessment

Existing P5 closure records are historical and explicitly bound to candidate `c6157158…` / tree `6195063e…`. Current implementation provides deterministic topology/failure RNG stream separation and deterministic serialization, but current-candidate execution/reproducibility evidence must be retained against the exact current candidate boundary.

The instrumentation dry run provides supporting evidence but is not a substitute for candidate-scoped P5 closure because its workflow head is `da40b085…`.

**Disposition: OPEN.**

## P6 assessment

Existing P6 closure is historical and explicitly bound to candidate `c6157158…`. The historical attestation proves the retention/hash mechanism, but not current-candidate custody. Current P6 requires a retained current-candidate artifact plus independent retrieval and hash verification at the applicable evidence boundary.

**Disposition: OPEN / FAIL-CLOSED.**

## P7 / P8 / P9

- P7 scientific target: adopted; exact final candidate/protocol/analysis/freeze binding remains open.
- P8: OPEN / FAIL-CLOSED until TGL/P-35 prerequisites and exact candidate analysis/protocol bindings are verified.
- P9: NOT EXECUTED; independent verification must operate after the current candidate evidence package is complete.

## Stale documentation rule

Older records stating that inline artifact validation is missing are historical/stale observations. They remain preserved as historical snapshots. They are not current implementation defects. Current evidence status is determined by the current implementation and exact candidate-scoped execution records.

## Critical path

`P3 current-candidate evidence → P4 current custody/blinding evidence → P5 current reproducibility evidence → P6 current durable-custody proof → P7 exact binding → P8 TGL/P-35 verification → independent P9 → new immutable freeze → explicit authorization → blinded pilot`

## Hard boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**

No state in this record authorizes empirical execution or unblinding.