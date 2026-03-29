# Script: new_insight.py

**File:** `scripts/new_insight.py`
**Purpose:** Full pipeline for creating bilingual Hugo insights posts — from raw draft to polished EN + BM markdown via Claude.

---

## How to Run

```bash
# Interactive — prompts for a topic/slug
python scripts/new_insight.py

# Direct — pass the slug
python scripts/new_insight.py my-topic-slug

# Process an existing draft through Claude
python scripts/new_insight.py --process --slug my-topic-slug

# Process all drafts that have draft.yaml but no index.en.md
python scripts/new_insight.py --all

# Preview output without saving files
python scripts/new_insight.py --process --slug my-topic-slug --dry-run
```

Run from the project root (`drnorfaizal-hugo/`).

---

## Workflow

### Step 1 — Create a draft scaffold

```bash
python scripts/new_insight.py why-your-headache-needs-an-mri
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

### Step 3 — Process through Claude

```bash
python scripts/new_insight.py --process --slug why-your-headache-needs-an-mri
```

Claude produces:

- `index.en.md` — polished English post (400–700 words)
- `index.bm.md` — natural Bahasa Melayu translation

### Step 4 — Review and publish

Open both files, tweak anything Claude missed. When satisfied:

```bash
git add content/insights/why-your-headache-needs-an-mri/
git commit -m "insight: why-your-headache-needs-an-mri"
git push
```

---

## Setup

### Install dependencies

```bash
pip install anthropic python-dotenv pyyaml
```

### API key

Add to `.env` at the project root:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

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

- You can re-run `--process` to regenerate — it overwrites `index.en.md` and `index.bm.md`.
- `raw_thoughts` is your voice — write messily, Claude will restructure it.
- Outputs stream to terminal in real time so you can watch progress.
