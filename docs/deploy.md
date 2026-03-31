# Script: deploy.sh

**File:** `tools/deploy.sh`
**Purpose:** One-command build, commit, push to GitHub, and purge Cloudflare cache.

---

## How to Run

```bash
bash tools/deploy.sh
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Does — Step by Step

| Step | Action |
|------|--------|
| 1 | Loads secrets from `.env` file |
| 1b | Safety check — aborts if `.env` is accidentally tracked by Git |
| 2 | Deletes `public/` and rebuilds with `hugo --gc --minify` |
| 3 | Stages all changes with `git add .` |
| 4 | Prompts for a commit message (5-second timeout, defaults to `Site Update YYYY-MM-DD HH:MM`) |
| 5 | Pushes to `origin main` → triggers Cloudflare Pages auto-deploy |
| 6 | Purges Cloudflare edge cache via API (if credentials are present in `.env`) |

---

## Requirements

### `.env` file (project root, never committed)
```
CF_API_TOKEN=your_cloudflare_api_token
CF_ZONE_ID=your_cloudflare_zone_id
```

> The script will abort if `.env` is missing.
> If `.env` is found in Git tracking, it removes it from cache automatically and exits — fix by committing the `.gitignore` change before re-running.

### `.gitignore` must include
```
.env
```

---

## Typical Workflow

```bash
# After editing content or templates:
bash tools/deploy.sh

# You'll see:
# 🏗️  Starting Hugo Build (Minified)...
# 📦 Staging changes for GitHub...
# Enter commit message [Default: Site Update]: Add glioblastoma article
# 🚀 Pushing to GitHub...
# 🧹 Purging Cloudflare Edge Cache...
# ✅ Cache Purged Successfully.
# 🏁 Process Complete.
```

---

## Notes

- Cloudflare Pages deploys automatically on every push to `main` — the cache purge step just clears the CDN edge so visitors see the update immediately.
- If there are no changes to commit, the script skips the commit/push step silently.
- Commit message prompt times out after 5 seconds and uses the default timestamp message.
