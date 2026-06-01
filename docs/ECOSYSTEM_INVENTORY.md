# ECOSYSTEM INVENTORY

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-31  
> **Anchor:** S068 (open)

Canonical inventory of all system components across GitHub, Supabase, and Vercel.
Source of truth for cross-platform deployment status.

---

## GitHub Repositories — 24 total

### Governance Spine (1)

| Repo | Visibility | Status |
|---|---|---|
| [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) | Public | 🟢 Active · S068 open |

### Active App / Tool Repos (8)

| Repo | Visibility | Vercel | Status |
|---|---|---|---|
| [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard) | Private | — Never deployed | 🟢 GitHub only |
| [aoga-dashboard](https://github.com/ndrorchestration/aoga-dashboard) | Private | ✅ Deployed | 🟢 Active |
| [Driftwatch](https://github.com/ndrorchestration/Driftwatch) | Public | ✅ Deployed (phiknightverticalcorridor) | 🟢 Active · see Vercel table |
| [phi-calculus-app](https://github.com/ndrorchestration/phi-calculus-app) | Private | — | 🟢 Active |
| [junior-apogee-app](https://github.com/ndrorchestration/junior-apogee-app) | Public | — | 🟢 Active |
| [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh) | Public | — | 🟢 Active |
| [3d-visualization-hub](https://github.com/ndrorchestration/3d-visualization-hub) | Public | — | 🟢 Active |
| [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) | Public | — | 🟢 Active |

### Portfolio / Eval Repos (5)

| Repo | Visibility | Status |
|---|---|---|
| [ai-prompt-systems-portfolio](https://github.com/ndrorchestration/ai-prompt-systems-portfolio) | Public | 🟢 Active |
| [resumeapex-eval](https://github.com/ndrorchestration/resumeapex-eval) | Public | 🟢 Active |
| [Amethyst-Governance-Eval-Stack](https://github.com/ndrorchestration/Amethyst-Governance-Eval-Stack) | Private | 🟢 Active |
| [ai-prompt-engineering-portfolio](https://github.com/ndrorchestration/ai-prompt-engineering-portfolio) | Private | 🟢 Active |
| [AI-Prompt-Engineer](https://github.com/ndrorchestration/AI-Prompt-Engineer) | Private | 🟢 Active |

### Framework / Standards (4)

| Repo | Visibility | Status |
|---|---|---|
| [ai-governance-frameworks](https://github.com/ndrorchestration/ai-governance-frameworks) | Public | 🟢 Active |
| [Gold-star-standards](https://github.com/ndrorchestration/Gold-star-standards) | Private | 🟢 Active |
| [prompt-optimization-library](https://github.com/ndrorchestration/prompt-optimization-library) | Private | 🟢 Active |
| [gold-star-qa-framework](https://github.com/ndrorchestration/gold-star-qa-framework) | Private | 🔴 Archived |

### Utility / Infra (4)

| Repo | Visibility | Status |
|---|---|---|
| [automation-scripts](https://github.com/ndrorchestration/automation-scripts) | Private | 🟢 Active |
| [.github](https://github.com/ndrorchestration/.github) | Public | 🟢 Active |
| [api](https://github.com/ndrorchestration/api) | Private | 🟢 Active |
| [chat-archives](https://github.com/ndrorchestration/chat-archives) | Private | 🟢 Active |

### Career / Positioning (2)

| Repo | Visibility | Status |
|---|---|---|
| [career-positioning](https://github.com/ndrorchestration/career-positioning) | Private | 🟢 Active |
| [ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) | Public | 🟢 Active (org profile) |

---

## Vercel Deployments — Ground Truth S068

> **Verified:** 2026-05-31 via Vercel dashboard (Ender) + `vercel project ls` CLI  
> **3 active projects** after `dgaf-framework` deleted 2026-05-31 23:20 EDT

| Vercel Project | Production URL | Source Repo | Last Deploy | Status |
|---|---|---|---|---|
| [ndrorchestration](https://vercel.com/ndrorchestration/ndrorchestration) | [ndrorchestration.vercel.app](https://ndrorchestration.vercel.app/) | [ndrorchestration/ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) | May 21 · COLLEEN SWEEP-001 Phase 3 | ✅ Ready |
| [phiknightverticalcorridor](https://vercel.com/ndrorchestration/phiknightverticalcorridor) | [project-7ybao.vercel.app](https://project-7ybao.vercel.app/) | [ndrorchestration/Driftwatch](https://github.com/ndrorchestration/Driftwatch) | May 26 | ⚠️ No Production Deployment |
| [aoga-dashboard](https://vercel.com/ndrorchestration/aoga-dashboard) | [aoga-dashboard.vercel.app](https://aoga-dashboard.vercel.app/) | [ndrorchestration/aoga-dashboard](https://github.com/ndrorchestration/aoga-dashboard) | May 27 · v1.2.0 tag [Amethyst] | ✅ Ready |
| ~~dgaf-framework~~ | ~~deleted~~ | ~~DGAF-Framework~~ | — | 🗑️ Deleted 2026-05-31 |

### Notes

- **`pptl-governance-dashboard`** — confirmed never deployed to Vercel. GitHub repo exists. S067 inventory entry was incorrect.
- **`phiknightverticalcorridor`** — Vercel project name for the Driftwatch repo. Has no Production Deployment (preview-only or deployment pending).
- **`ndrorchestration`** — org profile / ecosystem map site. Last updated by COLLEEN SWEEP-001 Phase 3 on May 21.

---

## Supabase Projects — 1 confirmed

| Project | ID | Region | Postgres | Status |
|---|---|---|---|---|
| ndrorchestration's Project | `lfisbywaidhmxsjyteud` | us-east-2 | 17.6.1 | 🟢 ACTIVE_HEALTHY |

---

## Summary Totals

| Platform | Total | Active / Ready | Notes |
|---|---|---|---|
| GitHub Repos | 24 | 23 | 1 archived |
| Vercel Projects | 3 | 2 Ready · 1 no production deploy | dgaf-framework deleted S068 |
| Supabase Projects | 1 | 1 | — |

---

*Created S067 · Finalized S068 · Amethyst × COLLEEN × Ender · 2026-05-31*  
*Vercel source: dashboard (Ender) + `vercel project ls` CLI · 2026-05-31 23:22 EDT*
