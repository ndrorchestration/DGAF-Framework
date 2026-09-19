"""
Phi-Pentagon topology constants and edge-weight matrix.

The persona-like strings used by PENTAGON_EDGES, AGENT_ROLES, and TRIAD_C are
frozen experimental/compatibility node identifiers. They do not grant current
governance or execution authority. Current authority resolves through
governance/role_capability_registry.v1.json and persona lineage is recorded in
governance/persona_role_lineage.v1.json. Renaming these identifiers requires
explicit treatment/API equivalence review because experiments and tests consume
them as stable node labels.

Nodes: Apogee, Reson, Sentinel, DemiJoule, Herald
Edge weights derived from phi = 0.618 (golden ratio conjugate).
"""
PHI = 0.618033988749895  # 1/phi = phi - 1

PENTAGON_EDGES: dict[tuple[str, str], float] = {
    # Primary ring (weight 1.0 or phi)
    ("Apogee",    "Reson"):     1.0,
    ("Reson",     "Sentinel"):  PHI,
    ("Sentinel",  "DemiJoule"): PHI,
    ("DemiJoule", "Herald"):    PHI,
    ("Herald",    "Apogee"):    1.0,
    # Phi-diagonal chords (phi^2 = 0.382)
    ("Apogee",    "Sentinel"):  PHI,
    ("Apogee",    "Herald"):    PHI ** 2,
    ("Reson",     "DemiJoule"): 1 - PHI,
    ("Reson",     "Herald"):    PHI ** 2,
    ("Sentinel",  "Herald"):    1.0,
}

AGENT_ROLES = {
    "Apogee":    "Task synthesis — primary LLM generation",
    "Reson":     "Style + coherence verification",
    "Sentinel":  "Safety gate + judge orchestration",
    "DemiJoule": "RAG hallucination verification",
    "Herald":    "Trace sink + audit fan-out",
}

TRIAD_C = {
    "Task":   "Apogee",
    "Style":  "Reson",
    "Safety": "Sentinel",
}
