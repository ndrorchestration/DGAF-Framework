"""Make sibling modules (artifacts, experiment, graph_harness, seeds,
output_schema) importable when pytest is invoked from the repo root.

The pdmal_topology test modules use bare ``from <module> import ...`` style
imports that assume the package directory is on sys.path. Adding this dir to
the path during collection restores that assumption without rewriting every
test import.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
