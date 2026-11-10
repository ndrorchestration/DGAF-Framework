"""Bound the canonical, project-defined hendecagon pP decimal presentation.

This is a documentation-integrity test, not a DGAF performance/efficacy test.
Historical/immutable experimental and audit records are intentionally excluded.
"""

from math import pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPLAY_DECIMAL = "1.7747327664"
SUPERSEDED_DECIMAL = "1.774732842"

# Current-facing, mutable documentation only; historical evidence is untouched.
CURRENT_REFERENCES = (
    "docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md",
    "docs/governance/PLATINUM_MEAN_SEMANTIC_CORRECTION_2026-08-28.md",
    "docs/formalism/constants/11Q-derivation.md",
    "docs/taxonomy/NDR_ACRONYM_REGISTRY.md",
    "docs/NDR_INTERNAL_VOCABULARY_MASTER.md",
    "docs/registry/NDR_PLATINUM_REGISTRY_SERVICE_P39_v1.md",
    "docs/EPISTEMIC_SUPERSESSION_REGISTER.md",
    "docs/patterns/NDR_CDPO_v4.2-HGF.md",
    "docs/substrate/NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md",
)


def test_unit_side_hendecagon_circumradius_display_precision():
    radius = 1.0 / (2.0 * sin(pi / 11.0))
    assert format(radius, ".10f") == DISPLAY_DECIMAL


def test_current_project_defined_pp_references_are_consistent():
    for relative_path in CURRENT_REFERENCES:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        assert DISPLAY_DECIMAL in content, f"Expected pP decimal missing: {relative_path}"
        assert SUPERSEDED_DECIMAL not in content, f"Superseded pP decimal still present: {relative_path}"
