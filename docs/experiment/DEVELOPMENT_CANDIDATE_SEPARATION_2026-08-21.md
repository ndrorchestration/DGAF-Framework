# Development / Candidate Separation

**Established:** 2026-08-21  
**Status:** NOT YET ESTABLISHED

---

## Current State

There is currently **no separation** between development and the candidate in the DGAF-Framework repository.

### What exists today

| Artifact | Location | SHA |
|---|---|---|
| Development HEAD | `main` branch | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Candidate (local) | `pr-77-head` branch | `94fb6fdff64f2919d35938c5b1cb506625cf1139` |
| Candidate (GitHub) | PR #77 head | `b25a914c0e86333a9af4b216a9acdfaec28e42b0` |
| Uncommitted changes | Working tree | `DGAF_PDMAL_EXECUTION_READINESS_REFINED_2026-08-21.md`, `DGAF_QA_ASSERTION_REPORT.md` |

### What's missing

1. **No candidate tag or branch that is protected from development changes.** The `pr-77-head` branch exists locally but is not a permanent separation — it's a snapshot of a PR state that can drift.

2. **No candidate manifest committed to the repository.** The `CANDIDATE_MANIFEST_2026-08-21.json` identifies the candidate but is not yet committed. Without a committed manifest, there is no canonical reference for "the candidate."

3. **No freeze commit.** The freeze manifest references `freeze_commit_sha: PLACEHOLDER`. No actual git commit freezes the candidate.

4. **No clear naming convention.** Files are not marked as "candidate" vs "development." Merging PR #77 to `main` would collapse the candidate into the development HEAD, losing the distinction.

---

## The Risk

If PR #77 is merged to `main` without first establishing separation:

1. The candidate (`94fb6fd` / `b25a914c`) becomes indistinguishable from development HEAD.
2. Any subsequent development change to `main` silently changes the "candidate."
3. The experiment later points to "whatever is on main" — which is ambiguous.
4. The evidence chain (`candidate SHA → source`) becomes untraceable because `main` moves.

This is exactly the ambiguity the sprint finding #1 and the expert panel correction C5 warn about.

---

## Recommended Approach

### Step 1: Commit the candidate manifest first

Before any merge, commit `CANDIDATE_MANIFEST_2026-08-21.json` to the repository. This establishes a canonical reference for the candidate that exists independently of any branch.

```
git add docs/experiment/CANDIDATE_MANIFEST_2026-08-21.json
git commit -m "docs(pdmal): establish candidate manifest for PR #77 corrected apparatus

This manifest identifies the PR #77 corrected pilot apparatus as a
specific candidate (SHA 94fb6fd locally, b25a914c on GitHub) with
all component blob SHAs verified against git ls-tree.

N=0. NOT AUTHORIZED. PRE-FREEZE. This manifest identifies the
candidate but does NOT make it immutable."
```

### Step 2: Create a candidate reference (branch or tag)

Create a named reference that points to the candidate SHA:

```
# Option A: tag (immutable by convention)
git tag pdmal-candidate-2026-08-21 94fb6fdff64f2919d35938c5b1cb506625cf1139

# Option B: dedicated branch (can be updated, needs protection)
git branch pdmal-candidate-2026-08-21 94fb6fdff64f2919d35938c5b1cb506625cf1139
```

A tag is preferred because it's conventionally immutable — you cannot move a tag without explicit force.

### Step 3: Protect the candidate reference

The candidate reference should not be movable by routine development:

- If using a tag: conventionally protected (force-push requires explicit action)
- If using a branch: protected via branch protection rules (if GitHub permissions allow)

### Step 4: Merge PR #77 to main separately

After the candidate is identified and referenced, merge PR #77 to `main` as a development vehicle:

```
# After candidate is tagged and manifest committed:
# Merge PR #77 to main (development continues on main)
# The candidate remains identifiable via the tag
```

### Step 5: Document the separation

Update this document (or a companion document) to record:

- Which SHA is the candidate
- Which reference identifies it (tag or branch)
- Which SHA is development HEAD
- The date separation was established

---

## What Separation Enables

With separation established:

1. **The candidate is identifiable.** Anyone can point to `pdmal-candidate-2026-08-21` and know exactly what is being tested.

2. **Development can continue.** Changes to `main` do not silently alter the candidate.

3. **P2 can bind to the candidate.** CI workflows can pin to the candidate SHA rather than running on `pull_request` paths.

4. **The evidence chain is traceable.** Later evidence can say "this result came from candidate `pdmal-candidate-2026-08-21`" and a reviewer can resolve that to exact blob SHAs.

5. **The freeze can be specific.** The freeze manifest's `freeze_commit_sha` can point to a specific commit that embodies the candidate, not to a moving branch.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This document describes a desired state (separation) that does NOT yet exist. It does NOT constitute a freeze. It does NOT authorize empirical data collection.

Separation is a prerequisite for Gate 2 (build immutable candidate), which is itself a prerequisite for the freeze that precedes authorization.
