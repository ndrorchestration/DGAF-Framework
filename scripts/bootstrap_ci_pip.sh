#!/usr/bin/env bash
set -euo pipefail

PIP_VERSION="26.2.1"
PIP_WHEEL="pip-26.2.1-py3-none-any.whl"
PIP_SHA256="71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e"

bootstrap_dir="${RUNNER_TEMP:-/tmp}/dgaf-ci-pip-bootstrap"
rm -rf "$bootstrap_dir"
mkdir -p "$bootstrap_dir"

python -m pip download   --disable-pip-version-check   --only-binary=:all:   --no-deps   --dest "$bootstrap_dir"   "pip==$PIP_VERSION"

test "$(sha256sum "$bootstrap_dir/$PIP_WHEEL" | awk '{print $1}')" = "$PIP_SHA256"

python -m pip install   --disable-pip-version-check   --no-index   --find-links "$bootstrap_dir"   "pip==$PIP_VERSION"

test "$(python -m pip --version | awk '{print $2}')" = "$PIP_VERSION"
rm -rf "$bootstrap_dir"
