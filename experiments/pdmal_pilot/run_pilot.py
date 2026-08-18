#!/usr/bin/env python3
"""Fail-closed PDMAL experiment runner.

Contract mode is the only executable mode while the protocol is PRE-FREEZE.
Pilot mode is intentionally unavailable until both protocol freeze and explicit
authorization are present. This module never silently upgrades modes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from time import monotonic

from harness_contract import deterministic_contract_run, stream_fingerprint
from task_engine import AttemptStatus, RetryPolicy, ScriptedTask, execute_trial

SUPPORTED_MODES = {"contract", "pilot"}
CONTRACT_ROOT_SEEDS = (20260817, 20260818)


def require_contract_mode() -> None:
    mode = os.getenv("PDMAL_MODE")
    if mode not in SUPPORTED_MODES:
        raise SystemExit("PDMAL_MODE must be explicitly set to 'contract' or 'pilot'.")


def write_contract_artifact(output_dir: Path, seed: int, payload: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
    }
    path = output_dir / f"contract_seed_{seed}.json"
    raw = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{digest}  {path.name}\n", encoding="utf-8"
    )


def run_contract(output_dir: Path) -> int:
    key = b"contract-only-test-key-000000000000000000"
    for seed in CONTRACT_ROOT_SEEDS:
        results = deterministic_contract_run(seed, key)
        if len(results) != 5 or not all(r.topology_valid for r in results):
            raise SystemExit(f"contract validation failed for seed {seed}")

        scripted = ScriptedTask([AttemptStatus.FAILURE, AttemptStatus.SUCCESS])
        trial = execute_trial(
            scripted,
            seed=seed,
            condition="CONTRACT_ONLY",
            policy=RetryPolicy(recovery_window_seconds=0.0),
            monotonic_clock=monotonic,
            sleeper=lambda _: None,
        )
        if not trial.ffcr_success:
            raise SystemExit(f"retry contract failed for seed {seed}")

        write_contract_artifact(
            output_dir,
            seed,
            {
                "seed": seed,
                "stream_fingerprint": stream_fingerprint(seed),
                "topology_contracts": [result.__dict__ for result in results],
                "retry_contract": {
                    "status": trial.status.value,
                    "ffcr_success": trial.ffcr_success,
                    "recovery_wait_seconds": trial.recovery_wait_seconds,
                    "attempts": [
                        {
                            "attempt": attempt.attempt,
                            "status": attempt.status.value,
                            "elapsed_seconds": attempt.elapsed_seconds,
                            "isolated": attempt.isolated,
                            "termination_reason": attempt.termination_reason,
                        }
                        for attempt in trial.attempts
                    ],
                },
            },
        )

    print(
        "CONTRACT_MODE_PASS: two validation seeds exercised; "
        "no empirical data collection performed"
    )
    return 0


def run_pilot() -> int:
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit(
            "pilot execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required"
        )
    if os.getenv("PDMAL_PILOT_AUTHORIZED") != "1":
        raise SystemExit(
            "pilot execution prohibited: PDMAL_PILOT_AUTHORIZED=1 is required"
        )
    raise SystemExit(
        "pilot execution unavailable: real experimental task executor is not implemented; "
        "no data collected"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=Path("test-artifacts"))
    args = parser.parse_args(argv)

    require_contract_mode()
    mode = os.environ["PDMAL_MODE"]
    if mode == "contract":
        if args.seeds != 2:
            raise SystemExit("contract mode is fixed at 2 validation seeds")
        return run_contract(args.output_dir)
    return run_pilot()


if __name__ == "__main__":
    raise SystemExit(main())
