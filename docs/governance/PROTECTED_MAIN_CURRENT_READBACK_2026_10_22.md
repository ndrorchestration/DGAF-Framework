# Protected main current enforcement readback — 2026-10-22

**Repository:** `ndrorchestration/DGAF-Framework`  
**Target branch:** `main`  
**Source baseline at reconciliation:** `1a95b94332dffb404c5a3ce026d70781a8c10b90`  
**Evidence class:** OWNER_OPERATOR_ADMIN_METADATA_READBACK / SAME_SYSTEM_NONINDEPENDENT  
**Independent acceptance:** NOT ESTABLISHED

## Purpose

Record the current repository-administration state after the 2026-10-22
release-hardening changes without rewriting earlier dated policy snapshots.
This record describes repository settings, not source-code acceptance,
scientific validation, or release authorization.

## Pull-request and history protection

Authenticated administration readback reports:

- protected branch: `main`;
- required approving reviews: **1**;
- approval of the most recent push by someone other than that pusher: **required**;
- stale approvals: **dismissed after new changes**;
- signed commits: **required**;
- administrator enforcement: **enabled**;
- linear history: **required**;
- force pushes: **disabled**;
- branch deletion: **disabled**.

The repository currently has only the owner account enumerated as a collaborator.
Therefore the approval requirement mechanically prevents owner-only normal
admission until another eligible reviewer is added. One GitHub approval does
not by itself establish Gate 0 reviewer independence or conflict-of-interest
eligibility.

## Strict required status contexts

The current protected-main strict required contexts are:

1. `PPTL CI`
2. `Governance CI`
3. `PR Issue-State Keyword Guard`
4. `security-scan`
5. `test (3.10)`
6. `test (3.11)`
7. `test (3.12)`

The last four are job-level contexts emitted by the
`Python Tests & Quality Checks` workflow. The workflow also emits sibling jobs
such as `staging-evidence`, `integration-tests`, and aggregate workflow state;
those are not globally required merely because they share the workflow.

The Python workflow is configured for every pull request targeting
`main` or `develop`, including documentation-only changes. At this readback,
the current `certifi 2026.7.22 / PYSEC-2026-4320` finding causes
`security-scan` to fail on unremediated heads and therefore acts as a
mechanical protected-main merge blocker.

## Deployment environments

GitHub environment metadata after hardening reports:

- `Production`: deployments restricted to protected branches;
- `Preview`: deployments restricted to protected branches;
- custom deployment branch policies: disabled;
- administrator bypass remains available;
- eligible required environment reviewers: not configured.

Source-level deployment hardening remains separately proposed in draft PR #1428.
Environment metadata does not substitute for source review or eligible reviewer
approval.

## Historical records preserved

This current readback does not revise event-time records including:

- `docs/governance/PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1.json`
  (recorded 2026-09-08);
- dated files under `docs/status/`;
- historical `CHANGELOG.md` entries.

Statements in those records remain attributable to their recorded dates and
must not be interpreted as current settings.

## Claim boundary

This record supports only the proposition that the listed repository settings
were observed through authenticated administrative metadata on 2026-10-22.
It does not establish that:

- every required check is sufficient for release;
- any reviewer is independently eligible;
- administrator bypass is eliminated;
- Production or Preview has independently approved required reviewers;
- DGAF v1 is releasable;
- scientific efficacy, independent validation, or High Assurance is established.

Current release state remains `DGAF_V1_RELEASE=HOLD`.
