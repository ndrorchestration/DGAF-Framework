#!/usr/bin/env python3
"""Prepare the exact Epoch 002 operator evidence-admission repository delta."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DEFAULT_RETENTION_DIR = Path.home() / "DGAF-Epoch002-Retention"
EVIDENCE_NAME = "track_a_epoch_002_dataset_lock_evidence.json"
LEDGER_NAME = "track_a_epoch_002_pre_lock_result_ledger.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_EVIDENCE_ADMISSION_PREP_FAIL: {message}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


dataset_lock = load_module(
    SCRIPTS / "validate_track_a_epoch_002_dataset_lock.py",
    "epoch_002_dataset_lock_for_operator_evidence_admission_preparer",
)


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def require_external_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    root = ROOT.resolve()
    if resolved == root or root in resolved.parents:
        fail(f"{label} must remain outside the repository")
    if not resolved.is_file():
        fail(f"{label} missing: {resolved}")
    return resolved


def require_clean_repository() -> None:
    status = git("status", "--porcelain", "--untracked-files=all")
    if status:
        fail("clean repository required before preparing operator evidence admission")


def require_absent_destination(path: Path) -> None:
    if path.exists():
        fail(f"destination already exists: {path.relative_to(ROOT)}")
    rel = path.relative_to(ROOT).as_posix()
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{rel}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        fail(f"destination already exists in HEAD: {rel}")


def validate_sources(evidence_path: Path, ledger_path: Path) -> dict[str, Any]:
    evidence, _ = dataset_lock.validate_evidence_file(evidence_path)
    if evidence.get("evidence_execution_class") != "OPERATOR_CODESPACE":
        fail("operator evidence admission requires OPERATOR_CODESPACE evidence")
    if evidence.get("collection_execution_class") != "OPERATOR_CODESPACE":
        fail("operator evidence admission requires OPERATOR_CODESPACE collection provenance")
    dataset_lock.validate_pre_lock_ledger(ledger_path, evidence)
    return evidence


def expected_untracked_status() -> list[str]:
    return sorted(
        [
            f"?? {dataset_lock.OPERATOR_EVIDENCE_REL}",
            f"?? {dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL}",
        ]
    )


def verify_exact_delta() -> None:
    actual = sorted(line for line in git("status", "--porcelain", "--untracked-files=all").splitlines() if line)
    expected = expected_untracked_status()
    if actual != expected:
        fail(f"repository delta must contain exactly the two admission files; got {actual}")


def prepare(
    *,
    retention_dir: Path = DEFAULT_RETENTION_DIR,
    evidence_path: Path | None = None,
    ledger_path: Path | None = None,
    write: bool = False,
) -> tuple[Path, Path]:
    evidence_source = require_external_file(
        evidence_path or retention_dir / EVIDENCE_NAME,
        "operator dataset-lock evidence",
    )
    ledger_source = require_external_file(
        ledger_path or retention_dir / LEDGER_NAME,
        "operator pre-lock result ledger",
    )

    evidence_dest = ROOT / dataset_lock.OPERATOR_EVIDENCE_REL
    ledger_dest = ROOT / dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL
    require_absent_destination(evidence_dest)
    require_absent_destination(ledger_dest)
    require_clean_repository()
    validate_sources(evidence_source, ledger_source)

    if not write:
        print("TRACK_A_EPOCH_002_OPERATOR_EVIDENCE_ADMISSION_PREPARER=" "PASS_DRY_RUN_NOT_WRITTEN")
        print(f"EVIDENCE_SOURCE={evidence_source}")
        print(f"LEDGER_SOURCE={ledger_source}")
        print(f"EVIDENCE_DESTINATION={evidence_dest}")
        print(f"LEDGER_DESTINATION={ledger_dest}")
        return evidence_dest, ledger_dest

    evidence_dest.parent.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        evidence_dest.write_bytes(evidence_source.read_bytes())
        created.append(evidence_dest)
        ledger_dest.write_bytes(ledger_source.read_bytes())
        created.append(ledger_dest)
        verify_exact_delta()
        persisted_evidence, _ = dataset_lock.validate_evidence_file(evidence_dest)
        dataset_lock.validate_pre_lock_ledger(ledger_dest, persisted_evidence)
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise

    print("TRACK_A_EPOCH_002_OPERATOR_EVIDENCE_ADMISSION_PREPARER=" "PASS_NONAUTHORIZING_DELTA_PREPARED")
    print(f"EVIDENCE_DESTINATION={evidence_dest}")
    print(f"LEDGER_DESTINATION={ledger_dest}")
    print(
        "NEXT_GIT_ADD=git add " f"{dataset_lock.OPERATOR_EVIDENCE_REL} " f"{dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL}"
    )
    print("NEXT_GIT_COMMIT=git commit -m 'admit Track A Epoch 002 operator dataset-lock evidence'")
    return evidence_dest, ledger_dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retention-dir", type=Path, default=DEFAULT_RETENTION_DIR)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--pre-lock-ledger", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    prepare(
        retention_dir=args.retention_dir,
        evidence_path=args.evidence,
        ledger_path=args.pre_lock_ledger,
        write=args.write,
    )
    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
