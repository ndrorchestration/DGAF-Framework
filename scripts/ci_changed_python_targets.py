from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _normalize_changed_paths(raw: bytes, root: Path = ROOT) -> list[str]:
    targets: list[str] = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        path = os.fsdecode(entry).replace("\\", "/")
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"unsafe changed path: {path!r}")
        if candidate.suffix not in {".py", ".pyi"}:
            continue
        if (root / candidate).is_file():
            targets.append(candidate.as_posix())
    return sorted(set(targets))


def changed_python_files(base_sha: str, head_sha: str, root: Path = ROOT) -> list[str]:
    raw = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            base_sha,
            head_sha,
            "--",
            "*.py",
            "*.pyi",
        ],
        cwd=root,
    )
    return _normalize_changed_paths(raw, root)


def main() -> int:
    parser = argparse.ArgumentParser(description="List changed tracked Python files for static-quality checks.")
    parser.add_argument("base_sha")
    parser.add_argument("head_sha")
    args = parser.parse_args()

    for path in changed_python_files(args.base_sha, args.head_sha):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
