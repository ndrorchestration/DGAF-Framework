"""Contract tests for the pre-freeze DGAF/TGL adapter.

CI trigger note: this file is otherwise semantically unchanged; the marker
forces a non-empty push so the pre-freeze workflow executes on the current head.
"""
from __future__ import annotations

import pytest

from dgaf_tgl_adapter import (
    ConsensusState,
    DGAF_TGLAdapter,
    apply_decision,
    canonicalize_state,
    decision_from_audit,
)