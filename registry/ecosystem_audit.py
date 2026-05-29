#!/usr/bin/env python3
"""Ecosystem Registry Audit — Amethyst/COLLEEN co-orchestration tool.

Compares ecosystem_registry.json against live GitHub repos for ndrorchestration.
Emits: unregistered repos, missing-in-github projects, and TODO deployment stubs.

Usage:
    GITHUB_TOKEN=<your-token> python ecosystem_audit.py
    REGISTRY_PATH=registry/ecosystem_registry.json python ecosystem_audit.py
"""
import os
import json
import sys
import requests

GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "ndrorchestration")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REGISTRY_PATH = os.environ.get("REGISTRY_PATH", "registry/ecosystem_registry.json")


def load_registry(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def fetch_github_repos(owner: str) -> list[dict]:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/search/repositories?q=user:{owner}&per_page=50&page={page}"
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        repos.extend(items)
        if len(items) < 50:
            break
        page += 1
    return repos


def run_audit():
    registry = load_registry(REGISTRY_PATH)
    projects = registry.get("projects", [])
    reg_keys = {f"{p['github']['owner']}/{p['github']['repo']}": p for p in projects if p.get("github")}

    print(f"Registry v{registry.get('registry_version')} — {len(projects)} projects loaded.")

    gh_repos = fetch_github_repos(GITHUB_OWNER)
    gh_keys = {r["full_name"]: r for r in gh_repos}
    print(f"GitHub — {len(gh_keys)} repos found for {GITHUB_OWNER}.")

    missing_in_registry = sorted(set(gh_keys) - set(reg_keys))
    missing_in_github = sorted(set(reg_keys) - set(gh_keys))

    print("\n=== REPOS IN GITHUB BUT NOT IN REGISTRY ===")
    if missing_in_registry:
        for key in missing_in_registry:
            r = gh_keys[key]
            print(f"  UNREGISTERED  {key}  (private={r.get('private')}, archived={r.get('archived')})")
    else:
        print("  None — registry is complete.")

    print("\n=== PROJECTS IN REGISTRY BUT MISSING FROM GITHUB ===")
    if missing_in_github:
        for key in missing_in_github:
            p = reg_keys[key]
            print(f"  MISSING  {key}  (id={p.get('id')}, lifecycle={p.get('lifecycle_state')})")
    else:
        print("  None — all registry projects have corresponding GitHub repos.")

    print("\n=== DEPLOYMENT TODO STUBS ===")
    for p in projects:
        for d in p.get("deployments", []):
            if str(d.get("url", "")).startswith("TODO") or str(d.get("project_id", "")).startswith("TODO"):
                print(f"  FILL_IN  {p['id']}  platform={d['platform']}  url={d.get('url')}")

    print("\n=== LIFECYCLE SUMMARY ===")
    from collections import Counter
    states = Counter(p.get("lifecycle_state") for p in projects)
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")

    print("\n=== PATTERN COVERAGE ===")
    from collections import defaultdict
    pattern_map = defaultdict(list)
    for p in projects:
        for pat in p.get("patterns", []):
            pattern_map[pat].append(p["id"])
    for pat, ids in sorted(pattern_map.items()):
        print(f"  {pat}: {len(ids)} projects")


if __name__ == "__main__":
    run_audit()
