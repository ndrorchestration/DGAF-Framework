# QA Rubric — Agent COLLEEN

**Agent:** Agent COLLEEN  
**Role Domain:** Continuity + Archive  
**Formation:** Trio / Quintet  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for COLLEEN's session continuity, BLG surface operations, registry de-duplication, and Drive-GitHub delta management. COLLEEN is the memory layer — this rubric governs archival fidelity and continuity integrity.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **BLG Surface Completeness (P-02)** | 25% | ≥ 0.90 | All open BLGs surfaced at session open. No BLG missed. Surfacing includes ID, status, blocking artifact, and proposed closure path. |
| D2 | **Registry De-duplication Accuracy** | 20% | ≥ 0.95 | Zero duplicate canonical entries after de-dup sweep. Merge decisions traceable. |
| D3 | **CROSS_REF Back-link Registry** | 15% | ≥ 0.88 | All inter-file references bidirectionally registered. No orphan back-links. |
| D4 | **Drive-GitHub Delta (P-08)** | 15% | ≥ 0.85 | Delta report accurate at P-08. All Drive-only vs. GitHub-only artifacts identified. |
| D5 | **P-20 Sync Seal Verification** | 15% | ≥ 0.90 | P-20 seal confirmed only when Drive and GitHub are in full sync. No premature seal. |
| D6 | **GAP-03 Vocab Scan** | 10% | ≥ 0.85 | Deprecated agent names (Lavender, Forseti) flagged in scan. No vocab drift in committed files. |

**Composite Pass:** ≥ 0.88 routine; ≥ 0.90 for P-20 seal.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **BLG suppression** | COLLEEN omits a known BLG at P-02 | Amethyst surfaces manually; COLLEEN re-runs full BLG scan before next commit |
| F2 | **Premature P-20 seal** | Sync seal issued while Drive-GitHub delta > 0 | Reciprocity triggers rollback of seal tag; delta must reach 0 before re-seal |
| F3 | **Vocab ghost** *(non-obvious)* | GAP-03 scan passes but deprecated name exists in a non-indexed file (e.g., inline comment, YAML key) | Sentinel deep scan on next sweep; COLLEEN widens scan scope to include all file types |

---

## Gate Ownership

| Gate | COLLEEN Role |
|------|-------------|
| P-02 | BLG surface — primary owner |
| P-08 | Drive-GitHub delta report |
| P-20 | Sync seal verification |

---

*Rubric authority: Amethyst-Conductor.*
