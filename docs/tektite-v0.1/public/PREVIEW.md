# Tektite v0.1 Static Preview Instructions

This document explains how to preview the static Tektite v0.1 public governance-console shell added under `docs/tektite-v0.1/public/`.

## Scope

This is a local/static preview guide only.

It does not add or authorize:

- deployment configuration;
- live repository mutation;
- rollback execution;
- production executor deployment;
- private Notion access;
- Remote Desktop Commander exposure;
- scripts or client-side automation;
- independent validation;
- canonical DGAF efficacy;
- High-Assurance status;
- certification or compliance claims.

## Files

```text
docs/tektite-v0.1/public/index.html
docs/tektite-v0.1/public/styles.css
docs/tektite-v0.1/public/PREVIEW.md
```

## Preview option A: open the file directly

From a local clone of this repository, open:

```text
docs/tektite-v0.1/public/index.html
```

in a browser.

This is sufficient for static visual review because the shell does not depend on JavaScript, package installation, private APIs, or a local server.

## Preview option B: serve the folder locally

If a browser blocks local-file behavior or a reviewer prefers a localhost URL, serve the folder with Python:

```bash
cd docs/tektite-v0.1/public
python -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080/
```

This local server is only a static file server. It does not create executor authority, deployment readiness, or public release authorization.

## Review checklist

Use this checklist for a bounded visual and content review:

- The page visibly explains Tektite as a public governance console.
- The page shows the five v0.1 sections: Home, Governance Console, Evidence Ledger, Case Studies, Services/About.
- The page shows current claim ceilings and does not hide negative status.
- The page does not imply independent validation.
- The page does not imply High-Assurance status.
- The page does not imply canonical DGAF efficacy.
- The page does not imply certification or legal compliance.
- The page does not expose private Notion, RDC, filesystem, credentials, personal logistics, or unsafe executor internals.
- The page remains understandable without running scripts or connecting services.

## Evidence ceiling preserved

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED
ROLLBACK_EXECUTION=NOT_AUTHORIZED
PRODUCTION_EXECUTOR=NOT_ESTABLISHED
```

## Next allowed steps

Allowed follow-up work remains bounded to:

- static copy review;
- static visual/UX refinement;
- accessibility review;
- evidence-link curation;
- case-study copy refinement;
- reviewer instructions.

Not allowed from this preview alone:

- treating the shell as a production deployment;
- attaching live executors;
- exposing private workspace data;
- claiming independent validation;
- claiming High-Assurance;
- claiming certification or compliance.