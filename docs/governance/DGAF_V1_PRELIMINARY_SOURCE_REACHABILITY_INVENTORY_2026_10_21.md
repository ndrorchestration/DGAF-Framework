# DGAF v1 — preliminary source-bound reachability inventory

**Classification:** OPERATOR-LOCAL / PRE-GATE-0 / NOT ACCEPTED.
**Source:** protected main `1a95b94332dffb404c5a3ce026d70781a8c10b90`.
**Controller:** <https://github.com/ndrorchestration/DGAF-Framework/issues/1421>

## Inspected existing paths

| Source path | Observed source semantics | Provisional disposition | Missing evidence |
| --- | --- | --- | --- |
| `pages/api/audit.ts` | POST calls `validateAuditAdmission`, denies invalid request with HTTP 403, and calls `consumeAuditAdmission(record.record_id)` before an effect | Candidate limited action path, not generalized authorization | Deployment authentication, cross-instance replay, revocation failure injection and reachability audit |
| `app/lib/action-admission.ts` | `usedRecordIds = new Set<string>()`; `replay_class: PROCESS_LOCAL`; `trust_anchor_class: SERVER_HMAC_ENV` | Explicitly exclude durable replay and independent issuer trust claims | Atomic durable consume, admitted external issuer, key lifecycle |
| `.github/workflows/pdmal-instrumentation-dry-run.yml` | Push/PR triggers; `PDMAL_BLINDING_KEY`; two `actions/upload-artifact` uses | Candidate P0 publication path | Independently accepted #1414 default-deny or verified disabling/route removal, negative controls for alternate publication paths |
| `actions/governed-repo/action.yml`; `components/governed_repo.py` | On protected-main file list: published source surfaces present | Candidate packaging/controlled GitHub action | Independent environment, packaging, action effects and outside-operator evidence |
| `packages/governed-repo/src/governed_repo/core.py` and `github_adapter.py` | Package source present on protected main | Candidate distribution subset | API compatibility, actor permissions, signed build and clean-install reproduction |

## Important status distinctions

- Current main contains source paths above; path presence alone never proves a route is externally reachable or unreachable.
- `/api/audit` has explicit denial branches, but negative source inspection does **not** establish all potential fallback-to-allow paths absent.
- #1414 is an **unmerged** publication guard; do not infer protected main has the candidate guard.
- #1416 operation matrix is design-only and not the v1 production issuer.
- #756 durable replay, #757 commit-time revocation and #770 provider admission remain separate future implementation/release decisions.
- No PDMAL key, historical protected artifact, live endpoint mutation or deployment credentials inspected here.
- Gate 0 is proposed and not frozen; this inventory cannot backfill gate acceptance.

## Next source-bound audit criteria

1. Identify all executable action entry points by exact path and action class, including GitHub workflow triggers and alternate dispatch mechanisms.
2. For each class: define protected effect, authority source, denial oracles, failure modes, dependency unavailability, and what class can be hard-disabled.
3. Enumerate upload and other data-egress routes, distinguishing dry-run structural outputs from protected scientific data; do not claim global containment from #1414 alone.
4. Bind raw test logs, independent verifier identity, clean reproduction, residual risks and exact release candidate SHA before any PASS.
5. Hold classification until preregistration and eligible independent blocker adjudication.

**Status:** GATE_0=PROPOSED; G1..G7=BLOCKED; DGAF_V1_RELEASE=HOLD; SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.
