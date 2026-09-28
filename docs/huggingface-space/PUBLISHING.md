# Publishing the DGAF Hugging Face Static Space

This directory is a self-contained source package for a Hugging Face **Static Space**.

## Why static

The Space is intentionally presentation-only. DGAF governance and the bounded proof runtime remain on the accepted Vercel deployment. The Hugging Face surface must not become a second policy engine, issuer, execution adapter, or evidence authority.

## Files to publish

Copy the contents of this directory into the root of a new Hugging Face Space repository:

- `README.md`
- `index.html`
- `evidence.json`

The root `README.md` already contains the required Space metadata with `sdk: static` and `app_file: index.html`.

## Recommended Space settings

- Visibility: **Public**
- SDK: **Static**
- No secrets required
- No variables required
- No compute runtime required
- No duplicated DGAF server logic

## Acceptance after publishing

Verify:

1. the Space loads without authentication;
2. the primary CTA opens the accepted DGAF live demo;
3. the GitHub source link is correct;
4. the evidence identity shown in the Space matches `evidence.json`;
5. no page copy implies independent validation, canonical efficacy, certification, or High-Assurance authorization;
6. the Space itself performs no governance decision or execution.

## Boundary

The Hugging Face Space has:

`presentation_effect=NONE`

`authority_effect=NONE`

The accepted live proof remains a same-system bounded engineering demonstration.
