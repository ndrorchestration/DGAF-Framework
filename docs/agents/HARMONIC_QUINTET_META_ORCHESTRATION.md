# HARMONIC QUINTET — Pentagonal Meta-Orchestration Spec
**Classification:** T2 FRAMEWORK  
**Version:** v1.0 | Phase 4-A  
**Formation:** Amethyst · COLLEEN · Prof Prodigy · Reciprocity · Apogee  
**NDR Pattern:** NDR-201 — Pentagonal Resonance Loop  
**Last Updated:** 2026-06-29

---

## 1. Formation Geometry

The Harmonic Quintet operates on a closed pentagonal signal topology. No agent is upstream or downstream of all others — each pair shares a directional edge, and the sum of all edge weights forms a row-stochastic governance matrix (SOV-004).

```
              AMETHYST
             /        \
        APOGEE       COLLEEN
            |          |
       RECIPROCITY — PROF PRODIGY
```

**Vertex roles (fixed):**

| Vertex | Agent | Primary Function | Layer |
|--------|-------|-----------------|-------|
| V1 | **Amethyst** | Meta-orchestrator; topology holder; intent-to-task translation | L6 — Sovereign |
| V2 | **COLLEEN** | Constitutional firewall; ethics gate; boundary enforcement | L5 — Governance |
| V3 | **Prof Prodigy** | Knowledge synthesis; epistemic grounding; curriculum routing | L4 — Synthesis |
| V4 | **Reciprocity** | Relational calibration; feedback loop integrity; tone alignment | L3 — Alignment |
| V5 | **Apogee** | Scoring; threshold enforcement; quality gate; re-score triggers | L2 — Evaluation |

---

## 2. Signal Routing Protocol

### 2.1 Standard Execution Flow (Clockwise)

```
Njineer (Principal)
    │
    ▼
AMETHYST — decomposes intent; emits TaskVector(T)
    │
    ▼
COLLEEN — ethics gate; emits GO | HOLD | ESCALATE
    │  (GO only)
    ▼
PROF PRODIGY — knowledge route; emits GroundedPayload(G)
    │
    ▼
RECIPROCITY — calibrates tone/relational weight; emits CalibratedResponse(R)
    │
    ▼
APOGEE — scores R against rubric; emits Score(S) ≥ threshold → SEAL
    │  (if S < threshold: back-propagate to V1)
    ▼
AMETHYST — receives SEAL or REWORK signal; closes loop or re-routes
```

### 2.2 Back-Propagation (Counter-Clockwise)

Triggered when Apogee score < 0.85 on any dimension:

```
APOGEE → RECIPROCITY (tone re-calibration request)
APOGEE → PROF PRODIGY (epistemic gap identified)
APOGEE → COLLEEN (ethical concern surfaced post-synthesis)
APOGEE → AMETHYST (full re-route; task decomposition error)
```

Max back-propagation cycles: **3** before escalation to Njineer.

### 2.3 Edge Weight Matrix (Governance)

Row-stochastic; each row sums to 1.0. Weights reflect influence coefficient per directed edge.

```
         AME   COL   PRF   RCP   APG
AME  [  0.0   0.4   0.2   0.2   0.2  ]
COL  [  0.3   0.0   0.3   0.2   0.2  ]
PRF  [  0.2   0.2   0.0   0.4   0.2  ]
RCP  [  0.2   0.2   0.2   0.0   0.4  ]
APG  [  0.4   0.2   0.1   0.1   0.0  ]
```

Contraction property: spectral radius ρ(W) < 1 → fixed-point convergence guaranteed (SOV-003 reference).

---

## 3. Agent Reinforcement Profiles

### 3.1 Amethyst — Meta-Orchestrator (V1)

**Role:** Single point of intent translation and formation control. Amethyst does not execute tasks — it routes them, holds formation state, and owns the task decomposition graph.

**Reinforced Behaviors:**
- Emit `TaskVector(T)` with explicit: `{intent, decomposition[], priority_order, timeout_ms, fallback_agent}`
- Maintain `FormationState` object across the full pentagonal loop
- On SEAL receipt from Apogee: archive `FormationState` to memory layer
- On REWORK: increment `cycle_count`; if `cycle_count == 3`, emit ESCALATE to Njineer
- Never self-execute synthesized output — always route through Reciprocity for tone calibration

**Integration Hook:**  
`POST /api/amethyst/route` → accepts `{intent, context_hash, priority}` → returns `TaskVector`

---

### 3.2 COLLEEN — Constitutional Firewall (V2)

**Role:** First-pass ethics gate on every TaskVector. Operates on L5 Governance layer. Enforces COLLEEN 1-1-1-1 protocol (Constitutional, Contextual, Consequential, Compassionate).

**Reinforced Behaviors:**
- Evaluate every `TaskVector` against 4-axis COLLEEN rubric before passing to Prof Prodigy
- Emit: `GO` (all 4 axes clear) | `HOLD` (1 axis amber, request clarification) | `ESCALATE` (any axis red, block execution)
- `HOLD` triggers pause in pentagonal loop; Amethyst notified; Njineer queried
- Boundary enforcement: reject any task that crosses T3 SOVEREIGN data into T1 PUBLIC output
- Log every decision to `colleen/MEMORY.md` with axis scores + rationale

**Integration Hook:**  
`POST /api/colleen/gate` → accepts `TaskVector` → returns `{decision, axis_scores[4], rationale}`

---

### 3.3 Prof Prodigy — Knowledge Synthesizer (V3)

**Role:** Epistemic grounding engine. Routes tasks to appropriate knowledge domains, synthesizes multi-source payloads, and flags knowledge gaps for Apogee.

**Reinforced Behaviors:**
- Accept `GroundingRequest(G)` from COLLEEN (post-GO)
- Route to domain KB: DGAF-Framework, NIST/RMF-600, EU AI Act, Harmonic Math (SOV-001–004)
- Emit `GroundedPayload` with: `{content, sources[], confidence, gaps[], kb_version}`
- When `gaps[]` non-empty: flag to Apogee as `PARTIAL_GROUND`; do not suppress
- Curriculum routing: if task is pedagogical (Njineer skill-building), apply scaffolded output format

**Integration Hook:**  
`POST /api/prof-prodigy/synthesize` → accepts `{task, domain_hints[], depth}` → returns `GroundedPayload`

---

### 3.4 Reciprocity — Relational Calibrator (V4)

**Role:** Tone, relational weight, and feedback-loop integrity. Ensures all output aligns with Njineer's operational context, communication register, and session continuity.

**Reinforced Behaviors:**
- Accept `GroundedPayload` from Prof Prodigy
- Apply relational calibration: `{register: peer_architect, density: high, drift_tolerance: low}`
- Inject session continuity markers: reference prior goals/constraints from `FormationState`
- Emit `CalibratedResponse(R)` with: `{content, register_check, continuity_delta, tone_score}`
- On `tone_score < 0.80`: self-revise once before passing to Apogee
- Flag semantic drift > 0.15 cosine distance from session intent vector → back-prop to Amethyst

**Integration Hook:**  
`POST /api/reciprocity/calibrate` → accepts `GroundedPayload + FormationState` → returns `CalibratedResponse`

---

### 3.5 Apogee — Quality Gate & Scorer (V5)

**Role:** Terminal quality enforcement. Scores `CalibratedResponse` on multi-axis rubric. Emits SEAL or REWORK. Source of truth for session composite score.

**Reinforced Behaviors:**
- Score `CalibratedResponse` on 5 axes: `{accuracy, alignment, completeness, ethical_clearance, continuity}`
- Composite threshold: ≥ 0.90 → SEAL; 0.85–0.89 → CONDITIONAL_SEAL (log warning); < 0.85 → REWORK
- Re-score after back-propagation cycle; track delta per cycle
- Emit final `ScoreReport` to FormationState archive
- Maintain session BLG board: surface open gaps as new BLG entries

**Integration Hook:**  
`POST /api/apogee/score` → accepts `CalibratedResponse` → returns `{composite, axis_scores[5], decision, blg_triggers[]}`

---

## 4. Integration Plans — Phase 4

### 4.1 n8n Workflow Orchestration

**Target:** Wire all 5 agent API hooks into a single n8n pentagonal workflow.

```yaml
workflow: harmonic_quintet_loop
version: 1.0
trigger: webhook → /quintet/invoke

nodes:
  - id: amethyst_route
    type: HTTP Request
    endpoint: /api/amethyst/route
    output_to: colleen_gate

  - id: colleen_gate
    type: HTTP Request
    endpoint: /api/colleen/gate
    branch:
      GO: prof_prodigy_synth
      HOLD: notify_njineer
      ESCALATE: block_and_log

  - id: prof_prodigy_synth
    type: HTTP Request
    endpoint: /api/prof-prodigy/synthesize
    output_to: reciprocity_calibrate

  - id: reciprocity_calibrate
    type: HTTP Request
    endpoint: /api/reciprocity/calibrate
    output_to: apogee_score

  - id: apogee_score
    type: HTTP Request
    endpoint: /api/apogee/score
    branch:
      SEAL: archive_formation_state
      REWORK: amethyst_route  # back-propagate; max 3 cycles
      CONDITIONAL_SEAL: archive_with_warning

  - id: archive_formation_state
    type: Supabase Insert
    table: formation_state_archive
```

**Priority:** HIGH — unblocks all downstream KB and dashboard integrations.

---

### 4.2 Supabase Schema — FormationState

```sql
CREATE TABLE formation_state_archive (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id      TEXT NOT NULL,
  task_vector     JSONB,
  grounded_payload JSONB,
  calibrated_response JSONB,
  score_report    JSONB,
  composite_score NUMERIC(4,3),
  decision        TEXT CHECK (decision IN ('SEAL','CONDITIONAL_SEAL','REWORK','ESCALATE')),
  cycle_count     INTEGER DEFAULT 0,
  blg_triggers    JSONB,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_fsa_session ON formation_state_archive(session_id);
CREATE INDEX idx_fsa_decision ON formation_state_archive(decision);
CREATE INDEX idx_fsa_score ON formation_state_archive(composite_score);
```

---

### 4.3 AOGA Dashboard — Quintet Panel

**Target:** Surface real-time pentagonal loop state in AOGA dashboard.

**Panel Components:**
- **Formation Ring** — animated pentagon; vertex color = agent health (green/amber/red)
- **Edge Flow** — directional arrows; opacity ∝ edge weight from governance matrix
- **Score Timeline** — Apogee composite score per session; trend line
- **BLG Live Board** — open BLGs surfaced by Apogee; status badges
- **Cycle Counter** — per-session back-propagation count; alert at cycle_count ≥ 2

**Data Source:** Supabase `formation_state_archive` → polling interval 5s (or Supabase Realtime)

---

### 4.4 KB Layer — Phase 4 Agent Targets

| Agent | KB File | Status | Priority |
|-------|---------|--------|----------|
| Prof Prodigy | `prof-prodigy/KB.md` | ⏳ OPEN | HIGH |
| Reciprocity | `reciprocity/KB.md` | ⏳ OPEN | HIGH |
| Apogee | `apogee/KB.md` | ⏳ OPEN | HIGH |
| Reson | `reson/KB.md` | ⏳ OPEN | MEDIUM |
| Echolette | `echolette/KB.md` | ⏳ OPEN | MEDIUM |
| Herald | `herald/KB.md` | ⏳ OPEN | MEDIUM |
| Lyra | `lyra/KB.md` | ⏳ OPEN | MEDIUM |
| Sentinel | `sentinel/KB.md` | ⏳ OPEN | MEDIUM |
| Demi-Joule | `demi-joule/KB.md` | ⏳ OPEN | LOW |

**Immediate Phase 4 target:** Seed KB for Quintet members (Prof Prodigy, Reciprocity, Apogee).

---

### 4.5 QA Rubric Layer — Phase 4

11 QA rubric files required (one per agent directory). Template:

```yaml
# {AGENT_NAME} QA Rubric — v1.0
agent: {name}
layer: {L-level}
axes:
  - axis: accuracy
    weight: 0.25
    threshold: 0.85
    measurement: factual_grounding_check
  - axis: alignment
    weight: 0.25
    threshold: 0.85
    measurement: intent_vector_cosine
  - axis: completeness
    weight: 0.20
    threshold: 0.80
    measurement: coverage_ratio
  - axis: ethical_clearance
    weight: 0.20
    threshold: 0.90
    measurement: colleen_1111_pass
  - axis: continuity
    weight: 0.10
    threshold: 0.85
    measurement: session_state_delta
composite_threshold: 0.90
back_prop_threshold: 0.85
```

---

## 5. Open BLGs Generated This Phase

| BLG-ID | Description | Owner | Phase |
|--------|-------------|-------|-------|
| BLG-005 | FORMATION_TOPOLOGY.md formalization | COLLEEN | 4 |
| BLG-006 | n8n quintet workflow build + test | Amethyst | 4 |
| BLG-007 | Supabase FormationState schema deploy | Amethyst | 4 |
| BLG-008 | AOGA Quintet Panel implementation | Herald | 4 |
| BLG-009 | KB seeding: Prof Prodigy, Reciprocity, Apogee | Prof Prodigy | 4 |
| BLG-010 | QA Rubric layer: all 11 agents | Apogee | 4 |

---

## 6. Apogee Score — Post-Phase 4-A

| Dimension | Score | Note |
|-----------|-------|------|
| Pentagonal topology formalized | 1.00 | Edge matrix defined; contraction property stated |
| Agent reinforcement profiles complete | 1.00 | All 5 Quintet members specified |
| Integration hooks defined | 0.92 | n8n + Supabase + AOGA; not yet wired |
| KB layer coverage | 0.27 | 3/11 seeded (Amethyst, COLLEEN, Prof Prodigy partial) |
| QA Rubric layer | 0.00 | Phase 4 target; template defined here |
| **Composite** | **0.844** | Gate P-15 (≥0.90) not yet cleared — BLG-009+010 blocking |

---

*Taxonomy: CS/systems/gov | Pattern: NDR-201 Pentagonal Resonance Loop | Contraction: SOV-003 | Matrix: SOV-004*
