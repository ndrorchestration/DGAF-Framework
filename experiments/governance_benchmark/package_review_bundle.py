"""Create a reproducible DGAF governance-benchmark review bundle."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
MANIFEST_PATH = ROOT / "build_evidence_manifest.py"

spec = importlib.util.spec_from_file_location("benchmark_manifest", MANIFEST_PATH)
assert spec and spec.loader
manifest_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest_module)


def load_json_script(script: str) -> Any:
    completed = subprocess.run(
        ["python", str(ROOT / script)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def encode_canonical(value: Any) -> bytes:
    canonical = manifest_module.canonicalize(value)
    return (json.dumps(canonical, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_bundle(output: Path) -> dict[str, str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    files: dict[str, bytes] = {
        "evidence-manifest.json": encode_canonical(manifest_module.build_manifest()),
        "evidence-envelope.json": encode_canonical(load_json_script("build_evidence_envelope.py")),
        "fixed-benchmark.json": encode_canonical(manifest_module.benchmark.run()),
        "mutations.json": encode_canonical(manifest_module.mutations.run_mutations()),
        "same-domain-interactions.json": encode_canonical(manifest_module.interactions.run_interactions()),
        "cross-domain-interactions.json": encode_canonical(
            manifest_module.cross_domain.run_cross_domain_interactions()
        ),
    }

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    handoff = (
        "# DGAF Governance Benchmark Review Bundle\n\n"
        f"Repository commit: `{head}`\n\n"
        "Verification class: same-system engineering evidence.\n\n"
        "All JSON payloads in this archive are canonicalized for reproducibility; "
        "informational runtime timing is excluded.\n\n"
        "Regenerate the bundle from this exact commit and compare canonical digests. "
        "This bundle does not establish independent validation, canonical efficacy, "
        "SOTA status, scientific-N increment, regulatory compliance, or High-Assurance authorization.\n"
    ).encode("utf-8")
    files["REVIEWER_HANDOFF.md"] = handoff

    sums = "".join(f"{sha256_bytes(files[name])}  {name}\n" for name in sorted(files)).encode("ascii")
    files["SHA256SUMS.txt"] = sums

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, files[name])

    return {name: sha256_bytes(data) for name, data in files.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    checksums = build_bundle(args.output)
    print(json.dumps({"output": str(args.output), "files": checksums}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
