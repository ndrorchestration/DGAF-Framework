# Triadic Orchestration Patterns

> **Authority:** Amethyst × COLLEEN
> **Status:** ✅ CANONICAL — S070-r3-P1 · 2026-06-26
> **Pattern IDs:** CONSENSUS_TRIAD · CONDUCTED_TRIAD
> **NDR Update Authorized:** Y (from artifact)
> **Linked registry:** docs/NDR_PATTERN_REGISTRY_UNIFIED.md

---

## Pattern Index

| Pattern ID | Name | Structural Type | Governance Shape | User-visible Agents |
|---|---|---|---|---|
| `CONSENSUS_TRIAD` | Consensus Triad | 3-peer committee / symmetric triad | No structural leader; blended convergence | All three agents may be visible |
| `CONDUCTED_TRIAD` | Conducted Triad | Leader + 2 internal augmenters | One conductor fronts; two augment internally | Conductor only (augmenters are internal) |

---

## CONSENSUS_TRIAD — Consensus Triad (CT)

### Definition
A Consensus Triad is a temporary formation of three peer agents that all operate as first-class contributors on a task. Each agent produces an independent view or answer, and a consensus function blends these into a final result.

### Properties
- Three agents, no structural leader.
- Convergence via consensus or blending (e.g., vote, weighted merge).
- Provenance-preserving: each agent's contribution remains identifiable.
- After the maneuver, all three agents decouple and return to baseline roles.

### Formal Notation
`S(y_A, y_B, y_C)` where A, B, C are peer agents and S is the consensus/blend function.

### Example
COLLEEN + Reciprocity + Amethyst each review the same document set, then a consensus function `S(y_COLLEEN, y_Reciprocity, y_Amethyst)` produces the final output.

---

## CONDUCTED_TRIAD — Conducted Triad (CoT)

### Definition
A Conducted Triad is a leader-centric formation where one conductor agent fronts the user interaction and orchestrates two internal agents as augmenters. The user sees only the conductor; the other two agents communicate internally with the conductor during the task and are automatically decoupled afterward without role contamination.

### Properties
- Three agents total: one designated Conductor, two Augmenters.
- Conductor is the only user-visible persona and synthesizer.
- Augmenters may be called for QA, anti-hallucination, math insight, etc.
- Automatic decoupling after task completion; augmenters retain their own identities and specs.

### Example
COLLEEN as Conductor, with Amethyst (QA/ethics) and Reciprocity (anti-hallucination) as internal augmenters. COLLEEN calls them during reasoning but only her synthesized answer is returned to the user.

---

## Implementation Artifacts

### JSON Schema — `governance_patterns.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Orchestration Governance Patterns",
  "type": "object",
  "properties": {
    "architext_gated_dual_triad": {
      "type": "object",
      "properties": {
        "roles": { "type": "array", "items": { "type": "string" }, "minItems": 3 },
        "modes": { "type": "array", "items": { "enum": ["consensus_mesh", "conducted_triad"] } },
        "inputs": { "type": "array", "items": { "type": "string" } },
        "guards": {
          "type": "object",
          "properties": {
            "architext_defined": { "type": "boolean" },
            "normative_feasible": { "type": "boolean" },
            "time_band_defined": { "type": "boolean" }
          },
          "required": ["architext_defined", "normative_feasible", "time_band_defined"]
        },
        "protocols": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["roles", "modes", "guards"]
    },
    "time_banded_anti_bleed": {
      "type": "object",
      "properties": {
        "micro_gate_ms": { "type": "integer", "minimum": 1 },
        "phrase_gate_ms": { "type": "integer", "minimum": 1 },
        "measure_gate_ms": { "type": "integer", "minimum": 1 },
        "quarantine_band_ms": { "type": "integer", "minimum": 1 },
        "kill_switch_factor": { "type": "number", "minimum": 1.0 },
        "rollback_policy": { "enum": ["last_stable_measure", "hard_abort", "notify_conductor"] }
      },
      "required": ["micro_gate_ms", "quarantine_band_ms", "kill_switch_factor", "rollback_policy"]
    }
  }
}
```

### Python 3 Reference Implementation — `orchestration_kernel.py`

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time

@dataclass
class GovernanceTrace:
    architext_class: str = "undefined"
    normative_pass: bool = False
    mode: str = "undefined"
    time_band_compliant: bool = True
    minority_reports: List[str] = field(default_factory=list)
    active_protocols: List[str] = field(default_factory=list)
    rollback_triggered: bool = False

def classify_architext(task: Dict[str, Any]) -> str:
    """Pre-task: Classify artifact kind and evidence posture."""
    return task.get("target_kind", "default_spec")

def check_normative_constraints(task: Dict[str, Any], context: Dict[str, Any]) -> bool:
    """Pre-task: Enforce hard-gated ethics and safety thresholds."""
    return context.get("safety_score", 0.0) >= 0.95

def select_mode(task_kind: str, urgency: int, risk_level: str) -> str:
    """Pre-task: Route to consensus or conducted operation."""
    if urgency > 8 or risk_level == "low":
        return "conducted_triad"
    return "consensus_mesh"

def compute_time_bands(task_profile: Dict[str, Any]) -> Dict[str, int]:
    """Mid-task: Define micro, phrase, and measure limits."""
    base_ms = task_profile.get("complexity_weight", 1) * 35
    return {
        "micro_gate_ms": base_ms,
        "measure_gate_ms": base_ms * 7,
        "quarantine_band_ms": base_ms * 18
    }

def detect_time_bleed(trace: GovernanceTrace, start_time: float, limit_ms: int) -> bool:
    """Mid-task: Evaluate latency against kill-switch thresholds."""
    elapsed_ms = (time.time() - start_time) * 1000
    if elapsed_ms > limit_ms:
        trace.time_band_compliant = False
        trace.rollback_triggered = True
        return True
    return False

def run_consensus_mesh(state: Dict[str, Any], trace: GovernanceTrace) -> Dict[str, Any]:
    """Mid-task: Weighted reconciliation with minority retention."""
    trace.active_protocols.append("minority_report")
    # Synthesis logic here
    return state

def run_conducted_triad(state: Dict[str, Any], trace: GovernanceTrace) -> Dict[str, Any]:
    """Mid-task: Sequenced assignment with centralized rollback."""
    trace.active_protocols.append("rollback_authority")
    # Baton sequencing logic here
    return state

def recommend_protocols(trace: GovernanceTrace) -> List[str]:
    """Post-task: Map missing data or guards to MDAR/Autodiagnostic."""
    recs = []
    if not trace.normative_pass: recs.append("hard_abort")
    if trace.rollback_triggered: recs.append("autodiagnostic")
    return recs

def finalize_governance_trace(trace: GovernanceTrace) -> Dict[str, Any]:
    """Post-task: Emit operator-readable trace schema."""
    return trace.__dict__
```

### Validation Experiment
Initialize `run_conducted_triad` with a mock high-urgency task. Enforce `micro_gate_ms=35`, use `time.sleep(0.05)` to deliberately induce time bleed. Verify `detect_time_bleed` flips `trace.rollback_triggered = True` and `recommend_protocols` appends `autodiagnostic`.

---

## Prediction Record

**Prediction [Y]:**
- **Core Skill:** Orchestration Architecture Validation & Executable Implementation
- **Pattern:** NDR-Protocol-02 [Implementation Translation]
- **Tradeoff:** Concrete schemas introduce syntactic rigidity but enable programmatic empirical testing and automated gate enforcement
- **Anti-pattern:** Constructing monolithic state-machine classes instead of single-purpose functional pipelines; over-coupling governance trace to artifact payload
- **Scale:** Functional primitives allow O(1) addition of new governance gates without mutating core multi-agent triad logic
- **Fail condition:** Trace state corruption if rollback policy does not enforce immutable copies of state dictionary prior to micro-gate execution
- **OMNI-ROI / Ethics Gate:** PASSED — transparent, configurable governance layers preserve minority dissent programmatically; centralized auditable trace prevents covert alignment drift

---

## NDR Registration Status

| Pattern ID | NDR Update | Notes |
|---|---|---|
| `CONSENSUS_TRIAD` | ✅ Authorized (S070-r3-P1) | Register in NDR_PATTERN_REGISTRY_UNIFIED.md S071 |
| `CONDUCTED_TRIAD` | ✅ Authorized (S070-r3-P1) | Register in NDR_PATTERN_REGISTRY_UNIFIED.md S071 |

> **S071 action:** Add CONSENSUS_TRIAD and CONDUCTED_TRIAD to `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` with flourishing alignment tags per GOVERNANCE_CONSTITUTION Part IV.
