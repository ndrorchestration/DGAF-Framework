# Temporal Snapshot — 2026-09-02

This snapshot is the current cross-layer reconciliation point. It does not rewrite historical records and does not transfer candidate-scoped evidence.

## Current identity boundary

- Documentation/control-plane main: `275756fd81c975f17ae3d16d24e599db0617cf85`
- Active experimental candidate: PR #192 / `edd3b5c8266e2680b9bb94301c2623a3f1ac0cf0`
- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- State: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

## Temporal classification

| Layer | State | Rule |
|---|---|---|
| README/current-state surfaces | CURRENT | Must identify the present control-plane and candidate boundary or explicitly label historical identities. |
| Candidate manifests/evidence | CANDIDATE | Exact SHA/tree/run/deployment scoped; no evidence transfer across material changes. |
| Timeline/progress pages | HISTORICAL + CURRENT OVERLAY | Preserve original chronology and measurements; append or prepend dated reconciliations. |
| Gate evidence | CANDIDATE / HISTORICAL | A passing result remains scoped to its producing identity. |
| Taxonomy/pattern registry | CURRENT | Semantic reconciliation does not redefine experimental identity. |
| Architecture snapshots | HISTORICAL unless explicitly updated | Older PR numbers and designs remain historical records. |
| Runtime/deployment | UNRESOLVED for PR #192 | No exact-candidate Vercel deployment is currently evidenced. |

## Current candidate CI boundary

The September 2 PR #192 workflow wave established:

- Pre-Authorization Security: PASS.
- Documentation, claim-hygiene, truth-layer, authority, PDMAL harness/instrumentation, and related deterministic checks: PASS.
- Pre-Freeze Runner Validation: FAIL because four legacy direct test callers do not provide the now-required explicit P-35 checker. This is a test-contract synchronization defect; the production fail-closed requirement remains intact.
- Governance CI: FAIL at the pinned TLA+ Tools v1.8.0 digest check. The official v1.8.0 release asset reports SHA-256 `dbcc75552f21978a4846688b8e23be1a6b6c0b3fcee35d78fec2df167958ec94`; the workflow was still pinned to an older digest.

## Remediation tracks

- Test-contract synchronization is isolated on `fix/2026-09-02-p35-test-callers` and does not mutate PR #192.
- TLA+ release-pin correction is isolated on `fix/2026-09-02-tlaplus-v180-digest` and does not mutate PR #192.
- These support branches remain non-authorizing until their own CI passes and their changes are explicitly incorporated into a future candidate lineage.

## Historical integrity rule

References to `92ff830b…`, `a43219b…`, `562753b…`, prior P-35 remediation heads, and their associated deployments/runs remain valid only within their historical scopes. They must not be rewritten as though they were the September 2 active candidate and must not be used to satisfy PR #192 predicates.
