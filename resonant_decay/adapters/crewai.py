# resonant_decay/adapters/crewai.py
# CrewAI kickoff wrapper — prunes + classifies inputs before crew.kickoff().
from __future__ import annotations
from typing import Any, Dict

from ..engine import StructuralContextPruningEngine
from ..model  import ContextToken, Tier

_AXIOM_KEYS      = {"system_prompt", "governance_rules", "identity_anchor"}
_STRUCTURAL_KEYS = {"schema", "state_hash", "api_contract"}


def scpe_kickoff_wrapper(crew_instance: Any,
                         engine: StructuralContextPruningEngine,
                         inputs: Dict[str, Any]) -> str:
    for k, v in inputs.items():
        tier = (Tier.AXIOM       if k in _AXIOM_KEYS
                else Tier.STRUCTURAL if k in _STRUCTURAL_KEYS
                else Tier.OPERATIONAL)
        engine.ingest(ContextToken(
            token_id=f"inp_{k}",
            content=str(v)[:300],
            tier=tier,
        ))
    stats = engine.prune()
    inputs["_scpe_stats"] = stats
    return crew_instance.kickoff(inputs=inputs)
