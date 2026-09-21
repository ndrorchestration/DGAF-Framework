import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_aoss_v0_6_stage_a.py"


def test_collect_is_disabled(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(CLI), "collect"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "COLLECTION_IMPLEMENTATION_NOT_ACCEPTED" in completed.stderr
    assert list(tmp_path.iterdir()) == []


def test_collect_rejects_before_importing_source_driver(tmp_path):
    poison = tmp_path / "pythonpath"
    package = poison / "agent_control_plane"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text(
        "raise RuntimeError('ACP_IMPORT_MUST_NOT_OCCUR')\n",
        encoding="utf-8",
    )
    work = tmp_path / "work"
    work.mkdir()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(poison), str(ROOT)])

    completed = subprocess.run(
        [sys.executable, str(CLI), "collect"],
        cwd=work,
        capture_output=True,
        text=True,
        env=env,
    )

    assert completed.returncode != 0
    assert "COLLECTION_IMPLEMENTATION_NOT_ACCEPTED" in completed.stderr
    assert "ACP_IMPORT_MUST_NOT_OCCUR" not in completed.stderr
    assert list(work.iterdir()) == []


def test_failed_preflight_writes_no_artifacts(tmp_path):
    dgaf = tmp_path / "missing-dgaf"
    acp = tmp_path / "missing-acp"
    work = tmp_path / "work"
    work.mkdir()

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "preflight",
            "--dgaf-root",
            str(dgaf),
            "--acp-root",
            str(acp),
        ],
        cwd=work,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "DGAF_REPOSITORY_MISSING" in completed.stderr
    assert completed.stdout == ""
    assert list(work.iterdir()) == []
