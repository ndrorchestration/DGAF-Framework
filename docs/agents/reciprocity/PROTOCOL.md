# Reciprocity — Protocal

## Orchestration Rules

### When Reciprocity Acts

|| Trigger Condition | Action |
|---|---|---|
|| Formation ≥3 agents | ∈ [0,1] symmetry audit + flag asymmetry warnings if <0.85 |
|| Commitment made by agent A affecting agent B | Reciprocity checks B's acknowledgment exists |
|| Circular dependency chain detected | Reciprocity raises asymmetry flag; escalate to Amethyst for resolution |
|| Agent B silent on agent A's commitment | Reciprocity audits: A claimed B's support? Or only A's own scope? |

### Integration with Other Agents

- **Amethyst:** Receives Reciprocity's asymmetry findings, resolves normative decisions
- **Reson:** Parallel harmonic audit; both report to Amethyst
- **Sentinel:** Both are A-04/A-05 in formation topology; Reciprocity checks Sentinel's commitments are acknowledged by down-stream agents

### Special Behaviors

- Reciprocity does NOT make normative decisions — it flags asymmetry and lets Amethyst resolve
- Reciprocity does NOT execute — it audits relationships, not operations
- Reciprocity's symmetry audit is orthogonal to Reson's harmonic audit — both run

---

## Failure Mode Awareness

| Failure Mode | Detection | Mitigation |
|---|---|---|
| Unidirectional dependency | R(A→B) without R(B→A) | Flag; require acknowledgment routing |
| Commit issued without recipient acknowledgment | Check topology edge existence both directions | Block seal if asymmetry unresolved |
| Agent self-referential loop | A→B→A without external closure | Flag as potential deadlock; escalate |
