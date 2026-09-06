# Pull-request issue-state transition policy

## Status

Status: **ACTIVE GOVERNANCE POLICY / PRE-MERGE SYNTAX CONTROL / NOT REPOSITORY-ADMIN PREVENTIVE ENFORCEMENT**

DGAF treats issue state as governance data. A pull-request description must not accidentally mutate a high-stakes issue merely because GitHub recognizes state-transition syntax.

This policy was introduced after a 2026-09-06 incident in which PR #340 merged a documentation-only review scaffold and GitHub automatically marked Issue #310 completed even though the PR text intended the opposite and the issue's acceptance contract remained unmet. The issue was reopened and the state drift was logged.

## Rule

Pull requests targeting `main` must not contain a GitHub issue-closing keyword immediately paired with an issue reference.

The prohibited state-transition keyword families are GitHub's documented close, fix, and resolve families, including their supported inflections. The guard applies even when ordinary-language context is negative, hypothetical, quoted, or explanatory. Parser semantics take precedence over author intent.

The guard recognizes these issue-reference shapes:

- local issue references such as `#123`;
- cross-repository references such as `owner/repository#123`;
- full GitHub issue URLs.

## Safe reference style

Use neutral references that cannot express an automatic issue-state transition, for example:

- `Related: #123`
- `Issue #123 remains OPEN`
- `No issue-state change for #123`

Issue closure or reopening must be a separate explicit governance action after the relevant acceptance criteria have been checked against exact evidence.

## Automated control

`scripts/check_pr_closure_keywords.py` scans the PR body and exits nonzero when dangerous syntax is present.

`.github/workflows/pr-issue-closure-keyword-guard.yml` runs the parser and its deterministic negative controls on PR events targeting `main`, including PR-body edits.

The workflow is deliberately fail closed for malformed event input. It reports the matched line and issue reference but performs no issue mutation.

## Threat model and limitations

This control addresses accidental PR-body issue-state transitions. It does not establish all possible GitHub issue-state protections and does not replace repository administration.

Known boundaries:

- commit-message issue-closing semantics are outside the initial parser scope;
- a user with sufficient GitHub permissions may still change issue state directly;
- branch/ruleset configuration currently does not establish this workflow as a required protected-main check;
- therefore this workflow is a pre-merge/detective compensating control until repository-admin readback proves otherwise;
- Issue #277 remains the authority for preventive protected-main enforcement.

## Acceptance evidence for this control

Before this policy is treated as integrated:

1. deterministic tests must demonstrate rejection of negated and affirmative closing-keyword syntax;
2. neutral issue-reference forms must pass;
3. the workflow must execute on the exact PR head;
4. all repository exact-head checks must pass before merge;
5. post-merge issue-state readback must confirm no tracked governance issue changed state by side effect;
6. the Main Push Provenance Audit should accept the resulting main update as PR-mediated.

## Non-effects

This policy does not establish P4 custody, independent security review, production R/A/C authority, real Confidential Space execution, final continuity acceptance, final-candidate designation, freeze, authorization, unblinding, or empirical execution.

**#277 OPEN · #310 OPEN · #316 OPEN · #320 OPEN · #295 OPEN · final v0.7.6 candidate NOT DESIGNATED · P4 OPEN / FAIL-CLOSED · PRE-FREEZE · NOT AUTHORIZED · empirical N=0.**
