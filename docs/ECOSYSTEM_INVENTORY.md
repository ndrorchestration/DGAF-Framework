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
| [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard) | Private | ❌ Not found in Vercel | ⚠️ Inventory correction — see note |
| [aoga-dashboard](https://github.com/ndrorchestration/aoga-dashboard) | Private | ✅ Deployed | 🟢 Active |
| [Driftwatch](https://github.com/ndrorchestration/Driftwatch) | Public | — | 🟢 Active |
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

> **Verified:** 2026-05-31 via `vercel project ls` (Ender terminal, Vercel CLI 54.6.1)  
> **Prior inventory was incorrect** — `pptl-governance-dashboard` does not exist as a Vercel project.

| Project | Production URL | Status | Notes |
|---|---|---|---|
| `aoga-dashboard` | [https://aoga-dashboard.vercel.app](https://aoga-dashboard.vercel.app) | ✅ Ready | Last deployed 4d ago |
| `dgaf-framework` | [https://dgaf-framework-ndrorchestration.vercel.app](https://dgaf-framework-ndrorchestration.vercel.app) | ⚠️ Error | 30+ failed builds · Python repo · **Recommended: delete project** |
| `ndrorchestration` | [https://ndrorchestration-ndrorchestration.vercel.app](https://ndrorchestration-ndrorchestration.vercel.app) | 🟡 Unknown | Not previously inventoried · requires Ender review |
| `phiknightverticalcorridor` | — | 🟡 No URL | Not previously inventoried · no production URL |

### ⚠️ Inventory Corrections (S068)

1. **`pptl-governance-dashboard`** — previously listed as "✅ Deployed" in S067 inventory. Confirmed **not present** in `vercel project ls` output. GitHub repo exists; Vercel project either was never created or was deleted. Requires Ender clarification.
2. **`dgaf-framework`** — Vercel project exists but should not. This is a Python governance library with no frontend. Produced 30+ consecutive `● Error` Production deployments (user `flickerflash-8879`, 2–3 days ago). **Action required: disconnect repo and delete Vercel project.**
3. **`ndrorchestration`** and **`phiknightverticalcorridor`** — present in Vercel but not in prior inventory. Requires Ender review and classification.

### Recommended Actions (Ender)

| Action | Priority | Command / URL |
|---|---|---|
| Delete `dgaf-framework` Vercel project | P1 | [vercel.com/ndrorchestration/dgaf-framework/settings](https://vercel.com/ndrorchestration/dgaf-framework/settings) → Danger Zone → Delete |
| Clarify `pptl-governance-dashboard` Vercel status | P1 | Was it deployed? Does it need to be re-created? |
| Review `ndrorchestration` project | P2 | [vercel.com/ndrorchestration/ndrorchestration](https://vercel.com/ndrorchestration/ndrorchestration) |
| Review `phiknightverticalcorridor` project | P2 | [vercel.com/ndrorchestration/phiknightverticalcorridor](https://vercel.com/ndrorchestration/phiknightverticalcorridor) |

---

## Supabase Projects — 1 confirmed

| Project | ID | Region | Postgres | Status |
|---|---|---|---|---|
| ndrorchestration's Project | `lfisbywaidhmxsjyteud` | us-east-2 | 17.6.1 | 🟢 ACTIVE_HEALTHY |

---

## Summary Totals

| Platform | Total | Active | Needs Action |
|---|---|---|---|
| GitHub Repos | 24 | 23 | 1 (archived) |
| Vercel Projects | 4 | 1 confirmed healthy | 3 require Ender review |
| Supabase Projects | 1 | 1 | 0 |

---

*Created S067 · Updated S068 · Amethyst × COLLEEN × Ender · 2026-05-31*  
*Vercel source: `vercel project ls` output · Ender terminal · 2026-05-31 23:17 EDT*
