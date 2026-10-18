"""Paired side-effect pilot against a fake provider; non-scientific, no live integrations."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from scripts.dgaf_capability_idempotency import (
    IdempotencyConflict,
    IdempotencyInFlight,
    IdempotencyOutcomeUnknown,
    InMemoryIdempotencyLedger,
)

ROOT = Path(__file__).resolve().parents[3]
ORACLE = Path(__file__).with_name("pilot_v1.json")
ARMS = ("DGAF_REFERENCE", "CONVENTIONAL_MATCHED")


def oracle_digest(path: Path = ORACLE) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PilotLedger(Protocol):
    def claim(self, key: str, digest: str) -> Any | None: ...
    def mark_completed(self, key: str, digest: str, result: Any) -> None: ...
    def mark_unknown(self, key: str, digest: str) -> None: ...
    def reconcile_failed(self, key: str, digest: str) -> None: ...


class ConventionalConflict(RuntimeError):
    """Independent conventional-policy digest conflict."""


class ConventionalOutcomeUnknown(RuntimeError):
    """Independent conventional-policy uncertain effect."""


class ConventionalInFlight(RuntimeError):
    """Independent conventional-policy duplicate in flight."""


class ConventionalMatchedLedger:
    """Conventional policy comparator with the same permitted state features."""

    def __init__(self) -> None:
        self._records: dict[str, tuple[str, str, Any | None]] = {}

    def claim(self, key: str, digest: str) -> Any | None:
        record = self._records.get(key)
        if record is None:
            self._records[key] = (digest, "RESERVED", None)
            return None
        prior_digest, state, result = record
        if prior_digest != digest:
            raise ConventionalConflict("different digest")
        if state == "OUTCOME_UNKNOWN":
            raise ConventionalOutcomeUnknown("cannot safely retry uncertain operation")
        if state == "RESERVED":
            raise ConventionalInFlight("original operation still reserved")
        return result

    def mark_completed(self, key: str, digest: str, result: Any) -> None:
        if self._records.get(key) != (digest, "RESERVED", None):
            raise ValueError("can only complete matching reserved operation")
        self._records[key] = (digest, "COMPLETED", result)

    def mark_unknown(self, key: str, digest: str) -> None:
        if self._records.get(key) != (digest, "RESERVED", None):
            raise ValueError("can only mark matching reserved operation unknown")
        self._records[key] = (digest, "OUTCOME_UNKNOWN", None)

    def reconcile_failed(self, key: str, digest: str) -> None:
        if self._records.get(key) != (digest, "OUTCOME_UNKNOWN", None):
            raise ValueError("only an unknown matching operation can reconcile to no effect")
        del self._records[key]


class LostAcknowledgement(Exception):
    """Mock provider did not communicate a trustworthy outcome."""


@dataclass
class FakeProvider:
    """Append-only effect record owned by the test harness, not the policy arm."""

    completed_effect_ids: list[str] = field(default_factory=list)
    attempted_writes: int = 0

    def dispatch(self, operation_id: str, fault: str = "NONE") -> dict[str, str]:
        self.attempted_writes += 1
        if fault == "BEFORE_COMMIT":
            raise LostAcknowledgement("failure before observed write")
        self.completed_effect_ids.append(operation_id)
        if fault == "AFTER_COMMIT":
            raise LostAcknowledgement("ack lost after append")
        return {"effect_id": operation_id, "source": "FAKE_PROVIDER_ONLY"}


def _claim(ledger: PilotLedger, key: str, digest: str) -> str:
    try:
        cached = ledger.claim(key, digest)
    except (IdempotencyOutcomeUnknown, ConventionalOutcomeUnknown):
        return "RECONCILE_REQUIRED"
    except (IdempotencyInFlight, ConventionalInFlight):
        return "IN_FLIGHT"
    except (IdempotencyConflict, ConventionalConflict):
        return "CONFLICT"
    return "CLAIMED" if cached is None else "REPLAY_COMPLETED"


def _execute(
    ledger: PilotLedger,
    provider: FakeProvider,
    decisions: list[str],
    *,
    key: str,
    digest: str,
    fault: str = "NONE",
) -> None:
    first_claim_has_reservation = decisions[0] == "CLAIMED" and decisions[-1] == "IN_FLIGHT"
    new_claim_has_reservation = decisions[-1] == "CLAIMED"
    if not (first_claim_has_reservation or new_claim_has_reservation):
        raise ValueError("dispatch only by a currently accepted, reserved caller")
    try:
        result = provider.dispatch(key, fault=fault)
    except LostAcknowledgement:
        ledger.mark_unknown(key, digest)
        decisions.append("OUTCOME_UNKNOWN")
        return
    ledger.mark_completed(key, digest, result)
    decisions.append("COMPLETED")


def _run(case: dict[str, Any], arm: str) -> dict[str, Any]:
    if arm not in ARMS:
        raise ValueError("unsupported arm")
    ledger: PilotLedger = InMemoryIdempotencyLedger() if arm == "DGAF_REFERENCE" else ConventionalMatchedLedger()
    provider = FakeProvider()
    key, digest = f"{case['id']}:operation", "fixed-request-digest-v1"
    decisions = [_claim(ledger, key, digest)]
    mode = case["mode"]

    if mode == "NORMAL_SUCCESS":
        _execute(ledger, provider, decisions, key=key, digest=digest)
        decisions.append(_claim(ledger, key, digest))
    elif mode == "ACK_LOST_AFTER_COMMIT":
        _execute(ledger, provider, decisions, key=key, digest=digest, fault="AFTER_COMMIT")
        decisions.append(_claim(ledger, key, digest))
    elif mode == "DUPLICATE_INTERLEAVING":
        decisions.append(_claim(ledger, key, digest))
        _execute(ledger, provider, decisions, key=key, digest=digest)
        decisions.append(_claim(ledger, key, digest))
    elif mode == "CONFIRMED_NO_EFFECT_THEN_FRESH_RETRY":
        _execute(ledger, provider, decisions, key=key, digest=digest, fault="BEFORE_COMMIT")
        decisions.append(_claim(ledger, key, digest))
        # An independently governed external verifier is NOT present in this toy system.
        # This proof is instead directly read from a separately maintained in-process fake-provider log.
        if provider.completed_effect_ids:
            raise RuntimeError("BLOCKED_NON_EFFECT_PROOF_MISSING")
        decisions.append("NON_EFFECT_OBSERVED")
        ledger.reconcile_failed(key, digest)
        decisions.append("FRESH_AUTHORIZATION_SIMULATED")
        decisions.append(_claim(ledger, key, digest))
        _execute(ledger, provider, decisions, key=key, digest=digest)
    else:
        raise ValueError(f"unsupported scenario mode: {mode}")

    oracle_decisions = case["expected_decisions"]
    oracle_effects = case["expected_effect_count"]
    expected_sequence = decisions == oracle_decisions
    expected_count = len(provider.completed_effect_ids) == oracle_effects
    no_duplicate_completed_effects = len(provider.completed_effect_ids) == len(set(provider.completed_effect_ids))
    return {
        "case_id": case["id"],
        "arm": arm,
        "decisions": decisions,
        "fake_provider_attempts": provider.attempted_writes,
        "observed_completed_effects": list(provider.completed_effect_ids),
        "oracle_expected_effect_count": oracle_effects,
        "oracle_expected_decisions": oracle_decisions,
        "matches_operator_local_oracle": expected_sequence and expected_count and no_duplicate_completed_effects,
        "decision_sequence_matches": expected_sequence,
        "effect_count_matches": expected_count,
        "no_duplicate_completed_effects": no_duplicate_completed_effects,
        "human_active_minutes": None,
        "actual_external_effect": False,
    }


def run(oracle_path: Path = ORACLE, expected_sha256: str | None = None) -> dict[str, Any]:
    actual_sha = oracle_digest(oracle_path)
    if expected_sha256 is None:
        raise RuntimeError("BLOCKED_ORACLE_DIGEST_NOT_SUPPLIED")
    if expected_sha256 != actual_sha:
        raise RuntimeError("BLOCKED_ORACLE_DIGEST_MISMATCH")
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    scenarios = oracle["scenarios"]
    ids = [item["id"] for item in scenarios]
    if ids != ["GOV2-01", "GOV2-04", "GOV2-05", "GOV2-06"]:
        raise RuntimeError("BLOCKED_UNEXPECTED_SCENARIO_SET")
    rows = [_run(case, arm) for case in scenarios for arm in ARMS]
    same_results = all(
        rows[i]["decisions"] == rows[i + 1]["decisions"]
        and rows[i]["observed_completed_effects"] == rows[i + 1]["observed_completed_effects"]
        for i in range(0, len(rows), 2)
    )
    return {
        "version": "DGAF_V2_FAKE_PROVIDER_EFFECT_PILOT_V1",
        "scope": "OPERATOR_LOCAL_SYNTHETIC_ENGINEERING_NOT_INDEPENDENTLY_VALIDATED",
        "oracle_verification": "HASH_MATCHED_OPERATOR_AUTHORED_NOT_EXTERNAL",
        "oracle_sha256": actual_sha,
        "source_revision": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip(),
        "scenario_count": len(scenarios),
        "arm_count": len(ARMS),
        "rows": rows,
        "summary": {
            "operator_oracle_matches": sum(row["matches_operator_local_oracle"] for row in rows),
            "total_rows": len(rows),
            "arm_parity": same_results,
            "external_provider_effects": 0,
            "human_workload_measurements": 0,
            "scientific_n_increment": 0,
        },
        "limitations": [
            "In-process fake provider, not a connected service or independent custody",
            "Deterministic interleaving, not concurrent cross-machine execution",
            "Oracle is operator authored; not prospectively independent or confirmatory",
            "Comparator is matched conventional idempotency code, not a deployed OPA integration",
            "No real human minutes, operational maintenance costs, or provider latency measured",
            "No safety superiority or generality beyond these four deterministic scenarios",
        ],
        "claim_ceiling": {
            "SCIENTIFIC_N_INCREMENT": 0,
            "INDEPENDENT_VALIDATION": "NOT_ESTABLISHED",
            "CANONICAL_DGAF_EFFICACY": "NOT_ESTABLISHED",
            "HIGH_ASSURANCE": "NOT_AUTHORIZED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-oracle-sha256", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = run(expected_sha256=args.expected_oracle_sha256)
    except (RuntimeError, ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return (
        0
        if (
            report["summary"]["operator_oracle_matches"] == report["summary"]["total_rows"]
            and report["summary"]["arm_parity"]
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
