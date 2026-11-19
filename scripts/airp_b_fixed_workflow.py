#!/usr/bin/env python3
"""AIRP B-FIXED: source-locked, synthetic-only, predetermined workflow baseline.

Research adapter over DGAF's existing ClaimGraph validator, Evidence Gate and
read-only attribution query. In-process snapshots ONLY; no persistent store,
external effects, new policy authority, or scientific evaluation.
"""

from __future__ import annotations

import base64
import binascii
import copy
import hashlib
import json
import re
import sys
import threading
from pathlib import Path

from components.evidence_gate import (
    ClaimScope,
    EvidenceObject,
    EvidenceTarget,
    ProvenanceBinding,
    admit_evidence,
)
from scripts.claimgraph_attribution_query import query_attribution
from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]

PROTECTED_MAIN = "1a95b94332dffb404c5a3ce026d70781a8c10b90"
LOCKED_GIT_BLOBS = {
    "docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json": (
        "ebea3130335c50716352e7aa6c749069bbd8b832"
    ),
    "docs/research/STRUCTURAL_EPISTEMICS_CLAIM_RECORD_SCHEMA.json": "bed1d9a57ef25a94a70379b9af99d2d0fcbb54a6",
    "docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json": "77f097d261289d9f595e8c4ae465b97d5b3ce64a",
    "scripts/validate_structural_epistemics_claim_graph.py": "d24e2798e305f76beca5b9ecfcb91ba8fa6ba847",
    "scripts/claimgraph_attribution_query.py": "e3ed75a9e3a0eb6b4a01754894df32bf10985b2a",
    "components/evidence_gate.py": "5878aa314813cd0770754c3c6fe14311ee8b117c",
}
FIXTURE = "docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json"
OPS = {"add_claim", "attach_evidence", "challenge", "fork", "inspect", "compare"}
MUTATIONS = {"add_claim", "attach_evidence", "challenge", "fork"}
ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9._-]{0,95}$")
BRANCH_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{0,47}$")
MAX_STEPS = 50
MAX_BRANCHES = 16
MAX_EVIDENCE_BYTES = 65536


def _digest(value: object) -> str:
    """Deterministic local fingerprint, NOT an authenticity signature."""
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()


def _git_blob(path: Path) -> str:
    data = path.read_bytes()
    # Git blob identity, not proof of independent custody.
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data, usedforsecurity=False).hexdigest()


def verify_source_locks() -> None:
    for relative, expected in LOCKED_GIT_BLOBS.items():
        if _git_blob(ROOT / relative) != expected:
            raise ValueError(f"SOURCE_LOCK_MISMATCH: {relative}")


def _closed(args: dict, expected: set[str]) -> None:
    if not isinstance(args, dict) or set(args) != expected:
        raise ValueError(f"ARGS_FIELDS_MISMATCH: expected {sorted(expected)}")


def _id(value: object) -> str:
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        raise ValueError("INVALID_SCOPED_IDENTIFIER")
    return value


def _version(snapshots: list[dict], version: int) -> dict:
    if type(version) is not int or version < 0 or version >= len(snapshots):
        raise ValueError("UNKNOWN_SNAPSHOT_VERSION")
    return snapshots[version]


class FixedWorkflow:
    """Serialized, isolated, preplanned baseline; not an agent-facing instrument."""

    def __init__(self) -> None:
        verify_source_locks()
        source = json.loads((ROOT / FIXTURE).read_text(encoding="utf-8"))
        validate_claim_graph(source)
        self._branches: dict[str, list[dict]] = {"base": [source]}
        self._cache: dict[tuple[str, str], tuple[str, dict]] = {}
        self._log: list[dict] = []
        self._lock = threading.RLock()

    @property
    def lineage(self) -> list[dict]:
        return copy.deepcopy(self._log)

    def snapshot(self, branch: str = "base", version: int | None = None) -> dict:
        """Returns a copy; callers cannot mutate an accepted snapshot."""
        with self._lock:
            versions = self._branches[branch]
            selected = len(versions) - 1 if version is None else version
            return copy.deepcopy(_version(versions, selected))

    def execute(self, command: dict) -> dict:
        """One deterministic step, guarded by in-process CAS and idempotency."""
        with self._lock:
            if not isinstance(command, dict) or set(command) != {
                "op",
                "branch",
                "expected_version",
                "request_id",
                "args",
            }:
                return self._reject("INVALID_COMMAND_ENVELOPE")
            op = command["op"]
            branch = command["branch"]
            request_id = command["request_id"]
            if (
                not isinstance(op, str)
                or op not in OPS
                or not isinstance(branch, str)
                or not isinstance(request_id, str)
            ):
                return self._reject("UNSUPPORTED_OPERATION_OR_IDENTITY")
            if not BRANCH_PATTERN.fullmatch(branch) or not ID_PATTERN.fullmatch(request_id):
                return self._reject("INVALID_BRANCH_OR_REQUEST_ID")
            try:
                fingerprint = _digest(command)
            except (TypeError, ValueError):
                return self._reject("INVALID_JSON_COMMAND")
            key = (branch, request_id)
            if key in self._cache:
                old_fingerprint, old_receipt = self._cache[key]
                if old_fingerprint != fingerprint:
                    return self._reject("IDEMPOTENCY_KEY_CONFLICT")
                return copy.deepcopy(old_receipt)
            try:
                result = self._execute_uncached(command)
            except (ValueError, KeyError, TypeError, IndexError, binascii.Error) as exc:
                # No mutations committed before all existing validators succeed.
                result = self._reject(f"REJECTED: {exc}")
            if len(self._log) < MAX_STEPS:
                event = {
                    "request_id": request_id,
                    "branch": branch,
                    "op": op,
                    "command_digest": fingerprint,
                    "status": result["status"],
                    "version": result.get("version"),
                }
                event["local_event_digest"] = _digest(event)
                self._log.append(event)
            self._cache[key] = (fingerprint, copy.deepcopy(result))
            return copy.deepcopy(result)

    @staticmethod
    def _reject(reason: str) -> dict:
        return {
            "status": "REJECTED",
            "reason": reason,
            "truth_effect": "NONE",
            "authorization_effect": "NONE",
            "independence_effect": "NONE",
            "external_effects": "NONE",
        }

    @staticmethod
    def _accept(**fields: object) -> dict:
        return {
            "status": "ACCEPTED_SYNTHETIC_ONLY",
            "truth_effect": "NONE",
            "authorization_effect": "NONE",
            "independence_effect": "NONE",
            "external_effects": "NONE",
            **fields,
        }

    def _execute_uncached(self, command: dict) -> dict:
        op, branch, args = command["op"], command["branch"], command["args"]
        if branch not in self._branches:
            raise ValueError("UNKNOWN_BRANCH")
        versions = self._branches[branch]
        actual = len(versions) - 1
        expected = command["expected_version"]
        if type(expected) is not int or expected != actual:
            raise ValueError("STALE_OR_INVALID_EXPECTED_VERSION")
        if len(self._log) >= MAX_STEPS:
            raise ValueError("STEP_BUDGET_EXCEEDED")
        graph = copy.deepcopy(versions[-1])
        if op == "inspect":
            _closed(args, {"attribution_observation"})
            validate_claim_graph(graph)
            attribution = None
            if args["attribution_observation"] is not None:
                attribution = query_attribution(graph, args["attribution_observation"])
            return self._accept(
                branch=branch,
                version=actual,
                state_digest=_digest(graph),
                state=graph,
                attribution=attribution,
                state_changed=False,
            )
        if op == "compare":
            _closed(args, {"other_branch", "other_version"})
            other = _version(self._branches[args["other_branch"]], args["other_version"])
            validate_claim_graph(other)
            return self._accept(
                branch=branch,
                version=actual,
                state_changed=False,
                comparison=self._compare(graph, other),
            )
        if op == "fork":
            _closed(args, {"new_branch"})
            new_branch = args["new_branch"]
            if not isinstance(new_branch, str) or not BRANCH_PATTERN.fullmatch(new_branch):
                raise ValueError("INVALID_NEW_BRANCH")
            if new_branch in self._branches or len(self._branches) >= MAX_BRANCHES:
                raise ValueError("BRANCH_ALREADY_EXISTS_OR_LIMIT")
            validate_claim_graph(graph)
            self._branches[new_branch] = [graph]
            return self._accept(
                branch=branch,
                version=actual,
                new_branch=new_branch,
                new_branch_version=0,
                state_digest=_digest(graph),
                state_changed=False,
            )
        metadata = {}
        if op == "add_claim":
            _closed(args, {"claim_id", "proposition"})
            claim_id = _id(args["claim_id"])
            proposition = args["proposition"]
            if not isinstance(proposition, str) or not proposition.strip() or len(proposition) > 5000:
                raise ValueError("INVALID_PROPOSITION")
            if any(claim["claim_id"] == claim_id for claim in graph["claims"]):
                raise ValueError("DUPLICATE_CLAIM")
            claim = copy.deepcopy(graph["claims"][0])
            claim.update(
                {
                    "claim_id": claim_id,
                    "proposition": proposition,
                    "claim_class": "HYPOTHESIS",
                    "epistemic_state": "PROPOSED",
                    "verification_status": "NOT_VERIFIED",
                    "authorization_relevance": "NONE",
                    "applicability_state": "CURRENT",
                    "supporting_evidence_ids": [],
                    "contradicting_evidence_ids": [],
                    "defeaters": [],
                    "supersedes": [],
                    "superseded_by": [],
                    "retraction": {"state": "NOT_RETRACTED", "reason": None},
                    "causal_level": "ASSOCIATION",
                }
            )
            graph["claims"].append(claim)
        elif op == "challenge":
            _closed(args, {"claim_id", "counterevidence_id"})
            claim = self._claim(graph, args["claim_id"])
            evidence_id = args["counterevidence_id"]
            evidence = next(
                (item for item in graph["evidence"] if item["evidence_id"] == evidence_id),
                None,
            )
            if evidence is None or evidence["evidence_class"] != "COUNTEREVIDENCE":
                raise ValueError("COUNTEREVIDENCE_NOT_FOUND")
            if evidence_id in claim["supporting_evidence_ids"] or evidence_id in claim["contradicting_evidence_ids"]:
                raise ValueError("DUPLICATE_OR_CONFLICTING_EVIDENCE_RELATION")
            claim["contradicting_evidence_ids"].append(evidence_id)
            claim["applicability_state"] = "CHALLENGED"
            suffix = _digest(command)[:16].upper()
            claim["defeaters"].append(
                {
                    "defeater_id": f"DEF-BFIX-{suffix}",
                    "condition": "synthetic referenced counterevidence",
                    "status": "TRIGGERED",
                }
            )
            graph["relations"].append(
                {
                    "relation_id": f"REL-BFIX-C-{suffix}",
                    "relation_type": "CONTRADICTS",
                    "source_id": evidence_id,
                    "target_id": claim["claim_id"],
                    "scope": "AIRP synthetic only",
                }
            )
        elif op == "attach_evidence":
            _closed(args, {"claim_id", "evidence_node", "evidence_object", "evidence_bytes_b64"})
            claim = self._claim(graph, args["claim_id"])
            node = args["evidence_node"]
            item = args["evidence_object"]
            if not isinstance(node, dict) or not isinstance(item, dict):
                raise ValueError("INVALID_EVIDENCE_OBJECTS")
            evidence_id = _id(node["evidence_id"])
            if evidence_id != item["evidence_id"]:
                raise ValueError("EVIDENCE_ID_MISMATCH")
            if node["evidence_class"] != "DERIVATION":
                raise ValueError("SYNTHETIC_DERIVATION_ONLY")
            if any(e["evidence_id"] == evidence_id for e in graph["evidence"]):
                raise ValueError("DUPLICATE_EVIDENCE")
            encoded = args["evidence_bytes_b64"]
            if not isinstance(encoded, str) or len(encoded) > 90000:
                raise ValueError("EVIDENCE_BYTES_LIMIT")
            data = base64.b64decode(encoded, validate=True)
            if not data or len(data) > MAX_EVIDENCE_BYTES:
                raise ValueError("EVIDENCE_BYTES_LIMIT")
            _closed(item, {"evidence_id", "evidence_type", "digest_algorithm", "content_digest", "source_class"})
            if item["source_class"] != "SYNTHETIC_TEST":
                raise ValueError("SYNTHETIC_SOURCE_ONLY")
            evidence = EvidenceObject(**item)
            target = EvidenceTarget(
                target_type="CLAIMGRAPH",
                target_id=graph["graph_id"],
                scope_id="AIRP-SYNTHETIC",
                source_revision=PROTECTED_MAIN,
            )
            provenance = ProvenanceBinding(producer_class="INTERNAL_SAME_SYSTEM", custody_class="SYNTHETIC_TEST")
            scope = ClaimScope(
                claim_id=claim["claim_id"],
                claim_class=claim["claim_class"],
                scope_id="AIRP-SYNTHETIC",
                evidence_class=node["evidence_class"],
                limitations=("SYNTHETIC_ONLY",),
                excluded_claims=("EFFICACY", "INDEPENDENCE", "AUTHORIZATION"),
            )
            admission = admit_evidence(
                evidence,
                target,
                provenance,
                scope,
                evidence_bytes=data,
                expected_target=target,
                required_producer_class="INTERNAL_SAME_SYSTEM",
            )
            if not admission.admitted:
                raise ValueError(f"EVIDENCE_GATE_REJECTED: {admission.reason_code}")
            graph["evidence"].append(copy.deepcopy(node))
            claim["supporting_evidence_ids"].append(evidence_id)
            suffix = _digest(command)[:16].upper()
            graph["relations"].append(
                {
                    "relation_id": f"REL-BFIX-S-{suffix}",
                    "relation_type": "SUPPORTS",
                    "source_id": evidence_id,
                    "target_id": claim["claim_id"],
                    "scope": "AIRP synthetic only",
                }
            )
            metadata = {
                "admission_class": "EVIDENCE_GATE_ADMITTED_SYNTHETIC_ONLY",
                "evidence_digest": admission.verified_digest,
                "admission_authorization_effect": "NONE",
            }
        else:
            raise ValueError("UNSUPPORTED_OPERATION")
        validate_claim_graph(graph)
        # Atomic only within this single in-process lock; no disk or distributed CAS.
        versions.append(graph)
        return self._accept(
            branch=branch,
            version=len(versions) - 1,
            state_digest=_digest(graph),
            state_changed=True,
            **metadata,
        )

    @staticmethod
    def _claim(graph: dict, claim_id: str) -> dict:
        for item in graph["claims"]:
            if item["claim_id"] == claim_id:
                return item
        raise ValueError("UNKNOWN_CLAIM")

    @staticmethod
    def _compare(left: dict, right: dict) -> dict:
        def indexed(graph: dict, key: str, identifier: str) -> dict[str, dict]:
            return {item[identifier]: item for item in graph[key]}

        changes = {}
        for key, identifier in (("claims", "claim_id"), ("evidence", "evidence_id"), ("relations", "relation_id")):
            a, b = indexed(left, key, identifier), indexed(right, key, identifier)
            changes[key] = {
                "only_left": sorted(a.keys() - b.keys()),
                "only_right": sorted(b.keys() - a.keys()),
                "changed": sorted(k for k in a.keys() & b.keys() if a[k] != b[k]),
            }
        return {
            "left_digest": _digest(left),
            "right_digest": _digest(right),
            "structural_difference_only": changes,
            "semantic_oracle_effect": "NONE",
        }

    def run_plan(self, plan: dict) -> dict:
        """B-FIXED runs a predeclared sequence; no agent feedback-loop branching."""
        if not isinstance(plan, dict) or set(plan) != {"record_type", "schema_version", "source_commit", "steps"}:
            raise ValueError("INVALID_FIXED_PLAN")
        if (plan["record_type"], plan["schema_version"], plan["source_commit"]) != (
            "AIRP_B_FIXED_PLAN",
            1,
            PROTECTED_MAIN,
        ):
            raise ValueError("INVALID_PLAN_IDENTITY")
        steps = plan["steps"]
        if not isinstance(steps, list) or not 1 <= len(steps) <= MAX_STEPS:
            raise ValueError("INVALID_STEP_COUNT")
        results = []
        for step in steps:
            result = self.execute(step)
            results.append(result)
            if result["status"] == "REJECTED":
                break
        return {
            "record_type": "AIRP_B_FIXED_RESULT",
            "schema_version": 1,
            "source_commit": PROTECTED_MAIN,
            "outcome": (
                "STOPPED_ON_REJECTION"
                if len(results) < len(steps) or results[-1]["status"] == "REJECTED"
                else "COMPLETED_SYNTHETIC_ONLY"
            ),
            "step_results": results,
            "lineage": self.lineage,
            "scientific_n_increment": 0,
            "independent_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
            "authorization_effect": "NONE",
            "external_effects": "NONE",
        }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.airp_b_fixed_workflow <disposable-plan.json>", file=sys.stderr)
        return 2
    try:
        plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = FixedWorkflow().run_plan(plan)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["outcome"] == "COMPLETED_SYNTHETIC_ONLY" else 2
    except (ValueError, TypeError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc), "authorization_effect": "NONE"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
