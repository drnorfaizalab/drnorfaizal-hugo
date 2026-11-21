# Script: new_insight.py

**File:** `tools/new_insight.py`
**Purpose:** Create a bilingual insight post (EN + BM) from your raw notes. Gemini writes both versions.

Run from the project root (`drnorfaizal-hugo/`).

---

## Workflow

### 1. Create the draft

```bash
python tools/new_insight.py why-your-headache-needs-an-mri
```

Creates `content/insights/why-your-headache-needs-an-mri/draft.yaml`.

### 2. Fill in draft.yaml

| Field | Required | Notes |
| ----- | -------- | ----- |
| `title_en` | Yes | Working English title |
| `title_ms` | No | Leave blank — Gemini suggests one |
| `categories` | Yes | Use the EN names from the category table in `.claude/skills/drfaizal-editorial-engine/tools/hugo-template.md` |
| `tags` | Yes | 4–6, lowercase-hyphenated |
| `seo_focus_keyword` | Recommended | One phrase, e.g. "chronic back pain Malaysia" |
| `keywords` | Recommended | 4–6, include "Malaysia" |
| `image` | No | Defaults to `/images/insights/insights-default.jpg` |
| `cta_type` | Yes | `appointment` \| `whatsapp` \| `download` \| `none` |
| `show_appointment_button` | No | Default `true` |
| `raw_thoughts` | Yes | Write freely — Manglish, fragments, bullets. Min 50 characters. Paste any YouTube link inline |

Photos: put them in the same folder and resize to ≤1200 px wide before committing.

### 3. Generate the posts

```bash
python tools/new_insight.py why-your-headache-needs-an-mri
```

Same command again. Because `draft.yaml` now exists, the script calls Gemini (`gemini-2.5-pro`) and writes:

- `index.en.md` — English post
- `index.ms.md` — Bahasa Malaysia post, written from the draft and the English post

Existing files are never overwritten — delete one to regenerate it.

### 4. Review, build, publish

```bash
hugo server -D                                  # review both languages at localhost:1313
hugo --gc --minify -d "$TEMP/check"             # must build with zero errors
git add content/insights/why-your-headache-needs-an-mri
git commit -m "Add insight: why your headache needs an MRI"
git push                                        # live in ~1 minute via Cloudflare Pages
```

Set `draft: false` in both files before pushing.

### 5. After it's live

```bash
python tools/indexnow_submit.py /insights/<slug>/ /ms/insights/<bm-slug>/
node tools/atomise.js content/insights/<slug>/index.en.md     # social pieces → Notion
```

---

## What every generated post includes

- **FAQ** — 4–5 Q&As as `faq_schema` front matter (FAQ rich results) plus a visible FAQ section
- **Video** — a YouTube link in `raw_thoughts` becomes a `{{< youtube "ID" >}}` embed and `youtube_id` front matter
- **`seoTitle`** — added when the title runs past ~60 characters

---

## Other options

```bash
python tools/new_insight.py                 # prompts for the slug
python tools/new_insight.py --list-models   # list available Gemini models
```

## Setup

```bash
pip install google-genai python-dotenv pyyaml
```

`.env` (project root): `GEMINI_API_KEY=...`
