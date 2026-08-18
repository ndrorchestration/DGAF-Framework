#!/usr/bin/env python3
"""Fail-closed PDMAL experiment runner.

Contract mode is the only executable mode while the protocol is PRE-FREEZE.
Pilot mode is intentionally unavailable until both protocol freeze and explicit
pilot authorization are present. This module never silently upgrades modes.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from harness_contract import deterministic_contract_run

SUPPORTED_MODES = {"contract", "pilot"}


def require_contract_mode() -> None:
    mode = os.getenv("PDMAL_MODE")
    if mode not in SUPPORTED_MODES:
        raise SystemExit("PDMAL_MODE must be explicitly set to 'contract' or 'pilot'.")


def run_contract() -> int:
    key = b"contract-only-test-key-000000000000000000"
    results = deterministic_contract_run(20260817, key)
    if len(results) != 5 or not all(r.topology_valid for r in results):
        raise SystemExit("contract validation failed")
    print("CONTRACT_MODE_PASS: no empirical data collection performed")
    return 0


def run_pilot() -> int:
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("pilot execution prohibited: PDMAL_PROTOCOL_FROZEN=1 is required")
    if os.getenv("PDMAL_PILOT_AUTHORIZED") != "1":
        raise SystemExit("pilot execution prohibited: PDMAL_PILOT_AUTHORIZED=1 is required")
    # Deliberately fail closed until the protocol-bound real task executor is
    # implemented and separately verified. A mode flag alone must never create
    # experimental evidence.
    raise SystemExit(
        "pilot execution unavailable: real experimental task executor is not implemented; no data collected"
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
        args.output_dir.mkdir(parents=True, exist_ok=True)
        return run_contract()
    return run_pilot()


if __name__ == "__main__":
    raise SystemExit(main())
