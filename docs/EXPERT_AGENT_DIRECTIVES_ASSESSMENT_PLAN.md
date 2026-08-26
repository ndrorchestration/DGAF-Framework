# Expert Agent Directives – Assessment & Implementation Plan

## Overall Agreement

The directives are correct and well-considered. I concur with the version target, the preservation of the project name, the local directory cleanup approach, the cautious version reference reconciliation, the API route deletion investigation, and the sequencing order.

---

## Assessment of Each Directive

### 1. Version Target: `1.8.0`

**Agreed.** The rationale is sound:

- `1.7.0` is the current engineering baseline.
- The current work adds substantial engineering/security/governance capability.
- It does **not** constitute a breaking architectural release or a validated scientific result.
- PDMAL efficacy remains `N=0`.

**Boundary statement should be explicit:**

> `1.8.0` — pre-authorization hardening / experimental apparatus integrity release; does not imply empirical validation or pilot authorization.

### 2. Name: Preserve `DGAF-Framework`

**Agreed.** Do not change the canonical project name. The repository name (`ndrorchestration/DGAF-Framework`) is the authoritative identity.

**The local directory cleanup should be:**

```text
DGAF-Framework/ → DGAF-Framework-LEGACY/
DGAF-Framework-1/ → DGAF-Framework/
```

This resolves the naming collision while making the local filesystem match the canonical GitHub identity. The legacy wrapper should contain a `LEGACY.md` file noting its obsolete nature, but its Git history should not be modified.

### 3. Local Directory Cleanup

**Agreed.** The distinction between the live repository and the legacy wrapper is correct. The cleanup should be:

1. Rename `DGAF-Framework/` → `DGAF-Framework-LEGACY/`
2. Rename `DGAF-Framework-1/` → `DGAF-Framework/`
3. Add `LEGACY.md` to the legacy wrapper (documentation only)
4. Ensure the live repository's `.git` remains intact

**Do not:**

- Merge the legacy wrapper's contents into the live repository.
- Modify the legacy wrapper's Git history.
- Treat the legacy wrapper as part of the canonical project.

### 4. Version References: Exhaustive Reconciliation

**Agreed.** The classification approach is correct:

| Type | Example | Action |
|------|---------|--------|
| Canonical project version | `__version__ = "1.8.0"` | Update |
| Release/version metadata | `package.json` version | Update |
| Runtime/API health metadata | `pages/api/health.ts` version | Update |
| CI/deployment metadata | Workflow artifacts | Update as needed |
| Historical experiment identifiers | `ensemble_v17.py` | **Retain as historical** |
| Filename identifiers | `live_regression_v17.py` | **Retain as historical** |
| Documentation examples | Version numbers in examples | Update if illustrative |
| Compatibility assertions | "Requires Python 3.12" | Verify and update if needed |

**The agent should produce a `VERSION_REFERENCE_INVENTORY.md`** with a before/after classification of every version-like reference found in the repository.

### 5. API Route Deletions: Stop and Investigate

**Critical.** This is the one item that requires manual investigation before committing.

The files:

- `app/api/audit/route.ts`
- `app/api/health/route.ts`
- `app/api/orchestrate/route.ts`

**Investigation steps:**

1. **Git history:** When were they added? When were they last modified? What was their purpose?
2. **Current application routing:** Are they referenced in the application's routing configuration?
3. **Imports/references:** Are they imported elsewhere in the codebase?
4. **Deployment configuration:** Are they referenced in Vercel configuration or health checks?
5. **Tests:** Are there tests for these endpoints?
6. **Documentation:** Are they mentioned in API documentation?
7. **Vercel configuration:** Are they part of the deployment pipeline?

**Decision criteria:**

- If they are intentionally obsolete stubs: document the removal and commit.
- If they are still part of the live application contract: restore them.
- If status is ambiguous: keep them and mark for future deprecation.

**Do not push either state until the agent establishes which one is correct.**

### 6. `__pycache__` / `.pyc` Cleanup

**Agreed.** Remove from Git staging and verify `.gitignore` coverage.

**Check:**

- Are any `.pyc` files currently tracked? → Remove from index.
- Is `.gitignore` correctly configured? → Add `__pycache__/` and `*.pyc` if missing.
- Ensure they do not enter the release commit.

### 7. Critical Sequencing

**Agreed.** The sequence is correct:

```text
expert findings
      ↓
version/reference inventory
      ↓
API deletion provenance check
      ↓
legacy wrapper isolation
      ↓
local canonical directory normalization
      ↓
1.8.0 metadata update
      ↓
full tests + lint + build
      ↓
git diff / status / tracked-file audit
      ↓
review exact resulting tree
      ↓
commit
      ↓
CI
      ↓
push
```

**The epistemic state must remain unchanged:**

```text
Historical freeze 3510b868 = historical
Corrected runner = candidate apparatus
New freeze = not created
Authorization = NOT GRANTED
Empirical N = 0
```

**The version bump must not cause** README, release notes, badges, or status documents to imply that PDMAL has been empirically validated.

---

## Expert Agent Perspectives (Cross-Check)

### Scientific / Epistemic Perspective

> "The version target `1.8.0` correctly signals a pre-authorization hardening release. The release boundary statement is clear and prevents conflation with empirical validation. The preservation of historical identifiers (`v17`, `post-S070`) is correct – they are not equivalent to the package version. The epistemic controls are working: the old freeze is correctly classified as historical/superseded."

### QA / Evaluation Perspective

> "The sequencing is correct. The `__pycache__` cleanup and git diff audit are necessary hygiene steps. The agent should ensure that after the version update, all tests still pass. The `1.8.0` release should include a `RELEASE_NOTES.md` that explicitly states what has changed and what has not changed (empirical state remains N=0)."

### Security / Architecture Perspective

> "The blinding and SHA binding corrections are critical. The agent should verify that `PDMAL_FROZEN_COMMIT_SHA` is not hardcoded but read from the environment or manifest. The API route deletion investigation is correct – health and orchestrate are likely live endpoints; the agent must confirm before deletion."

### Systems Architecture Perspective

> "The local directory cleanup is correct. The legacy wrapper should be isolated. The version reconciliation should not alter historical identifiers. The agent should ensure that the package identity remains `dgaf-framework` (lowercase) for Python packaging, while the display name remains `DGAF-Framework`. The `1.8.0` release should be tagged and published only after CI passes on the final commit."

---

## Implementation Summary

| Step | Action | Status |
|------|--------|--------|
| 1 | Version inventory | Pending |
| 2 | API route investigation | Pending |
| 3 | Legacy wrapper isolation | Pending |
| 4 | Directory normalization | Pending |
| 5 | `1.8.0` metadata update | Pending |
| 6 | Full tests + lint + build | Pending |
| 7 | git diff / status audit | Pending |
| 8 | Review resulting tree | Pending |
| 9 | Commit | Pending |
| 10 | CI | Pending |
| 11 | Push | Pending |

**The epistemic state remains unchanged:**

```text
Historical freeze 3510b868 = historical
Corrected runner = candidate apparatus
New freeze = not created
Authorization = NOT GRANTED
Empirical N = 0
```

---

## Concise Directive to Agents

> **Proceed with `1.8.0` as an engineering/pre-authorization hardening release. Preserve `DGAF-Framework` as the canonical project/package/display identity. Rename the obsolete local wrapper to `DGAF-Framework-LEGACY`, then normalize the actual repository directory to `DGAF-Framework`. Exhaustively inventory version references before modifying them; distinguish current semantic version metadata from historical identifiers such as `v17` and `post-S070`. Do not mechanically rewrite historical identifiers. Investigate the three deleted API routes through Git history, references, tests, and deployment configuration before deciding whether they should remain deleted. Remove `__pycache__`/`.pyc` from tracking. Do not push until the resulting tree, version-reference inventory, API-route disposition, and CI state are all reconciled. Preserve the epistemic state: PRE-AUTHORIZATION, NOT AUTHORIZED, N=0, historical freeze superseded for the corrected runner.**