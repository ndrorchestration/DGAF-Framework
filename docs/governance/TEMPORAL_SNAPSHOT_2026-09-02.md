# Temporal Snapshot — 2026-09-02

This snapshot is the current cross-layer reconciliation point. It does not rewrite historical records and does not transfer candidate-scoped evidence.

## Current identity boundary

- Documentation/control-plane main: `275756fd81c975f17ae3d16d24e599db0617cf85`
- Active experimental candidate: PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`
- Candidate tree: `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`
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
| Runtime/deployment | UNRESOLVED for PR #192 | No exact-candidate Vercel deployment is currently evidenced; provider is rate-limited. |

## Current candidate CI boundary

The September 2 PR #192 workflow wave established a complete successful CI wave on the exact candidate head `58ba9a…`:

- Pre-Authorization Security: PASS (`33616403843`).
- Pre-Freeze Runner Validation: PASS (`33616403754`).
- Governance CI: PASS (`33616403706`).
- Documentation, claim-hygiene, truth-layer, authority, PDMAL harness/instrumentation, regression, coverage, and deterministic checks: PASS.

The prior failures on `edd3b5c…` were resolved by incorporating the reviewed clean P-35 test-caller and TLA+ digest corrections directly into `58ba9a…`.

## Current exact-candidate evidence

- Pre-freeze runner artifact: `9841238710`.
- Governance evaluation evidence artifact: `9841231335`.
- Governance freeze-control evidence artifact: `9841228966`.
- Instrumentation dry-run artifact: `9841100424`.

The freeze-control artifact explicitly targets `58ba9a…`, records authorization `NOT_GRANTED`, freeze `NOT_CREATED`, and empirical N `0`, and retains verifier/toolchain/environment fingerprints. The workflow payload may also record GitHub's pull-request merge-ref commit; that execution identity is retained separately and is not substituted for the candidate head.

## Remediation and support records

Clean support PRs #197 and #198 were reviewed for the two prior candidate-CI blockers. Their reviewed diffs were incorporated directly into the selected candidate as `58ba9a…`; neither support branch confers experimental authority.

## Historical integrity rule

References to `92ff830b…`, `a43219b…`, `562753b…`, prior P-35 remediation heads, and their associated deployments/runs remain valid only within their historical scopes. They must not be rewritten as though they were the September 2 active candidate and must not be used to satisfy current-candidate predicates.

## Non-authorizing boundary

This snapshot changes no experimental gate, creates no freeze, grants no authorization, and establishes no empirical result. The remaining closure path is deployment-bound P2/P6a, full P3–P6 operational closure, exact P7 binding, P8, fresh final-candidate P9, immutable freeze, and explicit authorization before any empirical execution.
