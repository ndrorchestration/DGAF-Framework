# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Selected pilot candidate:** PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Selected candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus/source anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This checklist distinguishes implemented controls from executed verification evidence. Historical candidates and historical verifier runs remain provenance only. No historical result transfers to the selected candidate.

## Candidate identity reconciliation

- [x] Historical candidate identities are retained without evidence transfer.
- [x] Selected candidate is explicitly identified as `58ba9a…` with tree `abdbc9b…`.
- [x] Selected candidate remains pre-freeze and fail-closed.
- [x] P7 exact-candidate provenance binding is recorded separately for the adopted scientific specification.
- [ ] New candidate reaches a verified immutable freeze state.

## TGL/P-35 contract prerequisite

- [x] Fail-closed remediation path is implemented.
- [x] Selected-candidate regression callers provide the explicit premise checker.
- [x] Selected-candidate CI wave completed successfully, including DGAF regression and pre-authorization/pre-freeze validation.
- [ ] Full production-cycle exercise under an approved PDMAL constitutional premise policy.
- [ ] All remaining semantic skip/audit-state predicates independently demonstrated for final frozen execution.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis are explicit required fields.
- [x] Schema rejects malformed FFCR outcomes and inconsistent success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Corrective tests cover artifact/document identity, matrix uniqueness, blinded balance, retention integrity, unblinding bijection, bootstrap invariants, and recovery-state semantics.
- [x] Current selected candidate has successful instrumentation/schema/control evidence.

## Current candidate-tree CI evidence

- [x] Governance CI executed for selected candidate `58ba9a…` — run `33616403706`.
- [x] P8-relevant pre-freeze validation executed for selected candidate — run `33616403754`.
- [x] P8-relevant pre-authorization security executed for selected candidate — run `33616403843`.
- [x] Artifact/schema/security and regression checks passed in the September 2 workflow wave.
- [x] Run IDs and candidate SHA are retained in the current evidence dossier.
- [x] Pre-freeze job logs were directly inspected for the fail-closed runner/provenance contract job.

## Historical evidence boundaries

- [x] Historical E2b/M6/P2/P6a/P9 evidence remains explicitly scoped to its producing identity.
- [x] Prior P2/P6a evidence for `92ff830b…` is not reused for `58ba9a…`.
- [x] Prior completion-candidate P3/P4/P5/P6/P9 evidence is not reused for `58ba9a…`.

## Runtime verification

- [ ] Fresh authenticated P2 five-case matrix for `58ba9a…` on an exact-Git-SHA deployment.
- [ ] Fresh authenticated P6a four-case CORS matrix for `58ba9a…` on that same deployment.
- [ ] Exact deployment Git SHA independently confirmed.
- [ ] Provider rate-limit blocker cleared sufficiently to establish the required deployment identity.

## P9 final-candidate verification

- [ ] Fresh independent P9 verification for `58ba9a…` after the P-35 remediation is incorporated.
- [ ] Broader P9 evidence-chain closure against the selected candidate.
- [ ] External durable archive/custody requirements independently satisfied where required.

## Reproducibility and provenance

- [x] Selected-candidate source/tree identity is recorded.
- [x] Environment/dependency/toolchain fingerprints are retained in current candidate evidence.
- [x] Deterministic instrumentation and artifact hashes are retained.
- [ ] Final candidate-bound reproduction chain is independently closed.
- [ ] Seed/RNG separation and final trial ordering independently verified for the eventual frozen execution.

## Evidence custody and negative state

- [x] Current candidate CI artifacts are retained by GitHub Actions.
- [ ] Current candidate artifacts are independently retrieved from a durable external archive.
- [ ] Retrieval hashes are independently verified against the durable archive record.
- [x] Current verification artifacts retain negative-state evidence: N=0, no authorization, no pilot, no unblinding in the verification job/workspace.
- [ ] Full operational blinding custody boundary is independently closed.

## Closure rule

P8 remains open until every applicable unchecked item has current candidate-scoped evidence. Historical or synthetic evidence cannot substitute for current-candidate verification.

**Current state:** `P8 OPEN / FAIL-CLOSED`; GitHub CI is green for `58ba9a…`, while deployment-bound P2/P6a, operational P4, durable P6, final P9, freeze, authorization, and empirical execution remain open.
