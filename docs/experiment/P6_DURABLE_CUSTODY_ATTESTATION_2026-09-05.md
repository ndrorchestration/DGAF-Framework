# P6 Durable Evidence Custody — Current Candidate Attestation — 2026-09-05

**Status:** CURRENT-CANDIDATE ROUND-TRIP VERIFIED  
**Candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Purpose

Record the current-candidate P6 archive → independent retrieval → SHA-256 verification event. This is evidence-custody verification only. It does not close P4, bind P7/P8, establish a freeze, authorize a pilot, unblind data, or create empirical observations.

The historical file `docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION.md` remains preserved as historical/non-transferable evidence and is not reused here.

## Independent archive target

- Provider: Google Drive
- Folder: `DGAF PDMAL Evidence Archive — 7c1cc4bb — 2026-09-05`
- Folder ID: `1cbmvw8abh6m09M9YZRbRZ4kvsBlH2BLL`
- Archive scope: exact current-candidate engineering evidence artifacts

## Final current evidence set

| Evidence | GitHub run | GitHub artifact | GitHub ZIP SHA-256 | Drive file ID | Retrieved SHA-256 | Result |
|---|---:|---:|---|---|---|---|
| P3/P5 source, final mainline | `33939955138` | `9961526468` | `ed947f8a2f21a1e1122a6e8950240ea4a3ebdec7aad04c4231698de2f250285b` | `1c0SVv-8ed07f3sk89EfYbpWKHh6TsKzb` | `ed947f8a2f21a1e1122a6e8950240ea4a3ebdec7aad04c4231698de2f250285b` | PASS |
| P3/P5 registry, final mainline | `33939955138` | `9961526662` | `d7f592b45e76978600b6f1a4f22cac4b97dfe5f60605accbd99b61c50e149e93` | `1KLvCmf_s9_bP6to8nES5Wz64emrcbPZU` | `d7f592b45e76978600b6f1a4f22cac4b97dfe5f60605accbd99b61c50e149e93` | PASS |
| P4 synthetic operational source, mainline | `33939574283` | `9961339739` | `ea820d4c7a0dafab59a72d536f3f25e2e2adfd81173106d6ac56eb9490b49874` | `1u-on8QQycm5rESjHgp3wyjV2G2U9Trvz` | `ea820d4c7a0dafab59a72d536f3f25e2e2adfd81173106d6ac56eb9490b49874` | PASS |
| P4 synthetic operational registry, mainline | `33939574283` | `9961339938` | `544d28828b22f5adc24aee38486fbeac59a1d17fe6da252aa3b6582468829669` | `1jkfDr4sDkd31YHL5b4iFWT5AocwqU_if` | `544d28828b22f5adc24aee38486fbeac59a1d17fe6da252aa3b6582468829669` | PASS |

The final P3/P5 source artifact also binds its inner evidence JSON digest as `d6b7c85a80a2ecf8e857431ab1b132d2dd703176cb481c0e67fbc0d067fe3175`. The P4 source registry binds its inner evidence JSON digest as `c9bf326496a4682d33221f02499be404de406b8ffbdcfd9a4300c9e27e4ff42b`.

## Retrieval procedure

Each listed GitHub artifact was downloaded from its producing workflow run, uploaded as raw ZIP bytes to the candidate-scoped Google Drive folder, fetched back from Google Drive as raw bytes, and independently re-hashed with SHA-256 outside the producing GitHub workflow. Every retrieved hash matched the original GitHub artifact digest exactly.

The final P3/P5 Drive files were created and independently retrieved on 2026-09-05 UTC. The P4 files were likewise independently retrieved after archival. This satisfies the active P6 requirement for a real archive/retrieval/hash event rather than repository-local retention alone.

## Additional retained predecessor evidence

The same archive also contains the prior mainline P3/P5 evidence pair from run `33939308694`:

- source artifact `9961311877`, Drive ID `1Eem9TrBQGFCViHt3DNsubzldBQ5sT8vv`, ZIP SHA-256 `da75d4cc625555ac7abbbf17bd4698a46cfb9a90aafca46d4da8a73998f3d5c8`, retrieval PASS;
- registry artifact `9961312150`, Drive ID `1UrCoeHqEwPQjE2suZZuING4vHLJRxcwY`, ZIP SHA-256 `a7251361b75765dc5d3148678832956cb15a9dbb8aae7bbd84f5b002075a7897`, retrieval PASS.

These are retained for lineage/audit continuity; the final P3 adjudication uses the later run `33939955138`, which adds exact-candidate pilot artifact matrix/adversarial contract coverage.

## P6 adjudication

The P6 closure condition is durable archive plus independent retrieval/hash proof. The current candidate now has a separately located archive, stable object identifiers, retrieved raw bytes, independently recomputed SHA-256 digests, and exact equality for the finalized evidence set.

**P6 result: CLOSED / VERIFIED for candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.**

## Explicit non-claims

- P4 human/key custody separation remains unestablished.
- P5 final analysis implementation/configuration binding remains separate pre-freeze work.
- P7 final scientific binding remains open.
- P8 and P9 are not executed/closed by this custody event.
- Freeze is NOT ESTABLISHED.
- Pilot authorization is NOT GRANTED.
- No empirical workload was executed.
- No unblinding occurred.
- Empirical N remains `0`.
