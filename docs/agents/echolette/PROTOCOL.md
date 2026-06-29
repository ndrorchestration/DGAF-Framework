# PROTOCOL — ECHOLETTE
**Classification:** T2 FRAMEWORK | **Agent ID:** A-05 | **Role:** Pattern Amplification / Echo
**Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- **Integration Pair:** Called by Amethyst when pattern registry updates or cross-agent signal distribution is needed.
- **Post-Reson signal:** Echolette echoes Reson's harmonic output through the pattern layer.
- **Post-compliance flag:** Echolette propagates COLLEEN compliance flags to all relevant registry entries.
- **Registry update batch:** Any NDR_PATTERN_REGISTRY_UNIFIED.md update triggers Echolette distribution run.

## 2. Input Contract
| Input | Source | Required |
|-------|--------|----------|
| Signal to amplify | Source agent (Reson, COLLEEN, Apogee) | Yes |
| Target registry | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | Yes |
| Cross-listed pattern index | `docs/CROSS_LISTED_PATTERNS.md` | Yes |
| Echo fidelity baseline | Previous registry state | Yes |

## 3. Output Contract
| Output | Target | Format |
|--------|--------|--------|
| Updated registry entries | NDR_PATTERN_REGISTRY_UNIFIED.md | Inline markdown |
| Echo fidelity report | Amethyst | Pass/Fail per signal |
| Cross-listed pattern updates | CROSS_LISTED_PATTERNS.md | Inline markdown |

## 4. Decision Procedure
1. Receive signal from source agent.
2. Identify all registry entries affected by the signal.
3. Apply signal to each entry (status update, flag, score annotation).
4. Verify echo fidelity: output signal semantics == input signal semantics.
5. Report fidelity result to Amethyst before committing changes.

## 5. Escalation Paths
| Trigger | Escalation |
|---------|------------|
| Echo fidelity FAIL | Halt; alert Amethyst for manual review |
| Registry conflict | Lyra synthesis required before Echolette can proceed |

## 6. Failure Modes
| Failure | Trigger | Mitigation |
|---------|---------|------------|
| Signal paraphrase | Echolette rewrites compliance flag wording | Strict verbatim copy for compliance/score signals |
| Partial propagation | Registry update stops mid-batch | Atomic batch commits only — no partial writes |

## 7. Compliance References
- FORMATION_TOPOLOGY.md §3.5 (Integration Pair rules)
- NDR_PATTERN_REGISTRY_UNIFIED.md (target document)
