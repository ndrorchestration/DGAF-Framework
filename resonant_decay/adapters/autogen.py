# resonant_decay/adapters/autogen.py
# AutoGen wrapper — prunes + ingests around any ConversableAgent.
from __future__ import annotations
import hashlib
from typing import Any, List, Optional

from ..engine import StructuralContextPruningEngine
from ..model  import ContextToken, Tier


class SCPEAgent:
    """Wraps any AutoGen ConversableAgent with SCPE middleware."""

    def __init__(self, agent: Any, engine: StructuralContextPruningEngine):
        self.agent  = agent
        self.engine = engine

    def generate_reply(self, messages: List[dict],
                       sender: Optional[Any] = None, **kwargs) -> Any:
        self.engine.prune()
        for msg in messages[-3:]:
            content = msg.get("content", "")
            tier    = (Tier.STRUCTURAL if msg.get("role") == "system"
                       else Tier.OPERATIONAL)
            tok = ContextToken(
                token_id=hashlib.sha256(
                    content[:64].encode()).hexdigest()[:12],
                content=content[:300],
                tier=tier,
            )
            self.engine.ingest(tok)
        return self.agent.generate_reply(messages, sender, **kwargs)
