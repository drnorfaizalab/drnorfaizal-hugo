# Script: new_insight.py

**File:** `tools/new_insight.py`
**Purpose:** Pipeline for creating bilingual Hugo insights posts — from raw draft to polished EN + BM markdown via Claude Code (no API key required).

---

## How to Run

```bash
# Interactive — prompts for a topic/slug
python tools/new_insight.py

# Direct — pass the slug
python tools/new_insight.py my-topic-slug

# Optimize photos in a slug folder only
python tools/new_insight.py --photos --slug my-topic-slug

# Optimize photos + print ready-to-paste prompts for Claude Code
python tools/new_insight.py --prepare --slug my-topic-slug

# List all drafts that have draft.yaml but no index.en.md
python tools/new_insight.py --all
```

Run from the project root (`drnorfaizal-hugo/`).

---

## Workflow

### Step 1 — Create a draft scaffold

```bash
python tools/new_insight.py why-your-headache-needs-an-mri
```

Creates:

```text
content/insights/why-your-headache-needs-an-mri/
└── draft.yaml
```

### Step 2 — Fill in the draft

Open `draft.yaml` in VS Code. Fill in:

- `title_en` — working title
- `categories` / `tags` — drives the filter tabs on the Insights page
- `raw_thoughts` — write freely (Manglish, bullet points, fragments are fine)
- `photos` — list any images you're dropping in the folder
- `seo_focus_keyword` — single phrase that shapes how Claude writes the post

Drop any photos into the same folder alongside `draft.yaml`.

### Step 3 — Optimize photos + get prompts

```bash
python tools/new_insight.py --prepare --slug why-your-headache-needs-an-mri
```

This will:

1. **Optimize all photos** in the slug folder in-place — resize to max 1200px wide, compress (JPEG quality 82, PNG optimize, WebP quality 82), replace originals.
2. **Print two prompts** to the terminal — ready to paste into Claude Code.

### Step 4 — Generate posts via Claude Code

Paste **Prompt 1** into Claude Code → get `index.en.md` content → save the file.

Then paste **Prompt 2** into Claude Code (replacing the `<PASTE index.en.md CONTENT HERE>` placeholder with the output from Prompt 1) → get `index.bm.md` content → save the file.

### Step 5 — Review and publish

Open both files, tweak anything that needs adjusting. When satisfied:

```bash
git add content/insights/why-your-headache-needs-an-mri/
git commit -m "insight: why-your-headache-needs-an-mri"
git push
```

---

## Setup

### Install dependencies

```bash
pip install pyyaml Pillow  # YAML parser + image processing
```

No API key needed — content generation runs through your Claude Code session.

---

## Photo Optimization

Run standalone at any time (before or independent of `--prepare`):

```bash
python tools/new_insight.py --photos --slug my-topic-slug
```

| Setting | Value |
| ------- | ----- |
| Max width | 1200 px (aspect ratio preserved) |
| JPEG quality | 82 (progressive, optimize) |
| PNG | optimize=True |
| WebP quality | 82, method=6 |
| Formats handled | `.jpg` `.jpeg` `.png` `.webp` |

Originals are replaced in-place. Run before committing.

---

## draft.yaml Fields Reference

| Field | Required | Notes |
| ----- | -------- | ----- |
| `title_en` | Yes | Working English title |
| `title_bm` | No | Leave blank — Claude will suggest |
| `date` | Yes | Auto-filled as today |
| `categories` | Yes | Drives the filter tab — see insights-article-template.md |
| `tags` | Yes | Additional SEO keywords |
| `description_en` | No | Leave blank — Claude will write |
| `description_bm` | No | Leave blank — Claude will write |
| `seo_focus_keyword` | Recommended | Single phrase, e.g. "chronic back pain Malaysia" |
| `og_image` | No | Filename in the post folder |
| `cta_type` | Yes | `appointment` \| `whatsapp` \| `download` \| `none` |
| `raw_thoughts` | Yes | Your unfiltered notes — Claude cleans these up |
| `photos` | No | List of filenames + captions |

---

## Notes

- Re-running `--prepare` regenerates the prompts; it does not overwrite existing markdown files — you save those manually.
- `raw_thoughts` is your voice — write messily, Claude will restructure it.
- `--all` lists pending slugs with the exact commands to run, it does not auto-process them.
