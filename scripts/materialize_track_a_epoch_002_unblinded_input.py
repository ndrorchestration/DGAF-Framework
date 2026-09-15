#!/usr/bin/env python3
"""Controlled Stage-1 materializer for Track A Epoch 002."""

from __future__ import annotations

import argparse

PRIMARY_ANALYSIS_MARKER = "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-archive", required=True)
    parser.add_argument("--protected-archive", required=True)
    parser.add_argument("--custody-private-key", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser


if __name__ == "__main__":
    build_parser().parse_args()
    print(PRIMARY_ANALYSIS_MARKER)
