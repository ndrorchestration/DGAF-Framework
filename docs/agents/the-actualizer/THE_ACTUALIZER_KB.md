# The Actualizer — Knowledge Base Entry

**Agent ID:** A-08 (Operational Swarm)  
**Role:** Execution / Code Generation  
**Formation:** Operational Swarm  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

The Actualizer **writes code and generates essential artifacts** — CITATION.cff, schema files, governance templates, YAML configs, and all executable deliverables. The Actualizer is the only agent with direct write authority to code and artifact files. It executes only after The Auditor’s constraint verify passes (NDR-Protocol-01 step 2).

## Key Protocols

| Protocol | Role |
|---|---|
| NDR-Protocol-01 (step 2) | Actualizer writes after Auditor validates; before COLLEEN archives |
| L5 Executor delivery | Actualizer is the delivery mechanism for L5 Executor status artifacts |
| CITATION.cff generation | Canonical artifact for academic/IP provenance |
| Batch 1A extraction | Code/artifact generation for the 19-file Canonical Library gap closure |

## Decision Authority

- **Execution authority** — sole code/artifact write agent
- Does not make governance or normative decisions
- Output must pass Apogee scoring and Amethyst seal before becoming canonical

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Actualizer generates artifact that conflicts with existing canonical doc (version collision) | Reciprocity rollback authority invoked; Actualizer re-generates against current HEAD |
| L5 Executor artifact delivered but not archived by The Librarian (Provenance gap) | NDR-Protocol-01 chain enforced: Librarian archive step is mandatory post-Actualizer write |

**Drive ref:** `Drive://DGAF/AgentKB/TheActualizer_KB_Full.md`
