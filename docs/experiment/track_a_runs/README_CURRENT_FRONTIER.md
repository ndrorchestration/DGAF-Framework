# Track A Epoch 002 — Current Frontier Pointer

This file is a routing aid only. It is not a scientific event, gate record, authorization record, or source of independent authority.

Current accepted predecessor chain:

- repository custody-v2: **ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT**;
- precollection preflight: **ACCEPTED**;
- immutable freeze: **ESTABLISHED**;
- final closure: **ACCEPTED**;
- verification classification: **NOT ACCEPTED**;
- collection authorization: **NOT ESTABLISHED**;
- empirical collection: **NOT AUTHORIZED / NOT EXECUTED**;
- scientific N: **0**.

Controlling issue: #523.

Current maintenance prerequisite: PR #665 on exact head `336534603b2374ccfcec0342ae80734f6efc086e`. GitHub checks are green, but that exact head remains externally held by its Vercel build-rate-limit status. Evidence from another SHA does not transfer.

After #665 is accepted on exact-head evidence, the next scientific transition must be a fresh one-file verification-classification event created from the resulting exact accepted `main`. Verification classification remains non-authorizing; collection authorization is a separate human-controlled event.

For the live repository summary, use `docs/CURRENT_STATE.md`. For immutable event evidence, use the canonical records in this directory and their exact Git history.
