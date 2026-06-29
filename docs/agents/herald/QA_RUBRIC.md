# QA Rubric — Agent Herald

**Agent:** Agent Herald  
**Role Domain:** Communication + Release  
**Formation:** Extended  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Herald's external publication gate, changelog authorship, release notes, and inter-agent status broadcast. Herald is the release and communication authority — this rubric governs publication integrity and broadcast fidelity.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **External Publication Gate** | 30% | ≥ 0.92 | No external-facing content published without Herald clearance. Publication checklist complete before release. |
| D2 | **Changelog Accuracy** | 25% | ≥ 0.90 | Changelog entries accurately reflect committed changes. No omissions, no embellishments. SHA-traceable. |
| D3 | **Release Notes Quality** | 20% | ≥ 0.88 | Release notes complete, accurate, and audience-appropriate. No placeholder text. Lyra brand voice applied. |
| D4 | **Inter-agent Status Broadcast** | 15% | ≥ 0.88 | Status updates broadcast to all relevant agents at gate events. No agents left uninformed of state changes that affect their lane. |
| D5 | **Release Timing Compliance** | 10% | ≥ 0.90 | Releases occur only after P-15 seal + Amethyst sign-off. No premature releases. |

**Composite Pass:** ≥ 0.89.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Premature release** | External content published before P-15 seal | Sentinel flags; Herald retracts release; full Quintet re-seal required before re-publish |
| F2 | **Changelog omission** | Committed files not reflected in changelog | COLLEEN surfaces at next P-02; Herald patches changelog before next release |
| F3 | **Selective broadcast** *(non-obvious)* | Herald broadcasts gate status to orchestration agents but omits Extended formation agents whose lane is affected, creating split state | Amethyst audits broadcast log; Herald re-broadcasts to full active formation |

---

## Gate Ownership

| Gate | Herald Role |
|------|-------------|
| All release gates | External publication clearance |

---

*Rubric authority: Amethyst-Conductor.*
