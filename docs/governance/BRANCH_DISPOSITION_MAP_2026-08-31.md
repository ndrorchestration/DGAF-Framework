# Branch Disposition & Lineage Map — 2026-08-31

**Purpose:** classify surviving branches by authority, candidate epoch, PR lineage, duplication risk, and safe operational disposition without deleting or rewriting historical provenance.

## Authority rule

Branch names and passing checks do not confer experimental authority. The current control-plane authority is `main`; the corrected experimental apparatus boundary is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` with tree `973c9233…`. Current `main` tip `c00ff8f27374a402a2cdb942ba74c50e8c094afc` is later than the apparatus boundary because subsequent commits are control-plane/documentation corrections. Any branch or artifact outside the current candidate lineage is non-authoritative unless explicitly rebound and verified.

## Disposition vocabulary

- **KEEP-CURRENT:** current authoritative trunk or required current work.
- **KEEP-HISTORICAL:** preserve for provenance/evidence lineage.
- **KEEP-ACTIVE:** active engineering/research work with a current PR or clearly documented continuation.
- **SUPERSEDED:** historical remediation whose role is already represented by later merged lineage.
- **DUPLICATE-SHA:** multiple branch names point to the same commit; retain provenance but collapse operational references to one preferred name.
- **REVIEW:** requires branch-to-PR/ancestor review before any cleanup.
- **DELETE-CANDIDATE:** only after confirming no unique provenance, commits, or references remain. This map does not authorize deletion.

## Canonical current trunk

| Branch | Tip | Class | Notes |
|---|---|---|---|
| `main` | `c00ff8f27374a402a2cdb942ba74c50e8c094afc` | KEEP-CURRENT | Protected branch; current control-plane authority. Required check: `PPTL CI`. |

## Seven-gate restoration / provenance lineage

| Branch / PR | Tip | Disposition | Relationship |
|---|---|---|---|
| `experimental-candidate/restore-all-gates-2026-08-31` / #168 | `de7ad83701c4fcc1052bb31d0a2818e59404414f` | KEEP-HISTORICAL | Seven-gate restoration substrate; later provenance-integrity correction superseded its candidate status. |
| `fix/integrate-p162-provenance-after-restore` / #169, #170 lineage | `9123dc4a2b5b9859e3cf0ebde4d18202ba6b01d7` | KEEP-HISTORICAL | Consolidation/integration lineage; #170 merged. |
| `fix/seven-gate-provenance-binding` / #171/#172 lineage | `3c489459e09d2d9fb9d31239d9bae05df4b3548b` / `e0a653cc30d7fcee193415448d79c84a71b48d21` | SUPERSEDED | Same provenance defect addressed through successive draft/non-draft correction, ultimately replaced by rebased #174. |
| `fix/seven-gate-provenance-binding-rebased` / #174 | `4e345c038dc9838065e2927b1b67c1f6ff7d5f4c` | KEEP-HISTORICAL / MERGED | Authoritative correction lineage that produced the current apparatus boundary `2a54a67d…`. |
| `experimental-candidate/restore-p31-p33-2026-08-30` / #160 | `81e71b402af4dcc8060a8de70c79b07d66792d63` | KEEP-HISTORICAL | P31/P33 restoration predecessor; later seven-gate lineage superseded it. |

## Earlier candidate epochs

| Branch family | Disposition | Reason |
|---|---|---|
| `candidate/p7-binding-reconciliation-clean-20260828` | SUPERSEDED | Pre-restoration candidate reconciliation; obsolete after later apparatus identity changes. |
| `candidate/p7-binding-remediation-20260828` | SUPERSEDED | Same pre-restoration candidate epoch; do not use for current dispatch. |
| `experimental-candidate/2026-08-30-post151` | SUPERSEDED | Post-#151 predecessor; replaced by later restoration/provenance lineage. |
| `experimental-candidate/2026-08-30-reconciled` | SUPERSEDED | Reconciliation predecessor; replaced by #174 lineage. |
| `verification/p2-candidate-83e1678f` | KEEP-HISTORICAL | Old exact-candidate verification track; evidence does not transfer to current apparatus. |
| `verify/e2b-current-candidate-20260828` | KEEP-HISTORICAL | Prior verifier/evidence boundary; candidate-specific and non-transferable. |

## Current documentation / governance branches

| Branch | Disposition | Notes |
|---|---|---|
| `docs/reconcile-2026-08-31-drift` | KEEP-HISTORICAL / REVIEW | Reconciliation snapshot; useful provenance, not current authority. |
| `docs/dependency-hygiene-20260830` | DUPLICATE-SHA | Tip `103a40779954bb79f869413cc994de2636941b7f`. |
| `docs/dependency-hygiene-audit-20260830` | DUPLICATE-SHA | Same tip as above. |
| `docs/dependency-hygiene-audit-final-20260830` | DUPLICATE-SHA | Same tip as above. |
| `docs/dependency-hygiene-audit-final3-20260830` | DUPLICATE-SHA | Same tip as above. |
| `docs/dependency-hygiene-report-20260830` | DUPLICATE-SHA | Same tip as above. |
| `docs/dependency-hygiene-report-20260830b` | DUPLICATE-SHA | Same tip as above. |
| `docs/dependency-hygiene-audit-final2-20260830` | REVIEW | Distinct tip `cb0fe3c6589cbefc15f8a36fd3eb8bebe3540341`; determine whether unique content remains referenced. |
| `docs/current-state-hygiene-20260824` | KEEP-HISTORICAL | Historical reconciliation method. |
| `docs/p8-corrected-candidate-basis` | KEEP-HISTORICAL | Prior P8 candidate epoch; not current. |
| `docs/p42-current-main-reconciliation` | KEEP-HISTORICAL | Historical P42 reconciliation. |
| `docs/reconcile-p42-human-registry` | KEEP-HISTORICAL | Earlier P42 reconciliation. |
| `docs/publication-provenance-spine` | KEEP-HISTORICAL | Publication/provenance architecture predecessor. |
| `docs/governance-architecture-audit` | KEEP-HISTORICAL | Audit artifact; not apparatus authority. |
| `docs/forward-plan` | KEEP-HISTORICAL | Planning artifact. |
| `docs/readme-public-surface-20260829` / #140 | KEEP-ACTIVE | Documentation/public-surface scope, not experimental apparatus. |

## Engineering / security / verification branches

| Branch family | Disposition | Notes |
|---|---|---|
| `fix/f1-f3-apparatus-remediation-20260830` / #151 | KEEP-HISTORICAL | Merged remediation establishing predecessor apparatus boundary. |
| `fix/preflight-restoration-failure-modes` / #167 | SUPERSEDED | Preflight lineage absorbed by later restoration/provenance path. |
| `engineering/pdmal-tgl-integrity-20260828` / #131 | KEEP-HISTORICAL | Full-SHA TGL provenance correction. |
| `engineering/tgl-skip-semantics-20260829` / #132 | SUPERSEDED | Superseded by current-main TGL contract repair lineage. |
| `engineering/tgl-hpg-regression-20260828` / #130 | SUPERSEDED | Regression predecessor. |
| `engineering/tgl-p8-p6a-20260828` / #129 | SUPERSEDED | Verification predecessor. |
| `fix/tgl-contract-repair-132` / #133 | SUPERSEDED | Draft predecessor to #134/#148 lineage. |
| `fix/tgl-contract-repair-main-20260829` / #134 | SUPERSEDED | Current-main TGL remediation predecessor. |
| `fix/tgl-contract-repair-mainline-20260830` / #148 | KEEP-HISTORICAL | Merged governance-contract correction lineage. |
| `fix/tgl-orchestrator-contract-20260827` / #114 | KEEP-HISTORICAL | Runtime/test compatibility correction. |
| `security/codeql-workflow-permissions` / #111 | KEEP-HISTORICAL | Merged CI security hardening. |
| `fix/governance-ci-networkx` / #88 | KEEP-HISTORICAL | Merged CI dependency correction. |
| `fix/tzdata-require-hashes` / #98 | KEEP-HISTORICAL | Merged locked-dependency correction. |
| `fix/pytest-pin-conflict` / #94 | KEEP-HISTORICAL | Merged dependency correction. |
| `e2b-verifier-lock-20260827` / #115 | KEEP-HISTORICAL | Verifier-policy lock lineage; non-authorizing. |
| `governance/e2b-m6-hardening` / #107 | SUPERSEDED | Replaced by later E2b hardening lineage. |
| `governance/e2b-m6-hardening-v2` / #108 | KEEP-HISTORICAL | Merged freeze-admissibility control lineage. |
| `governance/e2b-m6-exact-tree-provenance` / #116 | KEEP-HISTORICAL | Exact-tree verifier provenance correction. |

## P7 / P8 / evaluation branches

| Branch | Disposition | Notes |
|---|---|---|
| `governance/p7-completion-adjudication` / #81 | KEEP-HISTORICAL | Scientific adjudication draft; P7 remains formally open. |
| `p7/adjudication-hardening-2026-08-23` / #83 | KEEP-HISTORICAL | Refined panel-ready P7 record. |
| `governance/proposed-gate-designations-20260831` / #164 | KEEP-HISTORICAL | Proposal-only; no normative authority by itself. |
| `feat/dgaf-eval-suite-issue-32` | KEEP-ACTIVE / REVIEW | Evaluation track; separate from PDMAL efficacy. |
| `feat/dgaf-v1-control-plane-finalize-20260829` / #139 | KEEP-HISTORICAL | Merged control-plane integration lineage. |
| `feat/epistemic-evidence-architecture-v1` / #87 | KEEP-HISTORICAL | Evidence architecture predecessor. |
| `feat/openai-dgaf-evaluator` / #76 | KEEP-HISTORICAL | Evaluator implementation; separate evidence boundary. |

## Additional branches requiring explicit review

The live branch inventory contains additional refs not yet assigned to a finalized lineage class above. They are intentionally **REVIEW**, not assumed current or historical, until PR/ancestor/reference inspection is complete:

| Branch | Preliminary class | Review target |
|---|---|---|
| `audit/complete-historical-gate-recovery-2026-08-30` | REVIEW | Confirm relationship to #161 and later restoration lineage. |
| `alert-autofix-38` | REVIEW | Determine whether generated/security-only and superseded. |
| `alert-autofix-49` | REVIEW | Determine whether generated/security-only and superseded. |
| `chore/preauth-completeness-2026-08-20` | REVIEW | Map to pre-authorization control lineage. |
| `chore/repository-structure-normalization` | REVIEW | Map to structural cleanup lineage and current references. |
| `ci/pytest-diagnostics` | REVIEW | Determine whether obsolete diagnostic tooling remains referenced. |
| `docs/dgaf-v1-control-plane-integration-20260829` | REVIEW | Compare with merged #139/control-plane integration. |
| `docs/fix-control-record-stale-gate-wording` | REVIEW | Verify whether superseded by later wording corrections. |
| `docs/fix-current-state-phrasing` | REVIEW | Verify whether superseded by current-state reconciliation. |
| `docs/fix-post-merge-main-sha` | REVIEW | Compare against current main-SHA corrections. |
| `docs/lint-md040-md036-20260830` | REVIEW | Map against current markdownlint debt/remediation. |
| `epistemic/pdmal-freeze-readiness-reconciliation` | REVIEW | Map to freeze-readiness lineage; verify non-authority. |
| `feat/kappa-v3.6-governance-classifier` | REVIEW | Research/implementation branch; verify whether it changes candidate semantics. |
| `feat/phi-calculus-whitepaper` | REVIEW | Research/publication branch; no experimental authority by default. |
| `feature/amethyst-expert-panel-consensus` | REVIEW | Panel/evidence branch; map to P7 adjudication lineage. |
| `fix/authority-matrix-historical-alias-test-20260830` | REVIEW | Likely governance invariant test; confirm whether merged elsewhere. |
| `fix/claim-hygiene-self-scan` | REVIEW | Claim-audit tooling; determine active lineage. |
| `fix/orchestration-firewall-test-contract` | REVIEW | Runtime/security test contract; determine whether merged/superseded. |
| `fix/p7-status-consistency` | REVIEW | P7 status-control remediation; map to current P7 record. |
| `noop-temporary-check` | REVIEW | Determine whether intentionally retained for required-check compatibility. |
| `rebuild/pr42-stasis-doc` | REVIEW | P42 historical/rebuild lineage. |
| `rebuild/pr74-pip-lockfiles` | REVIEW | Dependency rebuild lineage. |
| `rebuild/pr85-publication-spine` | REVIEW | Publication/provenance rebuild lineage. |
| `reconcile/pr139-with-main-20260830` | REVIEW | Reconciliation predecessor/descendant of #139. |
| `recovery/p31-p33-contract-evidence-2026-08-30` | REVIEW | P31/P33 evidence recovery lineage. |
| `review/pr139-ready-20260830` | REVIEW | Review/readiness snapshot around #139. |
| `stasis-cluster1-enumeration` | REVIEW | Stasis/historical enumeration track. |
| `tools/hermes-review-agents-20260830` | REVIEW | Tooling/review-only branch. |

These branches are **not counted as additional candidates**. Their review status is a guard against false completeness in this map.

## Patch and legacy branches

`ndrorchestration-patch-1` through `ndrorchestration-patch-22` are historical June maintenance branches. Several correspond to merged PRs (#17–#31). Classify as **KEEP-HISTORICAL** until a reference scan proves they are not needed for provenance; deletion is not authorized by this map.

## Strong duplicate group

### Exact SHA alias group

The following branches all point to `103a40779954bb79f869413cc994de2636941b7f`:

- `docs/dependency-hygiene-20260830`
- `docs/dependency-hygiene-audit-20260830`
- `docs/dependency-hygiene-audit-final-20260830`
- `docs/dependency-hygiene-audit-final3-20260830`
- `docs/dependency-hygiene-report-20260830`
- `docs/dependency-hygiene-report-20260830b`

**Operational recommendation:** select one preferred alias for current references; retain the others until a repository-reference scan establishes they are safe to delete.

## Candidate and authority invariants

1. `main` tip ≠ apparatus source ≠ candidate identity ≠ deployment identity.
2. A branch containing `candidate` in its name is not authoritative by naming alone.
3. Historical evidence remains valid provenance but cannot satisfy current candidate predicates without an explicit candidate-bound relationship.
4. Merged PR metadata does not by itself create a freeze or authorization transition.
5. A documentation-only descendant of `main` does not redefine the apparatus unless executable semantics change.
6. Any executable apparatus change after the current boundary requires a new candidate epoch and fresh verification.
7. Branch cleanup must never delete the only retained copy of unique historical evidence.

## Current experimental boundary

### Experimental state

PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

## Source basis

This map was created from the live GitHub branch inventory and PR metadata checked on 2026-08-31. It is a classification artifact, not a deletion authorization. The full inventory includes a residual-review section so that unmapped branches cannot be mistaken for absent branches. Where complete ancestry/reference inspection was not available, the disposition is intentionally conservative (`REVIEW` or `KEEP-HISTORICAL`).
