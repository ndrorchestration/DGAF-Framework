# Python 3.10 isolated-auditor diagnostic — noncanonical research

**2026-10-27 — pending exact-hosted verification.** This draft proof branch is stacked on security candidate [#1546](https://github.com/ndrorchestration/DGAF-Framework/pull/1546), NOT protected main, canonical package locks or signed bootstrap. The parent hosted proof established an incompatible dependency path in the Python 3.10 CI toolchain: `pip-audit 2.10.1 → CacheControl[filecache] → filelock 4.1.0`, resulting in **six non-waived CVE findings**. The reported fixed filelock >=4.2.1 requires Python >=3.11.

## Experimental separation, NOT an audit waiver

The new `scripts/proof_py310_audit_isolation.py` deliberately creates **one temporary requirements source** from the unchanged parent candidate `requirements-ci.txt`, deleting exactly the `pip-audit==2.10.1` **scanner** line and no other direct pin. It asserts the source's other pins remain identical. Then under Ubuntu 24.04 x64 and **Python 3.10**, pip 26.2.1 resolves its full transitive wheel set and writes a deterministic *test-only* SHA-256 per-wheel lock and manifest. A fresh Python 3.10 environment must install it with `--require-hashes --only-binary=:all:`, pass `pip check`, import the research test toolchain, and affirm the external auditor and scanner-only filelock dependency are not installed.

A separate **Python 3.11** auditor consumes an already **hosted verified** Python 3.11 hash-lock artifact from parent proof run 40466036612 (artifact `12716284080`), verifies the exact lock SHA-256 `c29bde77a4fdd192eb3285991e5752c749bb0ec5ad11450a65b28d4b459d104e`, installs it in an isolated fresh 3.11 venv with `--require-hashes`, and performs a **non-waived `pip-audit --local` on itself**. It then uses pip-audit's documented `--require-hashes --disable-pip -r` mode to scan the **complete Python 3.10 workload lock** with no dependency re-resolution. The diagnostic script compares every audited name and version against every package in the hash lock and fails closed if any package is skipped, extra, substituted, or vulnerable.

This proves only the possible **architecture** of separating the scanner from the 3.10 workload and retaining full vulnerability coverage. It does **not** prove that this separation is equivalent to the current canonical CI environment, because direct pins and signed lock contract tests would require a reviewed change. Even a successful test cannot promote the new lock or approve the change automatically. No `--ignore-vuln` or security-scan bypass exists.

## Acceptance and limits

- The proof workflow is run only for this isolated draft head and uploads the test source, resolver report, hash lock, freeze, JSON audit and manifests with 14-day retention, even on failures.
- Existing baseline hosted CI hash-lock proofs for the original complete source continue unchanged and **must still report the Python3.10 failure** until a reviewed replacement security architecture is admitted.
- An accepted candidate requires independently verified scanner lock provenance, complete toolchain inventory, all original Python3.10 tests, audit no-known-vulnerabilities, the three version-specific contracts and re-signed canonical hashes; none is authorized by this proof.
- The original Black, certifi and setuptools remediation proof remains separate; source pins are unchanged in this experiment.

No protected main, production runtime, scientific results or authorization effects. `DGAF_V1_RELEASE=HOLD`, `SCIENTIFIC_N_INCREMENT=0`, `HIGH_ASSURANCE=NOT_AUTHORIZED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`. Issues [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530) remain OPEN.
