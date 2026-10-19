# V2 operational-effects engineering pilot

This is separate from PR #1362's OPA fixed-fixture calibration.

A fake provider records in-process side-effect events. Paired implementations
use the repository's DGAF reference idempotency ledger and a separately
implemented conventional ledger with matching stateful capabilities. Four
author-designed scenarios cover a valid action, lost acknowledgement after
commit, duplicate interleaving, and verified local non-effect followed by a
fresh simulated attempt.

The operator-local expected results are pinned by SHA-256:
1d4312938a5847c6e000faa73a10c0660108044aebc84319b45be414bd4f34d0.

Run with repository hash-locked Python 3.12 dependencies from the root:

~~~bash
python -m experiments.governance_benchmark.effect_pilot.run_pilot \
  --expected-oracle-sha256 1d4312938a5847c6e000faa73a10c0660108044aebc84319b45be414bd4f34d0
python -m pytest tests/test_governance_benchmark_v2_effect_pilot.py -q
~~~

The fixed fixture digest binds operator-authored expectations, not an
independent adjudication. Matching traces are local engineering evidence only.
No real provider, external custody, real concurrency, independent review, or
human task duration is represented by this pilot.
