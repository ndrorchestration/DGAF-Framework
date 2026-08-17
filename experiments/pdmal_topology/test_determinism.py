import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent
SCRIPT = ROOT / "determinism.py"


def run_case(output: Path) -> bytes:
    command = [
        sys.executable,
        str(SCRIPT),
        "--seed", "42",
        "--topology", "pdmal",
        "--failures", "0",
        "--output", str(output),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True, cwd=ROOT)
    return completed.stdout.strip().encode("ascii")


def test_byte_for_byte_determinism(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    digest_a = run_case(first)
    digest_b = run_case(second)
    assert digest_a == digest_b
    assert first.read_bytes() == second.read_bytes()
