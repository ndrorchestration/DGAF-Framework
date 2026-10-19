# Cold reproduction — Ubuntu 24.04 / Python 3.12

**State: operator-local engineering only; NOT independent scientific evidence.**
This document describes the general Python regression path, distinct from
the cross-repository DGAF operator self-test and outside-operator trials.

## Preconditions and precise scope

- Clone the complete Git history. History-aware tests need old commit and
  blob identities. CI runs with fetch-depth: 0. Check that Git reports
  is-shallow-repository = false.
- Ubuntu 24.04 x86_64, Python 3.12.x; the matching requirements lock is
  requirements-ci-py312-ubuntu2404-x64.lock. It is platform-specific.
- The Vercel runtime Python constraint in pyproject.toml does not replace
  the separate 3.10/3.11 CI requirements locks.
- Choose the *exact reviewed SHA*, not an unqualified rolling main.
- No private experimental archives or production credentials are needed.

## Tested cold-drill command sequence

~~~bash
git clone https://github.com/ndrorchestration/DGAF-Framework.git
cd DGAF-Framework
git rev-parse --is-shallow-repository    # require false
git checkout --detach 0e09ae555136fb9d433c7294f445e0b656c7e705
git status --short                       # require clean
python3.12 -m venv .venv
. .venv/bin/activate
bash scripts/bootstrap_ci_pip.sh
python -m pip install --disable-pip-version-check \
  --require-hashes --only-binary=:all: \
  -r requirements-ci-py312-ubuntu2404-x64.lock
python -m pytest tests/ -q --timeout=30 -p no:cacheprovider -rs
git status --short
~~~

The checkout SHA is the dated historical baseline of the October 18 cold
drill, not a fresh declaration of main. Record actual OS, Python, pip,
requirements blob, Git commit, test exit status and raw skipped-item reasons.
Do not transfer historical test counts to newer exact heads.

For off-main Epoch 004 evidence, the frozen commit
9725ffd80d5386826d61b7f824524f7f8d89fce8 is currently reachable
from remote branch solo-canonical-epoch-004/run-20260907-001.
Do not rewrite historical evidence to satisfy Git lookup.

## Result classification and skip disclosure

- PASS means an assertion actually executed on the recorded source.
- SKIP means a test or whole module was not run; inspect pytest -rs.
  Three explicit Issue #32 live multi-agent trace cases remain skipped.
- BLOCKED means a missing Git object, unavailable private bytes,
  environment mismatch or permission, not automatically an app defect.
- Collection and execution test counts may differ; reconcile from raw
  collect-only and full test logs rather than dismissing mismatches.
- pandas is available in a separate control-plane lock; a 3.12 general
  lock alone does not prove the pandas-dependent path was covered.

The historical cold-drill observer reported 2047 passed / 5 skipped on
full Git history; these numbers have NOT been independently reproduced
by this documentation. The previously skipped ensemble_v16 quick
module caught a nonexistent ApogeeReviewer symbol and a nonexistent
_build_default_pdmal helper under a generic ImportError skip. Its
replacement tests assert the current public API instead and should
fail visibly if current required symbols disappear. Historical tests
remain available in Git history; old behavior was not resurrected.

General Python tests generate the staging-circuit-breaker receipt at
test-artifacts/staging-circuit-breaker-evidence.json, and the Python
workflow explicitly uploads this named evidence. This *single generated
file* is ignored to avoid local git-status noise; the rest of
test-artifacts/ is not ignored and must remain visible for custody
inspection. Preserve required evidence outside a disposable checkout.
Do not confuse an ignored local file with admitted research evidence.

## Evidence that this procedure does NOT establish

- Private Epoch 002 retained archive content or its unpublished estimate.
- Independent custody, blinding, fidelity or prospective ground truth.
- A replay of Epoch 004 dataset and key contents merely from recorded
  artifact IDs and SHA-256 metadata.
- Live provider effects, human effort, external validation, efficacy,
  scientific N increment or high-assurance permission.

As of October 18, GitHub metadata reports that the separate Epoch 004
dataset artifact 10039138297 and protected key artifact 10039138610
are present and expire December 7, 2026. This is metadata, not a
content-level replay; never expose protected keys to improve publicity.

SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.
