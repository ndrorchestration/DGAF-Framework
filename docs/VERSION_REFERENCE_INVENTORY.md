# Version Reference Inventory — DGAF-Framework

**Generated:** 2026-08-21
**Purpose:** Exhaustive classification of every version-like reference in the repository, with before/after state for the 1.7.0 → 1.8.0 canonical version bump.
---

## Classification Key

| Type | Description | Treatment |
|------|-------------|-----------|
| **Canonical version** | The project's current semantic version — what a user/package manager sees | Updated to 1.8.0 |
| **Release/runtime metadata** | Version strings surfaced at runtime, in CI, or in deployment config | Updated to 1.8.0 |
| **Historical identifier** | Version-like strings that are NOT the package version — experiment anchors, citation tags, filenames | Retained as-is |
| **Documentation example** | Version numbers in docs that illustrate a concept | Reviewed; updated if illustrative of current state |
| **Not a version** | Strings that look like versions but aren't (e.g., pattern IDs, session IDs) | No action |

---

## Current Semantic Version References (Updated to 1.8.0)

| File | Before | After | Type | Notes |
|------|--------|-------|------|-------|
| `package.json` | `1.7.0` | `1.8.0` | Canonical (npm) | `npm run build` consumes this |
| `resonant_decay/__init__.py` | `__version__ = "1.7.0"` | `__version__ = "1.8.0"` | Canonical (Python) | `import resonant_decay; resonant_decay.__version__` |
| `components/ensemble_v17.py` | `Version: 1.7.0` | `Version: 1.8.0` | Canonical (doc header) | File name retains `v17` — see Historical below |
| `pages/api/health.ts` | `'1.7.0'` | `'1.8.0'` | Runtime metadata | `ENSEMBLE_VERSION` env fallback |
| `pages/api/audit.ts` | `'1.7.0'` | `'1.8.0'` | Runtime metadata | `ENSEMBLE_VERSION` env fallback |
| `pages/api/roster.ts` | `'1.7.0'` | `'1.8.0'` | Runtime metadata | `ENSEMBLE_VERSION` env fallback |
| `.github/workflows/deploy.yml` (env var) | `echo "1.7.0" \| vercel env add ENSEMBLE_VERSION` | `echo "1.8.0"` | CI/deployment | Sets Vercel env var on deploy |
| `.github/workflows/deploy.yml` (assertion) | `[ "$VER" = "1.7.0" ]` | `[ "$VER" = "1.8.0" ]` | CI/deployment | Health check version assertion |
| `scripts/live_regression_v17.py` | `== "1.7.0"` | `== "1.8.0"` | Runtime assertion | Health pre-flight version check |
| `scripts/quick_check.py` | `v1.7.0` | `v1.8.0` | Documentation example | Package version printout |

---

## Historical Identifiers (Retained — NOT bumped)

These are version-like strings that are NOT the package version. They identify specific experiments, citation states, or filenames. Bumping them would destroy historical provenance.

| File/Location | Value | Meaning | Why retained |
|---------------|-------|---------|--------------|
| `CITATION.cff` | `version: "post-S070"` | Citation version tag tied to governance session S070 | NOT a package version; identifies the governance state at citation time |
| `components/ensemble_v17.py` | filename: `v17` | Ensemble version 1.7 identifier | Historical artifact; file documents v1.7 ensemble architecture |
| `components/ensemble_v16.py` | filename: `v16` | Ensemble version 1.6 identifier | Historical artifact; file documents v1.6 ensemble architecture |
| `scripts/live_regression_v17.py` | filename: `v17` | Regression script for ensemble v1.7 | Historical artifact; script tests v1.7 contract |
| `resonant_decay/simulations/drift_v17.py` | filename: `v17` | Drift simulation for v1.7 | Historical artifact |
| `tests/sim_multiturn_drift_v17.py` | filename: `v17` | Multi-turn drift simulation for v1.7 | Historical artifact |

**Rule:** Filenames containing `v17` or `v16` are NOT package version references. They are historical experiment identifiers. The canonical version bump does NOT rename these files.

---

## Not Version References (No Action)

| File/Location | Value | What it actually is |
|---------------|-------|---------------------|
| `CITATION.cff` | `cff-version: 1.2.0` | Citation file format version (CFF spec), not project version |
| `package-lock.json` | `"version": "1.7.0"` | Auto-generated from `package.json` — regenerated on next `npm install` |
| `.github/workflows/deploy.yml` | `tlaplus/releases/tag/v1.8.0` | TLA+ Tools release version (Java dependency), not DGAF version |
| `docs/formation_*.md` | Various `v1.x` refs | Formation topology version references |
| `docs/gates/GATE_*.md` | Various gate IDs | Gate identifiers, not versions |
| `components/KAPPA/` | `v3.6.0` | KAPPA router version (sub-component) |
| `docs/agents/*/SPEC.md` | Various agent spec versions | Per-agent spec versions, not project version |

---

## Files Without Version References (Verified)

- `middleware.ts` — no version string
- `lib/evidence.ts` — no version string
- `src/evidence_mode.py` — no version string
- `vercel.json` — no version string
- `CITATION.cff` — `post-S070` retained (see Historical)
- `app/api/` (deleted routes) — deleted in commit `7f7ef62`
- `requirements*.txt` — dependency pins only
- `tsconfig.json` — no version strings
- `schemas/*.json` — no version strings
- `dashboard/` — no version strings
- `registry/` — ecosystem audit, manifests
- `patterns/NDR_*.md` — no version strings
- `docs/` — agent SPEC versions are per-agent

---

## Epistemic Boundary

This inventory documents what was changed and what was deliberately not changed. It does not imply that version 1.8.0 has been empirically validated or that pilot authorization has been granted.

**Epistemic state (unchanged by this version bump):**
- Historical freeze `3510b868` = historical
- Corrected runner = candidate apparatus
- New freeze = not created
- Authorization = NOT GRANTED
- Empirical N = 0
