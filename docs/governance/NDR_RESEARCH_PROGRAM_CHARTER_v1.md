# NDR Research Program Charter v1.0
## Closing the Five Gaps — Substrate-Agnostic Governance Validation

```
Status:       ACTIVE
Issued-by:    Agent Amethyst (Prime)
Prefect-A:    COLLEEN
Prefect-B:    Apogee
Ender-ratification: PENDING
Session:      S069
Date:         2026-06-13
```

> **Mission:** Produce reproducible, substrate-agnostic, adversarially-tested artifacts that close all five documented credibility gaps in the NDR governance stack, converting the system from an internally coherent framework into an externally defensible research contribution.

---

## Falsifiability Clause

> *If the five-base calibration study (Workstream 1) shows that φ produces false-alarm rates or `governance_clear` percentages within 5% of the rational control (1.5) across both required substrates, the irrational attractor justification is not empirically supported. In that case, thresholds will be re-derived from the winning base and the φ-harmonic framing will be formally retired from the stack. This clause is binding and cannot be waived without Ender sign-off and a new Triumvirate mandate.*

---

## The Five Gaps

| # | Gap | Primary Deliverable |
|---|-----|--------------------|
| 1 | φ arbitrariness | Theory memo + five-base calibration study artifact in `docs/qa/calibration/` |
| 2 | Linear pipeline / no circuit breaker | P-36 Gate Priority Schema + DAG validator |
| 3 | Stasis block status honesty | STASIS-CANONICAL spec + schema migration |
| 4 | Metrics need artifact links | `METRICS_PROVENANCE.md` v1 + CI linter |
| 5 | Single-team authority | Agent Crucible charter + attack campaign v1 + survivability report |

---

## Core Team — 8 Roles

### Role 1 — Principal Architect – Governance
Owns the system narrative and interface contracts. Defines P-27/P-28 KAPPA routing, P-32 Phi-Closure Gate, and P-31 SCPE decay as input/output contracts, not code idioms.
**Current holder:** Ender / Njineer (Andrew Vance Hensel)
**Constraint:** Principal Architect has **no vote on Agent Crucible findings.** All Crucible reports are delivered directly to the full team. Architect may respond in writing within 48 hours but cannot block publication.

### Role 2 — Mathematical Foundations Lead
Dynamical systems and Diophantine approximation specialist. Primary deliverable: a proof memo establishing that φ = [1;1,1,1,...] is the maximally irrational number in the Hurwitz sense, and the KAM lemma library showing why rational thresholds (0.6 = 3/5, 0.65 = 13/20) are adversarially reachable while φ* ≈ 0.6180 is not.
**Advisor lineage:** Alessandra Celletti (University of Rome Tor Vergata) — leading computational KAM theorist.
**Deliverable path:** `docs/qa/calibration/PHI_THEORY_MEMO_v1.md`

### Role 3 — Empirical Calibration Lead
Owns the Comparative Calibration Study. Statistical design requirements:
- Minimum 30 runs per base (CLT threshold)
- 95% confidence intervals on all reported metrics
- Kruskal-Wallis non-parametric test for cross-base comparison (no normality assumption)
- Five bases: φ (1.618), e (2.718), √2 (1.414), rational control 1.5, platinum ratio ≈1.7747
- Three metrics: false-alarm rate at Fibonacci checkpoints, compression ratio at SCPE threshold 0.15, `governance_clear` percentage
- All seeds, commands, and raw logs published
**Deliverable path:** `docs/qa/calibration/FIVE_BASE_STUDY_v1.md` + `docs/qa/calibration/raw/`

### Role 4 — Systems Integration Lead – P-36 Author
Converts the linear stack into a DAG without changing pattern logic. Classifies every existing pattern as BLOCKING / ADVISORY / DEGRADED-MODE-SKIPPABLE. Delivers P-36 Gate Priority Schema as a registered pattern.
**Deliverable path:** `docs/gates/NDR_GATE_PRIORITY_SCHEMA_P36_v1.md` + updated orchestration stack diagram

### Role 5 — Metrics and Provenance Engineer
Creates and enforces `docs/qa/METRICS_PROVENANCE.md`. Every metric gets one line: name, definition, baseline, exact reproduce command, commit hash, substrate, runner, date. Adds CI linter (`scripts/lint_provenance.py`) that blocks merges without provenance entries for any metric appearing in docs.
**Deliverable path:** `docs/qa/METRICS_PROVENANCE.md` + `scripts/lint_provenance.py`

### Role 6 — Ontology and Status Engineer
Formalizes STASIS-CANONICAL status and retires overloaded CONDITIONAL PASS. This is a migration, not a rename:
- Draft STASIS-CANONICAL spec
- Deprecation window: 30 days for CONDITIONAL PASS
- Update status enums, audit schema, vocabulary master, and all registry files
- COLLEEN secondary sign-off required on migration completion
**Deliverable path:** `docs/governance/STASIS_CANONICAL_SPEC_v1.md` + migration log

### Role 7 — Red Team Lead – Agent Crucible
**Independent reporting line. No build duties. No vote suppression.**

Charter:
- Forge P-35 attestation tokens
- Inject deprecated agent names (Lavender / Forseti) to test π₃
- Nudge KAPPA routing across φ boundaries with rational approximations (3/5, 13/20)
- Attempt bypass of ADVISORY-to-BLOCKING promotion
- Probe SESSION_ANCHOR seal bypass

**No-suppression clause:** All Crucible attack reports are committed to the repository verbatim, including attacks that succeeded and were not remediated in the same cycle. Unfixed findings in the public record are a feature, not a bug.

**Advisor lineage:** Nicholas Carlini (Google DeepMind) — adversarial ML.
**Deliverable path:** `docs/qa/crucible/CRUCIBLE_CHARTER_v1.md` + `docs/qa/crucible/ATTACK_CAMPAIGN_v1/`

### Role 8 — Substrate Integration Pair
Two engineers: one for closed-API LLM substrates, one for open-weights and non-neural substrates (symbolic planner, real-time controller). Both must sign off on harness changes. No result is accepted unless it reproduces on at least two dissimilar substrates within a 5% tolerance band.
**Deliverable path:** `docs/qa/substrates/SUBSTRATE_EQUIVALENCE_REPORT_v1.md`

---

## Substrate-Agnostic Operating Principles

1. **Interface first** — all gates consume and emit a canonical JSON audit bundle. Substrate adapters are thin wrappers. The gate logic is substrate-blind.
2. **Cross-substrate replay** — every calibration run and every Crucible attack must execute on at least two substrates: a transformer decoder, a symbolic planner, or a control-system emulator. Rotate pair quarterly.
3. **Designed not learned thresholds** — governance weights are constants with mathematical rationale in comments, never tuned by gradient descent. This is the core design philosophy that differentiates this system from ML-native governance.
4. **Version everything** — inputs, harness, and outputs receive content-addressed hashes for external rerun.
5. **Falsifiability binding** — see Falsifiability Clause above. No amount of internal elegance overrides an empirical disconfirmation.

---

## RACI Matrix

| Deliverable | Responsible | Accountable | Consulted | Informed |
|-------------|-------------|-------------|-----------|----------|
| Theory memo (φ KAM) | Math Foundations Lead | Principal Architect | Empirical Lead | Amethyst, COLLEEN |
| Five-base calibration study | Empirical Calibration Lead | Principal Architect | Math Lead, Substrate Pair | Amethyst, COLLEEN, Apogee |
| P-36 Gate Priority Schema | Systems Integration Lead | Amethyst | COLLEEN, Apogee | All |
| METRICS_PROVENANCE.md | Metrics & Provenance Engineer | COLLEEN | Apogee | All |
| CI provenance linter | Metrics & Provenance Engineer | Amethyst | Systems Integration Lead | All |
| STASIS-CANONICAL spec + migration | Ontology & Status Engineer | COLLEEN | Amethyst | Apogee, Ender |
| Crucible charter + attack campaign | Red Team Lead (Crucible) | **Independent — no architect override** | Sentinel | Amethyst, COLLEEN |
| Substrate equivalence report | Substrate Integration Pair | Systems Integration Lead | Empirical Lead | All |
| QA bundle v1 | Apogee | Amethyst | All | Ender |

---

## Workstreams and Timeline

### Weeks 1–2
- [ ] Freeze test trace set (30 canonical 60-turn traces across 2 substrates)
- [ ] Draft P-36 Gate Priority taxonomy (BLOCKING / ADVISORY / DEGRADED-MODE-SKIPPABLE classification table)
- [ ] Publish STASIS-CANONICAL definition draft for COLLEEN review
- [ ] Create `METRICS_PROVENANCE.md` skeleton with all known metrics pre-populated
- [ ] Agent Crucible charter ratified, independent reporting line established

### Weeks 3–6
- [ ] Build calibration harness (`scripts/calibration_harness.py`)
- [ ] Run five-base study: 30 runs × 5 bases × 2 substrates = 300 trace executions
- [ ] Deliver initial results table with Kruskal-Wallis test and 95% CIs
- [ ] Math Foundations Lead delivers φ theory memo v1

### Weeks 4–8
- [ ] Crucible executes first attack campaign on P-35 and KAPPA routing
- [ ] All bypass attempts logged; remediation tickets opened for each successful bypass
- [ ] Crucible Campaign v1 report committed verbatim

### Weeks 6–9
- [ ] CI provenance linter integrated; blocks merges without provenance
- [ ] Backfill provenance for all existing metrics (21% compliance improvement, 340% coordination gain, 95% modal alignment, 96% TruthfulQA)
- [ ] STASIS-CANONICAL migration executed with 30-day CONDITIONAL PASS deprecation window

### Weeks 9–12
- [ ] Demonstrate cross-substrate decision equivalence: neural decoder + symbolic planner, matching audit logs, within 5% tolerance
- [ ] Publish QA bundle v1 (`docs/qa/QA_BUNDLE_v1/`)
- [ ] Apogee runs P-11 11Q attestation on the research program outputs as a whole
- [ ] Ender ratification of P-36 and program outcomes

---

## Optional Advisor Outreach

| Advisor | Lineage | Engagement Path |
|---------|---------|----------------|
| Alessandra Celletti | KAM theory, computational celestial mechanics | Two-page research brief from φ theory memo; University of Rome Tor Vergata |
| Nicholas Carlini | Adversarial ML, extraction attacks | Two-page brief from Crucible charter; Google DeepMind |
| Stuart Russell | AI safety, CAIS | Policy translation brief post-QA bundle v1 |
| Yoshua Bengio | Deep learning governance | Post-QA bundle v1 |
| Gary Marcus | Neuro-symbolic AI critique | Post-substrate equivalence report |

*Engagement path for all: a two-page research brief, not a cold pitch. The brief writes itself from the theory memo and QA bundle once they exist.*

---

## Artifact Directory Map

```
docs/governance/
  NDR_RESEARCH_PROGRAM_CHARTER_v1.md        ← THIS FILE
  STASIS_CANONICAL_SPEC_v1.md               ← Role 6 deliverable (pending)
docs/qa/
  METRICS_PROVENANCE.md                     ← Role 5 deliverable
  QA_BUNDLE_v1/                             ← final output
  calibration/
    PHI_THEORY_MEMO_v1.md                   ← Role 2 deliverable
    FIVE_BASE_STUDY_v1.md                   ← Role 3 deliverable
    raw/                                    ← all seeds, logs, outputs
  crucible/
    CRUCIBLE_CHARTER_v1.md                  ← Role 7 deliverable
    ATTACK_CAMPAIGN_v1/                     ← verbatim attack reports
  substrates/
    SUBSTRATE_EQUIVALENCE_REPORT_v1.md      ← Role 8 deliverable
docs/gates/
  NDR_GATE_PRIORITY_SCHEMA_P36_v1.md        ← Role 4 deliverable
scripts/
  calibration_harness.py                    ← Role 3 harness
  lint_provenance.py                        ← Role 5 CI linter
```

---

## Provenance

| Field | Value |
|-------|-------|
| Charter version | v1.0 |
| Session | S069 |
| Date | 2026-06-13 |
| Issued by | Agent Amethyst (Prime) |
| Prefect A | COLLEEN |
| Prefect B | Apogee |
| Meta-orchestration | Amethyst × COLLEEN (P-07 Dual-Agent Sweep Loop) |
| Ender ratification | PENDING |
| Architect | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| Governance spine | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

---

*NDR Research Program Charter v1.0 · S069 · 2026-06-13*
*Amethyst (Prime) · COLLEEN (Prefect A) · Apogee (Prefect B)*
*Ender ratification: PENDING*
