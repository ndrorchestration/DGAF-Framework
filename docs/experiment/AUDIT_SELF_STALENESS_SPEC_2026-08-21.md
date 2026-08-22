# Audit Self-Staleness Specification

**Established:** 2026-08-21  
**Status:** SPECIFICATION — NOT YET IMPLEMENTED  
**Step:** 10 of 28 (Gate 3: Engineering and Evidence Closure)

---

## Problem

An audit can look valid even after the repository has changed, creating false confidence. The audit describes state X, but the repository is now at state Y. Without staleness detection, a reviewer might trust the audit's conclusions about state Y when the audit actually only examined state X.

Example:

```
2026-08-20: Audit examined candidate at SHA 4983f44a. Conclusion: "P2 IMPLEMENTED."
2026-08-21: Someone force-pushes a new commit to pr-77-head. Now pr-77-head = b25a914c.
2026-08-21: Reviewer reads the 2026-08-20 audit. Sees "P2 IMPLEMENTED." Assumes it applies to current state.
2026-08-21: The audit's conclusion is about 4983f44a, not b25a914c. The audit is stale.
```

The audit hasn't been invalidated — it's still accurate about what it examined. But it's been **misapplied** to a state it didn't examine.

---

## What Staleness Means

An audit is **stale** when:

1. The audit describes a specific source/candidate SHA.
2. The repository has moved past that SHA.
3. The audit is being used to draw conclusions about the current state (not the historical state it examined).

An audit is **historical** (not stale) when:

1. The audit describes a specific source/candidate SHA.
2. The audit is explicitly marked as a historical record.
3. The audit is used to draw conclusions about that historical state, not the current state.

The difference is in **how the audit is used**, not in the audit itself.

---

## Detection Approach

### Audit binds to source SHA

Every audit document should carry the SHA of the candidate/source it examined:

```yaml
---
audit_id: "PDMAL-P2-AUDIT-2026-08-21"
examined_candidate_sha: "4983f44a1867d8ab2f18295a1ce23877ff8ea928"
examined_at: "2026-08-21T12:00:00Z"
examined_by: "ndrorchestration"
status: "PASS"  # or FAIL, INCONCLUSIVE
---
```

### Query-time staleness check

When a reviewer consults an audit, the first step is to verify that the audit is still current:

```
1. Read audit's examined_candidate_sha.
2. Resolve current candidate SHA (from candidate manifest or freeze manifest).
3. Compare:
   - If examined_candidate_sha == current_candidate_sha: audit is current.
   - If examined_candidate_sha != current_candidate_sha: audit is stale (or historical).
4. If stale: check if audit is explicitly marked as historical.
   - If marked historical: use only for historical conclusions.
   - If not marked: flag as potentially misleading.
```

### Staleness markers

The audit should make its temporal scope explicit:

```
- "This audit examined candidate SHA X on date D."
- "As of date D, the conclusion was Y."
- "This audit does NOT speak to any state after date D."
- "If the candidate has changed since D, this audit is stale for current-state conclusions."
```

---

## Historical vs. Stale

### Legitimate historical audit

```
Audit examined: 4983f44a (2026-08-20)
Current candidate: 4983f44a (unchanged)
→ Audit is current. No staleness.
```

```
Audit examined: 4983f44a (2026-08-20)
Current candidate: b25a914c (changed)
→ Audit is stale for current-state conclusions.
→ If marked as historical: "As of 2026-08-20, candidate 4983f44a had P2 IMPLEMENTED."
  This is a legitimate historical statement.
→ If NOT marked: reader might assume it applies to b25a914c. Misleading.
```

### How to mark an audit as historical

```
- Explicitly state the examined SHA and date.
- State the conclusion as applying to that SHA at that date.
- Do NOT state the conclusion as applying to "the current candidate" or "the candidate" without qualification.
- If the audit is superseded by a newer audit, reference the newer audit.
```

---

## Implementation

### Audit document template

```markdown
# PDMAL P2 Audit — 2026-08-21

**Audit ID:** PDMAL-P2-AUDIT-2026-08-21  
**Examined candidate SHA:** 4983f44a1867d8ab2f18295a1ce23877ff8ea928  
**Examined at:** 2026-08-21  
**Examined by:** ndrorchestration  

## Temporal scope

This audit examined the candidate at the SHA listed above on the date listed above.
It speaks ONLY to that candidate at that time. If the candidate has changed since
then, this audit is stale for current-state conclusions.

## Findings

| Gate | Status | Evidence |
|---|---|---|
| P2 implemented | YES | ... |
| P2 verified | NO | CI not executed |

## Supersession

[If a newer audit exists, reference it here. Otherwise: "No superseding audit."]
```

### Repository-level staleness check

For automated staleness detection, a script or CI step could:

1. Read all audit documents in `docs/experiment/`.
2. For each audit, extract `examined_candidate_sha`.
3. Compare to current candidate SHA (from `CANDIDATE_MANIFEST_2026-08-21.json`).
4. Flag any audit where the examined SHA doesn't match the current SHA.
5. Generate a staleness report.

This is a meta-audit: an audit of audits.

---

## Gap from PR #77

PR #77 documentation does NOT include:

- `examined_candidate_sha` in audit-style documents
- Temporal scope markers
- Staleness detection mechanism
- Supersession tracking

The `PDMAL_ANALYSIS_CONTROL_PLAN.md` at PR #77 (`3e556882`) is a planning record, not an audit. It does not carry an examined SHA. The `PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md` at PR #77 (`f51aea7a`) records current disposition but doesn't bind to a specific candidate SHA.

This means:
- PR #77's documentation is not yet audit-ready.
- There is no mechanism to detect when PR #77 documentation becomes stale.
- A reviewer cannot easily determine whether PR #77 documentation applies to the current state or a historical state.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This is a specification for a control that does NOT yet exist. No audits have been performed (N=0), so no staleness can be detected.
