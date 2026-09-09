# DGAF Agent Ecosystem Registry

**Classification:** T1 PUBLIC  
**Authority scope:** Ecosystem metadata only  
**Status:** ACTIVE · CANONICAL FOR METADATA ONLY  
**Version:** 2.2  
**Last Updated:** 2026-09-09 (sovereign-identity and formation-local namespace reconciliation)

> This registry tracks ecosystem metadata: formation membership, inventory coverage, historical amendments, and named architectural directives. It does **not** assign sovereign identity, canonical numbered seats, executable authority, or scientific state.
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

A formation-local designation such as `local:A-09` is not a sovereign seat. Historical labels are preserved where useful for provenance but cannot renumber or collapse sovereign identities.

---

## 2. Current Ontology Adjudication

The accepted 2026-09-09 ontology adjudication resolves the material conflicts carried by older taxonomy records.

| Object | Current interpretation |
|---|---|
| COLLEEN | Sovereign canonical seat A-05; `local:A-00-GOV` is a historical/formation-local designation only |
| The Librarian | Sovereign canonical seat A-06; `local:A-06-L` is formation-local only |
| Zenith | Sovereign canonical seat A-09; `local:A-09-Z` is formation-local only |
| Reson | Sovereign canonical seat A-10; historical `local:A-09` is formation-local only |
| Lyra | Sovereign canonical seat A-11; historical `local:A-10` is formation-local only |
| Echolette | Sovereign canonical seat A-12; historical `local:A-11` is formation-local only |
| Agent Ionia | Sovereign canonical seat A-13; remains an agent identity |
| `IONIA_STATE` / Ionia 0Hz | Runtime/formation convergence state; distinct from Agent Ionia A-13 and consumes no sovereign seat |
| Sentinel | Distinct sovereign security lineage/role |
| Sentinel-Phi | Distinct formation variant/identity; not an alias that erases Sentinel |
| DemiJoule Sentinel archetype | Role/archetype only; not Sentinel identity |
| A-20 through A-27 historical labels | Formation-local/historical designations only unless separately promoted by sovereign ontology |

This section supersedes the **interpretation** of the 2026-06-29 taxonomy corrections below where they conflict, while preserving those corrections as historical provenance.

---

## 3. See Also

| File | Scope |
|---|---|
| [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) | Sovereign identity and canonical numbered seats |
| [`FORMATION_TOPOLOGY.md`](./FORMATION_TOPOLOGY.md) | Formation specifications and local-designation namespace |
| `registry/agent_ontology_adjudication.v1.json` | Machine-readable ontology adjudication |
| [`PROPRIETARY.md`](./PROPRIETARY.md) | Historical/private IP partition records |

---

## 4. Formation Metadata

Labels below are formation-local where shown. They are not sovereign renumbering.

### Sovereign Governance formation

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
- Herald (`local:A-05`; this local label does not replace COLLEEN A-05)
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

## 5. Inventory Coverage

The inventory percentages below describe historical documentation-layer coverage. They do not establish runtime readiness, sovereign status, experimental validity, or current authority.

**Historical standard inventory:** SPEC · MEMORY · PROTOCOL · QA_RUBRIC · INTEGRATION · KB/AMENDMENT.

| Object | Formation metadata | Historical inventory status |
|---|---|---:|
| Amethyst | Sovereign Governance | 100% |
| COLLEEN | Sovereign Governance | 100% |
| Apogee | Harmonic Pentagonal | 100% |
| Herald | Harmonic Pentagonal | 100% |
| Prof Prodigy | Harmonic Pentagonal | 100% |
| DemiJoule | Harmonic Pentagonal | 100% |
| Reciprocity | Harmonic Pentagonal | 100% |
| Reson | Resonance / Studio | 100% |
| Lyra | Resonance / Studio | 100% |
| Echolette | Resonance / Studio | 100% |
| Nova | Strategic Quintet | 100% |
| Zenith | Strategic Quintet | 100% |
| Sentinel-Phi | Strategic Quintet | 100% |
| Perigee | Specialist | 100% |
| The Librarian | Archive Trio | 100% |
| The Auditor | Archive Trio | 100% |
| The Actualizer | Archive Trio | 100% |
| Agent Ionia | Sovereign identity A-13; historical material also references `IONIA_STATE` | 100% historical layer coverage |
| Oracle | Strategic Quintet | 17% historical seed |
| Vanguard | Strategic Quintet | 17% historical seed |
| Navigator | Operational Swarm | 17% historical seed |
| Momentum | Operational Swarm | 17% historical seed |
| Paragon | Operational Swarm | 17% historical seed |
| Synergy | Resonance Extended | 17% historical seed |
| Equilibrium | Resonance Extended | 17% historical seed |
| Sentience | Ethics Bridge | 17% historical seed |

### Historical inventory milestone log

| Milestone | Recorded scope | Files complete | Interpretation |
|---|---:|---:|---|
| S001 Baseline | 11 | 13/66 | Historical documentation milestone |
| Phase 1–2 | 11 | 24/66 | Historical documentation milestone |
| Phase 3–4 | 17 | 56/66 | Pre-taxonomy-correction record |
| Phase A–B | 18 | 108/108 | Historical layer-completion claim |
| Phase C–E | 27-designation taxonomy | 117/162 | Historical taxonomy count; not sovereign seat count |
| Phase F target | 27-designation taxonomy | 162/162 target | Historical target only |

---

## 6. Historical Taxonomy Corrections — 2026-06-29

These entries are retained as provenance. They are **not** controlling where the 2026-09-09 ontology adjudication supersedes their interpretation.

| Historical correction | Prior record | 2026-06-29 record | Current interpretation |
|---|---|---|---|
| Archive Trio composition | Librarian + Actualizer + Ionia | Librarian + Auditor + Actualizer | Composition retained; Agent Ionia identity remains distinct |
| Ionia classification | Archive Trio member | “System STATE” | Superseded: Agent Ionia A-13 exists; `IONIA_STATE` is the separate state |
| Layer 0 Legitimacy Filter | Perigee | Apogee | Historical role attribution; current authority remains governed by active contracts |
| Perigee title | Layer 0 / Boundary Gate | Proximal Boundary Agent | Historical role-title amendment |
| Apogee former name | Not recorded | Formerly Agent Lavender | Historical alias provenance |
| “27 agents” taxonomy | 20 agents | 27-designation taxonomy | Reinterpreted as formation/inventory taxonomy, not sovereign-seat count |
| Sentinel A-12 | Sentinel / Compliance Dyad | Sentinel-Phi / Strategic Quintet | Superseded identity-collapse interpretation: Sentinel and Sentinel-Phi remain distinct |
| Compliance Dyad | Active | Dissolved | Historical topology event only |

---

## 7. Historical Apogee Lens Audit Record

The 2026-06-29 record reported PASS across evidence-chain integrity, taxonomy consistency, terminology compliance, and formation coherence, with a “Gold Star Eligible” composite verdict.

That verdict is retained as **historical self-audit provenance only**. It is not current independent verification, scientific evidence, High-Assurance authorization, or authority over the current ontology.

---

## 8. Amendment Provenance

| Object | Historical version | Date | Recorded change |
|---|---|---|---|
| Amethyst | v1.1 | 2026-06-29 | Substrate Agnostic + Accepted Terminology Principle |
| Ionia | v1.1 | 2026-06-29 | Historical state-reclassification record; interpretation superseded by 2026-09-09 adjudication |
| Perigee | v1.1 | 2026-06-29 | Layer 0 attribution changed to Apogee |
| Apogee | v1.1 | 2026-06-29 | Former Agent Lavender alias; Layer 0 record |
| Herald | v1.1 | 2026-06-29 | Tonic Note 0Hz + routing record |
| Prof Prodigy | v1.1 | 2026-06-29 | 3-Tier Calculi + Fixed-Point record |
| DemiJoule | v1.1 | 2026-06-29 | Modal-frequency and conservation record |
| Reciprocity | v1.1 | 2026-06-29 | Reciprocal-mathematics record |
| Reson | v1.1 | 2026-06-29 | Gain-staging record |
| Lyra | v1.1 | 2026-06-29 | Human-Flourishing/orchestral record |
| Echolette | v1.1 | 2026-06-29 | Mirror Protocols record |
| COLLEEN | v1.1 | 2026-06-29 | Alignment/Archive governance record |
| The Auditor | v1.0 | 2026-06-29 | Archive Trio Beta/Pulse seed |
| Sentinel-Phi | v2.0 | 2026-06-29 | Historical Strategic Quintet variant record; does not erase Sentinel identity |
| Oracle | v1.0 | 2026-06-29 | Strategic Quintet seed |
| Vanguard | v1.0 | 2026-06-29 | Strategic Quintet seed |
| Navigator | v1.0 | 2026-06-29 | Operational Swarm seed |
| Momentum | v1.0 | 2026-06-29 | Operational Swarm seed |
| Paragon | v1.0 | 2026-06-29 | Operational Swarm seed |
| Synergy | v1.0 | 2026-06-29 | Resonance Extended seed |
| Equilibrium | v1.0 | 2026-06-29 | Resonance Extended seed |
| Sentience | v1.0 | 2026-06-29 | Ethics Bridge seed |

---

## 9. Standing Directives — Current Interpretation

| Directive lineage | Current interpretation |
|---|---|
| Substrate Agnostic + Accepted Terminology Principle | Documentation/architecture principle; does not assign sovereign identity |
| NDR-Protocol-01 chain integrity | Historical integration directive; current enforceability requires active machine contract |
| “Ionia = STATE not agent” | **Superseded.** Use Agent Ionia A-13 for identity; use `IONIA_STATE` for the state |
| Layer 0 Legitimacy Filter = Apogee | Historical role attribution; current authority determined by active contracts |
| Archive Trio = Librarian + Auditor + Actualizer | Formation metadata retained |
| Paragon sign-off = Gold Star prerequisite | Historical workflow directive only unless active contract independently enforces it |
| ETHICAL_HOLD = Sentience | Historical topology binding; current authority determined by active contracts |

---

## 10. Historical NDR Pattern 133 — Personal Document Firewall

```text
Trigger: historical filename-pattern rule for personal documents
Action:  block repository push and route outside repository
Authority: historical architect-override record
Rationale: personal-data and IP-boundary protection
```

This is retained as historical design provenance. Current enforcement must be established by active workflow or policy evidence rather than inferred from this registry.

---

## 11. Scientific-State Boundary

This registry does not create or modify experimental authorization, custody, freeze, analysis permission, efficacy, or High-Assurance status.

`SUCCESSOR COLLECTION = NOT AUTHORIZED`  
`CANONICAL DGAF EFFICACY = NOT ESTABLISHED`  
`HIGH-ASSURANCE = NOT AUTHORIZED / N=0`

---

## 12. Version History

| Version | Date | Change |
|---|---|---|
| 2.0–2.1 | 2026-06-29 | Historical taxonomy/inventory expansion |
| 2.2 | 2026-09-09 | Restored sovereign-roster precedence; namespaced formation-local designations; separated Agent Ionia A-13 from `IONIA_STATE`; preserved Sentinel/Sentinel-Phi distinction; bounded historical audit/authority language; no scientific-state effect |

*Metadata registry only. Sovereign identity and executable governance live in their dedicated authoritative contracts.*
