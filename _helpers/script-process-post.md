# Script: process-post.sh

**File:** `scripts/process-post.sh`
**Purpose:** Send a single article to Gemini CLI for medical authority editing and bilingual translation.

---

## How to Run

```bash
bash scripts/process-post.sh content/insights/your-article/index.en.md
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Does

1. Takes a single markdown file as input
2. Passes it to the Gemini CLI with instructions from `GEMINI.md`
3. Gemini edits the article for medical authority and tone
4. Gemini translates it and saves the output as the paired language version in the same folder

| Input file | Output created |
|------------|---------------|
| `index.en.md` | `index.bm.md` (Bahasa translation) |
| `index.bm.md` | `index.en.md` (English translation) |

The editing rules and tone guidelines are defined in `GEMINI.md` at the project root.

---

## Requirements

- Gemini CLI installed and authenticated (`gemini` command available in terminal)
- `GEMINI.md` present at project root — this is the SOP Gemini follows for tone and authority

---

## Typical Workflow

```bash
# 1. Write your draft in English
#    content/insights/trigeminal-neuralgia/index.en.md

# 2. Run process-post to edit + generate BM version
bash scripts/process-post.sh content/insights/trigeminal-neuralgia/index.en.md

# 3. Review both files before publishing
# 4. Set draft: false when ready
# 5. Deploy
bash scripts/deploy.sh
```

---

## Notes

- Always review Gemini's output before setting `draft: false` — treat it as a first draft, not a final.
- Works on any path inside `content/` — not limited to `insights/`.
- The script does not modify front matter — categories, tags, and date must be set manually.
