# P8 Verification Checklist

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Current `main`:** documentation/evidence lineage; do not treat the branch tip as experimental apparatus identity.  
**Current mainline runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a` / tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Latest controlled completion candidate:** `562753b3053b3566b0fcad1b0b1df151d7de119a` / branch `completion/2026-09-01-exact-candidate`  
**Historical experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Prior pre-remediation candidate:** `c6157158bf0ee4840e99a381a4b99bd2febe2302` (historical/superseded)

This checklist distinguishes implemented controls from executed verification evidence. Historical candidates and historical verifier runs remain provenance only. The selected pilot candidate must receive fresh candidate-scoped evidence before P8 closure.

## Candidate identity reconciliation

- [x] Historical candidate identities are retained without evidence transfer.
- [x] Current mainline runtime candidate `92ff830b…` is explicitly distinguished from the latest completion candidate `562753b…`.
- [x] Completion candidate branch is controlled but not frozen.
- [ ] Intended pilot candidate is explicitly selected and rebound through P7/P8.
- [ ] New candidate reaches a verified freeze state.

## TGL/P-35 contract prerequisite

- [x] Fail-closed remediation path is implemented.
- [ ] Complete candidate-scoped verification of the resulting TGL/P-35 contract.
- [ ] Premise-hook injection exercised by regression tests for the selected candidate.
- [ ] Fail-closed exception containment exercised by regression tests for the selected candidate.
- [ ] `PASS/WARN/SKIP/ESCALATE/KILL` reduction semantics explicitly tested for the selected candidate.
- [ ] Unwired required-gate `SKIP` distinguished from dependency-caused or intentionally non-applicable `SKIP`.
- [ ] Final audit seal proven to represent exactly the authoritative returned audit state.
- [ ] Current selected-candidate CI run, SHA, ref, event, logs, and artifacts retained.

## Candidate artifact contract

- [x] Explicit `ffcr_success` outcome is emitted by the runner.
- [x] `ffcr_success` is integrity-covered and required by the pilot artifact schema.
- [x] Matrix coordinates consumed by analysis (`topology`, `failure_count`) are explicit, required artifact fields.
- [x] Schema rejects malformed FFCR outcomes and `ffcr_success=true` with non-success status.
- [x] Analysis requires complete, non-duplicate condition matrices and an explicit unblinding map.
- [x] Canonical record serialization is shared by runner and schema validation.
- [x] Numeric Boolean values are rejected where integer identifiers/counts are required.
- [x] Corrective tests cover artifact/document identity, matrix uniqueness, blinded balance, retention integrity, unblinding bijection, bootstrap invariants, and recovery-state semantics.
- [ ] Fresh current-selected-candidate execution evidence exists.

## Current candidate-tree CI evidence

- [ ] Governance CI executed against the selected pilot candidate or exact descendant with unchanged executable apparatus and explicit provenance.
- [ ] P8 analysis tests passed in that exact candidate execution.
- [ ] P8 artifact-schema/security tests passed in that exact candidate execution.
- [ ] Compilation passed in that exact candidate execution.
- [ ] Run ID, URL, exact SHA, ref, and event retained.
- [ ] Job logs inspected rather than inferred from a commit/check placeholder.

## Historical evidence boundaries

- [x] Historical E2b verification retained as provenance for its recorded execution.
- [ ] Selected-candidate E2b applicability re-verified after candidate changes.
- [x] Prior P2/P6a evidence retained as exact evidence for `92ff830b…` only.
- [x] P2/P6a status is current for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.

## Runtime verification

- [x] Current mainline P2 five-case matrix: run `33509348174`, artifact `9800942933`, candidate `92ff830b…`.
- [x] Current mainline P6a four-case CORS matrix: run `33509416955`, artifact `9800972819`, candidate `92ff830b…`.
- [ ] Fresh P2/P6a evidence for the selected pilot candidate if it differs from `92ff830b…`.

## P9 scoped verification

- [x] Exact candidate identity verified by `git rev-parse HEAD == GITHUB_SHA` for `562753b…` — run `33567199896`.
- [x] Independent canonicalization path (`jq -S -c` + `sha256sum`) matched the DGAF/Python digest — run `33567199896`.
- [x] Authority identity regression passed (`4 passed`) against exact candidate `562753b…` — run `33567199896`.
- [x] Independent P9 evidence artifact uploaded — artifact `9823570326`.
- [ ] Full broader P9 evidence-chain closure against the selected pilot candidate.
- [ ] External durable archive/custody requirements independently satisfied where required.

## Reproducibility and provenance

- [ ] Executed candidate-tree identity reconciled with all P8 bindings for the selected candidate.
- [ ] Canonical protocol blob SHA bound to the eventual frozen candidate identity.
- [ ] Current candidate-bound E2b/M6 toolchain evidence captured and retained.
- [ ] Environment fingerprint evidence captured and assessed.
- [ ] Deterministic topology fingerprints reproduced for the selected candidate.
- [ ] Seed/RNG separation and trial ordering independently verified.

## Evidence custody and negative state

- [ ] Selected-candidate CI logs/artifacts retained at a durable location.
- [ ] Retained candidate artifacts retrieved independently.
- [ ] Retrieval hashes verified against recorded integrity values.
- [ ] Blinding custody boundary documented without exposing the key.
- [ ] Current selected candidate has a machine-retained negative-state artifact proving N=0, no authorization, no pilot, and no unblinding.

## Closure rule

P8 remains open until every applicable unchecked item has current candidate-scoped evidence. Historical or synthetic evidence cannot substitute for current-candidate verification.

**Current state:** `P8 OPEN / FAIL-CLOSED`; P9 has a scoped PASS on completion candidate `562753b…`, while broader P9 closure remains open; no new freeze; no authorization; empirical N = 0.
