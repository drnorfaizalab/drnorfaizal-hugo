# drnorfaizal.com — Hugo site

Personal-brand and patient-funnel site for Dr Nor Faizal Ahmad Bahuri (neurosurgeon, interventional pain). Bilingual: Bahasa Malaysia (`ms`) and English (`en`). Hosted on Cloudflare Pages, source on GitHub (`drnorfaizalab/drnorfaizal-hugo`, branch `main`).

This repo is PUBLIC. Never commit secrets, patient data or `.env`.

## Build

- Hugo 0.123.7 extended (pinned in `.github/workflows/build-deploy.yml`). If `hugo` is missing, download that exact release.
- Production build: `hugo --gc --minify -d <temp dir>`. Zero errors required before any push. Never build into the repo tree (`public/` is gitignored).
- Theme lives in `themes/drnorfaizal`. Site-level overrides in `layouts/`.
- Content pairs: `index.en.md` and `index.ms.md` in each page folder. Change both or say which one was skipped.

## Deploy

- Push to `main` triggers GitHub Actions: build, deploy to Cloudflare Pages, purge Cloudflare cache.
- Pull requests run the build only.
- Do not run `tools/deploy.sh` from cloud sessions. It needs a local `.env` and is for the home laptop only.
- Secrets live in GitHub (Settings > Secrets > Actions): `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CF_ZONE_ID`, optional `CF_CACHE_TOKEN`.

## Working rules for Claude

- Content edits and small fixes: build, then push to `main`, then report the files changed and the commit.
- Template, layout, schema, config or workflow changes: use a branch and pull request, report the build result, merge only when the user says so.
- Verify after deploy: check the Actions run is green, then confirm the live page (title, canonical, schema) in Chrome.
- Commit messages: short, imperative, one line (e.g. `Add international patients page`).
- SEO invariants: canonical URLs use `https://drnorfaizal.com/`; keep hreflang pairs; keep JSON-LD (Physician, MedicalWebPage) valid; sitemap at `/sitemap.xml` and `/en/sitemap.xml`.
- Tracking (GA4, Meta Pixel, Google Ads) is hard-coded in `themes/drnorfaizal/layouts/baseof.html` with no `hugo.IsProduction` guard yet. Do not add new tracking without a guard.
