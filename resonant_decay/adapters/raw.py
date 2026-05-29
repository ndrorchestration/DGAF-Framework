# resonant_decay/adapters/raw.py
# Simple decorator adapter — wraps any callable LLM function.
from __future__ import annotations
from functools import wraps
from typing import Any, Callable, Dict

from ..engine import StructuralContextPruningEngine


def scpe_middleware(engine: StructuralContextPruningEngine):
    """Decorator: prune context before every LLM call."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            stats = engine.prune()
            kwargs["_scpe_stats"] = stats
            return fn(*args, **kwargs)
        return wrapper
    return decorator
