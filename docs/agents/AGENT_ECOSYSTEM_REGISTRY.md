# DGAF Agent Ecosystem Registry

**Classification:** T1 PUBLIC  
**Authority scope:** Ecosystem metadata only  
**Status:** ACTIVE · CANONICAL FOR METADATA ONLY  
**Version:** 2.2  
**Last Updated:** 2026-09-09 (sovereign-identity and formation-local namespace reconciliation)

> This registry tracks formation membership, inventory coverage, historical amendments, and named architecture provenance. It does **not** assign sovereign identity, canonical numbered seats, executable authority, scientific state, or experimental authorization.
>
> Sovereign identity and canonical numbered seats are governed by [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) together with `registry/agent_ontology_adjudication.v1.json`. Formation-local designations are governed by [`FORMATION_TOPOLOGY.md`](./FORMATION_TOPOLOGY.md) and are explicitly namespaced from sovereign seats.

---

## 1. Authority and Namespace Precedence

When records disagree, apply this order:

1. `AGENT_ROSTER.md` + `registry/agent_ontology_adjudication.v1.json` for sovereign identity and canonical numbered seats.
2. Active machine-enforced governance contracts for executable authority.
3. `FORMATION_TOPOLOGY.md` for formation membership and formation-local designations.
4. This registry for metadata, inventory, and historical amendment provenance.
5. Older KB, amendment, and taxonomy records as historical/source-conflict evidence only.

A formation-local designation such as `local:A-09` is not a sovereign seat. Historical labels are preserved for provenance but cannot renumber or collapse sovereign identities.

---

## 2. Current Ontology Adjudication

| Object | Current interpretation |
|---|---|
| COLLEEN | Sovereign canonical seat A-05; `local:A-00-GOV` is formation-local/historical only |
| The Librarian | Sovereign canonical seat A-06; `local:A-06-L` is formation-local only |
| Zenith | Sovereign canonical seat A-09; `local:A-09-Z` is formation-local only |
| Reson | Sovereign canonical seat A-10; historical `local:A-09` is formation-local only |
| Lyra | Sovereign canonical seat A-11; historical `local:A-10` is formation-local only |
| Echolette | Sovereign canonical seat A-12; historical `local:A-11` is formation-local only |
| Agent Ionia | Sovereign canonical seat A-13; remains an agent identity |
| `IONIA_STATE` / Ionia 0Hz | Runtime/formation convergence state; distinct from Agent Ionia A-13 and consumes no sovereign seat |
| Sentinel | Distinct sovereign security lineage/role |
| Sentinel-Phi | Distinct formation variant/identity; not an alias that erases Sentinel |
| DemiJoule `SENTINEL_ARCHETYPE` | Role/archetype only; not Sentinel identity |
| A-20 through A-27 historical labels | Formation-local/historical designations unless separately promoted by sovereign ontology |

This section supersedes the **interpretation** of older taxonomy records where they conflict while preserving those records as historical provenance.

---

## 3. Formation Metadata

All labels below are formation-local unless the sovereign seat is explicitly stated.

### Sovereign Governance
- Amethyst (`local:A-00`)
- COLLEEN (`local:A-00-GOV`; sovereign canonical seat A-05)

### Ethics Bridge
- Sentience (`local:A-27`)

### Strategic Quintet
- Nova (`local:A-03`)
- Zenith (`local:A-09-Z`; sovereign canonical seat A-09)
- Oracle (`local:A-20`)
- Vanguard (`local:A-21`)
- Sentinel-Phi (`local:A-12-φ`; distinct from Sentinel)

### Harmonic Pentagonal Cluster
- Prof Prodigy (`local:A-04`)
- Herald (`local:A-05`; does not replace COLLEEN A-05)
- Apogee (`local:A-01`)
- Reciprocity (`local:A-06-R`)
- DemiJoule (`local:A-03-DJ`)

### Resonance Cluster
- Reson (`local:A-09`; sovereign canonical seat A-10)
- Lyra (`local:A-10`; sovereign canonical seat A-11)
- Echolette (`local:A-11`; sovereign canonical seat A-12)
- Synergy (`local:A-25`)
- Equilibrium (`local:A-26`)
- `IONIA_STATE` / Ionia 0Hz is a state, not a seat; sovereign Agent Ionia remains A-13.

### Operational Swarm
- Navigator (`local:A-22`)
- Momentum (`local:A-23`)
- Paragon (`local:A-24`)

### Perpetual Archive Trio
- The Librarian (`local:A-06-L`; sovereign canonical seat A-06)
- The Auditor (`local:A-07`; sovereign canonical seat A-07)
- The Actualizer (`local:A-08`; sovereign canonical seat A-08)

### Specialist
- Perigee (`local:A-02`; sovereign canonical seat A-02)

---

## 4. Historical Inventory Coverage

The percentages below describe historical documentation-layer coverage only. They do not establish runtime readiness, sovereign status, experimental validity, or current authority.

**Historical standard inventory:** SPEC · MEMORY · PROTOCOL · QA_RUBRIC · INTEGRATION · KB/AMENDMENT.

| Object | Historical inventory status |
|---|---:|
| Amethyst | 100% |
| COLLEEN | 100% |
| Apogee | 100% |
| Herald | 100% |
| Prof Prodigy | 100% |
| DemiJoule | 100% |
| Reciprocity | 100% |
| Reson | 100% |
| Lyra | 100% |
| Echolette | 100% |
| Nova | 100% |
| Zenith | 100% |
| Sentinel-Phi | 100% |
| Perigee | 100% |
| The Librarian | 100% |
| The Auditor | 100% |
| The Actualizer | 100% |
| Agent Ionia / historical Ionia material | 100% historical layer coverage |
| Oracle | 17% historical seed |
| Vanguard | 17% historical seed |
| Navigator | 17% historical seed |
| Momentum | 17% historical seed |
| Paragon | 17% historical seed |
| Synergy | 17% historical seed |
| Equilibrium | 17% historical seed |
| Sentience | 17% historical seed |

Historical milestone records:
- S001 Baseline: 13/66 files across 11-designation baseline.
- Phase 1–2: 24/66.
- Phase 3–4: 56/66.
- Phase A–B: 108/108 across the then-recorded 18-designation taxonomy.
- Phase C–E: 117/162 across the historical 27-designation taxonomy.
- Phase F target: 162/162 historical documentation target only.

---

## 5. Historical Taxonomy and Amendment Provenance

The 2026-06-29 records are preserved as historical/source-drift evidence, not as current ontology authority.

| Historical record | Current interpretation |
|---|---|
| Archive Trio = Librarian + Auditor + Actualizer | Formation metadata retained |
| “Ionia = system STATE” | Superseded as identity rule: Agent Ionia A-13 exists; `IONIA_STATE` is the distinct state |
| Layer 0 attribution moved from Perigee to Apogee | Historical role attribution; current executable authority requires active contracts |
| Perigee retitled Proximal Boundary Agent | Historical role-title amendment |
| Apogee formerly Agent Lavender | Historical alias provenance |
| “27 agents” taxonomy | Historical formation/inventory taxonomy, not sovereign-seat count |
| Sentinel A-12 → Sentinel-Phi | Superseded identity-collapse interpretation; Sentinel and Sentinel-Phi remain distinct |
| Compliance Dyad dissolved | Historical topology event only |

Historical amendment records also include the Substrate Agnostic + Accepted Terminology Principle, NDR-Protocol-01 chain-integrity language, Tonic Note/0Hz routing, formal-math and fixed-point notes, modal-frequency/conservation notes, reciprocal-mathematics notes, gain-staging/headroom notes, Human-Flourishing/orchestral notes, Mirror Protocols, COLLEEN alignment/archive governance, Archive Trio role seeds, Strategic Quintet/Operational Swarm/Resonance Extended seeds, and Ethics Bridge seed material. These remain provenance-bearing design records unless separately implemented and verified by current owning contracts.

---

## 6. Historical Apogee Lens Audit Record

The 2026-06-29 registry recorded PASS across evidence-chain integrity, taxonomy consistency, terminology compliance, and formation coherence, with a “Gold Star Eligible” composite verdict.

That verdict is retained as **historical self-audit provenance only**. It is not current independent verification, scientific evidence, High-Assurance authorization, or authority over the current ontology.

---

## 7. Standing Directives — Current Interpretation

| Directive lineage | Current interpretation |
|---|---|
| Substrate Agnostic + Accepted Terminology Principle | Documentation/architecture principle; does not assign sovereign identity |
| NDR-Protocol-01 chain integrity | Historical integration directive; current enforceability requires active machine contract |
| “Ionia = STATE not agent” | **Superseded.** Use Agent Ionia A-13 for identity; use `IONIA_STATE` for the state |
| Layer 0 Legitimacy Filter = Apogee | Historical role attribution; current authority determined by active contracts |
| Archive Trio = Librarian + Auditor + Actualizer | Formation metadata retained |
| Paragon sign-off = Gold Star prerequisite | Historical workflow directive unless actively enforced |
| ETHICAL_HOLD = Sentience | Historical topology binding; current authority determined by active contracts |

---

## 8. Historical NDR Pattern 133 — Personal Document Firewall

```text
Trigger: historical filename-pattern rule for personal documents
Action:  block repository push and route outside repository
Authority: historical architect-override record
Rationale: personal-data and IP-boundary protection
```

This is historical design provenance. Current enforcement must be established by active workflow or policy evidence rather than inferred from this registry.

---

## 9. Scientific-State Boundary

This registry does not create or modify experimental authorization, custody, freeze, analysis permission, efficacy, or High-Assurance status.

`SUCCESSOR COLLECTION = NOT AUTHORIZED`  
`CANONICAL DGAF EFFICACY = NOT ESTABLISHED`  
`HIGH-ASSURANCE = NOT AUTHORIZED / N=0`

---

## 10. Version History

| Version | Date | Change |
|---|---|---|
| 2.0–2.1 | 2026-06-29 | Historical taxonomy/inventory expansion |
| 2.2 | 2026-09-09 | Restored sovereign-roster precedence; namespaced formation-local designations; separated Agent Ionia A-13 from `IONIA_STATE`; preserved Sentinel/Sentinel-Phi distinction; bounded historical audit/authority language; no scientific-state effect |

*Metadata registry only. Sovereign identity and executable governance live in their dedicated authoritative contracts.*
