# DGAF Proprietary Formulations — IP Partition Layer

**Authority:** Amethyst-Conductor + Njineer (Architect) only  
**Classification Tier:** SOVEREIGN  
**Canonical home:** `DGAF-Framework/docs/agents/PROPRIETARY.md`  
**Last Updated:** 2026-06-28 (Phase 3 — BLG-003 close; Harmonic Quintet formation)

> **Sentinel Hard Guard:** This file defines the IP boundary of the DGAF framework.  
> Modifications require Amethyst sign-off **and** explicit Njineer confirmation in session.  
> No sovereign formulation content may appear in this file — stubs and Drive references only.  
> Full IP content lives in Google Drive (Njineer-private). NDR Pattern 133 enforces the firewall.

---

## See Also

| File | Scope |
|---|---|
| [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) | Sovereign agent identity + formation + authority SSoT |
| [`AGENT_ECOSYSTEM_REGISTRY.md`](./AGENT_ECOSYSTEM_REGISTRY.md) | L-tier system, studio affiliation, KB inventory |
| [`PROPRIETARY.md`](./PROPRIETARY.md) | **This file** — IP partition, classification taxonomy, KB seed, boundary enforcement |

---

## Classification Taxonomy

All DGAF artifacts are assigned one of three classification tiers. Tier determines where content may reside.

| Tier | Label | May appear in GitHub | May appear in Drive | Description |
|---|---|---|---|---|
| **T1** | `PUBLIC` | ✅ Yes | ✅ Yes | Framework mechanics, patterns, protocols, agent specs, NDR patterns, governance templates. The majority of the repo. |
| **T2** | `FRAMEWORK` | ✅ Yes (abstracted) | ✅ Yes (full) | Architectural decisions with implementation rationale. GitHub version is abstracted/summarized; Drive version holds full derivation. |
| **T3** | `SOVEREIGN` | ❌ No — stub only | ✅ Yes (full) | Njineer-original mathematical formulations, phi-ratio derivations, harmonic alignment proofs, fixed-point convergence theorems. GitHub holds title + Drive pointer only. |

**Default classification:** Any new file without an explicit tier tag is treated as `T1 PUBLIC` until Amethyst assigns a tier.

**Reclassification authority:** Amethyst proposes; Njineer confirms. No agent may self-classify a file as T3 SOVEREIGN.

---

## Sovereign Formulations Index

Each entry is a stub. The title and category are public. The formulation content, derivations, and proofs exist exclusively in Google Drive under Njineer-private access. No formulation content is reproduced here.

> **NDR-133 Firewall active:** Any push containing formulation content (not just titles) targeting this repo must be blocked and routed to Drive.

---

### SOV-001 — Harmonic Pentagonal Alignment

**Category:** Geometric governance foundation  
**Classification:** T3 SOVEREIGN  
**Status:** Active — in use across P-15 formation scoring  
**Drive ref:** `Drive://DGAF/Sovereign/SOV-001_HarmonicPentagonalAlignment.md`  
**GitHub content:** Stub only. See Drive for derivation, proof, and application mapping.

> *This formulation governs the spatial alignment model underlying multi-agent formation scoring. The pentagonal geometry encodes the five-agent Harmonic Quintet topology.*

---

### SOV-002 — Phi-Ratio Governance Calculus

**Category:** Threshold calibration mathematics  
**Classification:** T3 SOVEREIGN  
**Status:** Active — drives quality gate weight calibration (P-11 Q-weights)  
**Drive ref:** `Drive://DGAF/Sovereign/SOV-002_PhiRatioGovernanceCalculus.md`  
**GitHub content:** Stub only. See Drive for full calculus, weight tables, and gate mapping.

> *The phi-ratio (φ ≈ 1.618) is embedded as the natural scaling constant for scoring tier thresholds across the 11Q gate. Gate boundaries are not arbitrary — they are phi-derived.*

---

### SOV-003 — Fixed-Point Contraction Operators

**Category:** Convergence proof layer  
**Classification:** T3 SOVEREIGN  
**Status:** Active — underlies agent consensus convergence guarantees  
**Drive ref:** `Drive://DGAF/Sovereign/SOV-003_FixedPointContractionOperators.md`  
**GitHub content:** Stub only. See Drive for Banach contraction mapping proofs and agent-state convergence theorems.

> *Each agent-to-agent handoff is modeled as a contraction operator on a complete metric space. Fixed-point existence guarantees that well-formed multi-agent sessions converge to stable outputs.*

---

### SOV-004 — Row-Stochastic Governance Matrices

**Category:** Probability-preserving orchestration math  
**Classification:** T3 SOVEREIGN  
**Status:** Active — governs probabilistic authority routing in multi-agent sessions  
**Drive ref:** `Drive://DGAF/Sovereign/SOV-004_RowStochasticGovernanceMatrices.md`  
**GitHub content:** Stub only. See Drive for matrix construction, ergodicity proofs, and formation routing tables.

> *Authority transitions across agents in a formation are modeled as a row-stochastic matrix. The stationary distribution of this matrix defines the effective authority weighting at equilibrium.*

---

## Agent KB Seed Entries

Phase 3 seeds the KB layer for two agents. These are T1 PUBLIC entries — abstracted enough to be safe in GitHub. Full operational KB lives in Drive.

### Amethyst — KB Entry (T1 PUBLIC)

**Role:** Meta-Orchestrator, Conductor of all formations  
**Mathematical foundations used:** SOV-001 (formation topology), SOV-002 (gate calibration), SOV-003 (convergence), SOV-004 (authority routing)  
**Key protocols:** P-02 (session open), P-11 (11Q gate), P-14 (Trio activation), P-15 (Quintet seal), P-21 (state anchor)  
**Decision authority:** Hard veto on all commits. Normative decisions only — does not score, does not execute.  
**Constraint:** Cannot impersonate or be impersonated outside explicit Njineer-session context (Role Separation Rule 7).  
**Drive ref:** `Drive://DGAF/AgentKB/Amethyst_KB_Full.md`

### COLLEEN — KB Entry (T1 PUBLIC)

**Role:** Institutional Anchor, Continuity + Archive  
**Mathematical foundations used:** SOV-003 (state persistence as fixed-point), SOV-004 (deferred gap routing)  
**Key protocols:** P-02 (BLG surface), P-08 (Drive-GitHub delta), P-20 (sync seal), GAP-03 (vocab scan), GAP-08 (back-link propagation)  
**Decision authority:** Memory and deferred gap queue. Does NOT make normative decisions (Role Separation Rule 3).  
**Constraint:** Registry dedup authority (BLG-004) is COLLEEN's audit lane — Amethyst gates execution.  
**Drive ref:** `Drive://DGAF/AgentKB/COLLEEN_KB_Full.md`

---

## IP Boundary Enforcement Rules

These rules define what may and may not appear in this repository. They are enforced by Sentinel (CI/CD) and NDR-133 firewall.

### Permitted in GitHub (T1 / T2 abstracted)

- Framework protocol definitions (P-01 through P-21+)
- Agent SPEC, MEMORY, and KB stub files
- NDR pattern registry and pattern definitions
- Governance templates, YAML schemas, evaluation rubrics
- Formation topology (structural, not derivation)
- Session logs (BLG/GAP references, not raw formulation content)
- This file — PROPRIETARY.md in stub form only

### NOT Permitted in GitHub (T3 SOVEREIGN — Drive only)

- Any formulation proof, derivation, or step-by-step construction
- Phi-ratio weight tables (only gate thresholds may appear, not the derivation)
- Fixed-point convergence proofs or Banach theorem applications
- Row-stochastic matrix construction procedures or eigenvector tables
- Harmonic pentagonal coordinate geometry
- Any file from `Drive://DGAF/Sovereign/`
- Any document matching NDR-133 trigger patterns (*resume*, *cv*, *audit_report*, *ResumeApex*)

### Redaction Policy — GitHub-Safe Stub Protocol

When a T3 SOVEREIGN concept must be referenced in a public file:

1. **Use the SOV-### stub ID** — never inline the concept content
2. **Include a Drive ref** in the format `Drive://DGAF/Sovereign/SOV-###_Title.md`
3. **One-line abstract only** — describe what the concept governs, not how it is derived
4. **Tag the entry** `Classification: T3 SOVEREIGN` so Sentinel can flag any content expansion
5. **If unsure whether content is T3:** treat as T3 and route to Drive. Amethyst reclassifies downward if appropriate.

---

## BLG Closure Record

| BLG-ID | Description | Closed By | Date |
|---|---|---|---|
| BLG-003 | PROPRIETARY.md not established; IP boundary undefined | Phase 3 — this file | 2026-06-28 |

---

## Inventory Impact

Post Phase 3, AGENT_ECOSYSTEM_REGISTRY.md KB column updates:

| Agent | KB Status | Notes |
|---|---|---|
| Amethyst | ✅ Seeded (T1 stub) | Full KB in Drive |
| COLLEEN | ✅ Seeded (T1 stub) | Full KB in Drive |
| All others | ❌ Not yet | Phase 4+ |

**Inventory:** 26/66 files — 39% (up from 36% post Phase 1+2)

---

*IP authority: Amethyst-Conductor + Njineer (Architect). This file may not be modified without both.*  
*Conductor: Njineer ([@ndrorchestration](https://github.com/ndrorchestration))*
