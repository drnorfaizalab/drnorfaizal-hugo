# Script: process_post.py

**File:** `scripts/process_post.py`
**Purpose:** Edit and translate a Hugo content file using the Claude API, governed by the Dr. Faizal brand brief in `GEMINI.md`.

---

## How to Run

```bash
python scripts/process_post.py content/insights/your-article/index.en.md
```

Run from the project root (`drnorfaizal-hugo/`).

---

## What It Does

1. Reads the brand brief and SOP from `GEMINI.md`
2. Sends the source file to Claude (Sonnet) with the brief as the system prompt
3. Claude returns two outputs in a single API call:
   - **Edited source** — refined for medical authority, tone, and precision
   - **Translated mirror** — paired-language version following the correct voice
4. Both files are written to the same folder

| Input file | Output created |
|------------|----------------|
| `index.en.md` | `index.bm.md` (Bahasa Melayu translation) |
| `index.bm.md` | `index.en.md` (English translation) |

The source file is also overwritten with the edited version.

---

## Setup

### 1. Install dependency

```bash
pip install anthropic
```

### 2. Add API key

Add to your `.env` file at the project root (already excluded from Git):

```
ANTHROPIC_API_KEY=sk-ant-...
```

Or set it in your shell environment:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Requirements

- Python 3.8+
- `anthropic` package (`pip install anthropic`)
- `ANTHROPIC_API_KEY` in `.env` or environment
- `GEMINI.md` present at project root — this is the SOP Claude follows for tone and authority

---

## Typical Workflow

```bash
# 1. Write your draft in English
#    content/insights/trigeminal-neuralgia/index.en.md

# 2. Run process_post to edit + generate BM version
python scripts/process_post.py content/insights/trigeminal-neuralgia/index.en.md

# 3. Review both files before publishing
# 4. Set draft: false when ready
# 5. Deploy
bash scripts/deploy.sh
```

---

## Notes

- The source file is **overwritten** with the edited version — keep a git-tracked draft before running if you want a before/after diff.
- Frontmatter keys (`tags`, `categories`, `date`) are preserved unchanged. Only `title` and `description` values may be refined or translated.
- Medical terms without a professional Bahasa equivalent are kept in English italics with a brief explanation, per the SOP.
- Always review Claude's output before setting `draft: false` — treat it as a first draft.
- Works on any `.en.md` or `.bm.md` file inside `content/` — not limited to `insights/`.
