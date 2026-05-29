# resonant_decay — Topological Resonant Decay middleware
# Extracted from ensemble_v17.py for pip-installable, adapter-agnostic use.
# Version: 1.7.0 | NDR Pattern S045
from .model   import Tier, ContextToken, ContextBuffer
from .engine  import StructuralContextPruningEngine
from .phi_gate import PhiClosureGate
from .governance import compute_hash, lock_token, validate_token

__version__ = "1.7.0"
__all__ = [
    "Tier", "ContextToken", "ContextBuffer",
    "StructuralContextPruningEngine",
    "PhiClosureGate",
    "compute_hash", "lock_token", "validate_token",
]
