# Expert Panel Consensus Framework (EPCF)
## Amethyst Resonance Governance (ARG) Authority & Work Division

**Authority:** Agent Amethyst (Tribunal)  
**Steward:** COLLEEN (continuity)  
**Last Updated:** 2026-07-09  

---

## I. EXPERT PANEL COMPOSITION

### Panel Members (6 Experts + 1 Tribunal)

| Expert | Discipline | Role | Authority Level | Signature Pattern |
|--------|-----------|------|------------------|-------------------|
| **Dr. Lyapunov** | Control Theory & Stability | Verify dV/dt < 0; bifurcation calibration | Verifier (L3) | Formal proof + test suite |
| **Dr. Byzantine** | Distributed Consensus & Fault Tolerance | PBFT-Raft hybrid design; outlier detection | Verifier (L3) | Protocol spec + adversarial tests |
| **Dr. Epistemic** | Logic & Justification Systems | Contradiction detection; evidence graphs | Verifier (L3) | Formal semantics + case studies |
| **Dr. Entropy** | Information Theory & Coherence | Diversity-coherence bounds; entropy metrics | Verifier (L3) | Mathematical proofs + calibration data |
| **Dr. Mechanism** | Game Theory & Incentives | Incentive alignment; Nash equilibrium verification | Verifier (L3) | Strategic analysis + simulation results |
| **Dr. Merkle** | Provenance & Cryptography | Audit trail integrity; Merkle tree design | Verifier (L3) | Hash chain proofs + tamper detection tests |
| **Agent Amethyst** | Meta-Orchestrator & Tribunal | Final authority; consensus synthesis; escalation | Orchestrator (L2) | Seal + commitment |

---

## II. CONSENSUS PROTOCOL (7-Step Byzantine Agreement)

### Steps 1–3: Expert Independent Review
1. **Expert receives work unit** → produces findings + confidence score (0–100)
2. **Findings logged** → `docs/expert_reviews/[EXPERT]_[WORKUNIT]_REVIEW.md`
3. **Confidence threshold:** all experts ≥ 70% or escalate to Tribunal

### Steps 4–6: Consensus Building
4. **COLLEEN synthesizes** → identifies agreement zones + disagreements
5. **Disagreement zones escalated** → Tribunal (Amethyst) reviews + decides
6. **Amendment** → disputed expert revises finding or accepts Tribunal decision

### Step 7: Seal & Commit
7. **Amethyst commits** → `EXPERT_CONSENSUS_SEAL_[DATE].md` → GitHub commit

---

## III. WORK DIVISION MATRIX

### Phase 0: Research & Formalization (Parallel, No Dependencies)

| Work Unit | Primary Expert(s) | Deliverable | Confidence Target | Deadline |
|-----------|-------------------|-------------|-------------------|----------|
| **Q1: Lyapunov Stability** | Dr. Lyapunov + Dr. Entropy | `AHG_LYAPUNOV_STABILITY.md` + proof | 95% | Sprint 1 W3 |
| **Q2: Bifurcation Calibration** | Dr. Lyapunov + Dr. Mechanism | `BIFURCATION_CALIBRATION.md` + data | 90% | Sprint 1 W3 |
| **Q10: Diversity-Coherence** | Dr. Entropy + Dr. Mechanism | `DIVERSITY_COHERENCE_FORMALIZATION.md` | 85% | Sprint 1 W2 |
| **Q3: Contradiction Detection** | Dr. Epistemic + Dr. Entropy | `EPISTEMIC_CONTRADICTION_DETECTION.md` | 80% | Sprint 1 W4 |
| **Q4: Coherence Metrics** | Dr. Entropy + Dr. Epistemic | `COHERENCE_METRICS.md` | 85% | Sprint 1 W2 |

### Phase 1: Core Layers (Sequential Dependencies)

| Layer | Primary Expert | Dependencies | Deliverable | Confidence Target |
|-------|----------------|--------------|-------------|-------------------|
| **Layer 0 (ADG)** | Dr. Mechanism | Q10 (Entropy) | `amethyst_adg.py` + tests | 90% |
| **Layer 2 (Epistemic)** | Dr. Epistemic | Q3, Q4 | `epistemic_integrity_layer.py` | 85% |
| **Layer 3 (Byzantine)** | Dr. Byzantine | — | `hybrid_pbft_raft.py` + sim | 95% |
| **Layer 4 (Provenance)** | Dr. Merkle | Q8 | `merkle_attestation_tree.py` | 90% |
| **Layer 5 (Stability)** | Dr. Lyapunov | Q1, Q2 | `gmsm_lyapunov.py` + tests | 95% |

### Phase 2–3: Advanced & Verification (Depends on Phase 1)

| Work Unit | Primary Expert(s) | Deliverable | Confidence Target |
|-----------|-------------------|-------------|-------------------|
| **Q11: Phase Prediction** | Dr. Lyapunov + Dr. Entropy | `ahg_phase_predictor.py` | 85% |
| **Q13: Formal Verification** | Dr. Epistemic + Dr. Byzantine | `ARG_FORMAL_SPEC.tla` | 90% |
| **Q9: Incentive Analysis** | Dr. Mechanism + Dr. Entropy | `INCENTIVE_COMPATIBILITY_ANALYSIS.md` | 80% |

---

## IV. CONSENSUS HANDLING: Dispute Resolution

### Disagreement Escalation Path

**Level 1 (Expert-to-Expert):** 
- Experts with <5% confidence gap negotiate directly (max 2 turns)
- Record in `EXPERT_CONSENSUS_LOG.md`

**Level 2 (COLLEEN Mediation):**
- Gap ≥5%: COLLEEN identifies common ground + proposes amendment
- Amendment accepted if both experts ≥70% confidence

**Level 3 (Amethyst Tribunal):**
- Gap ≥10% or amendment fails: Amethyst decides
  - **Decision criterion:** which finding maximizes φ stability + epistemic integrity + collective good (J function)
  - **Authority:** Tribunal decision is final; binding on all experts

### Example: Bifurcation Calibration Dispute

- **Dr. Lyapunov:** φ_crit = 1.618 (80% confidence)
- **Dr. Entropy:** φ_crit = 1.642 (75% confidence) — 5% gap
- **COLLEEN:** proposes φ_crit ∈ [1.618, 1.642] with empirical calibration sweep
- **Both experts:** accept at 85% confidence
- **Outcome:** Calibration work unit proceeds with confidence range; Amethyst seals

---

## V. FINE DETAILS & INTEGRATION RULES

### Rule 1: Cross-Expert Dependency Tracking
- COLLEEN maintains `EXPERT_DEPENDENCY_GRAPH.md` → prevent circular wait
- If Q1 (Lyapunov) blocks Phase 1, escalate automatically to Tribunal

### Rule 2: Hybrid Method Reconciliation
- When multiple methods conflict (e.g., Lyapunov vs. game-theoretic control):
  - Create `HYBRID_METHOD_RECONCILIATION_[ID].md`
  - Document both approaches; Tribunal picks or synthesizes
  - Example: "Lyapunov + incentive-compatible control hybrid" (Dr. Lyapunov + Dr. Mechanism)

### Rule 3: Evidence Quality Tiers
- **Tier A (Gold):** Formal proof + empirical validation + >90% expert confidence
- **Tier B (Silver):** Formal proof OR empirical validation + >80% confidence
- **Tier C (Bronze):** Theoretical justification + >70% confidence
- Work units must reach Tier B minimum before Phase 1 start

### Rule 4: Delta Updates & Amendments
- If expert discovers flaw post-consensus:
  - Create `AMENDMENT_[EXPERT]_[DATE].md` → detailed correction
  - Amethyst re-seals if confidence impact <5%; otherwise re-review
  - No retroactive log edits; all changes append-only (immutable)

### Rule 5: Individual Accountability & Hybrid Credit
- Each expert signs their section in deliverable
- Hybrid sections list all contributors: "Dr. Lyapunov + Dr. Entropy (shared)"
- COLLEEN maintains contributor matrix for attestation (P-30 Gold Star)

---

## VI. CONSENSUS LOG & SEALING

### Session Checkpoints (COLLEEN Managed)

| Checkpoint | Trigger | Output | Owner |
|------------|---------|--------|-------|
| **Review Complete** | All experts submit findings | `EXPERT_REVIEWS_COMPILED_[ID].md` | COLLEEN |
| **Consensus Ready** | Confidence ≥70% or dispute resolved | `EXPERT_CONSENSUS_READY_[ID].md` | COLLEEN |
| **Tribunal Seal** | Amethyst approves | `EXPERT_CONSENSUS_SEAL_[ID].md` | Amethyst |
| **Implementation** | Developers code deliverables | GitHub commits tagged `[expert-panel-id]` | Dev Team |

### Immutable Log Structure
```
docs/expert_consensus/
├── EXPERT_CONSENSUS_MASTER_LOG.md (append-only)
├── EXPERT_REVIEWS/
│   ├── LYAPUNOV_Q1_STABILITY_REVIEW.md
│   ├── BYZANTINE_LAYER3_REVIEW.md
│   └── ...
├── DISPUTES_RESOLVED/
│   └── DISPUTE_BIFURCATION_CALIBRATION_20260709.md
├── SEALS/
│   └── EXPERT_CONSENSUS_SEAL_20260709_PHASE0.md
└── AMENDMENTS/
    └── AMENDMENT_LYAPUNOV_Q1_20260712.md
```

---

## VII. SUCCESS CRITERIA & COMPLETION DEFINITION

### Phase 0 (Research) Complete When:
- [ ] All 5 research units (Q1, Q2, Q10, Q3, Q4) ≥80% confidence tier
- [ ] COLLEEN synthesizes consensus document
- [ ] Amethyst seals Phase 0
- [ ] Zero unresolved disagreements (all disputes resolved or Tribunal decided)

### Phase 1 (Layers) Complete When:
- [ ] All 5 layers (ADG, Epistemic, Byzantine, Provenance, Stability) ≥85% confidence
- [ ] Integration tests passing (all layers communicate correctly)
- [ ] Amethyst seals Phase 1
- [ ] Ready for Phase 2

### Full ARG Orchestration Complete When:
- [ ] Phases 0–3 sealed by Amethyst
- [ ] Formal verification (TLA+) passes all specs
- [ ] Multi-agent end-to-end tests ≥95% success rate
- [ ] Attestation chain (Merkle tree) verified immutable
- [ ] P-43 through P-50 (ARG patterns) added to registry
- [ ] Amethyst multi-agent consensus orchestration live

---

## VIII. IMMEDIATE ACTION ITEMS (Next 48 Hours)

1. **Create expert review kickoff** → Email/notify each expert of assigned units
2. **Set up consensus logging** → Create `docs/expert_consensus/` directory structure
3. **COLLEEN configures tracking** → `EXPERT_DEPENDENCY_GRAPH.md` + `EXPERT_CONSENSUS_MASTER_LOG.md`
4. **Amethyst prepares sealing workflow** → GitHub action: auto-tag commits `[expert-panel-id]`
5. **Schedule dispute resolution meetings** → Weekly (Thursdays 14:00 UTC) if needed

---

**Framework Authority:** Agent Amethyst (Tribunal)  
**Consensus Ratified:** 2026-07-09  
**Version:** ARG-EPCF v1.0  
*Next review: Post-Phase-0 completion*
