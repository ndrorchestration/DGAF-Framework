# CI Dependency Hash-Lock Proof — 2026-09-24

## Scope

This record documents the first canonical adoption tranche for Issue #943. It hardens the **CI evidence-gate toolchain** used by `Python Tests & Quality Checks`; it does not redefine application/runtime compatibility or any scientific dependency contract.

## Source contract

- direct input: `requirements-ci.txt`
- source SHA-256: `1abada5e8dabbcb6706e33c5b5dfa30c45b784e8b9a9b18166a52562b5c3dfa9`
- resolver: `pip==26.2.1`
- pip wheel SHA-256 verified before resolver installation: `71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e`
- platform scope: Ubuntu 24.04 x64
- proof PR: #984, exact proof head `61129f93e2eab7245557918294446eedc80b819d`
- proof PR disposition: **CLOSED / NOT MERGED**

Every proof lane resolved wheel artifacts only, emitted artifact SHA-256 values, reinstalled its generated lock in a fresh virtual environment with `pip --require-hashes --only-binary=:all:`, and passed `pip check`.

## Accepted interpreter locks

| Python lane | Packages | Resolved-set SHA-256 | Proof artifact ID | Canonical lock SHA-256 |
| --- | ---: | --- | ---: | --- |
| 3.10 | 65 | `7b7f6edb9c686b921d1450aabc3c8345ec6cb41ca84a6feadd16210dafb3c4e3` | 10799922222 | `18206a193da4de952c25d5384187edd82fa134eb4a9a3c5322f6999258a6d05c` |
| 3.11 | 63 | `dabebe2879148dfed404f1163f17c248ba01ce7b98778782f9c6c12f9acac14d` | 10800271087 | `ff5111b07dc1949c06a6a364722bdece93f1f10e70a0c6e719704c091096344d` |
| 3.12 | 63 | `7931d5f2ad8b22cbd71dea2cc60ce4c1f8a3b4ccde34a46be0fa5e284526fba9` | 10799643634 | `d131e53fc8c8506ee282f4082eae451af77b45c08c37b69fce091b4bca865197` |

The canonical lock files differ from the raw #984 proof files only in provenance comments added before adoption; package/version/hash bodies are unchanged and must be revalidated on the adoption PR exact head.

## Why one universal lock is rejected

The proof observed real cross-minor divergence. Python 3.10 resolved 65 packages while 3.11/3.12 resolved 63. Python 3.10 alone required `backports-asyncio-runner==1.2.0` and `exceptiongroup==1.3.1`. It also resolved `rpds-py==0.30.0` and `stevedore==5.8.0`, while 3.11/3.12 resolved `rpds-py==2026.6.3` and `stevedore==5.9.1`. Multiple compiled packages also selected interpreter-specific wheel hashes.

## Python 3.12 patch evidence

Exact proof lanes for Python 3.12.0, 3.12.3, and current 3.12.14 produced the identical 63-package artifact set with resolved-set SHA-256 `7931d5f2ad8b22cbd71dea2cc60ce4c1f8a3b4ccde34a46be0fa5e284526fba9`. Their package/version/hash bodies were byte-for-byte identical. The 3.12 lock is therefore admitted for the current Ubuntu 24.04 x64 3.12 patch consumers, subject to exact-head workflow validation.

## First adoption tranche

Only `.github/workflows/python-tests.yml` is migrated here:

- staging evidence: Python 3.11 lock;
- quality matrix: Python 3.10 / 3.11 / 3.12 matching locks;
- integration wrapper: Python 3.11 lock, with redundant direct `pyyaml` overlay removed;
- security scan: Python 3.11 lock;
- all CI-toolchain installs use `--require-hashes --only-binary=:all:`;
- exact `pip==26.2.1` is bootstrapped only after its wheel SHA-256 is verified.

## Second adoption tranche — control-plane pandas overlay

Temporary proof PR #986, exact head `fb26ea011fbc4eb50457a640173a18d6c1a1b314`, resolved `requirements-ci.txt + pandas==3.0.5` under Python 3.12, 3.12.0, and 3.12.3 on Ubuntu 24.04 x64.

All three proof lanes produced an identical 66-package artifact set:

- resolved-set SHA-256: `e18eb434f83c2f0e2801f218c77b1fbb8db76526dc57c57a734b3f12a3ed7b41`;
- package/body SHA-256: `a793e17998fb403a214cd362fbae68f586e09540e806eb9c2626add52c6b483b`;
- pandas overlay literal SHA-256: `0f7011f8e062802ab40c0bcfa852c079b99f0097f1a3ea085d2eacfef42263f9`;
- canonical control-plane lock SHA-256: `208c68c614cbb4a3e17dfc7eaeffdd39b57ee3688f3b662c7c22e7e64d802b70`.

The control-plane workflow is migrated to Ubuntu 24.04, exact pip bootstrap, and the single augmented Python 3.12 lock using `--require-hashes --only-binary=:all:`. The separate unbound `pandas==3.0.5` install is removed.

## Remaining #943 scope

Issue #943 remains OPEN after this tranche. Other current `requirements-ci.txt` consumers are not migrated by this change. Scientific/runtime locks remain outside this maintenance surface.

## Non-effects

This change does not authorize experiments, change candidate/freeze/preregistration/custody/analysis state, increment scientific N, establish efficacy or independent validation, or authorize High-Assurance operation.
