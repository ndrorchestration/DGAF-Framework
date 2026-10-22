# Gate 0 boundary review — October 21, 2026 (America/New_York)

Status: preliminary source/settings evidence, not frozen criteria or gate acceptance.
Baseline: `1a95b94332dffb404c5a3ce026d70781a8c10b90`; remote main rechecked on neontic.
Tracking: [Gate 0 issue #1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421)

## Reproduction and coverage

Run `python docs/GOVERNANCE/gate0-boundary-review/inventory.py` with Python 3.12 and PyYAML 6.0.3. The script reads immutable Git objects, never imports or executes audited code, and retains source hashes. It inventories 144 workflows, 55 upload jobs, 68 upload steps and 10 API source files. Zero YAML parse errors. See source_inventory.json and its SHA-256 sidecar for every upload path, declared permission, condition, checkout, retention and secret-reference name. Values of secrets are not collected.

This is complete enumeration of direct upload-artifact steps in the selected workflow files, NOT complete semantic review of every producer, transitive egress path, actual artifact payload or recipient ACL. Every job remains CONTENT_AND_RECIPIENT_ADMISSION_NOT_ESTABLISHED. No scientific outcomes or artifact archives were accessed.

The prior retained report hash was recomputed successfully:
`d18a16a7e45a609bf116d07617c93f385627f3a59d2e2328efca32f813a6c2ca`.
Its API loop covered pages/api/*.ts only. The corrected inventory also includes api/ahg_herald.py. Two command-pattern matches were never an exhaustive publisher count.

## Evidence register

| ID | Classification | Finding and limitation | Proposed next control / oracle |
|---|---|---|---|
| B01 | VERIFIED source | deploy.yml permits workflow_dispatch without a main-ref guard. The classifier returns BUILD when the base is unavailable. No job environment is bound. | Deny non-main dispatch before credentials; bind reviewed production environment. Test main/branch/tag/manual/missing context. |
| B02 | VERIFIED source | Production environment variables are changed before deploy and identity/runtime tests. cancel-in-progress is true. No rollback transaction is shown. | Serialize production changes; separately design and test configuration/deployment recovery. Post-deploy PASS is not pre-deploy authorization. |
| B03 | VERIFIED source | Preview job checks out PR head and has job-wide Vercel token and bypass secret. No explicit trusted-source approval or protected environment. | Separate unprivileged PR checks from explicitly authorized deployment; credentials scoped to necessary steps; reviewed preview project and environment. |
| B04 | VERIFIED settings | Production and Preview environment protection_rules are empty; deployment_branch_policy is null. | Establish eligible reviewers and branch policy before binding jobs. Merely naming an environment adds no protection. |
| B05 | VERIFIED settings | Main requires PPTL CI, Governance CI and PR Issue-State Keyword Guard; required approving review count is 0. Main ruleset only prevents deletion/non-fast-forward, no bypass actors. | Independent approval requirement is not enforced by these settings. Freeze eligibility before configuring approval policy; do not self-admit. |
| B06 | VERIFIED source | PDMAL dry-run validates schema/checksum before upload but has no separate publication-eligibility gate. | Continue existing #1399/#1414 lane; verify denied publication and no fallback before admission. Do not create competing remediation. |
| B07 | VERIFIED source | Three historical solo/canonical execution workflows generate keys and upload key files separately from datasets. Branch-specific push and one-file run-request checks exist; source labels same-system custody. | Explicitly adjudicate same-system custody, recipient access and v1 exclusion reachability. Separate artifacts are not independent custody. No key was downloaded. |
| B08 | VERIFIED source | p4-mode-t-rekor-timing.yml invokes helper-driven public Rekor submission with id-token: write. Manual confirmation, exact-head binding and first-attempt checks exist. | Include in egress inventory; retain explicit irreversible-side-effect approval and synthetic-only tests. Do not execute for this audit. |
| B09 | VERIFIED source / UNKNOWN runtime | api/ahg_herald.py logs records and optionally writes KV/posts webhook. Missing key is denied only when VERCEL_ENV equals production. Preview without key is allowed by source. | Establish deployed reachability and preview configuration. Test missing/malformed environment and key with mocked network; no live webhook calls. |
| B10 | VERIFIED source | mandate.ts unconditionally returns 410 with state_change DISABLED. sweep.ts plans remediations and returns mutation_performed false. | Earlier mutation text matches are not evidence of mutation. Sweep helper transitive behavior and deployment remain separate checks. |

## Existing candidate and negative evidence

PR #1414 remained OPEN/DRAFT at `a09781ee923aa9d5988302854a43889a51ba68bd` when inspected.
Two pdmal-dry-run failures were observed: runs 39242673061 and 39242784549. They were not rerun, relabeled or assumed intentional. Other successful checks do not close the publication issue.

The default Python 3.14 and installed Python 3.12 lacked PyYAML. A task-scoped dependency directory was used with PyYAML 6.0.3; no project dependency files or global packages were modified. PowerShell Get-FileHash was unavailable; Python hashlib successfully verified the retained report.

## Concrete remediation proposal

deployment-boundaries.patch is an unapplied review candidate, not a tested/admitted fix. It:

- adds a main-ref restriction to production deployment;
- stops cancellation of an in-progress production deployment;
- binds production/preview jobs to their corresponding environments;
- changes credentialed preview execution to manual-only and restricts its job to main.

This intentionally removes automatic credentialed PR-preview deployment and therefore changes the staging evidence workflow contract. It must not be applied without reviewing that contract and updating its tests. The existing environments have no reviewer restrictions, so the patch alone is insufficient. It does not solve provider-token scope, step-level secret exposure, configuration rollback, raw metadata minimization or all publication controls. A separate reviewed design is required for authorized arbitrary-candidate previews.

## Completion boundary

Completed: immutable source inventory; all direct upload declarations enumerated; GitHub settings readback; priority trust-boundary source review; original report digest verification; reviewable remediation proposal.
Remaining: transitive producer/recipient/content verification for 55 jobs; all route fault tests; Vercel project/token/routing evidence; independent G0 adjudication; all G1–G7 sign-offs. No claim of all security work complete.

G0=PROPOSED_NOT_FROZEN; G1..G7=BLOCKED_NOT_INDEPENDENTLY_CONFIRMED; DGAF_V1_RELEASE=HOLD.
SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED;
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.

## Provider metadata follow-up

Vercel connector readback identifies production deployment `dpl_6JkzUxhJnMrH9bn6f324P92PrSco` as READY, source cli, with `meta.githubCommitSha` equal to the audited baseline. This is provider-reported source metadata, not an independent build provenance attestation or route-execution test. Project SSO protection is enabled for `all_except_custom_domains`; password and trusted-IP protection are disabled. See vercel_metadata.json. The production source-identity metadata gap is narrowed; route reachability and credential scope remain unknown.

## Validation receipt

Candidate workflow texts parse with PyYAML 6.0.3 and the unapplied patch passes `git apply --check`. Inventory rerun is byte-identical; all 55 job identities are unique; the 68-step sum and Python API inclusion were checked. These checks do not establish runtime behavior of the proposed deployment changes.

## First hosted verification findings

At initial head 82fce3b, PR-scope Markdown lint found a bare link and missing blank line; changed-Python checks found formatting violations in inventory.py. These author-introduced issues were corrected in the follow-up commit. Original failed runs remain retained: 39714247448 and 39714247455. The same Python workflow also reported certifi 2026.7.22 / PYSEC-2026-4320, with fix version 2026.10.19; this dependency finding is not fixed by this documentation-only PR. GitHub Dependabot separately reports open high alerts 46 (source-map-js) and 47 (sharp). These are reported scanner findings requiring dependency/reachability review, not proof of exploitation.
