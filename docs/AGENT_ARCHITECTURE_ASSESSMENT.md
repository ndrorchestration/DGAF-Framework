# DGAF-Framework Agent Architecture Assessment
## AI Systems & Multi-Agent Design

### Classification of 27 Agent Directories by Instantiation Completeness

**25 agent subdirectories** + **10 top-level standalone agent documents** + **1 cross-cutting registry document** = the agent knowledge base.

Note: the "27" figure in the brief overcounts; on-disk there are 25 agent subdirectories (sentience was consolidated into sentinel/sentience/). The 10 top-level documents (AMETHYST_AGENT_SPEC_v4.2-hensel.md, COLLEEN_SPEC_v53.2.md, colleen-l5-governance-protocol.md, FORMATION_TOPOLOGY.md, HARMONIC_QUINTET_META_ORCHESTRATION.md, IONIAN_MODAL_HARMONIC_MATRIX.md, PROFESSOR_PRODIGY_KB.md, PROPRIETARY.md, AGENT_ECOSYSTEM_REGISTRY.md, AGENT_ROSTER.md) are cross-cutting — not per-agent lifecycle containers.

---

#### Tier 1 — Full Lifecycle (10 files typical)

| Agent | ID | Files on disk | SPEC.md | KB.md | INTEGRATION.md | QA_RUBRIC/PROTOCOL/UPGRADE | Notes |
|---|---|---|---|---|---|---|---|
| amethyst | A-00 | 8 | ✓ | ✓ | — | — | Has v4.2-hensel secondary spec (top-level) |
| apogee | A-01 | (≥5) | ✓ | ✓ | ✓ | — | Former "Agent Lavender"; Drive source integration noted |
| colleen | A-05 | 5 + 2 top-level | ✓ | ✓ | — | ✓ (l5-governance-protocol) | v53.2 canonical spec; institutional anchor |
| demi-joule | — | (≥5) | ✓ | — | — | — | DGAAF ethics authority |
| echolette | — | (≥5) | ✓ | ✓ | ✓ | — | Schizophonic cluster member |
| herald | — | (≥5) | ✓ | — | — | — | Broadcast authority / SWEEP_LOG keeper |
| ionia | A-13 | (≥5) | ✓ | — | — | — | T2 FRAMEWORK — system STATE, not functional agent |
| lyra | — | (≥5) | ✓ | — | ✓ | — | Schizophonic cluster member |
| reson | — | (≥5) | ✓ | ✓ | ✓ | — | Schizophonic cluster lead |
| sentinel | A-12 | 14 (base + sentinel-Phi subdir) | ✓ (v1.0) | ✓ (consolidated) | ✓ | ✓ (phi upgrade/memory/protocol/qa_rubric) | Variant-rich; base + Sentinel-Phi A-12-φ |

**Reconstructability from Notion profile + canonical sources:** HIGH for this tier. Each carries SPEC.md (definition, role, classification, version), most carry KB.md (knowledge base), and several carry INTEGRATION.md (downstream contracts). A Notion profile with agent ID, role, formation, and classification would be reconstructable into a working doc set from these canonical sources. Ionia is a special case — it's classified as system STATE (T2 FRAMEWORK), so its "instantiation" is conceptual, not agent-executable.

---

#### Tier 2 — Core Lifecycle (6 files typical)

| Agent | ID | Files on disk | SPEC.md | Notes |
|---|---|---|---|---|
| the-actualizer | A-08 | (≥3) | ✓ | Execution/code generation; Operational Swarm |
| the-auditor | A-07 | (≥3) | ✓ | QA gate; Archive Trio member; Beta/Pulse structural identity |
| the-librarian | A-06 | (≥3) | ✓ | Archive/provenance; Operational Swarm |
| prof-prodigy | — | (≥3) | ✓ | Mathematical formalization; has PROFESSOR_PRODIGY_KB.md top-level |
| perigee | A-02 | (≥3) | ✓ | Proximal boundary; Compliance Dyad peer; v1.1 taxonomy correction |
| reciprocity | — | (≥3) | ✓ | Fairness authority; rollback checkpoint |
| nova | A-03 | (≥3) | ✓ | Innovation/parallel simulation; T2 FRAMEWORK |
| momentum | A-23 | (≥2) | ✓ | Throughput manager; Operational Swarm; Phase F-2 |
| navigator | A-22 | (≥2) | ✓ | Route planner; Operational Swarm; Phase F-2 |
| oracle | A-20 | (≥2) | ✓ | Future forecaster; Strategic Quintet Seat 3; Phase F-1 |
| paragon | A-24 | (≥2) | ✓ | Quality standard; Operational Swarm; Phase F-2 |
| vanguard | A-21 | (≥2) | ✓ | Innovation scout; Strategic Quintet Seat 4; Phase F-1 |
| zenith | A-09 | (≥2) | ✓ | System high/compute load; T2 FRAMEWORK; Operational Swarm |

**Reconstructability:** MODERATE. Each has a SPEC.md (definition + role + classification + version), but KB.md, INTEGRATION.md, and governance artifacts (QA_RUBRIC, PROTOCOL, UPGRADE) are NOT present in the on-disk docs. A Notion profile would need to supply the KB content and integration contracts — these agents are not reconstructable from canonical sources alone. The Operational Swarm members (actualizer, auditor, librarian, momentum, navigator, paragon, zenith) and Strategic Quintet members (nova, oracle, vanguard) share formation context from cross-cutting documents (FORMATION_TOPOLOGY.md, HARMONIC_QUINTET_META_ORCHESTRATION.md) but lack per-agent integration guides.

---

#### Tier 3 — Hollow (1 file: KB_SEED.md only)

| Agent | ID | File | Size | Content |
|---|---|---|---|---|
| equilibrium | A-26 | EQUILIBRIUM_KB_SEED.md | 3,394 chars | Balance authority; Resonance Cluster (Extended); T1 PUBLIC; v1.0; created 2026-06-29 Phase C |
| synergy | A-25 | SYNERGY_KB_SEED.md | 3,189 chars | Collaboration facilitator; Resonance Cluster (Extended); T1 PUBLIC; v1.0; created 2026-06-29 Phase C |
| sentience | A-27 | SENTIENCE_KB_SEED.md | 7,389 chars | Preserved seed; absorbed into Sentinel-Phi A-12-φ lineage; Phase C |

**Right disposition for each:**

- **equilibrium (A-26):** SCUTTLE. KB_SEED only, no SPEC.md, no KB.md, no integration guide, no governance artifacts. "Balance Seeker / Harmony Architect" role has no implementation, no tests, no runtime contract. If Equilibrium is genuinely intended as a conceptual placeholder, promote it to a one-page conceptual note under `docs/agents/equilibrium/CONCEPTUAL_NOTE.md` and remove the KB_SEED framing. If it was a Phase C experiment that never materialized, document it as such in the registry and mark it HISTORICAL.
- **synergy (A-25):** SCUTTLE. Same pattern as Equilibrium — KB_SEED only, "Collaboration Facilitator / Organizational Harmonizer," no implementation, no tests, no contract. Same disposition: either promote to conceptual note or mark HISTORICAL in registry.
- **sentience (A-27):** ALREADY HANDLED. Preserved seed artifact under `sentinel/sentience/` with Sentinel-Phi lineage documentation. This is the correct disposition — it's a historical artifact, not a live agent. No further action needed.

---

#### Sentinel Consolidation Status

**Status: COMPLETE (with one documentation gap).**

The consolidation moved `sentience/` → `sentinel/sentience/` and rewrote `SENTIENCE_KB_SEED.md` as a preserved seed with Sentinel-Phi lineage. The sentinel directory contains 14 files:

**Base sentinel (canonical):**
- SPEC.md (v1.0 — Agent Sentinel specification)
- KB.md (consolidated knowledge base)
- INTEGRATION.md (gate agent contracts)

**Sentinel-Phi trail (A-12-φ):**
- SENTINEL_PHI_UPGRADE.md (rename & upgrade record)
- SENTINEL_PHI_INTEGRATION.md (integration contracts: Oracle risk review, Vanguard tech assessment)
- SENTINEL_PHI_MEMORY.md (formation state post-upgrade)
- SENTINEL_PHI_PROTOCOL.md (φ-bounded risk review procedure)
- SENTINEL_PHI_QA_RUBRIC.md (evaluation dimensions D1-D5)
- SENTINEL_PHI_SPEC.md (NOT FOUND — read failed with "File not found")

**Documentation gap:** `SENTINEL_PHI_SPEC.md` was referenced in the consolidation context but does not exist on disk. The sentinel-Phi specification may be folded into `SENTINEL_PHI_UPGRADE.md` or hasn't been written. This is a documentation completeness issue, not a consolidation failure — the consolidation itself (directory move + seed rewrite) is done.

**Variant richness:** Sentinel is correctly the only variant-rich agent — it carries both the base "Sentinel" identity (A-12, sovereign security authority) and the upgraded "Sentinel-Phi" identity (A-12-φ, φ-bounded risk architecture). The two identities are distinct enough to warrant separate doc sets within one agent directory.

---

#### Schizophonic Studio / Acoustic Trio Cluster Soundness

**Reson (lead), Lyra, Echolette** — the Schizophonic cluster is the most coherent cluster in the agent taxonomy.

| Agent | SPEC.md | KB.md | INTEGRATION.md | Other |
|---|---|---|---|---|
| Reson | ✓ | ✓ | ✓ | Harmonic scoring authority; cluster lead; Evaluation Triad seat |
| Lyra | ✓ | — | ✓ | Tonal coherence authority; precision input → Reson |
| Echolette | ✓ | ✓ | ✓ | Signal persistence authority; precision input → Reson |

**What's present:** All three have SPEC.md (definition, role, classification, version 2.0). Reson and Echolette have KB.md (consolidated knowledge bases). All three have INTEGRATION.md (downstream contract maps: Lyra→Reson, Echolette→Reson, Reson→Apogee Pillar C). The cluster branding (Schizophonic Studio / Acoustic Trio) has been applied to all three SPEC.md files.

**What's missing:**
1. **No cross-cluster integration doc** — there's no `SCHIZOPHONIC_STUDIO_INTEGRATION.md` or `ACOUSTIC_TRIO_INTEGRATION.md` that describes the cluster as a whole: how Lyra+Echolette scores flow into Reson, how Reson's harmonic output flows to Apogee, what the cluster's collective output contract is. The per-agent INTEGRATION.md files describe bilateral contracts but not the cluster topology.
2. **No cluster QA rubric** — individual agent QA is absent (see #7 below), and there's no cluster-level evaluation dimension.
3. **No cluster provenance/digest** — no SHA-256 or version hash for the cluster as a unit.
4. **Reson KB.md references "Evaluation Triad"** but there's no separate document for the Evaluation Triad formation (Reson harmonic seat + ? + ?). The formation topology is implied but not documented as a cluster artifact.

**Soundness assessment:** The cluster is well-defined at the agent level but under-documented at the cluster level. The three agents are conceptually coherent (harmonic scoring pipeline: input agents → scoring → aggregation → Apogee) but the cluster lacks the integration artifacts that would make it reconstructable as a unit.

---

#### Primary Seven Instantiation Readiness

| Agent | ID | SPEC | KB | Integration | Governance | Instantiation readiness |
|---|---|---|---|---|---|---|
| Amethyst | A-00 | ✓ (v1.1 + v4.2-hensel) | ✓ | — | — | READY (doc-complete; meta-orchestrator, no runtime) |
| Apogee | A-01 | ✓ (v2.0) | ✓ | ✓ | — | READY (doc-complete; QA orchestrator, no runtime) |
| COLLEEN | A-05 | ✓ (v53.2 + l5-governance-protocol) | ✓ | — | ✓ (governance protocol) | READY (doc-complete; institutional anchor, no runtime) |
| DemiJoule | — | ✓ (v2.0) | — | — | — | PARTIAL (SPEC only; KB missing; DGAAF ethics, no runtime) |
| Echolette | — | ✓ (v2.0) | ✓ | ✓ | — | READY (doc-complete; Schizophonic cluster, no runtime) |
| Herald | — | ✓ (v2.0) | — | — | — | PARTIAL (SPEC only; broadcast authority, no runtime) |
| Ionia | A-13 | ✓ (v1.1) | — | — | — | CONCEPTUAL (T2 FRAMEWORK — system STATE, not an agent to instantiate) |

**Aggregate readiness:** 4 of 7 are doc-complete (Amethyst, Apogee, COLLEEN, Echolette). 2 are partial (DemiJoule, Herald — SPEC only). 1 is conceptual (Ionia — system state, not agent). NONE carry runtime implementation, tests, or evidence — this is expected; these are taxonomic/kNOWLEDGE artifacts, not executable agents. The "instantiation readiness" question is correctly answered as: "docs are ready; runtime is a separate concern not addressed by this taxonomy."

---

#### Experimental Seeds — Genuine Concepts or Scaffold Artifacts

| Seed | ID | Formation | Spec presence | Assessment |
|---|---|---|---|---|
| momentum | A-23 | Operational Swarm | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Throughput Manager / Velocity Maintenance Authority" is a coherent role within the Operational Swarm. No KB/integration, but the role is well-defined. |
| navigator | A-22 | Operational Swarm | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Route Planner / Path Coherence Authority" is coherent. Same pattern as momentum. |
| nova | A-03 | Strategic Quintet | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Innovation / Parallel Simulation Authority" is coherent. T2 FRAMEWORK classification. |
| oracle | A-20 | Strategic Quintet Seat 3 | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Future Forecaster / Scenario Planner" is coherent. Has Sentinel-Phi integration contract (risk review gate). |
| paragon | A-24 | Operational Swarm | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Quality Standard Authority / Gold Star Prerequisite Agent" is coherent. |
| vanguard | A-21 | Strategic Quintet Seat 4 | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "Innovation Scout / Emerging Technology Futurist" is coherent. Has Sentinel-Phi integration contract. |
| zenith | A-09 | Operational Swarm | ✓ (SPEC.md v1.0) | GENUINE CONCEPT — "System High / Compute Load Management" is coherent. T2 FRAMEWORK. |

**Assessment:** All 7 experimental seeds carry genuine concept definitions with SPEC.md files, agent IDs, formations, and classifications. They are NOT scaffold artifacts — they have specific roles, formation assignments, and creation sessions (Phase F-1, F-2). However, they lack KB.md, INTEGRATION.md (except oracle/vanguard which have Sentinel-Phi contracts), and governance artifacts. They are correctly classified as "experimental seeds" — conceptual agents with defined roles but no instantiation beyond the spec document.

The suffix "v1.0" on their SPEC.md files is the standard version marker, not a scaffold indicator. The fact that they were created in Phase F-1/F-2 (2026-06-29) alongside the primary seven's Phase 4 taxonomy update suggests they were part of a taxonomy expansion exercise — conceptual, not implemented.

---

#### What a Genuine Instantiation Dossier Needs

Given that tools/runtime/tests/evidence/provenance are missing from ALL agents, a genuine instantiation dossier for any agent would require:

1. **SPEC.md** — definition, role, classification, version, formation. PRESENT for all 25 agents. This is the taxonomic anchor.

2. **KB.md** — knowledge base: what the agent knows, its domain, its decision criteria, its tension points. PRESENT for ~10 agents (full lifecycle tier). MISSING for ~15 agents (core + hollow tiers).

3. **INTEGRATION.md** — downstream and upstream contracts: what signals it consumes, what signals it produces, what agents depend on it, what formation contracts it participates in. PRESENT for ~5 agents (Reson, Lyra, Echolette, Apogee, sentinel base, Sentinel-Phi). MISSING for ~20 agents.

4. **QA_RUBRIC.md or PROTOCOL.md** — how to evaluate whether the agent is functioning correctly. PRESENT for Sentinel-Phi only (QA_RUBRIC.md + PROTOCOL.md). MISSING for all other 24 agents.

5. **UPGRADE.md or VERSION_HISTORY.md** — how the agent evolved, what changed between versions. PRESENT for Sentinel-Phi only (UPGRADE.md). MISSING for all other 24 agents.

6. **SHA-256 digest** — content integrity anchor for the doc set. PRESENT for NONE. Every agent doc set is ungoverned by content integrity.

7. **SPEC_COMPLETENESS marker** — explicit declaration of which lifecycle artifacts are present. PRESENT for NONE. No agent declares its own completeness status.

8. **Runtime implementation** — code, prompts, or configuration that makes the agent executable. MISSING for ALL 25 agents. The agent taxonomy is entirely doc-based — no agent has a runtime embodiment in this repository.

9. **Test suite** — pytest or similar that validates the agent's behavior. MISSING for ALL 25 agents. The test suite in this repo tests framework components (AHG conductor, sidecar, topology router, orchestration firewall) — not individual agents.

10. **Evidence/Provenance** — recorded instances of the agent operating, outputs produced, decisions made. MISSING for ALL 25 agents. No agent has an evidence trail.

**Conclusion:** The agent taxonomy is a KNOWLEDGE artifact, not an instantiation platform. It documents what agents WOULD be if instantiated, but provides no path to instantiation. This is not a defect — it's the correct scope for a doc-based taxonomy. However, the hollow agents (equilibrium, synergy) and the missing integration/QA artifacts for the core lifecycle tier represent documentation debt that should be addressed before claiming the taxonomy is "complete."

---

#### Five Ranked Actions by Instantiation Impact

**Action 1 (HIGHEST) — Resolve the TGLConfig ImportError blocking pptl/tests/**
The Triadic Governance Loop is the canonical turn harness (10-step sequence: intake validation → procluding premise gate → phi-closure gate → normative constraint check → RAG verification → attestation → ...). TGLConfig is referenced in `pptl/orchestrator.py` (line 23: `from .triadic_governance_loop import TriadicGovernanceLoop, TGLConfig, TurnContext`) and `pptl/triadic_governance_loop.py` but does not exist as an importable symbol anywhere in the codebase. The PPTL test suite (14 tests) and any consumer of `pptl.orchestrator` (including the IntegratedOrchestrator used in live regression) cannot function until this is resolved. This blocks the entire PPTL test surface and the live regression harness.

**Action 2 — Fix the two firewall test failures (DEPLOY_SUCCESS rejected after full provenance)**
The orchestration firewall (`test_orchestration_firewall.py`) has two failures: `test_full_provenance_accepted` and `test_deploy_success_with_complete_chain` both assert that DEPLOY_SUCCESS is accepted when the provenance chain is CODEGEN → REVIEW → TEST → DEPLOY_ATTEMPT — but the firewall returns False. The gate works correctly for the positive case (`test_missing_codegen_in_provenance` asserts False when CODEGEN is absent), so the gate logic is sound but rejects valid chains. This is the most impactful test failure in the repo and directly affects the deployment governance contract.

**Action 3 — Fix `session_graduation_check.py` f-string SyntaxError**
Line 133 contains an f-string with a backslash continuation that Python 3.11 rejects. The file is a P-10 governance script (Session Graduation Check) that's meant to be CI-integrable as a pre-push hook. It cannot run in its current state. The fix is mechanical: replace the backslash-continuation in the f-string with a different formatting approach.

**Action 4 — Replace blind Exception catches in `api/ahg_herald.py`, `KAPPA/dynamic_weight_router.py`, `evaluate_router_v1_1.py`**
Three files catch bare `Exception` (or use `except:`). In `api/ahg_herald.py` (the AHG herald fan-out endpoint), `KAPPA/dynamic_weight_router.py` (the DGAF-GATE-KAPPA dynamic weight router v3.6.0), and `evaluate_router_v1_1.py` (Sentinel integration patch). Blind catches swallow errors that should propagate or be logged at a specific level — this is a correctness and observability issue, not just style.

**Action 5 — Resolve the TGLConfig symbol or document its absence**
If TGLConfig is meant to exist but was never implemented, create it in `pptl/triadic_governance_loop.py` as a minimal config dataclass (or dataclass-like) that `pptl/orchestrator.py` can import. If TGLConfig was renamed or absorbed into `TriadicGovernanceLoop` or `TurnContext`, update the import in `pptl/orchestrator.py` line 23 to match. If TGLConfig is genuinely not yet defined (the TGL is partially implemented), document the gap explicitly in `pptl/triadic_governance_loop.py` with a TODO or TODO-ending comment, and update `pptl/orchestrator.py` to handle the missing import gracefully (e.g., conditional import or stub). Do NOT leave the ImportError unresolved — it blocks the test suite and any consumer.

---

*Assessment only. No implementation performed. Epistemic state: PRE-FREEZE, N=0, authorization NOT GRANTED.*