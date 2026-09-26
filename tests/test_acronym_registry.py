import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_acronym_registry.py"

spec = importlib.util.spec_from_file_location("validate_acronym_registry", SCRIPT)
assert spec is not None
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_acronym_registry_schema_and_required_tokens():
    data = module.load()
    assert module.validate_registry(data) == []


def test_current_surfaces_have_no_unregistered_acronyms():
    data = module.load()
    assert module.lint_surfaces(data) == []


def test_status_prose_is_not_misclassified_as_acronyms():
    text = "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / CURRENT / ONLY"
    assert module._candidate_tokens(text) == set()


def test_parenthetical_first_use_is_detected():
    assert module._candidate_tokens("Policy Enforcement Point (PEP)") == {"PEP"}
