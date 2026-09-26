from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_acronym_registry.py"

spec = importlib.util.spec_from_file_location("validate_acronym_registry", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

def test_acronym_registry_schema_and_required_tokens():
    data = module.load()
    assert module.validate_registry(data) == []

def test_current_surfaces_have_no_unregistered_acronyms():
    data = module.load()
    assert module.lint_surfaces(data) == []
