# DOFT Website

This directory contains the public-facing website for DOFT — Delayed
Oscillator Field Theory.

The website combines an editorial overview with a figure-led Study 06 page for
a physics audience. It introduces the working hypothesis, separates current
evidence from long-term interpretation, maps Studies 01–06, and links every
summary back to its source record.

## Editorial principles

- Lead with the physical question rather than the project history.
- Distinguish measurements, causal results, model-dependent interpretations,
  falsifications, and open conjectures.
- Treat negative results and retractions as part of the research record.
- Keep study code and data in their source repositories.
- Do not import or execute anything from `legacy/`.
- Use English throughout the public site.

The Spanish Study 06 HTML supplied as a design and content reference remains a
local-only file named `draft.html`. It is intentionally ignored by Git.

## Local development

Requirements: Node.js 22.13 or newer.

```bash
npm install
npm run dev
```

The local server normally starts at <http://localhost:3000>.

## Verification

```bash
npm run lint
npm test
```

`npm test` builds the site and verifies its server-rendered HTML. No hosting
credentials or live deployment are required.

## Main files

- `app/page.tsx` — website content and semantic structure
- `app/dynamics/page.tsx` — Study 06 figures and in-depth evidence discussion
- `app/globals.css` — visual system and responsive layout
- `app/layout.tsx` — metadata and document shell
- `public/doft-social-card.jpg` — generated editorial social-preview image
- `public/figures/` — English re-renderings of the versioned Study 06 charts
- `scripts/generate_dynamics_figures.py` — reproducible figure generator

## Public routes

| Route | Purpose |
| --- | --- |
| `/` | Global DOFT overview |
| `/dynamics/` | Study 06 dynamics, figures, notation, and evidence limits |

## GitHub Pages

The deployment workflow is
`.github/workflows/deploy-website-pages.yml`. It builds the static website from
`website/` and publishes `website/out/`.

The production URL is:

<https://doft.space/>

The static build is configured for the root of that domain. It intentionally
does not add the repository name as a URL prefix.

In the GitHub repository settings, select **Settings → Pages → Source: GitHub
Actions**, set the custom domain to `doft.space`, and enable HTTPS after GitHub
finishes provisioning the certificate. GitHub ignores `CNAME` files when Pages
is published with a custom Actions workflow, so no such file is required here.

## Evidence date

The first version reflects the central index and the versioned Study 06 record
reviewed on 24 July 2026. Study 06 remains active, so public claims should be
updated only after their source verdicts are sealed.
