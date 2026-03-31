# Script: quick-start.sh

**File:** `scripts/quick-start.sh`
**Purpose:** Interactive menu for common Hugo development tasks — content creation, local server, builds, git, and site stats.

---

## How to Run

```bash
bash scripts/quick-start.sh
```

Run from the project root (`drnorfaizal-hugo/`).

---

## Menu Options

```
Content Creation:
  1) Create new blog post
  2) Create new specialty page
  3) Create new patient guide

Development:
  4) Start local server (with drafts)
  5) Build site for production
  6) Clean build

Git & Deployment:
  7) Show git status
  8) Commit and push changes
  9) Show recent commits

Utilities:
 10) List all content
 11) Check for broken links
 12) Show site statistics

  0) Exit
```

---

## What Each Option Does

| Option | Action |
|--------|--------|
| 1 | Prompts for a slug, runs `hugo new content blog/<slug>/` for both `.en.md` and `.bm.md` |
| 2 | Same for `expertise/<slug>/` |
| 3 | Same for `patients/guides/<slug>/` |
| 4 | Runs `hugo server --buildDrafts --disableFastRender` |
| 5 | Deletes `public/`, runs `hugo --minify` |
| 6 | Deletes `public/` and `resources/`, runs `hugo --minify` |
| 7 | Shows `git status` and last 10 commits |
| 8 | Stages all, prompts for commit message, optionally pushes to `origin main` |
| 9 | Shows last 15 commits |
| 10 | Counts `.en.md` and `.bm.md` files by section |
| 11 | Runs `hugo --printMemoryStats` (basic integrity check) |
| 12 | Reports content file count, project size, and build size |

---

## Notes

- The script `cd`s to the Hugo project root automatically — safe to run from any directory.
- Option 8 prompts before staging and before pushing — no accidental commits.
- For insights posts, prefer the dedicated `scripts/new_insight.py` pipeline over option 1.
