# QA Rubric — Agent Lyra

**Agent:** Agent Lyra  
**Role Domain:** Narrative + Expression  
**Formation:** Extended  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Lyra's narrative coherence, IMP-05 brand voice consistency, and portfolio language quality. Lyra governs the expressive layer of DGAF outputs — documentation, communications, and portfolio materials.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Narrative Coherence** | 30% | ≥ 0.85 | Session arc, commit messages, and documentation tell a consistent story. No contradictory narratives across files. |
| D2 | **IMP-05 Brand Voice (P-19)** | 30% | ≥ 0.88 | Brand voice consistent with DGAF IMP-05 standard at P-19. Tone, register, and terminology aligned. |
| D3 | **Portfolio Language Quality** | 20% | ≥ 0.85 | Portfolio-facing text (READMEs, Needle templates, release notes) meets quality bar. No placeholder text shipped. |
| D4 | **Terminology Consistency** | 20% | ≥ 0.90 | Agent names, framework terms, and versioning language consistent across all files in a session. |

**Composite Pass:** ≥ 0.87.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Narrative contradiction** | Two committed files describe the same event with conflicting framing | COLLEEN surfaces delta; Lyra authors reconciliation patch; Amethyst gates re-commit |
| F2 | **Placeholder shipped** | Portfolio-facing file contains [PLACEHOLDER] or TBD text at release | Herald blocks release; Lyra completes content before P-19 re-check |
| F3 | **Voice drift** *(non-obvious)* | Lyra gradually shifts DGAF brand voice across sessions without a formal IMP-05 revision, making old docs feel out-of-brand | Reciprocity flags cross-session tone delta; Lyra issues IMP-05 revision or revertion |

---

## Gate Ownership

| Gate | Lyra Role |
|------|----------|
| P-19 | Brand voice consistency |

---

*Rubric authority: Amethyst-Conductor.*
