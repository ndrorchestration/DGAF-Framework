# Protected main — remaining admin readback

Status: **PARTIAL READBACK / FULL PREVENTIVE ENFORCEMENT NOT VERIFIED**
Controller: issue #277. Scientific-state effect: NONE.

## Fresh connected evidence

At main `c147df1ac226b641e5a85cd08fb45e9a838ac825`, the branch API reports
`protected=true` and required contexts `PPTL CI`, `Governance CI`, and
`PR Issue-State Keyword Guard`, each tied to app ID 15368, with enforcement
level `everyone`.

Active ruleset `Main` (16909314) targets the default branch and exposes
`deletion` and `non_fast_forward` rules, no bypass actors, and
`current_user_can_bypass=never`.

The detailed branch-protection API returns HTTP 403, `Resource not accessible
by integration`. The connected GitHub tools expose no protection mutation.
Consequently the full effective review requirements, PR-only enforcement,
admin/bypass semantics, and strict status-check policy remain NOT VERIFIED.
A partial ruleset is not evidence that legacy protection is absent.

## Minimal operator readback

Open the repository Settings > Branches and Settings > Rules > Rulesets
using the owner's authenticated browser. Inspect the effective rules for main.
Retain a non-secret export or screenshots showing:

1. pull requests are required before merging;
2. required status checks and whether the branch must be up to date;
3. review count, stale-review dismissal, and last-push approval policy;
4. admin/enforcement and every bypass list across both protection mechanisms;
5. force-push and deletion prevention, plus effective merge-method policy.

Do not add a review-count requirement that a solo owner cannot satisfy without
first arranging an actual eligible reviewer. Preserve the small working
required-context set; do not restore the historical 68-context deadlock.
If a setting is missing, prepare the intended change and review its effect on
this solo workflow before saving. Read back again after any change.

For owners already using authenticated GitHub CLI, a read-only export is:

```bash
gh api repos/ndrorchestration/DGAF-Framework/branches/main/protection
gh api repos/ndrorchestration/DGAF-Framework/rulesets/16909314
```

Do not supply tokens in chat or perform a direct-write test against main.
Issue #277 remains open until the complete accepted readback establishes its
predicates. Green CI and successful PR merges do not close this admin gate.
