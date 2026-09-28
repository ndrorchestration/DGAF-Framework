from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "architecture" / "DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json"
PROFILE_BUNDLES = ROOT / "docs" / "architecture" / "DGAF_PROFILE_BUNDLE_REGISTRY.v1.json"
ASSURANCE_BUNDLES = ROOT / "docs" / "architecture" / "DGAF_ASSURANCE_BUNDLE_REGISTRY.v1.json"

AUTHORITY_TERMS = re.compile(
    r"authorization|authorize|admission|allow|deny|policy|replay|idempot|revocation|"
    r"state_machine|transition|custody|freeze|unblind|materializ|rollback|compensat|reconcil",
    re.I,
)
EVIDENCE_TERMS = re.compile(
    r"receipt|provenance|evidence|attestation|verification|claim",
    re.I,
)
PROFILE_TERMS = re.compile(
    r"aoss|track_a|epoch_|mode_t|pdmal|self_application",
    re.I,
)
ASSURANCE_TERMS = re.compile(
    r"(^|/)(test|tests|validate|validator|audit|check|lint|reconcile|derive)",
    re.I,
)

IN_SCOPE_PREFIXES = ("scripts/", "schemas/", "app/lib/", "registry/")
EXTENSIONS = {".py", ".ts", ".js", ".json", ".yaml", ".yml"}


def registered_paths() -> set[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {str(record["path"]) for record in data["records"]}


def classify(rel: str, text: str) -> str | None:
    name_authority = bool(AUTHORITY_TERMS.search(rel))
    content_authority = bool(AUTHORITY_TERMS.search(text))
    evidence = bool(EVIDENCE_TERMS.search(rel)) or bool(EVIDENCE_TERMS.search(text))

    if not (name_authority or content_authority or evidence):
        return None

    if (
        ".test." in rel
        or rel.endswith("_test.py")
        or rel.endswith("_tests.py")
        or "/tests/" in rel
        or rel.startswith("tests/")
        or ASSURANCE_TERMS.search(rel)
    ):
        return "ASSURANCE"

    if PROFILE_TERMS.search(rel):
        return "PROFILE"

    if rel.startswith(("app/lib/", "schemas/", "registry/")) and name_authority:
        return "HIGH"

    if rel.startswith("scripts/") and name_authority:
        return "HIGH"

    return "MEDIUM"


def candidates() -> dict[str, list[str]]:
    registered = registered_paths()
    buckets: dict[str, list[str]] = {
        "HIGH": [],
        "PROFILE": [],
        "MEDIUM": [],
        "ASSURANCE": [],
    }

    for prefix in IN_SCOPE_PREFIXES:
        base = ROOT / prefix
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in registered:
                continue
            if any(part in {"node_modules", "__pycache__"} for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:12000]
            except OSError:
                text = ""
            bucket = classify(rel, text)
            if bucket:
                buckets[bucket].append(rel)

    for bucket in buckets:
        buckets[bucket] = sorted(set(buckets[bucket]))
    return buckets


def profile_bundle_covered_paths(paths: list[str]) -> set[str]:
    if not PROFILE_BUNDLES.exists():
        return set()
    data = json.loads(PROFILE_BUNDLES.read_text(encoding="utf-8"))
    profiles = data.get("profiles", [])
    covered: set[str] = set()
    for path in paths:
        matches = 0
        for profile in profiles:
            globs = profile.get("path_globs", [])
            if isinstance(globs, list) and any(fnmatch.fnmatch(path, str(pattern)) for pattern in globs):
                matches += 1
        if matches == 1:
            covered.add(path)
    return covered


def assurance_bundle_covered_paths(paths: list[str]) -> set[str]:
    if not ASSURANCE_BUNDLES.exists():
        return set()
    data = json.loads(ASSURANCE_BUNDLES.read_text(encoding="utf-8"))
    bundles = data.get("bundles", [])
    covered: set[str] = set()
    for path in paths:
        matches = 0
        for bundle in bundles:
            includes = bundle.get("include_globs", [])
            excludes = bundle.get("exclude_globs", [])
            if not isinstance(includes, list) or not isinstance(excludes, list):
                continue
            included = any(fnmatch.fnmatch(path, str(pattern)) for pattern in includes)
            excluded = any(fnmatch.fnmatch(path, str(pattern)) for pattern in excludes)
            if included and not excluded:
                matches += 1
        if matches == 1:
            covered.add(path)
    return covered


def main() -> int:
    buckets = candidates()
    print("DGAF architecture ownership drift scan: ADVISORY")
    profile_covered = profile_bundle_covered_paths(buckets["PROFILE"])
    assurance_covered = assurance_bundle_covered_paths(buckets["ASSURANCE"])
    for bucket in ("HIGH", "PROFILE", "MEDIUM", "ASSURANCE"):
        items = buckets[bucket]
        if bucket == "PROFILE":
            items = [path for path in items if path not in profile_covered]
        if bucket == "ASSURANCE":
            items = [path for path in items if path not in assurance_covered]
        print(f"{bucket}_UNMAPPED={len(items)}")
        for path in items[:40]:
            print(f"{bucket}: {path}")
        if len(items) > 40:
            print(f"{bucket}: ... {len(items) - 40} additional candidates " "omitted from CLI display")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
