# Drive-GitHub Sync Spec

**Pattern:** P-20 — Drive-GitHub-Sync-Seal  
**Version:** 1.0  
**Maintained by:** Amethyst-Conductor (COLLEEN sub-agent)  
**Last updated:** 2026-05-01 (S012)

---

## Purpose

At every SWEEP_LOG seal, COLLEEN verifies bidirectional consistency between Google Drive (working doc layer) and GitHub (canonical governance layer).

## Sync Architecture

```
┌─────────────────────────────────────────────────────────┐
│              CROSS-PLATFORM SYNC ARCHITECTURE            │
│                 IMP-05 / DGAF-Framework                  │
├──────────────┬──────────────────┬───────────────────────┤
│   LAYER      │   SOURCE         │   DIRECTION            │
├──────────────┼──────────────────┼───────────────────────┤
│ Canonical    │ GitHub           │ → Drive (export)       │
│ Governance   │ DGAF-Framework   │ Drive = read replica   │
├──────────────┼──────────────────┼───────────────────────┤
│ Working Docs │ Google Drive     │ → GitHub (commit-back) │
│ Session Notes│ Drive/00-Inbox   │ COLLEEN gates transfer │
├──────────────┼──────────────────┼───────────────────────┤
│ Eval Assets  │ Drive/01-Projects│ Bidirectional (P-08)   │
│ Rubrics      │ + GitHub repos   │ Delta verified at seal │
├──────────────┼──────────────────┼───────────────────────┤
│ Brand Docs   │ Drive/02-Brand   │ → GitHub (P-19 audit)  │
│ IMP-05 spec  │ IMP_05_BRAND_SPEC│ Read-only on GitHub    │
├──────────────┼──────────────────┼───────────────────────┤
│ Career / IP  │ Drive (private)  │ NEVER → GitHub public  │
│ PATHS.md     │ career-position  │ Private repo only      │
└──────────────┴──────────────────┴───────────────────────┘
```

## Seal Verification Checklist (P-20)

Before any SWEEP_LOG seal commit, COLLEEN verifies:

- [ ] Drive master inventory matches GitHub CROSS_REF repo count
- [ ] No active Drive doc exists for an archived/deleted GitHub repo
- [ ] Session notes from current session committed or summarized to SWEEP_LOG
- [ ] No CSDF / CyberShield references in any Drive doc that crosses to GitHub
- [ ] IMP-05 four-element checklist verified on all public repos touched this session

## Exclusions (Never Sync to GitHub Public)

- `career-positioning` private repo docs
- PATHS.md and career strategy documents
- Client data or proprietary workflow configs
- Raw session transcripts without COLLEEN sanitization

## Current Status

**Drive API scope:** NOT active in current session toolset.  
**Workaround:** Manual Drive verification by Njineer at each seal.  
**Resolution path:** Scope Drive API access to enable P-08/P-20 auto-execution.
