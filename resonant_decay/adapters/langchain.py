# resonant_decay/adapters/langchain.py
# LangChain callback handler — prunes before LLM call, ingests response.
from __future__ import annotations
import time
from typing import Any, Dict, List

try:
    from langchain.callbacks.base import BaseCallbackHandler
except ImportError:
    BaseCallbackHandler = object  # type: ignore

from ..engine import StructuralContextPruningEngine
from ..model  import ContextToken, Tier


class SCPECallbackHandler(BaseCallbackHandler):
    def __init__(self, engine: StructuralContextPruningEngine):
        self.engine = engine

    def on_llm_start(self, serialized: Dict[str, Any],
                     prompts: List[str], **kwargs) -> None:
        stats = self.engine.prune()
        print(f"[SCPE] pre-LLM prune: {stats['pruned']} dropped, "
              f"compression={stats['compression_ratio']:.3f}")

    def on_llm_end(self, response: Any, **kwargs) -> None:
        for gen_list in response.generations:
            for gen in gen_list:
                tok = ContextToken(
                    token_id=f"resp_{int(time.time()*1000)}",
                    content=getattr(gen, 'text', str(gen))[:200],
                    tier=Tier.OPERATIONAL,
                )
                self.engine.ingest(tok)
