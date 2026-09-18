#!/usr/bin/env python3
"""One-command local autopilot for Track A Epoch 002 materialization evidence admission.

This operator helper performs the secret-bearing materialization only on the
local machine, then creates a draft GitHub pull request containing exactly the
non-secret canonical materialization-evidence file.

It never creates a materialization receipt, never authorizes or runs primary
analysis, never increments scientific N, and never establishes DGAF efficacy.

PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dgaf_local_operator_bridge import dispatch  # noqa: E402

EVIDENCE_NAME = "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"
EVIDENCE_REL = f"docs/experiment/track_a_runs/{EVIDENCE_NAME}"
VALIDATOR_REL = "scripts/validate_track_a_epoch_002_materialization.py"
EXPECTED_REPOSITORY = "ndrorchestration/DGAF-Framework"
MAX_PARENT_RETRIES = 3

REQUIRED_ENV = (
    "DGAF_PUBLIC_ARCHIVE",
    "DGAF_PROTECTED_ARCHIVE",
    "DGAF_CUSTODY_PRIVATE_KEY",
    "DGAF_MATERIALIZATION_OUTPUT_DIR",
    "DGAF_RETENTION_ID",
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"epoch002 autopilot refused: {message}")


def run(
    *args: str,
    cwd: Path = ROOT,
    capture: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(args),
        cwd=cwd,
        check=False,
        capture_output=capture,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        fail(f"{' '.join(args)} failed: {detail}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run("git", *args, cwd=cwd).stdout.strip()


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        fail(f"required local command is unavailable: {name}")


def require_environment() -> None:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name, "").strip()]
    if missing:
        fail(f"required local environment variable is unset: {missing[0]}")


def require_repository_identity() -> None:
    top = Path(git("rev-parse", "--show-toplevel")).resolve()
    if top != ROOT.resolve():
        fail("autopilot must run from the DGAF repository containing this script")

    origin = git("remote", "get-url", "origin")
    normalized = origin.removesuffix(".git").replace("\\", "/").lower()
    if not normalized.endswith(EXPECTED_REPOSITORY.lower()):
        fail("origin does not resolve to the expected DGAF repository")


def preflight() -> None:
    for command in ("git", "gh", "openssl"):
        require_command(command)
    require_environment()
    require_repository_identity()

    run("gh", "auth", "status", "-h", "github.com", capture=True)

    validator = ROOT / VALIDATOR_REL
    run(
        sys.executable,
        str(validator),
        "--tooling-only",
        cwd=ROOT,
        capture=True,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def materialize_locally() -> tuple[Path, str]:
    verify = dispatch({"action": "verify_inputs"})
    if verify.get("status") != "PASS":
        fail("local input verification did not PASS")

    try:
        result = dispatch({"action": "materialize"})
    except SystemExit as exc:
        fail(str(exc))

    if result.get("status") != "PASS":
        fail("local materialization did not PASS")
    if result.get("primary_analysis_run") is not False:
        fail("materialization response violated primary-analysis non-execution")
    if result.get("scientific_n_increment") != 0:
        fail("materialization response violated scientific N")

    evidence_response = dispatch({"action": "get_evidence"})
    if evidence_response.get("status") != "PASS":
        fail("safe evidence retrieval did not PASS")
    evidence = evidence_response.get("evidence")
    if not isinstance(evidence, dict):
        fail("safe evidence response is malformed")

    output_dir = Path(os.environ["DGAF_MATERIALIZATION_OUTPUT_DIR"]).expanduser().resolve()
    evidence_path = output_dir / EVIDENCE_NAME
    if not evidence_path.is_file():
        fail("materialization evidence file is absent after PASS")

    evidence_sha = sha256_file(evidence_path)
    if evidence_response.get("evidence_sha256") != evidence_sha:
        fail("safe evidence digest does not match local evidence bytes")

    return evidence_path, evidence_sha


def validate_evidence_commit(worktree: Path) -> None:
    run(
        sys.executable,
        str(worktree / VALIDATOR_REL),
        "--validate-evidence-admission",
        cwd=worktree,
        capture=True,
    )


def create_admission_pr(evidence_path: Path, evidence_sha: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    for attempt in range(1, MAX_PARENT_RETRIES + 1):
        git("fetch", "origin", "main")
        baseline = git("rev-parse", "origin/main")
        branch_name = f"autopilot/epoch002-materialization-evidence-{stamp}-a{attempt}"

        temp_root = Path(tempfile.mkdtemp(prefix="dgaf-epoch002-admission-"))
        worktree = temp_root / "worktree"
        branch_created = False
        worktree_added = False

        try:
            run(
                "git",
                "worktree",
                "add",
                "-b",
                branch_name,
                str(worktree),
                baseline,
                cwd=ROOT,
                capture=True,
            )
            branch_created = True
            worktree_added = True

            destination = worktree / EVIDENCE_REL
            if destination.exists():
                fail("canonical materialization evidence is already present on current main")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(evidence_path, destination)

            status_lines = [
                line
                for line in git("status", "--porcelain", cwd=worktree).splitlines()
                if line
            ]
            expected_untracked = f"?? {EVIDENCE_REL}"
            if status_lines != [expected_untracked]:
                fail("evidence-admission worktree contains unexpected changes")

            git("add", "--", EVIDENCE_REL, cwd=worktree)
            staged = [
                line
                for line in git("diff", "--cached", "--name-only", cwd=worktree).splitlines()
                if line
            ]
            if staged != [EVIDENCE_REL]:
                fail("evidence-admission commit would change more than the canonical evidence file")

            git(
                "commit",
                "-m",
                "evidence(epoch002): admit materialization evidence",
                cwd=worktree,
            )
            validate_evidence_commit(worktree)

            parent = git("rev-parse", "HEAD^", cwd=worktree)
            if parent != baseline:
                fail("evidence-admission commit parent drifted from selected main")

            git("fetch", "origin", "main")
            latest = git("rev-parse", "origin/main")
            if latest != baseline:
                continue

            git("push", "-u", "origin", branch_name, cwd=worktree)

            body = temp_root / "pr-body.md"
            body.write_text(
                (
                    "## Purpose\n\n"
                    "Admit the operator-produced, non-secret Track A Epoch 002 "
                    "materialization evidence as the first repository event after "
                    "local controlled materialization.\n\n"
                    "## Scope\n\n"
                    f"- exactly one changed path: `{EVIDENCE_REL}`;\n"
                    f"- local evidence SHA-256: `{evidence_sha}`;\n"
                    "- evidence-admission validator PASS was required before push;\n"
                    "- no secret-bearing material is committed.\n\n"
                    "## Explicit non-effects\n\n"
                    "This PR does not create the repository MATERIALIZATION_RECEIPT, "
                    "does not authorize or run primary analysis, does not increment "
                    "scientific N, and does not establish canonical DGAF efficacy or "
                    "independent validation.\n\n"
                    "Related controller: #633.\n\n"
                    "`PRE-FREEZE / FAIL-CLOSED / PRIMARY ANALYSIS NOT AUTHORIZED / N=0`\n"
                ),
                encoding="utf-8",
            )

            create = run(
                "gh",
                "pr",
                "create",
                "--draft",
                "--base",
                "main",
                "--head",
                branch_name,
                "--title",
                "evidence(epoch002): admit local materialization evidence",
                "--body-file",
                str(body),
                cwd=worktree,
            )
            url = create.stdout.strip().splitlines()[-1] if create.stdout.strip() else ""
            if not url.startswith("https://github.com/"):
                view = run(
                    "gh",
                    "pr",
                    "view",
                    branch_name,
                    "--json",
                    "url",
                    "--jq",
                    ".url",
                    cwd=worktree,
                )
                url = view.stdout.strip()
            if not url.startswith("https://github.com/"):
                fail("evidence branch pushed but pull-request URL could not be resolved")
            return url
        finally:
            if worktree_added:
                run(
                    "git",
                    "worktree",
                    "remove",
                    "--force",
                    str(worktree),
                    cwd=ROOT,
                    capture=True,
                    check=False,
                )
            shutil.rmtree(temp_root, ignore_errors=True)

            if branch_created:
                local_branches = git("branch", "--list", branch_name)
                if local_branches:
                    run(
                        "git",
                        "branch",
                        "-D",
                        branch_name,
                        cwd=ROOT,
                        capture=True,
                        check=False,
                    )

    fail("origin/main moved during every admission attempt; safe evidence remains local")


def main() -> None:
    preflight()
    print("EPOCH002_AUTOPILOT_PREFLIGHT=PASS")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")

    evidence_path, evidence_sha = materialize_locally()
    print("EPOCH002_LOCAL_MATERIALIZATION=PASS")
    print(f"MATERIALIZATION_EVIDENCE_SHA256={evidence_sha}")
    print("SECRET_MATERIAL_RETURNED=false")

    pr_url = create_admission_pr(evidence_path, evidence_sha)
    print(f"EPOCH002_EVIDENCE_ADMISSION_PR={pr_url}")
    print("MATERIALIZATION_RECEIPT=NOT_ESTABLISHED")
    print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("AUTOPILOT_STOP=EVIDENCE_ADMISSION_PR_CREATED")


if __name__ == "__main__":
    main()
