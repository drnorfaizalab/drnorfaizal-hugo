# drnorfaizal.com — Hugo site

Personal-brand and patient-funnel site for Dr Nor Faizal Ahmad Bahuri (neurosurgeon, interventional pain). Bilingual: Bahasa Malaysia (`ms`) and English (`en`). Hosted on Cloudflare Pages, source on GitHub (`drnorfaizalab/drnorfaizal-hugo`, branch `main`).

This repo is PUBLIC. Never commit secrets, patient data or `.env`.

## Build

- Hugo 0.157.0 extended, the version set as `HUGO_VERSION` in Cloudflare Pages (Settings > Variables). Keep local builds on the same version. If `hugo` is missing, download that exact release.
- Production build: `hugo --gc --minify -d <temp dir>`. Zero errors required before any push. Never build into the repo tree (`public/` is gitignored).
- Theme lives in `themes/drnorfaizal`. Site-level overrides in `layouts/`.
- Content pairs: `index.en.md` and `index.ms.md` in each page folder. Change both or say which one was skipped.

## Deploy

- Deployment is Cloudflare Pages' own Git integration (project `drnorfaizal-hugo`, build `hugo --gc --minify`, output `public`). A push to `main` builds and goes live on drnorfaizal.com within about a minute. There is no GitHub Action deploy.
- Any other branch gets a preview build at `<hash>.drnorfaizal-hugo.pages.dev`; production is untouched.
- Cache purge is not automatic. If a deployed change does not show, purge in Cloudflare (drnorfaizal.com > Caching > Configuration > Purge Everything) via Chrome.
- Do not run `tools/deploy.sh` from cloud sessions. It needs a local `.env` and is for the home laptop only.
- Never put API tokens in chat or in the repo.

## Working rules for Claude

- Content edits and small fixes: build, then push to `main`, then report the files changed and the commit.
- Template, layout, schema, config or workflow changes: use a branch and pull request, report the build result, merge only when the user says so.
- Verify after deploy: in Chrome, open Cloudflare > Workers & Pages > drnorfaizal-hugo > Deployments and confirm the new commit shows green, then confirm the live page (title, canonical, schema).
- Commit messages: short, imperative, one line (e.g. `Add international patients page`).
- SEO invariants: canonical URLs use `https://drnorfaizal.com/`; keep hreflang pairs; keep JSON-LD (Physician, MedicalWebPage) valid; sitemap at `/sitemap.xml` and `/en/sitemap.xml`.
- Tracking (GA4, Meta Pixel, Google Ads) is hard-coded in `themes/drnorfaizal/layouts/baseof.html` with no `hugo.IsProduction` guard yet. Do not add new tracking without a guard.
