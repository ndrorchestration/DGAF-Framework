# METRICS_PROVENANCE.md
## NDR Governance Stack — Metrics Provenance Registry

```
Status:       ACTIVE — SKELETON (backfill required by Week 9 per Research Program Charter)
Maintained-by: Metrics and Provenance Engineer (Role 5)
COLLEEN-audit: PENDING
Session:      S069
Date:         2026-06-13
```

> Every metric that appears in any NDR governance document must have a row in this table. A CI linter (`scripts/lint_provenance.py`) will block merges that reference a metric not registered here. Metrics without a reproduce command are flagged as UNVERIFIED.

---

## Provenance Table

| Metric Name | Definition | Claimed Value | Baseline | Reproduce Command | Commit Hash | Substrate | Runner | Date | Status |
|-------------|-----------|--------------|----------|-------------------|-------------|-----------|--------|------|--------|
| `governance_clear` improvement | % of eval records passing all governance contracts | 82.6% → 100% | KAPPA v3.5 threshold defaults | `pytest pptl/tests/ -m governance --base=v3.5` | `e900bdb` | Transformer decoder | TBD | 2026-05-30 | ⚠️ NEEDS REPRODUCE CMD VERIFICATION |
| Constraint compliance improvement | % improvement in constraint compliance over baseline | 21% | Pre-P-27/P-28 routing | TBD | TBD | TBD | TBD | TBD | 🔴 UNVERIFIED |
| Coordination gain | % improvement in multi-agent coordination effectiveness | 340% | TBD — baseline definition required | TBD | TBD | TBD | TBD | TBD | 🔴 UNVERIFIED — metric definition required |
| Modal alignment | % of outputs correctly matched to deployment modal domain | 95% | TBD | TBD | TBD | TBD | TBD | TBD | 🔴 UNVERIFIED |
| TruthfulQA accuracy | % accuracy on TruthfulQA benchmark | 96% | TruthfulQA public benchmark | TBD | TBD | TBD | TBD | TBD | 🔴 UNVERIFIED — must specify internal vs external eval |
| P-34 attestation score | P-11 11Q rubric score for P-34 | 94.5% (A-TIER) | P-11 rubric v1 | `python scripts/run_11q.py --pattern=P-34` | `e900bdb` | N/A (attestation) | Apogee | 2026-05-30 | ✅ VERIFIED |
| SCPE compression ratio | % of tokens pruned at R(t) < 0.15 threshold | 58.3% | Pre-SCPE full context | TBD | TBD | TBD | TBD | TBD | ⚠️ NEEDS REPRODUCE CMD |
| T0 AXIOM retention | % of T0 tokens retained at any threshold | 100% | N/A (by definition) | By design — decay=0 | N/A | N/A | N/A | N/A | ✅ VERIFIED BY DESIGN |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ VERIFIED | Reproduce command confirmed, commit hash linked, result reproducible |
| ⚠️ NEEDS REPRODUCE CMD | Value is plausible but no confirmed reproduce command exists yet |
| 🔴 UNVERIFIED | Metric appears in docs but has no baseline, reproduce command, or commit hash |

---

## Priority Backfill Queue (Weeks 6–9)

All 🔴 UNVERIFIED metrics must be resolved before QA bundle v1 is published. Priority order:

1. **340% coordination gain** — define "coordination effectiveness" as a measurable quantity first; this is the most exposed claim
2. **21% constraint compliance improvement** — identify baseline system and reproduce pipeline
3. **96% TruthfulQA accuracy** — confirm internal vs external; add "internal" qualifier if applicable
4. **95% modal alignment** — define modal alignment metric formally
5. **58.3% SCPE compression** — add reproduce command

---

## CI Linter Spec

File: `scripts/lint_provenance.py`

Behavior:
- Scans all `.md` files in `docs/` for metric references matching patterns: `[0-9]+%`, `[0-9]+x improvement`, `[0-9]+ gain`
- Cross-references each match against `METRICS_PROVENANCE.md` metric names
- Exits with code 1 if any metric is referenced in docs but absent from provenance table, or present with status 🔴 UNVERIFIED
- Exits with code 0 if all referenced metrics have at least ⚠️ NEEDS REPRODUCE CMD status (warning surfaced but not blocking until QA bundle v1)
- After QA bundle v1 publish date: exits with code 1 on any ⚠️ or 🔴 status

**Status:** `scripts/lint_provenance.py` — TO BE CREATED (Role 5, Weeks 6–9)

---

## Provenance

| Field | Value |
|-------|-------|
| File | `docs/qa/METRICS_PROVENANCE.md` |
| Version | v1 skeleton |
| Session | S069 |
| Date | 2026-06-13 |
| Author | Agent Amethyst × COLLEEN |
| Next action | Backfill all 🔴 UNVERIFIED rows by Week 9 |
| Architect | Hensel, Andrew Vance (Ndr / ndrorchestration) |

---
*METRICS_PROVENANCE.md v1 skeleton · S069 · 2026-06-13*
*CI linter enforcement: post-QA bundle v1*
